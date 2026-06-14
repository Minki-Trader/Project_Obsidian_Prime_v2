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
from stage_pipelines.stage_frontier_26 import materialize_frontier26a_stage_open as f26a


STAGE_ID = f26a.STAGE_ID
RUN_ID = "frontier26B_joint_micro_satisfaction_before_bridge_union_proxy_scout_v1"
RUN_NUMBER = "frontier26B"
PARENT_RUN_ID = f26a.RUN_ID
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier26C_grok_pre_expensive_joint_micro_handoff_review_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier26C_joint_micro_satisfaction_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_26/frontier26b_joint_micro_satisfaction_proxy_scout.py")

F26A_SUMMARY = STAGE_ROOT / "02_runs" / f26a.RUN_ID / "stage_open_summary.json"
F26A_LOCK = STAGE_ROOT / "02_runs" / f26a.RUN_ID / "joint_micro_satisfaction_lock.json"
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

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

MICRO_MIN_PF = float(f26a.LOCKS["micro_gate_contract"]["train_profit_factor_min"])
MICRO_MAX_DD = float(f26a.LOCKS["micro_gate_contract"]["train_dd_risk_max"])
MICRO_MIN_DENSITY = float(f26a.LOCKS["micro_gate_contract"]["train_trades_per_day_min"])
MICRO_MAX_DENSITY = float(f26a.LOCKS["micro_gate_contract"]["train_trades_per_day_max"])
MICRO_MIN_R2 = float(f26a.LOCKS["micro_gate_contract"]["train_equity_trend_r2_min"])
MICRO_MAX_LOSS_STREAK = int(f26a.LOCKS["micro_gate_contract"]["train_max_loss_streak_max"])

UNION_MIN_PF = float(f26a.LOCKS["union_gate_contract"]["train_profit_factor_min"])
UNION_MAX_DD = float(f26a.LOCKS["union_gate_contract"]["train_dd_risk_max"])
UNION_MIN_DENSITY = float(f26a.LOCKS["union_gate_contract"]["train_trades_per_day_min"])
UNION_MAX_DENSITY = float(f26a.LOCKS["union_gate_contract"]["train_trades_per_day_max"])
MAX_OVERLAP_RATIO = float(f26a.LOCKS["union_gate_contract"]["overlap_ratio_max"])
MIN_UNIQUE_DENSITY_CONTRIB = float(f26a.LOCKS["union_gate_contract"]["min_unique_density_contribution_min"])

TOP_FORWARD_ROWS = 30
SCOUT_PF = f26a.CRITERIA["scout_clue"]["pf"]
SCOUT_DENSITY_LOW = f26a.CRITERIA["scout_clue"]["density_low"]
SCOUT_DENSITY_HIGH = f26a.CRITERIA["scout_clue"]["density_high"]
SCOUT_DD_CAP = f26a.CRITERIA["scout_clue"]["dd_cap"]
SEED_PF = f26a.CRITERIA["seed_surface"]["pf"]
SEED_DD_CAP = f26a.CRITERIA["seed_surface"]["dd_cap"]
HANDOFF_PF = f26a.CRITERIA["handoff_candidate"]["pf"]
HANDOFF_DD_CAP = f26a.CRITERIA["handoff_candidate"]["dd_cap"]
HANDOFF_R2 = f26a.CRITERIA["handoff_candidate"]["equity_trend_r2"]


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F26A_SUMMARY)
    lock = read_json(F26A_LOCK)
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    context = validate_context(stage_open, lock, feature_order)
    baselines = f23b.build_unconditional_baselines(frame)
    condition_pool = f23b.build_condition_pool(frame, feature_order, baselines)
    f23b_candidates = pd.read_csv(io_path(f24b.F23B_CANDIDATES))
    source_candidates = f23c.rebuild_source_candidates(frame, condition_pool, f23b_candidates)
    f23c_repair_candidates = f23c.build_repair_candidates(frame, condition_pool, source_candidates)
    micro_pockets = f24b.build_micro_pockets(frame, f23c_repair_candidates)
    micro_audit, passers, source_median_adverse = build_micro_joint_pass_audit(micro_pockets)
    union_rejection_audit = build_joint_union_rejection_audit(frame, passers)
    unions = build_joint_unions(frame, passers, source_median_adverse)
    metrics = evaluate_joint_unions(frame, unions)
    summary = summarize_joint_unions(metrics)
    repeat_audit = build_repeat_audit(summary)
    final = build_final(
        created_at,
        stage_open,
        context,
        micro_pockets,
        micro_audit,
        unions,
        union_rejection_audit,
        metrics,
        summary,
        repeat_audit,
        source_median_adverse,
    )
    write_outputs(final, micro_audit, unions, union_rejection_audit, metrics, summary, repeat_audit)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "micro_pocket_rows": final["micro_pocket_rows"],
        "joint_micro_pass_rows": final["joint_micro_pass_rows"],
        "joint_union_candidate_rows": final["joint_union_candidate_rows"],
        "density_bridge_rows": final["density_bridge_rows"],
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "top10_f24b_overlap_count": final["top10_f24b_overlap_count"],
        "top10_f25b_overlap_count": final["top10_f25b_overlap_count"],
        "best_joint_union_id": final["best_joint_union_id"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_context(stage_open: dict[str, Any], lock: dict[str, Any], feature_order: list[str]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    lock_body = lock.get("locks", {})
    checks = {
        "workspace_current_stage_frontier26": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_or_current_frontier26b": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_run_matches_parent": stage_open.get("run_id") == PARENT_RUN_ID,
        "lock_changed_variable_joint_micro": lock_body.get("changed_variable") == "joint_micro_satisfaction_before_bridge_union",
        "lock_no_repair_frontier26b": "no_repair_in_frontier26b" in lock_body,
        "lock_selection_train_only": lock_body.get("selection_split") == "train_only",
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_exists": path_exists(f23b.DATASET_PATH),
        "f24b_reference_table_available": path_exists(F24B_SUMMARY_TABLE),
        "f25b_reference_table_available": path_exists(F25B_SUMMARY_TABLE),
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier26B context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def build_micro_joint_pass_audit(micro_pockets: list[dict[str, Any]]) -> tuple[pd.DataFrame, list[dict[str, Any]], float]:
    adverse_values = [float(pocket["train_adverse_loss_p10_abs"]) for pocket in micro_pockets]
    source_median_adverse = float(np.nanmedian(adverse_values)) if adverse_values else math.nan
    rows: list[dict[str, Any]] = []
    passers: list[dict[str, Any]] = []
    for pocket in micro_pockets:
        row = clean_micro_for_csv(pocket)
        pf = float(pocket["train_profit_factor"])
        dd = float(pocket["train_dd_risk"])
        density = float(pocket["train_trades_per_day"])
        r2 = float(pocket["train_equity_trend_r2"])
        loss_streak = int(pocket["train_max_loss_streak"])
        adverse = float(pocket["train_adverse_loss_p10_abs"])
        checks = {
            "pass_train_pf": pf >= MICRO_MIN_PF,
            "pass_train_dd": dd <= MICRO_MAX_DD,
            "pass_train_density": MICRO_MIN_DENSITY <= density <= MICRO_MAX_DENSITY,
            "pass_train_equity_r2": r2 >= MICRO_MIN_R2,
            "pass_train_max_loss_streak": loss_streak <= MICRO_MAX_LOSS_STREAK,
            "pass_train_adverse_loss_p10_abs": adverse <= source_median_adverse,
        }
        joint_pass = all(checks.values())
        joint_score = micro_joint_score(pocket, source_median_adverse)
        row.update(checks)
        row.update({
            "source_median_train_adverse_loss_p10_abs": source_median_adverse,
            "joint_micro_pass_flag": bool(joint_pass),
            "joint_micro_satisfaction_score": joint_score,
            "selection_boundary": "train_only_micro_joint_gate(학습 전용 미세 구간 합동 게이트)",
        })
        rows.append(row)
        if joint_pass:
            enriched = dict(pocket)
            enriched["joint_micro_satisfaction_score"] = joint_score
            passers.append(enriched)
    passers.sort(key=lambda row: float(row["joint_micro_satisfaction_score"]), reverse=True)
    return pd.DataFrame(rows), passers, source_median_adverse


def micro_joint_score(pocket: dict[str, Any], source_median_adverse: float) -> float:
    pf_term = min(float(pocket["train_profit_factor"]) / MICRO_MIN_PF, 2.0)
    dd_margin = max(0.0, MICRO_MAX_DD - float(pocket["train_dd_risk"])) / MICRO_MAX_DD
    density_mid = (MICRO_MIN_DENSITY + MICRO_MAX_DENSITY) / 2.0
    density_fit = 1.0 / (1.0 + abs(float(pocket["train_trades_per_day"]) - density_mid) / density_mid)
    r2_term = max(float(pocket["train_equity_trend_r2"]), 0.0)
    streak_term = max(0.0, MICRO_MAX_LOSS_STREAK - float(pocket["train_max_loss_streak"])) / MICRO_MAX_LOSS_STREAK
    adverse_margin = max(0.0, source_median_adverse - float(pocket["train_adverse_loss_p10_abs"])) / max(source_median_adverse, 1e-9)
    return float(pf_term * (1.0 + dd_margin) * density_fit * (1.0 + r2_term) * (1.0 + streak_term) * (1.0 + adverse_margin))


def build_joint_unions(frame: pd.DataFrame, passers: list[dict[str, Any]], source_median_adverse: float) -> list[dict[str, Any]]:
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    rows: list[dict[str, Any]] = []
    for size in (2, 3):
        for pockets in itertools.combinations(passers, size):
            maybe = joint_union_from_pockets(frame, pockets, train_mask, "pair" if size == 2 else "triple", source_median_adverse)
            if maybe is not None:
                rows.append(maybe)
    rows.sort(key=lambda row: float(row["joint_micro_satisfaction_score"]), reverse=True)
    for index, row in enumerate(rows, start=1):
        row["joint_union_id"] = f"f26b_{index:04d}"
    return rows


def build_joint_union_rejection_audit(frame: pd.DataFrame, passers: list[dict[str, Any]]) -> pd.DataFrame:
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    rows: list[dict[str, Any]] = []
    for size in (2, 3):
        for pockets in itertools.combinations(passers, size):
            family_tokens: list[str] = []
            for pocket in pockets:
                family_tokens.extend(str(pocket["feature_families"]).split("|"))
            family_set = sorted(set(family_tokens))
            side_values = {int(pocket["side_value"]) for pocket in pockets}
            masks = [np.asarray(pocket["mask"], dtype=bool) for pocket in pockets]
            stats = f24b.overlap_stats(masks, train_mask)
            union_mask = np.logical_or.reduce(masks)
            side_value = int(pockets[0]["side_value"])
            train = f23b.evaluate_mask(frame, union_mask, side_value, "train")
            checks = {
                "pass_same_side": len(side_values) == 1,
                "pass_family_diversity": len(family_set) >= 2
                and (max(family_tokens.count(family) for family in family_set) <= 4 if family_set else False),
                "pass_overlap_ratio": stats["overlap_ratio"] <= MAX_OVERLAP_RATIO,
                "pass_min_unique_density": stats["min_unique_density_contribution"] >= MIN_UNIQUE_DENSITY_CONTRIB,
                "pass_train_net_profit": train["net_profit"] > 0,
                "pass_train_profit_factor": train["profit_factor"] >= UNION_MIN_PF,
                "pass_train_density": UNION_MIN_DENSITY <= train["trades_per_day"] <= UNION_MAX_DENSITY,
                "pass_train_dd_risk": float(train["dd_risk"]) <= UNION_MAX_DD,
            }
            pass_flag = all(checks.values())
            rows.append({
                "union_type": "pair" if size == 2 else "triple",
                "micro_ids": "|".join(str(pocket["micro_id"]) for pocket in pockets),
                "micro_key": micro_key(pocket["micro_id"] for pocket in pockets),
                "side_values": "|".join(str(value) for value in sorted(side_values)),
                "feature_families": "|".join(family_set),
                "train_overlap_ratio": stats["overlap_ratio"],
                "min_unique_density_contribution": stats["min_unique_density_contribution"],
                "train_profit_factor": train["profit_factor"],
                "train_trades_per_day": train["trades_per_day"],
                "train_dd_risk": train["dd_risk"],
                "train_net_profit": train["net_profit"],
                **checks,
                "joint_union_pass_flag": bool(pass_flag),
                "failure_reason": "|".join(key for key, value in checks.items() if not value),
                "selection_boundary": "train_only_union_gate_rejection_audit(학습 전용 합집합 게이트 거절 감사)",
            })
    return pd.DataFrame(rows)


def joint_union_from_pockets(
    frame: pd.DataFrame,
    pockets: tuple[dict[str, Any], ...],
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
    if stats["overlap_ratio"] > MAX_OVERLAP_RATIO:
        return None
    if stats["min_unique_density_contribution"] < MIN_UNIQUE_DENSITY_CONTRIB:
        return None
    side_value = int(pockets[0]["side_value"])
    train = f23b.evaluate_mask(frame, union_mask, side_value, "train")
    if train["net_profit"] <= 0 or train["profit_factor"] < UNION_MIN_PF:
        return None
    if not (UNION_MIN_DENSITY <= train["trades_per_day"] <= UNION_MAX_DENSITY):
        return None
    if float(train["dd_risk"]) > UNION_MAX_DD:
        return None
    score = joint_union_score(train, stats, pockets, source_median_adverse)
    return {
        "joint_union_id": "pending",
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
        "micro_joint_score_floor": min(float(pocket["joint_micro_satisfaction_score"]) for pocket in pockets),
        "joint_micro_satisfaction_score": score,
        **stats,
        **{f"train_{key}": value for key, value in train.items()},
        "mask": union_mask,
    }


def joint_union_score(metrics: dict[str, Any], stats: dict[str, Any], pockets: tuple[dict[str, Any], ...], source_median_adverse: float) -> float:
    micro_pf_floor = min(float(pocket["train_profit_factor"]) for pocket in pockets)
    micro_dd_margin = min(max(0.0, MICRO_MAX_DD - float(pocket["train_dd_risk"])) / MICRO_MAX_DD for pocket in pockets)
    micro_r2_floor = min(max(float(pocket["train_equity_trend_r2"]), 0.0) for pocket in pockets)
    adverse_max = max(float(pocket["train_adverse_loss_p10_abs"]) for pocket in pockets)
    adverse_margin = max(0.0, source_median_adverse - adverse_max) / max(source_median_adverse, 1e-9)
    density_mid = (UNION_MIN_DENSITY + UNION_MAX_DENSITY) / 2.0
    density_fit = 1.0 / (1.0 + abs(float(metrics["trades_per_day"]) - density_mid) / density_mid)
    union_pf = min(float(metrics["profit_factor"]), 3.0)
    union_dd_margin = max(0.0, UNION_MAX_DD - float(metrics["dd_risk"])) / UNION_MAX_DD
    unique_term = max(float(stats["min_unique_density_contribution"]), 0.0)
    overlap_penalty = float(stats["overlap_ratio"]) * 1.5
    density_penalty = abs(float(metrics["trades_per_day"]) - density_mid) / density_mid
    return float(
        min(micro_pf_floor / MICRO_MIN_PF, 2.0)
        * (1.0 + micro_dd_margin)
        * (1.0 + micro_r2_floor)
        * (1.0 + adverse_margin)
        * union_pf
        * (1.0 + union_dd_margin)
        * density_fit
        * unique_term
        / (1.0 + overlap_penalty + density_penalty)
    )


def evaluate_joint_unions(frame: pd.DataFrame, unions: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for rank, candidate in enumerate(unions, start=1):
        for split in ("train", "validation", "oos"):
            metrics = f23b.evaluate_mask(frame, candidate["mask"], int(candidate["side_value"]), split)
            rows.append({
                "joint_union_id": candidate["joint_union_id"],
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
                "micro_joint_score_floor": candidate["micro_joint_score_floor"],
                "train_overlap_ratio": candidate["overlap_ratio"],
                "train_union_hits": candidate["train_union_hits"],
                "train_overlap_hits": candidate["train_overlap_hits"],
                "min_unique_density_contribution": candidate["min_unique_density_contribution"],
                "joint_micro_satisfaction_score": candidate["joint_micro_satisfaction_score"],
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
                "selection_boundary": "train_only_joint_union_rank(학습 전용 합동 합집합 순위)" if split == "train" else "read_only_forward_diagnostic(읽기 전용 전진 진단)",
            })
    return pd.DataFrame(rows)


def summarize_joint_unions(metrics: pd.DataFrame) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for union_id, group in metrics.groupby("joint_union_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        base = {
            "joint_union_id": union_id,
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
            "micro_joint_score_floor": train["micro_joint_score_floor"],
            "train_overlap_ratio": train["train_overlap_ratio"],
            "min_unique_density_contribution": train["min_unique_density_contribution"],
            "joint_micro_satisfaction_score": train["joint_micro_satisfaction_score"],
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
            min(validation["profit_factor"], 4.0)
            * min(oos["profit_factor"], 4.0)
            * min(validation["trades_per_day"], oos["trades_per_day"], 10.0)
            * (1.0 + min(validation["equity_trend_r2"], oos["equity_trend_r2"], 1.0))
            / (1.0 + forward_max_dd / 10.0)
        )
        rows.append(base)
    return pd.DataFrame(rows).sort_values(
        ["handoff_candidate_flag", "seed_surface_flag", "scout_clue_flag", "density_bridge_flag", "forward_read_score"],
        ascending=[False, False, False, False, False],
    )


def build_repeat_audit(summary: pd.DataFrame) -> pd.DataFrame:
    f24_top = pd.read_csv(io_path(F24B_SUMMARY_TABLE)).head(10).copy()
    f25_top = pd.read_csv(io_path(F25B_SUMMARY_TABLE)).head(10).copy()
    f24_top["_key"] = f24_top["micro_ids"].map(lambda value: micro_key(str(value).split("|")))
    f25_top["_key"] = f25_top["micro_ids"].map(lambda value: micro_key(str(value).split("|")))
    f24_keys = set(f24_top["_key"])
    f25_keys = set(f25_top["_key"])
    rows: list[dict[str, Any]] = []
    top = summary.sort_values("train_rank").head(10) if not summary.empty else pd.DataFrame()
    for _, row in top.iterrows():
        key = row["micro_key"]
        match25 = f25_top.loc[f25_top["_key"].eq(key)]
        match24 = f24_top.loc[f24_top["_key"].eq(key)]
        f26_forward_max_dd = max(float(row["validation_dd_risk"]), float(row["oos_dd_risk"]))
        f25_forward_max_dd = (
            max(float(match25.iloc[0]["validation_dd_risk"]), float(match25.iloc[0]["oos_dd_risk"]))
            if not match25.empty
            else math.nan
        )
        rows.append({
            "f26_joint_union_id": row["joint_union_id"],
            "micro_key": key,
            "in_f24b_top10": bool(key in f24_keys),
            "in_f25b_top10": bool(key in f25_keys),
            "f26_validation_profit_factor": row["validation_profit_factor"],
            "f26_oos_profit_factor": row["oos_profit_factor"],
            "f26_forward_min_pf": min(float(row["validation_profit_factor"]), float(row["oos_profit_factor"])),
            "f26_forward_max_dd": f26_forward_max_dd,
            "f25_forward_max_dd_if_matched": f25_forward_max_dd if not match25.empty else "",
            "forward_dd_lift_vs_f25_if_matched": (f25_forward_max_dd - f26_forward_max_dd) if not match25.empty else "",
            "f24_match_bridge_id": match24.iloc[0]["bridge_id"] if not match24.empty else "",
            "f25_match_archetype_id": match25.iloc[0]["archetype_id"] if not match25.empty else "",
        })
    return pd.DataFrame(rows)


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
    unions: list[dict[str, Any]],
    union_rejection_audit: pd.DataFrame,
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
    repeat_audit: pd.DataFrame,
    source_median_adverse: float,
) -> dict[str, Any]:
    density_count = int(summary["density_bridge_flag"].sum()) if not summary.empty else 0
    scout_count = int(summary["scout_clue_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if not summary.empty else 0
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if not summary.empty else 0
    pass_count = int(micro_audit["joint_micro_pass_flag"].sum()) if not micro_audit.empty else 0
    top10_f24_overlap = int(repeat_audit["in_f24b_top10"].sum()) if not repeat_audit.empty else 0
    top10_f25_overlap = int(repeat_audit["in_f25b_top10"].sum()) if not repeat_audit.empty else 0
    if handoff_count:
        status = "joint_micro_handoff_candidate_proxy_no_authority"
        judgment = "handoff_candidate_requires_grok_pre_expensive_review_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
    elif seed_count:
        status = "joint_micro_seed_surface_proxy_no_authority"
        judgment = "seed_surface_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif scout_count:
        status = "joint_micro_scout_clue_proxy_no_authority"
        judgment = "scout_clue_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif density_count:
        status = "joint_micro_density_only_proxy_no_authority"
        judgment = "density_only_or_pf_dd_shortfall_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif pass_count == 0:
        status = "invalid_setup_joint_gate_collapsed_no_authority"
        judgment = "invalid_setup_zero_joint_micro_passers_requires_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif not unions:
        status = "invalid_setup_joint_union_collapsed_no_authority"
        judgment = "invalid_setup_zero_joint_unions_requires_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    else:
        status = "joint_micro_no_forward_clue_proxy_no_authority"
        judgment = "negative_or_no_forward_clue_requires_closeout_no_authority"
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
        "context": context,
        "stage_open": {
            "status": stage_open.get("status"),
            "judgment": stage_open.get("judgment"),
            "grok_classification": stage_open.get("grok", {}).get("classification", ""),
        },
        "source_median_train_adverse_loss_p10_abs": source_median_adverse,
        "micro_pocket_rows": int(len(micro_pockets)),
        "joint_micro_pass_rows": pass_count,
        "joint_union_attempt_rows": int(len(union_rejection_audit)),
        "joint_union_rejection_counts": (
            union_rejection_audit["failure_reason"].value_counts(dropna=False).to_dict()
            if not union_rejection_audit.empty
            else {}
        ),
        "joint_union_candidate_rows": int(len(unions)),
        "metric_rows": int(len(metrics)) if not metrics.empty else 0,
        "density_bridge_rows": density_count,
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "top10_f24b_overlap_count": top10_f24_overlap,
        "top10_f25b_overlap_count": top10_f25_overlap,
        "best_joint_union_id": best.get("joint_union_id", ""),
        "best_joint_union": json_ready(best),
        "result_boundary": "joint_micro_satisfaction_proxy_no_repair_no_wfo_no_mt5_no_runtime_authority(미세 구간 합동 충족 프록시, 수리/WFO/MT5/런타임 권위 없음)",
        "runtime_probe_status": "pre_expensive_grok_required_before_mt5(비싼 MT5 전 Grok 검토 필요)" if handoff_count else "out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(
    final: dict[str, Any],
    micro_audit: pd.DataFrame,
    unions: list[dict[str, Any]],
    union_rejection_audit: pd.DataFrame,
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
    repeat_audit: pd.DataFrame,
) -> None:
    micro_audit.to_csv(io_path(RUN_ROOT / "micro_joint_pass_audit.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame([clean_union_for_csv(row) for row in unions]).to_csv(
        io_path(RUN_ROOT / "train_ranked_joint_union_candidates.csv"), index=False, encoding="utf-8-sig"
    )
    union_rejection_audit.to_csv(io_path(RUN_ROOT / "joint_union_rejection_audit.csv"), index=False, encoding="utf-8-sig")
    metrics.to_csv(io_path(RUN_ROOT / "joint_union_metrics_by_split.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "joint_union_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    if not summary.empty:
        summary.sort_values("forward_read_score", ascending=False).head(TOP_FORWARD_ROWS).to_csv(
            io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig"
        )
    else:
        pd.DataFrame().to_csv(io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig")
    repeat_audit.to_csv(io_path(RUN_ROOT / "f24b_f25b_top10_nonrepeat_audit.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, summary))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F26A_SUMMARY,
        F26A_LOCK,
        F24B_SUMMARY_TABLE,
        F25B_SUMMARY_TABLE,
        RUN_ROOT / "micro_joint_pass_audit.csv",
        RUN_ROOT / "joint_union_rejection_audit.csv",
        RUN_ROOT / "train_ranked_joint_union_candidates.csv",
        RUN_ROOT / "joint_union_metrics_by_split.csv",
        RUN_ROOT / "joint_union_candidate_summary.csv",
        RUN_ROOT / "f24b_f25b_top10_nonrepeat_audit.csv",
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
            "source": "F24 micro pocket assembly rebuilt from F23C repairs(F24 미세 구간 조립을 F23C 수리에서 재구성)",
            "selection": "train-only joint micro satisfaction before union(학습 전용 합집합 전 미세 구간 합동 충족)",
            "forbidden": "no validation selection, no capped repair in F26B, no ONNX, no MT5 before handoff(검증 선택 없음, F26B 상한 수리 없음, 인계 전 ONNX/MT5 없음)",
        },
        "results": {
            "cross_split": {
                "density_bridge_rows": final["density_bridge_rows"],
                "scout_clue_rows": final["scout_clue_rows"],
                "seed_surface_rows": final["seed_surface_rows"],
                "handoff_candidate_rows": final["handoff_candidate_rows"],
                "best_joint_union_id": final["best_joint_union_id"],
                "top10_f24b_overlap_count": final["top10_f24b_overlap_count"],
                "top10_f25b_overlap_count": final["top10_f25b_overlap_count"],
            },
            "report_refs": [{"role": "joint_micro_satisfaction_proxy_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {"schema_version": "frontier26b_joint_micro_satisfaction_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["best_joint_union"]
    top_rows: list[str] = []
    if not summary.empty:
        for _, row in summary.head(12).iterrows():
            top_rows.append(
                f"| `{row['joint_union_id']}` | `{row['micro_ids']}` | {fmt(row['micro_train_pf_floor'])} | {fmt(row['micro_train_dd_max'])} | "
                f"{fmt(row['train_profit_factor'])} | {fmt(row['train_dd_risk'])} | "
                f"{fmt(row['validation_profit_factor'])} | {fmt(row['validation_trades_per_day'])} | {fmt(row['validation_dd_risk'])} | "
                f"{fmt(row['oos_profit_factor'])} | {fmt(row['oos_trades_per_day'])} | {fmt(row['oos_dd_risk'])} | {row['scout_clue_flag']} | {row['seed_surface_flag']} |"
            )
    table = "\n".join(top_rows) if top_rows else "| none(없음) | | | | | | | | | | | | | | |"
    return f"""# Frontier26B Joint Micro Satisfaction Proxy Report(전선26B 미세 구간 합동 충족 프록시 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F24 micro pockets(F24 미세 구간)을 재구성하고, 각 micro pocket(미세 구간)이 train-only PF/DD/density/R2/streak/adverse-loss(학습 전용 수익 팩터/손실폭/빈도/R2/연패/불리한 손실)을 동시에 통과한 뒤에만 same-side pair/triple OR-union(같은 방향 쌍/삼중 OR 합집합)을 만들었습니다.

Effect(효과): F25(전선25)의 union-level DD-headroom-first ranking(합집합 수준 손실폭 여유 우선 순위)을 반복하지 않고, union before admission(합집합 전 유입) 품질이 seed DD gap(씨앗 손실폭 간격)을 줄이는지 확인했습니다.

Micro/pass/union attempts/valid union/metric rows(미세/통과/합집합 시도/유효 합집합/지표 행): `{final['micro_pocket_rows']}` / `{final['joint_micro_pass_rows']}` / `{final['joint_union_attempt_rows']}` / `{final['joint_union_candidate_rows']}` / `{final['metric_rows']}`

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

F24B/F25B top10 overlap(F24B/F25B 상위10 중복): `{final['top10_f24b_overlap_count']}` / `{final['top10_f25b_overlap_count']}`

Best joint union(최상 합동 합집합): `{final['best_joint_union_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Top Joint Union Rows(상위 합동 합집합 행)

| union(합집합) | micro ids(미세 ID) | micro PF floor | micro DD max | train PF | train DD | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier26B Gate Audit(전선26B 게이트 감사)

- scope_completion_gate(범위 완료 게이트): joint micro artifacts(합동 미세 구간 산출물) created(생성) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- micro_gate_contract(미세 구간 게이트 계약): pass rows(통과 행) `{final['joint_micro_pass_rows']}` from source rows(원천 행) `{final['micro_pocket_rows']}`
- union_gate_contract(합집합 게이트 계약): attempt/valid rows(시도/유효 행) `{final['joint_union_attempt_rows']}` / `{final['joint_union_candidate_rows']}`
- kpi_contract_audit(KPI 계약 감사): joint union metrics/summary/repeat audit(합동 합집합 지표/요약/반복 감사) created(생성)
- no_repair_primary_path_gate(기본 경로 수리 금지 게이트): pass(통과), F26B applies no capped repair(F26B는 상한 수리 미적용)
- non_repeat_gate(반복 방지 게이트): F24B/F25B top10 overlap(F24B/F25B 상위10 중복) `{final['top10_f24b_overlap_count']}` / `{final['top10_f25b_overlap_count']}`
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier26 Selection Status(전선26 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest proxy(최근 프록시): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best joint union(최상 합동 합집합): `{final['best_joint_union_id']}`

Micro/pass/union attempt/valid rows(미세/통과/합집합 시도/유효 행): `{final['micro_pocket_rows']}` / `{final['joint_micro_pass_rows']}` / `{final['joint_union_attempt_rows']}` / `{final['joint_union_candidate_rows']}`

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
    best = final["best_joint_union"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "joint_micro_satisfaction_proxy_scout(미세 구간 합동 충족 프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"pass={final['joint_micro_pass_rows']};attempt={final['joint_union_attempt_rows']};union={final['joint_union_candidate_rows']};density={final['density_bridge_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};best={final['best_joint_union_id']};f24overlap={final['top10_f24b_overlap_count']};f25overlap={final['top10_f25b_overlap_count']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={final['best_joint_union_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "joint_micro_satisfaction_no_repair_no_wfo_no_mt5_no_authority(미세 구간 합동 충족, 수리/WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_joint_union"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_joint_micro_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_joint_micro_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "joint_micro_satisfaction_proxy_not_runtime(미세 구간 합동 충족 프록시, 런타임 아님)",
        "scoreboard_lane": "trade_shape_proxy(거래 형태 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"best={final['best_joint_union_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "proxy_only_no_repair_no_wfo_no_mt5_no_authority(프록시 전용, 수리/WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"pass={final['joint_micro_pass_rows']};attempt={final['joint_union_attempt_rows']};union={final['joint_union_candidate_rows']};density={final['density_bridge_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};f24overlap={final['top10_f24b_overlap_count']};f25overlap={final['top10_f25b_overlap_count']}",
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
        "notes": "Tier B source absent(Tier B 원천 없음)",
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
        f"- {final['created_at_utc']}: `{RUN_ID}` ran joint micro satisfaction proxy scout(미세 구간 합동 충족 프록시 탐색). "
        f"Effect(효과): micro/pass/attempt/union(미세/통과/시도/합집합) counts are {final['micro_pocket_rows']}/{final['joint_micro_pass_rows']}/{final['joint_union_attempt_rows']}/{final['joint_union_candidate_rows']}; density/scout/seed/handoff(빈도/탐색/씨앗/인계) counts are {final['density_bridge_rows']}/{final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']} and next run(다음 실행) is `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR26-JOINT-MICRO-SATISFACTION-BEFORE-UNION-ONNX-SCOUT`: `{RUN_ID}` tested train-only joint micro satisfaction before union(학습 전용 합집합 전 미세 구간 합동 충족). "
        f"Effect(효과): best joint union `{final['best_joint_union_id']}` remains proxy-only(프록시 전용) with no authority(권위 없음).\n"
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
    best = final["best_joint_union"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F26B(전선26B)가 train-only joint micro satisfaction before union(학습 전용 합집합 전 미세 구간 합동 충족)을 실행했습니다.

Effect(효과): F25(전선25)의 union-level ranking(합집합 수준 순위) 반복이 아니라, 합집합에 들어가기 전 micro pocket(미세 구간) 품질을 먼저 시험했습니다.

Best joint union(최상 합동 합집합): `{final['best_joint_union_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def micro_key(values: Any) -> str:
    if isinstance(values, str):
        tokens = [token for token in values.split("|") if token]
    else:
        tokens = [str(token) for token in values]
    return "|".join(sorted(tokens))


def clean_micro_for_csv(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "mask"}


def clean_union_for_csv(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "mask"}


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
        return "NA"
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
