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
from stage_pipelines.stage_frontier_28 import frontier28b_train_only_stability_gap_proxy_scout as f28b
from stage_pipelines.stage_frontier_29 import frontier29b_train_only_loss_concentration_veto_proxy_scout as f29b
from stage_pipelines.stage_frontier_31 import materialize_frontier31a_stage_open as f31a


STAGE_ID = f31a.STAGE_ID
RUN_ID = "frontier31B_return_space_exit_shape_proxy_scout_v1"
RUN_NUMBER = "frontier31B"
PARENT_RUN_ID = f31a.RUN_ID
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier31C_grok_pre_expensive_return_space_exit_shape_handoff_review_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier31C_return_space_exit_shape_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_31/frontier31b_return_space_exit_shape_proxy_scout.py")

F31A_SUMMARY = STAGE_ROOT / "02_runs" / f31a.RUN_ID / "stage_open_summary.json"
F31A_LOCK = STAGE_ROOT / "02_runs" / f31a.RUN_ID / "return_space_exit_shape_lock.json"
F30B_CANDIDATE_SUMMARY = f31a.F30B_CANDIDATE_SUMMARY

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

SCOUT_PF = f29b.SCOUT_PF
SCOUT_DENSITY_LOW = f29b.SCOUT_DENSITY_LOW
SCOUT_DENSITY_HIGH = f29b.SCOUT_DENSITY_HIGH
SCOUT_DD_CAP = f29b.SCOUT_DD_CAP
SEED_PF = f29b.SEED_PF
SEED_DD_CAP = f29b.SEED_DD_CAP
HANDOFF_PF = f29b.HANDOFF_PF
HANDOFF_DD_CAP = f29b.HANDOFF_DD_CAP
HANDOFF_R2 = f29b.HANDOFF_R2
TOP_FORWARD_ROWS = 60


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F31A_SUMMARY)
    lock = read_json(F31A_LOCK)
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    f30_candidates = pd.read_csv(io_path(F30B_CANDIDATE_SUMMARY))
    context = validate_context(stage_open, lock, frame, feature_order, f30_candidates)
    micro_pockets = f28b.rebuild_f24_micro_pockets(frame, feature_order)
    fixed_scouts = reconstruct_fixed_scouts(frame, f30_candidates, micro_pockets, lock)
    variants = build_exit_shape_variants(frame, fixed_scouts, lock)
    metrics = evaluate_variants(frame, variants)
    summary = summarize_variants(metrics, variants)
    final = build_final(created_at, stage_open, context, fixed_scouts, variants, metrics, summary)
    write_outputs(final, fixed_scouts, variants, metrics, summary)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "fixed_scout_rows": final["fixed_scout_rows"],
        "variant_rows": final["variant_rows"],
        "density_bridge_rows": final["density_bridge_rows"],
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "realistic_handoff_candidate_rows": final["realistic_handoff_candidate_rows"],
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
    f30_candidates: pd.DataFrame,
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    locks = lock
    scout_rows = f30_candidates.loc[
        f30_candidates["scout_clue_flag"].astype(bool)
        & f30_candidates["branch"].astype(str).eq("source_no_veto_density_preservation_branch")
    ].copy()
    checks = {
        "workspace_current_stage_frontier31": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier31b": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_parent_matches": stage_open.get("run_id") == PARENT_RUN_ID,
        "stage_open_grok_accepted": stage_open.get("grok", {}).get("classification", "").startswith("accepted"),
        "lock_changed_variable_exit_shape": locks.get("active_changed_variable")
        == "train_only_return_space_exit_shape_transform_for_density_preserved_source_scouts",
        "lock_fixed_entry_surface": locks.get("fixed_entry_surface") == "f30b_source_no_veto_scout_rows_only",
        "lock_blocks_forward_selection": "select_exit_params_by_validation_or_oos_pf_dd_density" in locks.get("forbidden_primary_path", []),
        "lock_blocks_entry_change": "change_f30b_entry_masks_or_source_scout_identity" in locks.get("forbidden_primary_path", []),
        "lock_blocks_runtime_claim_from_clip": "claim_mt5_executable_behavior_from_return_space_clip_only" in locks.get("forbidden_primary_path", []),
        "f30_candidate_summary_available": path_exists(F30B_CANDIDATE_SUMMARY),
        "fixed_scout_rows_five": len(scout_rows) == 5,
        "fixed_scout_ids_match": tuple(scout_rows.sort_values("candidate_id")["candidate_id"].astype(str).tolist())
        == tuple(locks.get("fixed_candidate_ids", [])),
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_has_future_log_return_12": "future_log_return_12" in frame.columns,
        "dataset_has_required_splits": set(frame["split"].astype(str).unique()) == {"train", "validation", "oos"},
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier31B context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def reconstruct_fixed_scouts(
    frame: pd.DataFrame,
    f30_candidates: pd.DataFrame,
    micro_pockets: list[dict[str, Any]],
    lock: dict[str, Any],
) -> list[dict[str, Any]]:
    id_to_micro = {str(row["micro_id"]): row for row in micro_pockets}
    fixed_ids = tuple(lock.get("fixed_candidate_ids", []))
    rows = (
        f30_candidates.loc[f30_candidates["candidate_id"].astype(str).isin(fixed_ids)]
        .copy()
        .sort_values("candidate_id")
    )
    reconstructed: list[dict[str, Any]] = []
    for _, source in rows.iterrows():
        micro_ids = [token for token in str(source["micro_ids"]).split("|") if token]
        pockets = [id_to_micro[micro_id] for micro_id in micro_ids if micro_id in id_to_micro]
        if len(pockets) != len(micro_ids):
            raise RuntimeError(f"Missing micro pockets for {source['candidate_id']}: {micro_ids}")
        side_values = {int(pocket["side_value"]) for pocket in pockets}
        if len(side_values) != 1:
            raise RuntimeError(f"Mixed side micro pockets for {source['candidate_id']}: {micro_ids}")
        masks = [np.asarray(pocket["mask"], dtype=bool) for pocket in pockets]
        union_mask = np.logical_or.reduce(masks)
        side_value = int(pockets[0]["side_value"])
        control = {split: f23b.evaluate_mask(frame, union_mask, side_value, split) for split in ("train", "validation", "oos")}
        reconstructed.append({
            "f30_candidate_id": str(source["candidate_id"]),
            "source_stability_union_id": str(source["source_stability_union_id"]),
            "source_soft_union_id": str(source["source_soft_union_id"]),
            "micro_ids": "|".join(micro_ids),
            "micro_key": str(source.get("micro_key", "")),
            "side_value": side_value,
            "side": "long(롱)" if side_value > 0 else "short(숏)",
            "branch": str(source["branch"]),
            "rule_definition": str(source["rule_definition"]),
            "f30_validation_profit_factor": float(source["validation_profit_factor"]),
            "f30_oos_profit_factor": float(source["oos_profit_factor"]),
            "f30_validation_dd_risk": float(source["validation_dd_risk"]),
            "f30_oos_dd_risk": float(source["oos_dd_risk"]),
            "mask": union_mask,
            "control_metrics": control,
        })
    return reconstructed


def build_exit_shape_variants(
    frame: pd.DataFrame,
    fixed_scouts: list[dict[str, Any]],
    lock: dict[str, Any],
) -> list[dict[str, Any]]:
    contract = lock["return_space_exit_shape_contract"]
    loss_quantiles = tuple(float(value) for value in contract["loss_cap_quantiles"])
    take_quantiles = tuple(float(value) for value in contract["take_cap_quantiles"])
    minimum_stop = float(contract["minimum_stop_cap_log_return"])
    variants: list[dict[str, Any]] = []
    train_scope = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    returns = pd.to_numeric(frame["future_log_return_12"], errors="coerce").to_numpy(dtype="float64")
    for scout_row in fixed_scouts:
        mask = np.asarray(scout_row["mask"], dtype=bool)
        train_trade_mask = mask & train_scope
        train_index = np.flatnonzero(train_trade_mask)
        raw_train_pnl = returns[train_index] * float(scout_row["side_value"]) - scout.ROUGH_COST_LOG_RETURN
        raw_train_pnl = raw_train_pnl[np.isfinite(raw_train_pnl)]
        if raw_train_pnl.size == 0:
            continue
        losses = np.abs(raw_train_pnl[raw_train_pnl < 0.0])
        wins = raw_train_pnl[raw_train_pnl > 0.0]
        if losses.size < 20 or wins.size < 20:
            continue
        loss_q25 = float(np.nanquantile(losses, 0.25))
        variants.append(variant_row(scout_row, "control_no_exit_transform", None, None, 0.0, False, 0.0, 0.0))
        for loss_q in loss_quantiles:
            stop_cap = max(float(np.nanquantile(losses, loss_q)), minimum_stop)
            capped_fraction = float(np.mean(raw_train_pnl < -stop_cap))
            unrealistic = bool(stop_cap <= max(minimum_stop, loss_q25) or capped_fraction > 0.55)
            variants.append(variant_row(
                scout_row,
                "loss_cap_train_loss_quantile",
                stop_cap,
                None,
                loss_q,
                unrealistic,
                capped_fraction,
                0.0,
            ))
            for take_q in take_quantiles:
                take_cap = float(np.nanquantile(wins, take_q))
                if not math.isfinite(take_cap) or take_cap <= 0.0:
                    continue
                win_capped_fraction = float(np.mean(raw_train_pnl > take_cap))
                variants.append(variant_row(
                    scout_row,
                    "asymmetric_clip_train_loss_and_win_quantiles",
                    stop_cap,
                    take_cap,
                    loss_q,
                    unrealistic,
                    capped_fraction,
                    take_q,
                    win_capped_fraction,
                ))
    for index, row in enumerate(variants, start=1):
        row["exit_variant_id"] = f"f31b_raw_{index:04d}"
    return variants


def variant_row(
    scout_row: dict[str, Any],
    transform_family: str,
    stop_cap: float | None,
    take_cap: float | None,
    loss_quantile: float,
    unrealistic_tight_clip_flag: bool,
    train_loss_capped_fraction: float,
    take_quantile: float,
    train_win_capped_fraction: float = 0.0,
) -> dict[str, Any]:
    return {
        "exit_variant_id": "pending",
        "f30_candidate_id": scout_row["f30_candidate_id"],
        "source_stability_union_id": scout_row["source_stability_union_id"],
        "source_soft_union_id": scout_row["source_soft_union_id"],
        "micro_ids": scout_row["micro_ids"],
        "side_value": scout_row["side_value"],
        "side": scout_row["side"],
        "branch": scout_row["branch"],
        "rule_definition": scout_row["rule_definition"],
        "transform_family": transform_family,
        "stop_cap_log_return": float(stop_cap) if stop_cap is not None else math.nan,
        "take_cap_log_return": float(take_cap) if take_cap is not None else math.nan,
        "loss_quantile": float(loss_quantile),
        "take_quantile": float(take_quantile),
        "train_loss_capped_fraction": float(train_loss_capped_fraction),
        "train_win_capped_fraction": float(train_win_capped_fraction),
        "unrealistic_tight_clip_flag": bool(unrealistic_tight_clip_flag),
        "selection_boundary": "train_only_return_space_exit_shape_parameterization_validation_oos_read_only",
        "mask": scout_row["mask"],
    }


def evaluate_variants(frame: pd.DataFrame, variants: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for variant in variants:
        for split in ("train", "validation", "oos"):
            metrics = evaluate_variant_on_split(frame, variant, split)
            rows.append({
                **identity_fields(variant),
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
                "dd_risk": metrics["dd_risk"],
                "underwater_ratio": metrics["underwater_ratio"],
                "max_loss_streak": metrics["max_loss_streak"],
                "equity_trend_r2": metrics["equity_trend_r2"],
                "raw_net_profit": metrics["raw_net_profit"],
                "raw_profit_factor": metrics["raw_profit_factor"],
                "raw_dd_risk": metrics["raw_dd_risk"],
                "selection_boundary": "train_only_exit_shape_selection" if split == "train" else "read_only_forward_diagnostic",
            })
    return pd.DataFrame(rows)


def evaluate_variant_on_split(frame: pd.DataFrame, variant: dict[str, Any], split: str) -> dict[str, Any]:
    split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
    trade_mask = np.asarray(variant["mask"], dtype=bool) & split_mask
    split_times = frame.loc[split_mask, "timestamp"]
    days = scout.count_scope_days(split_times)
    returns = pd.to_numeric(frame.loc[trade_mask, "future_log_return_12"], errors="coerce").to_numpy(dtype="float64")
    raw_pnl = returns * float(variant["side_value"]) - scout.ROUGH_COST_LOG_RETURN
    transformed = transform_pnl(raw_pnl, variant)
    trade_times = frame.loc[trade_mask, "timestamp"]
    metrics = scout.trade_metrics(transformed, trade_times)
    raw_metrics = scout.trade_metrics(raw_pnl, trade_times)
    shape = f23b.payoff_shape(transformed)
    trade_count = int(len(transformed))
    return {
        **metrics,
        **shape,
        "trade_count": trade_count,
        "days_in_scope": days,
        "trades_per_day": float(trade_count / days) if days else 0.0,
        "dd_risk": max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"])),
        "raw_net_profit": float(raw_metrics["net_profit"]),
        "raw_profit_factor": float(raw_metrics["profit_factor"]),
        "raw_dd_risk": max(float(raw_metrics["max_drawdown_percent"]), float(raw_metrics["max_monthly_drawdown_percent"])),
    }


def transform_pnl(raw_pnl: np.ndarray, variant: dict[str, Any]) -> np.ndarray:
    pnl = np.asarray(raw_pnl, dtype="float64")
    out = pnl.copy()
    stop_cap = variant.get("stop_cap_log_return")
    take_cap = variant.get("take_cap_log_return")
    if stop_cap is not None and math.isfinite(float(stop_cap)) and float(stop_cap) > 0.0:
        out = np.maximum(out, -float(stop_cap))
    if take_cap is not None and math.isfinite(float(take_cap)) and float(take_cap) > 0.0:
        out = np.minimum(out, float(take_cap))
    return out


def summarize_variants(metrics: pd.DataFrame, variants: list[dict[str, Any]]) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    variant_map = {row["exit_variant_id"]: row for row in variants}
    rows: list[dict[str, Any]] = []
    for variant_id, group in metrics.groupby("exit_variant_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        variant = variant_map[str(variant_id)]
        base = identity_fields(variant)
        for prefix, row in (("train", train), ("validation", validation), ("oos", oos)):
            for field in (
                "trade_count",
                "days_in_scope",
                "trades_per_day",
                "net_profit",
                "profit_factor",
                "expectancy",
                "win_rate",
                "avg_win",
                "avg_loss_abs",
                "payoff_ratio",
                "right_tail_loss_tail_ratio",
                "adverse_loss_p10_abs",
                "dd_risk",
                "underwater_ratio",
                "max_loss_streak",
                "equity_trend_r2",
                "raw_net_profit",
                "raw_profit_factor",
                "raw_dd_risk",
            ):
                base[f"{prefix}_{field}"] = row[field]
        base["train_pf_lift_vs_raw"] = safe_float(train["profit_factor"]) - safe_float(train["raw_profit_factor"])
        base["train_dd_reduction_vs_raw"] = safe_float(train["raw_dd_risk"]) - safe_float(train["dd_risk"])
        base["validation_pf_lift_vs_raw"] = safe_float(validation["profit_factor"]) - safe_float(validation["raw_profit_factor"])
        base["oos_pf_lift_vs_raw"] = safe_float(oos["profit_factor"]) - safe_float(oos["raw_profit_factor"])
        forward_min_pf = min(safe_float(validation["profit_factor"]), safe_float(oos["profit_factor"]))
        forward_max_dd = max(safe_float(validation["dd_risk"]), safe_float(oos["dd_risk"]))
        forward_min_density = min(safe_float(validation["trades_per_day"]), safe_float(oos["trades_per_day"]))
        forward_max_density = max(safe_float(validation["trades_per_day"]), safe_float(oos["trades_per_day"]))
        base["forward_min_pf"] = forward_min_pf
        base["forward_max_dd"] = forward_max_dd
        base["forward_min_density"] = forward_min_density
        base["forward_max_density"] = forward_max_density
        base["density_bridge_flag"] = bool(SCOUT_DENSITY_LOW <= forward_min_density and forward_max_density <= SCOUT_DENSITY_HIGH)
        base["scout_clue_flag"] = bool(
            base["density_bridge_flag"]
            and safe_float(validation["net_profit"]) > 0
            and safe_float(oos["net_profit"]) > 0
            and forward_min_pf >= SCOUT_PF
            and forward_max_dd <= SCOUT_DD_CAP
        )
        base["seed_surface_flag"] = bool(base["scout_clue_flag"] and forward_min_pf >= SEED_PF and forward_max_dd <= SEED_DD_CAP)
        base["smoothness_proxy_pass"] = bool(
            safe_float(validation["equity_trend_r2"]) >= HANDOFF_R2
            and safe_float(oos["equity_trend_r2"]) >= HANDOFF_R2
            and int(validation["max_loss_streak"]) <= 20
            and int(oos["max_loss_streak"]) <= 20
        )
        base["handoff_candidate_flag"] = bool(
            base["seed_surface_flag"]
            and forward_min_pf >= HANDOFF_PF
            and forward_max_dd <= HANDOFF_DD_CAP
            and base["smoothness_proxy_pass"]
        )
        base["realistic_proxy_flag"] = not bool(base["unrealistic_tight_clip_flag"])
        base["realistic_handoff_candidate_flag"] = bool(base["handoff_candidate_flag"] and base["realistic_proxy_flag"])
        base["executable_exit_representation_available"] = False
        base["return_space_proxy_only_flag"] = True
        base["train_exit_shape_score"] = train_exit_shape_score(base)
        base["forward_read_score"] = forward_read_score(base)
        rows.append(base)
    summary = pd.DataFrame(rows).sort_values("train_exit_shape_score", ascending=False).reset_index(drop=True)
    summary["train_exit_shape_rank"] = np.arange(1, len(summary) + 1)
    summary["candidate_id"] = [f"f31b_{index:04d}" for index in summary["train_exit_shape_rank"]]
    return summary


def train_exit_shape_score(row: dict[str, Any]) -> float:
    pf = min(safe_float(row["train_profit_factor"]), 4.0)
    density = min(safe_float(row["train_trades_per_day"]), 10.0)
    dd = safe_float(row["train_dd_risk"])
    r2 = max(0.0, min(safe_float(row["train_equity_trend_r2"]), 1.0))
    pf_lift = max(0.0, safe_float(row["train_pf_lift_vs_raw"]))
    dd_reduction = max(0.0, safe_float(row["train_dd_reduction_vs_raw"]))
    unrealistic_penalty = 1.75 if bool(row["unrealistic_tight_clip_flag"]) else 1.0
    return float((pf + pf_lift) * density * (1.0 + r2 + dd_reduction / 10.0) / ((1.0 + dd / 10.0) * unrealistic_penalty))


def forward_read_score(row: dict[str, Any]) -> float:
    return float(
        max(safe_float(row["forward_min_pf"]), 0.0)
        * min(safe_float(row["forward_min_density"]), 10.0)
        * (1.0 + min(safe_float(row["validation_equity_trend_r2"]), safe_float(row["oos_equity_trend_r2"]), 1.0))
        / (1.0 + safe_float(row["forward_max_dd"]) / 10.0 + (0.5 if bool(row["unrealistic_tight_clip_flag"]) else 0.0))
    )


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    context: dict[str, Any],
    fixed_scouts: list[dict[str, Any]],
    variants: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, Any]:
    density_count = int(summary["density_bridge_flag"].astype(bool).sum()) if not summary.empty else 0
    scout_count = int(summary["scout_clue_flag"].astype(bool).sum()) if not summary.empty else 0
    seed_count = int(summary["seed_surface_flag"].astype(bool).sum()) if not summary.empty else 0
    handoff_count = int(summary["handoff_candidate_flag"].astype(bool).sum()) if not summary.empty else 0
    realistic_handoff = int(summary["realistic_handoff_candidate_flag"].astype(bool).sum()) if not summary.empty else 0
    unrealistic_handoff = int((summary["handoff_candidate_flag"].astype(bool) & summary["unrealistic_tight_clip_flag"].astype(bool)).sum()) if not summary.empty else 0
    executable_handoff = int((summary["handoff_candidate_flag"].astype(bool) & summary["executable_exit_representation_available"].astype(bool)).sum()) if not summary.empty else 0
    if realistic_handoff:
        status = "return_space_exit_shape_handoff_surface_proxy_needs_executable_repair_no_authority"
        judgment = "return_space_handoff_surface_requires_repair_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_pending_executable_exit_representation_repair_before_mt5"
    elif handoff_count:
        status = "return_space_exit_shape_unrealistic_handoff_proxy_invalid_risk_no_authority"
        judgment = "invalid_risk_tight_clip_handoff_surface_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_out_of_scope_by_claim_unrealistic_return_space_proxy_only"
    elif seed_count:
        status = "return_space_exit_shape_seed_surface_proxy_no_authority"
        judgment = "seed_surface_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_out_of_scope_by_claim_seed_only_no_executable_handoff"
    elif scout_count:
        status = "return_space_exit_shape_scout_clue_proxy_no_authority"
        judgment = "scout_clue_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_out_of_scope_by_claim_scout_only_no_executable_handoff"
    else:
        status = "return_space_exit_shape_no_scout_no_seed_no_handoff_proxy_no_authority"
        judgment = "negative_memory_candidate_requires_closeout_or_capped_repair_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_ineligible_no_handoff_candidate_after_f31b_proxy"
    best_train = dict(summary.iloc[0]) if not summary.empty else {}
    best_forward = dict(summary.sort_values("forward_read_score", ascending=False).iloc[0]) if not summary.empty else {}
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "fixed_scout_rows": int(len(fixed_scouts)),
        "variant_rows": int(len(variants)),
        "metric_rows": int(len(metrics)),
        "summary_rows": int(len(summary)),
        "density_bridge_rows": density_count,
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "realistic_handoff_candidate_rows": realistic_handoff,
        "unrealistic_handoff_candidate_rows": unrealistic_handoff,
        "executable_handoff_candidate_rows": executable_handoff,
        "best_train_candidate_id": best_train.get("candidate_id", ""),
        "best_train_candidate": json_ready(best_train),
        "best_forward_readonly_candidate_id": best_forward.get("candidate_id", ""),
        "best_forward_readonly_candidate": json_ready(best_forward),
        "context": context,
        "stage_open": {
            "run_id": stage_open.get("run_id"),
            "grok_classification": stage_open.get("grok", {}).get("classification", ""),
            "lock_changed_variable": stage_open.get("locks", {}).get("active_changed_variable", ""),
        },
        "runtime_probe_status": runtime_probe_status,
        "result_boundary": "return_space_proxy_only_no_wfo_no_mt5_no_onnx_no_authority",
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(
    final: dict[str, Any],
    fixed_scouts: list[dict[str, Any]],
    variants: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    fixed_for_csv = [{key: value for key, value in row.items() if key not in {"mask", "control_metrics"}} for row in fixed_scouts]
    pd.DataFrame(fixed_for_csv).to_csv(io_path(RUN_ROOT / "fixed_f30_source_scouts.csv"), index=False, encoding="utf-8-sig")
    variant_for_csv = [{key: value for key, value in row.items() if key != "mask"} for row in variants]
    pd.DataFrame(variant_for_csv).to_csv(io_path(RUN_ROOT / "return_space_exit_shape_variant_ledger.csv"), index=False, encoding="utf-8-sig")
    metrics.to_csv(io_path(RUN_ROOT / "return_space_exit_shape_split_metrics.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "return_space_exit_shape_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    if not summary.empty:
        summary.sort_values("forward_read_score", ascending=False).head(TOP_FORWARD_ROWS).to_csv(
            io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig"
        )
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, summary))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F31A_SUMMARY,
        F31A_LOCK,
        F30B_CANDIDATE_SUMMARY,
        f23b.DATASET_PATH,
        f23b.FEATURE_ORDER_PATH,
        RUN_ROOT / "fixed_f30_source_scouts.csv",
        RUN_ROOT / "return_space_exit_shape_variant_ledger.csv",
        RUN_ROOT / "return_space_exit_shape_split_metrics.csv",
        RUN_ROOT / "return_space_exit_shape_candidate_summary.csv",
        RUN_ROOT / "top_forward_readonly_diagnostic.csv",
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
        "selection_boundary": "train_only_return_space_exit_shape_parameterization_validation_oos_read_only",
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f31a.upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "proxy_scout(프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"variants={final['variant_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};realistic_handoff={final['realistic_handoff_candidate_rows']};next={final['next_run_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"variant={final['variant_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']}",
        "guardrail_kpi": "return_space_proxy_only_no_executable_exit_no_wfo_no_mt5_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_return_space_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_return_space_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "proxy_scout_no_runtime(프록시 탐색, 런타임 아님)",
        "scoreboard_lane": "proxy_scout(프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"variant={final['variant_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']}",
        "guardrail_kpi": "return_space_exit_shape_validation_oos_read_only_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"realistic_handoff={final['realistic_handoff_candidate_rows']};executable_handoff={final['executable_handoff_candidate_rows']};next={final['next_run_id']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "proxy_scout(프록시 탐색)",
    }
    tier_b = dict(primary)
    tier_b.update({
        "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
        "subrun_id": f"{RUN_ID}__tier_b_missing_required",
        "record_view": "Tier B separate(티어 B 분리)",
        "tier_scope": "Tier B(티어 B)",
        "kpi_scope": "missing_required(필수 누락)",
        "primary_kpi": "missing_required(필수 누락)",
        "notes": "Tier B not materialized in F31B return-space proxy(전선31B 수익률 공간 프록시에서 티어 B 미물질화)",
    })
    tier_ab = dict(primary)
    tier_ab.update({
        "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "record_view": "Tier A+B combined(티어 A+B 합산)",
        "tier_scope": "Tier A+B(티어 A+B)",
        "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
        "primary_kpi": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": "Combined tier not claimed in F31B return-space proxy(전선31B 수익률 공간 프록시에서 합산 티어 주장 없음)",
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


def report_text(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["best_forward_readonly_candidate"]
    return f"""# Frontier31B Return-Space Exit Shape Proxy Report(전선31B 수익률 공간 청산 형태 프록시 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F30B(전선30B)의 fixed source scout rows(고정 원천 탐색 행) 5개에 train-only return-space exit-shape transform(학습 전용 수익률 공간 청산 형태 변환)을 적용했습니다.

Effect(효과): entry mask(진입 마스크)는 바꾸지 않고, validation/OOS(검증/표본외)는 read-only(읽기 전용)로만 PF/DD(수익 팩터/손실폭) 변화를 측정했습니다.

Fixed/variant rows(고정/변형 행): `{final['fixed_scout_rows']}` / `{final['variant_rows']}`

Density/scout/seed/handoff rows(밀도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Realistic/executable handoff rows(현실성 통과/실행 가능 인계 행): `{final['realistic_handoff_candidate_rows']}` / `{final['executable_handoff_candidate_rows']}`

Best read-only forward candidate(최상 읽기 전용 전진 후보): `{final['best_forward_readonly_candidate_id']}` from F30(전선30) `{best.get('f30_candidate_id', '')}` transform(변환) `{best.get('transform_family', '')}`.

Best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk'))}`

Best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk'))}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier31B Gate Audit(전선31B 게이트 감사)

- stage_open_lock_gate(단계 개방 잠금 게이트): `{F31A_LOCK.as_posix()}` read(읽음)
- fixed_entry_surface_gate(고정 진입 표면 게이트): F30B source no-veto scout rows(전선30B 원천 무차단 탐색 행) `{final['fixed_scout_rows']}` only(만 사용)
- train_only_selection_gate(학습 전용 선택 게이트): stop/take(손절/익절) caps(상한)는 train PnL distribution(학습 손익 분포)에서만 산출
- leakage_guard(누수 방어): validation/OOS(검증/표본외)는 read-only diagnostics(읽기 전용 진단)
- executable_boundary_gate(실행 가능성 경계 게이트): return-space clipping(수익률 공간 클리핑)은 MT5 executable representation(MT5 실행 가능 표현)이 아님
- tier_pair_gate(티어 쌍 게이트): Tier B(티어 B)는 missing_required(필수 누락), Tier A+B(티어 A+B)는 out_of_scope_by_claim(주장 범위 밖)
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier31 Selection Status(전선31 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest proxy(최근 프록시): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Scout/seed/handoff(탐색/씨앗/인계): `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Realistic/executable handoff(현실성 통과/실행 가능 인계): `{final['realistic_handoff_candidate_rows']}` / `{final['executable_handoff_candidate_rows']}`

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

Action(행동): F31B(전선31B)는 return-space exit-shape proxy(수익률 공간 청산 형태 프록시)를 실행했습니다.

Effect(효과): scout/seed/handoff(탐색/씨앗/인계) `{final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']}`를 측정했지만, executable exit representation(실행 가능한 청산 표현)은 아직 없습니다.

Runtime probe boundary(런타임 탐침 경계): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran return-space exit-shape proxy(수익률 공간 청산 형태 프록시). "
        f"Effect(효과): variants={final['variant_rows']}, scout={final['scout_clue_rows']}, seed={final['seed_surface_rows']}, handoff={final['handoff_candidate_rows']}, next=`{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR31-RETURN-SPACE-EXIT-SHAPE-PF-LIFT-ONNX-SCOUT`: `{RUN_ID}` tested train-only return-space loss caps/asymmetric clips(학습 전용 수익률 공간 손실 상한/비대칭 클립). "
        f"Effect(효과): proxy scout/seed/handoff(프록시 탐색/씨앗/인계) `{final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']}` with executable handoff(실행 가능 인계) `{final['executable_handoff_candidate_rows']}`.\n"
    )


def identity_fields(variant: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "exit_variant_id",
        "f30_candidate_id",
        "source_stability_union_id",
        "source_soft_union_id",
        "micro_ids",
        "side_value",
        "side",
        "branch",
        "rule_definition",
        "transform_family",
        "stop_cap_log_return",
        "take_cap_log_return",
        "loss_quantile",
        "take_quantile",
        "train_loss_capped_fraction",
        "train_win_capped_fraction",
        "unrealistic_tight_clip_flag",
        "selection_boundary",
    ]
    return {key: variant.get(key, "") for key in keys}


def split_row(group: pd.DataFrame, split: str) -> dict[str, Any]:
    row = group.loc[group["split"].eq(split)]
    if row.empty:
        raise ValueError(f"Missing split row(분할 행 누락): {split}")
    return dict(row.iloc[0])


def safe_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


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
