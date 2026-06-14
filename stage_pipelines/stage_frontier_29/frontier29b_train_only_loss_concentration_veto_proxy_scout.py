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
from stage_pipelines.stage_frontier_29 import materialize_frontier29a_stage_open as f29a


STAGE_ID = f29a.STAGE_ID
RUN_ID = "frontier29B_train_only_loss_concentration_veto_proxy_scout_v1"
RUN_NUMBER = "frontier29B"
PARENT_RUN_ID = f29a.RUN_ID
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier29C_grok_pre_expensive_loss_concentration_handoff_review_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier29C_loss_concentration_veto_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_29/frontier29b_train_only_loss_concentration_veto_proxy_scout.py")

F29A_SUMMARY = STAGE_ROOT / "02_runs" / f29a.RUN_ID / "stage_open_summary.json"
F29A_LOCK = STAGE_ROOT / "02_runs" / f29a.RUN_ID / "loss_concentration_veto_lock.json"
F28B_CANDIDATE_SUMMARY = f29a.F28B_CANDIDATE_SUMMARY

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

LOSS_QUANTILES = (0.10, 0.25, 0.75, 0.90)
GLOBAL_DENSITY_TARGET = 7.5
SCOUT_PF = 1.10
SCOUT_DENSITY_LOW = 5.0
SCOUT_DENSITY_HIGH = 10.0
SCOUT_DD_CAP = 25.0
SEED_PF = 1.20
SEED_DD_CAP = 18.0
HANDOFF_PF = 1.50
HANDOFF_DD_CAP = 12.0
HANDOFF_R2 = 0.35
TOP_FORWARD_ROWS = 60


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F29A_SUMMARY)
    lock = read_json(F29A_LOCK)
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    source_summary = pd.read_csv(io_path(F28B_CANDIDATE_SUMMARY))
    context = validate_context(stage_open, lock, feature_order, source_summary)
    micro_pockets = f28b.rebuild_f24_micro_pockets(frame, feature_order)
    candidates = reconstruct_candidates(source_summary, micro_pockets)
    feature_arrays = {feature: pd.to_numeric(frame[feature], errors="coerce").to_numpy(dtype="float64") for feature in feature_order}
    screened_rules, selected_candidates = build_loss_veto_candidates(frame, feature_order, feature_arrays, candidates, stage_open)
    split_metrics = evaluate_selected_by_split(frame, selected_candidates)
    summary = summarize_selected(split_metrics, selected_candidates)
    final = build_final(created_at, stage_open, context, candidates, screened_rules, selected_candidates, split_metrics, summary)
    write_outputs(final, screened_rules, selected_candidates, split_metrics, summary)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "source_candidate_rows": final["source_candidate_rows"],
        "screened_rule_rows": final["screened_rule_rows"],
        "selected_veto_rows": final["selected_veto_rows"],
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "best_veto_candidate_id": final["best_veto_candidate_id"],
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
    feature_order: list[str],
    source_summary: pd.DataFrame,
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    locks = lock.get("locks", {})
    veto_contract = locks.get("veto_contract", {})
    checks = {
        "workspace_current_stage_frontier29": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier29b": f"next_run_id: {RUN_ID}" in workspace,
        "stage_open_parent_matches": stage_open.get("run_id") == PARENT_RUN_ID,
        "stage_open_grok_accepted": stage_open.get("grok", {}).get("classification", "").startswith("accepted"),
        "stage_open_joinability_234": int(stage_open.get("joinability", {}).get("joinable_candidate_rows", -1)) == 234,
        "lock_changed_variable_loss_veto": locks.get("changed_variable") == "train_loss_conditioned_veto_mask",
        "lock_no_posthoc_edits": bool(veto_contract.get("no_post_hoc_edits")),
        "lock_all_variants_recorded": bool(veto_contract.get("all_variants_recorded")),
        "lock_blocks_forward_selection": "select_by_validation_or_oos_metrics" in locks.get("forbidden_primary_path", []),
        "source_summary_234": len(source_summary) == 234,
        "source_summary_handoff_zero": int(source_summary["handoff_candidate_flag"].sum()) == 0,
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_exists": path_exists(f23b.DATASET_PATH),
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier29B context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def reconstruct_candidates(source_summary: pd.DataFrame, micro_pockets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    id_to_micro = {str(row["micro_id"]): row for row in micro_pockets}
    rows: list[dict[str, Any]] = []
    for _, source in source_summary.iterrows():
        micro_ids = [token for token in str(source["micro_ids"]).split("|") if token]
        pockets = [id_to_micro[micro_id] for micro_id in micro_ids if micro_id in id_to_micro]
        if len(pockets) != len(micro_ids):
            continue
        masks = [np.asarray(pocket["mask"], dtype=bool) for pocket in pockets]
        union_mask = np.logical_or.reduce(masks)
        side_value = int(source["side_value"]) if "side_value" in source else int(pockets[0]["side_value"])
        rows.append({
            "source_stability_union_id": str(source["stability_union_id"]),
            "source_stability_rank": int(source["stability_rank"]),
            "source_soft_union_id": str(source["source_soft_union_id"]),
            "micro_ids": "|".join(micro_ids),
            "micro_key": str(source["micro_key"]),
            "side": str(source["side"]),
            "side_value": side_value,
            "features": str(source.get("features", "")),
            "feature_families": str(source.get("feature_families", "")),
            "source_rule_definition": str(source.get("rule_definition", "")),
            "source_train_profit_factor": float(source.get("train_profit_factor", 0.0)),
            "source_train_trades_per_day": float(source.get("train_trades_per_day", 0.0)),
            "source_train_dd_risk": float(source.get("train_dd_risk", 0.0)),
            "source_validation_profit_factor": float(source.get("validation_profit_factor", 0.0)),
            "source_validation_trades_per_day": float(source.get("validation_trades_per_day", 0.0)),
            "source_validation_dd_risk": float(source.get("validation_dd_risk", 0.0)),
            "source_oos_profit_factor": float(source.get("oos_profit_factor", 0.0)),
            "source_oos_trades_per_day": float(source.get("oos_trades_per_day", 0.0)),
            "source_oos_dd_risk": float(source.get("oos_dd_risk", 0.0)),
            "mask": union_mask,
        })
    return rows


def build_loss_veto_candidates(
    frame: pd.DataFrame,
    feature_order: list[str],
    feature_arrays: dict[str, np.ndarray],
    candidates: list[dict[str, Any]],
    stage_open: dict[str, Any],
) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    train_scope = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    train_days = scout.count_scope_days(frame.loc[train_scope, "timestamp"])
    returns = pd.to_numeric(frame["future_log_return_12"], errors="coerce").to_numpy(dtype="float64")
    max_variants = int(stage_open["locks"]["veto_contract"]["max_variants_per_union"])
    max_singles = int(stage_open["locks"]["veto_contract"]["max_single_feature_variants_per_union"])
    max_pairs = int(stage_open["locks"]["veto_contract"]["max_pair_variants_per_union"])
    min_removed = float(stage_open["locks"]["veto_contract"]["min_removed_train_trade_fraction"])
    max_removed = float(stage_open["locks"]["veto_contract"]["max_removed_train_trade_fraction"])
    min_loss_capture = float(stage_open["locks"]["veto_contract"]["min_loss_capture_ratio"])

    screened_rows: list[dict[str, Any]] = []
    selected: list[dict[str, Any]] = []
    for candidate in candidates:
        union_mask = np.asarray(candidate["mask"], dtype=bool)
        train_trade_mask = union_mask & train_scope
        train_index = np.flatnonzero(train_trade_mask)
        side = int(candidate["side_value"])
        pnl = returns[train_index] * float(side) - scout.ROUGH_COST_LOG_RETURN
        trade_times = frame.loc[train_trade_mask, "timestamp"]
        base_metrics = quick_metrics(pnl, trade_times, train_days)
        loss_mask = pnl < 0.0
        total_loss_abs = float(np.abs(pnl[loss_mask]).sum())
        if len(train_index) == 0 or total_loss_abs <= 0.0:
            continue

        prelim_rules: list[dict[str, Any]] = []
        for feature in feature_order:
            values = feature_arrays[feature][train_index]
            loss_values = values[loss_mask & np.isfinite(values)]
            if len(loss_values) < 20:
                continue
            for quantile in LOSS_QUANTILES:
                threshold = float(np.nanquantile(loss_values, quantile))
                if not math.isfinite(threshold):
                    continue
                operator = "<=" if quantile <= 0.5 else ">="
                condition_train = values <= threshold if operator == "<=" else values >= threshold
                condition_train = condition_train & np.isfinite(values)
                rule_parts = [{
                    "feature": feature,
                    "operator": operator,
                    "threshold": threshold,
                    "loss_quantile": quantile,
                }]
                prelim = cheap_screen_rule(
                    candidate,
                    pnl,
                    condition_train,
                    total_loss_abs,
                    min_removed,
                    max_removed,
                    min_loss_capture,
                    rule_parts,
                    "single_feature_loss_concentration",
                )
                if prelim:
                    screened_rows.append({key: value for key, value in prelim.items() if key != "_condition_train"})
                    prelim_rules.append(prelim)

        single_rules: list[dict[str, Any]] = []
        prelim_rules.sort(key=lambda row: float(row["loss_screen_score"]), reverse=True)
        for prelim in prelim_rules[: max(max_singles * 6, 24)]:
            rule = score_veto_rule(
                candidate,
                base_metrics,
                pnl,
                trade_times,
                train_days,
                np.asarray(prelim["_condition_train"], dtype=bool),
                total_loss_abs,
                min_removed,
                max_removed,
                min_loss_capture,
                prelim["rule_parts"],
                prelim["rule_family"],
            )
            if rule:
                single_rules.append(rule)
        single_rules.sort(key=lambda row: float(row["train_veto_score"]), reverse=True)
        top_singles = single_rules[:max_singles]
        pair_rules: list[dict[str, Any]] = []
        for first_index, first in enumerate(top_singles):
            for second in top_singles[first_index + 1 :]:
                first_part = first["rule_parts"][0]
                second_part = second["rule_parts"][0]
                if first_part["feature"] == second_part["feature"]:
                    continue
                condition_train = np.asarray(first["_condition_train"], dtype=bool) | np.asarray(second["_condition_train"], dtype=bool)
                rule = score_veto_rule(
                    candidate,
                    base_metrics,
                    pnl,
                    trade_times,
                    train_days,
                    condition_train,
                    total_loss_abs,
                    min_removed,
                    max_removed,
                    min_loss_capture,
                    [first_part, second_part],
                    "capped_pair_loss_concentration",
                )
                if rule:
                    screened_rows.append({key: value for key, value in rule.items() if key != "_condition_train"})
                    pair_rules.append(rule)

        candidate_rules = (top_singles + sorted(pair_rules, key=lambda row: float(row["train_veto_score"]), reverse=True)[:max_pairs])
        candidate_rules.sort(key=lambda row: float(row["train_veto_score"]), reverse=True)
        for rule in candidate_rules[:max_variants]:
            condition_global = build_global_condition(feature_arrays, rule["rule_parts"])
            after_mask = union_mask & ~condition_global
            selected.append({
                **candidate,
                **{key: value for key, value in rule.items() if key != "_condition_train"},
                "mask": after_mask,
                "source_mask": union_mask,
                "selection_boundary": "train_only_loss_concentration_veto_rank",
            })

    selected.sort(key=lambda row: float(row["train_veto_score"]), reverse=True)
    for rank, row in enumerate(selected, start=1):
        row["veto_candidate_id"] = f"f29b_{rank:04d}"
        row["veto_rank"] = rank
    screened = pd.DataFrame(screened_rows)
    if not screened.empty:
        screened = screened.sort_values(["source_stability_union_id", "train_veto_score"], ascending=[True, False])
    return screened, selected


def cheap_screen_rule(
    candidate: dict[str, Any],
    pnl: np.ndarray,
    condition_train: np.ndarray,
    total_loss_abs: float,
    min_removed: float,
    max_removed: float,
    min_loss_capture: float,
    rule_parts: list[dict[str, Any]],
    rule_family: str,
) -> dict[str, Any] | None:
    condition_train = np.asarray(condition_train, dtype=bool)
    train_trade_count = int(len(pnl))
    if train_trade_count == 0:
        return None
    removed_count = int(condition_train.sum())
    removed_fraction = float(removed_count / train_trade_count)
    if removed_fraction < min_removed or removed_fraction > max_removed:
        return None
    removed_pnl = pnl[condition_train]
    removed_loss_abs = float(np.abs(removed_pnl[removed_pnl < 0.0]).sum())
    loss_capture_ratio = removed_loss_abs / total_loss_abs if total_loss_abs > 0 else 0.0
    if loss_capture_ratio < min_loss_capture:
        return None
    loss_quality = loss_capture_ratio / max(removed_fraction, 1e-9)
    removed_net = float(removed_pnl.sum()) if len(removed_pnl) else 0.0
    loss_screen_score = float(
        1.20 * loss_capture_ratio
        + 0.12 * min(loss_quality, 6.0)
        + 0.20 * max(0.0, -removed_net)
        - 0.25 * max(0.0, removed_fraction - 0.25)
    )
    return {
        "source_stability_union_id": candidate["source_stability_union_id"],
        "source_soft_union_id": candidate["source_soft_union_id"],
        "micro_ids": candidate["micro_ids"],
        "side": candidate["side"],
        "side_value": candidate["side_value"],
        "rule_family": rule_family,
        "rule_parts": rule_parts,
        "rule_definition": rule_definition(rule_parts),
        "train_trade_count_before": train_trade_count,
        "removed_train_trade_count": removed_count,
        "removed_train_trade_fraction": removed_fraction,
        "removed_train_loss_abs": removed_loss_abs,
        "loss_capture_ratio": loss_capture_ratio,
        "loss_quality_ratio": loss_quality,
        "removed_net_profit": removed_net,
        "loss_screen_score": loss_screen_score,
        "_condition_train": condition_train,
    }


def score_veto_rule(
    candidate: dict[str, Any],
    base_metrics: dict[str, Any],
    pnl: np.ndarray,
    trade_times: pd.Series,
    train_days: int,
    condition_train: np.ndarray,
    total_loss_abs: float,
    min_removed: float,
    max_removed: float,
    min_loss_capture: float,
    rule_parts: list[dict[str, Any]],
    rule_family: str,
) -> dict[str, Any] | None:
    condition_train = np.asarray(condition_train, dtype=bool)
    removed_count = int(condition_train.sum())
    train_trade_count = int(len(pnl))
    if train_trade_count == 0:
        return None
    removed_fraction = float(removed_count / train_trade_count)
    if removed_fraction < min_removed or removed_fraction > max_removed:
        return None
    removed_pnl = pnl[condition_train]
    kept_pnl = pnl[~condition_train]
    if len(kept_pnl) < max(40, int(train_trade_count * 0.50)):
        return None
    removed_loss_abs = float(np.abs(removed_pnl[removed_pnl < 0.0]).sum())
    loss_capture_ratio = removed_loss_abs / total_loss_abs if total_loss_abs > 0 else 0.0
    if loss_capture_ratio < min_loss_capture:
        return None
    kept_times = trade_times.loc[~condition_train]
    after_metrics = quick_metrics(kept_pnl, kept_times, train_days)
    density_penalty = abs(float(after_metrics["trades_per_day"]) - GLOBAL_DENSITY_TARGET) / GLOBAL_DENSITY_TARGET
    pf_gain = bounded_pf(after_metrics["profit_factor"]) - bounded_pf(base_metrics["profit_factor"])
    dd_reduction = max(0.0, float(base_metrics["dd_risk"]) - float(after_metrics["dd_risk"])) / max(float(base_metrics["dd_risk"]), 1.0)
    loss_quality = loss_capture_ratio / max(removed_fraction, 1e-9)
    net_guard = 0.20 if float(after_metrics["net_profit"]) > float(base_metrics["net_profit"]) else 0.0
    train_veto_score = float(
        1.15 * max(pf_gain, -0.25)
        + 1.35 * dd_reduction
        + 0.85 * loss_capture_ratio
        + 0.08 * min(loss_quality, 6.0)
        + net_guard
        - 0.35 * density_penalty
        - 0.20 * max(0.0, removed_fraction - 0.25)
    )
    return {
        "source_stability_union_id": candidate["source_stability_union_id"],
        "source_soft_union_id": candidate["source_soft_union_id"],
        "micro_ids": candidate["micro_ids"],
        "side": candidate["side"],
        "side_value": candidate["side_value"],
        "rule_family": rule_family,
        "rule_parts": rule_parts,
        "rule_definition": rule_definition(rule_parts),
        "train_trade_count_before": train_trade_count,
        "train_trade_count_after": int(len(kept_pnl)),
        "removed_train_trade_count": removed_count,
        "removed_train_trade_fraction": removed_fraction,
        "removed_train_loss_abs": removed_loss_abs,
        "loss_capture_ratio": loss_capture_ratio,
        "loss_quality_ratio": loss_quality,
        "train_profit_factor_before": float(base_metrics["profit_factor"]),
        "train_profit_factor_after": float(after_metrics["profit_factor"]),
        "train_net_profit_before": float(base_metrics["net_profit"]),
        "train_net_profit_after": float(after_metrics["net_profit"]),
        "train_dd_risk_before": float(base_metrics["dd_risk"]),
        "train_dd_risk_after": float(after_metrics["dd_risk"]),
        "train_trades_per_day_before": float(base_metrics["trades_per_day"]),
        "train_trades_per_day_after": float(after_metrics["trades_per_day"]),
        "train_equity_trend_r2_after": float(after_metrics["equity_trend_r2"]),
        "train_max_loss_streak_after": float(after_metrics["max_loss_streak"]),
        "train_veto_score": train_veto_score,
        "_condition_train": condition_train,
    }


def build_global_condition(feature_arrays: dict[str, np.ndarray], rule_parts: list[dict[str, Any]]) -> np.ndarray:
    conditions: list[np.ndarray] = []
    for part in rule_parts:
        values = feature_arrays[str(part["feature"])]
        threshold = float(part["threshold"])
        if part["operator"] == "<=":
            conditions.append((values <= threshold) & np.isfinite(values))
        else:
            conditions.append((values >= threshold) & np.isfinite(values))
    return np.logical_or.reduce(conditions) if conditions else np.zeros(len(next(iter(feature_arrays.values()))), dtype=bool)


def evaluate_selected_by_split(frame: pd.DataFrame, selected: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for candidate in selected:
        for split in ("train", "validation", "oos"):
            metrics = f23b.evaluate_mask(frame, candidate["mask"], int(candidate["side_value"]), split)
            rows.append({
                "veto_candidate_id": candidate["veto_candidate_id"],
                "veto_rank": candidate["veto_rank"],
                "source_stability_union_id": candidate["source_stability_union_id"],
                "source_stability_rank": candidate["source_stability_rank"],
                "source_soft_union_id": candidate["source_soft_union_id"],
                "micro_ids": candidate["micro_ids"],
                "side": candidate["side"],
                "side_value": candidate["side_value"],
                "rule_family": candidate["rule_family"],
                "rule_definition": candidate["rule_definition"],
                "removed_train_trade_fraction": candidate["removed_train_trade_fraction"],
                "loss_capture_ratio": candidate["loss_capture_ratio"],
                "train_veto_score": candidate["train_veto_score"],
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
                "payoff_ratio": metrics["payoff_ratio"],
                "right_tail_loss_tail_ratio": metrics["right_tail_loss_tail_ratio"],
                "adverse_loss_p10_abs": metrics["adverse_loss_p10_abs"],
                "dd_risk": metrics["dd_risk"],
                "underwater_ratio": metrics["underwater_ratio"],
                "max_loss_streak": metrics["max_loss_streak"],
                "equity_trend_r2": metrics["equity_trend_r2"],
                "selection_boundary": "train_only_loss_concentration_veto_rank(학습 전용 손실 집중 차단 순위)"
                if split == "train"
                else "read_only_forward_diagnostic(읽기 전용 전진 진단)",
            })
    return pd.DataFrame(rows)


def summarize_selected(metrics: pd.DataFrame, selected: list[dict[str, Any]]) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    selected_by_id = {row["veto_candidate_id"]: row for row in selected}
    rows: list[dict[str, Any]] = []
    for candidate_id, group in metrics.groupby("veto_candidate_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        source = selected_by_id[str(candidate_id)]
        base = {
            "veto_candidate_id": candidate_id,
            "veto_rank": int(train["veto_rank"]),
            "source_stability_union_id": train["source_stability_union_id"],
            "source_stability_rank": int(train["source_stability_rank"]),
            "source_soft_union_id": train["source_soft_union_id"],
            "micro_ids": train["micro_ids"],
            "side": train["side"],
            "side_value": int(train["side_value"]),
            "rule_family": train["rule_family"],
            "rule_definition": train["rule_definition"],
            "removed_train_trade_fraction": train["removed_train_trade_fraction"],
            "loss_capture_ratio": train["loss_capture_ratio"],
            "loss_quality_ratio": source["loss_quality_ratio"],
            "train_veto_score": train["train_veto_score"],
            "source_validation_profit_factor": source["source_validation_profit_factor"],
            "source_validation_trades_per_day": source["source_validation_trades_per_day"],
            "source_validation_dd_risk": source["source_validation_dd_risk"],
            "source_oos_profit_factor": source["source_oos_profit_factor"],
            "source_oos_trades_per_day": source["source_oos_trades_per_day"],
            "source_oos_dd_risk": source["source_oos_dd_risk"],
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
            ):
                base[f"{prefix}_{field}"] = row[field]
        forward_min_pf = min(float(validation["profit_factor"]), float(oos["profit_factor"]))
        forward_max_dd = max(float(validation["dd_risk"]), float(oos["dd_risk"]))
        forward_min_density = min(float(validation["trades_per_day"]), float(oos["trades_per_day"]))
        forward_max_density = max(float(validation["trades_per_day"]), float(oos["trades_per_day"]))
        base["forward_min_pf"] = forward_min_pf
        base["forward_max_dd"] = forward_max_dd
        base["forward_min_density"] = forward_min_density
        base["forward_max_density"] = forward_max_density
        base["density_bridge_flag"] = bool(
            SCOUT_DENSITY_LOW <= forward_min_density
            and forward_max_density <= SCOUT_DENSITY_HIGH
        )
        base["scout_clue_flag"] = bool(
            base["density_bridge_flag"]
            and validation["net_profit"] > 0
            and oos["net_profit"] > 0
            and forward_min_pf >= SCOUT_PF
            and forward_max_dd <= SCOUT_DD_CAP
        )
        base["seed_surface_flag"] = bool(
            base["scout_clue_flag"]
            and forward_min_pf >= SEED_PF
            and forward_max_dd <= SEED_DD_CAP
        )
        base["smoothness_proxy_pass"] = bool(
            validation["equity_trend_r2"] >= HANDOFF_R2
            and oos["equity_trend_r2"] >= HANDOFF_R2
            and validation["max_loss_streak"] <= 20
            and oos["max_loss_streak"] <= 20
        )
        base["handoff_candidate_flag"] = bool(
            base["seed_surface_flag"]
            and forward_min_pf >= HANDOFF_PF
            and forward_max_dd <= HANDOFF_DD_CAP
            and base["smoothness_proxy_pass"]
        )
        base["forward_read_score"] = float(
            min(bounded_pf(validation["profit_factor"]), 4.0)
            * min(bounded_pf(oos["profit_factor"]), 4.0)
            * min(forward_min_density, 10.0)
            * (1.0 + min(float(validation["equity_trend_r2"]), float(oos["equity_trend_r2"]), 1.0))
            / (1.0 + forward_max_dd / 10.0 + float(base["removed_train_trade_fraction"]))
        )
        rows.append(base)
    return pd.DataFrame(rows).sort_values("veto_rank")


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    context: dict[str, Any],
    candidates: list[dict[str, Any]],
    screened_rules: pd.DataFrame,
    selected: list[dict[str, Any]],
    split_metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, Any]:
    density_count = int(summary["density_bridge_flag"].sum()) if not summary.empty else 0
    scout_count = int(summary["scout_clue_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if not summary.empty else 0
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if not summary.empty else 0
    if handoff_count:
        status = "loss_concentration_veto_handoff_candidate_proxy_no_authority"
        judgment = "handoff_candidate_requires_grok_pre_expensive_review_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
        runtime_probe_status = "runtime_probe_pending_handoff_candidate_pre_expensive_grok_required"
    elif seed_count:
        status = "loss_concentration_veto_seed_surface_proxy_no_authority"
        judgment = "seed_surface_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_out_of_scope_by_claim_seed_only_no_handoff"
    elif scout_count:
        status = "loss_concentration_veto_scout_clue_proxy_no_authority"
        judgment = "scout_clue_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_out_of_scope_by_claim_scout_only_no_handoff"
    else:
        status = "loss_concentration_veto_no_scout_no_seed_no_handoff_proxy_no_authority"
        judgment = "negative_memory_candidate_requires_closeout_or_capped_repair_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_ineligible_no_handoff_candidate_after_f29b_proxy"
    best_train = dict(summary.sort_values("train_veto_score", ascending=False).iloc[0]) if not summary.empty else {}
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
        "source_candidate_rows": int(len(candidates)),
        "screened_rule_rows": int(len(screened_rules)),
        "selected_veto_rows": int(len(selected)),
        "split_metric_rows": int(len(split_metrics)),
        "density_bridge_rows": density_count,
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "best_veto_candidate_id": best_train.get("veto_candidate_id", ""),
        "best_train_veto_candidate": json_ready(best_train),
        "best_forward_readonly_candidate_id": best_forward.get("veto_candidate_id", ""),
        "best_forward_readonly_candidate": json_ready(best_forward),
        "context": context,
        "stage_open": {
            "run_id": stage_open.get("run_id"),
            "grok_classification": stage_open.get("grok", {}).get("classification", ""),
            "joinable_candidate_rows": stage_open.get("joinability", {}).get("joinable_candidate_rows"),
        },
        "runtime_probe_status": runtime_probe_status,
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
        "result_boundary": "proxy_scout_only_no_wfo_no_mt5_no_onnx_no_authority",
    }


def write_outputs(
    final: dict[str, Any],
    screened_rules: pd.DataFrame,
    selected: list[dict[str, Any]],
    split_metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    csv_selected = pd.DataFrame([clean_for_csv(row) for row in selected])
    screened_rules.to_csv(io_path(RUN_ROOT / "loss_concentration_screened_rule_ledger.csv"), index=False, encoding="utf-8-sig")
    csv_selected.to_csv(io_path(RUN_ROOT / "train_ranked_loss_veto_candidates.csv"), index=False, encoding="utf-8-sig")
    split_metrics.to_csv(io_path(RUN_ROOT / "loss_veto_metrics_by_split.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "loss_veto_candidate_summary.csv"), index=False, encoding="utf-8-sig")
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
        F29A_SUMMARY,
        F29A_LOCK,
        F28B_CANDIDATE_SUMMARY,
        RUN_ROOT / "loss_concentration_screened_rule_ledger.csv",
        RUN_ROOT / "train_ranked_loss_veto_candidates.csv",
        RUN_ROOT / "loss_veto_metrics_by_split.csv",
        RUN_ROOT / "loss_veto_candidate_summary.csv",
        REPORT_PATH,
        GATE_AUDIT_PATH,
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
        "rule_stack": {
            "source": "F28B 234 stability union rows reconstructed from F24 micro masks",
            "selection": "train-only loss concentration veto score",
            "forbidden": "no validation/OOS selection, no generic feature-veto replay, no ONNX/MT5/WFO before handoff",
        },
        "results": {
            "screened_rule_rows": final["screened_rule_rows"],
            "selected_veto_rows": final["selected_veto_rows"],
            "density_bridge_rows": final["density_bridge_rows"],
            "scout_clue_rows": final["scout_clue_rows"],
            "seed_surface_rows": final["seed_surface_rows"],
            "handoff_candidate_rows": final["handoff_candidate_rows"],
        },
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    best = final["best_forward_readonly_candidate"] or final["best_train_veto_candidate"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "loss_concentration_veto_proxy_scout(손실 집중 차단 프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"source={final['source_candidate_rows']};screened={final['screened_rule_rows']};selected={final['selected_veto_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={best.get('veto_candidate_id', '')};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "train_only_loss_veto_no_wfo_no_mt5_no_onnx_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_forward_readonly_candidate"] or final["best_train_veto_candidate"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_loss_veto_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_loss_veto_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "loss_concentration_veto_proxy_not_runtime(손실 집중 차단 프록시, 런타임 아님)",
        "scoreboard_lane": "trade_shape_proxy(거래 형태 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"best={best.get('veto_candidate_id', '')};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "proxy_only_no_wfo_no_mt5_no_onnx_no_authority(프록시 전용, WFO/MT5/ONNX/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"screened={final['screened_rule_rows']};selected={final['selected_veto_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']}",
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
        "external_verification_status": "not_applicable_proxy_no_mt5(프록시라 MT5 없음)",
        "notes": "Tier B source absent(티어 B 원천 없음)",
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
        "external_verification_status": "not_applicable_proxy_no_mt5(프록시라 MT5 없음)",
        "notes": "Combined source absent(합산 원천 없음)",
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
    best = final["best_forward_readonly_candidate"] or final["best_train_veto_candidate"]
    top_rows: list[str] = []
    if not summary.empty:
        for _, row in summary.sort_values("forward_read_score", ascending=False).head(12).iterrows():
            top_rows.append(
                f"| `{row['veto_candidate_id']}` | `{row['source_stability_union_id']}` | {fmt(row['train_veto_score'])} | "
                f"{fmt(row['removed_train_trade_fraction'])} | {fmt(row['loss_capture_ratio'])} | "
                f"{fmt(row['validation_profit_factor'])} | {fmt(row['validation_trades_per_day'])} | {fmt(row['validation_dd_risk'])} | "
                f"{fmt(row['oos_profit_factor'])} | {fmt(row['oos_trades_per_day'])} | {fmt(row['oos_dd_risk'])} | "
                f"{row['scout_clue_flag']} | {row['seed_surface_flag']} | {row['handoff_candidate_flag']} |"
            )
    table = "\n".join(top_rows) if top_rows else "| none(없음) | | | | | | | | | | | | | |"
    return f"""# Frontier29B Train-Only Loss Concentration Veto Proxy Report(전선29B 학습 전용 손실 집중 차단 프록시 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F28 reference union surface(F28 참조 합집합 표면) `{final['source_candidate_rows']}`개에 train-only loss concentration veto(학습 전용 손실 집중 차단)를 적용했습니다.

Effect(효과): selection(선택)은 train loss capture(학습 손실 포착), removed fraction(제거 비율), train PF/DD(학습 수익 팩터/손실폭)만 사용했고 validation/OOS(검증/표본외)는 read-only(읽기 전용)로 기록했습니다.

Screened/selected rows(선별/선택 행): `{final['screened_rule_rows']}` / `{final['selected_veto_rows']}`

Density/scout/seed/handoff rows(밀도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Best forward read-only candidate(최상 전진 읽기 전용 후보): `{best.get('veto_candidate_id', '')}` from `{best.get('source_stability_union_id', '')}`

Best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Top Read-Only Forward Rows(상위 읽기 전용 전진 행)

| veto(차단) | source(F28 원천) | train score(학습 점수) | removed frac(제거 비율) | loss capture(손실 포착) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed | handoff |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier29B Gate Audit(전선29B 게이트 감사)

- proxy_artifact_gate(프록시 산출물 게이트): loss veto ledger/metrics/summary(손실 차단 장부/지표/요약) created(생성)
- leakage_guard(누수 방지): train-only loss concentration score(학습 전용 손실 집중 점수) selected(선택), validation/OOS read-only(검증/표본외 읽기 전용)
- density_side_effect_gate(밀도 부작용 게이트): before/after removed fraction and forward density(전후 제거 비율과 전진 밀도) recorded(기록)
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier29 Selection Status(전선29 선택 상태)

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest proxy(최근 프록시): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best veto candidate(최상 차단 후보): `{final['best_veto_candidate_id']}`

Density/scout/seed/handoff rows(밀도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def current_working_state(final: dict[str, Any]) -> str:
    best = final["best_forward_readonly_candidate"] or final["best_train_veto_candidate"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F29B(전선29B)가 train-only loss concentration veto(학습 전용 손실 집중 차단) proxy(프록시)를 실행했습니다.

Effect(효과): selected veto rows(선택 차단 행) `{final['selected_veto_rows']}`개와 scout/seed/handoff(탐색/씨앗/인계) `{final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']}`개를 기록했습니다.

Best read-only forward candidate(최상 읽기 전용 전진 후보): `{best.get('veto_candidate_id', '')}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-밀도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran train-only loss concentration veto proxy(학습 전용 손실 집중 차단 프록시 실행). "
        f"Effect(효과): screened/selected/scout/seed/handoff(선별/선택/탐색/씨앗/인계) counts are {final['screened_rule_rows']}/{final['selected_veto_rows']}/{final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']} and next run(다음 실행) is `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR29-TRAIN-ONLY-LOSS-CONCENTRATION-VETO-PF-DD-BALANCE-ONNX-SCOUT`: `{RUN_ID}` tested train-only loss concentration veto(학습 전용 손실 집중 차단). "
        f"Effect(효과): selected veto rows(선택 차단 행) `{final['selected_veto_rows']}` remain proxy-only(프록시 전용) with no authority(권위 없음).\n"
    )


def quick_metrics(pnl: np.ndarray, trade_times: pd.Series, days: int) -> dict[str, Any]:
    pnl = np.asarray(pnl, dtype="float64")
    metrics = scout.trade_metrics(pnl, trade_times)
    shape = f23b.payoff_shape(pnl)
    trade_count = int(len(pnl))
    return {
        **metrics,
        **shape,
        "trade_count": trade_count,
        "days_in_scope": days,
        "trades_per_day": float(trade_count / days) if days else 0.0,
        "dd_risk": max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"])),
    }


def rule_definition(rule_parts: list[dict[str, Any]]) -> str:
    tokens = []
    for part in rule_parts:
        tokens.append(f"{part['feature']} {part['operator']} {float(part['threshold']):.8g} @ loss_q{int(float(part['loss_quantile']) * 100):02d}")
    return " OR ".join(tokens)


def split_row(group: pd.DataFrame, split: str) -> dict[str, Any]:
    row = group.loc[group["split"].eq(split)]
    if row.empty:
        raise ValueError(f"Missing split row(분할 행 누락): {split}")
    return dict(row.iloc[0])


def clean_for_csv(row: dict[str, Any]) -> dict[str, Any]:
    cleaned = {key: value for key, value in row.items() if key not in {"mask", "source_mask"}}
    if "rule_parts" in cleaned:
        cleaned["rule_parts"] = json.dumps(json_ready(cleaned["rule_parts"]), ensure_ascii=False, sort_keys=True)
    return cleaned


def bounded_pf(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(number):
        return 4.0
    if number >= 999.0:
        return 4.0
    return max(number, 0.0)


def fmt(value: Any) -> str:
    if value is None or value == "":
        return "NA"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(number):
        return "NA"
    return f"{number:.3f}"


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing"}


def sha256_io(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
