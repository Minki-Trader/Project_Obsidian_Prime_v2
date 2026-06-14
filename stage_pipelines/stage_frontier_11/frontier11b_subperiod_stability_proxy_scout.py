from __future__ import annotations

import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash, ordered_sklearn_probabilities, sha256_file
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_04 import frontier04b_path_aware_label_proxy_scout as f04b
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b
from stage_pipelines.stage_frontier_10 import frontier10b_utility_distillation_proxy_scout as f10b


STAGE_ID = "stage_frontier_11__subperiod_stability_first_onnx_scout"
RUN_ID = "frontier11B_subperiod_stability_proxy_scout_v1"
RUN_NUMBER = "frontier11B"
PARENT_RUN_ID = "frontier11A_stage_open_subperiod_stability_first_onnx_scout_v1"
SOURCE_RUN_ID = "frontier10C_utility_distillation_capped_repair_scout_v1"
NEXT_STRICT_RUN_ID = "frontier11C_grok_pre_expensive_subperiod_stability_review_v1"
NEXT_REPAIR_RUN_ID = "frontier11C_stability_selector_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_11/frontier11b_subperiod_stability_proxy_scout.py")

SOURCE_RUN_ROOT = (
    Path("stages")
    / "stage_frontier_10__split_consistent_utility_distillation"
    / "02_runs"
    / SOURCE_RUN_ID
)
SOURCE_SUMMARY_PATH = SOURCE_RUN_ROOT / "repair_candidate_summary.csv"
SOURCE_MANIFEST_PATH = SOURCE_RUN_ROOT / "run_manifest.json"
SOURCE_FINAL_PATH = SOURCE_RUN_ROOT / "repair_final_decision.json"
SOURCE_REPORT_PATH = (
    Path("stages")
    / "stage_frontier_10__split_consistent_utility_distillation"
    / "03_reviews"
    / f"{SOURCE_RUN_ID}_report.md"
)

LABEL_ORDER = f04d.LABEL_ORDER
SCOUT_DENSITY_LOW = 5.0
SCOUT_DENSITY_HIGH = 10.0
PF_FLOOR = 1.2
DD_HARD_REFERENCE_PERCENT = 10.0
NEGATIVE_PERIOD_FRACTION_CEILING = 0.25
ENTROPY_FLOOR = 0.65


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    source_summary = read_csv_frame(SOURCE_SUMMARY_PATH)
    source_manifest = read_json(SOURCE_MANIFEST_PATH)
    source_final = read_json(SOURCE_FINAL_PATH)
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    path = f07b.path_arrays(full, raw, f10b.HORIZON_BARS)
    result = evaluate_existing_candidate_pool(
        full=full,
        feature_order=feature_order,
        fwd_return=path["fwd_return"],
        source_summary=source_summary,
        source_manifest=source_manifest,
    )
    final = build_final(
        created_at=created_at,
        result=result,
        source_summary=source_summary,
        source_manifest=source_manifest,
        source_final=source_final,
        source_integrity=source_integrity,
        feature_order=feature_order,
    )
    artifacts = write_artifacts(result, final)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "run_id": RUN_ID,
                    "strict_scout_clue_rows": final["strict_scout_clue_rows"],
                    "preserved_clue_rows": final["preserved_clue_rows"],
                    "aggregate_top": final["aggregate_top_candidate"].get("candidate_id"),
                    "stability_top": final["best_candidate_row"].get("candidate_id"),
                    "next_run_id": final["next_run_id"],
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def evaluate_existing_candidate_pool(
    *,
    full: pd.DataFrame,
    feature_order: list[str],
    fwd_return: np.ndarray,
    source_summary: pd.DataFrame,
    source_manifest: dict[str, Any],
) -> dict[str, Any]:
    candidate_rows = [row.to_dict() for _, row in source_summary.iterrows()]
    model_map = {
        str(model["model_instance_id"]): model
        for model in source_manifest.get("models", [])
        if str(model.get("model_instance_id", "")).strip()
    }
    missing_models = missing_candidate_models(candidate_rows, model_map)
    if missing_models:
        return {
            "blocked": True,
            "candidate_summary": [],
            "subperiod_metrics": [],
            "selector_comparison": [],
            "missing_models": missing_models,
            "model_signal_identity": [],
        }

    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values.")

    subperiod_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    enriched_candidates: list[dict[str, Any]] = []
    for aggregate_rank, row in enumerate(candidate_rows, start=1):
        model_identity = model_map[str(row["model_instance_id"])]
        model_path = Path(str(model_identity["joblib_path"]))
        model = joblib.load(io_path(model_path))
        probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
        pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
        signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")
        signal_rows.append(
            {
                "candidate_id": row["candidate_id"],
                "target_id": row["target_id"],
                "model_instance_id": row["model_instance_id"],
                "source_joblib_path": model_identity["joblib_path"],
                "source_joblib_sha256": sha256_file(model_path),
                "source_onnx_path": model_identity["onnx_path"],
                "source_onnx_sha256": model_identity["onnx_sha256"],
                "signal_contract": row.get("signal_contract", ""),
                "nonflat_signal_rows": int((signal != 0).sum()),
            }
        )
        candidate_subperiod_rows = subperiod_metrics_for_candidate(
            full=full,
            signal=signal,
            fwd_return=fwd_return,
            row=row,
        )
        subperiod_rows.extend(candidate_subperiod_rows)
        enriched_candidates.append(
            enrich_candidate_with_stability(
                row=row,
                aggregate_rank=aggregate_rank,
                subperiod_rows=candidate_subperiod_rows,
            )
        )

    ranked = rank_stability_candidates(enriched_candidates)
    selector_comparison = build_selector_comparison(ranked, candidate_rows)
    return {
        "blocked": False,
        "candidate_summary": ranked,
        "subperiod_metrics": subperiod_rows,
        "selector_comparison": selector_comparison,
        "missing_models": [],
        "model_signal_identity": signal_rows,
    }


def missing_candidate_models(
    candidate_rows: list[dict[str, Any]],
    model_map: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    missing: list[dict[str, Any]] = []
    for row in candidate_rows:
        model = model_map.get(str(row.get("model_instance_id", "")))
        if not model:
            missing.append(
                {
                    "candidate_id": row.get("candidate_id", ""),
                    "model_instance_id": row.get("model_instance_id", ""),
                    "reason": "model_manifest_row_missing(모델 실행 목록 행 누락)",
                }
            )
            continue
        for field in ("joblib_path", "onnx_path"):
            path = Path(str(model.get(field, "")))
            if not path_exists(path):
                missing.append(
                    {
                        "candidate_id": row.get("candidate_id", ""),
                        "model_instance_id": row.get("model_instance_id", ""),
                        "path": path.as_posix(),
                        "reason": f"{field}_missing({field} 누락)",
                    }
                )
    return missing


def subperiod_metrics_for_candidate(
    *,
    full: pd.DataFrame,
    signal: np.ndarray,
    fwd_return: np.ndarray,
    row: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    timestamps = pd.to_datetime(full["timestamp"], utc=True)
    local_times = timestamps.dt.tz_convert("America/New_York").dt.tz_localize(None)
    periods = {
        "month(월)": local_times.dt.to_period("M").astype(str),
        "quarter(분기)": local_times.dt.to_period("Q").astype(str),
    }
    for split in ("train", "validation", "oos"):
        split_mask = full["split"].astype(str).eq(split).to_numpy()
        for granularity, period_values in periods.items():
            split_periods = pd.Series(period_values[split_mask]).reset_index(drop=True)
            for period in sorted(split_periods.unique()):
                period_mask_within_split = split_periods.eq(period).to_numpy()
                absolute_mask = np.zeros(len(full), dtype=bool)
                split_indexes = np.flatnonzero(split_mask)
                absolute_mask[split_indexes[period_mask_within_split]] = True
                rows.append(
                    evaluate_mask(
                        full=full,
                        signal=signal,
                        fwd_return=fwd_return,
                        mask=absolute_mask,
                        candidate_row=row,
                        split=split,
                        granularity=granularity,
                        period=str(period),
                    )
                )
    return rows


def evaluate_mask(
    *,
    full: pd.DataFrame,
    signal: np.ndarray,
    fwd_return: np.ndarray,
    mask: np.ndarray,
    candidate_row: dict[str, Any],
    split: str,
    granularity: str,
    period: str,
) -> dict[str, Any]:
    split_signal = signal[mask].astype("int8")
    trade_mask = split_signal != 0
    pnl = split_signal.astype("float64") * fwd_return[mask] - trade_mask.astype("float64") * scout.ROUGH_COST_LOG_RETURN
    trade_pnl = pnl[trade_mask]
    timestamps = full.loc[mask, "timestamp"].reset_index(drop=True)
    trade_times = timestamps.loc[trade_mask]
    metrics = scout.trade_metrics(trade_pnl, trade_times)
    days = scout.count_scope_days(timestamps) if len(timestamps) else 0
    trade_count = int(trade_mask.sum())
    trades_per_day = float(trade_count / days) if days else 0.0
    sparse_floor = max(5, int(math.ceil(days / 2))) if days else 5
    sparse_flag = trade_count < sparse_floor
    pf999_sparse_flag = bool(metrics["profit_factor"] >= 999.0 and sparse_flag)
    dd_risk = max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"]))
    density_distance = scout.density_axis_distance(trades_per_day)
    pf_distance = scout.profit_factor_axis_distance(metrics["profit_factor"], trade_count, sparse_flag, pf999_sparse_flag)
    dd_distance = max(0.0, (dd_risk - scout.DD_TARGET_PERCENT) / scout.DD_TARGET_PERCENT)
    smoothness_distance = scout.smoothness_axis_distance(metrics)
    return {
        "candidate_id": candidate_row["candidate_id"],
        "target_id": candidate_row["target_id"],
        "model_id": candidate_row["model_id"],
        "model_instance_id": candidate_row["model_instance_id"],
        "split": split,
        "granularity": granularity,
        "period": period,
        "tier_scope": "Tier A(티어 A)",
        "record_view": "Tier A separate(티어 A 분리)",
        "rows_in_slice": int(mask.sum()),
        "trade_count": trade_count,
        "days_in_scope": days,
        "trades_per_day": trades_per_day,
        "long_trade_count": int((split_signal == 1).sum()),
        "short_trade_count": int((split_signal == -1).sum()),
        "flat_count": int((split_signal == 0).sum()),
        "net_profit": metrics["net_profit"],
        "profit_factor": metrics["profit_factor"],
        "expectancy": metrics["expectancy"],
        "win_rate": metrics["win_rate"],
        "max_drawdown_percent": metrics["max_drawdown_percent"],
        "max_monthly_drawdown_percent": metrics["max_monthly_drawdown_percent"],
        "dd_risk_percent": dd_risk,
        "underwater_ratio": metrics["underwater_ratio"],
        "max_loss_streak": metrics["max_loss_streak"],
        "equity_trend_r2": metrics["equity_trend_r2"],
        "density_axis_distance": density_distance,
        "pf_axis_distance": pf_distance,
        "dd_axis_distance": dd_distance,
        "smoothness_axis_distance": smoothness_distance,
        "aspiration_distance_score": density_distance + pf_distance + dd_distance + smoothness_distance,
        "sparse_flag": bool(sparse_flag),
        "pf999_sparse_flag": pf999_sparse_flag,
        "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
    }


def enrich_candidate_with_stability(
    *,
    row: dict[str, Any],
    aggregate_rank: int,
    subperiod_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    item = dict(row)
    item["aggregate_rank"] = aggregate_rank
    item["source_run_id"] = SOURCE_RUN_ID
    item["selector_surface"] = "subperiod_stability_first(하위기간 안정성 우선)"
    for split in ("validation", "oos"):
        for granularity_key, label in (("month", "month(월)"), ("quarter", "quarter(분기)")):
            prefix = f"{split}_{granularity_key}"
            group = [
                metric
                for metric in subperiod_rows
                if metric["split"] == split and metric["granularity"] == label
            ]
            add_group_summary(item, prefix, group)
    add_cross_split_stability(item)
    item["strict_scout_clue_pass"] = strict_stability_pass(item)
    item["stability_preserved_clue_pass"] = False
    item["preserved_clue_pass"] = False
    return json_ready(item)


def add_group_summary(item: dict[str, Any], prefix: str, group: list[dict[str, Any]]) -> None:
    if not group:
        item[f"{prefix}_slice_count"] = 0
        item[f"{prefix}_worst_dd_risk_percent"] = 999.0
        item[f"{prefix}_worst_net_profit"] = -999.0
        item[f"{prefix}_negative_net_fraction"] = 1.0
        item[f"{prefix}_max_underwater_ratio"] = 1.0
        item[f"{prefix}_min_equity_trend_r2"] = 0.0
        item[f"{prefix}_trade_count_entropy"] = 0.0
        item[f"{prefix}_min_trades_per_day"] = 0.0
        item[f"{prefix}_max_trades_per_day"] = 0.0
        item[f"{prefix}_mean_aspiration_distance_score"] = 999.0
        return
    item[f"{prefix}_slice_count"] = len(group)
    item[f"{prefix}_worst_dd_risk_percent"] = max(float(row["dd_risk_percent"]) for row in group)
    item[f"{prefix}_worst_net_profit"] = min(float(row["net_profit"]) for row in group)
    item[f"{prefix}_negative_net_fraction"] = float(np.mean([float(row["net_profit"]) <= 0.0 for row in group]))
    item[f"{prefix}_max_underwater_ratio"] = max(float(row["underwater_ratio"]) for row in group)
    item[f"{prefix}_min_equity_trend_r2"] = min(float(row["equity_trend_r2"]) for row in group)
    item[f"{prefix}_trade_count_entropy"] = trade_count_entropy([int(row["trade_count"]) for row in group])
    item[f"{prefix}_min_trades_per_day"] = min(float(row["trades_per_day"]) for row in group)
    item[f"{prefix}_max_trades_per_day"] = max(float(row["trades_per_day"]) for row in group)
    item[f"{prefix}_mean_aspiration_distance_score"] = float(
        np.mean([float(row["aspiration_distance_score"]) for row in group])
    )


def add_cross_split_stability(item: dict[str, Any]) -> None:
    dd_keys = [
        "validation_month_worst_dd_risk_percent",
        "validation_quarter_worst_dd_risk_percent",
        "oos_month_worst_dd_risk_percent",
        "oos_quarter_worst_dd_risk_percent",
    ]
    negative_keys = [
        "validation_month_negative_net_fraction",
        "validation_quarter_negative_net_fraction",
        "oos_month_negative_net_fraction",
        "oos_quarter_negative_net_fraction",
    ]
    entropy_keys = [
        "validation_month_trade_count_entropy",
        "validation_quarter_trade_count_entropy",
        "oos_month_trade_count_entropy",
        "oos_quarter_trade_count_entropy",
    ]
    underwater_keys = [
        "validation_month_max_underwater_ratio",
        "validation_quarter_max_underwater_ratio",
        "oos_month_max_underwater_ratio",
        "oos_quarter_max_underwater_ratio",
    ]
    r2_keys = [
        "validation_month_min_equity_trend_r2",
        "validation_quarter_min_equity_trend_r2",
        "oos_month_min_equity_trend_r2",
        "oos_quarter_min_equity_trend_r2",
    ]
    aggregate_score = safe_float(item.get("validation_oos_score_sum"), 999.0)
    worst_dd = max(safe_float(item.get(key), 999.0) for key in dd_keys)
    negative_mean = float(np.mean([safe_float(item.get(key), 1.0) for key in negative_keys]))
    entropy_mean = float(np.mean([safe_float(item.get(key), 0.0) for key in entropy_keys]))
    underwater_mean = float(np.mean([safe_float(item.get(key), 1.0) for key in underwater_keys]))
    smoothness_loss = float(np.mean([1.0 - min(max(safe_float(item.get(key), 0.0), 0.0), 1.0) for key in r2_keys]))
    dd_component = float(np.mean([safe_float(item.get(key), 999.0) / DD_HARD_REFERENCE_PERCENT for key in dd_keys]))
    density_component = float(
        np.mean(
            [
                scout.density_axis_distance(safe_float(item.get("validation_trades_per_day"), 0.0)),
                scout.density_axis_distance(safe_float(item.get("oos_trades_per_day"), 0.0)),
            ]
        )
    )
    item["validation_oos_subperiod_worst_dd_risk_percent"] = worst_dd
    item["validation_oos_negative_period_fraction_mean"] = negative_mean
    item["validation_oos_trade_count_entropy_mean"] = entropy_mean
    item["validation_oos_underwater_mean"] = underwater_mean
    item["validation_oos_subperiod_smoothness_loss"] = smoothness_loss
    item["validation_oos_density_component"] = density_component
    item["stability_score"] = (
        0.35 * aggregate_score
        + 0.25 * dd_component
        + 0.15 * negative_mean
        + 0.10 * underwater_mean
        + 0.10 * smoothness_loss
        + 0.05 * (1.0 - entropy_mean)
        + 0.05 * density_component
    )


def strict_stability_pass(item: dict[str, Any]) -> bool:
    aggregate_pass = all(
        [
            boolish(item.get("parity_passed")),
            boolish(item.get("learnability_pass")),
            PF_FLOOR <= safe_float(item.get("validation_profit_factor")),
            PF_FLOOR <= safe_float(item.get("oos_profit_factor")),
            safe_float(item.get("validation_net_profit")) > 0.0,
            safe_float(item.get("oos_net_profit")) > 0.0,
            SCOUT_DENSITY_LOW <= safe_float(item.get("validation_trades_per_day")) <= SCOUT_DENSITY_HIGH,
            SCOUT_DENSITY_LOW <= safe_float(item.get("oos_trades_per_day")) <= SCOUT_DENSITY_HIGH,
            safe_float(item.get("validation_dd_risk_percent"), 999.0) < DD_HARD_REFERENCE_PERCENT,
            safe_float(item.get("oos_dd_risk_percent"), 999.0) < DD_HARD_REFERENCE_PERCENT,
        ]
    )
    subperiod_pass = all(
        [
            safe_float(item.get("validation_oos_subperiod_worst_dd_risk_percent"), 999.0) < DD_HARD_REFERENCE_PERCENT,
            safe_float(item.get("validation_oos_negative_period_fraction_mean"), 1.0) <= NEGATIVE_PERIOD_FRACTION_CEILING,
            safe_float(item.get("validation_oos_trade_count_entropy_mean"), 0.0) >= ENTROPY_FLOOR,
        ]
    )
    return bool(aggregate_pass and subperiod_pass)


def rank_stability_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    aggregate_top = min(candidates, key=lambda row: int(row["aggregate_rank"]))
    aggregate_top_score = safe_float(aggregate_top.get("stability_score"), 999.0)
    aggregate_top_worst_dd = safe_float(aggregate_top.get("validation_oos_subperiod_worst_dd_risk_percent"), 999.0)
    ranked = sorted(
        candidates,
        key=lambda row: (
            not boolish(row.get("strict_scout_clue_pass")),
            safe_float(row.get("stability_score"), 999.0),
            safe_float(row.get("validation_oos_subperiod_worst_dd_risk_percent"), 999.0),
            safe_float(row.get("oos_dd_risk_percent"), 999.0),
            -safe_float(row.get("oos_profit_factor"), 0.0),
        ),
    )
    for rank, row in enumerate(ranked, start=1):
        row["stability_rank"] = rank
        row["stability_beats_aggregate_top_score"] = bool(safe_float(row["stability_score"], 999.0) < aggregate_top_score - 1e-12)
        row["stability_worst_dd_beats_aggregate_top"] = bool(
            safe_float(row["validation_oos_subperiod_worst_dd_risk_percent"], 999.0) < aggregate_top_worst_dd - 1e-12
        )
        row["stability_preserved_clue_pass"] = bool(
            not boolish(row.get("strict_scout_clue_pass"))
            and boolish(row.get("source_preserved_clue_pass", row.get("repair_preserved_clue_pass", False)))
            and rank <= 10
            and row["stability_beats_aggregate_top_score"]
            and row["stability_worst_dd_beats_aggregate_top"]
        )
        row["preserved_clue_pass"] = row["stability_preserved_clue_pass"]
    ranked.sort(
        key=lambda row: (
            not boolish(row.get("strict_scout_clue_pass")),
            not boolish(row.get("preserved_clue_pass")),
            safe_float(row.get("stability_score"), 999.0),
            safe_float(row.get("validation_oos_subperiod_worst_dd_risk_percent"), 999.0),
            safe_float(row.get("oos_dd_risk_percent"), 999.0),
        )
    )
    return ranked


def build_selector_comparison(ranked: list[dict[str, Any]], source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    aggregate_top_id = str(source_rows[0]["candidate_id"]) if source_rows else ""
    aggregate_top = next((row for row in ranked if str(row["candidate_id"]) == aggregate_top_id), ranked[0] if ranked else {})
    stability_top = ranked[0] if ranked else {}
    comparison = []
    for selector, row in (
        ("aggregate_only_selector(합계 전용 선택기)", aggregate_top),
        ("stability_first_selector(안정성 우선 선택기)", stability_top),
    ):
        comparison.append(selector_row(selector, row))
    if aggregate_top and stability_top:
        comparison.append(
            {
                "selector": "stability_minus_aggregate_delta(안정성-합계 차이)",
                "candidate_id": f"{stability_top.get('candidate_id')} minus {aggregate_top.get('candidate_id')}",
                "stability_score_delta": safe_float(stability_top.get("stability_score")) - safe_float(aggregate_top.get("stability_score")),
                "worst_subperiod_dd_delta": safe_float(stability_top.get("validation_oos_subperiod_worst_dd_risk_percent"))
                - safe_float(aggregate_top.get("validation_oos_subperiod_worst_dd_risk_percent")),
                "validation_dd_delta": safe_float(stability_top.get("validation_dd_risk_percent"))
                - safe_float(aggregate_top.get("validation_dd_risk_percent")),
                "oos_dd_delta": safe_float(stability_top.get("oos_dd_risk_percent"))
                - safe_float(aggregate_top.get("oos_dd_risk_percent")),
                "validation_pf_delta": safe_float(stability_top.get("validation_profit_factor"))
                - safe_float(aggregate_top.get("validation_profit_factor")),
                "oos_pf_delta": safe_float(stability_top.get("oos_profit_factor"))
                - safe_float(aggregate_top.get("oos_profit_factor")),
                "claim_boundary": "selector_delta_only_no_authority(선택기 차이만, 권위 없음)",
            }
        )
    return comparison


def selector_row(selector: str, row: dict[str, Any]) -> dict[str, Any]:
    return {
        "selector": selector,
        "candidate_id": row.get("candidate_id", ""),
        "aggregate_rank": row.get("aggregate_rank", ""),
        "stability_rank": row.get("stability_rank", ""),
        "stability_score": row.get("stability_score", ""),
        "strict_scout_clue_pass": row.get("strict_scout_clue_pass", False),
        "preserved_clue_pass": row.get("preserved_clue_pass", False),
        "validation_pf": row.get("validation_profit_factor", ""),
        "validation_density": row.get("validation_trades_per_day", ""),
        "validation_dd": row.get("validation_dd_risk_percent", ""),
        "oos_pf": row.get("oos_profit_factor", ""),
        "oos_density": row.get("oos_trades_per_day", ""),
        "oos_dd": row.get("oos_dd_risk_percent", ""),
        "worst_subperiod_dd": row.get("validation_oos_subperiod_worst_dd_risk_percent", ""),
        "negative_period_fraction_mean": row.get("validation_oos_negative_period_fraction_mean", ""),
        "trade_count_entropy_mean": row.get("validation_oos_trade_count_entropy_mean", ""),
    }


def build_final(
    *,
    created_at: str,
    result: dict[str, Any],
    source_summary: pd.DataFrame,
    source_manifest: dict[str, Any],
    source_final: dict[str, Any],
    source_integrity: dict[str, Any],
    feature_order: list[str],
) -> dict[str, Any]:
    candidates = result["candidate_summary"]
    strict_rows = int(sum(1 for row in candidates if boolish(row.get("strict_scout_clue_pass"))))
    preserved_rows = int(sum(1 for row in candidates if boolish(row.get("preserved_clue_pass"))))
    best = candidates[0] if candidates else {}
    aggregate_top_id = str(source_summary.iloc[0]["candidate_id"]) if not source_summary.empty else ""
    aggregate_top = next((row for row in candidates if str(row.get("candidate_id", "")) == aggregate_top_id), {})
    if result["blocked"]:
        status = "subperiod_stability_blocked_missing_source_models_no_authority"
        judgment = "blocked_missing_source_candidate_models(원천 후보 모델 누락 차단)"
        next_run_id = "frontier11B_repair_source_model_availability_before_selector_v1"
        judgment_class = "blocked(차단)"
    elif strict_rows:
        status = "subperiod_stability_strict_scout_clue_no_authority"
        judgment = "strict_scout_clue(엄격 탐색 단서)"
        next_run_id = NEXT_STRICT_RUN_ID
        judgment_class = "positive_with_boundary(경계부 긍정)"
    elif preserved_rows:
        status = "subperiod_stability_preserved_clue_no_authority"
        judgment = "preserved_clue(보존 단서)"
        next_run_id = NEXT_REPAIR_RUN_ID
        judgment_class = "mixed_preserved_clue(혼합 보존 단서)"
    else:
        status = "subperiod_stability_no_strict_clue_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run_id = NEXT_REPAIR_RUN_ID
        judgment_class = "negative_with_repair_or_closeout_boundary(수리 또는 마감 경계부 부정)"
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "judgment_class": judgment_class,
        "next_run_id": next_run_id,
        "strict_scout_clue_rows": strict_rows,
        "preserved_clue_rows": preserved_rows,
        "candidate_row_count": len(candidates),
        "source_candidate_row_count": int(len(source_summary)),
        "subperiod_metric_rows": len(result["subperiod_metrics"]),
        "missing_model_rows": len(result["missing_models"]),
        "best_candidate_row": best,
        "aggregate_top_candidate": aggregate_top,
        "selector_comparison": result["selector_comparison"],
        "source_final_status": source_final.get("status", ""),
        "source_final_judgment": source_final.get("judgment", ""),
        "feature_order_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "feature_order_sha256": sha256_file(f03b.FEATURE_ORDER_PATH),
        "data_integrity": {
            **source_integrity,
            "data_source": f03b.DATASET_PATH.as_posix(),
            "time_axis": "closed_bar_m5_timestamp(확정 5분봉 타임스탬프)",
            "feature_label_boundary": (
                "Frontier11B reuses existing F10C fitted models and does not refit labels/objectives/weights"
                "(전선11B는 기존 F10C 적합 모델을 재사용하고 라벨/목적/가중을 다시 적합하지 않음)"
            ),
            "split_boundary": (
                "subperiod metrics are post-fit validation/OOS ranking diagnostics only"
                "(하위기간 지표는 적합 후 검증/OOS 순위 진단 전용)"
            ),
            "leakage_judgment": "post_fit_selector_only_no_validation_oos_fit(적합 후 선택기 전용, 검증/OOS 적합 없음)",
        },
        "model_validation": {
            "model_family": "existing F10C fixed argmax ONNX/joblib pool(기존 F10C 고정 최대확률 ONNX/joblib 후보군)",
            "selection_metric": (
                "stability_score = aggregate score plus worst subperiod DD, negative period fraction, underwater, smoothness loss, entropy, density component"
                "(안정성 점수 = 합계 점수 + 최악 하위기간 손실폭/음수 기간 비율/수중 비율/매끄러움 손실/엔트로피/밀도 요소)"
            ),
            "control_arm": "aggregate_only_selector from F10C row order(F10C 행 순서 합계 전용 선택기)",
            "threshold_policy": "argmax_only_no_threshold_search_no_bridge(최대확률 전용, 임계값 탐색/브리지 없음)",
            "overfit_risk": "selector observes validation/OOS only as scout diagnostic, so no authority claim(선택기는 검증/OOS를 탐색 진단으로만 보므로 권위 주장 없음)",
        },
        "artifact_lineage": {
            "source_inputs": [SOURCE_SUMMARY_PATH.as_posix(), SOURCE_MANIFEST_PATH.as_posix(), SOURCE_FINAL_PATH.as_posix()],
            "source_manifest_sha256": sha256_file(SOURCE_MANIFEST_PATH),
            "source_summary_sha256": sha256_file(SOURCE_SUMMARY_PATH),
            "source_report": SOURCE_REPORT_PATH.as_posix(),
            "producer": SCRIPT_PATH.as_posix(),
            "consumer": next_run_id,
            "lineage_judgment": "connected_existing_candidate_pool_no_refit(기존 후보군 연결, 재적합 없음)",
            "source_manifest_model_count": len(source_manifest.get("models", [])),
        },
        "runtime_parity": {
            "source_onnx_parity": "inherited_as_reference_from_F10C_manifest(F10C 실행 목록에서 참조로만 계승)",
            "new_parity_run": "not_run_no_new_model_export(새 모델 export 없음으로 미실행)",
            "runtime_claim_boundary": "research_selector_only_no_wfo_no_mt5(연구 선택기 전용, WFO/MT5 없음)",
        },
        "tier_records": {
            "Tier A separate(티어 A 분리)": "computed_from_existing_F10C_Tier_A_candidate_pool(기존 F10C 티어A 후보군에서 계산)",
            "Tier B separate(티어 B 분리)": "missing_required_no_paired_source(필수 누락, 짝 원천 없음)",
            "Tier A+B combined(티어 A+B 합산)": "missing_required_no_combined_claim(필수 누락, 합산 주장 없음)",
        },
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_artifacts(result: dict[str, Any], final: dict[str, Any]) -> dict[str, Path]:
    artifacts = {
        "stability_candidate_summary": RUN_ROOT / "stability_candidate_summary.csv",
        "subperiod_metrics": RUN_ROOT / "subperiod_metrics.csv",
        "selector_comparison": RUN_ROOT / "selector_comparison.csv",
        "model_signal_identity": RUN_ROOT / "model_signal_identity.csv",
        "missing_models": RUN_ROOT / "missing_models.csv",
        "final_decision": RUN_ROOT / "final_decision.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_csv(artifacts["stability_candidate_summary"], result["candidate_summary"])
    write_csv(artifacts["subperiod_metrics"], result["subperiod_metrics"])
    write_csv(artifacts["selector_comparison"], result["selector_comparison"])
    write_csv(artifacts["model_signal_identity"], result["model_signal_identity"])
    write_csv(artifacts["missing_models"], result["missing_models"])
    final["artifact_lineage"]["artifact_paths"] = [path.as_posix() for path in artifacts.values()]
    write_json(artifacts["final_decision"], final)
    manifest = {
        **final,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "artifacts": {
            name: {"path": path.as_posix(), "sha256": sha256_file(path)}
            for name, path in artifacts.items()
            if name != "run_manifest" and path_exists(path)
        },
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }
    write_json(artifacts["run_manifest"], manifest)
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    aggregate = final["aggregate_top_candidate"]
    text = f"""# Frontier11B Subperiod Stability Proxy Scout Report(전선11B 하위기간 안정성 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier11B(전선11B)는 기존 F10C(전선10C) ONNX/joblib model files(온엑스/joblib 모델 파일) 후보군을 재학습 없이 읽고, validation/OOS(검증/표본밖) month/quarter(월/분기) slice(조각) 안정성을 계산했습니다.

Effect(효과): label/objective/weight/bridge(라벨/목적/가중/브리지) 수리를 반복하지 않고, aggregate-only selector(합계 전용 선택기)와 stability-first selector(안정성 우선 선택기)를 같은 후보 풀(candidate pool, 후보 풀)에서 비교합니다.

## Selector Read(선택기 판독)

- aggregate-only top(합계 전용 최상위): `{aggregate.get('candidate_id', 'none')}`
- stability-first top(안정성 우선 최상위): `{best.get('candidate_id', 'none')}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- stability top validation PF/density/DD(안정성 최상위 검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- stability top OOS PF/density/DD(안정성 최상위 표본밖 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- worst subperiod DD(최악 하위기간 손실폭): `{fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}%`
- negative period fraction mean(음수 기간 비율 평균): `{fmt(best.get('validation_oos_negative_period_fraction_mean'))}`
- trade count entropy mean(거래 수 엔트로피 평균): `{fmt(best.get('validation_oos_trade_count_entropy_mean'))}`

## Local Verification(로컬 검증)

- source candidate pool(원천 후보군): `{SOURCE_SUMMARY_PATH.as_posix()}`
- source manifest(원천 실행 목록): `{SOURCE_MANIFEST_PATH.as_posix()}`
- no refit(재적합 없음): F11B(전선11B)는 model fit/export(모델 적합/내보내기)를 하지 않았습니다.
- slice definition(조각 정의): America/New_York(뉴욕 시간) month/quarter(월/분기) period(기간), split(분할) 내부에서만 계산.
- control arm(대조군): F10C aggregate row order(F10C 합계 행 순서).

## Artifacts(산출물)

- stability candidate summary(안정성 후보 요약): `{artifacts['stability_candidate_summary'].as_posix()}`
- subperiod metrics(하위기간 지표): `{artifacts['subperiod_metrics'].as_posix()}`
- selector comparison(선택기 비교): `{artifacts['selector_comparison'].as_posix()}`
- model signal identity(모델 신호 정체성): `{artifacts['model_signal_identity'].as_posix()}`
- final decision(최종 판단): `{artifacts['final_decision'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다. WFO/MT5(WFO/MT5)는 strict scout clue(엄격 탐색 단서)와 Grok pre-expensive review(그록 비싼 검증 전 검토) 전까지 실행하지 않습니다.

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동): strict clue(엄격 단서)가 있으면 Grok pre-expensive review(그록 비싼 검증 전 검토)로 가고, 없으면 repair/closeout decision(수리/마감 결정)으로 갑니다. Effect(효과): subperiod stability(하위기간 안정성)를 completion candidate(완성 후보)로 과장하지 않고 다음 경계를 고릅니다.
"""
    write_text_sig(REPORT_PATH, text)


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    state_text = f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {final['next_run_id']}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{final['created_at_utc']}'
"""
    io_path(f03b.WORKSPACE_STATE).write_text(state_text, encoding="utf-8-sig", newline="\n")
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(final))
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(final, artifacts))
    write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index_text(final, artifacts))
    write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit_text(final))
    upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    for row in ledger_rows(final, artifacts):
        upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv(stage_ledger, "ledger_row_id", row)
    append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): strict scout clue rows(엄격 탐색 단서 행) `{final['strict_scout_clue_rows']}`, preserved clue rows(보존 단서 행) `{final['preserved_clue_rows']}`, next run(다음 실행) `{final['next_run_id']}`.\n",
    )
    append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{RUN_ID}`: subperiod stability-first selector scout(하위기간 안정성 우선 선택기 탐색)를 기록했습니다. Effect(효과): 기존 F10C(전선10C) 후보군을 재학습하지 않고 안정성 선택 표면만 비교합니다.\n",
    )


def current_state_text(final: dict[str, Any]) -> str:
    best = final["best_candidate_row"]
    aggregate = final["aggregate_top_candidate"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier11B(전선11B)는 기존 F10C(전선10C) 후보군에 subperiod stability-first selector(하위기간 안정성 우선 선택기)를 적용했습니다.

Effect(효과): aggregate-only top(합계 전용 최상위) `{aggregate.get('candidate_id', 'none')}`와 stability-first top(안정성 우선 최상위) `{best.get('candidate_id', 'none')}`를 같은 후보 풀에서 비교했습니다.

Best read(최상위 판독): strict scout clue rows(엄격 탐색 단서 행) `{final['strict_scout_clue_rows']}`, preserved clue rows(보존 단서 행) `{final['preserved_clue_rows']}`, worst subperiod DD(최악 하위기간 손실폭) `{fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}%`.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_candidate_row"]
    aggregate = final["aggregate_top_candidate"]
    return f"""# Frontier11 Selection Status(전선11 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Latest run(최근 실행): `{RUN_ID}`

Report(보고서): `{REPORT_PATH.as_posix()}`

Final decision(최종 판단 파일): `{artifacts['final_decision'].as_posix()}`

Aggregate-only top(합계 전용 최상위): `{aggregate.get('candidate_id', 'none')}`

Stability-first top(안정성 우선 최상위): `{best.get('candidate_id', 'none')}`

Strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`

Preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def review_index_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    artifact_lines = "\n".join(f"- `{path.as_posix()}`" for path in artifacts.values())
    return f"""# Frontier11 Review Index(전선11 검토 색인)

Updated(갱신): {final['created_at_utc']}

## Reviews(검토)

- `frontier11A_stage_open_subperiod_stability_first_onnx_scout_v1`: stage open(단계 개방), Grok retry accepted(그록 재시도 수용), Stage171/273 archive boundary verified(171/273단계 보관소 경계 검증).
- `{RUN_ID}`: subperiod stability proxy scout(하위기간 안정성 프록시 탐색), existing F10C candidate pool(기존 F10C 후보군), no refit(재적합 없음), selector comparison(선택기 비교).

## Latest Artifacts(최신 산출물)

{artifact_lines}
"""


def gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier11B Required Gate Coverage Audit(전선11B 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계부 통과)

## Gate Coverage(게이트 커버리지)

- scope_completion_gate(범위 완료 게이트): satisfied_with_boundary(경계부 충족)
- data_integrity_gate(데이터 무결성 게이트): existing F10C fitted models reused without refit(기존 F10C 적합 모델을 재적합 없이 재사용)
- model_validation_gate(모델 검증 게이트): aggregate selector control and stability selector recorded(합계 선택기 대조군과 안정성 선택기 기록)
- artifact_lineage_gate(산출물 계보 게이트): source manifest/model hashes and run manifest written(원천 실행 목록/모델 해시와 실행 목록 기록)
- paired_tier_gate(티어 쌍 게이트): Tier A computed, Tier B and A+B marked missing_required(티어A 계산, 티어B와 합산은 필수 누락 명시)
- final_claim_guard(최종 주장 보호): satisfied_with_boundary(경계부 충족)

Action(행동): proxy scout(프록시 탐색)는 subperiod month/quarter metrics(하위기간 월/분기 지표)까지 완료했습니다.

Effect(효과): WFO/MT5(WFO/MT5), operating promotion(운영 승격), runtime authority(런타임 권위), completion(완성)은 주장하지 않습니다.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "subperiod_stability_selector_scout(하위기간 안정성 선택기 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_refit;no_authority",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["candidate_row_count"]),
        "claim_boundary": "subperiod_stability_selector_no_refit_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_subperiod_stability_selector",
        "subrun_id": f"{RUN_ID}__tier_a_subperiod_stability_selector",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "subperiod_stability_selector_not_runtime(하위기간 안정성 선택기, 런타임 아님)",
        "primary_kpi": primary_kpi_text(best),
        "guardrail_kpi": "existing_f10c_models_no_refit_no_threshold_no_bridge_no_wfo_no_mt5_no_authority(기존 F10C 모델, 재적합/임계값/브리지/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "source_run_id": SOURCE_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "subperiod_selector_scout_only(하위기간 선택기 탐색 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can subperiod stability-first selection improve zoomed DD and smoothness?(하위기간 안정성 우선 선택이 확대 구간 손실폭과 매끄러움을 개선하는가?)",
        "skill_family": "experiment_execution(실험 실행)",
        "lineage_summary": "frontier10c_existing_candidate_pool_to_frontier11b_selector(전선10C 기존 후보군에서 전선11B 선택기)",
        "best_candidate_id": best.get("candidate_id", ""),
        "best_validation_pf": best.get("validation_profit_factor", ""),
        "best_validation_density": best.get("validation_trades_per_day", ""),
        "best_validation_dd": best.get("validation_dd_risk_percent", ""),
        "best_oos_pf": best.get("oos_profit_factor", ""),
        "best_oos_density": best.get("oos_trades_per_day", ""),
        "best_oos_dd": best.get("oos_dd_risk_percent", ""),
    }


def ledger_rows(final: dict[str, Any], artifacts: dict[str, Path]) -> list[dict[str, Any]]:
    best = final["best_candidate_row"]
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "subperiod_stability_selector_scout(하위기간 안정성 선택기 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "existing_f10c_models_no_refit_no_threshold_no_bridge_no_wfo_no_mt5_no_authority(기존 F10C 모델, 재적합/임계값/브리지/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_subperiod_stability_selector",
            "subrun_id": f"{RUN_ID}__tier_a_subperiod_stability_selector",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "subperiod_stability_selector_not_runtime(하위기간 안정성 선택기, 런타임 아님)",
            "primary_kpi": primary_kpi_text(best),
            "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_authority",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_paired_source(필수 누락, 짝 원천 없음)",
            "notes": "Tier B paired materialization not available(티어 B 짝 물질화 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B(티어 A+B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_combined_claim(필수 누락, 합산 주장 없음)",
            "notes": "combined record blocked by missing Tier B(티어 B 부재로 합산 기록 차단)",
        },
    ]


def primary_kpi_text(best: dict[str, Any]) -> str:
    return (
        f"best={best.get('candidate_id', 'none')};"
        f"strict={best.get('strict_scout_clue_pass', False)};"
        f"preserved={best.get('preserved_clue_pass', False)};"
        f"stability_score={fmt(best.get('stability_score'))};"
        f"worst_subperiod_dd={fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))};"
        f"oos_pf={fmt(best.get('oos_profit_factor'))};"
        f"oos_density={fmt(best.get('oos_trades_per_day'))};"
        f"oos_dd={fmt(best.get('oos_dd_risk_percent'))}"
    )


def trade_count_entropy(counts: list[int]) -> float:
    total = float(sum(max(count, 0) for count in counts))
    if total <= 0.0:
        return 0.0
    if len(counts) <= 1:
        return 1.0
    probs = np.array([max(count, 0) / total for count in counts if count > 0], dtype="float64")
    if len(probs) == 0:
        return 0.0
    entropy = -float(np.sum(probs * np.log(probs)))
    return float(entropy / math.log(len(counts)))


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    return text in {"true", "1", "yes", "y"}


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def csv_header(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    header = csv_header(path)
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows.extend(dict(existing) for existing in csv.DictReader(handle))
    normalized = {column: stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: stringify(item.get(column, "")) for column in header})


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = csv_header(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)


def append_once(path: Path, marker: str, line: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    marker_text = f"<!-- {marker} -->"
    if marker_text in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    text += f"{marker_text}\n{line}"
    write_text_sig(path, text)


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def fmt(value: Any) -> str:
    try:
        value_float = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if math.isinf(value_float):
        return "inf"
    return f"{value_float:.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
