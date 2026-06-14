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
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_28 import frontier28b_train_only_stability_gap_proxy_scout as f28b
from stage_pipelines.stage_frontier_32 import materialize_frontier32a_stage_open as f32a


STAGE_ID = f32a.STAGE_ID
RUN_ID = "frontier32B_executable_sl_tp_path_proxy_scout_v1"
RUN_NUMBER = "frontier32B"
PARENT_RUN_ID = f32a.RUN_ID
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier32C_grok_pre_expensive_executable_sl_tp_runtime_probe_review_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier32C_executable_sl_tp_mapping_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_32/frontier32b_executable_sl_tp_path_proxy_scout.py")

F32A_SUMMARY = STAGE_ROOT / "02_runs" / f32a.RUN_ID / "stage_open_summary.json"
F32A_QUEUE = STAGE_ROOT / "01_inputs" / "f31_executable_mapping_queue.csv"
F32A_TOP_QUEUE = STAGE_ROOT / "01_inputs" / "f31_top_executable_mapping_queue.csv"
F32A_ALIGNMENT = STAGE_ROOT / "01_inputs" / "raw_open_to_open_alignment_audit.json"
RAW_US100_PATH = f32a.RAW_US100_PATH

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

SCOUT_PF = 1.05
SCOUT_DD_CAP = 20.0
SEED_PF = 1.20
SEED_DD_CAP = 15.0
RUNTIME_PF = 1.50
RUNTIME_DD_CAP = 12.0
RUNTIME_STRICT_DD_CAP = 10.0
DENSITY_LOW = 5.0
DENSITY_HIGH = 10.0
TOP_FORWARD_ROWS = 16


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F32A_SUMMARY)
    queue = pd.read_csv(io_path(F32A_QUEUE))
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    context = validate_context(stage_open, queue, frame, feature_order)
    micro_pockets = f28b.rebuild_f24_micro_pockets(frame, feature_order)
    raw_path = load_raw_path(frame)
    path_rows, split_metrics = run_path_proxy(frame, queue, micro_pockets, raw_path)
    summary = summarize_candidates(path_rows, split_metrics)
    final = build_final(created_at, stage_open, context, queue, raw_path, path_rows, split_metrics, summary)
    write_outputs(final, path_rows, split_metrics, summary)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "queue_rows": final["queue_rows"],
        "path_scout_clue_rows": final["path_scout_clue_rows"],
        "path_seed_surface_rows": final["path_seed_surface_rows"],
        "runtime_probe_candidate_rows": final["runtime_probe_candidate_rows"],
        "runtime_strict_candidate_rows": final["runtime_strict_candidate_rows"],
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
    queue: pd.DataFrame,
    frame: pd.DataFrame,
    feature_order: list[str],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    alignment = read_json(F32A_ALIGNMENT)
    checks = {
        "workspace_current_frontier32a_or_frontier32b": f"current_stage_id: {STAGE_ID}" in workspace
        and (f"current_run_id: {f32a.RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace),
        "workspace_next_run_frontier32b": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_parent_matches": stage_open.get("run_id") == PARENT_RUN_ID,
        "stage_open_grok_accepted": stage_open.get("grok", {}).get("classification", "").startswith("accepted"),
        "stage_open_lock_changed_variable": stage_open.get("locks", {}).get("active_changed_variable")
        == "fixed_log_return_caps_to_price_path_sl_tp_representation",
        "queue_rows_sixteen": len(queue) == 16,
        "queue_head_f31b_0013": str(queue.iloc[0]["candidate_id"]) == "f31b_0013",
        "queue_all_runtime_not_allowed_before_proxy": (~queue["runtime_attempt_allowed_now"].astype(bool)).all(),
        "alignment_no_missing": int(alignment.get("missing_entry_open_rows", -1)) == 0
        and int(alignment.get("missing_future_open_rows", -1)) == 0,
        "alignment_p99_small": float(alignment.get("p99_abs_delta", 999.0)) <= 0.0002,
        "raw_path_exists": path_exists(RAW_US100_PATH),
        "dataset_required_columns": {"timestamp", "future_timestamp", "split", "horizon_bars"}.issubset(frame.columns),
        "feature_order_contract": len(feature_order) == 58,
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier32B context check failed: {json.dumps(checks, ensure_ascii=False)}")
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


def run_path_proxy(
    frame: pd.DataFrame,
    queue: pd.DataFrame,
    micro_pockets: list[dict[str, Any]],
    raw_path: dict[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    id_to_micro = {str(row["micro_id"]): row for row in micro_pockets}
    raw = raw_path["raw"]
    open_prices = raw["open"].to_numpy(dtype="float64")
    high_prices = raw["high"].to_numpy(dtype="float64")
    low_prices = raw["low"].to_numpy(dtype="float64")
    entry_pos = raw_path["entry_pos"]
    future_pos = raw_path["future_pos"]
    path_rows: list[dict[str, Any]] = []
    metric_rows: list[dict[str, Any]] = []
    for index, queue_row in queue.reset_index(drop=True).iterrows():
        candidate_id = f"f32b_{index + 1:04d}"
        micro_ids = [token for token in str(queue_row["micro_ids"]).split("|") if token]
        pockets = [id_to_micro[micro_id] for micro_id in micro_ids if micro_id in id_to_micro]
        if len(pockets) != len(micro_ids):
            raise RuntimeError(f"Missing micro pockets for {queue_row['candidate_id']}: {micro_ids}")
        masks = [np.asarray(pocket["mask"], dtype=bool) for pocket in pockets]
        mask = np.logical_or.reduce(masks)
        side_value = int(queue_row["side_value"])
        simulation = simulate_path(frame, mask, queue_row, side_value, open_prices, high_prices, low_prices, entry_pos, future_pos)
        path_rows.append({
            "candidate_id": candidate_id,
            "source_f31_candidate_id": str(queue_row["candidate_id"]),
            "f30_candidate_id": str(queue_row["f30_candidate_id"]),
            "source_stability_union_id": str(queue_row["source_stability_union_id"]),
            "micro_ids": "|".join(micro_ids),
            "side_value": side_value,
            "transform_family": str(queue_row["transform_family"]),
            "stop_cap_log_return": safe_float_or_nan(queue_row.get("stop_cap_log_return")),
            "take_cap_log_return": safe_float_or_nan(queue_row.get("take_cap_log_return")),
            "f31_validation_profit_factor": safe_float_or_nan(queue_row.get("validation_profit_factor")),
            "f31_validation_trades_per_day": safe_float_or_nan(queue_row.get("validation_trades_per_day")),
            "f31_validation_dd_risk": safe_float_or_nan(queue_row.get("validation_dd_risk")),
            "f31_oos_profit_factor": safe_float_or_nan(queue_row.get("oos_profit_factor")),
            "f31_oos_trades_per_day": safe_float_or_nan(queue_row.get("oos_trades_per_day")),
            "f31_oos_dd_risk": safe_float_or_nan(queue_row.get("oos_dd_risk")),
            **simulation["aggregate"],
        })
        for split in ("train", "validation", "oos"):
            metric_rows.append({
                "candidate_id": candidate_id,
                "source_f31_candidate_id": str(queue_row["candidate_id"]),
                "split": split,
                "record_view": "Tier A separate(티어 A 분리)",
                "tier_scope": "Tier A(티어 A)",
                **simulation["split_metrics"][split],
            })
    return pd.DataFrame(path_rows), pd.DataFrame(metric_rows)


def simulate_path(
    frame: pd.DataFrame,
    mask: np.ndarray,
    queue_row: pd.Series,
    side_value: int,
    open_prices: np.ndarray,
    high_prices: np.ndarray,
    low_prices: np.ndarray,
    entry_pos: np.ndarray,
    future_pos: np.ndarray,
) -> dict[str, Any]:
    stop_cap = safe_float_or_nan(queue_row.get("stop_cap_log_return"))
    take_cap = safe_float_or_nan(queue_row.get("take_cap_log_return"))
    trade_indices = np.flatnonzero(mask)
    pnl = np.full(len(frame), np.nan, dtype="float64")
    reasons: list[str] = [""] * len(frame)
    holding_bars = np.full(len(frame), np.nan, dtype="float64")
    ambiguous = np.zeros(len(frame), dtype=bool)
    valid_trade = np.zeros(len(frame), dtype=bool)
    for idx in trade_indices:
        p = int(entry_pos[idx])
        q = int(future_pos[idx])
        if p < 0 or q <= p or q >= len(open_prices):
            continue
        entry = float(open_prices[p])
        if not math.isfinite(entry) or entry <= 0.0:
            continue
        result = simulate_one_trade(side_value, entry, p, q, stop_cap, take_cap, open_prices, high_prices, low_prices)
        pnl[idx] = result["pnl_log"] - scout.ROUGH_COST_LOG_RETURN
        reasons[idx] = result["exit_reason"]
        holding_bars[idx] = result["holding_bars"]
        ambiguous[idx] = result["ambiguous_both_hit"]
        valid_trade[idx] = True
    split_metrics = {}
    for split in ("train", "validation", "oos"):
        split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool) & valid_trade
        trade_pnl = pnl[split_mask]
        trade_times = frame.loc[split_mask, "timestamp"]
        metrics = scout.trade_metrics(trade_pnl, trade_times)
        days = scout.count_scope_days(frame.loc[frame["split"].astype(str).eq(split), "timestamp"])
        reason_values = pd.Series([reasons[i] for i in np.flatnonzero(split_mask)])
        split_metrics[split] = {
            "trade_count": int(len(trade_pnl)),
            "days_in_scope": int(days),
            "trades_per_day": float(len(trade_pnl) / days) if days else 0.0,
            "net_profit": float(metrics["net_profit"]),
            "profit_factor": float(metrics["profit_factor"]),
            "expectancy": float(metrics["expectancy"]),
            "win_rate": float(metrics["win_rate"]),
            "dd_risk": max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"])),
            "max_drawdown_percent": float(metrics["max_drawdown_percent"]),
            "max_monthly_drawdown_percent": float(metrics["max_monthly_drawdown_percent"]),
            "underwater_ratio": float(metrics["underwater_ratio"]),
            "max_loss_streak": int(metrics["max_loss_streak"]),
            "equity_trend_r2": float(metrics["equity_trend_r2"]),
            "stop_hit_count": int((reason_values == "stop").sum()),
            "take_hit_count": int((reason_values == "take").sum()),
            "horizon_exit_count": int((reason_values == "horizon").sum()),
            "ambiguous_both_hit_count": int(np.sum(ambiguous[split_mask])),
            "avg_holding_bars": safe_mean(holding_bars[split_mask]),
            "median_holding_bars": safe_median(holding_bars[split_mask]),
        }
    aggregate = {
        "valid_trade_rows": int(valid_trade.sum()),
        "invalid_path_rows": int(len(trade_indices) - valid_trade.sum()),
        "total_ambiguous_both_hit_count": int(ambiguous[valid_trade].sum()),
        "total_stop_hit_count": int(sum(split_metrics[s]["stop_hit_count"] for s in ("train", "validation", "oos"))),
        "total_take_hit_count": int(sum(split_metrics[s]["take_hit_count"] for s in ("train", "validation", "oos"))),
        "total_horizon_exit_count": int(sum(split_metrics[s]["horizon_exit_count"] for s in ("train", "validation", "oos"))),
    }
    return {"aggregate": aggregate, "split_metrics": split_metrics}


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


def summarize_candidates(path_rows: pd.DataFrame, split_metrics: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for candidate_id, group in split_metrics.groupby("candidate_id", sort=False):
        base = dict(path_rows.loc[path_rows["candidate_id"].eq(candidate_id)].iloc[0])
        for split in ("train", "validation", "oos"):
            item = dict(group.loc[group["split"].eq(split)].iloc[0])
            for field in (
                "trade_count",
                "days_in_scope",
                "trades_per_day",
                "net_profit",
                "profit_factor",
                "expectancy",
                "win_rate",
                "dd_risk",
                "max_drawdown_percent",
                "max_monthly_drawdown_percent",
                "underwater_ratio",
                "max_loss_streak",
                "equity_trend_r2",
                "stop_hit_count",
                "take_hit_count",
                "horizon_exit_count",
                "ambiguous_both_hit_count",
                "avg_holding_bars",
                "median_holding_bars",
            ):
                base[f"{split}_{field}"] = item[field]
        forward_min_pf = min(safe_float(base["validation_profit_factor"]), safe_float(base["oos_profit_factor"]))
        forward_max_dd = max(safe_float(base["validation_dd_risk"]), safe_float(base["oos_dd_risk"]))
        forward_min_density = min(safe_float(base["validation_trades_per_day"]), safe_float(base["oos_trades_per_day"]))
        forward_max_density = max(safe_float(base["validation_trades_per_day"]), safe_float(base["oos_trades_per_day"]))
        forward_min_r2 = min(safe_float(base["validation_equity_trend_r2"]), safe_float(base["oos_equity_trend_r2"]))
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
            and forward_min_r2 >= 0.75
        )
        base["runtime_probe_candidate_flag"] = bool(
            base["path_seed_surface_flag"]
            and forward_min_pf >= RUNTIME_PF
            and forward_max_dd <= RUNTIME_DD_CAP
            and max(int(base["validation_max_loss_streak"]), int(base["oos_max_loss_streak"])) <= 25
        )
        base["runtime_strict_candidate_flag"] = bool(base["runtime_probe_candidate_flag"] and forward_max_dd <= RUNTIME_STRICT_DD_CAP)
        base["executable_representation_available"] = True
        base["mt5_probe_requires_pre_expensive_grok"] = bool(base["runtime_probe_candidate_flag"])
        base["f31_to_path_forward_pf_retention"] = forward_min_pf / max(min(safe_float(base["f31_validation_profit_factor"]), safe_float(base["f31_oos_profit_factor"])), 1e-12)
        base["f31_to_path_forward_dd_delta"] = forward_max_dd - max(safe_float(base["f31_validation_dd_risk"]), safe_float(base["f31_oos_dd_risk"]))
        base["path_read_score"] = (
            6.0 * min(forward_min_pf, 3.0)
            + 1.0 * min(forward_min_density, 10.0)
            + 3.0 * min(forward_min_r2, 1.0)
            - 0.35 * forward_max_dd
            - 0.03 * (safe_float(base["validation_ambiguous_both_hit_count"]) + safe_float(base["oos_ambiguous_both_hit_count"]))
        )
        rows.append(base)
    summary = pd.DataFrame(rows)
    if not summary.empty:
        summary = summary.sort_values("path_read_score", ascending=False).reset_index(drop=True)
        summary["path_rank"] = np.arange(1, len(summary) + 1)
    return summary


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    context: dict[str, Any],
    queue: pd.DataFrame,
    raw_path: dict[str, Any],
    path_rows: pd.DataFrame,
    split_metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, Any]:
    scout_count = int(summary["path_scout_clue_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["path_seed_surface_flag"].sum()) if not summary.empty else 0
    runtime_count = int(summary["runtime_probe_candidate_flag"].sum()) if not summary.empty else 0
    strict_count = int(summary["runtime_strict_candidate_flag"].sum()) if not summary.empty else 0
    if runtime_count:
        status = "executable_sl_tp_path_proxy_runtime_probe_surface_needs_pre_expensive_grok_no_authority"
        judgment = "runtime_probe_candidates_require_grok_before_mt5_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
        runtime_probe_status = "runtime_probe_candidate_pending_pre_expensive_grok_and_mt5_micro_probe"
    elif seed_count:
        status = "executable_sl_tp_path_proxy_seed_surface_no_runtime_candidate_no_authority"
        judgment = "seed_surface_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_out_of_scope_by_claim_path_proxy_seed_only_no_runtime_candidate"
    elif scout_count:
        status = "executable_sl_tp_path_proxy_scout_only_no_runtime_candidate_no_authority"
        judgment = "scout_clue_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_out_of_scope_by_claim_path_proxy_scout_only_no_runtime_candidate"
    else:
        status = "executable_sl_tp_path_proxy_no_scout_no_seed_no_runtime_candidate_no_authority"
        judgment = "negative_memory_candidate_return_space_surface_did_not_survive_path_proxy"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_ineligible_no_path_proxy_candidate_after_f32b"
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
        "queue_rows": int(len(queue)),
        "path_candidate_rows": int(len(path_rows)),
        "split_metric_rows": int(len(split_metrics)),
        "summary_rows": int(len(summary)),
        "path_scout_clue_rows": scout_count,
        "path_seed_surface_rows": seed_count,
        "runtime_probe_candidate_rows": runtime_count,
        "runtime_strict_candidate_rows": strict_count,
        "best_path_candidate_id": best.get("candidate_id", ""),
        "best_path_candidate": json_ready(best),
        "context": context,
        "stage_open": {
            "run_id": stage_open.get("run_id"),
            "grok_classification": stage_open.get("grok", {}).get("classification", ""),
            "alignment_p99_abs_delta": stage_open.get("alignment_audit", {}).get("p99_abs_delta"),
        },
        "raw_path": {
            "path": RAW_US100_PATH.as_posix(),
            "raw_rows": raw_path["raw_rows"],
            "missing_entry_positions": raw_path["missing_entry_positions"],
            "missing_future_positions": raw_path["missing_future_positions"],
        },
        "runtime_probe_status": runtime_probe_status,
        "result_boundary": "python_price_path_proxy_only_no_wfo_no_mt5_no_onnx_no_authority",
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(
    final: dict[str, Any],
    path_rows: pd.DataFrame,
    split_metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    path_rows.to_csv(io_path(RUN_ROOT / "path_candidate_ledger.csv"), index=False, encoding="utf-8-sig")
    split_metrics.to_csv(io_path(RUN_ROOT / "path_split_metrics.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "path_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    if not summary.empty:
        summary.head(TOP_FORWARD_ROWS).to_csv(io_path(RUN_ROOT / "top_path_forward_diagnostic.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F32A_SUMMARY,
        F32A_QUEUE,
        F32A_ALIGNMENT,
        f23b.DATASET_PATH,
        f23b.FEATURE_ORDER_PATH,
        RAW_US100_PATH,
        RUN_ROOT / "path_candidate_ledger.csv",
        RUN_ROOT / "path_split_metrics.csv",
        RUN_ROOT / "path_candidate_summary.csv",
        RUN_ROOT / "top_path_forward_diagnostic.csv",
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
        "runtime_claim_boundary": "python_price_path_proxy_only_no_mt5_runtime_authority",
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f32a.f31d.f31b.f31a.upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "path_proxy_scout(경로 프록시 탐색)",
        "family": "runtime_backtest(런타임 백테스트)",
        "work_family": "runtime_backtest(런타임 백테스트)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"path_scout={final['path_scout_clue_rows']};seed={final['path_seed_surface_rows']};runtime_candidate={final['runtime_probe_candidate_rows']};next={final['next_run_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"path_scout={final['path_scout_clue_rows']};seed={final['path_seed_surface_rows']};runtime_candidate={final['runtime_probe_candidate_rows']}",
        "guardrail_kpi": "python_path_proxy_only_pre_expensive_grok_required_before_mt5",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_path_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_path_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "python_path_proxy_no_mt5(파이썬 경로 프록시, MT5 아님)",
        "scoreboard_lane": "path_proxy_scout(경로 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"path_scout={final['path_scout_clue_rows']};seed={final['path_seed_surface_rows']};runtime_candidate={final['runtime_probe_candidate_rows']}",
        "guardrail_kpi": "fixed_queue_no_forward_rerank_no_mt5_authority",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"next={final['next_run_id']};best={final['best_path_candidate_id']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "path_proxy_scout(경로 프록시 탐색)",
    }
    tier_b = dict(primary)
    tier_b.update({
        "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
        "subrun_id": f"{RUN_ID}__tier_b_missing_required",
        "record_view": "Tier B separate(티어 B 분리)",
        "tier_scope": "Tier B(티어 B)",
        "kpi_scope": "missing_required(필수 누락)",
        "primary_kpi": "missing_required(필수 누락)",
        "notes": "Tier B not materialized in F32B executable SL/TP path proxy(전선32B 실행 손절/익절 경로 프록시에서 티어 B 미물질화)",
    })
    tier_ab = dict(primary)
    tier_ab.update({
        "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "record_view": "Tier A+B combined(티어 A+B 합산)",
        "tier_scope": "Tier A+B(티어 A+B)",
        "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
        "primary_kpi": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": "Combined tier not claimed in F32B executable SL/TP path proxy(전선32B 실행 손절/익절 경로 프록시에서 합산 티어 주장 없음)",
    })
    return [primary, tier_b, tier_ab]


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


def report_text(final: dict[str, Any]) -> str:
    best = final["best_path_candidate"]
    return f"""# Frontier32B Executable SL/TP Path Proxy Report(전선32B 실행 가능한 손절/익절 경로 프록시 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F31(전선31) mapping queue(매핑 큐)를 raw Bid OHLC(원천 매수호가 시가/고가/저가/종가) 기반 fixed SL/TP path proxy(고정 손절/익절 경로 프록시)로 재측정했습니다.

Effect(효과): return-space clip(수익률 공간 클립)의 좋은 숫자를 실제 high/low path(고가/저가 경로)에서 다시 깎아 보며, MT5(엠티5) 없이 runtime authority(런타임 권위)를 주장하지 않습니다.

Queue/path rows(큐/경로 행): `{final['queue_rows']}` / `{final['path_candidate_rows']}`

Path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보): `{final['path_scout_clue_rows']}` / `{final['path_seed_surface_rows']}` / `{final['runtime_probe_candidate_rows']}`

Strict DD candidate(엄격 손실폭 후보): `{final['runtime_strict_candidate_rows']}`

Best path candidate(최상 경로 후보): `{final['best_path_candidate_id']}` from F31(전선31) `{best.get('source_f31_candidate_id', '')}`.

Best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk'))}`

Best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk'))}`

Ambiguous same-bar hits(동일 봉 동시 터치): validation/OOS(검증/표본외) `{best.get('validation_ambiguous_both_hit_count', 'NA')}` / `{best.get('oos_ambiguous_both_hit_count', 'NA')}` counted stop-first(손절 우선).

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier32B Gate Audit(전선32B 게이트 감사)

- stage_open_lock_gate(단계 개방 잠금 게이트): `{F32A_SUMMARY.as_posix()}` read(읽음)
- fixed_queue_gate(고정 큐 게이트): `{F32A_QUEUE.as_posix()}` rows(행) `{final['queue_rows']}`
- raw_path_gate(원천 경로 게이트): `{RAW_US100_PATH.as_posix()}` rows(행) `{final['raw_path']['raw_rows']}`
- alignment_gate(정렬 게이트): p99 abs delta(99퍼센타일 절대 차이) `{fmt(final['stage_open']['alignment_p99_abs_delta'])}`
- tie_break_gate(동시 터치 게이트): conservative stop-first(보수적 손절 우선)
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성)는 not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier32 Selection Status(전선32 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest proxy(최근 프록시): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보): `{final['path_scout_clue_rows']}` / `{final['path_seed_surface_rows']}` / `{final['runtime_probe_candidate_rows']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def current_working_state(final: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F32B(전선32B)는 executable SL/TP path proxy(실행 가능한 손절/익절 경로 프록시)를 실행했습니다.

Effect(효과): path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보) `{final['path_scout_clue_rows']}/{final['path_seed_surface_rows']}/{final['runtime_probe_candidate_rows']}`를 측정했고, 다음 행동은 이 결과에 맞춰 정해졌습니다.

Runtime probe boundary(런타임 탐침 경계): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran executable SL/TP path proxy(실행 가능한 손절/익절 경로 프록시). "
        f"Effect(효과): path_scout={final['path_scout_clue_rows']}, seed={final['path_seed_surface_rows']}, runtime_candidate={final['runtime_probe_candidate_rows']}, next=`{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR32-EXECUTABLE-SLTP-MAPPING-ONNX-SCOUT`: `{RUN_ID}` tested fixed price-path SL/TP mapping(고정 가격 경로 손절/익절 매핑). "
        f"Effect(효과): path scout/seed/runtime candidate(경로 탐색/씨앗/런타임 후보) `{final['path_scout_clue_rows']}/{final['path_seed_surface_rows']}/{final['runtime_probe_candidate_rows']}`.\n"
    )


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


def read_json(path: Path) -> dict[str, Any]:
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
