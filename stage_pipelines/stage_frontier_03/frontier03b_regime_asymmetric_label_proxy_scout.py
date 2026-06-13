from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash, sha256_file
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout


STAGE_ID = "stage_frontier_03__regime_conditioned_asymmetric_onnx_labeling"
RUN_ID = "frontier03B_regime_asymmetric_label_proxy_scout_v1"
RUN_NUMBER = "frontier03B"
PARENT_RUN_ID = "frontier03A_stage_open_regime_conditioned_asymmetric_onnx_labeling_v1"
NEXT_CLUE_RUN_ID = "frontier03C_regime_asymmetric_label_micro_search_v1"
NEXT_NEGATIVE_RUN_ID = "frontier03C_label_proxy_repair_or_closeout_decision_v1"

DATASET_PATH = Path(
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = DATASET_PATH.with_name("model_input_feature_order.txt")
FEATURE_MANIFEST_PATH = DATASET_PATH.with_name("feature_set_manifest.json")
MODEL_INPUT_SUMMARY_PATH = DATASET_PATH.with_name("model_input_summary.json")
EXPECTED_FEATURE_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
FRONTIER02C_SUMMARY = Path(
    "stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/"
    "02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/"
    "decision_surface_summary.csv"
)

WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")
CHANGELOG = Path("docs/workspace/changelog.md")
RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")

FORBIDDEN_CLAIMS = [
    "completion",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
]


@dataclass(frozen=True)
class LabelVariant:
    variant_id: str
    description: str
    trend_band_multiplier: float
    chop_band_multiplier: float
    long_target_multiplier: float
    short_target_multiplier: float


VARIANTS: tuple[LabelVariant, ...] = (
    LabelVariant("f03b_v01_balanced_35", "balanced threshold around 3.5x base", 3.5, 3.5, 1.0, 1.0),
    LabelVariant("f03b_v02_balanced_40", "balanced threshold around 4.0x base", 4.0, 4.0, 1.0, 1.0),
    LabelVariant("f03b_v03_balanced_45", "balanced threshold around 4.5x base", 4.5, 4.5, 1.0, 1.0),
    LabelVariant("f03b_v04_trend_easy_chop_strict", "trend easier and chop stricter neutral band", 3.5, 4.5, 1.0, 1.0),
    LabelVariant("f03b_v05_trend_strict_chop_easy", "trend stricter and chop easier neutral band", 4.5, 3.5, 1.0, 1.0),
    LabelVariant("f03b_v06_long_easy_short_strict", "long target easier and short target stricter", 4.0, 4.0, 0.90, 1.10),
    LabelVariant("f03b_v07_long_strict_short_easy", "long target stricter and short target easier", 4.0, 4.0, 1.10, 0.90),
    LabelVariant("f03b_v08_trend_long_easy", "trend and long slightly easier", 3.75, 4.25, 0.90, 1.05),
    LabelVariant("f03b_v09_chop_short_easy", "chop and short slightly easier", 4.25, 3.75, 1.05, 0.90),
    LabelVariant("f03b_v10_strict_smooth", "strict neutral band for smoother fewer trades", 5.0, 5.0, 1.0, 1.0),
    LabelVariant("f03b_v11_trend_density_restore", "trend density restore with strict chop", 3.25, 4.75, 1.0, 1.0),
    LabelVariant("f03b_v12_chop_density_restore", "chop density restore with strict trend", 4.75, 3.25, 1.0, 1.0),
)


def main() -> int:
    ensure_dirs()
    now = utc_now()
    frame = load_and_validate_input()
    feature_order = read_feature_order()
    reference = load_frontier02c_reference()
    regime = build_regime(frame)
    base_threshold = compute_base_threshold(frame)
    variant_grid = build_variant_grid(base_threshold)
    metrics = evaluate_variants(frame, regime, base_threshold, reference)
    summary = build_summary(metrics, reference)
    top = rank_summary(summary).head(12)
    go_rows = summary.loc[summary["go_rule_flag"].astype(bool)].copy()
    final = build_final(now, frame, feature_order, base_threshold, regime, reference, summary, go_rows)
    write_outputs(frame, feature_order, regime, variant_grid, metrics, summary, top, go_rows, final)
    update_stage_docs(now, final, top)
    update_registries(now, final)
    update_current_truth(now, final)

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "variant_rows": len(VARIANTS),
                "metric_rows": int(len(metrics)),
                "go_rule_rows": int(len(go_rows)),
                "best_variant": final["best_variant_id"],
                "best_oos_pf": final["best_oos_profit_factor"],
                "best_oos_density": final["best_oos_trades_per_day"],
                "best_oos_dd": final["best_oos_max_drawdown_percent"],
                "next_run_id": final["next_run_id"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in [RUN_ROOT, REPORT_PATH.parent, STAGE_ROOT / "04_selected"]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_and_validate_input() -> pd.DataFrame:
    if not path_exists(DATASET_PATH):
        raise FileNotFoundError(DATASET_PATH)
    frame = pd.read_parquet(io_path(DATASET_PATH)).sort_values("timestamp").reset_index(drop=True)
    required = {
        "timestamp",
        "split",
        "future_log_return_12",
        "horizon_bars",
        "label",
        "label_class",
        "adx_14",
        "ema20_ema50_diff",
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    if frame["timestamp"].isna().any():
        raise ValueError("Input contains missing timestamp(타임스탬프 누락).")
    if frame["timestamp"].duplicated().any():
        raise ValueError("Input contains duplicate timestamp(중복 타임스탬프).")
    if set(frame["split"].dropna().astype(str)) != {"train", "validation", "oos"}:
        raise ValueError("Input split(분할)은 train/validation/oos만 포함해야 합니다.")
    if not pd.to_numeric(frame["horizon_bars"], errors="coerce").eq(12).all():
        raise ValueError("Frontier03B contract(계약)은 fwd12(12봉 선행) 전용입니다.")
    return frame


def read_feature_order() -> list[str]:
    features = [line.strip() for line in io_path(FEATURE_ORDER_PATH).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    feature_hash = ordered_hash(features)
    if feature_hash != EXPECTED_FEATURE_HASH:
        raise ValueError(f"Feature order hash mismatch(피처 순서 해시 불일치): {feature_hash}")
    return features


def load_frontier02c_reference() -> dict[str, Any]:
    summary = pd.read_csv(io_path(FRONTIER02C_SUMMARY))
    row = (
        summary.sort_values(
            ["validation_aspiration_distance_score", "validation_joint_pass_count", "oos_aspiration_distance_score"],
            ascending=[True, False, True],
        )
        .iloc[0]
        .to_dict()
    )
    return {
        "candidate_id": row["candidate_id"],
        "path": FRONTIER02C_SUMMARY.as_posix(),
        "sha256": sha256_file(FRONTIER02C_SUMMARY),
        "validation": reference_split(row, "validation"),
        "oos": reference_split(row, "oos"),
        "inheritance_boundary": "reference_only_not_baseline(참조 전용, 기준선 아님)",
    }


def reference_split(row: dict[str, Any], split: str) -> dict[str, float]:
    metrics = {
        "net_profit": num(row.get(f"{split}_net_profit")),
        "profit_factor": num(row.get(f"{split}_profit_factor")),
        "trades_per_day": num(row.get(f"{split}_trades_per_day")),
        "max_drawdown_percent": num(row.get(f"{split}_max_drawdown_percent")),
        "max_monthly_drawdown_percent": num(row.get(f"{split}_max_monthly_drawdown_percent")),
        "underwater_ratio": num(row.get(f"{split}_underwater_ratio")),
        "max_loss_streak": num(row.get(f"{split}_max_loss_streak")),
        "equity_trend_r2": num(row.get(f"{split}_equity_trend_r2")),
        "aspiration_distance_score": num(row.get(f"{split}_aspiration_distance_score")),
    }
    metrics["density_axis_distance"] = scout.density_axis_distance(metrics["trades_per_day"])
    metrics["pf_axis_distance"] = scout.profit_factor_axis_distance(metrics["profit_factor"], 9999, False, False)
    dd_risk = max(metrics["max_drawdown_percent"], metrics["max_monthly_drawdown_percent"])
    metrics["dd_axis_distance"] = max(0.0, (dd_risk - scout.DD_TARGET_PERCENT) / scout.DD_TARGET_PERCENT)
    metrics["smoothness_axis_distance"] = scout.smoothness_axis_distance(metrics)
    return metrics


def compute_base_threshold(frame: pd.DataFrame) -> float:
    train = frame["split"].astype(str).eq("train")
    threshold = float(pd.to_numeric(frame.loc[train, "future_log_return_12"], errors="coerce").abs().quantile(0.33))
    if not math.isfinite(threshold) or threshold <= 0:
        raise ValueError(f"Invalid base threshold(기준 임계값 무효): {threshold}")
    return threshold


def build_regime(frame: pd.DataFrame) -> pd.DataFrame:
    train = frame["split"].astype(str).eq("train")
    adx = pd.to_numeric(frame["adx_14"], errors="coerce").astype("float64")
    ema_abs = pd.to_numeric(frame["ema20_ema50_diff"], errors="coerce").abs().astype("float64")
    adx_z = train_z(adx, train)
    ema_z = train_z(ema_abs, train)
    score = (adx_z + ema_z).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    cutoff = float(score.loc[train].median())
    regime = pd.Series(np.where(score >= cutoff, "trend", "chop"), index=frame.index, dtype="object")
    return pd.DataFrame(
        {
            "timestamp": frame["timestamp"],
            "split": frame["split"].astype(str),
            "regime_score": score,
            "regime": regime,
            "regime_cutoff": cutoff,
            "rule": "train_z(adx_14)+train_z(abs(ema20_ema50_diff)) >= train_median",
            "feature_boundary": "closed_bar_features_only(종료봉 피처 전용)",
        }
    )


def train_z(series: pd.Series, train_mask: pd.Series) -> pd.Series:
    train_values = series.loc[train_mask].replace([np.inf, -np.inf], np.nan).dropna()
    mean = float(train_values.mean()) if len(train_values) else 0.0
    std = float(train_values.std(ddof=0)) if len(train_values) else 1.0
    if not math.isfinite(std) or std <= 1e-12:
        std = 1.0
    return (series - mean) / std


def build_variant_grid(base_threshold: float) -> pd.DataFrame:
    rows = []
    for variant in VARIANTS:
        payload = asdict(variant)
        payload["base_threshold_log_return"] = base_threshold
        payload["max_threshold_multiplier"] = max(
            variant.trend_band_multiplier * variant.long_target_multiplier,
            variant.trend_band_multiplier * variant.short_target_multiplier,
            variant.chop_band_multiplier * variant.long_target_multiplier,
            variant.chop_band_multiplier * variant.short_target_multiplier,
        )
        payload["horizon_bars"] = 12
        payload["model_training"] = "not_used(사용 안 함)"
        payload["onnx_export"] = "not_used(사용 안 함)"
        payload["wfo_mt5"] = "not_used(사용 안 함)"
        rows.append(payload)
    return pd.DataFrame(rows)


def evaluate_variants(
    frame: pd.DataFrame,
    regime: pd.DataFrame,
    base_threshold: float,
    reference: dict[str, Any],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    returns = pd.to_numeric(frame["future_log_return_12"], errors="coerce").astype("float64").to_numpy()
    for variant in VARIANTS:
        signal, thresholds = build_signal(returns, regime["regime"].to_numpy(), base_threshold, variant)
        for split in ("train", "validation", "oos"):
            row = evaluate_split(frame, regime, signal, thresholds, split, variant, reference)
            rows.append(row)
    return pd.DataFrame(rows)


def build_signal(
    returns: np.ndarray,
    regimes: np.ndarray,
    base_threshold: float,
    variant: LabelVariant,
) -> tuple[np.ndarray, np.ndarray]:
    regime_multiplier = np.where(regimes == "trend", variant.trend_band_multiplier, variant.chop_band_multiplier)
    long_threshold = base_threshold * regime_multiplier * variant.long_target_multiplier
    short_threshold = base_threshold * regime_multiplier * variant.short_target_multiplier
    signal = np.zeros(len(returns), dtype="int8")
    signal[returns > long_threshold] = 1
    signal[returns < -short_threshold] = -1
    thresholds = np.where(signal == 1, long_threshold, np.where(signal == -1, short_threshold, base_threshold * regime_multiplier))
    return signal, thresholds.astype("float64")


def evaluate_split(
    frame: pd.DataFrame,
    regime: pd.DataFrame,
    signal: np.ndarray,
    thresholds: np.ndarray,
    split: str,
    variant: LabelVariant,
    reference: dict[str, Any],
) -> dict[str, Any]:
    split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
    split_frame = frame.loc[split_mask, ["timestamp", "future_log_return_12"]].copy()
    split_signal = signal[split_mask].astype("int8")
    trade_mask = split_signal != 0
    pnl = (
        split_signal.astype("float64")
        * pd.to_numeric(split_frame["future_log_return_12"], errors="coerce").to_numpy(dtype="float64")
        - trade_mask.astype("float64") * scout.ROUGH_COST_LOG_RETURN
    )
    trade_pnl = pnl[trade_mask]
    trade_times = split_frame.loc[trade_mask, "timestamp"]
    metrics = scout.trade_metrics(trade_pnl, trade_times)
    trade_count = int(len(trade_pnl))
    days = scout.count_scope_days(split_frame["timestamp"])
    trades_per_day = float(trade_count / days) if days else 0.0
    sparse_floor = max(30, int(math.ceil(days)))
    sparse_flag = trade_count < sparse_floor
    pf999_sparse_flag = bool(metrics["profit_factor"] >= 999.0 and sparse_flag)
    density_distance = scout.density_axis_distance(trades_per_day)
    pf_distance = scout.profit_factor_axis_distance(metrics["profit_factor"], trade_count, sparse_flag, pf999_sparse_flag)
    dd_risk = max(float(metrics["max_drawdown_percent"]), float(metrics["max_monthly_drawdown_percent"]))
    dd_distance = max(0.0, (dd_risk - scout.DD_TARGET_PERCENT) / scout.DD_TARGET_PERCENT)
    smoothness_distance = scout.smoothness_axis_distance(metrics)
    label_counts = {
        "short": int((split_signal == -1).sum()),
        "flat": int((split_signal == 0).sum()),
        "long": int((split_signal == 1).sum()),
    }
    ref = reference.get(split, {})
    return {
        "variant_id": variant.variant_id,
        "description": variant.description,
        "split": split,
        "tier_scope": "Tier A",
        "record_view": "Tier A separate",
        "horizon_bars": 12,
        "trend_band_multiplier": variant.trend_band_multiplier,
        "chop_band_multiplier": variant.chop_band_multiplier,
        "long_target_multiplier": variant.long_target_multiplier,
        "short_target_multiplier": variant.short_target_multiplier,
        "trade_count": trade_count,
        "days_in_scope": days,
        "trades_per_day": trades_per_day,
        "sparse_flag": bool(sparse_flag),
        "pf999_sparse_flag": pf999_sparse_flag,
        "long_trade_count": label_counts["long"],
        "short_trade_count": label_counts["short"],
        "flat_count": label_counts["flat"],
        "trend_trade_count": int(((regime.loc[split_mask, "regime"].to_numpy() == "trend") & trade_mask).sum()),
        "chop_trade_count": int(((regime.loc[split_mask, "regime"].to_numpy() == "chop") & trade_mask).sum()),
        "mean_entry_threshold": float(np.nanmean(thresholds[split_mask][trade_mask])) if trade_count else 0.0,
        "net_profit": metrics["net_profit"],
        "profit_factor": metrics["profit_factor"],
        "expectancy": metrics["expectancy"],
        "win_rate": metrics["win_rate"],
        "max_drawdown_percent": metrics["max_drawdown_percent"],
        "max_monthly_drawdown_percent": metrics["max_monthly_drawdown_percent"],
        "underwater_ratio": metrics["underwater_ratio"],
        "max_loss_streak": metrics["max_loss_streak"],
        "equity_trend_r2": metrics["equity_trend_r2"],
        "density_axis_distance": density_distance,
        "pf_axis_distance": pf_distance,
        "dd_axis_distance": dd_distance,
        "smoothness_axis_distance": smoothness_distance,
        "aspiration_distance_score": density_distance + pf_distance + dd_distance + smoothness_distance,
        "density_pass": bool(scout.DENSITY_TARGET_LOW <= trades_per_day <= scout.DENSITY_TARGET_HIGH),
        "pf_pass": bool(metrics["profit_factor"] >= scout.PF_TARGET and metrics["net_profit"] > 0 and not sparse_flag),
        "dd_pass": bool(dd_risk < scout.DD_TARGET_PERCENT),
        "smoothness_pass": bool(
            metrics["net_profit"] > 0
            and metrics["underwater_ratio"] <= 0.45
            and metrics["equity_trend_r2"] >= 0.35
            and metrics["max_loss_streak"] <= 6
        ),
        "reference_candidate_id": reference["candidate_id"],
        "better_pf_axis_than_02c": bool(pf_distance < ref.get("pf_axis_distance", math.inf)),
        "better_density_axis_than_02c": bool(density_distance < ref.get("density_axis_distance", math.inf)),
        "better_dd_axis_than_02c": bool(dd_distance < ref.get("dd_axis_distance", math.inf)),
        "better_smoothness_axis_than_02c": bool(smoothness_distance < ref.get("smoothness_axis_distance", math.inf)),
        "better_total_distance_than_02c": bool((density_distance + pf_distance + dd_distance + smoothness_distance) < ref.get("aspiration_distance_score", math.inf)),
        "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
    }


def build_summary(metrics: pd.DataFrame, reference: dict[str, Any]) -> pd.DataFrame:
    keys = [
        "variant_id",
        "description",
        "horizon_bars",
        "trend_band_multiplier",
        "chop_band_multiplier",
        "long_target_multiplier",
        "short_target_multiplier",
        "reference_candidate_id",
    ]
    metric_cols = [
        "trade_count",
        "days_in_scope",
        "trades_per_day",
        "sparse_flag",
        "pf999_sparse_flag",
        "long_trade_count",
        "short_trade_count",
        "flat_count",
        "trend_trade_count",
        "chop_trade_count",
        "mean_entry_threshold",
        "net_profit",
        "profit_factor",
        "expectancy",
        "win_rate",
        "max_drawdown_percent",
        "max_monthly_drawdown_percent",
        "underwater_ratio",
        "max_loss_streak",
        "equity_trend_r2",
        "density_axis_distance",
        "pf_axis_distance",
        "dd_axis_distance",
        "smoothness_axis_distance",
        "aspiration_distance_score",
        "density_pass",
        "pf_pass",
        "dd_pass",
        "smoothness_pass",
        "better_pf_axis_than_02c",
        "better_density_axis_than_02c",
        "better_dd_axis_than_02c",
        "better_smoothness_axis_than_02c",
        "better_total_distance_than_02c",
    ]
    rows: list[dict[str, Any]] = []
    for _, group in metrics.groupby(keys, sort=False):
        row = {key: group.iloc[0][key] for key in keys}
        for split in ("train", "validation", "oos"):
            split_row = group.loc[group["split"].eq(split)].iloc[0]
            for column in metric_cols:
                row[f"{split}_{column}"] = split_row[column]
        axis_pairs = (
            ("pf", "better_pf_axis_than_02c"),
            ("density", "better_density_axis_than_02c"),
            ("dd", "better_dd_axis_than_02c"),
            ("smoothness", "better_smoothness_axis_than_02c"),
        )
        improved_axes = [
            name
            for name, column in axis_pairs
            if bool(row[f"validation_{column}"]) and bool(row[f"oos_{column}"])
        ]
        row["validation_oos_positive_net"] = bool(row["validation_net_profit"] > 0 and row["oos_net_profit"] > 0)
        row["axis_improvement_count_vs_02c"] = len(improved_axes)
        row["axis_improvements_vs_02c"] = "|".join(improved_axes)
        row["density_only_improvement"] = improved_axes == ["density"]
        row["go_rule_flag"] = bool(
            row["validation_oos_positive_net"]
            and len(improved_axes) >= 2
            and not row["density_only_improvement"]
        )
        rows.append(row)
    summary = pd.DataFrame(rows)
    summary["validation_rank"] = np.arange(1, len(summary) + 1)
    return rank_summary(summary).reset_index(drop=True)


def rank_summary(summary: pd.DataFrame) -> pd.DataFrame:
    return summary.sort_values(
        [
            "go_rule_flag",
            "axis_improvement_count_vs_02c",
            "oos_better_total_distance_than_02c",
            "validation_aspiration_distance_score",
            "oos_aspiration_distance_score",
        ],
        ascending=[False, False, False, True, True],
    )


def build_final(
    now: str,
    frame: pd.DataFrame,
    feature_order: list[str],
    base_threshold: float,
    regime: pd.DataFrame,
    reference: dict[str, Any],
    summary: pd.DataFrame,
    go_rows: pd.DataFrame,
) -> dict[str, Any]:
    ranked = rank_summary(summary)
    best = ranked.iloc[0].to_dict()
    has_clue = int(len(go_rows)) > 0
    status = "completed_label_proxy_scout_with_scout_clue_no_authority" if has_clue else "completed_label_proxy_scout_negative_memory_no_authority"
    judgment = "scout_clue_no_authority" if has_clue else "negative_memory_no_authority"
    next_run_id = NEXT_CLUE_RUN_ID if has_clue else NEXT_NEGATIVE_RUN_ID
    split_counts = {str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()}
    regime_counts = {str(k): int(v) for k, v in regime["regime"].value_counts().to_dict().items()}
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": now,
        "next_run_id": next_run_id,
        "variant_count": len(VARIANTS),
        "metric_rows": int(len(summary) * 3),
        "summary_rows": int(len(summary)),
        "go_rule_rows": int(len(go_rows)),
        "best_variant_id": str(best["variant_id"]),
        "best_axis_improvement_count_vs_02c": int(best["axis_improvement_count_vs_02c"]),
        "best_axis_improvements_vs_02c": str(best["axis_improvements_vs_02c"]),
        "best_validation_net_profit": num(best["validation_net_profit"]),
        "best_validation_profit_factor": num(best["validation_profit_factor"]),
        "best_validation_trades_per_day": num(best["validation_trades_per_day"]),
        "best_validation_max_drawdown_percent": num(best["validation_max_drawdown_percent"]),
        "best_validation_aspiration_distance_score": num(best["validation_aspiration_distance_score"]),
        "best_oos_net_profit": num(best["oos_net_profit"]),
        "best_oos_profit_factor": num(best["oos_profit_factor"]),
        "best_oos_trades_per_day": num(best["oos_trades_per_day"]),
        "best_oos_max_drawdown_percent": num(best["oos_max_drawdown_percent"]),
        "best_oos_aspiration_distance_score": num(best["oos_aspiration_distance_score"]),
        "reference": reference,
        "data_identity": {
            "dataset_path": DATASET_PATH.as_posix(),
            "dataset_sha256": sha256_file(DATASET_PATH),
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
            "feature_order_sha256": sha256_file(FEATURE_ORDER_PATH),
            "feature_order_hash": ordered_hash(feature_order),
            "feature_count": len(feature_order),
            "rows": int(len(frame)),
            "split_counts": split_counts,
        },
        "label_contract": {
            "horizon_bars": 12,
            "base_threshold_abs_quantile": 0.33,
            "base_threshold_log_return": base_threshold,
            "regime_rule": str(regime["rule"].iloc[0]),
            "regime_cutoff": num(regime["regime_cutoff"].iloc[0]),
            "regime_counts": regime_counts,
            "variant_cap": 12,
            "model_training": "not_used(사용 안 함)",
            "onnx_export": "not_used(사용 안 함)",
            "wfo_mt5": "not_used(사용 안 함)",
        },
        "tier_records": {
            "tier_a_separate": "materialized(물질화)",
            "tier_b_separate": "missing_required(필수 누락)",
            "tier_ab_combined": "out_of_scope_by_claim(주장 범위 밖)",
        },
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in FORBIDDEN_CLAIMS},
    }


def write_outputs(
    frame: pd.DataFrame,
    feature_order: list[str],
    regime: pd.DataFrame,
    variant_grid: pd.DataFrame,
    metrics: pd.DataFrame,
    summary: pd.DataFrame,
    top: pd.DataFrame,
    go_rows: pd.DataFrame,
    final: dict[str, Any],
) -> None:
    paths = {
        "label_variant_grid": RUN_ROOT / "label_variant_grid.csv",
        "label_replay_metrics": RUN_ROOT / "label_replay_metrics.csv",
        "label_replay_summary": RUN_ROOT / "label_replay_summary.csv",
        "top_label_proxy_surfaces": RUN_ROOT / "top_label_proxy_surfaces.csv",
        "go_rule_rows": RUN_ROOT / "go_rule_rows.csv",
        "regime_assignment_audit": RUN_ROOT / "regime_assignment_audit.csv",
        "data_integrity_audit": RUN_ROOT / "data_integrity_audit.json",
        "target_distance_reference": RUN_ROOT / "target_distance_reference.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    variant_grid.to_csv(io_path(paths["label_variant_grid"]), index=False, lineterminator="\n")
    metrics.to_csv(io_path(paths["label_replay_metrics"]), index=False, lineterminator="\n")
    summary.to_csv(io_path(paths["label_replay_summary"]), index=False, lineterminator="\n")
    top.to_csv(io_path(paths["top_label_proxy_surfaces"]), index=False, lineterminator="\n")
    go_rows.to_csv(io_path(paths["go_rule_rows"]), index=False, lineterminator="\n")
    regime.to_csv(io_path(paths["regime_assignment_audit"]), index=False, lineterminator="\n")

    write_json(paths["data_integrity_audit"], build_data_integrity_audit(frame, feature_order, regime, final))
    write_json(paths["target_distance_reference"], final["reference"])
    write_text_sig(REPORT_PATH, report_text(final, top))

    outputs = {
        name: {"path": path.as_posix(), "sha256": sha256_file(path)}
        for name, path in paths.items()
        if name != "run_manifest"
    }
    outputs["report"] = {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)}
    manifest = {
        **final,
        "script_path": "stage_pipelines/stage_frontier_03/frontier03b_regime_asymmetric_label_proxy_scout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_03/frontier03b_regime_asymmetric_label_proxy_scout.py")),
        "inputs": {
            "parent_run_id": PARENT_RUN_ID,
            "dataset_path": DATASET_PATH.as_posix(),
            "dataset_sha256": sha256_file(DATASET_PATH),
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
            "feature_order_sha256": sha256_file(FEATURE_ORDER_PATH),
            "frontier02c_reference_path": FRONTIER02C_SUMMARY.as_posix(),
            "frontier02c_reference_sha256": sha256_file(FRONTIER02C_SUMMARY),
        },
        "outputs": outputs,
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    write_json(paths["run_manifest"], manifest)


def build_data_integrity_audit(
    frame: pd.DataFrame,
    feature_order: list[str],
    regime: pd.DataFrame,
    final: dict[str, Any],
) -> dict[str, Any]:
    split_counts = {str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()}
    return {
        "status": "pass",
        "run_id": RUN_ID,
        "dataset_path": DATASET_PATH.as_posix(),
        "dataset_sha256": sha256_file(DATASET_PATH),
        "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
        "feature_order_sha256": sha256_file(FEATURE_ORDER_PATH),
        "feature_order_hash": ordered_hash(feature_order),
        "expected_feature_hash": EXPECTED_FEATURE_HASH,
        "rows": int(len(frame)),
        "split_counts": split_counts,
        "timestamp_first": frame["timestamp"].min().isoformat(),
        "timestamp_last": frame["timestamp"].max().isoformat(),
        "duplicate_timestamps": int(frame["timestamp"].duplicated().sum()),
        "horizon_bars_unique": sorted(pd.to_numeric(frame["horizon_bars"], errors="coerce").dropna().astype(int).unique().tolist()),
        "regime_rule": final["label_contract"]["regime_rule"],
        "regime_feature_boundary": "adx_14 and ema20_ema50_diff are closed-bar features(종료봉 피처)",
        "future_return_use": "future_log_return_12 used only for label replay target(라벨 재생 목표 전용)",
        "leakage_boundary": "oracle label replay is not runtime signal(오라클 라벨 재생은 런타임 신호 아님)",
        "tier_b_status": final["tier_records"]["tier_b_separate"],
        "tier_ab_status": final["tier_records"]["tier_ab_combined"],
        "regime_counts": {str(k): int(v) for k, v in regime["regime"].value_counts().to_dict().items()},
    }


def report_text(final: dict[str, Any], top: pd.DataFrame) -> str:
    top_rows = top.head(5).to_dict("records")
    best = top_rows[0]
    return f"""# Frontier03B Regime Asymmetric Label Proxy Scout Report(전선03B 레짐 비대칭 라벨 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Boundary(경계)

This run(이번 실행)은 label-proxy replay(라벨 프록시 재생)입니다. ONNX export(온엑스 내보내기), model training(모델 학습), WFO(워크포워드), MT5(메타트레이더5), runtime authority(런타임 권위), live readiness(실거래 준비)는 없습니다.

Effect(효과): regime/label axis(레짐/라벨 축)이 four-axis target distance(네 축 목표 거리)를 줄일 수 있는지 보는 oracle-style scout(오라클 방식 탐색)이며, tradable signal(거래 가능 신호)이 아닙니다.

## Best Read(최상위 판독)

- variant_id(변형 ID): `{best['variant_id']}`
- improvements vs 02C(02C 대비 개선 축): `{best['axis_improvements_vs_02c']}` count(수) `{best['axis_improvement_count_vs_02c']}`
- validation net/PF/density/DD(검증 순수익/수익 팩터/밀도/손실폭): `{fmt(best['validation_net_profit'])}` / `{fmt(best['validation_profit_factor'])}` / `{fmt(best['validation_trades_per_day'])}/day` / `{fmt(best['validation_max_drawdown_percent'])}%`
- OOS net/PF/density/DD(표본외 순수익/수익 팩터/밀도/손실폭): `{fmt(best['oos_net_profit'])}` / `{fmt(best['oos_profit_factor'])}` / `{fmt(best['oos_trades_per_day'])}/day` / `{fmt(best['oos_max_drawdown_percent'])}%`
- go_rule_rows(진행 규칙 행): `{final['go_rule_rows']}`

## Reference Boundary(참조 경계)

Frontier02C(전선02C) candidate(후보) `{final['reference']['candidate_id']}`는 comparison reference(비교 참조)일 뿐 baseline(기준선)이 아닙니다.

## Top Rows(상위 행)

```json
{json.dumps(json_ready(top_rows), ensure_ascii=False, indent=2)}
```

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): `{final['tier_records']['tier_a_separate']}`
- Tier B separate(Tier B 분리): `{final['tier_records']['tier_b_separate']}`
- Tier A+B combined(Tier A+B 합산): `{final['tier_records']['tier_ab_combined']}`

## Next Action(다음 행동)

`{final['next_run_id']}`

Action(행동): next run(다음 실행)은 scout clue(탐색 단서)를 micro-search(미세 탐색)로 좁히거나, 단서가 약하면 repair/closeout decision(수리/마감 결정)을 합니다. Effect(효과): 같은 수리를 반복하지 않고 가설 생명주기(hypothesis lifecycle, 가설 생명주기)를 앞으로 밀거나 정직하게 닫습니다.

## Claim Boundary(주장 경계)

No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def update_stage_docs(now: str, final: dict[str, Any], top: pd.DataFrame) -> None:
    append_once(
        STAGE_ROOT / "03_reviews" / "review_index.md",
        RUN_ID,
        f"- `{RUN_ID}`: `{REPORT_PATH.as_posix()}` - `{final['judgment']}`\n",
    )
    write_text_sig(
        STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage Frontier 03 Selection Status(전선 03단계 선택 상태)

Updated(갱신): {now}

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Judgment(판정): `{final['judgment']}`

Best label proxy(최상위 라벨 프록시): `{final['best_variant_id']}`

Go rule rows(진행 규칙 행): `{final['go_rule_rows']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
""",
    )


def update_current_truth(now: str, final: dict[str, Any]) -> None:
    payload = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": final["status"],
        "current_judgment": final["judgment"],
        "next_run_id": final["next_run_id"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": now,
    }
    io_path(WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False), encoding="utf-8")
    write_text_sig(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {now}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier03B(전선03B)는 regime/asymmetric label proxy replay(레짐/비대칭 라벨 프록시 재생)를 완료했습니다.

Judgment(판정): `{final['judgment']}`

Best read(최상위 판독): `{final['best_variant_id']}` has axis improvement count(축 개선 수) `{final['best_axis_improvement_count_vs_02c']}` versus Frontier02C reference(전선02C 참조).

Next action(다음 행동): `{final['next_run_id']}`. Action(행동)은 scout clue(탐색 단서)를 좁히거나 repair/closeout decision(수리/마감 결정)을 여는 것입니다. Effect(효과)는 Frontier03(전선03) 가설을 반복 없이 앞으로 밀거나 정직하게 닫는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
""",
    )


def update_registries(now: str, final: dict[str, Any]) -> None:
    upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(now, final))
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", ledger_row(final))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    upsert_csv(stage_ledger, "ledger_row_id", ledger_row(final))
    append_once(CHANGELOG, RUN_ID, f"- {now}: `{RUN_ID}` {final['judgment']}. Effect(효과): next run(다음 실행)은 `{final['next_run_id']}`입니다.\n")
    append_once(IDEA_REGISTRY, RUN_ID, f"- `{RUN_ID}`: regime/asymmetric label proxy scout(레짐/비대칭 라벨 프록시 탐색) completed(완료). Effect(효과): label axis(라벨 축)의 scout clue(탐색 단서) 여부를 기록했습니다.\n")
    if final["go_rule_rows"] == 0:
        append_once(NEGATIVE_RESULT_REGISTER, RUN_ID, f"- `{RUN_ID}`: no go-rule rows(진행 규칙 행 없음). Effect(효과): label proxy repair/closeout decision(라벨 프록시 수리/마감 결정)로 넘깁니다.\n")


def run_registry_row(now: str, final: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "label_proxy_scout(라벨 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"go_rule_rows={final['go_rule_rows']};best={final['best_variant_id']};no_authority",
        "work_family": "alpha_exploration(알파 탐색)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["summary_rows"]),
        "gate_count": "",
        "passed_gate_count": "",
        "claim_boundary": "label_proxy_only_no_model_no_onnx_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__tier_a_label_proxy",
        "subrun_id": f"{RUN_ID}__tier_a_label_proxy",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "label_proxy_oracle_not_runtime(라벨 프록시 오라클, 런타임 아님)",
        "primary_kpi": f"oos_pf={fmt(final['best_oos_profit_factor'])};oos_density={fmt(final['best_oos_trades_per_day'])};oos_dd={fmt(final['best_oos_max_drawdown_percent'])}",
        "guardrail_kpi": "no_model_training_no_onnx_no_wfo_no_mt5_no_authority(모델 학습/온엑스/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": (RUN_ROOT / "label_replay_summary.csv").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "label_proxy_oracle_only(라벨 프록시 오라클 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can regime-conditioned asymmetric labels improve four-axis target distance?(레짐 조건 비대칭 라벨이 네 축 목표 거리를 줄일 수 있는가?)",
        "skill_family": "alpha_exploration(알파 탐색)",
        "lineage_summary": "dataset_to_label_proxy_metrics(데이터셋에서 라벨 프록시 지표)",
    }


def ledger_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__tier_a_label_proxy",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_label_proxy",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "label_proxy_oracle_not_runtime(라벨 프록시 오라클, 런타임 아님)",
        "scoreboard_lane": "label_proxy_scout(라벨 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"oos_pf={fmt(final['best_oos_profit_factor'])};oos_density={fmt(final['best_oos_trades_per_day'])};oos_dd={fmt(final['best_oos_max_drawdown_percent'])}",
        "guardrail_kpi": "no_model_training_no_onnx_no_wfo_no_mt5_no_authority(모델 학습/온엑스/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "notes": f"go_rule_rows={final['go_rule_rows']};next={final['next_run_id']};no_authority",
    }


def read_csv_header(path: Path) -> list[str]:
    with path.resolve().open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    header = read_csv_header(path)
    rows: list[dict[str, str]] = []
    with path.resolve().open("r", encoding="utf-8-sig", newline="") as handle:
        for existing in csv.DictReader(handle):
            rows.append(dict(existing))
    normalized = {column: stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    path.resolve().parent.mkdir(parents=True, exist_ok=True)
    with path.resolve().open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: stringify(item.get(column, "")) for column in header})


def append_once(path: Path, marker: str, line: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    marker_text = f"<!-- {marker} -->"
    if marker_text in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    text += f"{marker_text}\n{line}"
    write_text_sig(path, text)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def num(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def fmt(value: Any) -> str:
    return f"{num(value):.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
