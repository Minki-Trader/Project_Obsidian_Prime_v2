from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage_frontier_02 import four_axis_proxy_scout as scout
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b


STAGE_ID = "stage_frontier_12__trade_shape_duration_controlled_onnx_scout"
RUN_ID = "frontier12B_trade_shape_duration_label_proxy_scout_v1"
RUN_NUMBER = "frontier12B"
PARENT_RUN_ID = "frontier12A_stage_open_trade_shape_duration_controlled_onnx_scout_v1"
NEXT_STRICT_RUN_ID = "frontier12C_grok_pre_expensive_trade_shape_duration_review_v1"
NEXT_REPAIR_RUN_ID = "frontier12C_trade_shape_duration_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_12/frontier12b_trade_shape_duration_label_proxy_scout.py")
STAGE_OPEN_SUMMARY = (
    STAGE_ROOT
    / "02_runs"
    / PARENT_RUN_ID
    / "stage_open_summary.json"
)

LABEL_ORDER = f04d.LABEL_ORDER
LABEL_NAMES = f04d.LABEL_NAMES
HOLD_MAX_BARS = 12
SCALE_QUANTILE = 0.90
SCOUT_DENSITY_LOW = 5.0
SCOUT_DENSITY_HIGH = 10.0
SCOUT_PF_FLOOR = 1.2
SCOUT_DD_CEILING = 15.0
F11_VALIDATION_DD_REFERENCE = 59.5315
WORST_SUBPERIOD_DD_PRESERVED_CEILING = 30.0

MODEL_ID_SHORT = {
    "logreg_l2_c0p5_plain_argmax": "lr_plain",
    "logreg_l2_c0p5_balanced_argmax": "lr_bal",
    "rf_depth5_leaf80_balanced_argmax": "rf_bal",
}


@dataclass(frozen=True)
class ShapeVariant:
    variant_id: str
    family_id: str
    hold_bars: int
    early_window_bars: int
    target_multiplier: float
    adverse_cap_multiplier: float
    early_adverse_cap_multiplier: float
    recovery_floor_multiplier: float
    score_margin_multiplier: float
    scale_quantile: float
    base_scale_log_return: float

    @property
    def target_log_return(self) -> float:
        return self.base_scale_log_return * self.target_multiplier

    @property
    def adverse_cap_log_return(self) -> float:
        return self.base_scale_log_return * self.adverse_cap_multiplier

    @property
    def early_adverse_cap_log_return(self) -> float:
        return self.base_scale_log_return * self.early_adverse_cap_multiplier

    @property
    def recovery_floor_log_return(self) -> float:
        return self.base_scale_log_return * self.recovery_floor_multiplier

    @property
    def score_margin(self) -> float:
        return self.base_scale_log_return * self.score_margin_multiplier


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    stage_open = read_json(STAGE_OPEN_SUMMARY)
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    variants = build_variants(full, raw)
    result = train_and_evaluate(full, raw, feature_order, variants)
    final = build_final(created_at, result, variants, source_integrity, feature_order, stage_open)
    artifacts = write_artifacts(result, final, variants)
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
                    "best_candidate": final["best_candidate_row"].get("candidate_id"),
                    "next_run_id": final["next_run_id"],
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def build_variants(full: pd.DataFrame, raw: pd.DataFrame) -> list[ShapeVariant]:
    raw_indexes = full["raw_index"].astype("int64").to_numpy()
    log_close = raw["log_close"].to_numpy(dtype="float64")
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    fwd = log_close[raw_indexes + HOLD_MAX_BARS] - log_close[raw_indexes]
    base_scale = float(np.nanquantile(np.abs(fwd[train_mask]), SCALE_QUANTILE))
    if not math.isfinite(base_scale) or base_scale <= 0:
        raise RuntimeError("Invalid train-only base scale(학습 전용 기준 척도 오류).")
    specs = [
        ("fast_shape", 6, 2, 0.72, 0.42, 0.24, 0.08, 0.06),
        ("base_shape", 9, 3, 0.86, 0.52, 0.30, 0.10, 0.08),
        ("full_horizon_shape", 12, 4, 1.00, 0.62, 0.36, 0.12, 0.10),
    ]
    variants: list[ShapeVariant] = []
    for family_id, hold, early, target, adverse_cap, early_cap, recovery, margin in specs:
        variant_id = (
            f"f12b_{family_id}_h{hold}_e{early}_"
            f"t{target:.2f}_cap{adverse_cap:.2f}_ecap{early_cap:.2f}_rec{recovery:.2f}"
        ).replace(".", "p")
        variants.append(
            ShapeVariant(
                variant_id=variant_id,
                family_id=family_id,
                hold_bars=hold,
                early_window_bars=early,
                target_multiplier=target,
                adverse_cap_multiplier=adverse_cap,
                early_adverse_cap_multiplier=early_cap,
                recovery_floor_multiplier=recovery,
                score_margin_multiplier=margin,
                scale_quantile=SCALE_QUANTILE,
                base_scale_log_return=base_scale,
            )
        )
    return variants


def train_and_evaluate(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    feature_order: list[str],
    variants: list[ShapeVariant],
) -> dict[str, Any]:
    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values(피처 행렬 NaN 또는 무한대).")
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    sample_indices = np.concatenate(
        [
            np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())[:256]
            for split in ("train", "validation", "oos")
        ]
    )
    model_metrics: list[dict[str, Any]] = []
    subperiod_metrics: list[dict[str, Any]] = []
    oracle_metrics: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    distribution_rows: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []
    target_diagnostics: list[dict[str, Any]] = []

    for variant in variants:
        path = shape_path_arrays(full, raw, variant)
        labels, oracle_signal, diagnostics = build_shape_labels(path, variant)
        target_diagnostics.append({"target_id": variant.variant_id, **json_ready(asdict(variant)), **diagnostics})
        distribution_rows.extend(label_distribution(full, labels, variant))
        oracle_metrics.extend(evaluate_all_splits(full, oracle_signal, path["fwd_return"], variant, "oracle_label_replay(오라클 라벨 재생)", "oracle"))
        missing = sorted(set(LABEL_ORDER) - set(int(value) for value in labels[train_mask]))
        if missing:
            skipped_rows.append(
                {
                    "target_id": variant.variant_id,
                    "reason": f"missing_train_classes={missing}",
                    "label_boundary": "train_only_label_materialization(학습 전용 라벨 물질화)",
                }
            )
            continue
        for spec in f04d.MODEL_SPECS:
            candidate_id = f"{variant.variant_id}__{MODEL_ID_SHORT.get(spec.model_id, spec.model_id[:10])}"
            model_instance_id = f"f12b_{candidate_id}"
            model = clone(spec.estimator)
            model.fit(x_all[train_mask], labels[train_mask])
            probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
            pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
            signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")

            target_dir = MODEL_DIR / variant.variant_id
            io_path(target_dir).mkdir(parents=True, exist_ok=True)
            model_path = target_dir / f"{model_instance_id}.joblib"
            onnx_path = target_dir / f"{model_instance_id}.onnx"
            joblib.dump(model, io_path(model_path))
            export_meta = export_sklearn_to_onnx_zipmap_disabled(
                model,
                onnx_path,
                feature_count=x_all.shape[1],
                target_opset=12,
                drop_label_output=False,
            )
            parity = check_onnxruntime_probability_parity(
                model,
                onnx_path,
                x_all[sample_indices],
                class_order=LABEL_ORDER,
                tolerance=1e-5,
            )
            parity_rows.append(
                {
                    "candidate_id": candidate_id,
                    "target_id": variant.variant_id,
                    "model_id": spec.model_id,
                    "model_instance_id": model_instance_id,
                    "onnx_path": onnx_path.as_posix(),
                    "onnx_sha256": export_meta["sha256"],
                    "joblib_path": model_path.as_posix(),
                    "joblib_sha256": sha256_file(model_path),
                    "parity_passed": bool(parity["passed"]),
                    "parity_max_abs_diff": parity["max_abs_diff"],
                    "parity_mean_abs_diff": parity["mean_abs_diff"],
                    "rows_checked": parity["rows"],
                    "input_name": parity["input_name"],
                    "output_names": "|".join(parity["output_names"]),
                }
            )
            classification_rows.extend(classification_metrics(full, labels, pred_label, variant, spec.model_id, model_instance_id, candidate_id))
            split_rows = evaluate_all_splits(
                full,
                signal,
                path["fwd_return"],
                variant,
                "argmax_model_signal(최대확률 모델 신호)",
                candidate_id,
                model_id=spec.model_id,
                model_instance_id=model_instance_id,
            )
            model_metrics.extend(split_rows)
            subperiod_metrics.extend(evaluate_subperiods(full, signal, path["fwd_return"], variant, candidate_id, spec.model_id, model_instance_id))

    candidate_summary = build_candidate_summary(model_metrics, subperiod_metrics, parity_rows, classification_rows)
    return {
        "model_metrics": model_metrics,
        "subperiod_metrics": subperiod_metrics,
        "oracle_metrics": oracle_metrics,
        "classification_metrics": classification_rows,
        "onnx_parity": parity_rows,
        "label_distribution": distribution_rows,
        "skipped": skipped_rows,
        "target_diagnostics": target_diagnostics,
        "candidate_summary": candidate_summary,
    }


def shape_path_arrays(full: pd.DataFrame, raw: pd.DataFrame, variant: ShapeVariant) -> dict[str, np.ndarray]:
    raw_indexes = full["raw_index"].astype("int64").to_numpy()
    base = raw["log_close"].to_numpy(dtype="float64")[raw_indexes]
    log_close = raw["log_close"].to_numpy(dtype="float64")
    log_high = raw["log_high"].to_numpy(dtype="float64")
    log_low = raw["log_low"].to_numpy(dtype="float64")
    high_steps = np.vstack([log_high[raw_indexes + step] - base for step in range(1, variant.hold_bars + 1)])
    low_steps = np.vstack([base - log_low[raw_indexes + step] for step in range(1, variant.hold_bars + 1)])
    early_end = min(variant.early_window_bars, variant.hold_bars)
    return {
        "long_mfe": np.nanmax(high_steps, axis=0),
        "long_mae": np.nanmax(low_steps, axis=0),
        "short_mfe": np.nanmax(low_steps, axis=0),
        "short_mae": np.nanmax(high_steps, axis=0),
        "early_long_mae": np.nanmax(low_steps[:early_end], axis=0),
        "early_short_mae": np.nanmax(high_steps[:early_end], axis=0),
        "fwd_return": log_close[raw_indexes + variant.hold_bars] - base,
        "high_steps": high_steps,
        "low_steps": low_steps,
    }


def build_shape_labels(path: dict[str, np.ndarray], variant: ShapeVariant) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    target = variant.target_log_return
    cap = variant.adverse_cap_log_return
    early_cap = variant.early_adverse_cap_log_return
    recovery = variant.recovery_floor_log_return
    score_margin = variant.score_margin
    long_score = (
        path["long_mfe"] / target
        - 0.85 * path["long_mae"] / cap
        - 0.45 * path["early_long_mae"] / early_cap
        + path["fwd_return"] / max(variant.base_scale_log_return, 1e-12)
    )
    short_score = (
        path["short_mfe"] / target
        - 0.85 * path["short_mae"] / cap
        - 0.45 * path["early_short_mae"] / early_cap
        - path["fwd_return"] / max(variant.base_scale_log_return, 1e-12)
    )
    long_ok = (
        (path["long_mfe"] >= target)
        & (path["long_mae"] <= cap)
        & (path["early_long_mae"] <= early_cap)
        & (path["fwd_return"] >= recovery)
        & ((long_score - short_score) >= score_margin)
    )
    short_ok = (
        (path["short_mfe"] >= target)
        & (path["short_mae"] <= cap)
        & (path["early_short_mae"] <= early_cap)
        & (path["fwd_return"] <= -recovery)
        & ((short_score - long_score) >= score_margin)
    )
    signal = np.zeros(len(path["fwd_return"]), dtype="int8")
    signal[long_ok] = 1
    signal[short_ok] = -1
    conflict = long_ok & short_ok
    if conflict.any():
        signal[conflict] = np.where(long_score[conflict] > short_score[conflict], 1, -1)
    labels = np.where(signal < 0, 0, np.where(signal > 0, 2, 1)).astype("int64")
    diagnostics = {
        "label_boundary": "train_only_scale_future_path_label_not_runtime(학습 전용 척도 미래 경로 라벨, 런타임 아님)",
        "oracle_long_count": int((signal == 1).sum()),
        "oracle_short_count": int((signal == -1).sum()),
        "oracle_flat_count": int((signal == 0).sum()),
        "conflict_count": int(conflict.sum()),
        "mean_long_score": float(np.nanmean(long_score)),
        "mean_short_score": float(np.nanmean(short_score)),
    }
    return labels, signal, diagnostics


def label_distribution(full: pd.DataFrame, labels: np.ndarray, variant: ShapeVariant) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        mask = full["split"].astype(str).eq(split).to_numpy()
        split_labels = labels[mask]
        total = int(mask.sum())
        row = {
            "target_id": variant.variant_id,
            "split": split,
            "rows": total,
            "short_count": int((split_labels == 0).sum()),
            "flat_count": int((split_labels == 1).sum()),
            "long_count": int((split_labels == 2).sum()),
        }
        for label, name in LABEL_NAMES.items():
            row[f"{name}_fraction"] = float((split_labels == label).sum() / total) if total else 0.0
        rows.append(row)
    return rows


def classification_metrics(
    full: pd.DataFrame,
    labels: np.ndarray,
    pred_label: np.ndarray,
    variant: ShapeVariant,
    model_id: str,
    model_instance_id: str,
    candidate_id: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        mask = full["split"].astype(str).eq(split).to_numpy()
        y_true = labels[mask]
        y_pred = pred_label[mask]
        rows.append(
            {
                "candidate_id": candidate_id,
                "target_id": variant.variant_id,
                "model_id": model_id,
                "model_instance_id": model_instance_id,
                "split": split,
                "rows": int(mask.sum()),
                "accuracy": float(accuracy_score(y_true, y_pred)),
                "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
                "macro_f1": float(f1_score(y_true, y_pred, labels=LABEL_ORDER, average="macro", zero_division=0)),
                "pred_short": int((y_pred == 0).sum()),
                "pred_flat": int((y_pred == 1).sum()),
                "pred_long": int((y_pred == 2).sum()),
                "true_short": int((y_true == 0).sum()),
                "true_flat": int((y_true == 1).sum()),
                "true_long": int((y_true == 2).sum()),
            }
        )
    return rows


def evaluate_all_splits(
    full: pd.DataFrame,
    signal: np.ndarray,
    fwd_return: np.ndarray,
    variant: ShapeVariant,
    comparison_kind: str,
    candidate_id: str,
    *,
    model_id: str = "oracle",
    model_instance_id: str = "oracle",
) -> list[dict[str, Any]]:
    return [
        evaluate_mask(
            full,
            signal,
            fwd_return,
            full["split"].astype(str).eq(split).to_numpy(),
            variant,
            comparison_kind,
            candidate_id,
            model_id,
            model_instance_id,
            split=split,
            granularity="aggregate(합계)",
            period=split,
        )
        for split in ("train", "validation", "oos")
    ]


def evaluate_subperiods(
    full: pd.DataFrame,
    signal: np.ndarray,
    fwd_return: np.ndarray,
    variant: ShapeVariant,
    candidate_id: str,
    model_id: str,
    model_instance_id: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    timestamps = pd.to_datetime(full["timestamp"], utc=True)
    local_times = timestamps.dt.tz_convert("America/New_York").dt.tz_localize(None)
    periods = {
        "month(月)": local_times.dt.to_period("M").astype(str),
        "quarter(분기)": local_times.dt.to_period("Q").astype(str),
    }
    for split in ("train", "validation", "oos"):
        split_mask = full["split"].astype(str).eq(split).to_numpy()
        split_indexes = np.flatnonzero(split_mask)
        for granularity, period_values in periods.items():
            split_periods = pd.Series(period_values[split_mask]).reset_index(drop=True)
            for period in sorted(split_periods.unique()):
                within = split_periods.eq(period).to_numpy()
                absolute = np.zeros(len(full), dtype=bool)
                absolute[split_indexes[within]] = True
                rows.append(
                    evaluate_mask(
                        full,
                        signal,
                        fwd_return,
                        absolute,
                        variant,
                        "subperiod_argmax_model_signal(하위기간 최대확률 모델 신호)",
                        candidate_id,
                        model_id,
                        model_instance_id,
                        split=split,
                        granularity=granularity,
                        period=str(period),
                    )
                )
    return rows


def evaluate_mask(
    full: pd.DataFrame,
    signal: np.ndarray,
    fwd_return: np.ndarray,
    mask: np.ndarray,
    variant: ShapeVariant,
    comparison_kind: str,
    candidate_id: str,
    model_id: str,
    model_instance_id: str,
    *,
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
        "candidate_id": candidate_id,
        "target_id": variant.variant_id,
        "model_id": model_id,
        "model_instance_id": model_instance_id,
        "comparison_kind": comparison_kind,
        "split": split,
        "granularity": granularity,
        "period": period,
        "tier_scope": "Tier A(티어 A)",
        "record_view": "Tier A separate(티어 A 분리)",
        "hold_bars": variant.hold_bars,
        "early_window_bars": variant.early_window_bars,
        "target_multiplier": variant.target_multiplier,
        "adverse_cap_multiplier": variant.adverse_cap_multiplier,
        "early_adverse_cap_multiplier": variant.early_adverse_cap_multiplier,
        "recovery_floor_multiplier": variant.recovery_floor_multiplier,
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
        "sparse_flag": bool(sparse_flag),
        "pf999_sparse_flag": bool(pf999_sparse_flag),
        "density_axis_distance": density_distance,
        "pf_axis_distance": pf_distance,
        "dd_axis_distance": dd_distance,
        "smoothness_axis_distance": smoothness_distance,
        "aspiration_distance_score": density_distance + pf_distance + dd_distance + smoothness_distance,
        "proxy_cost_log_return": scout.ROUGH_COST_LOG_RETURN,
    }


def build_candidate_summary(
    model_metrics: list[dict[str, Any]],
    subperiod_metrics: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
    classification_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    metrics_by_candidate: dict[str, list[dict[str, Any]]] = {}
    for row in model_metrics:
        metrics_by_candidate.setdefault(str(row["candidate_id"]), []).append(row)
    sub_by_candidate: dict[str, list[dict[str, Any]]] = {}
    for row in subperiod_metrics:
        sub_by_candidate.setdefault(str(row["candidate_id"]), []).append(row)
    parity_by_candidate = {str(row["candidate_id"]): row for row in parity_rows}
    class_by_candidate_split = {
        (str(row["candidate_id"]), str(row["split"])): row for row in classification_rows
    }
    summaries: list[dict[str, Any]] = []
    for candidate_id, rows in metrics_by_candidate.items():
        split_rows = {str(row["split"]): row for row in rows}
        if "validation" not in split_rows or "oos" not in split_rows:
            continue
        val = split_rows["validation"]
        oos = split_rows["oos"]
        subs = [row for row in sub_by_candidate.get(candidate_id, []) if row["split"] in {"validation", "oos"}]
        worst_sub_dd = max([float(row["dd_risk_percent"]) for row in subs], default=999.0)
        negative_subperiod_fraction = float(np.mean([float(row["net_profit"]) <= 0 for row in subs])) if subs else 1.0
        subperiod_density_min = min([float(row["trades_per_day"]) for row in subs], default=0.0)
        parity = parity_by_candidate.get(candidate_id, {})
        validation_class = class_by_candidate_split.get((candidate_id, "validation"), {})
        oos_class = class_by_candidate_split.get((candidate_id, "oos"), {})
        strict = all(
            [
                bool(parity.get("parity_passed")),
                metric_pass(val),
                metric_pass(oos),
                worst_sub_dd <= SCOUT_DD_CEILING,
                negative_subperiod_fraction <= 0.25,
            ]
        )
        preserved = all(
            [
                bool(parity.get("parity_passed")),
                float(val["dd_risk_percent"]) < F11_VALIDATION_DD_REFERENCE,
                float(oos["dd_risk_percent"]) <= SCOUT_DD_CEILING,
                float(oos["profit_factor"]) >= SCOUT_PF_FLOOR,
                float(oos["net_profit"]) > 0,
                worst_sub_dd < F11_VALIDATION_DD_REFERENCE,
                worst_sub_dd <= WORST_SUBPERIOD_DD_PRESERVED_CEILING,
            ]
        )
        score = (
            float(val["aspiration_distance_score"])
            + float(oos["aspiration_distance_score"])
            + (worst_sub_dd / 10.0)
            + negative_subperiod_fraction
        )
        summaries.append(
            {
                "candidate_id": candidate_id,
                "target_id": val["target_id"],
                "model_id": val["model_id"],
                "model_instance_id": val["model_instance_id"],
                "strict_scout_clue_pass": bool(strict),
                "preserved_clue_pass": bool(preserved),
                "shape_duration_score": score,
                "validation_profit_factor": val["profit_factor"],
                "validation_trades_per_day": val["trades_per_day"],
                "validation_dd_risk_percent": val["dd_risk_percent"],
                "validation_net_profit": val["net_profit"],
                "validation_equity_trend_r2": val["equity_trend_r2"],
                "oos_profit_factor": oos["profit_factor"],
                "oos_trades_per_day": oos["trades_per_day"],
                "oos_dd_risk_percent": oos["dd_risk_percent"],
                "oos_net_profit": oos["net_profit"],
                "oos_equity_trend_r2": oos["equity_trend_r2"],
                "validation_oos_subperiod_worst_dd_risk_percent": worst_sub_dd,
                "validation_oos_negative_subperiod_fraction": negative_subperiod_fraction,
                "validation_oos_subperiod_min_trades_per_day": subperiod_density_min,
                "parity_passed": bool(parity.get("parity_passed")),
                "onnx_path": parity.get("onnx_path", ""),
                "onnx_sha256": parity.get("onnx_sha256", ""),
                "joblib_path": parity.get("joblib_path", ""),
                "joblib_sha256": parity.get("joblib_sha256", ""),
                "validation_macro_f1": validation_class.get("macro_f1", ""),
                "oos_macro_f1": oos_class.get("macro_f1", ""),
                "signal_contract": "argmax_only_no_threshold_search(최대확률 전용, 임계값 탐색 없음)",
            }
        )
    summaries.sort(
        key=lambda row: (
            not bool(row["strict_scout_clue_pass"]),
            not bool(row["preserved_clue_pass"]),
            float(row["shape_duration_score"]),
        )
    )
    return json_ready(summaries)


def metric_pass(row: dict[str, Any]) -> bool:
    return all(
        [
            float(row["net_profit"]) > 0,
            float(row["profit_factor"]) >= SCOUT_PF_FLOOR,
            SCOUT_DENSITY_LOW <= float(row["trades_per_day"]) <= SCOUT_DENSITY_HIGH,
            float(row["dd_risk_percent"]) <= SCOUT_DD_CEILING,
        ]
    )


def build_final(
    created_at: str,
    result: dict[str, Any],
    variants: list[ShapeVariant],
    source_integrity: dict[str, Any],
    feature_order: list[str],
    stage_open: dict[str, Any],
) -> dict[str, Any]:
    candidate_summary = result["candidate_summary"]
    strict_rows = [row for row in candidate_summary if row.get("strict_scout_clue_pass")]
    preserved_rows = [row for row in candidate_summary if row.get("preserved_clue_pass")]
    best = candidate_summary[0] if candidate_summary else {}
    status = "trade_shape_duration_strict_scout_clue_no_authority" if strict_rows else (
        "trade_shape_duration_preserved_clue_no_authority" if preserved_rows else "trade_shape_duration_no_strict_clue_no_authority"
    )
    judgment = "strict_scout_clue_candidate(엄격 탐색 단서 후보)" if strict_rows else (
        "preserved_clue_candidate(보존 단서 후보)" if preserved_rows else "negative_memory_candidate(부정 기억 후보)"
    )
    next_run_id = NEXT_STRICT_RUN_ID if strict_rows else NEXT_REPAIR_RUN_ID
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "strict_scout_clue_rows": len(strict_rows),
        "preserved_clue_rows": len(preserved_rows),
        "candidate_row_count": len(candidate_summary),
        "best_candidate_row": best,
        "variant_count": len(variants),
        "model_count": len(f04d.MODEL_SPECS),
        "stage_open_status": stage_open.get("status", ""),
        "source_integrity": source_integrity,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "wfo_status": "not_run_requires_grok_pre_expensive_if_strict(엄격 단서가 있으면 그록 비싼 검증 전 검토 필요)",
        "mt5_status": "not_run_proxy_only_no_runtime_authority(프록시 전용, 런타임 권위 없음)",
    }


def write_artifacts(result: dict[str, Any], final: dict[str, Any], variants: list[ShapeVariant]) -> dict[str, Path]:
    artifacts = {
        "variant_manifest": RUN_ROOT / "variant_manifest.csv",
        "label_distribution": RUN_ROOT / "label_distribution.csv",
        "oracle_metrics": RUN_ROOT / "oracle_metrics.csv",
        "model_metrics": RUN_ROOT / "model_metrics.csv",
        "subperiod_metrics": RUN_ROOT / "subperiod_metrics.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "candidate_summary": RUN_ROOT / "candidate_summary.csv",
        "target_diagnostics": RUN_ROOT / "target_diagnostics.json",
        "skipped": RUN_ROOT / "skipped.csv",
        "final_decision": RUN_ROOT / "final_decision.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_csv(artifacts["variant_manifest"], [asdict(variant) for variant in variants])
    write_csv(artifacts["label_distribution"], result["label_distribution"])
    write_csv(artifacts["oracle_metrics"], result["oracle_metrics"])
    write_csv(artifacts["model_metrics"], result["model_metrics"])
    write_csv(artifacts["subperiod_metrics"], result["subperiod_metrics"])
    write_csv(artifacts["classification_metrics"], result["classification_metrics"])
    write_csv(artifacts["onnx_parity"], result["onnx_parity"])
    write_csv(artifacts["candidate_summary"], result["candidate_summary"])
    write_csv(artifacts["skipped"], result["skipped"])
    write_json(artifacts["target_diagnostics"], result["target_diagnostics"])
    write_json(artifacts["final_decision"], final)
    write_json(
        artifacts["run_manifest"],
        {
            **final,
            "script_path": SCRIPT_PATH.as_posix(),
            "script_sha256": sha256_file(SCRIPT_PATH),
            "stage_open_summary": artifact_identity(STAGE_OPEN_SUMMARY),
            "dataset": artifact_identity(f03b.DATASET_PATH),
            "feature_order": artifact_identity(f03b.FEATURE_ORDER_PATH),
            "artifacts": {key: path.as_posix() for key, path in artifacts.items()},
        },
    )
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    text = f"""# Frontier12B Trade Shape Duration Label Proxy Scout(프론티어12B 거래 형상 보유 기간 라벨 프록시 탐색)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): train-only scale(학습 전용 척도)로 3개 trade-shape label variants(거래 형상 라벨 변형)를 만들고, fixed argmax ONNX models(고정 최대확률 온엑스 모델)을 학습했습니다.

Effect(효과): label source(라벨 원천)를 바꿨을 때 validation/OOS DD(검증/표본밖 손실폭), density(빈도), PF(수익 팩터), smoothness(매끄러움)가 동시에 가까워지는지 봅니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `{final['candidate_row_count']}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- best candidate(최고 후보): `{best.get('candidate_id', 'none')}`
- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- worst subperiod DD(최악 하위기간 손실폭): `{fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}%`

## Artifacts(산출물)

- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- model metrics(모델 지표): `{artifacts['model_metrics'].as_posix()}`
- subperiod metrics(하위기간 지표): `{artifacts['subperiod_metrics'].as_posix()}`
- ONNX parity(온엑스 동등성): `{artifacts['onnx_parity'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다. WFO/MT5(WFO/MT5)는 strict scout clue(엄격 탐색 단서)와 Grok pre-expensive review(그록 비싼 검증 전 검토) 전에는 실행하지 않습니다.

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동): strict clue(엄격 단서)가 있으면 Grok pre-expensive review(그록 비싼 검증 전 검토)로 가고, 없으면 repair/closeout decision(수리/마감 결정)으로 갑니다. Effect(효과): proxy scout(프록시 탐색)를 completion candidate(완성 후보)로 과장하지 않습니다.
"""
    f03b.write_text_sig(REPORT_PATH, text)


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(final))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(final))
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    for row in ledger_rows(final, artifacts):
        f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(stage_ledger, "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): strict rows(엄격 행) `{final['strict_scout_clue_rows']}`, preserved rows(보존 행) `{final['preserved_clue_rows']}`, next run(다음 실행) `{final['next_run_id']}`.\n",
    )


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join(
        [
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
        ]
    )


def current_working_state(final: dict[str, Any]) -> str:
    best = final["best_candidate_row"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier12B(프론티어12B)는 trade-shape duration labels(거래 형상 보유 기간 라벨)를 ONNX proxy scout(온엑스 프록시 탐색)로 시험했습니다.

Effect(효과): best candidate(최고 후보) `{best.get('candidate_id', 'none')}`의 validation/OOS PF-density-DD(검증/표본밖 수익 팩터-빈도-손실폭)를 기록했고, authority claim(권위 주장)은 하지 않았습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_candidate_row"]
    return f"""# Frontier12 Selection Status(프론티어12 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Latest run(최근 실행): `{RUN_ID}`

Best candidate(최고 후보): `{best.get('candidate_id', 'none')}`

Strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`

Preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`

Report(보고서): `{REPORT_PATH.as_posix()}`

Candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def review_index(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    artifact_lines = "\n".join(f"- `{path.as_posix()}`" for path in artifacts.values())
    return f"""# Frontier12 Review Index(프론티어12 검토 색인)

Updated(갱신): {final['created_at_utc']}

## Reviews(검토)

- `frontier12A_stage_open_trade_shape_duration_controlled_onnx_scout_v1`: stage open(단계 개방), Grok accepted(그록 수용).
- `{RUN_ID}`: trade-shape duration label proxy scout(거래 형상 보유 기간 라벨 프록시 탐색), no WFO/MT5(WFO/MT5 없음).

## Latest Artifacts(최신 산출물)

{artifact_lines}
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier12B Required Gate Coverage Audit(프론티어12B 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- data_integrity_gate(데이터 무결성 게이트): train-only base scale(학습 전용 기준 척도), fixed split(고정 분할), feature order hash(피처 순서 해시) recorded(기록됨).
- model_validation_gate(모델 검증 게이트): ONNX parity(온엑스 동등성), classification metrics(분류 지표), validation/OOS metrics(검증/표본밖 지표) recorded(기록됨).
- artifact_lineage_gate(산출물 계보 게이트): run manifest(실행 목록), model hashes(모델 해시), ONNX hashes(온엑스 해시) recorded(기록됨).
- paired_tier_gate(짝 티어 게이트): Tier A separate(티어 A 분리) computed(계산됨), Tier B and combined(티어 B와 합산)은 missing_required(필수 누락)로 기록됨.
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음).

Effect(효과): proxy scout(프록시 탐색) 결과만 주장하고, runtime authority(런타임 권위)는 주장하지 않습니다.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "trade_shape_duration_label_proxy_scout(거래 형상 보유 기간 라벨 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_wfo_no_mt5_no_authority",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["candidate_row_count"]),
        "claim_boundary": "proxy_scout_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_trade_shape_duration_label_proxy",
        "subrun_id": f"{RUN_ID}__tier_a_trade_shape_duration_label_proxy",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "trade_shape_duration_label_proxy_not_runtime(거래 형상 보유 기간 라벨 프록시, 런타임 아님)",
        "primary_kpi": primary_kpi_text(best),
        "guardrail_kpi": "train_only_label_scale_argmax_only_no_threshold_no_wfo_no_mt5_no_authority(학습 전용 라벨 척도, 최대확률 전용, 임계값/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
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
        "scoreboard_lane": "trade_shape_duration_label_proxy_scout(거래 형상 보유 기간 라벨 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "train_only_label_scale_argmax_only_no_threshold_no_wfo_no_mt5_no_authority(학습 전용 라벨 척도, 최대확률 전용, 임계값/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_trade_shape_duration_label_proxy",
            "subrun_id": f"{RUN_ID}__tier_a_trade_shape_duration_label_proxy",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "trade_shape_duration_label_proxy_not_runtime(거래 형상 보유 기간 라벨 프록시, 런타임 아님)",
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
        f"val_pf={fmt(best.get('validation_profit_factor'))};"
        f"val_density={fmt(best.get('validation_trades_per_day'))};"
        f"val_dd={fmt(best.get('validation_dd_risk_percent'))};"
        f"oos_pf={fmt(best.get('oos_profit_factor'))};"
        f"oos_density={fmt(best.get('oos_trades_per_day'))};"
        f"oos_dd={fmt(best.get('oos_dd_risk_percent'))};"
        f"worst_sub_dd={fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}"
    )


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = f03b.read_csv_header(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    pd.DataFrame(json_ready(rows)).to_csv(io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if not math.isfinite(number):
        return "inf"
    return f"{number:.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
