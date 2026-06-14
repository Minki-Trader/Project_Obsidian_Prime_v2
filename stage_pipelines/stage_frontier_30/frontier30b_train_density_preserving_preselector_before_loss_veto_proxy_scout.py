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
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_29 import frontier29b_train_only_loss_concentration_veto_proxy_scout as f29b
from stage_pipelines.stage_frontier_30 import materialize_frontier30a_stage_open as f30a


STAGE_ID = f30a.STAGE_ID
RUN_ID = "frontier30B_train_density_preserving_preselector_before_loss_veto_proxy_scout_v1"
RUN_NUMBER = "frontier30B"
PARENT_RUN_ID = f30a.RUN_ID
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier30C_grok_pre_expensive_density_preselector_handoff_review_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier30C_density_preserving_preselector_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_30/frontier30b_train_density_preserving_preselector_before_loss_veto_proxy_scout.py")

F30A_SUMMARY = STAGE_ROOT / "02_runs" / f30a.RUN_ID / "stage_open_summary.json"
F30A_LOCK = STAGE_ROOT / "02_runs" / f30a.RUN_ID / "density_preserving_preselector_lock.json"
F28B_CANDIDATE_SUMMARY = (
    Path("stages/stage_frontier_28__train_only_stability_gap_penalty_for_pf_dd_balance_onnx_scout/02_runs")
    / "frontier28B_train_only_stability_gap_penalty_proxy_scout_v1"
    / "stability_gap_candidate_summary.csv"
)
F29B_CANDIDATE_SUMMARY = (
    Path("stages/stage_frontier_29__train_only_loss_concentration_veto_for_pf_dd_balance_onnx_scout/02_runs")
    / f29b.RUN_ID
    / "loss_veto_candidate_summary.csv"
)

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
    stage_open = read_json(F30A_SUMMARY)
    lock = read_json(F30A_LOCK)
    source = pd.read_csv(io_path(F28B_CANDIDATE_SUMMARY))
    veto = pd.read_csv(io_path(F29B_CANDIDATE_SUMMARY))
    context = validate_context(stage_open, lock, source, veto)
    preselector = build_preselector_ledger(source, veto, lock)
    selected_sources = preselector[preselector["preselector_selected_flag"]].copy()
    candidates = build_candidate_summary(source, veto, selected_sources, lock)
    final = build_final(created_at, stage_open, context, preselector, candidates)
    write_outputs(final, preselector, candidates)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "source_rows": final["source_rows"],
        "preselected_source_rows": final["preselected_source_rows"],
        "candidate_rows": final["candidate_rows"],
        "source_branch_scout_rows": final["source_branch_scout_rows"],
        "veto_branch_scout_rows": final["veto_branch_scout_rows"],
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
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
    source: pd.DataFrame,
    veto: pd.DataFrame,
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    locks = lock.get("locks", {})
    pre = locks.get("preselector_contract", {})
    checks = {
        "workspace_current_stage_frontier30": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier30b": f"next_run_id: {RUN_ID}" in workspace or f"current_run_id: {RUN_ID}" in workspace,
        "stage_open_parent_matches": stage_open.get("run_id") == PARENT_RUN_ID,
        "stage_open_grok_accepted": stage_open.get("grok", {}).get("classification", "").startswith("accepted"),
        "lock_changed_variable_density_preselector": locks.get("active_changed_variable") == "train_density_preserving_preselector_before_loss_veto",
        "lock_exit_shape_reference_only": locks.get("exit_shape_pivot_role") == "reference_fallback_only_not_active_changed_variable",
        "lock_source_keep_cap_160": int(pre.get("source_keep_cap", -1)) == 160,
        "lock_no_forward_rank_inputs": bool(pre.get("no_validation_oos_rank_inputs")),
        "lock_blocks_forward_selection": "select_by_validation_or_oos_pf_dd_density" in locks.get("forbidden_primary_path", []),
        "lock_blocks_f29_threshold_rescue": "retune_f29_loss_veto_thresholds_to_rescue_near_scout_rows" in locks.get("forbidden_primary_path", []),
        "lock_blocks_exit_shape_activation": "activate_exit_shape_pivot_in_f30b_proxy" in locks.get("forbidden_primary_path", []),
        "source_summary_234": len(source) == 234,
        "source_scout_19_reference_only": int(source["scout_clue_flag"].astype(bool).sum()) == 19,
        "source_seed_handoff_zero": int(source["seed_surface_flag"].astype(bool).sum()) == 0
        and int(source["handoff_candidate_flag"].astype(bool).sum()) == 0,
        "veto_summary_1438": len(veto) == 1438,
        "veto_scout_seed_handoff_zero": int(veto["scout_clue_flag"].astype(bool).sum()) == 0
        and int(veto["seed_surface_flag"].astype(bool).sum()) == 0
        and int(veto["handoff_candidate_flag"].astype(bool).sum()) == 0,
        "source_ids_join_veto_ids": source["stability_union_id"].astype(str).isin(veto["source_stability_union_id"].astype(str)).all(),
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier30B context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def build_preselector_ledger(source: pd.DataFrame, veto: pd.DataFrame, lock: dict[str, Any]) -> pd.DataFrame:
    pre = lock["locks"]["preselector_contract"]
    center = float(pre["density_target_center"])
    keep_cap = int(pre["source_keep_cap"])
    max_removed = float(pre["max_removed_train_trade_fraction_after_veto"])
    density_floor = float(pre["density_preservation_floor"])

    source_rows = source.copy()
    source_rows["source_stability_union_id"] = source_rows["stability_union_id"].astype(str)
    source_rows["train_density_margin"] = (1.0 - (source_rows["train_trades_per_day"].astype(float) - center).abs() / center).clip(-1.0, 1.0)
    source_rows["train_pf_balance"] = np.log1p(source_rows["train_profit_factor"].astype(float).clip(0.0, 5.0)) / math.log(6.0)
    source_rows["train_dd_containment"] = (1.0 - (source_rows["train_dd_risk"].astype(float) / 25.0).clip(0.0, 2.0)).clip(-1.0, 1.0)
    source_rows["train_smoothness"] = source_rows["train_equity_trend_r2"].astype(float).clip(0.0, 1.0)

    density_preserving_veto = veto[
        (veto["removed_train_trade_fraction"].astype(float) <= max_removed)
        & (veto["train_trades_per_day"].astype(float) >= density_floor)
    ].copy()
    density_preserving_veto["source_stability_union_id"] = density_preserving_veto["source_stability_union_id"].astype(str)
    density_preserving_veto["loss_capture_per_removed_trade"] = (
        density_preserving_veto["loss_capture_ratio"].astype(float)
        / density_preserving_veto["removed_train_trade_fraction"].replace(0, np.nan).astype(float)
    ).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    density_preserving_veto["density_thinning_penalty"] = (
        density_preserving_veto["source_stability_union_id"].map(
            source_rows.set_index("source_stability_union_id")["train_trades_per_day"].astype(float)
        )
        - density_preserving_veto["train_trades_per_day"].astype(float)
    ).clip(lower=0.0) / center
    density_preserving_veto["density_preserving_veto_score"] = (
        density_preserving_veto["train_veto_score"].astype(float)
        + 0.15 * density_preserving_veto["loss_capture_per_removed_trade"].clip(upper=6.0)
        - 0.35 * density_preserving_veto["density_thinning_penalty"].astype(float)
        - 0.20 * (density_preserving_veto["removed_train_trade_fraction"].astype(float) - 0.22).clip(lower=0.0)
    )

    aggregate = density_preserving_veto.groupby("source_stability_union_id").agg(
        density_preserving_veto_rows=("veto_candidate_id", "count"),
        best_density_preserving_veto_score=("density_preserving_veto_score", "max"),
        max_loss_capture_per_removed_trade=("loss_capture_per_removed_trade", "max"),
        best_veto_train_score=("train_veto_score", "max"),
        max_kept_train_density_after_veto=("train_trades_per_day", "max"),
        min_removed_train_trade_fraction=("removed_train_trade_fraction", "min"),
    ).reset_index()
    source_rows = source_rows.merge(aggregate, on="source_stability_union_id", how="left")
    fill_values = {
        "density_preserving_veto_rows": 0,
        "best_density_preserving_veto_score": 0.0,
        "max_loss_capture_per_removed_trade": 0.0,
        "best_veto_train_score": 0.0,
        "max_kept_train_density_after_veto": 0.0,
        "min_removed_train_trade_fraction": 1.0,
    }
    source_rows = source_rows.fillna(fill_values)
    source_rows["train_density_thinning_risk"] = (
        source_rows["train_trades_per_day"].astype(float) - source_rows["max_kept_train_density_after_veto"].astype(float)
    ).clip(lower=0.0) / center
    source_rows["train_only_preselector_score"] = (
        1.40 * source_rows["train_density_margin"].astype(float)
        + 0.80 * source_rows["train_pf_balance"].astype(float)
        + 0.70 * source_rows["train_dd_containment"].astype(float)
        + 0.20 * source_rows["train_smoothness"].astype(float)
        + 0.15 * source_rows["max_loss_capture_per_removed_trade"].astype(float).clip(upper=6.0)
        + 0.20 * source_rows["best_veto_train_score"].astype(float)
        - 0.25 * source_rows["train_density_thinning_risk"].astype(float)
    )
    source_rows = source_rows.sort_values("train_only_preselector_score", ascending=False).reset_index(drop=True)
    source_rows["preselector_rank"] = np.arange(1, len(source_rows) + 1)
    source_rows["preselector_selected_flag"] = source_rows["preselector_rank"] <= keep_cap
    source_rows["selection_boundary"] = "train_only_source_preselector_score_validation_oos_read_only"
    keep_columns = [
        "source_stability_union_id",
        "preselector_rank",
        "preselector_selected_flag",
        "train_only_preselector_score",
        "train_density_margin",
        "train_pf_balance",
        "train_dd_containment",
        "train_smoothness",
        "density_preserving_veto_rows",
        "best_density_preserving_veto_score",
        "max_loss_capture_per_removed_trade",
        "best_veto_train_score",
        "max_kept_train_density_after_veto",
        "min_removed_train_trade_fraction",
        "train_density_thinning_risk",
        "train_trades_per_day",
        "train_profit_factor",
        "train_dd_risk",
        "validation_profit_factor",
        "validation_trades_per_day",
        "validation_dd_risk",
        "oos_profit_factor",
        "oos_trades_per_day",
        "oos_dd_risk",
        "density_bridge_flag",
        "scout_clue_flag",
        "seed_surface_flag",
        "handoff_candidate_flag",
        "selection_boundary",
    ]
    return source_rows[keep_columns]


def build_candidate_summary(
    source: pd.DataFrame,
    veto: pd.DataFrame,
    selected_sources: pd.DataFrame,
    lock: dict[str, Any],
) -> pd.DataFrame:
    selected_ids = selected_sources["source_stability_union_id"].astype(str).tolist()
    selected_map = selected_sources.set_index("source_stability_union_id").to_dict("index")
    source_selected = source[source["stability_union_id"].astype(str).isin(selected_ids)].copy()
    source_rows = [source_branch_row(row, selected_map[str(row["stability_union_id"])], index) for index, (_, row) in enumerate(source_selected.iterrows(), start=1)]

    pre = lock["locks"]["preselector_contract"]
    density_floor = float(pre["density_preservation_floor"])
    max_removed = float(pre["max_removed_train_trade_fraction_after_veto"])
    veto_selected = veto[
        veto["source_stability_union_id"].astype(str).isin(selected_ids)
        & (veto["removed_train_trade_fraction"].astype(float) <= max_removed)
        & (veto["train_trades_per_day"].astype(float) >= density_floor)
    ].copy()
    if not veto_selected.empty:
        veto_selected["source_stability_union_id"] = veto_selected["source_stability_union_id"].astype(str)
        veto_selected["loss_capture_per_removed_trade"] = (
            veto_selected["loss_capture_ratio"].astype(float)
            / veto_selected["removed_train_trade_fraction"].replace(0, np.nan).astype(float)
        ).replace([np.inf, -np.inf], np.nan).fillna(0.0)
        veto_selected["branch_train_score"] = (
            veto_selected["train_veto_score"].astype(float)
            + 0.15 * veto_selected["loss_capture_per_removed_trade"].astype(float).clip(upper=6.0)
            - 0.20 * (veto_selected["removed_train_trade_fraction"].astype(float) - 0.22).clip(lower=0.0)
        )
        best_veto = (
            veto_selected.sort_values(["source_stability_union_id", "branch_train_score"], ascending=[True, False])
            .groupby("source_stability_union_id")
            .head(1)
            .copy()
        )
    else:
        best_veto = veto_selected
    veto_rows = [veto_branch_row(row, selected_map[str(row["source_stability_union_id"])], index) for index, (_, row) in enumerate(best_veto.iterrows(), start=1)]
    candidates = pd.DataFrame(source_rows + veto_rows)
    if candidates.empty:
        return candidates
    candidates = candidates.sort_values(["preselector_rank", "branch_sort"]).reset_index(drop=True)
    candidates["candidate_rank"] = np.arange(1, len(candidates) + 1)
    candidates["candidate_id"] = [f"f30b_{index:04d}" for index in candidates["candidate_rank"]]
    candidates["forward_min_pf"] = candidates[["validation_profit_factor", "oos_profit_factor"]].min(axis=1)
    candidates["forward_max_dd"] = candidates[["validation_dd_risk", "oos_dd_risk"]].max(axis=1)
    candidates["forward_min_density"] = candidates[["validation_trades_per_day", "oos_trades_per_day"]].min(axis=1)
    candidates["forward_max_density"] = candidates[["validation_trades_per_day", "oos_trades_per_day"]].max(axis=1)
    candidates["density_bridge_flag"] = (
        (candidates["forward_min_density"] >= SCOUT_DENSITY_LOW)
        & (candidates["forward_max_density"] <= SCOUT_DENSITY_HIGH)
    )
    candidates["scout_clue_flag"] = (
        candidates["density_bridge_flag"]
        & (candidates["validation_net_profit"] > 0)
        & (candidates["oos_net_profit"] > 0)
        & (candidates["forward_min_pf"] >= SCOUT_PF)
        & (candidates["forward_max_dd"] <= SCOUT_DD_CAP)
    )
    candidates["seed_surface_flag"] = (
        candidates["scout_clue_flag"]
        & (candidates["forward_min_pf"] >= SEED_PF)
        & (candidates["forward_max_dd"] <= SEED_DD_CAP)
    )
    candidates["smoothness_proxy_pass"] = (
        (candidates["validation_equity_trend_r2"] >= HANDOFF_R2)
        & (candidates["oos_equity_trend_r2"] >= HANDOFF_R2)
        & (candidates["validation_max_loss_streak"] <= 20)
        & (candidates["oos_max_loss_streak"] <= 20)
    )
    candidates["handoff_candidate_flag"] = (
        candidates["seed_surface_flag"]
        & (candidates["forward_min_pf"] >= HANDOFF_PF)
        & (candidates["forward_max_dd"] <= HANDOFF_DD_CAP)
        & candidates["smoothness_proxy_pass"]
    )
    candidates["forward_read_score"] = (
        candidates["forward_min_pf"].clip(0.0, 4.0)
        * candidates["forward_min_density"].clip(0.0, 10.0)
        * (1.0 + candidates[["validation_equity_trend_r2", "oos_equity_trend_r2"]].min(axis=1).clip(0.0, 1.0))
        / (1.0 + candidates["forward_max_dd"] / 10.0 + candidates["removed_train_trade_fraction"].fillna(0.0))
    )
    return candidates


def source_branch_row(row: pd.Series, selected: dict[str, Any], index: int) -> dict[str, Any]:
    base = common_split_fields(row)
    base.update({
        "candidate_id": f"pending_source_{index:04d}",
        "source_stability_union_id": str(row["stability_union_id"]),
        "source_soft_union_id": str(row["source_soft_union_id"]),
        "source_stability_rank": int(row["stability_rank"]),
        "preselector_rank": int(selected["preselector_rank"]),
        "train_only_preselector_score": float(selected["train_only_preselector_score"]),
        "branch": "source_no_veto_density_preservation_branch",
        "branch_sort": 0,
        "source_candidate_id": str(row["stability_union_id"]),
        "veto_candidate_id": "",
        "rule_family": "source_no_veto",
        "rule_definition": "density_preserving_preselector_kept_source_union_without_loss_veto",
        "removed_train_trade_fraction": 0.0,
        "loss_capture_ratio": 0.0,
        "loss_quality_ratio": 0.0,
        "train_veto_score": 0.0,
        "selection_boundary": "train_only_preselector_rank_validation_oos_read_only",
    })
    return base


def veto_branch_row(row: pd.Series, selected: dict[str, Any], index: int) -> dict[str, Any]:
    base = common_split_fields(row)
    base.update({
        "candidate_id": f"pending_veto_{index:04d}",
        "source_stability_union_id": str(row["source_stability_union_id"]),
        "source_soft_union_id": str(row["source_soft_union_id"]),
        "source_stability_rank": int(row["source_stability_rank"]),
        "preselector_rank": int(selected["preselector_rank"]),
        "train_only_preselector_score": float(selected["train_only_preselector_score"]),
        "branch": "top_density_preserving_loss_veto_variant_per_source",
        "branch_sort": 1,
        "source_candidate_id": str(row["source_stability_union_id"]),
        "veto_candidate_id": str(row["veto_candidate_id"]),
        "rule_family": str(row["rule_family"]),
        "rule_definition": str(row["rule_definition"]),
        "removed_train_trade_fraction": float(row["removed_train_trade_fraction"]),
        "loss_capture_ratio": float(row["loss_capture_ratio"]),
        "loss_quality_ratio": float(row.get("loss_quality_ratio", 0.0)),
        "train_veto_score": float(row["train_veto_score"]),
        "selection_boundary": "train_only_preselector_then_train_only_density_preserving_veto_validation_oos_read_only",
    })
    return base


def common_split_fields(row: pd.Series) -> dict[str, Any]:
    base: dict[str, Any] = {}
    for prefix in ("train", "validation", "oos"):
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
            base[f"{prefix}_{field}"] = row[f"{prefix}_{field}"]
    base["micro_ids"] = str(row.get("micro_ids", ""))
    base["side"] = str(row.get("side", ""))
    base["side_value"] = int(row.get("side_value", 0)) if "side_value" in row else 0
    return base


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    context: dict[str, Any],
    preselector: pd.DataFrame,
    candidates: pd.DataFrame,
) -> dict[str, Any]:
    density_count = int(candidates["density_bridge_flag"].astype(bool).sum()) if not candidates.empty else 0
    scout_count = int(candidates["scout_clue_flag"].astype(bool).sum()) if not candidates.empty else 0
    seed_count = int(candidates["seed_surface_flag"].astype(bool).sum()) if not candidates.empty else 0
    handoff_count = int(candidates["handoff_candidate_flag"].astype(bool).sum()) if not candidates.empty else 0
    source_scout = int(((candidates["branch"] == "source_no_veto_density_preservation_branch") & candidates["scout_clue_flag"].astype(bool)).sum()) if not candidates.empty else 0
    veto_scout = int(((candidates["branch"] == "top_density_preserving_loss_veto_variant_per_source") & candidates["scout_clue_flag"].astype(bool)).sum()) if not candidates.empty else 0
    if handoff_count:
        status = "density_preserving_preselector_handoff_candidate_proxy_no_authority"
        judgment = "handoff_candidate_requires_grok_pre_expensive_review_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
        runtime_probe_status = "runtime_probe_pending_handoff_candidate_pre_expensive_grok_required"
    elif seed_count:
        status = "density_preserving_preselector_seed_surface_proxy_no_authority"
        judgment = "seed_surface_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_out_of_scope_by_claim_seed_only_no_handoff"
    elif scout_count:
        status = "density_preserving_preselector_scout_clue_proxy_no_authority"
        judgment = "scout_clue_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_out_of_scope_by_claim_scout_only_no_handoff"
    else:
        status = "density_preserving_preselector_no_scout_no_seed_no_handoff_proxy_no_authority"
        judgment = "negative_memory_candidate_requires_closeout_or_capped_repair_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
        runtime_probe_status = "runtime_probe_ineligible_no_handoff_candidate_after_f30b_proxy"
    best_train = dict(candidates.sort_values("train_only_preselector_score", ascending=False).iloc[0]) if not candidates.empty else {}
    best_forward = dict(candidates.sort_values("forward_read_score", ascending=False).iloc[0]) if not candidates.empty else {}
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "source_rows": int(len(preselector)),
        "preselected_source_rows": int(preselector["preselector_selected_flag"].astype(bool).sum()),
        "candidate_rows": int(len(candidates)),
        "source_branch_rows": int((candidates["branch"] == "source_no_veto_density_preservation_branch").sum()) if not candidates.empty else 0,
        "veto_branch_rows": int((candidates["branch"] == "top_density_preserving_loss_veto_variant_per_source").sum()) if not candidates.empty else 0,
        "density_bridge_rows": density_count,
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "source_branch_scout_rows": source_scout,
        "veto_branch_scout_rows": veto_scout,
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
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
        "result_boundary": "proxy_scout_only_no_wfo_no_mt5_no_onnx_no_authority",
    }


def write_outputs(final: dict[str, Any], preselector: pd.DataFrame, candidates: pd.DataFrame) -> None:
    preselector.to_csv(io_path(RUN_ROOT / "train_density_preselector_source_ledger.csv"), index=False, encoding="utf-8-sig")
    candidates.to_csv(io_path(RUN_ROOT / "density_preselector_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    if not candidates.empty:
        candidates.sort_values("forward_read_score", ascending=False).head(TOP_FORWARD_ROWS).to_csv(
            io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig"
        )
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, candidates))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F30A_SUMMARY,
        F30A_LOCK,
        F28B_CANDIDATE_SUMMARY,
        F29B_CANDIDATE_SUMMARY,
        RUN_ROOT / "train_density_preselector_source_ledger.csv",
        RUN_ROOT / "density_preselector_candidate_summary.csv",
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
        "selection_boundary": "train_only_preselector_score_validation_oos_read_only",
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f30a.upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
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
        "notes": f"source={final['source_rows']};preselected={final['preselected_source_rows']};candidate={final['candidate_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};next={final['next_run_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"candidate={final['candidate_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']}",
        "guardrail_kpi": "train_only_preselector_no_wfo_no_mt5_no_onnx_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_preselector_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_preselector_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "proxy_scout_no_runtime(프록시 탐색, 런타임 아님)",
        "scoreboard_lane": "proxy_scout(프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"candidate={final['candidate_rows']};scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']}",
        "guardrail_kpi": "train_only_preselector_validation_oos_read_only_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"source_branch_scout={final['source_branch_scout_rows']};veto_branch_scout={final['veto_branch_scout_rows']};next={final['next_run_id']}",
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
        "notes": "Tier B not materialized in F30B proxy(전선30B 프록시에서 티어 B 미물질화)",
    })
    tier_ab = dict(primary)
    tier_ab.update({
        "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "record_view": "Tier A+B combined(티어 A+B 합산)",
        "tier_scope": "Tier A+B(티어 A+B)",
        "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)",
        "primary_kpi": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": "Combined tier not claimed in F30B proxy(전선30B 프록시에서 합산 티어 주장 없음)",
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


def report_text(final: dict[str, Any], candidates: pd.DataFrame) -> str:
    best = final["best_forward_readonly_candidate"]
    top_rows = top_forward_table(candidates)
    return f"""# Frontier30B Train Density Preserving Preselector Proxy Report(전선30B 학습 밀도 보존 사전 선택기 프록시 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F30A lock(전선30A 잠금)의 `top_160` train-only preselector(학습 전용 사전 선택기)를 F28/F29 reference surface(참조 표면)에 적용했습니다.

Effect(효과): selection(선택)은 train-only preselector score(학습 전용 사전 선택기 점수)만 사용했고, validation/OOS(검증/표본외)는 read-only(읽기 전용)로만 scout/seed/handoff(탐색/씨앗/인계)를 판독했습니다.

Source/preselected/candidate rows(원천/사전 선택/후보 행): `{final['source_rows']}` / `{final['preselected_source_rows']}` / `{final['candidate_rows']}`

Branch rows(분기 행): source no-veto(원천 무차단) `{final['source_branch_rows']}`, density-preserving veto(밀도 보존 차단) `{final['veto_branch_rows']}`

Density/scout/seed/handoff rows(밀도/탐색/씨앗/인계 행): `{final['density_bridge_rows']}` / `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Scout split(탐색 분해): source branch(원천 분기) `{final['source_branch_scout_rows']}`, veto branch(차단 분기) `{final['veto_branch_scout_rows']}`

Best forward read-only candidate(최상 전진 읽기 전용 후보): `{final['best_forward_readonly_candidate_id']}` from source(원천) `{best.get('source_stability_union_id', '')}` branch(분기) `{best.get('branch', '')}`

Best validation PF/density/DD(최상 검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk'))}`

Best OOS PF/density/DD(최상 표본외 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk'))}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Top Read-Only Forward Rows(상위 읽기 전용 전진 행)

{top_rows}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def top_forward_table(candidates: pd.DataFrame) -> str:
    if candidates.empty:
        return "No candidates(후보 없음)."
    rows = candidates.sort_values("forward_read_score", ascending=False).head(12)
    lines = [
        "| candidate(후보) | branch(분기) | source(원천) | train score(학습 점수) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed | handoff |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for _, row in rows.iterrows():
        lines.append(
            f"| `{row['candidate_id']}` | `{row['branch']}` | `{row['source_stability_union_id']}` | "
            f"{fmt(row['train_only_preselector_score'])} | {fmt(row['validation_profit_factor'])} | "
            f"{fmt(row['validation_trades_per_day'])} | {fmt(row['validation_dd_risk'])} | "
            f"{fmt(row['oos_profit_factor'])} | {fmt(row['oos_trades_per_day'])} | {fmt(row['oos_dd_risk'])} | "
            f"{bool(row['scout_clue_flag'])} | {bool(row['seed_surface_flag'])} | {bool(row['handoff_candidate_flag'])} |"
        )
    return "\n".join(lines)


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier30B Gate Audit(전선30B 게이트 감사)

- stage_open_lock_gate(단계 개방 잠금 게이트): `{F30A_LOCK.as_posix()}` read(읽음)
- source_surface_gate(원천 표면 게이트): `{F28B_CANDIDATE_SUMMARY.as_posix()}` rows(행) `{final['source_rows']}`
- veto_surface_gate(차단 표면 게이트): `{F29B_CANDIDATE_SUMMARY.as_posix()}` used as reference(참조로 사용)
- train_only_selection_gate(학습 전용 선택 게이트): preselector score(사전 선택기 점수)는 train inputs(학습 입력)만 사용
- leakage_guard(누수 방어): validation/OOS(검증/표본외)는 read-only diagnostics(읽기 전용 진단)
- tier_pair_gate(티어 쌍 게이트): Tier B(티어 B)는 missing_required(필수 누락), Tier A+B(티어 A+B)는 out_of_scope_by_claim(주장 범위 밖)
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier30 Selection Status(전선30 선택 상태)

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest proxy(최근 프록시): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Scout/seed/handoff(탐색/씨앗/인계): `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

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

Action(행동): F30B(전선30B)는 train-only density-preserving preselector(학습 전용 밀도 보존 사전 선택기)를 실행했습니다.

Effect(효과): scout clue(탐색 단서) `{final['scout_clue_rows']}`개를 만들었지만 seed/handoff(씨앗/인계)는 `{final['seed_surface_rows']}/{final['handoff_candidate_rows']}`개라서, MT5/ONNX/WFO(MT5/온엑스/워크포워드 최적화)는 아직 실행하지 않습니다.

Runtime probe boundary(런타임 탐침 경계): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran train-only density-preserving preselector proxy(학습 전용 밀도 보존 사전 선택기 프록시). "
        f"Effect(효과): candidates={final['candidate_rows']}, scout={final['scout_clue_rows']}, seed={final['seed_surface_rows']}, handoff={final['handoff_candidate_rows']}, next=`{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR30-TRAIN-DENSITY-PRESERVING-PRESELECTOR-BEFORE-LOSS-VETO-ONNX-SCOUT`: `{RUN_ID}` produced scout clue rows(탐색 단서 행) `{final['scout_clue_rows']}` but handoff(인계) `{final['handoff_candidate_rows']}`. "
        "Effect(효과): F30 moves to repair-or-closeout(수리 또는 마감) without runtime authority(런타임 권위 없음).\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing"}


def sha256_io(path: Path) -> str:
    return hashlib.sha256(io_path(path).read_bytes()).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.3f}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
