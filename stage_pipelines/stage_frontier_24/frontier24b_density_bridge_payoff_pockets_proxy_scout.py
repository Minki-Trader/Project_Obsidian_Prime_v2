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
from foundation.models.onnx_bridge import ordered_hash, sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_23 import frontier23c_payoff_asymmetry_entry_filter_repair as f23c
from stage_pipelines.stage_frontier_24 import materialize_frontier24a_stage_open as f24a


STAGE_ID = f24a.STAGE_ID
RUN_ID = "frontier24B_density_bridge_payoff_pockets_proxy_scout_v1"
RUN_NUMBER = "frontier24B"
PARENT_RUN_ID = f24a.RUN_ID
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier24C_grok_pre_expensive_density_bridge_handoff_review_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier24C_density_bridge_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_24/frontier24b_density_bridge_payoff_pockets_proxy_scout.py")

F24A_SUMMARY = STAGE_ROOT / "02_runs" / f24a.RUN_ID / "stage_open_summary.json"
F24A_LOCK = STAGE_ROOT / "02_runs" / f24a.RUN_ID / "density_bridge_lock.json"
F23B_CANDIDATES = Path("stages/stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout/02_runs") / f23b.RUN_ID / "candidate_summary.csv"
F23C_SUMMARY = Path("stages/stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout/02_runs") / f23c.RUN_ID / "final_summary.json"
F23C_CANDIDATES = Path("stages/stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout/02_runs") / f23c.RUN_ID / "repair_candidate_summary.csv"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

MICRO_KEEP = 80
PAIR_CAP = 120
TRIPLE_CAP = 80
FINAL_CANDIDATE_CAP = 180
MIN_MICRO_TRAIN_PF = 1.10
MIN_MICRO_DENSITY = 1.0
MAX_MICRO_DENSITY = 6.5
MIN_BRIDGE_DENSITY = 4.0
MAX_BRIDGE_DENSITY = 11.5
MAX_OVERLAP_RATIO = 0.55
MIN_UNIQUE_DENSITY_CONTRIB = 0.35

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
    stage_open = read_json(F24A_SUMMARY)
    lock = read_json(F24A_LOCK)
    f23c_summary = read_json(F23C_SUMMARY)
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    context = validate_context(stage_open, lock, f23c_summary, feature_order)
    baselines = f23b.build_unconditional_baselines(frame)
    condition_pool = f23b.build_condition_pool(frame, feature_order, baselines)
    f23b_candidates = pd.read_csv(io_path(F23B_CANDIDATES))
    source_candidates = f23c.rebuild_source_candidates(frame, condition_pool, f23b_candidates)
    repair_candidates = f23c.build_repair_candidates(frame, condition_pool, source_candidates)
    micro_pockets = build_micro_pockets(frame, repair_candidates)
    bridge_candidates = build_bridge_candidates(frame, micro_pockets)
    metrics = evaluate_bridge_candidates(frame, bridge_candidates)
    summary = summarize_bridge(metrics)
    final = build_final(created_at, stage_open, lock, context, micro_pockets, bridge_candidates, metrics, summary)
    write_outputs(final, micro_pockets, bridge_candidates, metrics, summary)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "micro_pocket_rows": final["micro_pocket_rows"],
        "bridge_candidate_rows": final["bridge_candidate_rows"],
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "best_bridge_id": final["best_bridge_id"],
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
    f23c_summary: dict[str, Any],
    feature_order: list[str],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier24": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier24b": f"next_run_id: {RUN_ID}" in workspace,
        "stage_open_run_matches_parent": stage_open.get("run_id") == PARENT_RUN_ID,
        "f23c_seed_handoff_zero": int(f23c_summary.get("seed_surface_rows", -1)) == 0
        and int(f23c_summary.get("handoff_candidate_rows", -1)) == 0,
        "or_union_lock_present": lock.get("locks", {}).get("structural_unit") == "same_side_multi_pocket_entry_time_or_union",
        "duplicate_trade_rule_present": "duplicate_trade_rule" in lock.get("locks", {}),
        "density_first_lock_present": "density_first" in lock.get("locks", {}),
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_exists": path_exists(f23b.DATASET_PATH),
        "f23c_candidates_available": path_exists(F23C_CANDIDATES),
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier24B context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def build_micro_pockets(frame: pd.DataFrame, repair_candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    pockets: list[dict[str, Any]] = []
    for candidate in repair_candidates:
        train = f23b.evaluate_mask(frame, candidate["mask"], int(candidate["side_value"]), "train")
        if train["net_profit"] <= 0 or train["profit_factor"] < MIN_MICRO_TRAIN_PF:
            continue
        if not (MIN_MICRO_DENSITY <= train["trades_per_day"] <= MAX_MICRO_DENSITY):
            continue
        features = feature_list(candidate)
        families = sorted({f23b.feature_family(feature) for feature in features})
        score = micro_score(train, len(families))
        pockets.append({
            "micro_id": f"f24p_{len(pockets)+1:04d}",
            "source_repair_id": candidate["repair_id"],
            "source_candidate_id": candidate["source_candidate_id"],
            "side_value": int(candidate["side_value"]),
            "side": candidate["side"],
            "features": "|".join(features),
            "feature_families": "|".join(families),
            "rule_definition": candidate["rule_definition"],
            "repair_type": candidate["repair_type"],
            "filter_feature": candidate["filter_feature"],
            "train_micro_score": score,
            "train_hit_count": int(np.asarray(candidate["mask"], dtype=bool)[train_mask].sum()),
            **{f"train_{key}": value for key, value in train.items()},
            "mask": np.asarray(candidate["mask"], dtype=bool),
        })
    pockets.sort(key=lambda item: float(item["train_micro_score"]), reverse=True)
    selected = pockets[:MICRO_KEEP]
    for index, pocket in enumerate(selected, start=1):
        pocket["micro_id"] = f"f24p_{index:04d}"
    return selected


def micro_score(metrics: dict[str, Any], family_count: int) -> float:
    density_target_penalty = abs(float(metrics["trades_per_day"]) - 3.5) / 3.5
    dd_penalty = max(0.0, float(metrics["dd_risk"]) - 18.0) / 25.0
    diversity_bonus = 1.0 + min(family_count, 4) * 0.08
    return float(
        diversity_bonus
        * max(float(metrics["net_profit"]), 0.0)
        * min(float(metrics["profit_factor"]), 4.0)
        * min(float(metrics["payoff_ratio"]), 4.0)
        / (1.0 + density_target_penalty + dd_penalty)
    )


def build_bridge_candidates(frame: pd.DataFrame, micro_pockets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    top_pair = micro_pockets[: min(len(micro_pockets), 45)]
    for left, right in itertools.combinations(top_pair, 2):
        maybe = bridge_from_pockets(frame, [left, right], train_mask, "pair")
        if maybe is not None:
            candidates.append(maybe)
    candidates.sort(key=lambda item: float(item["train_bridge_score"]), reverse=True)
    pair_kept = candidates[:PAIR_CAP]
    triple_candidates: list[dict[str, Any]] = []
    top_add = micro_pockets[: min(len(micro_pockets), 40)]
    for pair in pair_kept[:45]:
        existing_ids = set(str(pair["micro_ids"]).split("|"))
        existing = [pocket for pocket in micro_pockets if pocket["micro_id"] in existing_ids]
        for add in top_add:
            if add["micro_id"] in existing_ids:
                continue
            if add["side_value"] != existing[0]["side_value"]:
                continue
            maybe = bridge_from_pockets(frame, existing + [add], train_mask, "triple")
            if maybe is not None:
                triple_candidates.append(maybe)
    triple_candidates.sort(key=lambda item: float(item["train_bridge_score"]), reverse=True)
    all_candidates = pair_kept + triple_candidates[:TRIPLE_CAP]
    all_candidates.sort(key=lambda item: float(item["train_bridge_score"]), reverse=True)
    selected = dedupe_bridges(all_candidates)[:FINAL_CANDIDATE_CAP]
    for index, row in enumerate(selected, start=1):
        row["bridge_id"] = f"f24b_{index:04d}"
    return selected


def bridge_from_pockets(
    frame: pd.DataFrame,
    pockets: list[dict[str, Any]],
    train_mask: np.ndarray,
    bridge_type: str,
) -> dict[str, Any] | None:
    if len({int(pocket["side_value"]) for pocket in pockets}) != 1:
        return None
    family_tokens: list[str] = []
    for pocket in pockets:
        family_tokens.extend(str(pocket["feature_families"]).split("|"))
    if len(set(family_tokens)) < 2:
        return None
    max_same_family = max(family_tokens.count(family) for family in set(family_tokens))
    if max_same_family > 4:
        return None
    masks = [np.asarray(pocket["mask"], dtype=bool) for pocket in pockets]
    union_mask = np.logical_or.reduce(masks)
    stats = overlap_stats(masks, train_mask)
    if stats["overlap_ratio"] > MAX_OVERLAP_RATIO:
        return None
    if stats["min_unique_density_contribution"] < MIN_UNIQUE_DENSITY_CONTRIB:
        return None
    train = f23b.evaluate_mask(frame, union_mask, int(pockets[0]["side_value"]), "train")
    if train["net_profit"] <= 0 or train["profit_factor"] < 1.06:
        return None
    if not (MIN_BRIDGE_DENSITY <= train["trades_per_day"] <= MAX_BRIDGE_DENSITY):
        return None
    score = bridge_score(train, stats, len(set(family_tokens)), len(pockets))
    return {
        "bridge_id": "pending",
        "bridge_type": bridge_type,
        "pocket_count": len(pockets),
        "micro_ids": "|".join(str(pocket["micro_id"]) for pocket in pockets),
        "source_repair_ids": "|".join(str(pocket["source_repair_id"]) for pocket in pockets),
        "side_value": int(pockets[0]["side_value"]),
        "side": pockets[0]["side"],
        "features": " || ".join(str(pocket["features"]) for pocket in pockets),
        "feature_families": "|".join(sorted(set(family_tokens))),
        "rule_definition": " OR ".join(f"({pocket['rule_definition']})" for pocket in pockets),
        "train_bridge_score": score,
        **stats,
        **{f"train_{key}": value for key, value in train.items()},
        "mask": union_mask,
    }


def overlap_stats(masks: list[np.ndarray], train_mask: np.ndarray) -> dict[str, Any]:
    scoped = [np.asarray(mask, dtype=bool) & train_mask for mask in masks]
    union = np.logical_or.reduce(scoped)
    sum_hits = int(sum(mask.sum() for mask in scoped))
    union_hits = int(union.sum())
    overlap_hits = max(0, sum_hits - union_hits)
    unique_counts: list[int] = []
    for index, mask in enumerate(scoped):
        others = [other for other_index, other in enumerate(scoped) if other_index != index]
        other_union = np.logical_or.reduce(others) if others else np.zeros_like(mask, dtype=bool)
        unique_counts.append(int((mask & ~other_union).sum()))
    train_days = 573.0
    return {
        "train_sum_hits": sum_hits,
        "train_union_hits": union_hits,
        "train_overlap_hits": overlap_hits,
        "overlap_ratio": float(overlap_hits / sum_hits) if sum_hits else 0.0,
        "unique_contribution_min_hits": min(unique_counts) if unique_counts else 0,
        "unique_contribution_min_ratio": float(min(unique_counts) / union_hits) if union_hits and unique_counts else 0.0,
        "min_unique_density_contribution": float((min(unique_counts) if unique_counts else 0) / train_days),
    }


def bridge_score(metrics: dict[str, Any], stats: dict[str, Any], family_count: int, pocket_count: int) -> float:
    density_penalty = abs(float(metrics["trades_per_day"]) - 7.5) / 7.5
    dd_penalty = max(0.0, float(metrics["dd_risk"]) - 14.0) / 18.0
    overlap_penalty = float(stats["overlap_ratio"]) * 1.5
    diversity_bonus = 1.0 + min(family_count, 6) * 0.08
    pocket_penalty = max(0, pocket_count - 3) * 0.15
    return float(
        diversity_bonus
        * max(float(metrics["net_profit"]), 0.0)
        * min(float(metrics["profit_factor"]), 4.0)
        * min(float(metrics["payoff_ratio"]), 4.0)
        * min(float(metrics["trades_per_day"]), 12.0)
        / (1.0 + density_penalty + dd_penalty + overlap_penalty + pocket_penalty)
    )


def dedupe_bridges(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, Any]] = []
    for row in candidates:
        key = (str(row["side_value"]), "|".join(sorted(str(row["micro_ids"]).split("|"))))
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def evaluate_bridge_candidates(frame: pd.DataFrame, candidates: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for rank, candidate in enumerate(candidates, start=1):
        for split in ("train", "validation", "oos"):
            metrics = f23b.evaluate_mask(frame, candidate["mask"], int(candidate["side_value"]), split)
            rows.append({
                "bridge_id": candidate["bridge_id"],
                "train_rank": rank,
                "bridge_type": candidate["bridge_type"],
                "pocket_count": candidate["pocket_count"],
                "micro_ids": candidate["micro_ids"],
                "source_repair_ids": candidate["source_repair_ids"],
                "side": candidate["side"],
                "side_value": candidate["side_value"],
                "features": candidate["features"],
                "feature_families": candidate["feature_families"],
                "rule_definition": candidate["rule_definition"],
                "train_overlap_ratio": candidate["overlap_ratio"],
                "train_union_hits": candidate["train_union_hits"],
                "train_overlap_hits": candidate["train_overlap_hits"],
                "min_unique_density_contribution": candidate["min_unique_density_contribution"],
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
                "selection_boundary": "train_only_bridge_rank(학습 전용 연결 순위)" if split == "train" else "read_only_forward_diagnostic(읽기 전용 전진 진단)",
            })
    return pd.DataFrame(rows)


def summarize_bridge(metrics: pd.DataFrame) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for bridge_id, group in metrics.groupby("bridge_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        base = {
            "bridge_id": bridge_id,
            "train_rank": int(train["train_rank"]),
            "bridge_type": train["bridge_type"],
            "pocket_count": train["pocket_count"],
            "micro_ids": train["micro_ids"],
            "source_repair_ids": train["source_repair_ids"],
            "side": train["side"],
            "features": train["features"],
            "feature_families": train["feature_families"],
            "rule_definition": train["rule_definition"],
            "train_overlap_ratio": train["train_overlap_ratio"],
            "train_union_hits": train["train_union_hits"],
            "train_overlap_hits": train["train_overlap_hits"],
            "min_unique_density_contribution": train["min_unique_density_contribution"],
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
            and max(validation["dd_risk"], oos["dd_risk"]) <= SCOUT_DD_CAP
        )
        base["seed_surface_flag"] = bool(
            base["scout_clue_flag"]
            and validation["profit_factor"] >= SEED_PF
            and oos["profit_factor"] >= SEED_PF
            and max(validation["dd_risk"], oos["dd_risk"]) <= SEED_DD_CAP
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
            and max(validation["dd_risk"], oos["dd_risk"]) <= HANDOFF_DD_CAP
            and base["smoothness_proxy_pass"]
        )
        base["forward_read_score"] = float(
            min(validation["profit_factor"], 4.0)
            * min(oos["profit_factor"], 4.0)
            * min(validation["trades_per_day"], oos["trades_per_day"], 10.0)
            * (1.0 + min(validation["equity_trend_r2"], oos["equity_trend_r2"], 1.0))
            / (1.0 + max(validation["dd_risk"], oos["dd_risk"]) / 10.0 + float(base["train_overlap_ratio"]))
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
    context: dict[str, Any],
    micro_pockets: list[dict[str, Any]],
    bridge_candidates: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, Any]:
    scout_count = int(summary["scout_clue_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if not summary.empty else 0
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if not summary.empty else 0
    density_count = int(summary["density_bridge_flag"].sum()) if not summary.empty else 0
    if handoff_count:
        status = "density_bridge_handoff_candidate_proxy_no_authority"
        judgment = "handoff_candidate_requires_grok_pre_expensive_review_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
    elif seed_count:
        status = "density_bridge_seed_surface_proxy_no_authority"
        judgment = "seed_surface_requires_repair_or_pre_expensive_decision_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif scout_count:
        status = "density_bridge_scout_clue_proxy_no_authority"
        judgment = "scout_clue_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif density_count:
        status = "density_bridge_frequency_only_proxy_no_authority"
        judgment = "density_clue_pf_or_dd_shortfall_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    else:
        status = "density_bridge_no_forward_clue_proxy_no_authority"
        judgment = "negative_pressure_requires_closeout_no_authority"
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
        "lock_summary": {
            "structural_unit": lock.get("locks", {}).get("structural_unit"),
            "duplicate_trade_rule": lock.get("locks", {}).get("duplicate_trade_rule"),
            "density_first": lock.get("locks", {}).get("density_first"),
        },
        "micro_pocket_rows": int(len(micro_pockets)),
        "bridge_candidate_rows": int(len(bridge_candidates)),
        "metric_rows": int(len(metrics)) if not metrics.empty else 0,
        "density_bridge_rows": density_count,
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "best_bridge_id": best.get("bridge_id", ""),
        "best_bridge": json_ready(best),
        "result_boundary": "same_side_or_union_density_bridge_proxy_no_wfo_no_mt5_no_runtime_authority(같은 방향 OR 합집합 빈도 연결 프록시, WFO/MT5/런타임 권위 없음)",
        "runtime_probe_status": "pre_expensive_grok_required_before_mt5(비싼 MT5 전 그록 검토 필요)" if handoff_count else "out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(
    final: dict[str, Any],
    micro_pockets: list[dict[str, Any]],
    bridge_candidates: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> None:
    pd.DataFrame([clean_micro_for_csv(row) for row in micro_pockets]).to_csv(io_path(RUN_ROOT / "micro_pockets.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame([clean_bridge_for_csv(row) for row in bridge_candidates]).to_csv(io_path(RUN_ROOT / "train_ranked_bridge_candidates.csv"), index=False, encoding="utf-8-sig")
    metrics.to_csv(io_path(RUN_ROOT / "bridge_metrics_by_split.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "bridge_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    if not summary.empty:
        summary.sort_values("forward_read_score", ascending=False).head(30).to_csv(io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig")
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
        F23C_SUMMARY,
        F23C_CANDIDATES,
        RUN_ROOT / "micro_pockets.csv",
        RUN_ROOT / "train_ranked_bridge_candidates.csv",
        RUN_ROOT / "bridge_metrics_by_split.csv",
        RUN_ROOT / "bridge_candidate_summary.csv",
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
            "micro_pocket_lineage": "rederived_from_f23c_entry_filter_candidates(전선23C 진입 필터 후보에서 재파생)",
            "bridge": "same_side_entry_time_or_union(같은 방향 진입시점 OR 합집합)",
            "duplicate_trade_rule": "one_trade_per_timestamp(타임스탬프당 한 거래)",
            "selection": "train_only_density_bridge_rank(학습 전용 빈도 연결 순위)",
            "forbidden": "no_lifecycle_no_onnx_no_mt5_before_handoff(인계 전 생명주기/ONNX/MT5 없음)",
        },
        "results": {
            "cross_split": {
                "density_bridge_rows": final["density_bridge_rows"],
                "scout_clue_rows": final["scout_clue_rows"],
                "seed_surface_rows": final["seed_surface_rows"],
                "handoff_candidate_rows": final["handoff_candidate_rows"],
                "best_bridge_id": final["best_bridge_id"],
            },
            "report_refs": [{"role": "density_bridge_proxy_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {"schema_version": "frontier24b_density_bridge_proxy_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["best_bridge"]
    top_rows: list[str] = []
    if not summary.empty:
        for _, row in summary.head(12).iterrows():
            top_rows.append(
                f"| `{row['bridge_id']}` | {row['bridge_type']} | {row['pocket_count']} | {row['side']} | "
                f"{fmt(row['validation_profit_factor'])} | {fmt(row['validation_trades_per_day'])} | {fmt(row['validation_dd_risk'])} | "
                f"{fmt(row['oos_profit_factor'])} | {fmt(row['oos_trades_per_day'])} | {fmt(row['oos_dd_risk'])} | "
                f"{fmt(row['train_overlap_ratio'])} | {row['scout_clue_flag']} | {row['seed_surface_flag']} |"
            )
    table = "\n".join(top_rows) if top_rows else "| none(없음) | | | | | | | | | | | | |"
    return f"""# Frontier24B Density Bridge Payoff Pockets Proxy Scout Report(전선24B 빈도 연결 보상 구간 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F23C(전선23C)에서 파생한 micro-pocket(미세 구간)을 같은 방향 OR-union bridge(OR 합집합 연결)로 조립했습니다.

Effect(효과): timestamp(타임스탬프) 중복 신호는 한 거래로 세고, validation/OOS(검증/표본외)는 read-only diagnostic(읽기 전용 진단)으로만 사용해 density bridge(빈도 연결)가 실제 고유 빈도를 만드는지 확인했습니다.

Micro/bridge/metric rows(미세 구간/연결/지표 행): `{final['micro_pocket_rows']}` / `{final['bridge_candidate_rows']}` / `{final['metric_rows']}`

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Best bridge(최상 연결): `{final['best_bridge_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Top Readonly Forward Rows(상위 읽기 전용 전진 행)

| bridge(연결) | type(유형) | pockets(구간 수) | side(방향) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | train overlap | scout | seed |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier24B Gate Audit(전선24B 게이트 감사)

- scope_completion_gate(범위 완료 게이트): density bridge artifacts(빈도 연결 산출물) created(생성) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- OR_union_contract_gate(OR 합집합 계약 게이트): same-side only(같은 방향만), one trade per timestamp(타임스탬프당 한 거래), overlap penalty(중복 페널티) applied(적용)
- kpi_contract_audit(KPI 계약 감사): bridge metrics/summary(연결 지표/요약) created(생성)
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier24 Selection Status(전선24 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest proxy(최근 프록시): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best bridge(최상 연결): `{final['best_bridge_id']}`

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

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
    best = final["best_bridge"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "density_bridge_proxy_scout(빈도 연결 프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"density={final['density_bridge_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};best={final['best_bridge_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={final['best_bridge_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "same_side_or_union_train_only_validation_oos_read_only_no_authority(같은 방향 OR 합집합, 학습 전용, 검증/표본외 읽기 전용, 권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_bridge"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_density_bridge_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_density_bridge_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "density_bridge_proxy_not_runtime(빈도 연결 프록시, 런타임 아님)",
        "scoreboard_lane": "trade_shape_proxy(거래 형태 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"best={final['best_bridge_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
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
        f"- {final['created_at_utc']}: `{RUN_ID}` ran density bridge payoff pockets proxy scout(빈도 연결 보상 구간 프록시 탐색). "
        f"Effect(효과): density/scout/seed/handoff(빈도/탐색/씨앗/인계) counts are {final['density_bridge_rows']}/{final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']} and next run(다음 실행) is `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR24-DENSITY-BRIDGE-PAYOFF-POCKETS-ONNX-SCOUT`: `{RUN_ID}` tested same-side OR-union density bridge(같은 방향 OR 합집합 빈도 연결). "
        f"Effect(효과): best bridge `{final['best_bridge_id']}` remains proxy-only(프록시 전용) with no authority(권위 없음).\n"
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
    best = final["best_bridge"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F24B(전선24B)가 same-side OR-union density bridge proxy(같은 방향 OR 합집합 빈도 연결 프록시)를 실행했습니다.

Effect(효과): 여러 micro-pocket(미세 구간)의 중복 timestamp(타임스탬프)를 한 거래로 처리해, 빈도 증가가 실제 고유 진입인지 확인했습니다.

Best bridge(최상 연결): `{final['best_bridge_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def feature_list(candidate: dict[str, Any]) -> list[str]:
    features = []
    features.extend(str(candidate.get("source_features", "")).split("|"))
    filter_feature = str(candidate.get("filter_feature", ""))
    if filter_feature:
        features.append(filter_feature)
    return sorted({feature for feature in features if feature})


def clean_micro_for_csv(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key != "mask"}


def clean_bridge_for_csv(row: dict[str, Any]) -> dict[str, Any]:
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
