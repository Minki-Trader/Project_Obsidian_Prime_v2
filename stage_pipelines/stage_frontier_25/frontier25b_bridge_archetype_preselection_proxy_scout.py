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
from stage_pipelines.stage_frontier_25 import materialize_frontier25a_stage_open as f25a


STAGE_ID = f25a.STAGE_ID
RUN_ID = "frontier25B_bridge_archetype_preselection_proxy_scout_v1"
RUN_NUMBER = "frontier25B"
PARENT_RUN_ID = f25a.RUN_ID
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier25C_grok_pre_expensive_bridge_archetype_handoff_review_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier25C_bridge_archetype_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_25/frontier25b_bridge_archetype_preselection_proxy_scout.py")

F25A_SUMMARY = STAGE_ROOT / "02_runs" / f25a.RUN_ID / "stage_open_summary.json"
F25A_LOCK = STAGE_ROOT / "02_runs" / f25a.RUN_ID / "bridge_archetype_preselection_lock.json"
F24B_SUMMARY_TABLE = (
    Path("stages/stage_frontier_24__density_bridge_payoff_pockets_onnx_scout/02_runs")
    / f24b.RUN_ID
    / "bridge_candidate_summary.csv"
)

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PER_POCKET_TRAIN_DD_CAP = 16.0
BRIDGE_TRAIN_DD_CAP = 18.0
MIN_TRAIN_PF = 1.06
MIN_DENSITY = 5.0
MAX_DENSITY = 10.0
MAX_OVERLAP_RATIO = 0.45
MIN_UNIQUE_DENSITY_CONTRIB = 0.35
TOP_FORWARD_ROWS = 30

SCOUT_PF = f25a.CRITERIA["scout_clue"]["pf"]
SCOUT_DENSITY_LOW = f25a.CRITERIA["scout_clue"]["density_low"]
SCOUT_DENSITY_HIGH = f25a.CRITERIA["scout_clue"]["density_high"]
SCOUT_DD_CAP = f25a.CRITERIA["scout_clue"]["dd_cap"]
SEED_PF = f25a.CRITERIA["seed_surface"]["pf"]
SEED_DD_CAP = f25a.CRITERIA["seed_surface"]["dd_cap"]
HANDOFF_PF = f25a.CRITERIA["handoff_candidate"]["pf"]
HANDOFF_DD_CAP = f25a.CRITERIA["handoff_candidate"]["dd_cap"]
HANDOFF_R2 = f25a.CRITERIA["handoff_candidate"]["equity_trend_r2"]


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F25A_SUMMARY)
    lock = read_json(F25A_LOCK)
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    context = validate_context(stage_open, lock, feature_order)
    baselines = f23b.build_unconditional_baselines(frame)
    condition_pool = f23b.build_condition_pool(frame, feature_order, baselines)
    f23b_candidates = pd.read_csv(io_path(f24b.F23B_CANDIDATES))
    source_candidates = f23c.rebuild_source_candidates(frame, condition_pool, f23b_candidates)
    f23c_repair_candidates = f23c.build_repair_candidates(frame, condition_pool, source_candidates)
    micro_pockets = f24b.build_micro_pockets(frame, f23c_repair_candidates)
    archetypes = build_archetypes(frame, micro_pockets)
    metrics = evaluate_archetypes(frame, archetypes)
    summary = summarize_archetypes(metrics)
    repeat_audit = build_repeat_audit(archetypes, summary)
    final = build_final(created_at, stage_open, context, micro_pockets, archetypes, metrics, summary, repeat_audit)
    write_outputs(final, micro_pockets, archetypes, metrics, summary, repeat_audit)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "eligible_micro_rows": final["eligible_micro_rows"],
        "archetype_candidate_rows": final["archetype_candidate_rows"],
        "density_bridge_rows": final["density_bridge_rows"],
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "top10_f24b_overlap_count": final["top10_f24b_overlap_count"],
        "best_archetype_id": final["best_archetype_id"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_context(stage_open: dict[str, Any], lock: dict[str, Any], feature_order: list[str]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier25": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier25b": f"next_run_id: {RUN_ID}" in workspace,
        "stage_open_run_matches_parent": stage_open.get("run_id") == PARENT_RUN_ID,
        "lock_changed_variable_dd_headroom": lock.get("locks", {}).get("changed_variable") == "dd_headroom_first_bridge_archetype_preselection",
        "lock_no_repair_frontier25b": "no_repair_in_frontier25b" in lock.get("locks", {}),
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_exists": path_exists(f23b.DATASET_PATH),
        "f24b_reference_table_available": path_exists(F24B_SUMMARY_TABLE),
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier25B context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def build_archetypes(frame: pd.DataFrame, micro_pockets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    eligible = [pocket for pocket in micro_pockets if float(pocket["train_dd_risk"]) <= PER_POCKET_TRAIN_DD_CAP]
    rows: list[dict[str, Any]] = []
    for size in (2, 3):
        for pockets in itertools.combinations(eligible, size):
            maybe = archetype_from_pockets(frame, pockets, train_mask, "pair" if size == 2 else "triple")
            if maybe is not None:
                rows.append(maybe)
    rows.sort(key=lambda row: float(row["train_archetype_score"]), reverse=True)
    for index, row in enumerate(rows, start=1):
        row["archetype_id"] = f"f25b_{index:04d}"
    return rows


def archetype_from_pockets(
    frame: pd.DataFrame,
    pockets: tuple[dict[str, Any], ...],
    train_mask: np.ndarray,
    archetype_type: str,
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
    if train["net_profit"] <= 0 or train["profit_factor"] < MIN_TRAIN_PF:
        return None
    if not (MIN_DENSITY <= train["trades_per_day"] <= MAX_DENSITY):
        return None
    if float(train["dd_risk"]) > BRIDGE_TRAIN_DD_CAP:
        return None
    score = archetype_score(train, stats, len(family_set))
    return {
        "archetype_id": "pending",
        "archetype_type": archetype_type,
        "pocket_count": len(pockets),
        "micro_ids": "|".join(str(pocket["micro_id"]) for pocket in pockets),
        "micro_key": micro_key(pocket["micro_id"] for pocket in pockets),
        "source_repair_ids": "|".join(str(pocket["source_repair_id"]) for pocket in pockets),
        "side_value": side_value,
        "side": pockets[0]["side"],
        "features": " || ".join(str(pocket["features"]) for pocket in pockets),
        "feature_families": "|".join(family_set),
        "rule_definition": " OR ".join(f"({pocket['rule_definition']})" for pocket in pockets),
        "per_pocket_train_dd_max": max(float(pocket["train_dd_risk"]) for pocket in pockets),
        "per_pocket_train_dd_min": min(float(pocket["train_dd_risk"]) for pocket in pockets),
        "train_dd_headroom_to_seed_cap": float(BRIDGE_TRAIN_DD_CAP - float(train["dd_risk"])),
        "train_archetype_score": score,
        **stats,
        **{f"train_{key}": value for key, value in train.items()},
        "mask": union_mask,
    }


def archetype_score(metrics: dict[str, Any], stats: dict[str, Any], family_count: int) -> float:
    dd_headroom = max(0.0, BRIDGE_TRAIN_DD_CAP - float(metrics["dd_risk"]))
    density_penalty = abs(float(metrics["trades_per_day"]) - 7.5) / 7.5
    overlap_penalty = float(stats["overlap_ratio"]) * 1.5
    diversity_bonus = 1.0 + min(family_count, 6) * 0.08
    r2_bonus = 1.0 + max(float(metrics["equity_trend_r2"]), 0.0)
    return float(
        (1.0 + dd_headroom)
        * min(float(metrics["profit_factor"]), 3.0)
        * min(float(metrics["payoff_ratio"]), 3.0)
        * max(float(stats["min_unique_density_contribution"]), 0.0)
        * diversity_bonus
        * r2_bonus
        / (1.0 + density_penalty + overlap_penalty)
    )


def evaluate_archetypes(frame: pd.DataFrame, archetypes: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for rank, candidate in enumerate(archetypes, start=1):
        for split in ("train", "validation", "oos"):
            metrics = f23b.evaluate_mask(frame, candidate["mask"], int(candidate["side_value"]), split)
            rows.append({
                "archetype_id": candidate["archetype_id"],
                "train_rank": rank,
                "archetype_type": candidate["archetype_type"],
                "pocket_count": candidate["pocket_count"],
                "micro_ids": candidate["micro_ids"],
                "micro_key": candidate["micro_key"],
                "source_repair_ids": candidate["source_repair_ids"],
                "side": candidate["side"],
                "side_value": candidate["side_value"],
                "features": candidate["features"],
                "feature_families": candidate["feature_families"],
                "rule_definition": candidate["rule_definition"],
                "per_pocket_train_dd_max": candidate["per_pocket_train_dd_max"],
                "train_dd_headroom_to_seed_cap": candidate["train_dd_headroom_to_seed_cap"],
                "train_overlap_ratio": candidate["overlap_ratio"],
                "train_union_hits": candidate["train_union_hits"],
                "train_overlap_hits": candidate["train_overlap_hits"],
                "min_unique_density_contribution": candidate["min_unique_density_contribution"],
                "train_archetype_score": candidate["train_archetype_score"],
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
                "selection_boundary": "train_only_archetype_rank(학습 전용 원형 순위)" if split == "train" else "read_only_forward_diagnostic(읽기 전용 전진 진단)",
            })
    return pd.DataFrame(rows)


def summarize_archetypes(metrics: pd.DataFrame) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    for archetype_id, group in metrics.groupby("archetype_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        base = {
            "archetype_id": archetype_id,
            "train_rank": int(train["train_rank"]),
            "archetype_type": train["archetype_type"],
            "pocket_count": train["pocket_count"],
            "micro_ids": train["micro_ids"],
            "micro_key": train["micro_key"],
            "source_repair_ids": train["source_repair_ids"],
            "side": train["side"],
            "features": train["features"],
            "feature_families": train["feature_families"],
            "rule_definition": train["rule_definition"],
            "per_pocket_train_dd_max": train["per_pocket_train_dd_max"],
            "train_dd_headroom_to_seed_cap": train["train_dd_headroom_to_seed_cap"],
            "train_overlap_ratio": train["train_overlap_ratio"],
            "min_unique_density_contribution": train["min_unique_density_contribution"],
            "train_archetype_score": train["train_archetype_score"],
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


def build_repeat_audit(archetypes: list[dict[str, Any]], summary: pd.DataFrame) -> pd.DataFrame:
    f24 = pd.read_csv(io_path(F24B_SUMMARY_TABLE)).copy()
    f24["_key"] = f24["micro_ids"].map(lambda value: micro_key(str(value).split("|")))
    f24_top = f24.head(10).copy()
    f24_keys = set(f24_top["_key"])
    rows: list[dict[str, Any]] = []
    top = summary.sort_values("train_archetype_score", ascending=False).head(10) if not summary.empty else pd.DataFrame()
    for _, row in top.iterrows():
        key = row["micro_key"]
        match = f24_top.loc[f24_top["_key"].eq(key)]
        matched = not match.empty
        f24_train_dd = float(match.iloc[0]["train_dd_risk"]) if matched else math.nan
        f25_train_dd = float(row["train_dd_risk"])
        rows.append({
            "f25_archetype_id": row["archetype_id"],
            "micro_key": key,
            "in_f24b_top10": bool(key in f24_keys),
            "f25_train_dd": f25_train_dd,
            "f24_train_dd_if_matched": f24_train_dd if matched else "",
            "train_dd_lift_vs_f24": (f24_train_dd - f25_train_dd) if matched else "",
            "f25_validation_profit_factor": row["validation_profit_factor"],
            "f25_oos_profit_factor": row["oos_profit_factor"],
            "f25_forward_max_dd": max(float(row["validation_dd_risk"]), float(row["oos_dd_risk"])),
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
    archetypes: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
    repeat_audit: pd.DataFrame,
) -> dict[str, Any]:
    density_count = int(summary["density_bridge_flag"].sum()) if not summary.empty else 0
    scout_count = int(summary["scout_clue_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if not summary.empty else 0
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if not summary.empty else 0
    eligible_count = int(sum(float(pocket["train_dd_risk"]) <= PER_POCKET_TRAIN_DD_CAP for pocket in micro_pockets))
    top10_overlap = int(repeat_audit["in_f24b_top10"].sum()) if not repeat_audit.empty else 0
    if handoff_count:
        status = "bridge_archetype_handoff_candidate_proxy_no_authority"
        judgment = "handoff_candidate_requires_grok_pre_expensive_review_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
    elif seed_count:
        status = "bridge_archetype_seed_surface_proxy_no_authority"
        judgment = "seed_surface_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif scout_count:
        status = "bridge_archetype_scout_clue_proxy_no_authority"
        judgment = "scout_clue_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif density_count:
        status = "bridge_archetype_density_only_proxy_no_authority"
        judgment = "density_or_headroom_clue_pf_or_dd_shortfall_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif archetypes:
        status = "bridge_archetype_no_forward_clue_proxy_no_authority"
        judgment = "train_headroom_archetypes_failed_forward_clue_requires_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    else:
        status = "bridge_archetype_no_valid_archetypes_proxy_no_authority"
        judgment = "invalid_or_negative_setup_requires_closeout_no_authority"
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
        "micro_pocket_rows": int(len(micro_pockets)),
        "eligible_micro_rows": eligible_count,
        "archetype_candidate_rows": int(len(archetypes)),
        "metric_rows": int(len(metrics)) if not metrics.empty else 0,
        "density_bridge_rows": density_count,
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "top10_f24b_overlap_count": top10_overlap,
        "best_archetype_id": best.get("archetype_id", ""),
        "best_archetype": json_ready(best),
        "result_boundary": "dd_headroom_first_archetype_proxy_no_repair_no_wfo_no_mt5_no_runtime_authority(손실폭 여유 우선 원형 프록시, 수리/WFO/MT5/런타임 권위 없음)",
        "runtime_probe_status": "pre_expensive_grok_required_before_mt5(비싼 MT5 전 Grok 검토 필요)" if handoff_count else "out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(
    final: dict[str, Any],
    micro_pockets: list[dict[str, Any]],
    archetypes: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
    repeat_audit: pd.DataFrame,
) -> None:
    pd.DataFrame([clean_micro_for_csv(row) for row in micro_pockets]).assign(
        f25b_eligible=lambda df: pd.to_numeric(df["train_dd_risk"], errors="coerce") <= PER_POCKET_TRAIN_DD_CAP
    ).to_csv(io_path(RUN_ROOT / "micro_pocket_eligibility_audit.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame([clean_archetype_for_csv(row) for row in archetypes]).to_csv(
        io_path(RUN_ROOT / "train_ranked_archetype_candidates.csv"), index=False, encoding="utf-8-sig"
    )
    metrics.to_csv(io_path(RUN_ROOT / "archetype_metrics_by_split.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "archetype_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    if not summary.empty:
        summary.sort_values("forward_read_score", ascending=False).head(TOP_FORWARD_ROWS).to_csv(
            io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig"
        )
    else:
        pd.DataFrame().to_csv(io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig")
    repeat_audit.to_csv(io_path(RUN_ROOT / "f24b_top10_nonrepeat_audit.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, summary))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F25A_SUMMARY,
        F25A_LOCK,
        F24B_SUMMARY_TABLE,
        RUN_ROOT / "micro_pocket_eligibility_audit.csv",
        RUN_ROOT / "train_ranked_archetype_candidates.csv",
        RUN_ROOT / "archetype_metrics_by_split.csv",
        RUN_ROOT / "archetype_candidate_summary.csv",
        RUN_ROOT / "f24b_top10_nonrepeat_audit.csv",
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
            "selection": "train-only DD-headroom-first archetype score(학습 전용 손실폭 여유 우선 원형 점수)",
            "forbidden": "no validation selection, no capped repair in F25B, no ONNX, no MT5 before handoff(검증 선택 없음, F25B 상한 수리 없음, 인계 전 ONNX/MT5 없음)",
        },
        "results": {
            "cross_split": {
                "density_bridge_rows": final["density_bridge_rows"],
                "scout_clue_rows": final["scout_clue_rows"],
                "seed_surface_rows": final["seed_surface_rows"],
                "handoff_candidate_rows": final["handoff_candidate_rows"],
                "best_archetype_id": final["best_archetype_id"],
                "top10_f24b_overlap_count": final["top10_f24b_overlap_count"],
            },
            "report_refs": [{"role": "bridge_archetype_preselection_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {"schema_version": "frontier25b_bridge_archetype_preselection_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["best_archetype"]
    top_rows: list[str] = []
    if not summary.empty:
        for _, row in summary.head(12).iterrows():
            top_rows.append(
                f"| `{row['archetype_id']}` | `{row['micro_ids']}` | {fmt(row['train_dd_risk'])} | {fmt(row['train_dd_headroom_to_seed_cap'])} | "
                f"{fmt(row['validation_profit_factor'])} | {fmt(row['validation_trades_per_day'])} | {fmt(row['validation_dd_risk'])} | "
                f"{fmt(row['oos_profit_factor'])} | {fmt(row['oos_trades_per_day'])} | {fmt(row['oos_dd_risk'])} | {row['scout_clue_flag']} | {row['seed_surface_flag']} |"
            )
    table = "\n".join(top_rows) if top_rows else "| none(없음) | | | | | | | | | | | | |"
    return f"""# Frontier25B Bridge Archetype Preselection Proxy Report(전선25B 연결 원형 사전 선택 프록시 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F24 micro pockets(F24 미세 구간)를 재구성하고 train-only DD-headroom-first archetype score(학습 전용 손실폭 여유 우선 원형 점수)로 pair/triple OR-union(쌍/삼중 OR 합집합)을 선택했습니다.

Effect(효과): post-hoc repair(사후 수리) 없이 구조 선택만으로 PF/density/DD/smoothness(수익 팩터/빈도/손실폭/매끄러움)가 forward(전진)에서 좋아지는지 확인했습니다.

Micro/eligible/archetype/metric rows(미세/적격/원형/지표 행): `{final['micro_pocket_rows']}` / `{final['eligible_micro_rows']}` / `{final['archetype_candidate_rows']}` / `{final['metric_rows']}`

Density/scout/seed/handoff rows(빈도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

F24B top10 overlap(F24B 상위10 중복): `{final['top10_f24b_overlap_count']}`

Best archetype(최상 원형): `{final['best_archetype_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Top Archetype Rows(상위 원형 행)

| archetype(원형) | micro ids(미세 ID) | train DD | train DD headroom | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier25B Gate Audit(전선25B 게이트 감사)

- scope_completion_gate(범위 완료 게이트): archetype artifacts(원형 산출물) created(생성) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- kpi_contract_audit(KPI 계약 감사): archetype metrics/summary/repeat audit(원형 지표/요약/반복 감사) created(생성)
- no_repair_primary_path_gate(기본 경로 수리 금지 게이트): pass(통과), F25B applies no capped repair(F25B는 상한 수리 미적용)
- non_repeat_gate(반복 방지 게이트): F24B top10 overlap(F24B 상위10 중복) `{final['top10_f24b_overlap_count']}`
- tier_pair_record_gate(티어 쌍 기록 게이트): Tier A/Tier B/Tier A+B rows(티어 A/B/A+B 행) written(기록)
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier25 Selection Status(전선25 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest proxy(최근 프록시): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best archetype(최상 원형): `{final['best_archetype_id']}`

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
    best = final["best_archetype"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "bridge_archetype_proxy_scout(연결 원형 프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"density={final['density_bridge_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};best={final['best_archetype_id']};f24top10_overlap={final['top10_f24b_overlap_count']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={final['best_archetype_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "dd_headroom_first_no_repair_no_wfo_no_mt5_no_authority(손실폭 여유 우선, 수리/WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_archetype"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_archetype_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_archetype_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "bridge_archetype_preselection_proxy_not_runtime(연결 원형 사전 선택 프록시, 런타임 아님)",
        "scoreboard_lane": "trade_shape_proxy(거래 형태 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"best={final['best_archetype_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "proxy_only_no_repair_no_wfo_no_mt5_no_authority(프록시 전용, 수리/WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"density={final['density_bridge_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};f24top10_overlap={final['top10_f24b_overlap_count']}",
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
        f"- {final['created_at_utc']}: `{RUN_ID}` ran DD-headroom-first bridge archetype proxy scout(손실폭 여유 우선 연결 원형 프록시 탐색). "
        f"Effect(효과): density/scout/seed/handoff(빈도/탐색/씨앗/인계) counts are {final['density_bridge_rows']}/{final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']} and next run(다음 실행) is `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR25-BRIDGE-ARCHETYPE-PRESELECTION-ONNX-SCOUT`: `{RUN_ID}` tested DD-headroom-first bridge archetype preselection(손실폭 여유 우선 연결 원형 사전 선택). "
        f"Effect(효과): best archetype `{final['best_archetype_id']}` remains proxy-only(프록시 전용) with no authority(권위 없음).\n"
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
    best = final["best_archetype"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F25B(전선25B)가 train-only DD-headroom-first bridge archetype preselection(학습 전용 손실폭 여유 우선 연결 원형 사전 선택)을 실행했습니다.

Effect(효과): F24B(전선24B)의 density-first(빈도 우선)와 F24C(전선24C)의 post-hoc repair(사후 수리) 없이 원형 선택 자체의 forward read(전진 판독)를 확인했습니다.

Best archetype(최상 원형): `{final['best_archetype_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

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


def clean_archetype_for_csv(row: dict[str, Any]) -> dict[str, Any]:
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
