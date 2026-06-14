from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from pandas.errors import EmptyDataError

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_23 import frontier23c_payoff_asymmetry_entry_filter_repair as f23c
from stage_pipelines.stage_frontier_24 import frontier24b_density_bridge_payoff_pockets_proxy_scout as f24b
from stage_pipelines.stage_frontier_25 import frontier25b_bridge_archetype_preselection_proxy_scout as f25b
from stage_pipelines.stage_frontier_26 import frontier26b_joint_micro_satisfaction_proxy_scout as f26b
from stage_pipelines.stage_frontier_27 import materialize_frontier27a_stage_open as f27a


STAGE_ID = f27a.STAGE_ID
RUN_ID = "frontier27B_soft_joint_satisfaction_penalty_bridge_union_proxy_scout_v1"
RUN_NUMBER = "frontier27B"
PARENT_RUN_ID = f27a.RUN_ID
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier27C_grok_pre_expensive_soft_penalty_handoff_review_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier27C_soft_joint_satisfaction_penalty_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_27/frontier27b_soft_joint_satisfaction_penalty_proxy_scout.py")

F27A_SUMMARY = STAGE_ROOT / "02_runs" / f27a.RUN_ID / "stage_open_summary.json"
F27A_LOCK = STAGE_ROOT / "02_runs" / f27a.RUN_ID / "soft_joint_satisfaction_penalty_lock.json"
F24B_SUMMARY_TABLE = (
    Path("stages/stage_frontier_24__density_bridge_payoff_pockets_onnx_scout/02_runs")
    / f24b.RUN_ID
    / "bridge_candidate_summary.csv"
)
F25B_SUMMARY_TABLE = (
    Path("stages/stage_frontier_25__bridge_archetype_preselection_onnx_scout/02_runs")
    / f25b.RUN_ID
    / "archetype_candidate_summary.csv"
)
F26B_SUMMARY_TABLE = (
    Path("stages/stage_frontier_26__joint_micro_satisfaction_before_bridge_union_onnx_scout/02_runs")
    / f26b.RUN_ID
    / "joint_union_candidate_summary.csv"
)
F26B_REJECTION_AUDIT = (
    Path("stages/stage_frontier_26__joint_micro_satisfaction_before_bridge_union_onnx_scout/02_runs")
    / f26b.RUN_ID
    / "joint_union_rejection_audit.csv"
)

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

TOP_MICROS_FOR_PAIRS = 60
TOP_MICROS_FOR_TRIPLES = 55
PAIR_KEEP = 170
PAIR_FOR_TRIPLES = 80
TRIPLE_KEEP = 150
FINAL_CANDIDATE_CAP = 240
TOP_FORWARD_ROWS = 40

MICRO_PF_TARGET = 1.18
MICRO_DD_TARGET = 14.0
MICRO_DENSITY_LOW = 2.0
MICRO_DENSITY_HIGH = 6.0
MICRO_DENSITY_MID = 4.0
MICRO_R2_TARGET = 0.70
MICRO_STREAK_TARGET = 18.0
UNION_DD_TARGET = 16.0
UNION_DENSITY_TARGET = 7.5

SCOUT_PF = f27a.CRITERIA["scout_clue"]["pf"]
SCOUT_DENSITY_LOW = f27a.CRITERIA["scout_clue"]["density_low"]
SCOUT_DENSITY_HIGH = f27a.CRITERIA["scout_clue"]["density_high"]
SCOUT_DD_CAP = f27a.CRITERIA["scout_clue"]["dd_cap"]
SEED_PF = f27a.CRITERIA["seed_surface"]["pf"]
SEED_DD_CAP = f27a.CRITERIA["seed_surface"]["dd_cap"]
HANDOFF_PF = f27a.CRITERIA["handoff_candidate"]["pf"]
HANDOFF_DD_CAP = f27a.CRITERIA["handoff_candidate"]["dd_cap"]
HANDOFF_R2 = f27a.CRITERIA["handoff_candidate"]["equity_trend_r2"]


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F27A_SUMMARY)
    lock = read_json(F27A_LOCK)
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    context = validate_context(stage_open, lock, feature_order)
    baselines = f23b.build_unconditional_baselines(frame)
    condition_pool = f23b.build_condition_pool(frame, feature_order, baselines)
    f23b_candidates = pd.read_csv(io_path(f24b.F23B_CANDIDATES))
    source_candidates = f23c.rebuild_source_candidates(frame, condition_pool, f23b_candidates)
    f23c_repair_candidates = f23c.build_repair_candidates(frame, condition_pool, source_candidates)
    micro_pockets = f24b.build_micro_pockets(frame, f23c_repair_candidates)
    micro_audit, scored_micros, source_median_adverse = build_soft_micro_audit(micro_pockets)
    unions = build_soft_unions(frame, scored_micros, source_median_adverse)
    metrics = evaluate_soft_unions(frame, unions)
    summary = summarize_soft_unions(metrics)
    repeat_audit = build_repeat_audit(summary)
    final = build_final(
        created_at,
        stage_open,
        context,
        micro_pockets,
        micro_audit,
        scored_micros,
        unions,
        metrics,
        summary,
        repeat_audit,
        source_median_adverse,
    )
    write_outputs(final, micro_audit, unions, metrics, summary, repeat_audit)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "soft_micro_pool_rows": final["soft_micro_pool_rows"],
        "soft_union_candidate_rows": final["soft_union_candidate_rows"],
        "density_bridge_rows": final["density_bridge_rows"],
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "top10_f24b_overlap_count": final["top10_f24b_overlap_count"],
        "top10_f25b_overlap_count": final["top10_f25b_overlap_count"],
        "top10_f26b_overlap_count": final["top10_f26b_overlap_count"],
        "best_soft_union_id": final["best_soft_union_id"],
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
        "workspace_current_stage_frontier27": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_or_current_frontier27b": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_run_matches_parent": stage_open.get("run_id") == PARENT_RUN_ID,
        "lock_changed_variable_soft_penalty": locks.get("changed_variable") == "soft_joint_satisfaction_penalty_rank",
        "lock_full_80_source_pool": "80_micro" in locks.get("source_micro_pool", ""),
        "lock_blocks_f26_relaxation": "f26_hard_gate_numeric_threshold_relaxation" in locks.get("forbidden_primary_path", []),
        "lock_penalty_formula_written": len(locks.get("soft_penalty_contract", {}).get("terms", [])) >= 8,
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_exists": path_exists(f23b.DATASET_PATH),
        "f24b_reference_table_available": path_exists(F24B_SUMMARY_TABLE),
        "f25b_reference_table_available": path_exists(F25B_SUMMARY_TABLE),
        "f26b_rejection_audit_available": path_exists(F26B_REJECTION_AUDIT),
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier27B context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def build_soft_micro_audit(micro_pockets: list[dict[str, Any]]) -> tuple[pd.DataFrame, list[dict[str, Any]], float]:
    adverse_values = [float(pocket["train_adverse_loss_p10_abs"]) for pocket in micro_pockets]
    source_median_adverse = float(np.nanmedian(adverse_values)) if adverse_values else math.nan
    rows: list[dict[str, Any]] = []
    scored: list[dict[str, Any]] = []
    for pocket in micro_pockets:
        score, components = micro_soft_score(pocket, source_median_adverse)
        enriched = dict(pocket)
        enriched["soft_micro_score"] = score
        enriched.update({f"soft_{key}": value for key, value in components.items()})
        row = clean_for_csv(enriched)
        row["selection_boundary"] = "train_only_soft_micro_penalty_score(학습 전용 연성 미세 페널티 점수)"
        rows.append(row)
        scored.append(enriched)
    scored.sort(key=lambda row: float(row["soft_micro_score"]), reverse=True)
    for rank, row in enumerate(scored, start=1):
        row["soft_micro_rank"] = rank
    audit = pd.DataFrame(rows)
    if not audit.empty:
        rank_map = {row["micro_id"]: row["soft_micro_rank"] for row in scored}
        audit["soft_micro_rank"] = audit["micro_id"].map(rank_map)
        audit = audit.sort_values("soft_micro_rank")
    return audit, scored, source_median_adverse


def micro_soft_score(pocket: dict[str, Any], source_median_adverse: float) -> tuple[float, dict[str, float]]:
    pf = positive(float(pocket["train_profit_factor"]))
    dd = positive(float(pocket["train_dd_risk"]))
    density = positive(float(pocket["train_trades_per_day"]))
    r2 = float(pocket["train_equity_trend_r2"])
    streak = positive(float(pocket["train_max_loss_streak"]))
    adverse = positive(float(pocket["train_adverse_loss_p10_abs"]))
    pf_shortfall = max(0.0, MICRO_PF_TARGET - pf) / MICRO_PF_TARGET
    dd_pressure = max(0.0, dd - MICRO_DD_TARGET) / MICRO_DD_TARGET
    density_low_pressure = max(0.0, MICRO_DENSITY_LOW - density) / MICRO_DENSITY_LOW
    density_high_pressure = max(0.0, density - MICRO_DENSITY_HIGH) / MICRO_DENSITY_HIGH
    density_mid_distance = abs(density - MICRO_DENSITY_MID) / MICRO_DENSITY_MID
    r2_shortfall = max(0.0, MICRO_R2_TARGET - r2) / MICRO_R2_TARGET
    streak_pressure = max(0.0, streak - MICRO_STREAK_TARGET) / MICRO_STREAK_TARGET
    adverse_pressure = max(0.0, adverse - source_median_adverse) / max(source_median_adverse, 1e-9)
    density_fit = 1.0 / (1.0 + density_mid_distance)
    family_bonus = 1.0 + min(len(str(pocket["feature_families"]).split("|")), 4) * 0.08
    base = (
        family_bonus
        * min(pf, 4.0)
        * min(positive(float(pocket["train_payoff_ratio"])), 4.0)
        * density_fit
        * (1.0 + max(r2, 0.0))
    )
    penalty = (
        1.0
        + 1.6 * pf_shortfall
        + 1.4 * dd_pressure
        + 0.7 * density_low_pressure
        + 0.7 * density_high_pressure
        + 0.4 * density_mid_distance
        + 0.9 * r2_shortfall
        + 0.6 * streak_pressure
        + 0.8 * adverse_pressure
    )
    components = {
        "pf_shortfall": pf_shortfall,
        "dd_pressure": dd_pressure,
        "density_low_pressure": density_low_pressure,
        "density_high_pressure": density_high_pressure,
        "density_mid_distance": density_mid_distance,
        "r2_shortfall": r2_shortfall,
        "loss_streak_pressure": streak_pressure,
        "adverse_loss_pressure": adverse_pressure,
        "base": base,
        "penalty": penalty,
    }
    return float(base / max(penalty, 1e-9)), components


def build_soft_unions(frame: pd.DataFrame, scored_micros: list[dict[str, Any]], source_median_adverse: float) -> list[dict[str, Any]]:
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    candidates: list[dict[str, Any]] = []
    top_pair = scored_micros[: min(len(scored_micros), TOP_MICROS_FOR_PAIRS)]
    for pockets in itertools.combinations(top_pair, 2):
        maybe = soft_union_from_pockets(frame, list(pockets), train_mask, "pair", source_median_adverse)
        if maybe is not None:
            candidates.append(maybe)
    candidates.sort(key=lambda row: float(row["soft_joint_satisfaction_score"]), reverse=True)
    pair_kept = candidates[:PAIR_KEEP]
    triple_candidates: list[dict[str, Any]] = []
    id_to_micro = {str(pocket["micro_id"]): pocket for pocket in scored_micros}
    top_add = scored_micros[: min(len(scored_micros), TOP_MICROS_FOR_TRIPLES)]
    for pair in pair_kept[:PAIR_FOR_TRIPLES]:
        existing_ids = str(pair["micro_ids"]).split("|")
        existing = [id_to_micro[micro_id] for micro_id in existing_ids if micro_id in id_to_micro]
        if len(existing) != 2:
            continue
        for add in top_add:
            if add["micro_id"] in existing_ids:
                continue
            if int(add["side_value"]) != int(existing[0]["side_value"]):
                continue
            maybe = soft_union_from_pockets(frame, existing + [add], train_mask, "triple", source_median_adverse)
            if maybe is not None:
                triple_candidates.append(maybe)
    triple_candidates.sort(key=lambda row: float(row["soft_joint_satisfaction_score"]), reverse=True)
    all_candidates = pair_kept + triple_candidates[:TRIPLE_KEEP]
    all_candidates.sort(key=lambda row: float(row["soft_joint_satisfaction_score"]), reverse=True)
    selected = dedupe_unions(all_candidates)[:FINAL_CANDIDATE_CAP]
    for index, row in enumerate(selected, start=1):
        row["soft_union_id"] = f"f27b_{index:04d}"
    return selected


def soft_union_from_pockets(
    frame: pd.DataFrame,
    pockets: list[dict[str, Any]],
    train_mask: np.ndarray,
    union_type: str,
    source_median_adverse: float,
) -> dict[str, Any] | None:
    if len({int(pocket["side_value"]) for pocket in pockets}) != 1:
        return None
    family_tokens: list[str] = []
    for pocket in pockets:
        family_tokens.extend(str(pocket["feature_families"]).split("|"))
    family_set = sorted(set(family_tokens))
    if len(family_set) < 2:
        return None
    if max(family_tokens.count(family) for family in family_set) > 4:
        return None
    masks = [np.asarray(pocket["mask"], dtype=bool) for pocket in pockets]
    union_mask = np.logical_or.reduce(masks)
    stats = f24b.overlap_stats(masks, train_mask)
    side_value = int(pockets[0]["side_value"])
    train = f23b.evaluate_mask(frame, union_mask, side_value, "train")
    if int(train["trade_count"]) <= 0:
        return None
    score, score_components = soft_union_score(train, stats, pockets)
    envelope = broad_scout_envelope_flag(train, stats)
    return {
        "soft_union_id": "pending",
        "union_type": union_type,
        "pocket_count": len(pockets),
        "micro_ids": "|".join(str(pocket["micro_id"]) for pocket in pockets),
        "micro_key": micro_key(pocket["micro_id"] for pocket in pockets),
        "source_repair_ids": "|".join(str(pocket["source_repair_id"]) for pocket in pockets),
        "side_value": side_value,
        "side": pockets[0]["side"],
        "features": " || ".join(str(pocket["features"]) for pocket in pockets),
        "feature_families": "|".join(family_set),
        "rule_definition": " OR ".join(f"({pocket['rule_definition']})" for pocket in pockets),
        "micro_train_pf_floor": min(float(pocket["train_profit_factor"]) for pocket in pockets),
        "micro_train_dd_max": max(float(pocket["train_dd_risk"]) for pocket in pockets),
        "micro_train_r2_floor": min(float(pocket["train_equity_trend_r2"]) for pocket in pockets),
        "micro_train_max_loss_streak_max": max(float(pocket["train_max_loss_streak"]) for pocket in pockets),
        "micro_adverse_loss_p10_abs_max": max(float(pocket["train_adverse_loss_p10_abs"]) for pocket in pockets),
        "soft_micro_score_floor": min(float(pocket["soft_micro_score"]) for pocket in pockets),
        "soft_micro_score_mean": float(np.mean([float(pocket["soft_micro_score"]) for pocket in pockets])),
        "soft_joint_satisfaction_score": score,
        "source_median_train_adverse_loss_p10_abs": source_median_adverse,
        "broad_scout_envelope_flag": envelope,
        **{f"soft_union_{key}": value for key, value in score_components.items()},
        **stats,
        **{f"train_{key}": value for key, value in train.items()},
        "mask": union_mask,
    }


def soft_union_score(metrics: dict[str, Any], stats: dict[str, Any], pockets: list[dict[str, Any]]) -> tuple[float, dict[str, float]]:
    pf = positive(float(metrics["profit_factor"]))
    dd = positive(float(metrics["dd_risk"]))
    density = positive(float(metrics["trades_per_day"]))
    r2 = float(metrics["equity_trend_r2"])
    micro_floor = min(float(pocket["soft_micro_score"]) for pocket in pockets)
    micro_mean = float(np.mean([float(pocket["soft_micro_score"]) for pocket in pockets]))
    density_distance = abs(density - UNION_DENSITY_TARGET) / UNION_DENSITY_TARGET
    density_fit = 1.0 / (1.0 + density_distance)
    dd_pressure = max(0.0, dd - UNION_DD_TARGET) / UNION_DD_TARGET
    overlap_penalty = float(stats["overlap_ratio"]) * 1.5
    unique_reward = 1.0 + min(max(float(stats["min_unique_density_contribution"]), 0.0), 2.0) / 2.0
    net_penalty = 0.0 if float(metrics["net_profit"]) > 0 else 1.5
    union_quality = min(pf, 4.0) * density_fit * (1.0 + max(r2, 0.0)) * unique_reward
    penalty = 1.0 + dd_pressure + overlap_penalty + 0.4 * density_distance + net_penalty
    score = micro_floor * (1.0 + micro_mean) * union_quality / max(penalty, 1e-9)
    return float(score), {
        "density_distance": density_distance,
        "dd_pressure": dd_pressure,
        "overlap_penalty": overlap_penalty,
        "unique_reward": unique_reward,
        "net_penalty": net_penalty,
        "union_quality": union_quality,
        "penalty": penalty,
    }


def broad_scout_envelope_flag(metrics: dict[str, Any], stats: dict[str, Any]) -> bool:
    envelope = f27a.LOCKS["broad_scout_envelope"]
    return bool(
        float(metrics["net_profit"]) > 0
        and float(metrics["profit_factor"]) >= float(envelope["train_profit_factor_min"])
        and float(envelope["train_trades_per_day_min"]) <= float(metrics["trades_per_day"]) <= float(envelope["train_trades_per_day_max"])
        and float(metrics["dd_risk"]) <= float(envelope["train_dd_risk_max"])
        and float(stats["overlap_ratio"]) <= float(envelope["overlap_ratio_max"])
        and float(stats["min_unique_density_contribution"]) >= float(envelope["min_unique_density_contribution_min"])
    )


def dedupe_unions(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, Any]] = []
    for row in candidates:
        key = (str(row["side_value"]), row["micro_key"])
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def evaluate_soft_unions(frame: pd.DataFrame, unions: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for rank, candidate in enumerate(unions, start=1):
        for split in ("train", "validation", "oos"):
            metrics = f23b.evaluate_mask(frame, candidate["mask"], int(candidate["side_value"]), split)
            rows.append({
                "soft_union_id": candidate["soft_union_id"],
                "train_rank": rank,
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
                "micro_train_pf_floor": candidate["micro_train_pf_floor"],
                "micro_train_dd_max": candidate["micro_train_dd_max"],
                "micro_train_r2_floor": candidate["micro_train_r2_floor"],
                "micro_train_max_loss_streak_max": candidate["micro_train_max_loss_streak_max"],
                "micro_adverse_loss_p10_abs_max": candidate["micro_adverse_loss_p10_abs_max"],
                "soft_micro_score_floor": candidate["soft_micro_score_floor"],
                "soft_micro_score_mean": candidate["soft_micro_score_mean"],
                "train_overlap_ratio": candidate["overlap_ratio"],
                "train_union_hits": candidate["train_union_hits"],
                "train_overlap_hits": candidate["train_overlap_hits"],
                "min_unique_density_contribution": candidate["min_unique_density_contribution"],
                "soft_joint_satisfaction_score": candidate["soft_joint_satisfaction_score"],
                "broad_scout_envelope_flag": candidate["broad_scout_envelope_flag"],
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
                "selection_boundary": "train_only_soft_penalty_rank(학습 전용 연성 페널티 순위)" if split == "train" else "read_only_forward_diagnostic(읽기 전용 전방 진단)",
            })
    return pd.DataFrame(rows)


def summarize_soft_unions(metrics: pd.DataFrame) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for union_id, group in metrics.groupby("soft_union_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        base = {
            "soft_union_id": union_id,
            "train_rank": int(train["train_rank"]),
            "union_type": train["union_type"],
            "pocket_count": train["pocket_count"],
            "micro_ids": train["micro_ids"],
            "micro_key": train["micro_key"],
            "source_repair_ids": train["source_repair_ids"],
            "side": train["side"],
            "features": train["features"],
            "feature_families": train["feature_families"],
            "rule_definition": train["rule_definition"],
            "micro_train_pf_floor": train["micro_train_pf_floor"],
            "micro_train_dd_max": train["micro_train_dd_max"],
            "micro_train_r2_floor": train["micro_train_r2_floor"],
            "micro_train_max_loss_streak_max": train["micro_train_max_loss_streak_max"],
            "micro_adverse_loss_p10_abs_max": train["micro_adverse_loss_p10_abs_max"],
            "soft_micro_score_floor": train["soft_micro_score_floor"],
            "soft_micro_score_mean": train["soft_micro_score_mean"],
            "train_overlap_ratio": train["train_overlap_ratio"],
            "min_unique_density_contribution": train["min_unique_density_contribution"],
            "soft_joint_satisfaction_score": train["soft_joint_satisfaction_score"],
            "broad_scout_envelope_flag": bool(train["broad_scout_envelope_flag"]),
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
            min(positive(float(validation["profit_factor"])), 4.0)
            * min(positive(float(oos["profit_factor"])), 4.0)
            * min(float(validation["trades_per_day"]), float(oos["trades_per_day"]), 10.0)
            * (1.0 + min(float(validation["equity_trend_r2"]), float(oos["equity_trend_r2"]), 1.0))
            / (1.0 + forward_max_dd / 10.0 + float(base["train_overlap_ratio"]))
        )
        rows.append(base)
    return pd.DataFrame(rows).sort_values(
        ["handoff_candidate_flag", "seed_surface_flag", "scout_clue_flag", "density_bridge_flag", "forward_read_score"],
        ascending=[False, False, False, False, False],
    )


def build_repeat_audit(summary: pd.DataFrame) -> pd.DataFrame:
    f24_keys, f24_refs = reference_keys(F24B_SUMMARY_TABLE, "bridge_id")
    f25_keys, f25_refs = reference_keys(F25B_SUMMARY_TABLE, "archetype_id")
    f26_keys, f26_refs = reference_keys(F26B_SUMMARY_TABLE, "joint_union_id")
    if not f26_keys:
        f26_keys, f26_refs = reference_keys(F26B_REJECTION_AUDIT, "micro_key")
    rows: list[dict[str, Any]] = []
    top = summary.sort_values("train_rank").head(10) if not summary.empty else pd.DataFrame()
    for _, row in top.iterrows():
        key = row["micro_key"]
        rows.append({
            "f27_soft_union_id": row["soft_union_id"],
            "micro_key": key,
            "in_f24b_top10": key in f24_keys,
            "in_f25b_top10": key in f25_keys,
            "in_f26b_top10_or_rejection": key in f26_keys,
            "f24_reference_id": f24_refs.get(key, ""),
            "f25_reference_id": f25_refs.get(key, ""),
            "f26_reference_id": f26_refs.get(key, ""),
            "f27_forward_min_pf": min(float(row["validation_profit_factor"]), float(row["oos_profit_factor"])),
            "f27_forward_max_dd": max(float(row["validation_dd_risk"]), float(row["oos_dd_risk"])),
            "f27_seed_surface_flag": bool(row["seed_surface_flag"]),
            "nonrepeat_read": "repeat_requires_seed_gap_lift(반복은 씨앗 격차 개선 필요)" if key in (f24_keys | f25_keys | f26_keys) else "new_key(새 키)",
        })
    return pd.DataFrame(rows)


def reference_keys(path: Path, id_column: str) -> tuple[set[str], dict[str, str]]:
    if not path_exists(path):
        return set(), {}
    try:
        frame = pd.read_csv(io_path(path))
    except EmptyDataError:
        return set(), {}
    if frame.empty or "micro_key" not in frame.columns and "micro_ids" not in frame.columns:
        return set(), {}
    top = frame.head(10).copy()
    if "micro_key" not in top.columns:
        top["micro_key"] = top["micro_ids"].map(lambda value: micro_key(str(value).split("|")))
    refs = {str(row["micro_key"]): str(row.get(id_column, row.get("micro_key", ""))) for _, row in top.iterrows()}
    return set(refs), refs


def split_row(group: pd.DataFrame, split: str) -> dict[str, Any]:
    row = group.loc[group["split"].eq(split)]
    if row.empty:
        raise ValueError(f"Missing split row(분할 행 누락): {split}")
    return dict(row.iloc[0])


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    context: dict[str, Any],
    micro_pockets: list[dict[str, Any]],
    micro_audit: pd.DataFrame,
    scored_micros: list[dict[str, Any]],
    unions: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
    repeat_audit: pd.DataFrame,
    source_median_adverse: float,
) -> dict[str, Any]:
    density_count = int(summary["density_bridge_flag"].sum()) if not summary.empty else 0
    scout_count = int(summary["scout_clue_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if not summary.empty else 0
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if not summary.empty else 0
    envelope_count = int(summary["broad_scout_envelope_flag"].sum()) if not summary.empty else 0
    top10_f24_overlap = int(repeat_audit["in_f24b_top10"].sum()) if not repeat_audit.empty else 0
    top10_f25_overlap = int(repeat_audit["in_f25b_top10"].sum()) if not repeat_audit.empty else 0
    top10_f26_overlap = int(repeat_audit["in_f26b_top10_or_rejection"].sum()) if not repeat_audit.empty else 0
    if handoff_count:
        status = "soft_penalty_handoff_candidate_proxy_no_authority"
        judgment = "handoff_candidate_requires_grok_pre_expensive_review_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
    elif seed_count:
        status = "soft_penalty_seed_surface_proxy_no_authority"
        judgment = "seed_surface_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif scout_count:
        status = "soft_penalty_scout_clue_proxy_no_authority"
        judgment = "scout_clue_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif density_count:
        status = "soft_penalty_density_only_proxy_no_authority"
        judgment = "density_only_or_pf_dd_shortfall_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif not unions:
        status = "invalid_setup_soft_penalty_union_surface_zero_no_authority"
        judgment = "invalid_setup_zero_soft_penalty_unions_requires_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    else:
        status = "soft_penalty_no_forward_clue_proxy_no_authority"
        judgment = "negative_or_no_forward_clue_requires_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    best = dict(summary.iloc[0]) if not summary.empty else {}
    construction_pool = min(len(scored_micros), TOP_MICROS_FOR_PAIRS)
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
            "grok_classification": stage_open.get("grok", {}).get("classification", ""),
        },
        "source_median_train_adverse_loss_p10_abs": source_median_adverse,
        "micro_pocket_rows": int(len(micro_pockets)),
        "soft_micro_pool_rows": int(len(micro_audit)),
        "soft_micro_construction_pool_rows": int(construction_pool),
        "soft_union_candidate_rows": int(len(unions)),
        "metric_rows": int(len(metrics)) if not metrics.empty else 0,
        "broad_scout_envelope_rows": envelope_count,
        "density_bridge_rows": density_count,
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "top10_f24b_overlap_count": top10_f24_overlap,
        "top10_f25b_overlap_count": top10_f25_overlap,
        "top10_f26b_overlap_count": top10_f26_overlap,
        "best_soft_union_id": best.get("soft_union_id", ""),
        "best_soft_union": json_ready(best),
        "result_boundary": "soft_joint_satisfaction_penalty_proxy_no_repair_no_wfo_no_mt5_no_runtime_authority(연성 합동 충족 페널티 프록시, 수리/WFO/MT5/런타임 권위 없음)",
        "runtime_probe_status": "pre_expensive_grok_required_before_mt5(비싼 MT5 전 Grok 검토 필요)" if handoff_count else "out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(
    final: dict[str, Any],
    micro_audit: pd.DataFrame,
    unions: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
    repeat_audit: pd.DataFrame,
) -> None:
    micro_audit.to_csv(io_path(RUN_ROOT / "soft_micro_penalty_audit.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame([clean_for_csv(row) for row in unions]).to_csv(
        io_path(RUN_ROOT / "train_ranked_soft_penalty_union_candidates.csv"), index=False, encoding="utf-8-sig"
    )
    metrics.to_csv(io_path(RUN_ROOT / "soft_penalty_union_metrics_by_split.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "soft_penalty_union_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    if not summary.empty:
        summary.sort_values("forward_read_score", ascending=False).head(TOP_FORWARD_ROWS).to_csv(
            io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig"
        )
    else:
        pd.DataFrame().to_csv(io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig")
    repeat_audit.to_csv(io_path(RUN_ROOT / "f24b_f25b_f26b_top10_nonrepeat_audit.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, summary))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F27A_SUMMARY,
        F27A_LOCK,
        F24B_SUMMARY_TABLE,
        F25B_SUMMARY_TABLE,
        F26B_REJECTION_AUDIT,
        RUN_ROOT / "soft_micro_penalty_audit.csv",
        RUN_ROOT / "train_ranked_soft_penalty_union_candidates.csv",
        RUN_ROOT / "soft_penalty_union_metrics_by_split.csv",
        RUN_ROOT / "soft_penalty_union_candidate_summary.csv",
        RUN_ROOT / "f24b_f25b_f26b_top10_nonrepeat_audit.csv",
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
            "source": "full F24 80 micro pocket surface rebuilt from F23C repairs(F23C 수리에서 재구성한 F24 전체 80 미세 구간 표면)",
            "selection": "train-only soft joint satisfaction penalty rank(학습 전용 연성 합동 충족 페널티 순위)",
            "forbidden": "no F26 hard gate numeric relaxation, no validation selection, no ONNX, no MT5 before handoff(F26 경성 게이트 숫자 완화 없음, 검증 선택 없음, 인계 전 ONNX/MT5 없음)",
        },
        "results": {
            "cross_split": {
                "density_bridge_rows": final["density_bridge_rows"],
                "scout_clue_rows": final["scout_clue_rows"],
                "seed_surface_rows": final["seed_surface_rows"],
                "handoff_candidate_rows": final["handoff_candidate_rows"],
                "best_soft_union_id": final["best_soft_union_id"],
                "top10_f24b_overlap_count": final["top10_f24b_overlap_count"],
                "top10_f25b_overlap_count": final["top10_f25b_overlap_count"],
                "top10_f26b_overlap_count": final["top10_f26b_overlap_count"],
            },
            "report_refs": [{"role": "soft_penalty_proxy_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {"schema_version": "frontier27b_soft_penalty_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["best_soft_union"]
    top_rows: list[str] = []
    if not summary.empty:
        for _, row in summary.head(12).iterrows():
            top_rows.append(
                f"| `{row['soft_union_id']}` | `{row['micro_ids']}` | {fmt(row['soft_joint_satisfaction_score'])} | "
                f"{fmt(row['train_profit_factor'])} | {fmt(row['train_trades_per_day'])} | {fmt(row['train_dd_risk'])} | "
                f"{fmt(row['validation_profit_factor'])} | {fmt(row['validation_trades_per_day'])} | {fmt(row['validation_dd_risk'])} | "
                f"{fmt(row['oos_profit_factor'])} | {fmt(row['oos_trades_per_day'])} | {fmt(row['oos_dd_risk'])} | {row['scout_clue_flag']} | {row['seed_surface_flag']} |"
            )
    table = "\n".join(top_rows) if top_rows else "| none(없음) | | | | | | | | | | | | | |"
    return f"""# Frontier27B Soft Joint Satisfaction Penalty Proxy Report(전선27B 연성 합동 충족 페널티 프록시 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F24 full micro pool(F24 전체 미세 풀) `{final['soft_micro_pool_rows']}`개를 train-only soft penalty(학습 전용 연성 페널티)로 점수화하고, 같은 방향 pair/triple OR-union(2/3중 OR 합집합)을 순위화했습니다.

Effect(효과): F26 hard gate relaxation(F26 경성 게이트 완화)을 주 경로로 쓰지 않고, union surface(합집합 표면)가 연성 순위에서 살아나는지 확인했습니다.

Soft micro/construction/union rows(연성 미세/구성/합집합 행): `{final['soft_micro_pool_rows']}` / `{final['soft_micro_construction_pool_rows']}` / `{final['soft_union_candidate_rows']}`

Broad envelope/density/scout/seed/handoff rows(넓은 외피/빈도/탐색/씨앗/인계 행): `{final['broad_scout_envelope_rows']}` / `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Top10 overlap F24/F25/F26(상위10 중복 F24/F25/F26): `{final['top10_f24b_overlap_count']}` / `{final['top10_f25b_overlap_count']}` / `{final['top10_f26b_overlap_count']}`

Best soft union(최상 연성 합집합): `{final['best_soft_union_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best OOS PF/density/DD(최상 OOS 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Top Soft Union Rows(상위 연성 합집합 행)

| union(합집합) | micro ids(미세 ID) | soft score(연성 점수) | train PF | train density | train DD | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier27B Gate Audit(전선27B 게이트 감사)

- scope_completion_gate(범위 완료 게이트): soft penalty artifacts(연성 페널티 산출물) created(생성) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- soft_penalty_contract_gate(연성 페널티 계약 게이트): full micro rows(전체 미세 행) `{final['soft_micro_pool_rows']}`, construction rows(구성 행) `{final['soft_micro_construction_pool_rows']}`
- no_f26_relaxation_primary_path_gate(F26 완화 주 경로 금지 게이트): pass(통과), F27B ranks by soft penalty(F27B는 연성 페널티로 순위화)
- kpi_contract_audit(KPI 계약 감사): split metrics/summary/repeat audit(분할 지표/요약/반복 감사) created(생성)
- non_repeat_gate(반복 방지 게이트): F24/F25/F26 top10 overlap(상위10 중복) `{final['top10_f24b_overlap_count']}` / `{final['top10_f25b_overlap_count']}` / `{final['top10_f26b_overlap_count']}`
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier27 Selection Status(전선27 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest proxy(최근 프록시): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best soft union(최상 연성 합집합): `{final['best_soft_union_id']}`

Soft micro/construction/union rows(연성 미세/구성/합집합 행): `{final['soft_micro_pool_rows']}` / `{final['soft_micro_construction_pool_rows']}` / `{final['soft_union_candidate_rows']}`

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

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
    best = final["best_soft_union"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "soft_penalty_proxy_scout(연성 페널티 프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"micro={final['soft_micro_pool_rows']};construct={final['soft_micro_construction_pool_rows']};union={final['soft_union_candidate_rows']};density={final['density_bridge_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};best={final['best_soft_union_id']};f24overlap={final['top10_f24b_overlap_count']};f25overlap={final['top10_f25b_overlap_count']};f26overlap={final['top10_f26b_overlap_count']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={final['best_soft_union_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "soft_penalty_no_repair_no_wfo_no_mt5_no_authority(연성 페널티, 수리/WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_soft_union"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_soft_penalty_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_soft_penalty_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "soft_penalty_proxy_not_runtime(연성 페널티 프록시, 런타임 아님)",
        "scoreboard_lane": "trade_shape_proxy(거래 형태 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"best={final['best_soft_union_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "proxy_only_no_repair_no_wfo_no_mt5_no_authority(프록시 전용, 수리/WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"micro={final['soft_micro_pool_rows']};construct={final['soft_micro_construction_pool_rows']};union={final['soft_union_candidate_rows']};density={final['density_bridge_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};f24overlap={final['top10_f24b_overlap_count']};f25overlap={final['top10_f25b_overlap_count']};f26overlap={final['top10_f26b_overlap_count']}",
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


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran soft joint satisfaction penalty proxy scout(연성 합동 충족 페널티 프록시 탐색). "
        f"Effect(효과): micro/construct/union(미세/구성/합집합) counts are {final['soft_micro_pool_rows']}/{final['soft_micro_construction_pool_rows']}/{final['soft_union_candidate_rows']}; density/scout/seed/handoff(빈도/탐색/씨앗/인계) counts are {final['density_bridge_rows']}/{final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']} and next run(다음 실행) is `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR27-SOFT-JOINT-SATISFACTION-PENALTY-BRIDGE-UNION-ONNX-SCOUT`: `{RUN_ID}` tested train-only soft penalty rank before union(학습 전용 합집합 전 연성 페널티 순위). "
        f"Effect(효과): best soft union `{final['best_soft_union_id']}` remains proxy-only(프록시 전용) with no authority(권위 없음).\n"
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
    best = final["best_soft_union"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F27B(전선27B)가 train-only soft joint satisfaction penalty before union(학습 전용 합집합 전 연성 합동 충족 페널티)을 실행했습니다.

Effect(효과): F26 hard gate relaxation(F26 경성 게이트 완화)을 주 경로로 쓰지 않고, full 80 micro pool(전체 80 미세 풀)의 penalty rank(페널티 순위)로 합집합 표면을 다시 열었습니다.

Best soft union(최상 연성 합집합): `{final['best_soft_union_id']}` with validation/OOS PF-density-DD(검증/OOS 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def micro_key(values: Any) -> str:
    if isinstance(values, str):
        tokens = [token for token in values.split("|") if token]
    else:
        tokens = [str(token) for token in values]
    return "|".join(sorted(tokens))


def clean_for_csv(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "mask"}


def positive(value: float) -> float:
    if not math.isfinite(value):
        return 4.0
    return max(value, 0.0)


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "pending_or_missing(대기 또는 누락)"}


def sha256_io(path: Path) -> str:
    h = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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
        return "inf"
    return f"{number:.3f}"


if __name__ == "__main__":
    raise SystemExit(main())
