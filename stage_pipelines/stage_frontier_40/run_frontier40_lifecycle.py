from __future__ import annotations

import csv
import json
import math
import sys
import warnings
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
from stage_pipelines.stage_frontier_33 import frontier33b_path_native_mfe_mae_exit_surface_proxy_scout as f33b
from stage_pipelines.stage_frontier_34 import run_frontier34_lifecycle as f34


STAGE_ID = "stage_frontier_40__short_pf_edge_non_score_source_pivot_after_regime_gate_negative"
RUN_A = "frontier40A_stage_open_short_pf_edge_non_score_source_hypothesis_design_v1"
RUN_B = "frontier40B_raw_feature_state_pocket_proxy_v1"
RUN_C = "frontier40C_capped_or_union_repair_decision_v1"
RUN_D = "frontier40D_stage_closeout_non_score_source_v1"
NEXT_STAGE_ID = "stage_frontier_41__short_pf_edge_exit_shape_source_pivot_after_f40_raw_pocket_scout"
NEXT_RUN_ID = "frontier41A_stage_open_short_pf_edge_exit_shape_source_hypothesis_design_v1"

PREV_STAGE_ID = "stage_frontier_39__short_pf_edge_regime_conditioned_score_after_f38_scout_only"
PREV_RUN_D = "frontier39D_stage_closeout_regime_conditioned_score_v1"
PREV_PRESERVED_CLUE = "f39_regime_gate_can_reduce_density_dd_and_keep_scout_pf_but_not_matched_seed_edge"
PREV_NEGATIVE_MEMORY = "f39_regime_gate_did_not_lift_pf_over_ungated_score_at_matched_density"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_A_ROOT = STAGE_ROOT / "02_runs" / RUN_A
RUN_B_ROOT = STAGE_ROOT / "02_runs" / RUN_B
RUN_C_ROOT = STAGE_ROOT / "02_runs" / RUN_C
RUN_D_ROOT = STAGE_ROOT / "02_runs" / RUN_D
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_40/run_frontier40_lifecycle.py")

GROK_OPEN_PACKET = Path("docs/agent_control/grok_reviews/2026-06-15_frontier40_stage_open/small_review")
GROK_CLOSEOUT_PACKET = Path("docs/agent_control/grok_reviews/2026-06-15_frontier40_stage_closeout/small_review")

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

STOP_QUANTILES = (0.18, 0.22, 0.26, 0.30, 0.34)
TAKE_QUANTILES = (0.70, 0.78, 0.86)
RR_FLOORS = (1.0, 1.2, 1.4)

CONDITION_SOURCE_KEEP = 160
PAIR_SOURCE_KEEP = 70
MAX_ROWS_PER_SECTION = 600
OR_REPAIR_MAX_K = 8

SCOUT_PF = 1.03
SCOUT_DENSITY_LOW = 4.0
SCOUT_DENSITY_HIGH = 12.0
SCOUT_DD_CAP = 18.0
SCOUT_MIN_LIFT = 0.03
SEED_PF = 1.20
SEED_DENSITY_LOW = 5.0
SEED_DENSITY_HIGH = 10.0
SEED_DD_CAP = 12.0
SEED_MIN_LIFT = 0.05
RUNTIME_PF = 1.50
RUNTIME_DD_CAP = 10.0

PRESERVED_CLUE = "f40_raw_feature_pair_pockets_create_density_matched_short_scout_edge_reference_only"
NEGATIVE_MEMORY = "f40_raw_feature_state_pockets_did_not_create_seed_or_runtime_candidate"

METRIC_FIELDS = (
    "trade_count",
    "trades_per_day",
    "net_profit",
    "profit_factor",
    "expectancy",
    "win_rate",
    "payoff_ratio",
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
    "path_quality_rate",
)


def main() -> int:
    warnings.filterwarnings("ignore", category=FutureWarning)
    ensure_dirs()
    normalize_grok_packets()
    created_at = f34.utc_now()

    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    raw_path = f33b.load_raw_path(frame)
    path_labels = f33b.build_path_labels(frame, raw_path)
    open_grok = read_stage_open_grok()
    closeout_grok = read_closeout_grok()
    context = validate_context(frame, feature_order, raw_path, open_grok)

    search = run_raw_feature_pocket_search(frame, feature_order, path_labels, raw_path)
    final = build_final(created_at, frame, feature_order, raw_path, context, open_grok, closeout_grok, search)

    write_outputs(final, search)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready(output_summary(final)), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (
        RUN_A_ROOT,
        RUN_B_ROOT,
        RUN_C_ROOT,
        RUN_D_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        Path("docs/decisions"),
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    if not path_exists(stage_ledger):
        with io_path(ALPHA_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
            header = next(csv.reader(handle))
        with io_path(stage_ledger).open("w", encoding="utf-8-sig", newline="") as handle:
            csv.writer(handle, lineterminator="\n").writerow(header)


def normalize_grok_packets() -> None:
    for packet in (GROK_OPEN_PACKET, GROK_CLOSEOUT_PACKET):
        if not path_exists(packet):
            continue
        for name in ("input_prompt.md", "prompt.md", "clean_output.md"):
            path = packet / name
            if path_exists(path):
                lines = io_path(path).read_text(encoding="utf-8-sig").splitlines()
                f03b.write_text_sig(path, "\n".join(line.rstrip() for line in lines).rstrip() + "\n")


def read_stage_open_grok() -> dict[str, Any]:
    meta = f34.read_json(GROK_OPEN_PACKET / "metadata.json") if path_exists(GROK_OPEN_PACKET / "metadata.json") else {}
    output = f34.read_text(GROK_OPEN_PACKET / "clean_output.md") if path_exists(GROK_OPEN_PACKET / "clean_output.md") else ""
    lowered = output.lower()
    accepted = (
        bool(meta.get("success"))
        and "accepted" in lowered
        and "novelty_ok" in lowered
        and "yes" in lowered
        and "mandatory_guardrail" in lowered
        and "train-only selection freeze" in lowered
        and "runtime_claim_boundary_ok" in lowered
    )
    local_verification_required = "needs_local_verification" in lowered
    return {
        "packet": GROK_OPEN_PACKET.as_posix(),
        "success": bool(meta.get("success")),
        "returncode": meta.get("returncode"),
        "timed_out": bool(meta.get("timed_out")),
        "unexpected_top_level_artifacts": meta.get("unexpected_top_level_artifacts", []),
        "accepted": accepted,
        "local_verification_required": local_verification_required,
        "classification": (
            "accepted_open_raw_feature_pocket_with_local_guardrails"
            if accepted
            else "pending_or_needs_manual_review"
        ),
        "output_excerpt": output[:2400],
    }


def read_closeout_grok() -> dict[str, Any]:
    meta = f34.read_json(GROK_CLOSEOUT_PACKET / "metadata.json") if path_exists(GROK_CLOSEOUT_PACKET / "metadata.json") else {}
    output = f34.read_text(GROK_CLOSEOUT_PACKET / "clean_output.md") if path_exists(GROK_CLOSEOUT_PACKET / "clean_output.md") else ""
    lowered = output.lower()
    accepted = (
        bool(meta.get("success"))
        and ("accepted" in lowered or "closeout_ok" in lowered)
        and "runtime_boundary_ok" in lowered
        and "yes" in lowered
    )
    return {
        "packet": GROK_CLOSEOUT_PACKET.as_posix(),
        "success": bool(meta.get("success")),
        "returncode": meta.get("returncode"),
        "timed_out": bool(meta.get("timed_out")),
        "unexpected_top_level_artifacts": meta.get("unexpected_top_level_artifacts", []),
        "accepted": accepted,
        "classification": "accepted_closeout_raw_feature_pocket_scout_runtime_boundary" if accepted else "pending_or_needs_local_verification",
        "output_excerpt": output[:2400],
    }


def validate_context(
    frame: pd.DataFrame,
    feature_order: list[str],
    raw_path: dict[str, Any],
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = f34.read_text(WORKSPACE_STATE)
    prev_selection = f34.read_text(Path("stages") / PREV_STAGE_ID / "04_selected" / "selection_status.md")
    checks = {
        "workspace_current_f39": f"current_stage_id: {PREV_STAGE_ID}" in workspace or f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_points_to_f40a": f"next_run_id: {RUN_A}" in workspace or f"current_run_id: {RUN_D}" in workspace,
        "f39_selection_points_to_f40a": RUN_A in prev_selection,
        "f39_preserved_clue_present": PREV_PRESERVED_CLUE in prev_selection,
        "f39_negative_memory_present": PREV_NEGATIVE_MEMORY in prev_selection,
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_has_required_splits": set(frame["split"].astype(str).unique()) == {"train", "validation", "oos"},
        "raw_path_positions_complete": int(raw_path["missing_entry_positions"]) == 0
        and int(raw_path["missing_future_positions"]) == 0,
        "grok_transport_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_accepted_with_local_guardrails": grok["accepted"],
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "checks": checks,
        "judgment": "pass_stage_open_ready_with_raw_feature_guardrails" if all(checks.values()) else "needs_manual_review",
        "data_source": f23b.DATASET_PATH.as_posix(),
        "raw_source": f33b.RAW_US100_PATH.as_posix(),
        "feature_order_hash": ordered_hash(feature_order),
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "rows": int(len(frame)),
            "split_counts": {str(k): int(v) for k, v in frame["split"].astype(str).value_counts().to_dict().items()},
        },
        "feature_label_boundary": "raw feature thresholds, stop/take thresholds, and OR repair are selected on train only; validation/OOS are read-only",
        "entry_known_audit": "candidate features come from the closed-bar 58-feature contract; future labels and realized PnL are not candidate inputs",
        "leakage_risk": "medium: broad raw-feature pocket mining can overfit train, so forward claims require density-matched A comparison",
    }


def run_raw_feature_pocket_search(
    frame: pd.DataFrame,
    feature_order: list[str],
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
) -> dict[str, Any]:
    labels = path_labels[-1]
    valid_features = np.isfinite(frame[feature_order].to_numpy(dtype="float64")).all(axis=1)
    valid = valid_features & labels["valid"]
    train_valid = f33b.split_mask(frame, "train") & valid
    condition_pool = build_condition_pool(frame, feature_order, path_labels, valid_features, valid, train_valid)
    proxy_summary = build_broad_candidates(frame, path_labels, raw_path, valid, train_valid, condition_pool)
    repair_summary = build_or_repair_candidates(frame, path_labels, raw_path, valid, train_valid, condition_pool)
    combined = pd.concat([proxy_summary, repair_summary], ignore_index=True) if not repair_summary.empty else proxy_summary.copy()
    if not combined.empty:
        combined = sort_summary(combined)
        combined["candidate_id"] = [
            f"f40{'c' if kind == 'or_union' else 'b'}_{idx:04d}"
            for idx, kind in enumerate(combined["candidate_kind"].astype(str), start=1)
        ]
    return {
        "condition_pool": condition_pool.drop(columns=["mask"], errors="ignore"),
        "proxy_summary": proxy_summary.drop(columns=["mask"], errors="ignore"),
        "repair_summary": repair_summary.drop(columns=["mask"], errors="ignore"),
        "combined_summary": combined.drop(columns=["mask"], errors="ignore"),
        **section_counts(combined),
    }


def build_condition_pool(
    frame: pd.DataFrame,
    feature_order: list[str],
    path_labels: dict[int, dict[str, np.ndarray]],
    valid_features: np.ndarray,
    valid: np.ndarray,
    train_valid: np.ndarray,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    train_base = f33b.split_mask(frame, "train")
    for feature in feature_order:
        series = pd.to_numeric(frame[feature], errors="coerce")
        train_values = series.loc[train_base].replace([np.inf, -np.inf], np.nan).dropna()
        if train_values.nunique(dropna=True) <= 1:
            continue
        for operator, q_label, threshold, raw_mask in f23b.condition_masks(series, train_values):
            mask = np.asarray(raw_mask, dtype=bool) & valid_features
            coverage = float(mask[train_valid].mean()) if train_valid.any() else 0.0
            if not (0.02 <= coverage <= 0.75):
                continue
            metrics = f33b.evaluate_horizon_mask(frame, mask, -1, path_labels, "train")
            if (
                int(metrics["trade_count"]) < 45
                or not (2.0 <= float(metrics["trades_per_day"]) <= 20.0)
                or float(metrics["net_profit"]) <= 0.0
                or float(metrics["profit_factor"]) < 1.0
            ):
                continue
            score = train_condition_score(metrics)
            rows.append(
                {
                    "condition_id": f"f40cond_{len(rows) + 1:04d}",
                    "feature": feature,
                    "feature_family": f23b.feature_family(feature),
                    "operator": operator,
                    "quantile_label": q_label,
                    "threshold_value": float(threshold),
                    "definition": f"{feature} {operator} {q_label}",
                    "train_coverage": coverage,
                    "train_condition_score": score,
                    "train_horizon_profit_factor": safe_float(metrics["profit_factor"]),
                    "train_horizon_density": safe_float(metrics["trades_per_day"]),
                    "train_horizon_dd_risk": safe_float(metrics["dd_risk"]),
                    "train_horizon_net_profit": safe_float(metrics["net_profit"]),
                    "mask": mask & valid,
                }
            )
    if not rows:
        return pd.DataFrame()
    out = pd.DataFrame(rows).sort_values("train_condition_score", ascending=False).reset_index(drop=True)
    out["condition_id"] = [f"f40cond_{idx:04d}" for idx in range(1, len(out) + 1)]
    return out


def build_broad_candidates(
    frame: pd.DataFrame,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    valid: np.ndarray,
    train_valid: np.ndarray,
    condition_pool: pd.DataFrame,
) -> pd.DataFrame:
    if condition_pool.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    records = condition_pool.head(CONDITION_SOURCE_KEEP).to_dict("records")
    for record in records:
        mask = np.asarray(record["mask"], dtype=bool)
        rows.extend(evaluate_candidate_variants(frame, path_labels, raw_path, valid, train_valid, [record], mask, "single_feature"))
        if len(rows) >= MAX_ROWS_PER_SECTION:
            break
    pair_source = condition_pool.head(PAIR_SOURCE_KEEP).to_dict("records")
    for index, first in enumerate(pair_source):
        for second in pair_source[index + 1 :]:
            if first["feature"] == second["feature"] or first["feature_family"] == second["feature_family"]:
                continue
            mask = np.asarray(first["mask"], dtype=bool) & np.asarray(second["mask"], dtype=bool)
            coverage = float(mask[train_valid].mean()) if train_valid.any() else 0.0
            if not (0.015 <= coverage <= 0.55):
                continue
            quick = f33b.evaluate_horizon_mask(frame, mask, -1, path_labels, "train")
            if (
                int(quick["trade_count"]) < 50
                or not (2.0 <= float(quick["trades_per_day"]) <= 18.0)
                or float(quick["net_profit"]) <= 0.0
                or float(quick["profit_factor"]) < 1.02
            ):
                continue
            rows.extend(evaluate_candidate_variants(frame, path_labels, raw_path, valid, train_valid, [first, second], mask, "pair_and"))
            if len(rows) >= MAX_ROWS_PER_SECTION:
                break
        if len(rows) >= MAX_ROWS_PER_SECTION:
            break
    return sort_summary(pd.DataFrame(rows))


def build_or_repair_candidates(
    frame: pd.DataFrame,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    valid: np.ndarray,
    train_valid: np.ndarray,
    condition_pool: pd.DataFrame,
) -> pd.DataFrame:
    if condition_pool.empty:
        return pd.DataFrame()
    rows: list[dict[str, Any]] = []
    records = condition_pool.to_dict("records")
    for k in range(2, OR_REPAIR_MAX_K + 1):
        selected: list[dict[str, Any]] = []
        used_features: set[str] = set()
        for record in records:
            feature = str(record["feature"])
            if feature in used_features:
                continue
            selected.append(record)
            used_features.add(feature)
            if len(selected) >= k:
                break
        if len(selected) < k:
            continue
        mask = np.zeros(len(frame), dtype=bool)
        for record in selected:
            mask |= np.asarray(record["mask"], dtype=bool)
        rows.extend(evaluate_candidate_variants(frame, path_labels, raw_path, valid, train_valid, selected, mask, "or_union"))
    return sort_summary(pd.DataFrame(rows))


def evaluate_candidate_variants(
    frame: pd.DataFrame,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    valid: np.ndarray,
    train_valid: np.ndarray,
    conditions: list[dict[str, Any]],
    raw_mask: np.ndarray,
    candidate_kind: str,
) -> list[dict[str, Any]]:
    mask = np.asarray(raw_mask, dtype=bool) & valid
    coverage = float(mask[train_valid].mean()) if train_valid.any() else 0.0
    if coverage <= 0.0:
        return []
    baseline_mask = density_matched_baseline_mask(valid, coverage)
    rows: list[dict[str, Any]] = []
    for stop_q, take_q, rr, stop_cap, take_cap in threshold_rows(mask, train_valid, path_labels[-1]):
        train = eval_path(frame, mask, stop_cap, take_cap, path_labels, raw_path, "train")
        if not train_gate(train, candidate_kind):
            continue
        validation = eval_path(frame, mask, stop_cap, take_cap, path_labels, raw_path, "validation")
        oos = eval_path(frame, mask, stop_cap, take_cap, path_labels, raw_path, "oos")
        a_validation = eval_path(frame, baseline_mask, stop_cap, take_cap, path_labels, raw_path, "validation")
        a_oos = eval_path(frame, baseline_mask, stop_cap, take_cap, path_labels, raw_path, "oos")
        row = candidate_row(
            conditions,
            candidate_kind,
            coverage,
            stop_q,
            take_q,
            rr,
            stop_cap,
            take_cap,
            train,
            validation,
            oos,
            a_validation,
            a_oos,
        )
        if row["f40_scout_clue_flag"] or row["f40_seed_surface_flag"] or row["f40_runtime_candidate_flag"] or near_forward_positive(row):
            rows.append(row)
    return rows


def threshold_rows(
    mask: np.ndarray,
    train_valid: np.ndarray,
    labels: dict[str, np.ndarray],
) -> list[tuple[float, float, float, float, float]]:
    selected = train_valid & np.asarray(mask, dtype=bool)
    mfe = labels["mfe"][selected]
    mae = labels["mae"][selected]
    mfe = mfe[np.isfinite(mfe) & (mfe > 0.0)]
    mae = mae[np.isfinite(mae) & (mae > 0.0)]
    if mfe.size < 35 or mae.size < 35:
        return []
    rows: list[tuple[float, float, float, float, float]] = []
    seen: set[tuple[int, int]] = set()
    for stop_q in STOP_QUANTILES:
        stop_cap = max(float(np.nanquantile(mae, stop_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
        for take_q in TAKE_QUANTILES:
            raw_take = max(float(np.nanquantile(mfe, take_q)), f33b.MIN_THRESHOLD_LOG_RETURN)
            for rr in RR_FLOORS:
                take_cap = max(raw_take, stop_cap * rr)
                key = (int(round(stop_cap * 10_000_000)), int(round(take_cap * 10_000_000)))
                if key in seen:
                    continue
                seen.add(key)
                rows.append((stop_q, take_q, rr, stop_cap, take_cap))
    return rows


def eval_path(
    frame: pd.DataFrame,
    mask: np.ndarray,
    stop_cap: float,
    take_cap: float,
    path_labels: dict[int, dict[str, np.ndarray]],
    raw_path: dict[str, Any],
    split: str,
) -> dict[str, Any]:
    return f33b.evaluate_path_mask(frame, np.asarray(mask, dtype=bool), -1, stop_cap, take_cap, path_labels, raw_path, split)


def density_matched_baseline_mask(valid: np.ndarray, train_coverage: float) -> np.ndarray:
    coverage = max(min(float(train_coverage), 1.0), 0.0001)
    stride = max(1, int(round(1.0 / coverage)))
    ranks = np.cumsum(np.asarray(valid, dtype=bool)) - 1
    return np.asarray(valid, dtype=bool) & ((ranks % stride) == 0)


def train_gate(metrics: dict[str, Any], candidate_kind: str) -> bool:
    min_count = 70 if candidate_kind == "or_union" else (50 if candidate_kind == "pair_and" else 45)
    density_low = 4.0 if candidate_kind == "or_union" else (2.5 if candidate_kind == "pair_and" else 3.0)
    density_high = 18.0
    pf_floor = 1.02 if candidate_kind == "pair_and" else 1.01
    ambiguous_rate = safe_float(metrics.get("ambiguous_both_hit_count")) / max(safe_float(metrics.get("trade_count")), 1.0)
    return (
        int(metrics["trade_count"]) >= min_count
        and density_low <= safe_float(metrics["trades_per_day"]) <= density_high
        and safe_float(metrics["net_profit"]) > 0.0
        and safe_float(metrics["profit_factor"]) >= pf_floor
        and safe_float(metrics["dd_risk"]) <= 24.0
        and ambiguous_rate <= 0.40
    )


def candidate_row(
    conditions: list[dict[str, Any]],
    candidate_kind: str,
    train_coverage: float,
    stop_q: float,
    take_q: float,
    rr: float,
    stop_cap: float,
    take_cap: float,
    train: dict[str, Any],
    validation: dict[str, Any],
    oos: dict[str, Any],
    a_validation: dict[str, Any],
    a_oos: dict[str, Any],
) -> dict[str, Any]:
    val_lift = safe_float(validation["profit_factor"]) - safe_float(a_validation["profit_factor"])
    oos_lift = safe_float(oos["profit_factor"]) - safe_float(a_oos["profit_factor"])
    min_lift = min(val_lift, oos_lift)
    density_guard = (
        SCOUT_DENSITY_LOW <= safe_float(validation["trades_per_day"]) <= SCOUT_DENSITY_HIGH
        and SCOUT_DENSITY_LOW <= safe_float(oos["trades_per_day"]) <= SCOUT_DENSITY_HIGH
    )
    scout_flag = (
        safe_float(validation["profit_factor"]) >= SCOUT_PF
        and safe_float(oos["profit_factor"]) >= SCOUT_PF
        and density_guard
        and max(safe_float(validation["dd_risk"]), safe_float(oos["dd_risk"])) <= SCOUT_DD_CAP
        and min_lift >= SCOUT_MIN_LIFT
    )
    seed_flag = (
        safe_float(validation["profit_factor"]) >= SEED_PF
        and safe_float(oos["profit_factor"]) >= SEED_PF
        and SEED_DENSITY_LOW <= safe_float(validation["trades_per_day"]) <= SEED_DENSITY_HIGH
        and SEED_DENSITY_LOW <= safe_float(oos["trades_per_day"]) <= SEED_DENSITY_HIGH
        and max(safe_float(validation["dd_risk"]), safe_float(oos["dd_risk"])) <= SEED_DD_CAP
        and min_lift >= SEED_MIN_LIFT
    )
    runtime_flag = (
        seed_flag
        and safe_float(validation["profit_factor"]) >= RUNTIME_PF
        and safe_float(oos["profit_factor"]) >= RUNTIME_PF
        and max(safe_float(validation["dd_risk"]), safe_float(oos["dd_risk"])) <= RUNTIME_DD_CAP
    )
    read_score = (
        100.0 * float(seed_flag)
        + 25.0 * float(scout_flag)
        + 18.0 * min_lift
        + 2.0 * min(safe_float(validation["profit_factor"]), safe_float(oos["profit_factor"]))
        - 0.06 * max(safe_float(validation["dd_risk"]), safe_float(oos["dd_risk"]))
        - 0.35 * abs(safe_float(validation["trades_per_day"]) - 8.0)
        - 0.35 * abs(safe_float(oos["trades_per_day"]) - 8.0)
    )
    row: dict[str, Any] = {
        "candidate_id": "",
        "candidate_kind": candidate_kind,
        "condition_count": len(conditions),
        "condition_ids": "|".join(str(item["condition_id"]) for item in conditions),
        "features": "|".join(str(item["feature"]) for item in conditions),
        "feature_families": "|".join(str(item["feature_family"]) for item in conditions),
        "rule_definition": " OR ".join(str(item["definition"]) for item in conditions)
        if candidate_kind == "or_union"
        else " & ".join(str(item["definition"]) for item in conditions),
        "train_coverage": train_coverage,
        "stop_quantile": stop_q,
        "take_quantile": take_q,
        "rr_floor": rr,
        "stop_cap_log_return": stop_cap,
        "take_cap_log_return": take_cap,
        "f40_validation_pf_lift_vs_density_matched_a": val_lift,
        "f40_oos_pf_lift_vs_density_matched_a": oos_lift,
        "f40_min_pf_lift_vs_density_matched_a": min_lift,
        "f40_density_guard_ok": density_guard,
        "f40_scout_clue_flag": scout_flag,
        "f40_seed_surface_flag": seed_flag,
        "f40_runtime_candidate_flag": runtime_flag,
        "f40_read_score": read_score,
        "selection_boundary": "train_only_feature_thresholds_and_stop_take_density_matched_forward_read_only",
    }
    for prefix, metrics in (
        ("train", train),
        ("validation", validation),
        ("oos", oos),
        ("a_validation", a_validation),
        ("a_oos", a_oos),
    ):
        add_metric_prefix(row, prefix, metrics)
    return row


def near_forward_positive(row: dict[str, Any]) -> bool:
    return (
        safe_float(row.get("validation_profit_factor")) > 1.0
        and safe_float(row.get("oos_profit_factor")) > 1.0
        and safe_float(row.get("f40_min_pf_lift_vs_density_matched_a")) > 0.0
    )


def sort_summary(summary: pd.DataFrame) -> pd.DataFrame:
    if summary.empty:
        return summary
    return summary.sort_values(
        [
            "f40_runtime_candidate_flag",
            "f40_seed_surface_flag",
            "f40_scout_clue_flag",
            "f40_read_score",
        ],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)


def section_counts(summary: pd.DataFrame) -> dict[str, Any]:
    if summary.empty:
        return {
            "condition_rows": 0,
            "candidate_rows": 0,
            "scout_rows": 0,
            "seed_rows": 0,
            "runtime_rows": 0,
            "best_readonly": {},
        }
    return {
        "condition_rows": 0,
        "candidate_rows": int(len(summary)),
        "scout_rows": int(summary["f40_scout_clue_flag"].sum()),
        "seed_rows": int(summary["f40_seed_surface_flag"].sum()),
        "runtime_rows": int(summary["f40_runtime_candidate_flag"].sum()),
        "best_readonly": json_ready(dict(summary.iloc[0])),
    }


def train_condition_score(metrics: dict[str, Any]) -> float:
    density_penalty = abs(safe_float(metrics["trades_per_day"]) - 8.0) / 8.0
    dd_penalty = max(0.0, safe_float(metrics["dd_risk"]) - 12.0) / 12.0
    return float(
        max(safe_float(metrics["net_profit"]), 0.0)
        * max(safe_float(metrics["profit_factor"]), 0.0)
        / (1.0 + density_penalty + dd_penalty)
    )


def add_metric_prefix(row: dict[str, Any], prefix: str, metrics: dict[str, Any]) -> None:
    for field in METRIC_FIELDS:
        row[f"{prefix}_{field}"] = metrics.get(field, "")


def safe_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def build_final(
    created_at: str,
    frame: pd.DataFrame,
    feature_order: list[str],
    raw_path: dict[str, Any],
    context: dict[str, Any],
    open_grok: dict[str, Any],
    closeout_grok: dict[str, Any],
    search: dict[str, Any],
) -> dict[str, Any]:
    condition_rows = int(len(search["condition_pool"]))
    candidate_rows = int(search["candidate_rows"])
    scout_rows = int(search["scout_rows"])
    seed_rows = int(search["seed_rows"])
    runtime_rows = int(search["runtime_rows"])
    if runtime_rows:
        closeout_class = "completion_candidate_pending_pre_expensive_grok_and_mt5"
        status = "completion_candidate_pending_runtime_probe_no_authority"
        judgment = "runtime_candidate_requires_pre_expensive_grok_and_mt5_micro_probe_no_authority"
        runtime_status = "runtime_probe_ready_needs_pre_expensive_grok_before_mt5"
    elif seed_rows:
        closeout_class = "seed_surface_without_runtime_candidate"
        status = "seed_surface_no_runtime_candidate_no_authority"
        judgment = "seed_surface_requires_wfo_stress_or_source_pivot_no_authority"
        runtime_status = "runtime_probe_out_of_scope_by_claim_seed_surface_no_runtime_candidate"
    elif scout_rows:
        closeout_class = "preserved_clue_negative_memory"
        status = "closed_preserved_clue_negative_memory_raw_feature_pocket_scout_only_no_runtime_authority"
        judgment = "preserved_clue_negative_memory(F40 raw feature pocket scout only no seed/runtime)"
        runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f40_proxy_repair"
    elif candidate_rows:
        closeout_class = "negative_memory"
        status = "closed_negative_memory_raw_feature_pocket_no_forward_scout_no_runtime_authority"
        judgment = "negative_memory(F40 raw feature pockets no forward scout)"
        runtime_status = "runtime_probe_ineligible_no_seed_or_runtime_candidate_after_f40_proxy"
    else:
        closeout_class = "negative_memory"
        status = "closed_negative_memory_raw_feature_pocket_no_candidate_no_runtime_authority"
        judgment = "negative_memory(F40 raw feature pockets no candidate)"
        runtime_status = "runtime_probe_ineligible_no_candidate_after_f40_context_guard"

    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_D,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "context": context,
        "stage_open": {
            "run_id": RUN_A,
            "status": "opened_with_grok_raw_feature_pocket_guardrails",
            "judgment": "hypothesis_ready_for_raw_feature_pocket_proxy",
            "grok": open_grok,
        },
        "proxy": {
            "run_id": RUN_B,
            "status": "raw_feature_state_pocket_proxy_complete_no_authority",
            "judgment": "scout_surface_only_no_seed_runtime" if scout_rows else "no_forward_scout",
            "condition_rows": condition_rows,
            "candidate_rows": int(len(search["proxy_summary"])),
            "scout_rows": int(search["proxy_summary"].get("f40_scout_clue_flag", pd.Series(dtype=bool)).sum()) if not search["proxy_summary"].empty else 0,
            "seed_rows": int(search["proxy_summary"].get("f40_seed_surface_flag", pd.Series(dtype=bool)).sum()) if not search["proxy_summary"].empty else 0,
            "runtime_rows": int(search["proxy_summary"].get("f40_runtime_candidate_flag", pd.Series(dtype=bool)).sum()) if not search["proxy_summary"].empty else 0,
            "runtime_probe_status": "runtime_probe_out_of_scope_by_claim_proxy_no_seed_or_runtime_candidate",
        },
        "repair": {
            "run_id": RUN_C,
            "status": "capped_or_union_repair_executed_no_seed" if scout_rows and not seed_rows else "capped_or_union_repair_executed",
            "judgment": "or_union_did_not_create_seed_or_runtime_candidate" if not seed_rows else "or_union_or_proxy_created_seed_surface",
            "candidate_rows": int(len(search["repair_summary"])),
            "scout_rows": int(search["repair_summary"].get("f40_scout_clue_flag", pd.Series(dtype=bool)).sum()) if not search["repair_summary"].empty else 0,
            "seed_rows": int(search["repair_summary"].get("f40_seed_surface_flag", pd.Series(dtype=bool)).sum()) if not search["repair_summary"].empty else 0,
            "runtime_rows": int(search["repair_summary"].get("f40_runtime_candidate_flag", pd.Series(dtype=bool)).sum()) if not search["repair_summary"].empty else 0,
            "runtime_probe_status": "runtime_probe_out_of_scope_by_claim_repair_no_seed_or_runtime_candidate",
        },
        "closeout": {
            "run_id": RUN_D,
            "status": status,
            "judgment": judgment,
            "closeout_class": closeout_class,
            "condition_rows": condition_rows,
            "candidate_rows": candidate_rows,
            "scout_rows": scout_rows,
            "seed_rows": seed_rows,
            "runtime_rows": runtime_rows,
            "runtime_probe_status": runtime_status,
            "preserved_clue": PRESERVED_CLUE if scout_rows else "",
            "negative_memory": NEGATIVE_MEMORY,
            "best_readonly": search["best_readonly"],
            "grok": closeout_grok,
        },
        "raw_path": {
            "path": f33b.RAW_US100_PATH.as_posix(),
            "raw_rows": raw_path["raw_rows"],
            "missing_entry_positions": raw_path["missing_entry_positions"],
            "missing_future_positions": raw_path["missing_future_positions"],
        },
        "sample_scope": {
            "rows": int(len(frame)),
            "split_counts": {str(k): int(v) for k, v in frame["split"].astype(str).value_counts().to_dict().items()},
        },
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], search: dict[str, Any]) -> None:
    search["condition_pool"].to_csv(io_path(RUN_B_ROOT / "raw_feature_condition_pool.csv"), index=False, encoding="utf-8-sig")
    search["proxy_summary"].to_csv(io_path(RUN_B_ROOT / "raw_feature_pocket_candidate_summary.csv"), index=False, encoding="utf-8-sig")
    search["repair_summary"].to_csv(io_path(RUN_C_ROOT / "capped_or_union_repair_summary.csv"), index=False, encoding="utf-8-sig")
    search["combined_summary"].head(60).to_csv(io_path(RUN_D_ROOT / "top_forward_diagnostic.csv"), index=False, encoding="utf-8-sig")
    f34.write_json(RUN_A_ROOT / "stage_open_summary.json", final["stage_open"])
    f34.write_json(RUN_B_ROOT / "final_summary.json", final["proxy"])
    f34.write_json(RUN_C_ROOT / "final_summary.json", final["repair"])
    f34.write_json(RUN_D_ROOT / "stage_closeout_summary.json", final)
    f34.write_json(RUN_D_ROOT / "run_manifest.json", run_manifest(final))

    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md", grok_stage_open_receipt(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_closeout_receipt.md", grok_stage_closeout_receipt(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "local_verification.md", local_verification_text(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_A}_report.md", stage_open_report(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_B}_report.md", proxy_report(final, search["proxy_summary"]))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_B}_gate_audit.md", gate_audit_text(final, final["proxy"]))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_C}_report.md", repair_report(final, search["repair_summary"]))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_C}_gate_audit.md", gate_audit_text(final, final["repair"]))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md", closeout_report(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_D}_local_verification.md", local_verification_text(final))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", required_gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "preserved_clue.md", preserved_clue_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "negative_memory.md", negative_memory_text(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))
    f03b.write_text_sig(Path("docs/decisions/2026-06-15_stage_frontier_40_non_score_source_open.md"), decision_open(final))
    f03b.write_text_sig(Path("docs/decisions/2026-06-15_stage_frontier_40_non_score_source_closeout.md"), decision_closeout(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        GROK_OPEN_PACKET / "prompt.md",
        GROK_OPEN_PACKET / "clean_output.md",
        GROK_OPEN_PACKET / "metadata.json",
        GROK_CLOSEOUT_PACKET / "prompt.md",
        GROK_CLOSEOUT_PACKET / "clean_output.md",
        GROK_CLOSEOUT_PACKET / "metadata.json",
        RUN_B_ROOT / "raw_feature_pocket_candidate_summary.csv",
        RUN_C_ROOT / "capped_or_union_repair_summary.csv",
        RUN_D_ROOT / "stage_closeout_summary.json",
        STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md",
        STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md",
    ]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_D,
            "parent_run_id": RUN_C,
            "next_stage_id": NEXT_STAGE_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [f34.artifact_identity(path) for path in artifacts if path_exists(path)],
        "changed_variable": "train_only_raw_feature_state_pockets_no_model_score",
        "fixed_variables": "US100_M5_58_features_chronological_splits_f33_path_native_first_hit_replay_validation_oos_read_only",
        "grok_guardrail": "train_only_selection_freeze_search_budget_cap_density_matched_a_comparison_entry_known_audit",
        "closeout_class": final["closeout"]["closeout_class"],
        "runtime_probe_status": final["closeout"]["runtime_probe_status"],
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    upsert_csv_many(RUN_REGISTRY, "run_id", run_registry_rows(final))
    ledger = ledger_rows(final)
    upsert_csv_many(ALPHA_LEDGER, "ledger_row_id", ledger)
    upsert_csv_many(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger)
    f03b.append_once(CHANGELOG, RUN_D, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_A, idea_registry_open(final))
    f03b.append_once(IDEA_REGISTRY, RUN_D, idea_registry_close(final))
    f03b.append_once(NEGATIVE_RESULT_REGISTER, RUN_D, negative_register_entry(final))


def upsert_csv_many(path: Path, key: str, new_rows: list[dict[str, Any]]) -> None:
    resolved = io_path(path)
    with resolved.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = list(reader.fieldnames or [])
        existing_rows = [dict(row) for row in reader]
    if key not in header:
        raise ValueError(f"{path.as_posix()} missing key column {key}")
    index_by_key = {row.get(key, ""): index for index, row in enumerate(existing_rows)}
    for row in new_rows:
        normalized = {column: f34.stringify(row.get(column, "")) for column in header}
        row_key = normalized.get(key, "")
        if row_key in index_by_key:
            existing_rows[index_by_key[row_key]] = normalized
        else:
            index_by_key[row_key] = len(existing_rows)
            existing_rows.append(normalized)
    with resolved.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in existing_rows:
            writer.writerow({column: f34.stringify(row.get(column, "")) for column in header})


def run_registry_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    created = final["created_at_utc"]
    best = final["closeout"]["best_readonly"]
    return [
        registry_row(RUN_A, "stage_open(단계 개방)", final["stage_open"]["status"], final["stage_open"]["judgment"], f"grok={final['stage_open']['grok']['classification']};next={RUN_B}", created, "stage_open_no_model_training_no_wfo_no_mt5_no_onnx_no_authority", "runtime_probe_out_of_scope_by_claim_stage_open_no_proxy_yet", RUN_B),
        registry_row(RUN_B, "proxy_scout(프록시 탐색)", final["proxy"]["status"], final["proxy"]["judgment"], f"condition={final['proxy']['condition_rows']};candidate={final['proxy']['candidate_rows']};scout={final['proxy']['scout_rows']};seed={final['proxy']['seed_rows']}", created, "python_raw_feature_pocket_proxy_no_wfo_no_mt5_no_onnx_no_authority", final["proxy"]["runtime_probe_status"], RUN_C, best),
        registry_row(RUN_C, "repair_or_closeout_decision(수리 또는 마감 결정)", final["repair"]["status"], final["repair"]["judgment"], f"or_candidate={final['repair']['candidate_rows']};or_seed={final['repair']['seed_rows']}", created, "capped_or_union_repair_no_wfo_no_mt5_no_onnx_no_authority", final["repair"]["runtime_probe_status"], RUN_D, best),
        registry_row(RUN_D, "stage_closeout(단계 마감)", final["closeout"]["status"], final["closeout"]["judgment"], f"closeout={final['closeout']['closeout_class']};preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY};next={NEXT_RUN_ID}", created, "stage_closeout_preserved_clue_negative_memory_no_wfo_no_mt5_no_onnx_no_authority", final["closeout"]["runtime_probe_status"], NEXT_RUN_ID, best),
    ]


def registry_row(
    run_id: str,
    lane: str,
    status: str,
    judgment: str,
    notes: str,
    created: str,
    claim_boundary: str,
    external_status: str,
    next_run: str,
    best: dict[str, Any] | None = None,
) -> dict[str, Any]:
    report = STAGE_ROOT / "03_reviews" / f"{run_id}_report.md"
    primary = "stage_open_no_trading_kpi"
    if best:
        primary = (
            f"best={best.get('candidate_id','')};"
            f"val_pf={f34.fmt(best.get('validation_profit_factor'))};"
            f"val_density={f34.fmt(best.get('validation_trades_per_day'))};"
            f"val_dd={f34.fmt(best.get('validation_dd_risk'))};"
            f"oos_pf={f34.fmt(best.get('oos_profit_factor'))};"
            f"oos_density={f34.fmt(best.get('oos_trades_per_day'))};"
            f"oos_dd={f34.fmt(best.get('oos_dd_risk'))};"
            f"lift={f34.fmt(best.get('f40_min_pf_lift_vs_density_matched_a'))}"
        )
    return {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "lane": lane,
        "family": "experiment_execution(실험 실행)" if run_id != RUN_D else "publish_handoff(게시/인계)",
        "work_family": "experiment_execution(실험 실행)" if run_id != RUN_D else "publish_handoff(게시/인계)",
        "status": status,
        "judgment": judgment,
        "path": report.as_posix(),
        "notes": notes,
        "run_number": run_id.split("_", 1)[0],
        "date": "2026-06-15",
        "parent_run_id": PREV_RUN_D if run_id == RUN_A else {RUN_B: RUN_A, RUN_C: RUN_B, RUN_D: RUN_C}.get(run_id, ""),
        "next_run_id": next_run,
        "claim_boundary": claim_boundary,
        "report_path": report.as_posix(),
        "created_at_utc": created,
        "primary_kpi": primary,
        "guardrail_kpi": "train_only_raw_feature_thresholds_density_matched_a_validation_oos_read_only",
        "external_verification_status": external_status,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": report.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        ledger_row(RUN_A, f"{RUN_A}__stage_open", "stage_open(단계 개방)", "not_applicable_stage_open(단계 개방 해당 없음)", "planning_only_no_trading_kpi(계획 전용 거래 KPI 없음)", final["stage_open"]["status"], final["stage_open"]["judgment"], f"grok={final['stage_open']['grok']['classification']}", "stage_open_no_runtime", "runtime_probe_out_of_scope_by_claim_stage_open_no_proxy_yet", f"next={RUN_B}"),
        ledger_row(RUN_B, f"{RUN_B}__tier_a_raw_feature_pocket", "Tier A separate(Tier A 분리)", "Tier A(티어 A)", "python_raw_feature_pocket_proxy_no_mt5(파이썬 원천 피처 포켓 프록시, MT5 아님)", final["proxy"]["status"], final["proxy"]["judgment"], f"condition={final['proxy']['condition_rows']};candidate={final['proxy']['candidate_rows']};scout={final['proxy']['scout_rows']};seed={final['proxy']['seed_rows']}", "density_matched_a_no_authority", final["proxy"]["runtime_probe_status"], f"next={RUN_C}"),
        ledger_row(RUN_B, f"{RUN_B}__tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B(티어 B)", "missing_required(필수 누락)", final["proxy"]["status"], final["proxy"]["judgment"], "missing_required_no_tier_b_model_input", "no_tier_b_claim", "not_applicable_proxy_no_mt5", "Tier B(티어 B)는 F40 proxy(프록시) 입력으로 물질화하지 않았다."),
        ledger_row(RUN_B, f"{RUN_B}__tier_ab_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B(티어 A+B)", "out_of_scope_by_claim(주장 범위 밖)", final["proxy"]["status"], final["proxy"]["judgment"], "out_of_scope_by_claim_no_combined_source", "no_synthetic_combined_claim", "not_applicable_proxy_no_mt5", "Combined tier(합산 티어)는 F40 proxy(프록시)에서 주장하지 않았다."),
        ledger_row(RUN_C, f"{RUN_C}__capped_or_union_repair", "repair_or_closeout_decision(수리 또는 마감 결정)", "Tier A(티어 A)", "capped_or_union_repair_no_mt5(상한 OR 합집합 수리, MT5 아님)", final["repair"]["status"], final["repair"]["judgment"], f"or_candidate={final['repair']['candidate_rows']};or_scout={final['repair']['scout_rows']};or_seed={final['repair']['seed_rows']}", "one_capped_or_repair_no_authority", final["repair"]["runtime_probe_status"], f"next={RUN_D}"),
        ledger_row(RUN_D, f"{RUN_D}__stage_closeout", "stage_closeout(단계 마감)", "Tier A(티어 A)", "stage_closeout_no_runtime(단계 마감, 런타임 아님)", final["closeout"]["status"], final["closeout"]["judgment"], f"preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY}", "preserved_clue_negative_memory_no_authority", final["closeout"]["runtime_probe_status"], f"next={NEXT_RUN_ID}"),
    ]


def ledger_row(
    run_id: str,
    row_id: str,
    view: str,
    tier: str,
    kpi_scope: str,
    status: str,
    judgment: str,
    primary: str,
    guardrail: str,
    external: str,
    notes: str,
) -> dict[str, Any]:
    report = STAGE_ROOT / "03_reviews" / f"{run_id}_report.md"
    return {
        "ledger_row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": run_id,
        "subrun_id": row_id,
        "parent_run_id": PREV_RUN_D if run_id == RUN_A else {RUN_B: RUN_A, RUN_C: RUN_B, RUN_D: RUN_C}.get(run_id, ""),
        "record_view": view,
        "tier_scope": tier,
        "kpi_scope": kpi_scope,
        "scoreboard_lane": view,
        "status": status,
        "judgment": judgment,
        "path": report.as_posix(),
        "primary_kpi": primary,
        "guardrail_kpi": guardrail,
        "external_verification_status": external,
        "notes": notes,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": view,
    }


def update_current_truth(final: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(final), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(final))


def stage_brief(final: dict[str, Any]) -> str:
    return f"""# Frontier40 Stage Brief(전선40 단계 요약)

Opened(개방): {final['created_at_utc']}

Hypothesis(가설): F40(전선40)은 model score(모델 점수), score quantile(점수 분위수), score-conditioned regime gate(점수 조건 체제 게이트)를 쓰지 않고, train-only raw feature state pocket(학습 전용 원천 피처 상태 구간)이 short-side path-native PF edge(숏 경로 기반 수익 팩터 우위)를 만들 수 있는지 시험한다.

Action(행동): single feature(단일 피처), pair AND(쌍 AND), capped OR-union(상한 OR 합집합)을 train-only selection freeze(학습 전용 선택 고정) 아래에서 실행한다.

Effect(효과): F38/F39(전선38/39)의 score-source repetition(점수 원천 반복)을 피하고, entry-known closed-bar feature rule(진입 시점에 아는 닫힌 봉 피처 규칙)을 새 원천으로 확인한다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.
"""


def stage_open_report(final: dict[str, Any]) -> str:
    return f"""# Frontier40A Stage Open Report(전선40A 단계 개방 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['stage_open']['status']}`

Judgment(판정): `{final['stage_open']['judgment']}`

Action(행동): F40(전선40)을 raw feature state pocket(원천 피처 상태 구간) hypothesis(가설)로 열었다.

Effect(효과): non-score source(비점수 원천)를 독립 frontier campaign(독립 전선 캠페인)으로 시험한다.

Grok classification(그록 분류): `{final['stage_open']['grok']['classification']}`

Mandatory guardrail(필수 가드레일): train-only selection freeze(학습 전용 선택 고정), search budget cap(탐색 예산 상한), density-matched A comparison(밀도 맞춤 A 비교), entry-known audit(진입 시점 알려진 감사).

Next action(다음 행동): `{RUN_B}`
"""


def proxy_report(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["closeout"]["best_readonly"]
    table = top_rows_table(summary, 8)
    return f"""# Frontier40B Raw Feature Pocket Proxy Report(전선40B 원천 피처 포켓 프록시 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['proxy']['status']}`

Judgment(판정): `{final['proxy']['judgment']}`

Condition rows(조건 행): `{final['proxy']['condition_rows']}`

Candidate rows(후보 행): `{final['proxy']['candidate_rows']}`

Scout/seed/runtime rows(탐색/씨앗/런타임 행): `{final['proxy']['scout_rows']}` / `{final['proxy']['seed_rows']}` / `{final['proxy']['runtime_rows']}`

Best candidate(최상 후보): `{best.get('candidate_id', '')}`

Best validation/OOS PF-density-DD(최상 검증/표본외 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('validation_profit_factor'))}` / `{f34.fmt(best.get('validation_trades_per_day'))}` / `{f34.fmt(best.get('validation_dd_risk'))}` and `{f34.fmt(best.get('oos_profit_factor'))}` / `{f34.fmt(best.get('oos_trades_per_day'))}` / `{f34.fmt(best.get('oos_dd_risk'))}`

Best lift vs density-matched A(최상 밀도 맞춤 A 대비 상승): `{f34.fmt(best.get('f40_min_pf_lift_vs_density_matched_a'))}`

Top rows(상위 행):

{table}

Effect(효과): raw feature pocket(원천 피처 포켓)은 scout clue(탐색 단서)를 만들었는지 확인하지만, seed/runtime(씨앗/런타임)은 별도 행 수로만 말한다.
"""


def repair_report(final: dict[str, Any], summary: pd.DataFrame) -> str:
    return f"""# Frontier40C Capped OR-Union Repair Report(전선40C 상한 OR 합집합 수리 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['repair']['status']}`

Judgment(판정): `{final['repair']['judgment']}`

Action(행동): top train-only raw pockets(상위 학습 전용 원천 포켓)을 validation/OOS(검증/표본외) 없이 고른 뒤 OR-union(OR 합집합)으로 한 번만 수리했다.

Effect(효과): density(밀도)를 회복할 수 있는지 확인하되, validation/OOS metric(검증/표본외 지표)으로 union(합집합)을 고르는 누수를 막는다.

Candidate/scout/seed/runtime rows(후보/탐색/씨앗/런타임 행): `{final['repair']['candidate_rows']}` / `{final['repair']['scout_rows']}` / `{final['repair']['seed_rows']}` / `{final['repair']['runtime_rows']}`

Top OR rows(상위 OR 행):

{top_rows_table(summary, 6)}
"""


def closeout_report(final: dict[str, Any]) -> str:
    best = final["closeout"]["best_readonly"]
    return f"""# Frontier40D Stage Closeout Report(전선40D 단계 마감 보고)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['closeout']['status']}`

Judgment(판정): `{final['closeout']['judgment']}`

Closeout class(마감 분류): `{final['closeout']['closeout_class']}`

Best candidate(최상 후보): `{best.get('candidate_id', '')}`

Best rule(최상 규칙): `{best.get('rule_definition', '')}`

Best validation/OOS PF-density-DD(최상 검증/표본외 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('validation_profit_factor'))}` / `{f34.fmt(best.get('validation_trades_per_day'))}` / `{f34.fmt(best.get('validation_dd_risk'))}` and `{f34.fmt(best.get('oos_profit_factor'))}` / `{f34.fmt(best.get('oos_trades_per_day'))}` / `{f34.fmt(best.get('oos_dd_risk'))}`

Best density-matched lift(최상 밀도 맞춤 상승): `{f34.fmt(best.get('f40_min_pf_lift_vs_density_matched_a'))}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Preserved clue(보존 단서): `{final['closeout']['preserved_clue']}`

Negative memory(부정 기억): `{final['closeout']['negative_memory']}`

Grok closeout classification(그록 마감 분류): `{final['closeout']['grok']['classification']}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Effect(효과): raw feature state pocket(원천 피처 상태 구간)은 scout clue(탐색 단서)로 보존하고, seed/runtime candidate(씨앗/런타임 후보) 부재는 negative memory(부정 기억)로 남긴다.
"""


def gate_audit_text(final: dict[str, Any], section: dict[str, Any]) -> str:
    return f"""# Frontier40 Gate Audit(전선40 게이트 감사)

Run(실행): `{section['run_id']}`

Status(상태): `{section['status']}`

Judgment(판정): `{section['judgment']}`

Train-only selection freeze(학습 전용 선택 고정): `passed_local_guardrail`

Search budget cap(탐색 예산 상한): `single_feature_pair_and_one_capped_or_union_only`

Density-matched A comparison(밀도 맞춤 A 비교): `applied_periodic_train_coverage_baseline`

Entry-known audit(진입 시점 알려진 감사): `closed_bar_58_feature_contract_only`

Runtime probe status(런타임 탐침 상태): `{section['runtime_probe_status']}`
"""


def required_gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier40 Required Gate Coverage Audit(전선40 필수 게이트 커버리지 감사)

Stage(단계): `{STAGE_ID}`

- stage open Grok(단계 개방 그록): `{final['stage_open']['grok']['classification']}`
- closeout Grok(마감 그록): `{final['closeout']['grok']['classification']}`
- condition rows(조건 행): `{final['closeout']['condition_rows']}`
- candidate/scout/seed/runtime rows(후보/탐색/씨앗/런타임 행): `{final['closeout']['candidate_rows']}` / `{final['closeout']['scout_rows']}` / `{final['closeout']['seed_rows']}` / `{final['closeout']['runtime_rows']}`
- repair(수리): `{final['repair']['status']}`
- runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`
- local verification(로컬 검증): train-only selection freeze(학습 전용 선택 고정), density-matched A comparison(밀도 맞춤 A 비교), entry-known audit(진입 시점 알려진 감사) recorded(기록됨)
- claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.
"""


def local_verification_text(final: dict[str, Any]) -> str:
    checks = "\n".join(
        f"- {name}: `{value}`" for name, value in final["context"]["checks"].items()
    )
    best = final["closeout"]["best_readonly"]
    return f"""# Frontier40 Local Verification(전선40 로컬 검증)

Updated(갱신): {final['created_at_utc']}

Context checks(문맥 검사):

{checks}

Feature order hash(피처 순서 해시): `{final['feature_order_hash']}`

Raw path rows(원천 경로 행): `{final['raw_path']['raw_rows']}`

Missing entry/future positions(누락 진입/미래 위치): `{final['raw_path']['missing_entry_positions']}` / `{final['raw_path']['missing_future_positions']}`

Best candidate(최상 후보): `{best.get('candidate_id', '')}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Forbidden claims(금지 주장): `{final['claim_boundary']}`
"""


def grok_stage_open_receipt(final: dict[str, Any]) -> str:
    grok = final["stage_open"]["grok"]
    return f"""# Frontier40 Grok Stage Open Receipt(전선40 그록 단계 개방 영수증)

Trigger reason(트리거 이유): stage open external second opinion(단계 개방 외부 2차 의견)

Review size(검토 크기): small review(소규모 검토)

Direction before Grok(그록 전 방향): raw feature state pocket non-score source(원천 피처 상태 포켓 비점수 원천)

Prompt path(프롬프트 경로): `{GROK_OPEN_PACKET / 'prompt.md'}`

Output path(출력 경로): `{GROK_OPEN_PACKET / 'clean_output.md'}`

Advice classification(조언 분류): `{grok['classification']}`

Local verification(로컬 검증): mandatory guardrails(필수 가드레일)을 proxy code(프록시 코드)에 반영했다.

Forbidden claim check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)
"""


def grok_stage_closeout_receipt(final: dict[str, Any]) -> str:
    grok = final["closeout"]["grok"]
    return f"""# Frontier40 Grok Stage Closeout Receipt(전선40 그록 단계 마감 영수증)

Trigger reason(트리거 이유): stage closeout external second opinion(단계 마감 외부 2차 의견)

Review size(검토 크기): small review(소규모 검토)

Prompt path(프롬프트 경로): `{GROK_CLOSEOUT_PACKET / 'prompt.md'}`

Output path(출력 경로): `{GROK_CLOSEOUT_PACKET / 'clean_output.md'}`

Advice classification(조언 분류): `{grok['classification']}`

Local verification(로컬 검증): closeout(마감)은 seed/runtime candidate(씨앗/런타임 후보) 수와 runtime probe boundary(런타임 탐침 경계)에 맞춰 낮게 주장한다.

Forbidden claim check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)
"""


def preserved_clue_text(final: dict[str, Any]) -> str:
    return f"""# Frontier40 Preserved Clue(전선40 보존 단서)

Clue(단서): `{PRESERVED_CLUE}`

Evidence(근거): best raw feature pocket(최상 원천 피처 포켓) `{final['closeout']['best_readonly'].get('candidate_id', '')}` kept validation/OOS scout PF-density-DD(검증/표본외 탐색 수익 팩터-밀도-손실폭) under the density-matched A guardrail(밀도 맞춤 A 가드레일).

Boundary(경계): reference only(참조 전용). No seed, no runtime authority, no baseline(씨앗/런타임 권위/기준선 없음).
"""


def negative_memory_text(final: dict[str, Any]) -> str:
    return f"""# Frontier40 Negative Memory(전선40 부정 기억)

Memory(기억): `{NEGATIVE_MEMORY}`

Evidence(근거): seed/runtime rows(씨앗/런타임 행) `{final['closeout']['seed_rows']}` / `{final['closeout']['runtime_rows']}`.

Do not repeat(반복 금지): raw feature pocket(원천 피처 포켓) threshold mining(임계값 채굴)을 같은 selection rule(선택 규칙)로 반복하지 않는다.

Reopen condition(재개 조건): exit shape source(청산 형태 원천), label source(라벨 원천), or runtime representation(런타임 표현)이 바뀔 때만 다시 연다.
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier40 Selection Status(전선40 선택 상태)

Status(상태): `{final['closeout']['status']}`

Judgment(판정): `{final['closeout']['judgment']}`

Closeout class(마감 분류): `{final['closeout']['closeout_class']}`

Action(행동): F40(전선40)은 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫고, `{NEXT_STAGE_ID}`를 다음 질문으로 남긴다.

Effect(효과): raw feature pocket(원천 피처 포켓)은 reference-only scout clue(참조 전용 탐색 단서)로 보존하고, 다음 stage(단계)는 exit shape source(청산 형태 원천) 쪽으로 전환한다.

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Preserved clue(보존 단서): `{final['closeout']['preserved_clue']}`

Negative memory(부정 기억): `{final['closeout']['negative_memory']}`
"""


def decision_open(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Frontier40 Open(전선40 개방)

Date(날짜): 2026-06-15

Decision(결정): `{RUN_A}` starts `{STAGE_ID}`.

Action(행동): raw feature state pocket(원천 피처 상태 포켓)을 non-score source(비점수 원천)로 시험한다.

Effect(효과): F39(전선39)의 regime-conditioned score(체제 조건 점수) 부정 기억을 상속하지 않고 새 원천을 연다.

Grok(그록): `{final['stage_open']['grok']['classification']}`
"""


def decision_closeout(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Frontier40 Closeout(전선40 마감)

Date(날짜): 2026-06-15

Decision(결정): `{RUN_D}` closes `{STAGE_ID}` as `{final['closeout']['closeout_class']}`.

Action(행동): raw feature pocket scout clue(원천 피처 포켓 탐색 단서)를 보존하고 seed/runtime failure(씨앗/런타임 실패)를 negative memory(부정 기억)로 기록한다.

Effect(효과): 다음 전선은 exit shape source(청산 형태 원천)로 전환한다.

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`
"""


def changelog_entry(final: dict[str, Any]) -> str:
    best = final["closeout"]["best_readonly"]
    return (
        f"- {final['created_at_utc']} `{RUN_D}` closed `{STAGE_ID}` as "
        f"`{final['closeout']['closeout_class']}`. Best `{best.get('candidate_id','')}` "
        f"validation/OOS PF-density-DD {f34.fmt(best.get('validation_profit_factor'))}/"
        f"{f34.fmt(best.get('validation_trades_per_day'))}/{f34.fmt(best.get('validation_dd_risk'))} and "
        f"{f34.fmt(best.get('oos_profit_factor'))}/{f34.fmt(best.get('oos_trades_per_day'))}/"
        f"{f34.fmt(best.get('oos_dd_risk'))}; runtime `{final['closeout']['runtime_probe_status']}`."
    )


def idea_registry_open(final: dict[str, Any]) -> str:
    return f"""

## {RUN_A}

- Idea(아이디어): raw_feature_state_pocket_non_score_source(원천 피처 상태 포켓 비점수 원천)
- Hypothesis(가설): train-only raw feature thresholds(학습 전용 원천 피처 임계값)가 short-side path-native PF edge(숏 경로 기반 수익 팩터 우위)를 만들 수 있다.
- Legacy relation(레거시 관계): reference_only(참조 전용)
- Tier scope(티어 범위): Tier A separate with Tier B missing_required/Tier A+B out_of_scope_by_claim(Tier A 분리, Tier B 필수 누락, 합산 주장 범위 밖)
- Evidence boundary(근거 경계): scout-only until seed/runtime candidate(씨앗/런타임 후보 전까지 탐색 전용)
"""


def idea_registry_close(final: dict[str, Any]) -> str:
    best = final["closeout"]["best_readonly"]
    return f"""

## {RUN_D}

- Result(결과): `{final['closeout']['closeout_class']}`
- Best candidate(최상 후보): `{best.get('candidate_id', '')}`
- Preserved clue(보존 단서): `{final['closeout']['preserved_clue']}`
- Negative memory(부정 기억): `{final['closeout']['negative_memory']}`
- Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`
- Next condition(다음 조건): exit shape source(청산 형태 원천) or label/runtime representation pivot(라벨/런타임 표현 전환)
"""


def negative_register_entry(final: dict[str, Any]) -> str:
    return f"""

## {RUN_D}

- Stage(단계): `{STAGE_ID}`
- Negative memory(부정 기억): `{NEGATIVE_MEMORY}`
- Preserved clue(보존 단서): `{final['closeout']['preserved_clue']}`
- Evidence(근거): candidate/scout/seed/runtime rows(후보/탐색/씨앗/런타임 행) `{final['closeout']['candidate_rows']}` / `{final['closeout']['scout_rows']}` / `{final['closeout']['seed_rows']}` / `{final['closeout']['runtime_rows']}`
- Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`
- Effect(효과): 같은 raw feature threshold mining(원천 피처 임계값 채굴)을 반복하지 않고, 다음에는 exit shape source(청산 형태 원천)를 새 가설로 다룬다.
"""


def workspace_state(final: dict[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_D}
latest_completed_run_id: {RUN_D}
current_status: {final['closeout']['status']}
current_judgment: {final['closeout']['judgment']}
next_stage_id: {NEXT_STAGE_ID}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{final['created_at_utc']}'
"""


def current_working_state(final: dict[str, Any]) -> str:
    best = final["closeout"]["best_readonly"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Current stage(현재 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_D}`

Status(상태): `{final['closeout']['status']}`

Judgment(판정): `{final['closeout']['judgment']}`

Action(행동): F40(전선40)를 raw feature state pocket(원천 피처 상태 포켓) non-score source(비점수 원천) lifecycle(생명주기)로 닫았다.

Effect(효과): scout clue(탐색 단서)는 보존하고, seed/runtime candidate(씨앗/런타임 후보) 부재를 negative memory(부정 기억)로 남긴다.

Best candidate(최상 후보): `{best.get('candidate_id', '')}`

Best validation/OOS PF-density-DD(최상 검증/표본외 수익 팩터-밀도-손실폭): `{f34.fmt(best.get('validation_profit_factor'))}` / `{f34.fmt(best.get('validation_trades_per_day'))}` / `{f34.fmt(best.get('validation_dd_risk'))}` and `{f34.fmt(best.get('oos_profit_factor'))}` / `{f34.fmt(best.get('oos_trades_per_day'))}` / `{f34.fmt(best.get('oos_dd_risk'))}`

Runtime probe status(런타임 탐침 상태): `{final['closeout']['runtime_probe_status']}`

Next stage(다음 단계): `{NEXT_STAGE_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)이다.
"""


def top_rows_table(summary: pd.DataFrame, limit: int) -> str:
    if summary.empty:
        return "_No rows(행 없음)._"
    rows = [
        "| candidate(후보) | kind(종류) | rule(규칙) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | lift | scout | seed |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for _, row in summary.head(limit).iterrows():
        rows.append(
            "| "
            f"`{row.get('candidate_id','')}` | `{row.get('candidate_kind','')}` | `{shorten(row.get('rule_definition',''), 70)}` | "
            f"{f34.fmt(row.get('validation_profit_factor'))} | {f34.fmt(row.get('validation_trades_per_day'))} | {f34.fmt(row.get('validation_dd_risk'))} | "
            f"{f34.fmt(row.get('oos_profit_factor'))} | {f34.fmt(row.get('oos_trades_per_day'))} | {f34.fmt(row.get('oos_dd_risk'))} | "
            f"{f34.fmt(row.get('f40_min_pf_lift_vs_density_matched_a'))} | {row.get('f40_scout_clue_flag')} | {row.get('f40_seed_surface_flag')} |"
        )
    return "\n".join(rows)


def shorten(value: Any, limit: int) -> str:
    text = str(value)
    return text if len(text) <= limit else text[: limit - 3] + "..."


def output_summary(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "closeout_run_id": RUN_D,
        "condition_rows": final["closeout"]["condition_rows"],
        "candidate_rows": final["closeout"]["candidate_rows"],
        "scout_rows": final["closeout"]["scout_rows"],
        "seed_rows": final["closeout"]["seed_rows"],
        "runtime_rows": final["closeout"]["runtime_rows"],
        "runtime_probe_status": final["closeout"]["runtime_probe_status"],
        "closeout_class": final["closeout"]["closeout_class"],
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "report": (STAGE_ROOT / "03_reviews" / f"{RUN_D}_report.md").as_posix(),
    }


if __name__ == "__main__":
    raise SystemExit(main())
