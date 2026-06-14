from __future__ import annotations

import csv
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
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_22__session_return_shock_pf_source_onnx_scout"
RUN_ID = "frontier22B_session_return_shock_pf_source_proxy_scout_v1"
RUN_NUMBER = "frontier22B"
PARENT_RUN_ID = "frontier22A_stage_open_new_pf_edge_source_hypothesis_design_v1"
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier22C_grok_pre_expensive_shock_pf_source_review_v1"
NEXT_REPAIR_OR_CLOSEOUT_RUN_ID = "frontier22C_shock_pf_source_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_22/frontier22b_session_return_shock_pf_source_proxy_scout.py")

F22A_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "stage_open_summary.json"
F22A_LOCK = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "shock_pf_source_lock.json"
DATASET_PATH = Path(
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = DATASET_PATH.with_name("model_input_feature_order.txt")
EXPECTED_FEATURE_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

LOW_QUANTILES = (0.20, 0.30)
HIGH_QUANTILES = (0.70, 0.80)
FAMILY_CONDITION_CAP = 8
MAX_CANDIDATES = 200
MIN_TRAIN_DENSITY = 2.0
MAX_TRAIN_DENSITY = 18.0
MIN_TRAIN_TRADES = 60
MIN_TRAIN_PF = 1.05
SCOUT_MIN_PF = 1.05
SCOUT_DENSITY_LOW = 3.0
SCOUT_DENSITY_HIGH = 12.0
SCOUT_DD_CAP = 35.0
SEED_PF = 1.20
SEED_DD_CAP = 25.0
HANDOFF_PF = 1.50
HANDOFF_DD_CAP = 15.0


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F22A_SUMMARY)
    lock = read_json(F22A_LOCK)
    frame = load_frame()
    feature_order = read_feature_order()
    context = validate_context(stage_open, lock, frame, feature_order)
    condition_pool = build_condition_pool(frame, lock["buckets"])
    candidate_pool = build_candidate_pool(frame, condition_pool)
    selected = select_candidates(frame, candidate_pool)
    metrics = evaluate_selected(frame, selected)
    summary = summarize_candidates(metrics)
    final = build_final(created_at, stage_open, lock, feature_order, context, condition_pool, candidate_pool, selected, metrics, summary)
    write_outputs(final, condition_pool, selected, metrics, summary)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "condition_pool_rows": final["condition_pool_rows"],
        "candidate_pool_rows": final["candidate_pool_rows"],
        "selected_candidate_rows": final["selected_candidate_rows"],
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "best_candidate_id": final["best_candidate_id"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_context(stage_open: dict[str, Any], lock: dict[str, Any], frame: pd.DataFrame, feature_order: list[str]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    bucket_features = {feature for features in lock["buckets"].values() for feature in features}
    checks = {
        "workspace_current_stage_frontier22": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier22b": f"next_run_id: {RUN_ID}" in workspace,
        "stage_open_run_matches_parent": stage_open.get("run_id") == PARENT_RUN_ID,
        "mandatory_rule_shape_locked": "mandatory_rule_shape" in lock.get("locks", {}),
        "feature_order_hash_matches_contract": ordered_hash(feature_order) == EXPECTED_FEATURE_HASH,
        "feature_count_is_58": len(feature_order) == 58,
        "bucket_features_exist": bucket_features.issubset(set(frame.columns)),
        "dataset_exists": path_exists(DATASET_PATH),
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier22B context check failed: {json.dumps(checks, ensure_ascii=False)}")
    return {"checks": checks}


def load_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(DATASET_PATH)).sort_values("timestamp").reset_index(drop=True)
    required = {"timestamp", "split", "future_log_return_12", "label_class"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns(필수 열 누락): {missing}")
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    if frame["timestamp"].isna().any():
        raise ValueError("Timestamp contains NaT(타임스탬프 결측).")
    if frame["timestamp"].duplicated().any():
        raise ValueError("Timestamp contains duplicates(타임스탬프 중복).")
    if set(frame["split"].astype(str).unique()) != {"train", "validation", "oos"}:
        raise ValueError("Split must be train/validation/oos(분할은 학습/검증/표본외만 허용).")
    return frame


def read_feature_order() -> list[str]:
    features = [line.strip() for line in io_path(FEATURE_ORDER_PATH).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if len(features) != 58 or ordered_hash(features) != EXPECTED_FEATURE_HASH:
        raise ValueError("Feature order contract mismatch(피처 순서 계약 불일치).")
    return features


def build_condition_pool(frame: pd.DataFrame, buckets: dict[str, list[str]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for family, features in buckets.items():
        family_rows: list[dict[str, Any]] = []
        for feature in features:
            family_rows.extend(build_feature_conditions(frame, family, feature))
        family_rows.sort(key=lambda row: float(row["condition_rank_score"]), reverse=True)
        rows.extend(family_rows[:FAMILY_CONDITION_CAP])
    if not rows:
        raise RuntimeError("No condition pool rows(조건 풀 행 없음).")
    for index, row in enumerate(rows, start=1):
        row["condition_id"] = f"f22cond_{index:03d}"
    return pd.DataFrame(rows)


def build_feature_conditions(frame: pd.DataFrame, family: str, feature: str) -> list[dict[str, Any]]:
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool)
    series = pd.to_numeric(frame[feature], errors="coerce")
    values = series.to_numpy(dtype="float64")
    train_values = series.loc[train_mask]
    if train_values.nunique(dropna=True) <= 1:
        return []

    specs: list[tuple[str, float | None, str | None]] = []
    if train_values.nunique(dropna=True) <= 3:
        specs = [(">=", 0.5, None), ("<", 0.5, None)]
    else:
        specs.extend(("<=", q, "negative") for q in LOW_QUANTILES)
        specs.extend((">=", q, "positive") for q in HIGH_QUANTILES)

    rows: list[dict[str, Any]] = []
    for operator, quantile_or_threshold, polarity_hint in specs:
        if quantile_or_threshold is None:
            continue
        threshold = float(quantile_or_threshold if train_values.nunique(dropna=True) <= 3 else np.nanquantile(train_values, quantile_or_threshold))
        finite = np.isfinite(values)
        if operator == "<":
            mask = (values < threshold) & finite
            q_label = "lt0p5"
        elif operator == "<=":
            mask = (values <= threshold) & finite
            q_label = f"q{int(float(quantile_or_threshold) * 100)}"
        else:
            mask = (values >= threshold) & finite
            q_label = "ge0p5" if train_values.nunique(dropna=True) <= 3 else f"q{int(float(quantile_or_threshold) * 100)}"
        coverage = float(mask[train_mask].mean()) if train_mask.any() else 0.0
        if not (0.03 <= coverage <= 0.85):
            continue
        polarity = polarity_hint or ("positive" if operator == ">=" else "negative")
        score = single_condition_score(frame, mask)
        rows.append({
            "condition_id": "",
            "family": family,
            "feature": feature,
            "operator": operator,
            "quantile_label": q_label,
            "threshold_value": threshold,
            "polarity": polarity if family == "shock" else "context",
            "train_coverage": coverage,
            "condition_rank_score": score,
            "definition": f"{feature} {operator} {q_label}",
            "_mask": mask,
        })
    return rows


def single_condition_score(frame: pd.DataFrame, mask: np.ndarray) -> float:
    long_metrics = evaluate_mask(frame, mask, 1, "train")
    short_metrics = evaluate_mask(frame, mask, -1, "train")
    best = long_metrics if long_metrics["net_profit"] >= short_metrics["net_profit"] else short_metrics
    coverage_penalty = abs(best["trades_per_day"] - 8.0) / 8.0
    return float(best["net_profit"]) * min(float(best["profit_factor"]), 3.0) / (1.0 + best["dd_risk"] / 20.0 + coverage_penalty)


def build_candidate_pool(frame: pd.DataFrame, condition_pool: pd.DataFrame) -> list[dict[str, Any]]:
    shock_rows = condition_pool.loc[condition_pool["family"].eq("shock")].to_dict("records")
    context_rows = condition_pool.loc[~condition_pool["family"].eq("shock")].to_dict("records")
    candidates: list[dict[str, Any]] = []
    for shock in shock_rows:
        for context in context_rows:
            if shock["feature"] == context["feature"]:
                continue
            mask = np.asarray(shock["_mask"], dtype=bool) & np.asarray(context["_mask"], dtype=bool)
            for lane in ("shock_continuation", "shock_fade"):
                side = side_for_lane(str(shock["polarity"]), lane)
                metrics = evaluate_mask(frame, mask, side, "train")
                candidates.append({
                    "candidate_id": f"f22b_{len(candidates)+1:04d}",
                    "lane": lane,
                    "side": side,
                    "side_name": "long(롱)" if side > 0 else "short(숏)",
                    "shock_condition_id": shock["condition_id"],
                    "context_condition_id": context["condition_id"],
                    "shock_feature": shock["feature"],
                    "context_feature": context["feature"],
                    "context_family": context["family"],
                    "shock_polarity": shock["polarity"],
                    "rule_definition": f"{shock['definition']} & {context['definition']} [{lane}]",
                    "mask": mask,
                    "train_rank_score": train_rank_score(metrics),
                    "train_selection_metrics": metrics,
                    "f20_duplicate_pressure": is_f20_duplicate(shock["feature"], context["feature"]),
                })
    if not candidates:
        raise RuntimeError("No candidate pool rows(후보 풀 행 없음).")
    return candidates


def side_for_lane(polarity: str, lane: str) -> int:
    positive = polarity == "positive"
    if lane == "shock_continuation":
        return 1 if positive else -1
    return -1 if positive else 1


def is_f20_duplicate(shock_feature: str, context_feature: str) -> bool:
    return {shock_feature, context_feature} == {"vix_zscore_20", "close_ema50_ratio"}


def select_candidates(frame: pd.DataFrame, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = [
        item for item in candidates
        if MIN_TRAIN_DENSITY <= item["train_selection_metrics"]["trades_per_day"] <= MAX_TRAIN_DENSITY
        and item["train_selection_metrics"]["trade_count"] >= MIN_TRAIN_TRADES
        and item["train_selection_metrics"]["net_profit"] > 0
        and item["train_selection_metrics"]["profit_factor"] >= MIN_TRAIN_PF
    ]
    selected.sort(key=lambda item: float(item["train_rank_score"]), reverse=True)
    if not selected:
        selected = sorted(candidates, key=lambda item: float(item["train_rank_score"]), reverse=True)[: min(MAX_CANDIDATES, len(candidates))]
    return selected[:MAX_CANDIDATES]


def evaluate_selected(frame: pd.DataFrame, selected: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for rank, candidate in enumerate(selected, start=1):
        for split in ("train", "validation", "oos"):
            metrics = evaluate_mask(frame, candidate["mask"], int(candidate["side"]), split)
            sparse_floor = max(20, int(math.ceil(metrics["days_in_scope"] * 0.5)))
            sparse_flag = metrics["trade_count"] < sparse_floor
            pf999_sparse_flag = bool(metrics["profit_factor"] >= 999.0 and sparse_flag)
            density_distance = scout.density_axis_distance(metrics["trades_per_day"])
            pf_distance = scout.profit_factor_axis_distance(metrics["profit_factor"], metrics["trade_count"], sparse_flag, pf999_sparse_flag)
            dd_distance = max(0.0, (metrics["dd_risk"] - scout.DD_TARGET_PERCENT) / scout.DD_TARGET_PERCENT)
            smoothness_distance = scout.smoothness_axis_distance(metrics)
            rows.append({
                "candidate_id": candidate["candidate_id"],
                "train_rank": rank,
                "lane": candidate["lane"],
                "side": candidate["side_name"],
                "side_value": candidate["side"],
                "rule_definition": candidate["rule_definition"],
                "shock_condition_id": candidate["shock_condition_id"],
                "context_condition_id": candidate["context_condition_id"],
                "shock_feature": candidate["shock_feature"],
                "context_feature": candidate["context_feature"],
                "context_family": candidate["context_family"],
                "shock_polarity": candidate["shock_polarity"],
                "f20_duplicate_pressure": candidate["f20_duplicate_pressure"],
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
                "max_drawdown_percent": metrics["max_drawdown_percent"],
                "max_monthly_drawdown_percent": metrics["max_monthly_drawdown_percent"],
                "dd_risk": metrics["dd_risk"],
                "underwater_ratio": metrics["underwater_ratio"],
                "max_loss_streak": metrics["max_loss_streak"],
                "equity_trend_r2": metrics["equity_trend_r2"],
                "sparse_flag": sparse_flag,
                "pf999_sparse_flag": pf999_sparse_flag,
                "density_axis_distance": density_distance,
                "pf_axis_distance": pf_distance,
                "dd_axis_distance": dd_distance,
                "smoothness_axis_distance": smoothness_distance,
                "joint_axis_distance": density_distance + pf_distance + dd_distance + smoothness_distance,
                "density_pass": bool(scout.DENSITY_TARGET_LOW <= metrics["trades_per_day"] <= scout.DENSITY_TARGET_HIGH),
                "pf_pass": bool(metrics["profit_factor"] >= scout.PF_TARGET and metrics["net_profit"] > 0 and not sparse_flag),
                "dd_pass": bool(metrics["dd_risk"] < scout.DD_TARGET_PERCENT),
                "smoothness_pass": bool(
                    metrics["net_profit"] > 0
                    and metrics["underwater_ratio"] <= 0.45
                    and metrics["equity_trend_r2"] >= 0.35
                    and metrics["max_loss_streak"] <= 6
                ),
                "selection_boundary": "train_only_rank(학습 전용 순위)" if split == "train" else "read_only_forward_diagnostic(읽기 전용 전진 진단)",
                "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
            })
    if not rows:
        raise RuntimeError("No selected candidate metrics(선택 후보 지표 없음).")
    return pd.DataFrame(rows)


def evaluate_mask(frame: pd.DataFrame, mask: np.ndarray, side: int, split: str) -> dict[str, Any]:
    split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
    trade_mask = np.asarray(mask, dtype=bool) & split_mask
    split_times = frame.loc[split_mask, "timestamp"]
    days = scout.count_scope_days(split_times)
    returns = pd.to_numeric(frame.loc[trade_mask, "future_log_return_12"], errors="coerce").to_numpy(dtype="float64")
    pnl = returns * float(side) - scout.ROUGH_COST_LOG_RETURN
    trade_times = frame.loc[trade_mask, "timestamp"]
    metrics = scout.trade_metrics(pnl, trade_times)
    trade_count = int(len(pnl))
    return {
        **metrics,
        "trade_count": trade_count,
        "days_in_scope": days,
        "trades_per_day": float(trade_count / days) if days else 0.0,
        "dd_risk": max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"])),
    }


def train_rank_score(metrics: dict[str, Any]) -> float:
    density_penalty = abs(float(metrics["trades_per_day"]) - 8.0) / 8.0
    dd_penalty = max(0.0, float(metrics["dd_risk"]) - 12.0) / 18.0
    return float(metrics["net_profit"]) * min(float(metrics["profit_factor"]), 4.0) / (1.0 + density_penalty + dd_penalty)


def summarize_candidates(metrics: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for candidate_id, group in metrics.groupby("candidate_id", sort=False):
        train = split_row(group, "train")
        validation = split_row(group, "validation")
        oos = split_row(group, "oos")
        base = {
            "candidate_id": candidate_id,
            "train_rank": int(train["train_rank"]),
            "lane": train["lane"],
            "side": train["side"],
            "rule_definition": train["rule_definition"],
            "shock_feature": train["shock_feature"],
            "context_feature": train["context_feature"],
            "context_family": train["context_family"],
            "shock_polarity": train["shock_polarity"],
            "f20_duplicate_pressure": bool(train["f20_duplicate_pressure"]),
        }
        for prefix, row in (("train", train), ("validation", validation), ("oos", oos)):
            for field in (
                "trade_count",
                "trades_per_day",
                "net_profit",
                "profit_factor",
                "expectancy",
                "win_rate",
                "dd_risk",
                "underwater_ratio",
                "max_loss_streak",
                "equity_trend_r2",
                "joint_axis_distance",
                "density_pass",
                "pf_pass",
                "dd_pass",
                "smoothness_pass",
            ):
                base[f"{prefix}_{field}"] = row[field]
        base["scout_clue_flag"] = bool(
            not base["f20_duplicate_pressure"]
            and validation["net_profit"] > 0
            and oos["net_profit"] > 0
            and validation["profit_factor"] >= SCOUT_MIN_PF
            and oos["profit_factor"] >= SCOUT_MIN_PF
            and SCOUT_DENSITY_LOW <= validation["trades_per_day"] <= SCOUT_DENSITY_HIGH
            and SCOUT_DENSITY_LOW <= oos["trades_per_day"] <= SCOUT_DENSITY_HIGH
            and max(validation["dd_risk"], oos["dd_risk"]) <= SCOUT_DD_CAP
        )
        base["seed_surface_flag"] = bool(
            not base["f20_duplicate_pressure"]
            and validation["net_profit"] > 0
            and oos["net_profit"] > 0
            and validation["profit_factor"] >= SEED_PF
            and oos["profit_factor"] >= SEED_PF
            and scout.DENSITY_TARGET_LOW <= validation["trades_per_day"] <= scout.DENSITY_TARGET_HIGH
            and scout.DENSITY_TARGET_LOW <= oos["trades_per_day"] <= scout.DENSITY_TARGET_HIGH
            and max(validation["dd_risk"], oos["dd_risk"]) <= SEED_DD_CAP
        )
        base["handoff_candidate_flag"] = bool(
            base["seed_surface_flag"]
            and validation["profit_factor"] >= HANDOFF_PF
            and oos["profit_factor"] >= HANDOFF_PF
            and max(validation["dd_risk"], oos["dd_risk"]) <= HANDOFF_DD_CAP
            and validation["smoothness_pass"]
            and oos["smoothness_pass"]
        )
        base["forward_read_score"] = float(
            min(validation["profit_factor"], 3.0)
            * min(oos["profit_factor"], 3.0)
            * min(validation["trades_per_day"], oos["trades_per_day"], 12.0)
            / (1.0 + max(validation["dd_risk"], oos["dd_risk"]) / 18.0)
        )
        rows.append(base)
    return pd.DataFrame(rows).sort_values(
        ["handoff_candidate_flag", "seed_surface_flag", "scout_clue_flag", "forward_read_score"],
        ascending=[False, False, False, False],
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
    feature_order: list[str],
    context: dict[str, Any],
    condition_pool: pd.DataFrame,
    candidate_pool: list[dict[str, Any]],
    selected: list[dict[str, Any]],
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
) -> dict[str, Any]:
    scout_count = int(summary["scout_clue_flag"].sum()) if "scout_clue_flag" in summary else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if "seed_surface_flag" in summary else 0
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if "handoff_candidate_flag" in summary else 0
    duplicate_count = int(summary["f20_duplicate_pressure"].sum()) if "f20_duplicate_pressure" in summary else 0
    if handoff_count:
        status = "shock_pf_source_handoff_candidate_proxy_no_authority"
        judgment = "handoff_candidate_requires_grok_pre_expensive_review_no_authority"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
    elif seed_count:
        status = "shock_pf_source_seed_surface_proxy_no_runtime_no_authority"
        judgment = "seed_surface_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    elif scout_count:
        status = "shock_pf_source_scout_clue_proxy_no_runtime_no_authority"
        judgment = "scout_clue_requires_repair_or_closeout_no_authority"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    else:
        status = "shock_pf_source_no_forward_clue_proxy_no_authority"
        judgment = "negative_pressure_needs_repair_or_closeout(부정 압력, 수리 또는 마감 필요)"
        next_run_id = NEXT_REPAIR_OR_CLOSEOUT_RUN_ID
    best = dict(summary.iloc[0]) if len(summary) else {}
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "stage_open_run": stage_open.get("run_id"),
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "context": context,
        "lock": lock,
        "condition_pool_rows": int(len(condition_pool)),
        "candidate_pool_rows": int(len(candidate_pool)),
        "selected_candidate_rows": int(len(selected)),
        "metric_rows": int(len(metrics)),
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "f20_duplicate_pressure_rows": duplicate_count,
        "best_candidate_id": best.get("candidate_id", ""),
        "best_candidate": json_ready(best),
        "result_boundary": "proxy_only_no_wfo_no_mt5_no_runtime_authority(프록시 전용, WFO/MT5/런타임 권위 없음)",
        "runtime_probe_status": "pre_expensive_grok_required_before_mt5(비싼 MT5 전 그록 검토 필요)" if handoff_count else "out_of_scope_by_claim_no_handoff_candidate_yet(인계 후보 전이라 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], condition_pool: pd.DataFrame, selected: list[dict[str, Any]], metrics: pd.DataFrame, summary: pd.DataFrame) -> None:
    condition_output = condition_pool.drop(columns=["_mask"], errors="ignore")
    candidate_rows = [
        {
            "candidate_id": item["candidate_id"],
            "lane": item["lane"],
            "side": item["side_name"],
            "rule_definition": item["rule_definition"],
            "shock_feature": item["shock_feature"],
            "context_feature": item["context_feature"],
            "context_family": item["context_family"],
            "shock_polarity": item["shock_polarity"],
            "train_rank_score": item["train_rank_score"],
            "f20_duplicate_pressure": item["f20_duplicate_pressure"],
            **{f"train_{key}": value for key, value in item["train_selection_metrics"].items()},
        }
        for item in selected
    ]
    condition_output.to_csv(io_path(RUN_ROOT / "condition_pool.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame(candidate_rows).to_csv(io_path(RUN_ROOT / "train_ranked_candidates.csv"), index=False, encoding="utf-8-sig")
    metrics.to_csv(io_path(RUN_ROOT / "proxy_metrics_by_split.csv"), index=False, encoding="utf-8-sig")
    summary.to_csv(io_path(RUN_ROOT / "candidate_summary.csv"), index=False, encoding="utf-8-sig")
    summary.sort_values("forward_read_score", ascending=False).head(30).to_csv(io_path(RUN_ROOT / "top_forward_readonly_diagnostic.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final, summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md", gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F22A_SUMMARY,
        F22A_LOCK,
        DATASET_PATH,
        FEATURE_ORDER_PATH,
        RUN_ROOT / "condition_pool.csv",
        RUN_ROOT / "train_ranked_candidates.csv",
        RUN_ROOT / "proxy_metrics_by_split.csv",
        RUN_ROOT / "candidate_summary.csv",
        RUN_ROOT / "top_forward_readonly_diagnostic.csv",
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
            "feature_count": final["feature_count"],
            "feature_order_hash": final["feature_order_hash"],
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
        },
        "data_snapshot": {
            "dataset_path": DATASET_PATH.as_posix(),
            "split_names": ["train", "validation", "oos"],
        },
        "runtime_snapshot": {
            "symbol": "US100",
            "timeframe": "M5",
            "entry_timing": "closed_bar_signal_horizon_proxy(종료봉 신호 예측수평선 프록시)",
            "cost_behavior": "rough_log_return_cost_proxy_only(거친 로그수익 비용 프록시 전용)",
        },
        "rule_stack": {
            "entry": "shock_plus_one_context_condition(충격 조건과 문맥 조건 1개)",
            "exit": "future_log_return_12_proxy(12봉 미래 수익률 프록시)",
            "side": "locked_shock_continuation_or_fade(고정 충격 지속 또는 되돌림)",
        },
        "results": {
            "by_split": {"metrics_path": (RUN_ROOT / "proxy_metrics_by_split.csv").as_posix()},
            "cross_split": {
                "scout_clue_rows": final["scout_clue_rows"],
                "seed_surface_rows": final["seed_surface_rows"],
                "handoff_candidate_rows": final["handoff_candidate_rows"],
                "best_candidate_id": final["best_candidate_id"],
            },
            "report_refs": [{"role": "proxy_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {
            "schema_version": "frontier22b_proxy_v1",
            "mismatch_policy": "fail_fast(빠른 실패)",
            "required_output_schema": "not_applicable_no_onnx_export_yet(ONNX 내보내기 전이라 해당 없음)",
        },
        "claim_boundary": final["claim_boundary"],
    }


def report_text(final: dict[str, Any], summary: pd.DataFrame) -> str:
    best = final["best_candidate"]
    top_rows = []
    for _, row in summary.head(12).iterrows():
        top_rows.append(
            f"| `{row['candidate_id']}` | {row['lane']} | {row['side']} | `{row['shock_feature']}+{row['context_feature']}` | "
            f"{fmt(row['validation_profit_factor'])} | {fmt(row['validation_trades_per_day'])} | {fmt(row['validation_dd_risk'])} | "
            f"{fmt(row['oos_profit_factor'])} | {fmt(row['oos_trades_per_day'])} | {fmt(row['oos_dd_risk'])} | {row['scout_clue_flag']} | {row['seed_surface_flag']} |"
        )
    table = "\n".join(top_rows)
    return f"""# Frontier22B Session Return Shock PF Source Proxy Scout Report(전선22B 세션 수익률 충격 수익 팩터 원천 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): shock condition(충격 조건) 1개와 context condition(문맥 조건) 1개를 결합한 후보를 train-only rank(학습 전용 순위)로 고르고, validation/OOS(검증/표본외)는 read-only diagnostic(읽기 전용 진단)으로만 봤습니다.

Effect(효과): F20 전체 규칙 지도 재탐색을 막고, PF edge(수익 팩터 우위)가 shock-anchored entry state(충격 고정 진입 상태)에서 나오는지 분리했습니다.

Condition/candidate/selected rows(조건/후보/선택 행): `{final['condition_pool_rows']}` / `{final['candidate_pool_rows']}` / `{final['selected_candidate_rows']}`

Scout/seed/handoff rows(탐색/씨앗/인계 행): `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

F20 duplicate pressure rows(F20 중복 압력 행): `{final['f20_duplicate_pressure_rows']}`

Best candidate(최상 후보): `{final['best_candidate_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk'))}%`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

## Top Readonly Forward Rows(상위 읽기 전용 전진 행)

| candidate(후보) | lane(방향) | side(방향) | features(피처) | val PF | val density | val DD | OOS PF | OOS density | OOS DD | scout | seed |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{table}

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier22B Gate Audit(전선22B 게이트 감사)

- scope_completion_gate(범위 완료 게이트): proxy artifacts created(프록시 산출물 생성) `{(RUN_ROOT / 'final_summary.json').as_posix()}`
- kpi_contract_audit(KPI 계약 감사): metrics/candidate/condition outputs(지표/후보/조건 출력) created(생성)
- shock_contract_gate(충격 계약 게이트): candidates require shock+context(후보는 충격+문맥 필수)
- f20_duplicate_guard(F20 중복 가드): duplicate rows(중복 행) `{final['f20_duplicate_pressure_rows']}`
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일)
- final_claim_guard(최종 주장 방지): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier22 Selection Status(전선22 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest proxy(최근 프록시): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best candidate(최상 후보): `{final['best_candidate_id']}`

Scout/seed/handoff rows(탐색/씨앗/인계 행): `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

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
    best = final["best_candidate"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "shock_pf_source_proxy_scout(충격 수익 팩터 원천 프록시 탐색)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};best={final['best_candidate_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"best={final['best_candidate_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "shock_required_train_only_selection_validation_oos_read_only_no_authority(충격 필수, 학습 전용 선택, 검증/표본외 읽기 전용, 권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_candidate"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_shock_pf_source_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_shock_pf_source_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "shock_pf_source_proxy_not_runtime(충격 수익 팩터 원천 프록시, 런타임 아님)",
        "scoreboard_lane": "trade_shape_proxy(거래 형태 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"best={final['best_candidate_id']};oos_pf={fmt(best.get('oos_profit_factor'))};oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk'))}",
        "guardrail_kpi": "proxy_only_no_wfo_no_mt5_no_authority(프록시 전용, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']}",
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
        "notes": "Tier B model input not available in this dataset(Tier B 모델 입력이 이 데이터셋에 없음)",
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
        "notes": "Combined record blocked by missing Tier B source(Tier B 원천 누락으로 합산 기록 차단)",
    }
    return [primary, tier_b, combined]


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran shock PF source proxy scout(충격 수익 팩터 원천 프록시 탐색). "
        f"Effect(효과): scout/seed/handoff(탐색/씨앗/인계) counts are {final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']} and next run(다음 실행) is `{final['next_run_id']}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR22-SESSION-RETURN-SHOCK-PF-SOURCE-ONNX-SCOUT`: `{RUN_ID}` tested shock+context entry states(충격+문맥 진입 상태). "
        f"Effect(효과): best candidate `{final['best_candidate_id']}` remains proxy-only(프록시 전용) and no authority(권위 없음).\n"
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
    best = final["best_candidate"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F22B(전선22B)가 shock+context PF source proxy(충격+문맥 수익 팩터 원천 프록시)를 실행했습니다.

Effect(효과): PF edge(수익 팩터 우위)가 단순 생명주기 수리 전 entry state(진입 상태)에서 나오는지 proxy-only(프록시 전용) 근거로 분리했습니다.

Best candidate(최상 후보): `{final['best_candidate_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(best.get('validation_profit_factor'))}/{fmt(best.get('validation_trades_per_day'))}/{fmt(best.get('validation_dd_risk'))}` and `{fmt(best.get('oos_profit_factor'))}/{fmt(best.get('oos_trades_per_day'))}/{fmt(best.get('oos_dd_risk'))}`.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "pending_or_missing(대기 또는 누락)"}


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
