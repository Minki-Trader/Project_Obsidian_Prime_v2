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
from stage_pipelines.stage_frontier_23 import frontier23c_payoff_asymmetry_entry_filter_repair as f23c
from stage_pipelines.stage_frontier_24 import frontier24b_density_bridge_payoff_pockets_proxy_scout as f24b
from stage_pipelines.stage_frontier_27 import frontier27b_soft_joint_satisfaction_penalty_proxy_scout as f27b
from stage_pipelines.stage_frontier_28 import materialize_frontier28a_stage_open as f28a


STAGE_ID = f28a.STAGE_ID
RUN_ID = "frontier28B_train_only_stability_gap_penalty_proxy_scout_v1"
RUN_NUMBER = "frontier28B"
PARENT_RUN_ID = f28a.RUN_ID
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier28C_grok_pre_expensive_stability_gap_handoff_review_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier28C_stability_gap_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_28/frontier28b_train_only_stability_gap_proxy_scout.py")
F28A_SUMMARY = STAGE_ROOT / "02_runs" / f28a.RUN_ID / "stage_open_summary.json"
F28A_LOCK = STAGE_ROOT / "02_runs" / f28a.RUN_ID / "stability_gap_penalty_lock.json"
F27B_REFERENCE_UNIONS = (
    Path("stages/stage_frontier_27__soft_joint_satisfaction_penalty_bridge_union_onnx_scout/02_runs")
    / f27b.RUN_ID
    / "train_ranked_soft_penalty_union_candidates.csv"
)
F27B_REFERENCE_SUMMARY = (
    Path("stages/stage_frontier_27__soft_joint_satisfaction_penalty_bridge_union_onnx_scout/02_runs")
    / f27b.RUN_ID
    / "soft_penalty_union_candidate_summary.csv"
)

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

CHUNK_PF_FLOOR_TARGET = 1.05
CHUNK_DD_CAP = 14.0
CHUNK_R2_FLOOR_TARGET = 0.20
CHUNK_LOSS_STREAK_TARGET = 14.0
CHUNK_NET_POSITIVE_TARGET = 3
GLOBAL_DENSITY_TARGET = 7.5
FINAL_CANDIDATE_CAP = 234
TOP_FORWARD_ROWS = 40

SCOUT_PF = 1.10
SCOUT_DENSITY_LOW = 5.0
SCOUT_DENSITY_HIGH = 10.0
SCOUT_DD_CAP = 25.0
SEED_PF = 1.20
SEED_DD_CAP = 18.0
HANDOFF_PF = 1.50
HANDOFF_DD_CAP = 12.0
HANDOFF_R2 = 0.35


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F28A_SUMMARY)
    lock = read_json(F28A_LOCK)
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    context = validate_context(stage_open, lock, feature_order)
    micro_pockets = rebuild_f24_micro_pockets(frame, feature_order)
    reference_unions = pd.read_csv(io_path(F27B_REFERENCE_UNIONS))
    reconstructed = reconstruct_reference_unions(frame, reference_unions, micro_pockets, stage_open)
    chunk_metrics = evaluate_chunk_metrics(frame, reconstructed, stage_open)
    scored = score_stability_candidates(reconstructed, chunk_metrics)
    split_metrics = evaluate_by_split(frame, scored)
    summary = summarize_candidates(split_metrics, chunk_metrics, scored)
    final = build_final(created_at, stage_open, context, micro_pockets, reconstructed, chunk_metrics, split_metrics, summary)
    write_outputs(final, reconstructed, chunk_metrics, scored, split_metrics, summary)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "reference_union_rows": final["reference_union_rows"],
        "stability_candidate_rows": final["stability_candidate_rows"],
        "density_bridge_rows": final["density_bridge_rows"],
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "best_stability_union_id": final["best_stability_union_id"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_context(stage_open: dict[str, Any], lock: dict[str, Any], feature_order: list[str]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    locks = lock.get("locks", {})
    checks = {
        "workspace_current_stage_frontier28": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier28b": f"next_run_id: {RUN_ID}" in workspace,
        "stage_open_parent_matches": stage_open.get("run_id") == PARENT_RUN_ID,
        "stage_open_grok_retry_accepted": stage_open.get("grok", {}).get("retry", {}).get("classification", "").startswith("accepted"),
        "lock_changed_variable_stability_gap": locks.get("changed_variable") == "train_subperiod_pf_dd_balance_stability_gap_rank",
        "lock_f27_reference_only": "reference_clue_only" in locks.get("f27_soft_penalty_role", ""),
        "lock_chunk_count_four": len(locks.get("chunk_boundaries", [])) == 4,
        "lock_no_posthoc_edits": bool(locks.get("chunking_contract", {}).get("no_post_hoc_edits")),
        "lock_blocks_forward_selection": "select_by_validation_or_oos_metrics" in locks.get("forbidden_primary_path", []),
        "feature_hash_matches_contract": f28a.ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_exists": path_exists(f23b.DATASET_PATH),
        "f27_reference_unions_available": path_exists(F27B_REFERENCE_UNIONS),
        "f27_reference_summary_available": path_exists(F27B_REFERENCE_SUMMARY),
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier28B context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def rebuild_f24_micro_pockets(frame: pd.DataFrame, feature_order: list[str]) -> list[dict[str, Any]]:
    baselines = f23b.build_unconditional_baselines(frame)
    condition_pool = f23b.build_condition_pool(frame, feature_order, baselines)
    f23b_candidates = pd.read_csv(io_path(f24b.F23B_CANDIDATES))
    source_candidates = f23c.rebuild_source_candidates(frame, condition_pool, f23b_candidates)
    repair_candidates = f23c.build_repair_candidates(frame, condition_pool, source_candidates)
    return f24b.build_micro_pockets(frame, repair_candidates)


def reconstruct_reference_unions(
    frame: pd.DataFrame,
    reference_unions: pd.DataFrame,
    micro_pockets: list[dict[str, Any]],
    stage_open: dict[str, Any],
) -> list[dict[str, Any]]:
    id_to_micro = {str(row["micro_id"]): row for row in micro_pockets}
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    reconstructed: list[dict[str, Any]] = []
    for _, source in reference_unions.head(FINAL_CANDIDATE_CAP).iterrows():
        micro_ids = [token for token in str(source["micro_ids"]).split("|") if token]
        pockets = [id_to_micro[micro_id] for micro_id in micro_ids if micro_id in id_to_micro]
        if len(pockets) != len(micro_ids):
            continue
        if len({int(pocket["side_value"]) for pocket in pockets}) != 1:
            continue
        masks = [np.asarray(pocket["mask"], dtype=bool) for pocket in pockets]
        union_mask = np.logical_or.reduce(masks)
        stats = f24b.overlap_stats(masks, train_mask)
        side_value = int(pockets[0]["side_value"])
        train = f23b.evaluate_mask(frame, union_mask, side_value, "train")
        reconstructed.append({
            "stability_union_id": "pending",
            "source_soft_union_id": str(source["soft_union_id"]),
            "source_train_rank": int(source.get("train_rank", 0)),
            "source_soft_joint_satisfaction_score": float(source.get("soft_joint_satisfaction_score", 0.0)),
            "union_type": str(source.get("union_type", "")),
            "pocket_count": int(source.get("pocket_count", len(pockets))),
            "micro_ids": "|".join(micro_ids),
            "micro_key": f27b.micro_key(micro_ids),
            "source_repair_ids": "|".join(str(pocket["source_repair_id"]) for pocket in pockets),
            "side_value": side_value,
            "side": str(source.get("side", pockets[0]["side"])),
            "features": str(source.get("features", " || ".join(str(pocket["features"]) for pocket in pockets))),
            "feature_families": str(source.get("feature_families", "|".join(sorted(set("|".join(str(pocket["feature_families"]) for pocket in pockets).split("|")))))),
            "rule_definition": str(source.get("rule_definition", " OR ".join(f"({pocket['rule_definition']})" for pocket in pockets))),
            "selection_boundary": "train_only_stability_gap_rank(학습 전용 안정성 격차 순위)",
            **stats,
            **{f"train_{key}": value for key, value in train.items()},
            "mask": union_mask,
        })
    return reconstructed


def evaluate_chunk_metrics(
    frame: pd.DataFrame,
    candidates: list[dict[str, Any]],
    stage_open: dict[str, Any],
) -> pd.DataFrame:
    chunk_scopes = build_chunk_scopes(frame, stage_open["locks"]["chunk_boundaries"])
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        for chunk in chunk_scopes:
            metrics = evaluate_mask_on_scope(frame, candidate["mask"], int(candidate["side_value"]), chunk["scope_mask"])
            rows.append({
                "source_soft_union_id": candidate["source_soft_union_id"],
                "micro_ids": candidate["micro_ids"],
                "micro_key": candidate["micro_key"],
                "side_value": candidate["side_value"],
                "chunk_id": chunk["chunk_id"],
                "chunk_start_timestamp": chunk["start_timestamp"],
                "chunk_end_timestamp": chunk["end_timestamp"],
                "chunk_row_count": chunk["row_count"],
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
                "selection_boundary": "train_only_chunk_metric(학습 전용 조각 지표)",
            })
    return pd.DataFrame(rows)


def build_chunk_scopes(frame: pd.DataFrame, chunk_boundaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    train_positions = np.flatnonzero(frame["split"].astype(str).eq("train").to_numpy(dtype=bool))
    scopes: list[dict[str, Any]] = []
    for chunk in chunk_boundaries:
        start = int(chunk["row_start_index"])
        end = int(chunk["row_end_index"])
        scope_mask = np.zeros(len(frame), dtype=bool)
        scope_mask[train_positions[start : end + 1]] = True
        scopes.append({**chunk, "scope_mask": scope_mask})
    return scopes


def evaluate_mask_on_scope(frame: pd.DataFrame, mask: np.ndarray, side: int, scope_mask: np.ndarray) -> dict[str, Any]:
    scope_mask = np.asarray(scope_mask, dtype=bool)
    trade_mask = np.asarray(mask, dtype=bool) & scope_mask
    scope_times = frame.loc[scope_mask, "timestamp"]
    days = scout.count_scope_days(scope_times)
    returns = pd.to_numeric(frame.loc[trade_mask, "future_log_return_12"], errors="coerce").to_numpy(dtype="float64")
    pnl = returns * float(side) - scout.ROUGH_COST_LOG_RETURN
    trade_times = frame.loc[trade_mask, "timestamp"]
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


def score_stability_candidates(candidates: list[dict[str, Any]], chunk_metrics: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        group = chunk_metrics.loc[chunk_metrics["source_soft_union_id"].eq(candidate["source_soft_union_id"])]
        score, components = stability_gap_score(candidate, group)
        enriched = dict(candidate)
        enriched["stability_gap_score"] = score
        enriched.update(components)
        rows.append(enriched)
    rows.sort(key=lambda row: float(row["stability_gap_score"]), reverse=True)
    for rank, row in enumerate(rows, start=1):
        row["stability_rank"] = rank
        row["stability_union_id"] = f"f28b_{rank:04d}"
    return rows


def stability_gap_score(candidate: dict[str, Any], chunks: pd.DataFrame) -> tuple[float, dict[str, float]]:
    pf_values = [bounded_pf(value) for value in chunks["profit_factor"].tolist()]
    dd_values = [positive(value) for value in chunks["dd_risk"].tolist()]
    density_values = [positive(value) for value in chunks["trades_per_day"].tolist()]
    net_values = [float(value) for value in chunks["net_profit"].tolist()]
    r2_values = [float(value) for value in chunks["equity_trend_r2"].tolist()]
    streak_values = [positive(value) for value in chunks["max_loss_streak"].tolist()]
    pf_floor = min(pf_values) if pf_values else 0.0
    dd_max = max(dd_values) if dd_values else 0.0
    density_mean = float(np.mean(density_values)) if density_values else 0.0
    density_std = float(np.std(density_values)) if density_values else 0.0
    density_cv = density_std / max(density_mean, 1e-9)
    net_positive_count = int(sum(value > 0 for value in net_values))
    r2_floor = min(r2_values) if r2_values else 0.0
    streak_max = max(streak_values) if streak_values else 0.0
    train_pf = bounded_pf(candidate["train_profit_factor"])
    train_dd = positive(candidate["train_dd_risk"])
    train_density = positive(candidate["train_trades_per_day"])
    train_r2 = float(candidate["train_equity_trend_r2"])
    pf_shortfall = max(0.0, CHUNK_PF_FLOOR_TARGET - pf_floor) / CHUNK_PF_FLOOR_TARGET
    pf_gap = max(0.0, train_pf - pf_floor) / max(train_pf, 1.0)
    dd_pressure = max(0.0, dd_max - CHUNK_DD_CAP) / CHUNK_DD_CAP
    dd_concentration = max(0.0, dd_max - train_dd) / max(train_dd, 1.0)
    net_positive_shortfall = max(0.0, CHUNK_NET_POSITIVE_TARGET - net_positive_count) / CHUNK_NET_POSITIVE_TARGET
    r2_shortfall = max(0.0, CHUNK_R2_FLOOR_TARGET - r2_floor) / CHUNK_R2_FLOOR_TARGET
    streak_pressure = max(0.0, streak_max - CHUNK_LOSS_STREAK_TARGET) / CHUNK_LOSS_STREAK_TARGET
    density_target_distance = abs(train_density - GLOBAL_DENSITY_TARGET) / GLOBAL_DENSITY_TARGET
    global_quality = (
        min(train_pf, 4.0)
        * min(train_density, 11.0)
        * (1.0 + max(train_r2, 0.0))
        / (1.0 + train_dd / 14.0 + density_target_distance)
    )
    penalty = (
        1.0
        + 1.8 * pf_shortfall
        + 1.1 * pf_gap
        + 1.6 * dd_pressure
        + 0.9 * dd_concentration
        + 0.8 * density_cv
        + 0.9 * net_positive_shortfall
        + 0.5 * r2_shortfall
        + 0.7 * streak_pressure
    )
    return float(global_quality / max(penalty, 1e-9)), {
        "chunk_pf_floor": pf_floor,
        "chunk_dd_max": dd_max,
        "chunk_density_mean": density_mean,
        "chunk_density_cv": density_cv,
        "chunk_net_positive_count": float(net_positive_count),
        "chunk_equity_r2_floor": r2_floor,
        "chunk_max_loss_streak_max": streak_max,
        "stability_pf_shortfall": pf_shortfall,
        "stability_pf_gap": pf_gap,
        "stability_dd_pressure": dd_pressure,
        "stability_dd_concentration": dd_concentration,
        "stability_net_positive_shortfall": net_positive_shortfall,
        "stability_r2_shortfall": r2_shortfall,
        "stability_streak_pressure": streak_pressure,
        "stability_density_target_distance": density_target_distance,
        "stability_global_quality": global_quality,
        "stability_penalty": penalty,
    }


def evaluate_by_split(frame: pd.DataFrame, candidates: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        for split in ("train", "validation", "oos"):
            metrics = f23b.evaluate_mask(frame, candidate["mask"], int(candidate["side_value"]), split)
            rows.append({
                "stability_union_id": candidate["stability_union_id"],
                "stability_rank": candidate["stability_rank"],
                "source_soft_union_id": candidate["source_soft_union_id"],
                "source_train_rank": candidate["source_train_rank"],
                "source_soft_joint_satisfaction_score": candidate["source_soft_joint_satisfaction_score"],
                "union_type": candidate["union_type"],
                "pocket_count": candidate["pocket_count"],
                "micro_ids": candidate["micro_ids"],
                "micro_key": candidate["micro_key"],
                "source_repair_ids": candidate["source_repair_ids"],
                "side": candidate["side"],
                "side_value": candidate["side_value"],
                "features": candidate["features"],
                "feature_families": candidate["feature_families"],
                "rule_definition": candidate["rule_definition"],
                "train_overlap_ratio": candidate["overlap_ratio"],
                "min_unique_density_contribution": candidate["min_unique_density_contribution"],
                "stability_gap_score": candidate["stability_gap_score"],
                "chunk_pf_floor": candidate["chunk_pf_floor"],
                "chunk_dd_max": candidate["chunk_dd_max"],
                "chunk_density_mean": candidate["chunk_density_mean"],
                "chunk_density_cv": candidate["chunk_density_cv"],
                "chunk_net_positive_count": candidate["chunk_net_positive_count"],
                "chunk_equity_r2_floor": candidate["chunk_equity_r2_floor"],
                "chunk_max_loss_streak_max": candidate["chunk_max_loss_streak_max"],
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
                "selection_boundary": "train_only_stability_gap_rank(학습 전용 안정성 격차 순위)" if split == "train" else "read_only_forward_diagnostic(읽기 전용 전진 진단)",
            })
    return pd.DataFrame(rows)


def summarize_candidates(metrics: pd.DataFrame, chunk_metrics: pd.DataFrame, candidates: list[dict[str, Any]]) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for candidate_id, group in metrics.groupby("stability_union_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        base = {
            "stability_union_id": candidate_id,
            "stability_rank": int(train["stability_rank"]),
            "source_soft_union_id": train["source_soft_union_id"],
            "source_train_rank": train["source_train_rank"],
            "source_soft_joint_satisfaction_score": train["source_soft_joint_satisfaction_score"],
            "union_type": train["union_type"],
            "pocket_count": train["pocket_count"],
            "micro_ids": train["micro_ids"],
            "micro_key": train["micro_key"],
            "source_repair_ids": train["source_repair_ids"],
            "side": train["side"],
            "features": train["features"],
            "feature_families": train["feature_families"],
            "rule_definition": train["rule_definition"],
            "train_overlap_ratio": train["train_overlap_ratio"],
            "min_unique_density_contribution": train["min_unique_density_contribution"],
            "stability_gap_score": train["stability_gap_score"],
            "chunk_pf_floor": train["chunk_pf_floor"],
            "chunk_dd_max": train["chunk_dd_max"],
            "chunk_density_mean": train["chunk_density_mean"],
            "chunk_density_cv": train["chunk_density_cv"],
            "chunk_net_positive_count": train["chunk_net_positive_count"],
            "chunk_equity_r2_floor": train["chunk_equity_r2_floor"],
            "chunk_max_loss_streak_max": train["chunk_max_loss_streak_max"],
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
        forward_max_dd = max(float(validation["dd_risk"]), float(oos["dd_risk"]))
        base["density_bridge_flag"] = bool(
            SCOUT_DENSITY_LOW <= validation["trades_per_day"] <= SCOUT_DENSITY_HIGH
            and SCOUT_DENSITY_LOW <= oos["trades_per_day"] <= SCOUT_DENSITY_HIGH
        )
        base["scout_clue_flag"] = bool(
            base["density_bridge_flag"]
            and validation["net_profit"] > 0
            and oos["net_profit"] > 0
            and validation["profit_factor"] >= SCOUT_PF
            and oos["profit_factor"] >= SCOUT_PF
            and forward_max_dd <= SCOUT_DD_CAP
        )
        base["seed_surface_flag"] = bool(
            base["scout_clue_flag"]
            and validation["profit_factor"] >= SEED_PF
            and oos["profit_factor"] >= SEED_PF
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
            and validation["profit_factor"] >= HANDOFF_PF
            and oos["profit_factor"] >= HANDOFF_PF
            and forward_max_dd <= HANDOFF_DD_CAP
            and base["smoothness_proxy_pass"]
        )
        base["forward_read_score"] = float(
            min(bounded_pf(validation["profit_factor"]), 4.0)
            * min(bounded_pf(oos["profit_factor"]), 4.0)
            * min(float(validation["trades_per_day"]), float(oos["trades_per_day"]), 10.0)
            * (1.0 + min(float(validation["equity_trend_r2"]), float(oos["equity_trend_r2"]), 1.0))
            / (1.0 + forward_max_dd / 10.0 + float(base["train_overlap_ratio"]))
        )
        rows.append(base)
    return pd.DataFrame(rows).sort_values("stability_rank")


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    context: dict[str, Any],
    micro_pockets: list[dict[str, Any]],
    reconstructed: list[dict[str, Any]],
    chunk_metrics: pd.DataFrame,
    split_metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, Any]:
    density_count = int(summary["density_bridge_flag"].sum()) if not summary.empty else 0
    scout_count = int(summary["scout_clue_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if not summary.empty else 0
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if not summary.empty else 0
    if handoff_count:
        status = "stability_gap_handoff_candidate_proxy_no_authority"
        judgment = "handoff_candidate_requires_grok_pre_expensive_review_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
    elif seed_count:
        status = "stability_gap_seed_surface_proxy_no_authority"
        judgment = "seed_surface_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif scout_count:
        status = "stability_gap_scout_clue_proxy_no_authority"
        judgment = "scout_clue_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif not reconstructed:
        status = "invalid_setup_stability_gap_reference_reconstruction_zero_no_authority"
        judgment = "invalid_setup_zero_reconstructed_unions_requires_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    else:
        status = "stability_gap_no_forward_clue_proxy_no_authority"
        judgment = "negative_or_no_forward_clue_requires_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    best = dict(summary.iloc[0]) if not summary.empty else {}
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
        "context": context,
        "stage_open": {
            "status": stage_open.get("status"),
            "judgment": stage_open.get("judgment"),
            "grok_retry_classification": stage_open.get("grok", {}).get("retry", {}).get("classification", ""),
        },
        "micro_pocket_rows": int(len(micro_pockets)),
        "reference_union_rows": int(len(pd.read_csv(io_path(F27B_REFERENCE_UNIONS)))),
        "stability_candidate_rows": int(len(reconstructed)),
        "chunk_metric_rows": int(len(chunk_metrics)),
        "split_metric_rows": int(len(split_metrics)),
        "density_bridge_rows": density_count,
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "best_stability_union_id": best.get("stability_union_id", ""),
        "best_stability_union": json_ready(best),
        "best_forward_readonly_union_id": best_forward.get("stability_union_id", ""),
        "best_forward_readonly_union": json_ready(best_forward),
        "result_boundary": "train_only_stability_gap_proxy_no_wfo_no_mt5_no_runtime_authority(학습 전용 안정성 격차 프록시, WFO/MT5/런타임 권위 없음)",
        "runtime_probe_status": "pre_expensive_grok_required_before_mt5(비싼 MT5 전 Grok 검토 필요)" if handoff_count else "out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(
    final: dict[str, Any],
    reconstructed: list[dict[str, Any]],
    chunk_metrics: pd.DataFrame,
    scored: list[dict[str, Any]],
    split_metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    pd.DataFrame([clean_for_csv(row) for row in reconstructed]).to_csv(
        io_path(RUN_ROOT / "reconstructed_f27_reference_union_candidates.csv"), index=False, encoding="utf-8-sig"
    )
    chunk_metrics.to_csv(io_path(RUN_ROOT / "stability_gap_chunk_metrics.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame([clean_for_csv(row) for row in scored]).to_csv(
        io_path(RUN_ROOT / "train_ranked_stability_gap_candidates.csv"), index=False, encoding="utf-8-sig"
    )
    split_metrics.to_csv(io_path(RUN_ROOT / "stability_gap_metrics_by_split.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "stability_gap_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    if not summary.empty:
        summary.sort_values("forward_read_score", ascending=False).head(TOP_FORWARD_ROWS).to_csv(
            io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig"
        )
    else:
        pd.DataFrame().to_csv(io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, summary))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F28A_SUMMARY,
        F28A_LOCK,
        F27B_REFERENCE_UNIONS,
        F27B_REFERENCE_SUMMARY,
        RUN_ROOT / "stability_gap_chunk_metrics.csv",
        RUN_ROOT / "train_ranked_stability_gap_candidates.csv",
        RUN_ROOT / "stability_gap_metrics_by_split.csv",
        RUN_ROOT / "stability_gap_candidate_summary.csv",
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
            "feature_count": 58,
            "feature_order_hash": f23b.EXPECTED_FEATURE_HASH,
            "feature_order_path": f23b.FEATURE_ORDER_PATH.as_posix(),
        },
        "rule_stack": {
            "source": "F27B 234 soft union rows reconstructed from F24 micro masks(F24 미세 마스크에서 재구성한 F27B 234 연성 합집합 행)",
            "selection": "train-only four-chunk stability gap rank(학습 전용 4조각 안정성 격차 순위)",
            "forbidden": "no validation/OOS selection, no F27 weight retune, no ONNX/MT5/WFO before handoff(검증/표본외 선택 없음, F27 가중치 조정 없음, 인계 전 온엑스/MT5/WFO 없음)",
        },
        "results": {
            "density_bridge_rows": final["density_bridge_rows"],
            "scout_clue_rows": final["scout_clue_rows"],
            "seed_surface_rows": final["seed_surface_rows"],
            "handoff_candidate_rows": final["handoff_candidate_rows"],
            "best_stability_union_id": final["best_stability_union_id"],
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
    best = final["best_stability_union"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stability_gap_proxy_scout(안정성 격차 프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"reference_union={final['reference_union_rows']};candidate={final['stability_candidate_rows']};density={final['density_bridge_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};best={final['best_stability_union_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={final['best_stability_union_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "stability_gap_no_repair_no_wfo_no_mt5_no_authority(안정성 격차, 수리/WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_stability_union"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_stability_gap_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_stability_gap_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "stability_gap_proxy_not_runtime(안정성 격차 프록시, 런타임 아님)",
        "scoreboard_lane": "trade_shape_proxy(거래 형태 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"best={final['best_stability_union_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "proxy_only_no_repair_no_wfo_no_mt5_no_authority(프록시 전용, 수리/WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"reference_union={final['reference_union_rows']};candidate={final['stability_candidate_rows']};density={final['density_bridge_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']}",
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
        "external_verification_status": "not_applicable_proxy_no_mt5(프록시, MT5 없음)",
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
    best = final["best_stability_union"]
    top_rows: list[str] = []
    if not summary.empty:
        for _, row in summary.head(12).iterrows():
            top_rows.append(
                f"| `{row['stability_union_id']}` | `{row['source_soft_union_id']}` | `{row['micro_ids']}` | {fmt(row['stability_gap_score'])} | "
                f"{fmt(row['chunk_pf_floor'])} | {fmt(row['chunk_dd_max'])} | {fmt(row['chunk_density_cv'])} | {fmt(row['chunk_net_positive_count'])} | "
                f"{fmt(row['validation_profit_factor'])} | {fmt(row['validation_trades_per_day'])} | {fmt(row['validation_dd_risk'])} | "
                f"{fmt(row['oos_profit_factor'])} | {fmt(row['oos_trades_per_day'])} | {fmt(row['oos_dd_risk'])} | {row['scout_clue_flag']} | {row['seed_surface_flag']} |"
            )
    table = "\n".join(top_rows) if top_rows else "| none(없음) | | | | | | | | | | | | | | | |"
    return f"""# Frontier28B Train-Only Stability Gap Proxy Report(전선28B 학습 전용 안정성 격차 프록시 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F27B reference union surface(F27B 참조 합집합 표면) `{final['reference_union_rows']}`개를 재구성하고, train-only four-chunk stability gap rank(학습 전용 4조각 안정성 격차 순위)로 다시 정렬했습니다.

Effect(효과): validation/OOS(검증/표본외)를 선택에 쓰지 않고, 학습 내부의 PF/DD instability(수익 팩터/손실폭 불안정성)가 전진 균형을 더 잘 예고하는지 확인했습니다.

Reference/stability/chunk rows(참조/안정성/조각 행): `{final['reference_union_rows']}` / `{final['stability_candidate_rows']}` / `{final['chunk_metric_rows']}`

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Best stability union(최상 안정성 합집합): `{final['best_stability_union_id']}` from `{best.get('source_soft_union_id', '')}`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Top Stability Rows(상위 안정성 행)

| F28 union(F28 합집합) | source(F27 원천) | micro ids(미세 ID) | stability score(안정성 점수) | chunk PF floor(조각 PF 바닥) | chunk DD max(조각 DD 최대) | density CV(빈도 변동계수) | net+ chunks(양수 조각) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier28B Gate Audit(전선28B 게이트 감사)

- scope_completion_gate(범위 완료 게이트): stability gap artifacts(안정성 격차 산출물) created(생성) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- kpi_contract_audit(KPI 계약 감사): split metrics/chunk metrics/summary(분할 지표/조각 지표/요약) created(생성)
- leakage_guard(누수 방지): selection boundary(선택 경계)는 train-only chunk rank(학습 전용 조각 순위), validation/OOS(검증/표본외)는 read-only(읽기 전용)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): stage ledger/run registry rows(단계 장부/실행 등록부 행) written(기록)
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier28 Selection Status(전선28 선택 상태)

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest proxy(최근 프록시): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best stability union(최상 안정성 합집합): `{final['best_stability_union_id']}`

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def current_working_state(final: dict[str, Any]) -> str:
    best = final["best_stability_union"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F28B(전선28B)가 F27B reference union surface(F27B 참조 합집합 표면)를 train-only chunk stability gap rank(학습 전용 조각 안정성 격차 순위)로 재정렬했습니다.

Effect(효과): validation/OOS(검증/표본외) 선택 없이 학습 내부 안정성이 forward PF/DD balance(전진 수익 팩터/손실폭 균형)를 밀어올리는지 확인했습니다.

Best stability union(최상 안정성 합집합): `{final['best_stability_union_id']}` from `{best.get('source_soft_union_id', '')}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran train-only stability gap proxy scout(학습 전용 안정성 격차 프록시 탐색). "
        f"Effect(효과): reference/stability/scout/seed/handoff(참조/안정성/탐색/씨앗/인계) counts are {final['reference_union_rows']}/{final['stability_candidate_rows']}/{final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']} and next run(다음 실행) is `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR28-TRAIN-ONLY-STABILITY-GAP-PENALTY-PF-DD-BALANCE-ONNX-SCOUT`: `{RUN_ID}` tested train-only four-chunk stability gap rank(학습 전용 4조각 안정성 격차 순위). "
        f"Effect(효과): best stability union `{final['best_stability_union_id']}` remains proxy-only(프록시 전용) with no authority(권위 없음).\n"
    )


def split_row(group: pd.DataFrame, split: str) -> dict[str, Any]:
    row = group.loc[group["split"].eq(split)]
    if row.empty:
        raise ValueError(f"Missing split row(분할 행 누락): {split}")
    return dict(row.iloc[0])


def clean_for_csv(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "mask"}


def bounded_pf(value: Any) -> float:
    value = float(value)
    if not math.isfinite(value):
        return 4.0
    if value >= 999.0:
        return 4.0
    return max(value, 0.0)


def positive(value: Any) -> float:
    value = float(value)
    if not math.isfinite(value):
        return 0.0
    return max(value, 0.0)


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
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing(누락)"}


def sha256_io(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
