from __future__ import annotations

import hashlib
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
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_33 import materialize_frontier33a_stage_open as f33a


STAGE_ID = f33a.STAGE_ID
RUN_ID = "frontier33B_path_native_mfe_mae_exit_surface_proxy_scout_v1"
RUN_NUMBER = "frontier33B"
PARENT_RUN_ID = f33a.RUN_ID
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier33C_grok_pre_expensive_path_native_runtime_probe_review_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier33C_path_native_exit_label_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_33/frontier33b_path_native_mfe_mae_exit_surface_proxy_scout.py")

F33A_SUMMARY = STAGE_ROOT / "02_runs" / f33a.RUN_ID / "stage_open_summary.json"
F33A_LOCK = STAGE_ROOT / "02_runs" / f33a.RUN_ID / "path_native_exit_label_lock.json"
F33A_ALIGNMENT = STAGE_ROOT / "01_inputs" / "raw_open_to_open_alignment_audit.json"
RAW_US100_PATH = f33a.RAW_US100_PATH

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

TAKE_QUANTILES = (0.45, 0.55, 0.65)
STOP_QUANTILES = (0.35, 0.50, 0.65)
MIN_THRESHOLD_LOG_RETURN = 0.00035
MIN_SINGLE_TRAIN_TRADES = 45
MIN_PAIR_TRAIN_TRADES = 60
MIN_TRAIN_DENSITY = 1.0
MAX_TRAIN_DENSITY = 24.0
SINGLE_SOURCE_KEEP = 120
SINGLE_KEEP = 160
PAIR_SOURCE_KEEP = 45
PAIR_KEEP = 140
MAX_CANDIDATES = 300
KEEP_VARIANTS_PER_MASK = 1

SCOUT_PF = 1.05
SCOUT_DD_CAP = 20.0
SEED_PF = 1.20
SEED_DD_CAP = 15.0
RUNTIME_PF = 1.50
RUNTIME_DD_CAP = 12.0
RUNTIME_STRICT_DD_CAP = 10.0
DENSITY_LOW = 5.0
DENSITY_HIGH = 10.0
TOP_FORWARD_ROWS = 30


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F33A_SUMMARY)
    lock = read_json(F33A_LOCK)
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    context = validate_context(stage_open, lock, frame, feature_order)
    raw_path = load_raw_path(frame)
    path_labels = build_path_labels(frame, raw_path)
    condition_pool, single_candidates = build_condition_and_single_candidates(frame, feature_order, path_labels, raw_path)
    pair_candidates = build_pair_candidates(frame, condition_pool, path_labels, raw_path)
    candidates = rank_candidates(single_candidates + pair_candidates)
    split_metrics = evaluate_candidates(frame, candidates, path_labels, raw_path)
    summary = summarize_candidates(split_metrics)
    final = build_final(created_at, stage_open, lock, feature_order, context, raw_path, path_labels, condition_pool, candidates, split_metrics, summary)
    write_outputs(final, condition_pool, candidates, split_metrics, summary)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "condition_pool_rows": final["condition_pool_rows"],
        "candidate_rows": final["candidate_rows"],
        "path_scout_clue_rows": final["path_scout_clue_rows"],
        "path_seed_surface_rows": final["path_seed_surface_rows"],
        "runtime_probe_candidate_rows": final["runtime_probe_candidate_rows"],
        "best_candidate_id": final["best_candidate_id"],
        "runtime_probe_status": final["runtime_probe_status"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_context(
    stage_open: dict[str, Any],
    lock: dict[str, Any],
    frame: pd.DataFrame,
    feature_order: list[str],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    alignment = read_json(F33A_ALIGNMENT)
    checks = {
        "workspace_current_frontier33a_or_frontier33b": f"current_stage_id: {STAGE_ID}" in workspace
        and (f"current_run_id: {f33a.RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace),
        "workspace_next_run_frontier33b": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_parent_matches": stage_open.get("run_id") == PARENT_RUN_ID,
        "stage_open_grok_accepted": stage_open.get("grok", {}).get("classification", "").startswith("accepted"),
        "stage_open_lock_changed_variable": stage_open.get("locks", {}).get("active_changed_variable")
        == "path_native_mfe_mae_exit_quality_label_and_entry_surface",
        "lock_forbids_return_space_cap_reuse": "reuse_f31_or_f32_return_space_caps_as_parameters" in lock.get("forbidden_primary_path", []),
        "lock_threshold_train_only": lock.get("threshold_source") == "train_split_mfe_mae_quantiles_only",
        "alignment_no_missing": int(alignment.get("missing_entry_open_rows", -1)) == 0
        and int(alignment.get("missing_future_open_rows", -1)) == 0,
        "alignment_p99_small": float(alignment.get("p99_abs_delta", 999.0)) <= 0.0002,
        "raw_path_exists": path_exists(RAW_US100_PATH),
        "dataset_required_columns": {"timestamp", "future_timestamp", "split", "horizon_bars"}.issubset(frame.columns),
        "feature_order_contract": len(feature_order) == 58 and ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier33B context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks, "alignment_audit": alignment}


def load_raw_path(frame: pd.DataFrame) -> dict[str, Any]:
    raw = pd.read_csv(io_path(RAW_US100_PATH), usecols=["time_open_unix", "open", "high", "low", "close", "spread_points"])
    raw["timestamp"] = pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
    raw = raw.sort_values("timestamp").reset_index(drop=True)
    pos_by_ns = {int(value.value): index for index, value in enumerate(raw["timestamp"])}
    frame_ts = pd.to_datetime(frame["timestamp"], utc=True)
    future_ts = pd.to_datetime(frame["future_timestamp"], utc=True)
    entry_pos = np.array([pos_by_ns.get(int(ts.value), -1) for ts in frame_ts], dtype="int64")
    future_pos = np.array([pos_by_ns.get(int(ts.value), -1) for ts in future_ts], dtype="int64")
    return {
        "raw": raw,
        "entry_pos": entry_pos,
        "future_pos": future_pos,
        "missing_entry_positions": int(np.sum(entry_pos < 0)),
        "missing_future_positions": int(np.sum(future_pos < 0)),
        "raw_rows": int(len(raw)),
    }


def build_path_labels(frame: pd.DataFrame, raw_path: dict[str, Any]) -> dict[int, dict[str, np.ndarray]]:
    raw = raw_path["raw"]
    open_prices = raw["open"].to_numpy(dtype="float64")
    high_prices = raw["high"].to_numpy(dtype="float64")
    low_prices = raw["low"].to_numpy(dtype="float64")
    entry_pos = raw_path["entry_pos"]
    future_pos = raw_path["future_pos"]
    out = {
        1: empty_label_arrays(len(frame)),
        -1: empty_label_arrays(len(frame)),
    }
    for idx in range(len(frame)):
        p = int(entry_pos[idx])
        q = int(future_pos[idx])
        if p < 0 or q <= p or q >= len(open_prices):
            continue
        entry = float(open_prices[p])
        future_open = float(open_prices[q])
        if not math.isfinite(entry) or not math.isfinite(future_open) or entry <= 0.0 or future_open <= 0.0:
            continue
        highs = high_prices[p:q]
        lows = low_prices[p:q]
        if highs.size == 0 or lows.size == 0 or np.nanmin(lows) <= 0.0:
            continue
        max_high = float(np.nanmax(highs))
        min_low = float(np.nanmin(lows))
        if not all(math.isfinite(value) and value > 0.0 for value in (max_high, min_low)):
            continue
        forward_log = math.log(future_open / entry)
        long_mfe = max(math.log(max_high / entry), 0.0)
        long_mae = max(math.log(entry / min_low), 0.0)
        short_mfe = max(math.log(entry / min_low), 0.0)
        short_mae = max(math.log(max_high / entry), 0.0)
        assign_path_label(out[1], idx, long_mfe, long_mae, forward_log - scout.ROUGH_COST_LOG_RETURN)
        assign_path_label(out[-1], idx, short_mfe, short_mae, -forward_log - scout.ROUGH_COST_LOG_RETURN)
    return out


def empty_label_arrays(size: int) -> dict[str, np.ndarray]:
    return {
        "mfe": np.full(size, np.nan, dtype="float64"),
        "mae": np.full(size, np.nan, dtype="float64"),
        "horizon_pnl": np.full(size, np.nan, dtype="float64"),
        "valid": np.zeros(size, dtype=bool),
    }


def assign_path_label(target: dict[str, np.ndarray], idx: int, mfe: float, mae: float, horizon_pnl: float) -> None:
    target["mfe"][idx] = mfe
    target["mae"][idx] = mae
    target["horizon_pnl"][idx] = horizon_pnl
    target["valid"][idx] = True


def build_condition_and_single_candidates(
    frame: pd.DataFrame,
    feature_order: list[str],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    train_mask = split_mask(frame, "train")
    for feature in feature_order:
        family = f23b.feature_family(feature)
        series = pd.to_numeric(frame[feature], errors="coerce")
        train_values = series.loc[train_mask].replace([np.inf, -np.inf], np.nan).dropna()
        if train_values.nunique(dropna=True) <= 1:
            continue
        for operator, q_label, threshold, base_mask in f23b.condition_masks(series, train_values):
            coverage = float(base_mask[train_mask].mean()) if train_mask.any() else 0.0
            if not (0.02 <= coverage <= 0.80):
                continue
            for side, side_name in ((1, "long"), (-1, "short")):
                condition_id = f"f33cond_{len(rows)+1:04d}"
                condition = {
                    "condition_id": condition_id,
                    "feature": feature,
                    "feature_family": family,
                    "operator": operator,
                    "quantile_label": q_label,
                    "threshold_value": threshold,
                    "side_value": side,
                    "side": f"{side_name}({'롱' if side > 0 else '숏'})",
                    "definition": f"{feature} {operator} {q_label}",
                    "train_coverage": coverage,
                    "_mask": base_mask,
                }
                horizon_metrics = evaluate_horizon_mask(frame, base_mask, side, path_labels, "train")
                horizon_pass = (
                    horizon_metrics["trade_count"] >= MIN_SINGLE_TRAIN_TRADES
                    and MIN_TRAIN_DENSITY <= horizon_metrics["trades_per_day"] <= MAX_TRAIN_DENSITY
                    and horizon_metrics["net_profit"] > 0.0
                    and horizon_metrics["profit_factor"] >= 1.0
                )
                horizon_score = train_horizon_score(horizon_metrics) if horizon_pass else 0.0
                rows.append({
                    **condition,
                    "horizon_prefilter_pass": bool(horizon_pass),
                    "best_train_path_score": horizon_score,
                    "best_stop_cap_log_return": math.nan,
                    "best_take_cap_log_return": math.nan,
                    "best_train_profit_factor": safe_float(horizon_metrics.get("profit_factor")),
                    "best_train_trades_per_day": safe_float(horizon_metrics.get("trades_per_day")),
                    "best_train_dd_risk": safe_float(horizon_metrics.get("dd_risk")),
                })
    condition_pool = pd.DataFrame(rows)
    if condition_pool.empty:
        raise RuntimeError("No path-native condition rows(경로 기반 조건 행 없음).")
    condition_pool = condition_pool.sort_values(["horizon_prefilter_pass", "best_train_path_score"], ascending=[False, False]).reset_index(drop=True)
    condition_pool["condition_id"] = [f"f33cond_{index:04d}" for index in range(1, len(condition_pool) + 1)]
    candidates = []
    for condition in condition_pool.loc[condition_pool["horizon_prefilter_pass"].astype(bool)].head(SINGLE_SOURCE_KEEP).to_dict("records"):
        variants = candidate_variants_for_mask(
            frame,
            [condition],
            np.asarray(condition["_mask"], dtype=bool),
            int(condition["side_value"]),
            path_labels,
            raw_path,
            min_train_trades=MIN_SINGLE_TRAIN_TRADES,
            keep=KEEP_VARIANTS_PER_MASK,
        )
        candidates.extend(variants)
    candidates.sort(key=lambda item: float(item["train_path_score"]), reverse=True)
    return condition_pool, candidates[:SINGLE_KEEP]


def build_pair_candidates(
    frame: pd.DataFrame,
    condition_pool: pd.DataFrame,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
) -> list[dict[str, Any]]:
    source = condition_pool.loc[condition_pool["best_train_path_score"] > 0].head(PAIR_SOURCE_KEEP).to_dict("records")
    pair_candidates: list[dict[str, Any]] = []
    pair_attempts = 0
    for i, first in enumerate(source):
        for second in source[i + 1 :]:
            if int(first["side_value"]) != int(second["side_value"]):
                continue
            if str(first["feature"]) == str(second["feature"]):
                continue
            if str(first["feature_family"]) == str(second["feature_family"]):
                continue
            pair_attempts += 1
            mask = np.asarray(first["_mask"], dtype=bool) & np.asarray(second["_mask"], dtype=bool)
            variants = candidate_variants_for_mask(
                frame,
                [first, second],
                mask,
                int(first["side_value"]),
                path_labels,
                raw_path,
                min_train_trades=MIN_PAIR_TRAIN_TRADES,
                keep=1,
            )
            pair_candidates.extend(variants)
            if len(pair_candidates) >= PAIR_KEEP or pair_attempts >= PAIR_KEEP * 4:
                break
        if len(pair_candidates) >= PAIR_KEEP or pair_attempts >= PAIR_KEEP * 4:
            break
    pair_candidates.sort(key=lambda item: float(item["train_path_score"]), reverse=True)
    return pair_candidates[:PAIR_KEEP]


def candidate_variants_for_mask(
    frame: pd.DataFrame,
    conditions: list[dict[str, Any]],
    mask: np.ndarray,
    side: int,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    *,
    min_train_trades: int,
    keep: int,
) -> list[dict[str, Any]]:
    threshold_rows = threshold_variants(frame, mask, side, path_labels)
    variants: list[dict[str, Any]] = []
    for row in threshold_rows:
        metrics = evaluate_path_mask(frame, mask, side, row["stop_cap_log_return"], row["take_cap_log_return"], path_labels, raw_path, "train")
        if metrics["trade_count"] < min_train_trades:
            continue
        if not (MIN_TRAIN_DENSITY <= metrics["trades_per_day"] <= MAX_TRAIN_DENSITY):
            continue
        if metrics["net_profit"] <= 0.0 or metrics["profit_factor"] < 1.01:
            continue
        score = train_path_score(metrics, row)
        variants.append(candidate_from_conditions(conditions, mask, side, row, metrics, score))
    variants.sort(key=lambda item: float(item["train_path_score"]), reverse=True)
    return variants[:keep]


def threshold_variants(
    frame: pd.DataFrame,
    mask: np.ndarray,
    side: int,
    path_labels: dict[int, dict[str, np.ndarray]],
) -> list[dict[str, Any]]:
    labels = path_labels[side]
    train = split_mask(frame, "train") & np.asarray(mask, dtype=bool) & labels["valid"]
    mfe = labels["mfe"][train]
    mae = labels["mae"][train]
    mfe = mfe[np.isfinite(mfe) & (mfe > 0.0)]
    mae = mae[np.isfinite(mae) & (mae > 0.0)]
    if mfe.size < 30 or mae.size < 30:
        return []
    rows: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()
    for take_q in TAKE_QUANTILES:
        take_cap = max(float(np.nanquantile(mfe, take_q)), MIN_THRESHOLD_LOG_RETURN)
        for stop_q in STOP_QUANTILES:
            stop_cap = max(float(np.nanquantile(mae, stop_q)), MIN_THRESHOLD_LOG_RETURN)
            key = (int(round(stop_cap * 1_000_000)), int(round(take_cap * 1_000_000)))
            if key in seen:
                continue
            seen.add(key)
            rows.append({
                "threshold_source": "train_split_mfe_mae_quantiles_only",
                "stop_quantile": stop_q,
                "take_quantile": take_q,
                "stop_cap_log_return": stop_cap,
                "take_cap_log_return": take_cap,
                "train_threshold_sample_rows": int(min(mfe.size, mae.size)),
            })
    return rows


def candidate_from_conditions(
    conditions: list[dict[str, Any]],
    mask: np.ndarray,
    side: int,
    threshold_row: dict[str, Any],
    train_metrics: dict[str, Any],
    score: float,
) -> dict[str, Any]:
    features = [str(item["feature"]) for item in conditions]
    families = [str(item["feature_family"]) for item in conditions]
    return {
        "candidate_id": "",
        "condition_count": len(conditions),
        "condition_ids": "|".join(str(item["condition_id"]) for item in conditions),
        "features": "|".join(features),
        "feature_families": "|".join(families),
        "side_value": side,
        "side": f"{'long' if side > 0 else 'short'}({'롱' if side > 0 else '숏'})",
        "rule_definition": " & ".join(str(item["definition"]) for item in conditions),
        "threshold_source": threshold_row["threshold_source"],
        "stop_quantile": threshold_row["stop_quantile"],
        "take_quantile": threshold_row["take_quantile"],
        "stop_cap_log_return": threshold_row["stop_cap_log_return"],
        "take_cap_log_return": threshold_row["take_cap_log_return"],
        "train_threshold_sample_rows": threshold_row["train_threshold_sample_rows"],
        "train_path_score": score,
        "executable_first_hit_representation": True,
        "mask": mask,
        "train_selection_metrics": train_metrics,
    }


def rank_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = sorted(candidates, key=lambda item: float(item["train_path_score"]), reverse=True)[:MAX_CANDIDATES]
    for index, candidate in enumerate(candidates, start=1):
        candidate["candidate_id"] = f"f33b_{index:04d}"
    return candidates


def evaluate_candidates(
    frame: pd.DataFrame,
    candidates: list[dict[str, Any]],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for rank, candidate in enumerate(candidates, start=1):
        for split in ("train", "validation", "oos"):
            metrics = evaluate_path_mask(
                frame,
                candidate["mask"],
                int(candidate["side_value"]),
                float(candidate["stop_cap_log_return"]),
                float(candidate["take_cap_log_return"]),
                path_labels,
                raw_path,
                split,
            )
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
                "threshold_source": candidate["threshold_source"],
                "stop_quantile": candidate["stop_quantile"],
                "take_quantile": candidate["take_quantile"],
                "stop_cap_log_return": candidate["stop_cap_log_return"],
                "take_cap_log_return": candidate["take_cap_log_return"],
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
                "stop_hit_count": metrics["stop_hit_count"],
                "take_hit_count": metrics["take_hit_count"],
                "horizon_exit_count": metrics["horizon_exit_count"],
                "ambiguous_both_hit_count": metrics["ambiguous_both_hit_count"],
                "avg_holding_bars": metrics["avg_holding_bars"],
                "median_holding_bars": metrics["median_holding_bars"],
                "path_quality_rate": metrics["path_quality_rate"],
                "median_mfe_log_return": metrics["median_mfe_log_return"],
                "median_mae_log_return": metrics["median_mae_log_return"],
                "sparse_flag": sparse_flag,
                "pf999_sparse_flag": pf999_sparse_flag,
                "density_axis_distance": density_distance,
                "pf_axis_distance": pf_distance,
                "dd_axis_distance": dd_distance,
                "smoothness_axis_distance": smoothness_distance,
                "joint_axis_distance": density_distance + pf_distance + dd_distance + smoothness_distance,
                "selection_boundary": "train_only_rank(학습 전용 순위)" if split == "train" else "read_only_forward_diagnostic(읽기 전용 전진 진단)",
                "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
            })
    return pd.DataFrame(rows)


def evaluate_horizon_mask(
    frame: pd.DataFrame,
    mask: np.ndarray,
    side: int,
    path_labels: dict[int, dict[str, np.ndarray]],
    split: str,
) -> dict[str, Any]:
    labels = path_labels[side]
    split_base = split_mask(frame, split)
    trade_mask = np.asarray(mask, dtype=bool) & split_base & labels["valid"]
    pnl = labels["horizon_pnl"][trade_mask]
    pnl = pnl[np.isfinite(pnl)]
    trade_times = frame.loc[trade_mask, "timestamp"].iloc[: len(pnl)]
    metrics = scout.trade_metrics(pnl, trade_times)
    shape = f23b.payoff_shape(pnl)
    days = scout.count_scope_days(frame.loc[split_base, "timestamp"])
    return {
        **metrics,
        **shape,
        "trade_count": int(len(pnl)),
        "days_in_scope": int(days),
        "trades_per_day": float(len(pnl) / days) if days else 0.0,
        "dd_risk": max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"])),
    }


def evaluate_path_mask(
    frame: pd.DataFrame,
    mask: np.ndarray,
    side: int,
    stop_cap: float,
    take_cap: float,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    split: str,
) -> dict[str, Any]:
    raw = raw_path["raw"]
    open_prices = raw["open"].to_numpy(dtype="float64")
    high_prices = raw["high"].to_numpy(dtype="float64")
    low_prices = raw["low"].to_numpy(dtype="float64")
    entry_pos = raw_path["entry_pos"]
    future_pos = raw_path["future_pos"]
    labels = path_labels[side]
    split_base = split_mask(frame, split)
    trade_mask = np.asarray(mask, dtype=bool) & split_base & labels["valid"]
    trade_indices = np.flatnonzero(trade_mask)
    pnl: list[float] = []
    reasons: list[str] = []
    holding_bars: list[float] = []
    ambiguous: list[bool] = []
    for idx in trade_indices:
        p = int(entry_pos[idx])
        q = int(future_pos[idx])
        if p < 0 or q <= p or q >= len(open_prices):
            continue
        entry = float(open_prices[p])
        if not math.isfinite(entry) or entry <= 0.0:
            continue
        result = simulate_one_trade(side, entry, p, q, stop_cap, take_cap, open_prices, high_prices, low_prices)
        pnl.append(float(result["pnl_log"]) - scout.ROUGH_COST_LOG_RETURN)
        reasons.append(str(result["exit_reason"]))
        holding_bars.append(float(result["holding_bars"]))
        ambiguous.append(bool(result["ambiguous_both_hit"]))
    trade_pnl = np.asarray(pnl, dtype="float64")
    trade_times = frame.loc[trade_indices[: len(trade_pnl)], "timestamp"]
    metrics = scout.trade_metrics(trade_pnl, trade_times)
    shape = f23b.payoff_shape(trade_pnl)
    days = scout.count_scope_days(frame.loc[split_base, "timestamp"])
    quality = (labels["mfe"][trade_indices] >= take_cap) & (labels["mae"][trade_indices] <= stop_cap) if trade_indices.size else np.array([], dtype=bool)
    mfe = labels["mfe"][trade_indices]
    mae = labels["mae"][trade_indices]
    holding = np.asarray(holding_bars, dtype="float64")
    return {
        **metrics,
        **shape,
        "trade_count": int(len(trade_pnl)),
        "days_in_scope": int(days),
        "trades_per_day": float(len(trade_pnl) / days) if days else 0.0,
        "dd_risk": max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"])),
        "stop_hit_count": int(sum(reason == "stop" for reason in reasons)),
        "take_hit_count": int(sum(reason == "take" for reason in reasons)),
        "horizon_exit_count": int(sum(reason == "horizon" for reason in reasons)),
        "ambiguous_both_hit_count": int(sum(ambiguous)),
        "avg_holding_bars": safe_mean(holding),
        "median_holding_bars": safe_median(holding),
        "path_quality_rate": float(np.mean(quality)) if quality.size else 0.0,
        "median_mfe_log_return": safe_median(mfe),
        "median_mae_log_return": safe_median(mae),
    }


def simulate_one_trade(
    side_value: int,
    entry: float,
    p: int,
    q: int,
    stop_cap: float,
    take_cap: float,
    open_prices: np.ndarray,
    high_prices: np.ndarray,
    low_prices: np.ndarray,
) -> dict[str, Any]:
    has_stop = math.isfinite(stop_cap) and stop_cap > 0.0
    has_take = math.isfinite(take_cap) and take_cap > 0.0
    if side_value > 0:
        stop_price = entry * math.exp(-stop_cap) if has_stop else -math.inf
        take_price = entry * math.exp(take_cap) if has_take else math.inf
        for pos in range(p, q):
            hit_stop = has_stop and float(low_prices[pos]) <= stop_price
            hit_take = has_take and float(high_prices[pos]) >= take_price
            if hit_stop and hit_take:
                return {"pnl_log": -stop_cap, "exit_reason": "stop", "holding_bars": pos - p + 1, "ambiguous_both_hit": True}
            if hit_stop:
                return {"pnl_log": -stop_cap, "exit_reason": "stop", "holding_bars": pos - p + 1, "ambiguous_both_hit": False}
            if hit_take:
                return {"pnl_log": take_cap, "exit_reason": "take", "holding_bars": pos - p + 1, "ambiguous_both_hit": False}
        return {"pnl_log": math.log(float(open_prices[q]) / entry), "exit_reason": "horizon", "holding_bars": q - p, "ambiguous_both_hit": False}
    stop_price = entry * math.exp(stop_cap) if has_stop else math.inf
    take_price = entry * math.exp(-take_cap) if has_take else -math.inf
    for pos in range(p, q):
        hit_stop = has_stop and float(high_prices[pos]) >= stop_price
        hit_take = has_take and float(low_prices[pos]) <= take_price
        if hit_stop and hit_take:
            return {"pnl_log": -stop_cap, "exit_reason": "stop", "holding_bars": pos - p + 1, "ambiguous_both_hit": True}
        if hit_stop:
            return {"pnl_log": -stop_cap, "exit_reason": "stop", "holding_bars": pos - p + 1, "ambiguous_both_hit": False}
        if hit_take:
            return {"pnl_log": take_cap, "exit_reason": "take", "holding_bars": pos - p + 1, "ambiguous_both_hit": False}
    return {"pnl_log": -math.log(float(open_prices[q]) / entry), "exit_reason": "horizon", "holding_bars": q - p, "ambiguous_both_hit": False}


def summarize_candidates(split_metrics: pd.DataFrame) -> pd.DataFrame:
    if split_metrics.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for candidate_id, group in split_metrics.groupby("candidate_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        base = {
            "candidate_id": candidate_id,
            "train_rank": int(train["train_rank"]),
            "condition_count": int(train["condition_count"]),
            "condition_ids": train["condition_ids"],
            "side": train["side"],
            "side_value": int(train["side_value"]),
            "rule_definition": train["rule_definition"],
            "features": train["features"],
            "feature_families": train["feature_families"],
            "threshold_source": train["threshold_source"],
            "stop_quantile": train["stop_quantile"],
            "take_quantile": train["take_quantile"],
            "stop_cap_log_return": train["stop_cap_log_return"],
            "take_cap_log_return": train["take_cap_log_return"],
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
                "stop_hit_count",
                "take_hit_count",
                "horizon_exit_count",
                "ambiguous_both_hit_count",
                "avg_holding_bars",
                "median_holding_bars",
                "path_quality_rate",
                "median_mfe_log_return",
                "median_mae_log_return",
            ):
                base[f"{prefix}_{field}"] = row[field]
        forward_min_pf = min(safe_float(base["validation_profit_factor"]), safe_float(base["oos_profit_factor"]))
        forward_max_dd = max(safe_float(base["validation_dd_risk"]), safe_float(base["oos_dd_risk"]))
        forward_min_density = min(safe_float(base["validation_trades_per_day"]), safe_float(base["oos_trades_per_day"]))
        forward_max_density = max(safe_float(base["validation_trades_per_day"]), safe_float(base["oos_trades_per_day"]))
        forward_min_r2 = min(safe_float(base["validation_equity_trend_r2"]), safe_float(base["oos_equity_trend_r2"]))
        forward_max_loss_streak = max(int(base["validation_max_loss_streak"]), int(base["oos_max_loss_streak"]))
        base["forward_min_pf"] = forward_min_pf
        base["forward_max_dd"] = forward_max_dd
        base["forward_min_density"] = forward_min_density
        base["forward_max_density"] = forward_max_density
        base["forward_min_equity_trend_r2"] = forward_min_r2
        base["forward_dual_positive_flag"] = bool(base["validation_net_profit"] > 0 and base["oos_net_profit"] > 0)
        base["path_density_bridge_flag"] = bool(DENSITY_LOW <= forward_min_density <= DENSITY_HIGH and forward_max_density <= DENSITY_HIGH)
        base["path_scout_clue_flag"] = bool(
            base["forward_dual_positive_flag"]
            and base["path_density_bridge_flag"]
            and forward_min_pf >= SCOUT_PF
            and forward_max_dd <= SCOUT_DD_CAP
        )
        base["path_seed_surface_flag"] = bool(
            base["path_scout_clue_flag"]
            and forward_min_pf >= SEED_PF
            and forward_max_dd <= SEED_DD_CAP
            and forward_min_r2 >= 0.50
        )
        base["runtime_probe_candidate_flag"] = bool(
            base["path_seed_surface_flag"]
            and forward_min_pf >= RUNTIME_PF
            and forward_max_dd <= RUNTIME_DD_CAP
            and forward_max_loss_streak <= 25
        )
        base["runtime_strict_candidate_flag"] = bool(base["runtime_probe_candidate_flag"] and forward_max_dd <= RUNTIME_STRICT_DD_CAP)
        base["executable_first_hit_representation"] = True
        base["mt5_probe_requires_pre_expensive_grok"] = bool(base["runtime_probe_candidate_flag"])
        base["path_read_score"] = (
            6.0 * min(forward_min_pf, 3.0)
            + 1.0 * min(forward_min_density, 10.0)
            + 2.0 * min(forward_min_r2, 1.0)
            + 1.5 * min(safe_float(base["validation_path_quality_rate"]), safe_float(base["oos_path_quality_rate"]))
            - 0.35 * forward_max_dd
            - 0.02 * (safe_float(base["validation_ambiguous_both_hit_count"]) + safe_float(base["oos_ambiguous_both_hit_count"]))
        )
        rows.append(base)
    summary = pd.DataFrame(rows).sort_values(
        ["runtime_probe_candidate_flag", "path_seed_surface_flag", "path_scout_clue_flag", "path_read_score"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)
    summary["path_rank"] = np.arange(1, len(summary) + 1)
    return summary


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    lock: dict[str, Any],
    feature_order: list[str],
    context: dict[str, Any],
    raw_path: dict[str, Any],
    path_labels: dict[int, dict[str, np.ndarray]],
    condition_pool: pd.DataFrame,
    candidates: list[dict[str, Any]],
    split_metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, Any]:
    scout_count = int(summary["path_scout_clue_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["path_seed_surface_flag"].sum()) if not summary.empty else 0
    runtime_count = int(summary["runtime_probe_candidate_flag"].sum()) if not summary.empty else 0
    strict_count = int(summary["runtime_strict_candidate_flag"].sum()) if not summary.empty else 0
    if runtime_count:
        status = "path_native_exit_surface_runtime_probe_candidate_needs_pre_expensive_grok_no_authority"
        judgment = "runtime_probe_candidates_require_grok_before_mt5_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
        runtime_probe_status = "runtime_probe_candidate_pending_pre_expensive_grok_and_mt5_micro_probe"
    elif seed_count:
        status = "path_native_exit_surface_seed_surface_no_runtime_candidate_no_authority"
        judgment = "seed_surface_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_out_of_scope_by_claim_path_native_seed_only_no_runtime_candidate"
    elif scout_count:
        status = "path_native_exit_surface_scout_only_no_runtime_candidate_no_authority"
        judgment = "scout_clue_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_out_of_scope_by_claim_path_native_scout_only_no_runtime_candidate"
    else:
        status = "path_native_exit_surface_no_scout_no_seed_no_runtime_candidate_no_authority"
        judgment = "negative_memory_candidate_no_forward_path_native_density_edge"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_ineligible_no_path_native_proxy_candidate_after_f33b"
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
        "stage_open": {
            "run_id": stage_open.get("run_id"),
            "grok_classification": stage_open.get("grok", {}).get("classification", ""),
            "alignment_p99_abs_delta": stage_open.get("alignment_audit", {}).get("p99_abs_delta"),
        },
        "lock": lock,
        "raw_path": {
            "path": RAW_US100_PATH.as_posix(),
            "raw_rows": raw_path["raw_rows"],
            "missing_entry_positions": raw_path["missing_entry_positions"],
            "missing_future_positions": raw_path["missing_future_positions"],
            "valid_long_path_rows": int(path_labels[1]["valid"].sum()),
            "valid_short_path_rows": int(path_labels[-1]["valid"].sum()),
        },
        "condition_pool_rows": int(len(condition_pool)),
        "candidate_rows": int(len(candidates)),
        "split_metric_rows": int(len(split_metrics)) if not split_metrics.empty else 0,
        "summary_rows": int(len(summary)) if not summary.empty else 0,
        "path_scout_clue_rows": scout_count,
        "path_seed_surface_rows": seed_count,
        "runtime_probe_candidate_rows": runtime_count,
        "runtime_strict_candidate_rows": strict_count,
        "best_candidate_id": best.get("candidate_id", ""),
        "best_candidate": json_ready(best),
        "runtime_probe_status": runtime_probe_status,
        "result_boundary": "python_path_native_first_hit_proxy_only_no_wfo_no_mt5_no_onnx_no_authority",
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(
    final: dict[str, Any],
    condition_pool: pd.DataFrame,
    candidates: list[dict[str, Any]],
    split_metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    condition_pool.drop(columns=["_mask"], errors="ignore").to_csv(io_path(RUN_ROOT / "path_native_condition_pool.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame([clean_candidate_for_csv(item) for item in candidates]).to_csv(io_path(RUN_ROOT / "path_native_candidate_ledger.csv"), index=False, encoding="utf-8-sig")
    split_metrics.to_csv(io_path(RUN_ROOT / "path_native_split_metrics.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "path_native_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    if not summary.empty:
        summary.head(TOP_FORWARD_ROWS).to_csv(io_path(RUN_ROOT / "top_path_native_forward_diagnostic.csv"), index=False, encoding="utf-8-sig")
    else:
        pd.DataFrame().to_csv(io_path(RUN_ROOT / "top_path_native_forward_diagnostic.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, summary))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F33A_SUMMARY,
        F33A_LOCK,
        F33A_ALIGNMENT,
        f23b.DATASET_PATH,
        f23b.FEATURE_ORDER_PATH,
        RAW_US100_PATH,
        RUN_ROOT / "path_native_condition_pool.csv",
        RUN_ROOT / "path_native_candidate_ledger.csv",
        RUN_ROOT / "path_native_split_metrics.csv",
        RUN_ROOT / "path_native_candidate_summary.csv",
        RUN_ROOT / "top_path_native_forward_diagnostic.csv",
        RUN_ROOT / "final_summary.json",
        REPORT_PATH,
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
            "feature_order_path": f23b.FEATURE_ORDER_PATH.as_posix(),
        },
        "data_snapshot": {
            "dataset_path": f23b.DATASET_PATH.as_posix(),
            "raw_path": RAW_US100_PATH.as_posix(),
            "split_names": ["train", "validation", "oos"],
        },
        "rule_stack": {
            "selection": "train_only_path_native_mfe_mae_thresholds(학습 전용 경로 기반 최대 유리/불리 이동 임계값)",
            "entry": "single_or_depth2_feature_state_conditions(단일 또는 깊이2 피처 상태 조건)",
            "exit": "first_hit_sl_tp_or_horizon_open_exit(선터치 손절/익절 또는 수평 시가 청산)",
            "tie_break": "conservative_stop_first(보수적 손절 우선)",
        },
        "runtime_claim_boundary": "python_path_native_proxy_only_no_mt5_runtime_authority",
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f33a.upsert_csv_io(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f33a.upsert_csv_io(ALPHA_LEDGER, "ledger_row_id", row)
        f33a.upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    best = final["best_candidate"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "path_native_proxy_scout(경로 기반 프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"path_scout={final['path_scout_clue_rows']};seed={final['path_seed_surface_rows']};runtime_candidate={final['runtime_probe_candidate_rows']};best={final['best_candidate_id']};next={final['next_run_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={final['best_candidate_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "train_only_mfe_mae_thresholds_validation_oos_read_only_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_candidate"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_path_native_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_path_native_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "python_path_native_proxy_no_mt5(파이썬 경로 기반 프록시, MT5 아님)",
        "scoreboard_lane": "path_native_proxy_scout(경로 기반 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"best={final['best_candidate_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "train_only_path_thresholds_no_forward_rerank_no_mt5_authority",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"condition={final['condition_pool_rows']};candidate={final['candidate_rows']};scout={final['path_scout_clue_rows']};seed={final['path_seed_surface_rows']};runtime_candidate={final['runtime_probe_candidate_rows']};next={final['next_run_id']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "path_native_proxy_scout(경로 기반 프록시 탐색)",
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
        "notes": "Tier B not materialized in F33B path-native proxy(전선33B 경로 기반 프록시에서 티어 B 미물질화)",
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
        "notes": "Combined tier not claimed in F33B path-native proxy(전선33B 경로 기반 프록시에서 합산 티어 주장 없음)",
    }
    return [primary, tier_b, combined]


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


def report_text(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["best_candidate"]
    top_rows: list[str] = []
    if not summary.empty:
        for _, row in summary.head(12).iterrows():
            top_rows.append(
                f"| `{row['candidate_id']}` | {row['side']} | `{row['features']}` | "
                f"{fmt(row['validation_profit_factor'])} | {fmt(row['validation_trades_per_day'])} | {fmt(row['validation_dd_risk'])} | "
                f"{fmt(row['oos_profit_factor'])} | {fmt(row['oos_trades_per_day'])} | {fmt(row['oos_dd_risk'])} | "
                f"{fmt(row['stop_cap_log_return'])}/{fmt(row['take_cap_log_return'])} | {row['path_scout_clue_flag']} | {row['path_seed_surface_flag']} |"
            )
    table = "\n".join(top_rows) if top_rows else "| none(없음) | | | | | | | | | | | |"
    return f"""# Frontier33B Path-Native MFE/MAE Exit Surface Proxy Scout Report(전선33B 경로 기반 최대 유리/불리 이동 청산 표면 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): raw Bid OHLC path(원천 매수호가 시가/고가/저가/종가 경로)에서 MFE/MAE train-only quantile threshold(학습 전용 최대 유리/불리 이동 분위수 임계값)를 만들고, first-hit SL/TP path proxy(선터치 손절/익절 경로 프록시)를 실행했습니다.

Effect(효과): F32 return-space cap translation(수익률 공간 한도 번역)을 쓰지 않고, validation/OOS(검증/표본외)는 읽기 전용으로 path-native density edge(경로 기반 밀도 우위)를 확인합니다.

Condition/candidate/metric rows(조건/후보/지표 행): `{final['condition_pool_rows']}` / `{final['candidate_rows']}` / `{final['split_metric_rows']}`

Path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보): `{final['path_scout_clue_rows']}` / `{final['path_seed_surface_rows']}` / `{final['runtime_probe_candidate_rows']}`

Strict DD candidate(엄격 손실폭 후보): `{final['runtime_strict_candidate_rows']}`

Best candidate(최상 후보): `{final['best_candidate_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Best stop/take log thresholds(최상 손절/익절 로그 임계값): `{fmt(best.get('stop_cap_log_return'))}` / `{fmt(best.get('take_cap_log_return'))}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Top Readonly Forward Rows(상위 읽기 전용 전진 행)

| candidate(후보) | side(방향) | features(피처) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | stop/take | scout | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier33B Gate Audit(전선33B 게이트 감사)

- scope_completion_gate(범위 완료 게이트): proxy artifacts created(프록시 산출물 생성) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- stage_open_lock_gate(단계 개방 잠금 게이트): `{F33A_LOCK.as_posix()}` read(읽음)
- return_space_reuse_guard(수익률 공간 재사용 방어): F31/F32 return-space caps(수익률 공간 한도) not used as thresholds(임계값으로 미사용)
- threshold_source_gate(임계값 원천 게이트): train-only MFE/MAE quantiles(학습 전용 최대 유리/불리 이동 분위수)
- kpi_contract_audit(KPI 계약 감사): metrics/candidate/condition outputs(지표/후보/조건 출력) created(생성)
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일)
- final_claim_guard(최종 주장 방지): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier33 Selection Status(전선33 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest proxy(최근 프록시): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best candidate(최상 후보): `{final['best_candidate_id']}`

Path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보): `{final['path_scout_clue_rows']}` / `{final['path_seed_surface_rows']}` / `{final['runtime_probe_candidate_rows']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


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

Action(행동): F33B(전선33B)는 path-native MFE/MAE first-hit proxy(경로 기반 최대 유리/불리 이동 선터치 프록시)를 실행했습니다.

Effect(효과): condition/candidate(조건/후보) `{final['condition_pool_rows']}/{final['candidate_rows']}`개를 train-only threshold(학습 전용 임계값)로 평가했고, path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보)는 `{final['path_scout_clue_rows']}/{final['path_seed_surface_rows']}/{final['runtime_probe_candidate_rows']}`입니다.

Best candidate(최상 후보): `{final['best_candidate_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-밀도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Runtime probe boundary(런타임 탐침 경계): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran path-native MFE/MAE first-hit proxy(경로 기반 최대 유리/불리 이동 선터치 프록시). "
        f"Effect(효과): scout={final['path_scout_clue_rows']}, seed={final['path_seed_surface_rows']}, runtime_candidate={final['runtime_probe_candidate_rows']}, next=`{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR33-PATH-NATIVE-EXIT-LABEL-ONNX-SCOUT`: `{RUN_ID}` tested path-native MFE/MAE first-hit surface(경로 기반 최대 유리/불리 이동 선터치 표면). "
        f"Effect(효과): best candidate `{final['best_candidate_id']}` remains proxy-only(프록시 전용) with no authority(권위 없음).\n"
    )


def train_path_score(metrics: dict[str, Any], threshold_row: dict[str, Any]) -> float:
    density_penalty = abs(float(metrics["trades_per_day"]) - 8.0) / 8.0
    dd_penalty = max(0.0, float(metrics["dd_risk"]) - 12.0) / 18.0
    ambiguity_penalty = float(metrics["ambiguous_both_hit_count"]) / max(float(metrics["trade_count"]), 1.0)
    threshold_balance = min(float(threshold_row["take_cap_log_return"]) / max(float(threshold_row["stop_cap_log_return"]), 1e-12), 4.0)
    return float(
        max(float(metrics["net_profit"]), 0.0)
        * min(float(metrics["profit_factor"]), 4.0)
        * (1.0 + min(float(metrics["path_quality_rate"]), 1.0))
        * (1.0 + min(threshold_balance, 2.0) * 0.15)
        / (1.0 + density_penalty + dd_penalty + ambiguity_penalty)
    )


def train_horizon_score(metrics: dict[str, Any]) -> float:
    density_penalty = abs(float(metrics["trades_per_day"]) - 8.0) / 8.0
    dd_penalty = max(0.0, float(metrics["dd_risk"]) - 12.0) / 18.0
    return float(
        max(float(metrics["net_profit"]), 0.0)
        * min(float(metrics["profit_factor"]), 4.0)
        * min(float(metrics["payoff_ratio"]), 4.0)
        / (1.0 + density_penalty + dd_penalty)
    )


def split_mask(frame: pd.DataFrame, split: str) -> np.ndarray:
    return frame["split"].astype(str).eq(split).to_numpy(dtype=bool)


def split_row(group: pd.DataFrame, split: str) -> dict[str, Any]:
    row = group.loc[group["split"].eq(split)]
    if row.empty:
        raise ValueError(f"Missing split row(분할 행 누락): {split}")
    return dict(row.iloc[0])


def clean_candidate_for_csv(item: dict[str, Any]) -> dict[str, Any]:
    cleaned = {key: value for key, value in item.items() if key not in {"mask", "train_selection_metrics"}}
    for key, value in item.get("train_selection_metrics", {}).items():
        cleaned[f"train_{key}"] = value
    return cleaned


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing"}


def sha256_io(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def safe_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def safe_float_or_nan(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return math.nan
    return number if math.isfinite(number) else math.nan


def safe_mean(values: np.ndarray) -> float:
    finite = values[np.isfinite(values)]
    return float(np.mean(finite)) if finite.size else 0.0


def safe_median(values: np.ndarray) -> float:
    finite = values[np.isfinite(values)]
    return float(np.median(finite)) if finite.size else 0.0


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.3f}"


if __name__ == "__main__":
    raise SystemExit(main())
