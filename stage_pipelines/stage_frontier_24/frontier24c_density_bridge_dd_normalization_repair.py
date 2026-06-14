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
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_23 import frontier23c_payoff_asymmetry_entry_filter_repair as f23c
from stage_pipelines.stage_frontier_24 import frontier24b_density_bridge_payoff_pockets_proxy_scout as f24b
from stage_pipelines.stage_frontier_24 import materialize_frontier24a_stage_open as f24a


STAGE_ID = f24a.STAGE_ID
RUN_ID = "frontier24C_density_bridge_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier24C"
PARENT_RUN_ID = f24b.RUN_ID
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier24D_grok_pre_expensive_density_bridge_handoff_review_v1"
NEXT_CLOSEOUT_RUN_ID = "frontier24D_stage_closeout_density_bridge_payoff_pockets_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_24/frontier24c_density_bridge_dd_normalization_repair.py")

F24A_SUMMARY = STAGE_ROOT / "02_runs" / f24a.RUN_ID / "stage_open_summary.json"
F24A_LOCK = STAGE_ROOT / "02_runs" / f24a.RUN_ID / "density_bridge_lock.json"
F24B_SUMMARY = STAGE_ROOT / "02_runs" / f24b.RUN_ID / "final_summary.json"
F24B_BRIDGE_SUMMARY = STAGE_ROOT / "02_runs" / f24b.RUN_ID / "bridge_candidate_summary.csv"
F23B_CANDIDATES = (
    Path("stages/stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout/02_runs")
    / f23b.RUN_ID
    / "candidate_summary.csv"
)
F23C_SUMMARY = (
    Path("stages/stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout/02_runs")
    / f23c.RUN_ID
    / "final_summary.json"
)

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

SOURCE_BRIDGE_KEEP = 18
POSITIVE_FILTER_KEEP = 64
RISK_FILTER_KEEP = 64
FILTER_KEEP = 96
MAX_REPAIR_CANDIDATES = 220
MIN_REPAIR_DENSITY = 4.5
MAX_REPAIR_DENSITY = 11.0
MIN_TRAIN_PF = 1.03
MIN_DD_RELIEF_ABS = 0.75
MIN_PF_LIFT = 0.02

SCOUT_PF = f24b.SCOUT_PF
SCOUT_DENSITY_LOW = f24b.SCOUT_DENSITY_LOW
SCOUT_DENSITY_HIGH = f24b.SCOUT_DENSITY_HIGH
SCOUT_DD_CAP = f24b.SCOUT_DD_CAP
SEED_PF = f24b.SEED_PF
SEED_DD_CAP = f24b.SEED_DD_CAP
HANDOFF_PF = f24b.HANDOFF_PF
HANDOFF_DD_CAP = f24b.HANDOFF_DD_CAP
HANDOFF_R2 = f24b.HANDOFF_R2


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F24A_SUMMARY)
    lock = read_json(F24A_LOCK)
    f24b_summary = read_json(F24B_SUMMARY)
    f23c_summary = read_json(F23C_SUMMARY)
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    context = validate_context(stage_open, lock, f24b_summary, f23c_summary, feature_order)
    baselines = f23b.build_unconditional_baselines(frame)
    condition_pool = f23b.build_condition_pool(frame, feature_order, baselines)
    f23b_candidates = pd.read_csv(io_path(F23B_CANDIDATES))
    source_candidates = f23c.rebuild_source_candidates(frame, condition_pool, f23b_candidates)
    f23c_repair_candidates = f23c.build_repair_candidates(frame, condition_pool, source_candidates)
    micro_pockets = f24b.build_micro_pockets(frame, f23c_repair_candidates)
    source_bridges = rebuild_source_bridges(frame, micro_pockets)
    filter_pool = build_filter_pool(condition_pool)
    repair_candidates = build_repair_candidates(frame, source_bridges, filter_pool)
    metrics = evaluate_repair_candidates(frame, repair_candidates)
    summary = summarize_repair(metrics)
    final = build_final(
        created_at,
        stage_open,
        lock,
        f24b_summary,
        context,
        source_bridges,
        filter_pool,
        repair_candidates,
        metrics,
        summary,
    )
    write_outputs(final, source_bridges, filter_pool, repair_candidates, metrics, summary)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "source_bridge_rows": final["source_bridge_rows"],
        "filter_rows": final["filter_rows"],
        "repair_candidate_rows": final["repair_candidate_rows"],
        "density_bridge_rows": final["density_bridge_rows"],
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "best_repair_id": final["best_repair_id"],
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
    f24b_summary: dict[str, Any],
    f23c_summary: dict[str, Any],
    feature_order: list[str],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier24": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_or_current_frontier24c": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_run_matches": stage_open.get("run_id") == f24a.RUN_ID,
        "f24b_parent_matches": f24b_summary.get("run_id") == PARENT_RUN_ID,
        "f24b_density_bridge_available": int(f24b_summary.get("density_bridge_rows", 0)) > 0,
        "f24b_no_handoff_yet": int(f24b_summary.get("handoff_candidate_rows", -1)) == 0,
        "f23c_no_handoff_inherited": int(f23c_summary.get("handoff_candidate_rows", -1)) == 0,
        "same_side_or_lock_present": lock.get("locks", {}).get("structural_unit") == "same_side_multi_pocket_entry_time_or_union",
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "f24b_summary_available": path_exists(F24B_BRIDGE_SUMMARY),
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier24C context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def rebuild_source_bridges(frame: pd.DataFrame, micro_pockets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary = pd.read_csv(io_path(F24B_BRIDGE_SUMMARY))
    if summary.empty:
        raise RuntimeError("Frontier24B bridge summary is empty(F24B 연결 요약이 비어 있음).")
    ordered = summary.copy()
    ordered["_density"] = ordered.get("density_bridge_flag", False).map(as_bool)
    ordered["_forward"] = pd.to_numeric(ordered.get("forward_read_score"), errors="coerce").fillna(-1.0)
    density_only = ordered.loc[ordered["_density"]].copy()
    if not density_only.empty:
        ordered = density_only
    ordered = ordered.sort_values(["_forward"], ascending=[False]).head(SOURCE_BRIDGE_KEEP)
    by_micro_id = {str(pocket["micro_id"]): pocket for pocket in micro_pockets}
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    out: list[dict[str, Any]] = []
    for _, row in ordered.iterrows():
        micro_ids = [token for token in str(row["micro_ids"]).split("|") if token]
        pockets = [by_micro_id[token] for token in micro_ids if token in by_micro_id]
        if len(pockets) != len(micro_ids) or not pockets:
            continue
        if len({int(pocket["side_value"]) for pocket in pockets}) != 1:
            continue
        masks = [np.asarray(pocket["mask"], dtype=bool) for pocket in pockets]
        union_mask = np.logical_or.reduce(masks)
        stats = f24b.overlap_stats(masks, train_mask)
        side_value = int(pockets[0]["side_value"])
        train = f23b.evaluate_mask(frame, union_mask, side_value, "train")
        out.append({
            "source_bridge_id": str(row["bridge_id"]),
            "source_bridge_type": str(row["bridge_type"]),
            "pocket_count": len(pockets),
            "micro_ids": "|".join(micro_ids),
            "source_repair_ids": "|".join(str(pocket["source_repair_id"]) for pocket in pockets),
            "side_value": side_value,
            "side": str(pockets[0]["side"]),
            "features": str(row["features"]),
            "feature_families": str(row["feature_families"]),
            "rule_definition": str(row["rule_definition"]),
            "train_overlap_ratio": stats["overlap_ratio"],
            "min_unique_density_contribution": stats["min_unique_density_contribution"],
            "source_train_profit_factor": train["profit_factor"],
            "source_train_trades_per_day": train["trades_per_day"],
            "source_train_dd_risk": train["dd_risk"],
            "source_validation_profit_factor": as_float(row.get("validation_profit_factor")),
            "source_validation_trades_per_day": as_float(row.get("validation_trades_per_day")),
            "source_validation_dd_risk": as_float(row.get("validation_dd_risk")),
            "source_oos_profit_factor": as_float(row.get("oos_profit_factor")),
            "source_oos_trades_per_day": as_float(row.get("oos_trades_per_day")),
            "source_oos_dd_risk": as_float(row.get("oos_dd_risk")),
            "source_forward_read_score": as_float(row.get("forward_read_score")),
            "source_density_bridge_flag": as_bool(row.get("density_bridge_flag")),
            "source_scout_clue_flag": as_bool(row.get("scout_clue_flag")),
            "source_seed_surface_flag": as_bool(row.get("seed_surface_flag")),
            "mask": union_mask,
        })
    if not out:
        raise RuntimeError("No source bridges could be rebuilt(F24B 연결 후보를 재구성하지 못함).")
    return out


def build_filter_pool(condition_pool: pd.DataFrame) -> pd.DataFrame:
    pool = condition_pool.copy()
    pool["risk_filter_score"] = risk_filter_score(pool)
    positive = (
        pool.loc[pool["sanity_pass"].astype(bool)]
        .sort_values("train_payoff_score", ascending=False)
        .head(POSITIVE_FILTER_KEEP)
        .assign(filter_lane="payoff_positive(보상 양호)")
    )
    risk = (
        pool.sort_values("risk_filter_score", ascending=False)
        .head(RISK_FILTER_KEEP)
        .assign(filter_lane="risk_veto(위험 제외)")
    )
    filters = pd.concat([positive, risk], ignore_index=True)
    filters = filters.drop_duplicates("condition_id", keep="first")
    filters = filters.sort_values(["filter_lane", "train_payoff_score"], ascending=[True, False]).head(FILTER_KEEP)
    return filters.reset_index(drop=True)


def risk_filter_score(pool: pd.DataFrame) -> pd.Series:
    pf = pd.to_numeric(pool.get("train_profit_factor"), errors="coerce").fillna(1.0)
    dd = pd.to_numeric(pool.get("train_dd_risk"), errors="coerce").fillna(0.0)
    uw = pd.to_numeric(pool.get("train_underwater_ratio"), errors="coerce").fillna(0.0)
    streak = pd.to_numeric(pool.get("train_max_loss_streak"), errors="coerce").fillna(0.0)
    coverage = pd.to_numeric(pool.get("train_coverage"), errors="coerce").fillna(0.0)
    poor_pf = (1.05 - pf).clip(lower=0.0)
    return (poor_pf * 3.0 + dd / 18.0 + uw + streak / 18.0) * (0.5 + coverage)


def build_repair_candidates(
    frame: pd.DataFrame,
    source_bridges: list[dict[str, Any]],
    filter_pool: pd.DataFrame,
) -> list[dict[str, Any]]:
    repair_rows: list[dict[str, Any]] = []
    filters = filter_pool.to_dict("records")
    for bridge in source_bridges:
        source_mask = np.asarray(bridge["mask"], dtype=bool)
        source_side = int(bridge["side_value"])
        source_features = feature_tokens(str(bridge["features"]))
        source_train = f23b.evaluate_mask(frame, source_mask, source_side, "train")
        for filter_row in filters:
            if int(filter_row["side_value"]) != source_side:
                continue
            filter_feature = str(filter_row["feature"])
            if filter_feature in source_features:
                continue
            filter_mask = np.asarray(filter_row["_mask"], dtype=bool)
            repair_shapes = (
                ("include", source_mask & filter_mask),
                ("veto", source_mask & ~filter_mask),
            )
            for repair_type, repaired_mask in repair_shapes:
                metrics = f23b.evaluate_mask(frame, repaired_mask, source_side, "train")
                if not train_repair_passes(metrics, source_train):
                    continue
                score = repair_score(metrics, source_train, bridge)
                if score <= 0:
                    continue
                dd_delta = float(source_train["dd_risk"]) - float(metrics["dd_risk"])
                pf_delta = float(metrics["profit_factor"]) - float(source_train["profit_factor"])
                repair_rows.append({
                    "repair_id": f"f24c_{len(repair_rows)+1:04d}",
                    "source_bridge_id": bridge["source_bridge_id"],
                    "source_bridge_type": bridge["source_bridge_type"],
                    "pocket_count": bridge["pocket_count"],
                    "micro_ids": bridge["micro_ids"],
                    "source_repair_ids": bridge["source_repair_ids"],
                    "side_value": source_side,
                    "side": bridge["side"],
                    "features": bridge["features"],
                    "feature_families": bridge["feature_families"],
                    "repair_type": repair_type,
                    "filter_lane": filter_row.get("filter_lane", ""),
                    "filter_condition_id": filter_row["condition_id"],
                    "filter_feature": filter_feature,
                    "filter_family": filter_row["feature_family"],
                    "filter_definition": filter_row["definition"],
                    "rule_definition": repair_rule(bridge["rule_definition"], repair_type, str(filter_row["definition"])),
                    "train_repair_score": score,
                    "source_train_profit_factor": source_train["profit_factor"],
                    "source_train_trades_per_day": source_train["trades_per_day"],
                    "source_train_dd_risk": source_train["dd_risk"],
                    "source_forward_max_dd": max(
                        as_float(bridge["source_validation_dd_risk"]),
                        as_float(bridge["source_oos_dd_risk"]),
                    ),
                    "train_dd_delta": dd_delta,
                    "train_pf_delta": pf_delta,
                    "train_selection_metrics": metrics,
                    "mask": repaired_mask,
                })
    repair_rows.sort(key=lambda row: float(row["train_repair_score"]), reverse=True)
    selected = repair_rows[:MAX_REPAIR_CANDIDATES]
    for index, row in enumerate(selected, start=1):
        row["repair_id"] = f"f24c_{index:04d}"
    return selected


def train_repair_passes(metrics: dict[str, Any], source_train: dict[str, Any]) -> bool:
    if metrics["net_profit"] <= 0 or metrics["profit_factor"] < MIN_TRAIN_PF:
        return False
    if not (MIN_REPAIR_DENSITY <= metrics["trades_per_day"] <= MAX_REPAIR_DENSITY):
        return False
    dd_delta = float(source_train["dd_risk"]) - float(metrics["dd_risk"])
    pf_delta = float(metrics["profit_factor"]) - float(source_train["profit_factor"])
    if dd_delta < MIN_DD_RELIEF_ABS and pf_delta < MIN_PF_LIFT:
        return False
    return True


def repair_score(metrics: dict[str, Any], source_train: dict[str, Any], bridge: dict[str, Any]) -> float:
    source_dd = max(float(source_train["dd_risk"]), 1.0)
    dd_relief = max(float(source_train["dd_risk"]) - float(metrics["dd_risk"]), 0.0) / source_dd
    pf_lift = max(float(metrics["profit_factor"]) - float(source_train["profit_factor"]), 0.0)
    density_penalty = abs(float(metrics["trades_per_day"]) - 7.5) / 7.5
    dd_penalty = max(0.0, float(metrics["dd_risk"]) - 14.0) / 18.0
    overlap_penalty = float(bridge["train_overlap_ratio"]) * 1.2
    return float(
        max(float(metrics["net_profit"]), 0.0)
        * min(float(metrics["profit_factor"]), 4.0)
        * min(float(metrics["payoff_ratio"]), 4.0)
        * min(float(metrics["trades_per_day"]), 11.0)
        * (1.0 + dd_relief * 2.0 + pf_lift)
        / (1.0 + density_penalty + dd_penalty + overlap_penalty)
    )


def evaluate_repair_candidates(frame: pd.DataFrame, candidates: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for rank, candidate in enumerate(candidates, start=1):
        for split in ("train", "validation", "oos"):
            metrics = f23b.evaluate_mask(frame, candidate["mask"], int(candidate["side_value"]), split)
            rows.append({
                "repair_id": candidate["repair_id"],
                "train_rank": rank,
                "source_bridge_id": candidate["source_bridge_id"],
                "source_bridge_type": candidate["source_bridge_type"],
                "pocket_count": candidate["pocket_count"],
                "micro_ids": candidate["micro_ids"],
                "source_repair_ids": candidate["source_repair_ids"],
                "side": candidate["side"],
                "side_value": candidate["side_value"],
                "features": candidate["features"],
                "feature_families": candidate["feature_families"],
                "repair_type": candidate["repair_type"],
                "filter_lane": candidate["filter_lane"],
                "filter_condition_id": candidate["filter_condition_id"],
                "filter_feature": candidate["filter_feature"],
                "filter_family": candidate["filter_family"],
                "rule_definition": candidate["rule_definition"],
                "source_train_profit_factor": candidate["source_train_profit_factor"],
                "source_train_trades_per_day": candidate["source_train_trades_per_day"],
                "source_train_dd_risk": candidate["source_train_dd_risk"],
                "source_forward_max_dd": candidate["source_forward_max_dd"],
                "train_dd_delta": candidate["train_dd_delta"],
                "train_pf_delta": candidate["train_pf_delta"],
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
                "selection_boundary": "train_only_repair_rank(학습 전용 수리 순위)" if split == "train" else "read_only_forward_diagnostic(읽기 전용 전진 진단)",
            })
    return pd.DataFrame(rows)


def summarize_repair(metrics: pd.DataFrame) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for repair_id, group in metrics.groupby("repair_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        base = {
            "repair_id": repair_id,
            "train_rank": int(train["train_rank"]),
            "source_bridge_id": train["source_bridge_id"],
            "source_bridge_type": train["source_bridge_type"],
            "pocket_count": train["pocket_count"],
            "micro_ids": train["micro_ids"],
            "source_repair_ids": train["source_repair_ids"],
            "side": train["side"],
            "features": train["features"],
            "feature_families": train["feature_families"],
            "repair_type": train["repair_type"],
            "filter_lane": train["filter_lane"],
            "filter_feature": train["filter_feature"],
            "filter_family": train["filter_family"],
            "rule_definition": train["rule_definition"],
            "source_train_profit_factor": train["source_train_profit_factor"],
            "source_train_trades_per_day": train["source_train_trades_per_day"],
            "source_train_dd_risk": train["source_train_dd_risk"],
            "source_forward_max_dd": train["source_forward_max_dd"],
            "train_dd_delta": train["train_dd_delta"],
            "train_pf_delta": train["train_pf_delta"],
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
        base["forward_dd_relief"] = max(float(base["source_forward_max_dd"]) - forward_max_dd, 0.0)
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
            * (1.0 + min(base["forward_dd_relief"], 20.0) / 20.0)
            / (1.0 + forward_max_dd / 10.0)
        )
        rows.append(base)
    return pd.DataFrame(rows).sort_values(
        ["handoff_candidate_flag", "seed_surface_flag", "scout_clue_flag", "density_bridge_flag", "forward_read_score"],
        ascending=[False, False, False, False, False],
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
    f24b_summary: dict[str, Any],
    context: dict[str, Any],
    source_bridges: list[dict[str, Any]],
    filter_pool: pd.DataFrame,
    repair_candidates: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, Any]:
    density_count = int(summary["density_bridge_flag"].sum()) if not summary.empty else 0
    scout_count = int(summary["scout_clue_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if not summary.empty else 0
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if not summary.empty else 0
    if handoff_count:
        status = "density_bridge_dd_repair_handoff_candidate_proxy_no_authority"
        judgment = "handoff_candidate_requires_grok_pre_expensive_review_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
    elif seed_count:
        status = "density_bridge_dd_repair_seed_surface_proxy_no_authority"
        judgment = "seed_surface_preserved_clue_requires_closeout_no_authority"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
    elif scout_count:
        status = "density_bridge_dd_repair_scout_clue_proxy_no_authority"
        judgment = "scout_clue_preserved_clue_requires_closeout_no_authority"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
    elif density_count:
        status = "density_bridge_dd_repair_frequency_only_proxy_no_authority"
        judgment = "density_bridge_remains_pf_or_dd_shortfall_requires_closeout_no_authority"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
    else:
        status = "density_bridge_dd_repair_no_forward_clue_proxy_no_authority"
        judgment = "repair_failed_to_preserve_density_bridge_requires_closeout_no_authority"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
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
        "f24b_summary": {
            "status": f24b_summary.get("status"),
            "judgment": f24b_summary.get("judgment"),
            "density_bridge_rows": f24b_summary.get("density_bridge_rows"),
            "scout_clue_rows": f24b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f24b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f24b_summary.get("handoff_candidate_rows"),
            "best_bridge_id": f24b_summary.get("best_bridge_id"),
        },
        "lock_summary": {
            "structural_unit": lock.get("locks", {}).get("structural_unit"),
            "duplicate_trade_rule": lock.get("locks", {}).get("duplicate_trade_rule"),
            "density_first": lock.get("locks", {}).get("density_first"),
        },
        "source_bridge_rows": int(len(source_bridges)),
        "filter_rows": int(len(filter_pool)),
        "repair_candidate_rows": int(len(repair_candidates)),
        "metric_rows": int(len(metrics)) if not metrics.empty else 0,
        "density_bridge_rows": density_count,
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "best_repair_id": best.get("repair_id", ""),
        "best_repair": json_ready(best),
        "result_boundary": "capped_density_bridge_dd_repair_proxy_no_wfo_no_mt5_no_runtime_authority(상한 있는 빈도 연결 손실폭 수리 프록시, WFO/MT5/런타임 권위 없음)",
        "runtime_probe_status": "pre_expensive_grok_required_before_mt5(비싼 MT5 전 Grok 검토 필요)" if handoff_count else "out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(
    final: dict[str, Any],
    source_bridges: list[dict[str, Any]],
    filter_pool: pd.DataFrame,
    repair_candidates: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    pd.DataFrame([clean_source_bridge_for_csv(row) for row in source_bridges]).to_csv(
        io_path(RUN_ROOT / "source_bridges_rebuilt.csv"), index=False, encoding="utf-8-sig"
    )
    filter_pool.drop(columns=["_mask"], errors="ignore").to_csv(
        io_path(RUN_ROOT / "filter_pool.csv"), index=False, encoding="utf-8-sig"
    )
    pd.DataFrame([clean_repair_for_csv(row) for row in repair_candidates]).to_csv(
        io_path(RUN_ROOT / "train_ranked_repair_candidates.csv"), index=False, encoding="utf-8-sig"
    )
    metrics.to_csv(io_path(RUN_ROOT / "repair_metrics_by_split.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "repair_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    if not summary.empty:
        summary.sort_values("forward_read_score", ascending=False).head(30).to_csv(
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
        F24A_SUMMARY,
        F24A_LOCK,
        F24B_SUMMARY,
        F24B_BRIDGE_SUMMARY,
        F23C_SUMMARY,
        RUN_ROOT / "source_bridges_rebuilt.csv",
        RUN_ROOT / "filter_pool.csv",
        RUN_ROOT / "train_ranked_repair_candidates.csv",
        RUN_ROOT / "repair_metrics_by_split.csv",
        RUN_ROOT / "repair_candidate_summary.csv",
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
            "source": "F24B density bridge source(F24B 빈도 연결 원천)",
            "repair": "train-only include/veto entry-time filter(학습 전용 포함/제외 진입 시점 필터)",
            "forbidden": "no lifecycle repair, no ONNX, no MT5 before handoff(인계 전 생명주기 수리/ONNX/MT5 없음)",
        },
        "results": {
            "cross_split": {
                "density_bridge_rows": final["density_bridge_rows"],
                "scout_clue_rows": final["scout_clue_rows"],
                "seed_surface_rows": final["seed_surface_rows"],
                "handoff_candidate_rows": final["handoff_candidate_rows"],
                "best_repair_id": final["best_repair_id"],
            },
            "report_refs": [{"role": "density_bridge_dd_repair_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {"schema_version": "frontier24c_density_bridge_dd_repair_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["best_repair"]
    top_rows: list[str] = []
    if not summary.empty:
        for _, row in summary.head(12).iterrows():
            top_rows.append(
                f"| `{row['repair_id']}` | `{row['source_bridge_id']}` | {row['repair_type']} | `{row['filter_feature']}` | "
                f"{fmt(row['validation_profit_factor'])} | {fmt(row['validation_trades_per_day'])} | {fmt(row['validation_dd_risk'])} | "
                f"{fmt(row['oos_profit_factor'])} | {fmt(row['oos_trades_per_day'])} | {fmt(row['oos_dd_risk'])} | "
                f"{fmt(row['forward_dd_relief'])} | {row['scout_clue_flag']} | {row['seed_surface_flag']} |"
            )
    table = "\n".join(top_rows) if top_rows else "| none(없음) | | | | | | | | | | | | | |"
    return f"""# Frontier24C Density Bridge DD Repair Report(전선24C 빈도 연결 손실폭 수리 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F24B(전선24B)의 density bridge(빈도 연결) 후보에 train-only include/veto filter(학습 전용 포함/제외 필터)를 붙여 DD(drawdown, 손실폭) normalization repair(정규화 수리)를 실행했습니다.

Effect(효과): trade frequency(거래 빈도)를 유지한 상태에서 PF(profit factor, 수익 팩터)와 DD(drawdown, 손실폭)가 함께 좋아지는지 확인했습니다.

Source/filter/repair/metric rows(원천/필터/수리/지표 행): `{final['source_bridge_rows']}` / `{final['filter_rows']}` / `{final['repair_candidate_rows']}` / `{final['metric_rows']}`

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Best repair(최상 수리): `{final['best_repair_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Top Repair Rows(상위 수리 행)

| repair(수리) | source bridge(원천 연결) | type(유형) | filter(필터) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | DD relief | scout | seed |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier24C Gate Audit(전선24C 게이트 감사)

- scope_completion_gate(범위 완료 게이트): repair artifacts(수리 산출물) created(생성) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- capped_repair_gate(상한 수리 게이트): source bridges(원천 연결) `{final['source_bridge_rows']}`, filters(필터) `{final['filter_rows']}`, repair candidates(수리 후보) `{final['repair_candidate_rows']}`
- no_lifecycle_before_handoff_gate(인계 전 생명주기 금지 게이트): pass(통과), only entry-time include/veto filters(진입 시점 포함/제외 필터만 사용)
- kpi_contract_audit(KPI 계약 감사): repair metrics/summary(수리 지표/요약) created(생성)
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier24 Selection Status(전선24 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest repair(최근 수리): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best repair(최상 수리): `{final['best_repair_id']}`

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 not_claimed(주장 없음)입니다.
"""


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    best = final["best_repair"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "density_bridge_dd_repair(빈도 연결 손실폭 수리)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"density={final['density_bridge_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};best={final['best_repair_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={final['best_repair_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "capped_dd_repair_no_wfo_no_mt5_no_authority(상한 손실폭 수리, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_repair"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_dd_repair_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_dd_repair_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "density_bridge_dd_repair_not_runtime(빈도 연결 손실폭 수리, 런타임 아님)",
        "scoreboard_lane": "trade_shape_proxy(거래 형태 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"best={final['best_repair_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "proxy_only_no_wfo_no_mt5_no_authority(프록시 전용, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"density={final['density_bridge_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']}",
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
        "external_verification_status": "not_applicable_proxy_no_mt5(프록시라 MT5 없음)",
        "notes": "Combined source absent(합산 원천 없음)",
    }
    return [primary, tier_b, combined]


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran capped density bridge DD repair(상한 있는 빈도 연결 손실폭 수리). "
        f"Effect(효과): density/scout/seed/handoff(빈도/탐색/씨앗/인계) counts are {final['density_bridge_rows']}/{final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']} and next run(다음 실행) is `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR24-DENSITY-BRIDGE-PAYOFF-POCKETS-ONNX-SCOUT`: `{RUN_ID}` applied capped DD normalization repair(상한 있는 손실폭 정규화 수리). "
        f"Effect(효과): best repair `{final['best_repair_id']}` remains proxy-only(프록시 전용) with no authority(권위 없음).\n"
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
    best = final["best_repair"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F24C(전선24C)가 F24B density bridge(전선24B 빈도 연결)에 capped DD normalization repair(상한 있는 손실폭 정규화 수리)를 적용했습니다.

Effect(효과): ONNX(온엑스)나 MT5(메타트레이더5) 없이 proxy(프록시) 수준에서 frequency/PF/DD/smoothness(빈도/수익 팩터/손실폭/매끄러움)가 함께 개선되는지 확인했습니다.

Best repair(최상 수리): `{final['best_repair_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def feature_tokens(features: str) -> set[str]:
    return {token.strip() for token in features.replace(" || ", "|").split("|") if token.strip()}


def repair_rule(source_rule: str, repair_type: str, filter_definition: str) -> str:
    joiner = "AND" if repair_type == "include" else "AND NOT"
    return f"({source_rule}) {joiner} ({filter_definition})"


def clean_source_bridge_for_csv(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "mask"}


def clean_repair_for_csv(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key not in {"mask", "train_selection_metrics"}}


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


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def fmt(value: Any) -> str:
    number = as_float(value)
    return "NA" if not math.isfinite(number) else f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
