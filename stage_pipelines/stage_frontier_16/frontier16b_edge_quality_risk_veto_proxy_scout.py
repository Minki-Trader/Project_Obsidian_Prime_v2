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
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b
from stage_pipelines.stage_frontier_12 import frontier12b_trade_shape_duration_label_proxy_scout as f12b


STAGE_ID = "stage_frontier_16__edge_quality_risk_veto_density_transfer_onnx_scout"
RUN_ID = "frontier16B_edge_quality_risk_veto_proxy_scout_v1"
RUN_NUMBER = "frontier16B"
PARENT_RUN_ID = "frontier16A_stage_open_edge_quality_risk_veto_density_transfer_onnx_scout_v1"
NEXT_STRICT_RUN_ID = "frontier16C_grok_pre_expensive_edge_quality_risk_review_v1"
NEXT_REPAIR_RUN_ID = "frontier16C_edge_quality_risk_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_16/frontier16b_edge_quality_risk_veto_proxy_scout.py")
STAGE_OPEN_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "stage_open_summary.json"

LABEL_ORDER = f04d.LABEL_ORDER
LABEL_NAMES = f04d.LABEL_NAMES
PRIMARY_CELL_ID = "edge_margin__target8"
SCALE_QUANTILE = 0.90
EARLY_WINDOW_BARS = 2
SCOUT_DENSITY_LOW = 5.0
SCOUT_DENSITY_HIGH = 10.0
F15_PRIMARY_VALIDATION_PF = 0.895191
F15_PRIMARY_OOS_PF = 1.071237
F15_PRIMARY_VALIDATION_DD = 21.830578
F15_PRIMARY_OOS_DD = 11.834035

MODEL_ID_SHORT = {
    "logreg_l2_c0p5_plain_argmax": "lr_plain",
    "logreg_l2_c0p5_balanced_argmax": "lr_bal",
    "rf_depth5_leaf80_balanced_argmax": "rf_bal",
}


@dataclass(frozen=True)
class EdgeQualityVariant:
    variant_id: str
    family_id: str
    hold_bars: int
    early_window_bars: int
    target_multiplier: float
    adverse_cap_multiplier: float
    early_adverse_cap_multiplier: float
    recovery_floor_multiplier: float
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


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    stage_open = read_json(STAGE_OPEN_SUMMARY)
    validate_stage_open(stage_open)
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    variants = build_variants(full, raw)
    result = train_and_evaluate(full, raw, feature_order, variants)
    final = build_final(created_at, result, variants, source_integrity, feature_order, stage_open)
    artifacts = write_artifacts(result, final, variants)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "strict_scout_clue_rows": final["strict_scout_clue_rows"],
        "preserved_clue_rows": final["preserved_clue_rows"],
        "candidate_row_count": final["candidate_row_count"],
        "best_candidate": final["best_candidate_row"].get("candidate_id"),
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def validate_stage_open(stage_open: dict[str, Any]) -> None:
    if stage_open.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError("Frontier16A stage-open summary mismatch(프론티어16A 단계 개방 요약 불일치).")
    contract = stage_open.get("locked_decision_contract", {})
    if contract.get("cell_id") != PRIMARY_CELL_ID or int(contract.get("target_density_per_day", 0)) != 8:
        raise RuntimeError("Locked decision contract mismatch(고정 결정 계약 불일치).")
    if len(stage_open.get("label_variants", [])) != 3:
        raise RuntimeError("Variant cap mismatch(변형 상한 불일치).")


def build_variants(full: pd.DataFrame, raw: pd.DataFrame) -> list[EdgeQualityVariant]:
    raw_indexes = full["raw_index"].astype("int64").to_numpy()
    log_close = raw["log_close"].to_numpy(dtype="float64")
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    specs = [
        ("f16b_edge_h8_t0p30_cap0p45_early0p25", "edge_h8_soft_target", 8, 0.30, 0.45, 0.25),
        ("f16b_edge_h8_t0p45_cap0p35_early0p20", "edge_h8_tight_veto", 8, 0.45, 0.35, 0.20),
        ("f16b_edge_h12_t0p50_cap0p50_early0p30", "edge_h12_balanced_veto", 12, 0.50, 0.50, 0.30),
    ]
    variants: list[EdgeQualityVariant] = []
    for variant_id, family_id, hold, target, cap, early_cap in specs:
        fwd = log_close[raw_indexes + hold] - log_close[raw_indexes]
        base_scale = float(np.nanquantile(np.abs(fwd[train_mask]), SCALE_QUANTILE))
        if not math.isfinite(base_scale) or base_scale <= 0:
            raise RuntimeError(f"Invalid train-only base scale for {variant_id}(학습 전용 기준 척도 오류).")
        variants.append(EdgeQualityVariant(
            variant_id=variant_id,
            family_id=family_id,
            hold_bars=hold,
            early_window_bars=min(EARLY_WINDOW_BARS, hold),
            target_multiplier=target,
            adverse_cap_multiplier=cap,
            early_adverse_cap_multiplier=early_cap,
            recovery_floor_multiplier=0.0,
            scale_quantile=SCALE_QUANTILE,
            base_scale_log_return=base_scale,
        ))
    return variants


def train_and_evaluate(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    feature_order: list[str],
    variants: list[EdgeQualityVariant],
) -> dict[str, Any]:
    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values(피처 행렬에 NaN 또는 무한대가 있습니다).")
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    sample_indices = np.concatenate([
        np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())[:256]
        for split in ("train", "validation", "oos")
    ])

    model_metrics: list[dict[str, Any]] = []
    subperiod_metrics: list[dict[str, Any]] = []
    argmax_baseline_metrics: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    distribution_rows: list[dict[str, Any]] = []
    threshold_rows: list[dict[str, Any]] = []
    density_audit: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []
    target_diagnostics: list[dict[str, Any]] = []

    for variant in variants:
        path = edge_path_arrays(full, raw, variant)
        labels, oracle_signal, diagnostics = build_edge_quality_labels(path, variant)
        target_diagnostics.append({"target_id": variant.variant_id, **json_ready(asdict(variant)), **diagnostics})
        distribution_rows.extend(f12b.label_distribution(full, labels, variant))
        missing = sorted(set(LABEL_ORDER) - set(int(value) for value in labels[train_mask]))
        if missing:
            skipped_rows.append({
                "target_id": variant.variant_id,
                "reason": f"missing_train_classes={missing}",
                "label_boundary": "pre_registered_edge_quality_label(사전 등록 엣지 품질 라벨)",
            })
            continue
        for spec in f04d.MODEL_SPECS:
            model_short = MODEL_ID_SHORT.get(spec.model_id, spec.model_id[:10])
            candidate_base = f"{variant.variant_id}__{model_short}"
            model_instance_id = f"f16b_{candidate_base}"
            model = clone(spec.estimator)
            model.fit(x_all[train_mask], labels[train_mask])
            probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
            pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
            argmax_signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")

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
            parity_base = {
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

            argmax_id = f"{candidate_base}__argmax_baseline"
            argmax_baseline_metrics.extend(f12b.evaluate_all_splits(
                full,
                argmax_signal,
                path["fwd_return"],
                variant,
                "argmax_baseline_model_signal(최대확률 기준선 모델 신호)",
                argmax_id,
                model_id=spec.model_id,
                model_instance_id=model_instance_id,
            ))

            score = edge_margin(probabilities)
            direction = np.where(probabilities[:, 0] >= probabilities[:, 2], -1, 1).astype("int8")
            threshold_info = fit_train_threshold(full, score, train_mask, 8)
            threshold = float(threshold_info["threshold_value"])
            selected = np.isfinite(score) & (score >= threshold)
            threshold_signal = np.where(selected, direction, 0).astype("int8")
            candidate_id = f"{candidate_base}__edge_margin__target8"

            threshold_rows.append({
                "candidate_id": candidate_id,
                "target_id": variant.variant_id,
                "model_id": spec.model_id,
                "model_instance_id": model_instance_id,
                "score_contract_id": "edge_margin",
                "cell_id": PRIMARY_CELL_ID,
                "target_density_per_day": 8,
                "is_primary_cell": True,
                "score_expression": "max(p_short, p_long) - p_flat",
                **threshold_info,
                "actual_all_selected_count": int(selected.sum()),
                "threshold_policy": "train_scores_calendar_only_no_pnl(학습 점수와 달력만 사용, 손익 미사용)",
            })
            parity_rows.append({"candidate_id": candidate_id, **parity_base})
            classification_rows.extend(f12b.classification_metrics(
                full,
                labels,
                pred_label,
                variant,
                spec.model_id,
                model_instance_id,
                candidate_id,
            ))
            model_metrics.extend(enrich_metric_rows(f12b.evaluate_all_splits(
                full,
                threshold_signal,
                path["fwd_return"],
                variant,
                "locked_edge_margin_target8_signal(고정 엣지 마진 목표8 신호)",
                candidate_id,
                model_id=spec.model_id,
                model_instance_id=model_instance_id,
            ), threshold))
            subperiod_metrics.extend(enrich_metric_rows(evaluate_threshold_subperiods(
                full,
                threshold_signal,
                path["fwd_return"],
                variant,
                candidate_id,
                spec.model_id,
                model_instance_id,
            ), threshold))
            density_audit.extend(density_audit_rows(full, oracle_signal, argmax_signal, threshold_signal, variant, candidate_id, spec.model_id, model_instance_id, threshold))

    candidate_summary = build_candidate_summary(model_metrics, subperiod_metrics, parity_rows, classification_rows, threshold_rows)
    return {
        "model_metrics": model_metrics,
        "subperiod_metrics": subperiod_metrics,
        "argmax_baseline_metrics": argmax_baseline_metrics,
        "classification_metrics": classification_rows,
        "onnx_parity": parity_rows,
        "label_distribution": distribution_rows,
        "threshold_manifest": threshold_rows,
        "score_contract_manifest": score_contract_manifest_rows(),
        "density_transfer_audit": density_audit,
        "skipped": skipped_rows,
        "target_diagnostics": target_diagnostics,
        "candidate_summary": candidate_summary,
    }


def edge_path_arrays(full: pd.DataFrame, raw: pd.DataFrame, variant: EdgeQualityVariant) -> dict[str, np.ndarray]:
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


def build_edge_quality_labels(path: dict[str, np.ndarray], variant: EdgeQualityVariant) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    target = variant.target_log_return
    cap = variant.adverse_cap_log_return
    early_cap = variant.early_adverse_cap_log_return
    scale = max(variant.base_scale_log_return, 1e-12)
    long_score = (
        path["long_mfe"] / target
        - path["long_mae"] / cap
        - 0.5 * path["early_long_mae"] / early_cap
        + path["fwd_return"] / scale
    )
    short_score = (
        path["short_mfe"] / target
        - path["short_mae"] / cap
        - 0.5 * path["early_short_mae"] / early_cap
        - path["fwd_return"] / scale
    )
    long_ok = (
        (path["fwd_return"] > 0)
        & (path["long_mfe"] >= target)
        & (path["long_mae"] <= cap)
        & (path["early_long_mae"] <= early_cap)
    )
    short_ok = (
        (path["fwd_return"] < 0)
        & (path["short_mfe"] >= target)
        & (path["short_mae"] <= cap)
        & (path["early_short_mae"] <= early_cap)
    )
    signal = np.zeros(len(path["fwd_return"]), dtype="int8")
    signal[long_ok] = 1
    signal[short_ok] = -1
    conflict = long_ok & short_ok
    if conflict.any():
        signal[conflict] = np.where(long_score[conflict] > short_score[conflict], 1, -1)
    labels = np.where(signal < 0, 0, np.where(signal > 0, 2, 1)).astype("int64")
    diagnostics = {
        "label_boundary": "train_only_scale_risk_quality_future_path_label_not_runtime(학습 전용 척도 위험 품질 미래 경로 라벨, 런타임 아님)",
        "oracle_long_count": int((signal == 1).sum()),
        "oracle_short_count": int((signal == -1).sum()),
        "oracle_flat_count": int((signal == 0).sum()),
        "conflict_count": int(conflict.sum()),
        "target_log_return": target,
        "adverse_cap_log_return": cap,
        "early_adverse_cap_log_return": early_cap,
        "mean_long_score": float(np.nanmean(long_score)),
        "mean_short_score": float(np.nanmean(short_score)),
    }
    return labels, signal, diagnostics


def edge_margin(probabilities: np.ndarray) -> np.ndarray:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    return np.maximum(p_short, p_long) - p_flat


def fit_train_threshold(
    full: pd.DataFrame,
    score: np.ndarray,
    train_mask: np.ndarray,
    target_density_per_day: int,
) -> dict[str, Any]:
    timestamps = pd.to_datetime(full.loc[train_mask, "timestamp"], errors="raise").reset_index(drop=True)
    days = f12b.scout.count_scope_days(timestamps) if len(timestamps) else 0
    train_score = np.asarray(score[train_mask], dtype="float64")
    finite_train = train_score[np.isfinite(train_score)]
    target_count = int(math.ceil(float(days) * float(target_density_per_day))) if days else 0
    if target_count <= 0 or len(finite_train) == 0:
        threshold = math.inf
    elif target_count >= len(finite_train):
        threshold = -math.inf
    else:
        threshold = float(np.sort(finite_train)[::-1][target_count - 1])
    selected_train = np.isfinite(train_score) & (train_score >= threshold)
    return {
        "threshold_value": threshold,
        "train_days_in_scope": int(days),
        "target_train_trade_count": int(target_count),
        "actual_train_selected_count": int(selected_train.sum()),
        "actual_train_selected_density_per_day": float(selected_train.sum() / days) if days else 0.0,
        "train_threshold_tie_policy": "numeric_threshold_score_greater_equal(숫자 임계값 이상 선택)",
    }


def evaluate_threshold_subperiods(
    full: pd.DataFrame,
    signal: np.ndarray,
    fwd_return: np.ndarray,
    variant: EdgeQualityVariant,
    candidate_id: str,
    model_id: str,
    model_instance_id: str,
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
        split_indexes = np.flatnonzero(split_mask)
        for granularity, period_values in periods.items():
            split_periods = pd.Series(period_values[split_mask]).reset_index(drop=True)
            for period in sorted(split_periods.unique()):
                within = split_periods.eq(period).to_numpy()
                absolute = np.zeros(len(full), dtype=bool)
                absolute[split_indexes[within]] = True
                rows.append(f12b.evaluate_mask(
                    full,
                    signal,
                    fwd_return,
                    absolute,
                    variant,
                    "subperiod_locked_edge_margin_target8_signal(하위기간 고정 엣지 마진 목표8 신호)",
                    candidate_id,
                    model_id,
                    model_instance_id,
                    split=split,
                    granularity=granularity,
                    period=str(period),
                ))
    return rows


def enrich_metric_rows(rows: list[dict[str, Any]], threshold: float) -> list[dict[str, Any]]:
    for row in rows:
        row.update({
            "score_contract_id": "edge_margin",
            "cell_id": PRIMARY_CELL_ID,
            "target_density_per_day": 8,
            "is_primary_cell": True,
            "threshold_value": threshold,
            "signal_contract": "locked_edge_margin_target8_train_only(학습 전용 고정 엣지 마진 목표8)",
        })
    return rows


def density_audit_rows(
    full: pd.DataFrame,
    label_signal: np.ndarray,
    argmax_signal: np.ndarray,
    threshold_signal: np.ndarray,
    variant: EdgeQualityVariant,
    candidate_id: str,
    model_id: str,
    model_instance_id: str,
    threshold: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        mask = full["split"].astype(str).eq(split).to_numpy()
        timestamps = pd.to_datetime(full.loc[mask, "timestamp"], errors="raise").reset_index(drop=True)
        days = f12b.scout.count_scope_days(timestamps) if len(timestamps) else 0
        for kind, signal in (
            ("label_oracle(라벨 오라클)", label_signal),
            ("argmax_baseline(최대확률 기준선)", argmax_signal),
            ("edge_margin_target8(엣지 마진 목표8)", threshold_signal),
        ):
            split_signal = signal[mask]
            trade_count = int((split_signal != 0).sum())
            rows.append({
                "candidate_id": candidate_id,
                "target_id": variant.variant_id,
                "model_id": model_id,
                "model_instance_id": model_instance_id,
                "split": split,
                "signal_kind": kind,
                "cell_id": PRIMARY_CELL_ID if "edge_margin" in kind else "",
                "threshold_value": threshold if "edge_margin" in kind else "",
                "days_in_scope": days,
                "trade_count": trade_count,
                "trades_per_day": float(trade_count / days) if days else 0.0,
                "long_trade_count": int((split_signal == 1).sum()),
                "short_trade_count": int((split_signal == -1).sum()),
                "flat_count": int((split_signal == 0).sum()),
            })
    return rows


def score_contract_manifest_rows() -> list[dict[str, Any]]:
    return [{
        "score_contract_id": "edge_margin",
        "cell_id": PRIMARY_CELL_ID,
        "target_density_per_day": 8,
        "is_primary_cell": True,
        "score_expression": "max(p_short, p_long) - p_flat",
        "threshold_fit_policy": "train_probability_scores_plus_train_calendar_only(학습 확률 점수와 학습 달력만 사용)",
        "selection_rule": "locked_single_policy_no_grid(고정 단일 정책, 격자 없음)",
    }]


def build_candidate_summary(
    model_metrics: list[dict[str, Any]],
    subperiod_metrics: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
    classification_rows: list[dict[str, Any]],
    threshold_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    summaries = f12b.build_candidate_summary(model_metrics, subperiod_metrics, parity_rows, classification_rows)
    threshold_by_candidate = {str(row["candidate_id"]): row for row in threshold_rows}
    enriched: list[dict[str, Any]] = []
    for row in summaries:
        threshold = threshold_by_candidate.get(str(row["candidate_id"]), {})
        density_controlled = (
            SCOUT_DENSITY_LOW <= float(row.get("validation_trades_per_day", 0.0)) <= SCOUT_DENSITY_HIGH
            and SCOUT_DENSITY_LOW <= float(row.get("oos_trades_per_day", 0.0)) <= SCOUT_DENSITY_HIGH
        )
        pf_axis_improved = (
            float(row.get("validation_profit_factor", 0.0)) > F15_PRIMARY_VALIDATION_PF
            and float(row.get("oos_profit_factor", 0.0)) > F15_PRIMARY_OOS_PF
        )
        dd_axis_improved = (
            float(row.get("validation_dd_risk_percent", 999.0)) < F15_PRIMARY_VALIDATION_DD
            and float(row.get("oos_dd_risk_percent", 999.0)) < F15_PRIMARY_OOS_DD
        )
        row.update({
            "score_contract_id": "edge_margin",
            "cell_id": PRIMARY_CELL_ID,
            "target_density_per_day": 8,
            "is_primary_cell": True,
            "threshold_value": threshold.get("threshold_value", ""),
            "actual_train_selected_density_per_day": threshold.get("actual_train_selected_density_per_day", ""),
            "target_train_trade_count": threshold.get("target_train_trade_count", ""),
            "actual_train_selected_count": threshold.get("actual_train_selected_count", ""),
            "density_controlled_validation_oos": bool(density_controlled),
            "pf_axis_improved_vs_f15_primary": bool(pf_axis_improved),
            "dd_axis_improved_vs_f15_primary": bool(dd_axis_improved),
            "raw_strict_scout_clue_pass": bool(row.get("strict_scout_clue_pass")),
            "strict_scout_clue_pass_for_forward": bool(row.get("strict_scout_clue_pass")),
            "preserved_clue_pass": bool(row.get("preserved_clue_pass") or (row.get("parity_passed") and density_controlled and (pf_axis_improved or dd_axis_improved))),
            "signal_contract": "locked_edge_margin_target8_train_only(학습 전용 고정 엣지 마진 목표8)",
        })
        enriched.append(row)
    enriched.sort(key=lambda item: (
        not bool(item["strict_scout_clue_pass"]),
        not bool(item["preserved_clue_pass"]),
        float(item.get("shape_duration_score", 999999.0)),
    ))
    return json_ready(enriched)


def build_final(
    created_at: str,
    result: dict[str, Any],
    variants: list[EdgeQualityVariant],
    source_integrity: dict[str, Any],
    feature_order: list[str],
    stage_open: dict[str, Any],
) -> dict[str, Any]:
    candidate_summary = result["candidate_summary"]
    strict_rows = [row for row in candidate_summary if row.get("strict_scout_clue_pass")]
    preserved_rows = [row for row in candidate_summary if row.get("preserved_clue_pass")]
    best = candidate_summary[0] if candidate_summary else {}
    if strict_rows:
        status = "edge_quality_risk_veto_strict_scout_clue_no_authority"
        judgment = "strict_scout_clue_candidate(엄격 탐색 단서 후보)"
        next_run_id = NEXT_STRICT_RUN_ID
    elif preserved_rows:
        status = "edge_quality_risk_veto_preserved_clue_no_authority"
        judgment = "preserved_clue_candidate(보존 단서 후보)"
        next_run_id = NEXT_REPAIR_RUN_ID
    else:
        status = "edge_quality_risk_veto_no_strict_clue_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run_id = NEXT_REPAIR_RUN_ID
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
        "score_cell_count": 1,
        "stage_open_status": stage_open.get("status", ""),
        "source_integrity": source_integrity,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "data_integrity": data_integrity_record(source_integrity),
        "model_validation": model_validation_record(best),
        "artifact_lineage": artifact_lineage_record(),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "wfo_status": "not_run_requires_grok_pre_expensive_if_strict(엄격 단서가 있으면 Grok 비싼 검증 전 검토 필요)",
        "mt5_status": "not_run_proxy_only_no_runtime_authority(프록시 전용, 런타임 권위 없음)",
    }


def data_integrity_record(source_integrity: dict[str, Any]) -> dict[str, Any]:
    return {
        "data_source": f03b.DATASET_PATH.as_posix(),
        "time_axis": "US100 M5 closed-bar timestamp order(US100 5분봉 확정봉 시각 순서)",
        "sample_scope": "Tier A train/validation/OOS fixed split(티어 A 학습/검증/표본밖 고정 분할)",
        "feature_label_boundary": "features use closed bars; labels use future path as supervised target only(피처는 확정봉, 라벨은 미래 경로를 감독 목표로만 사용)",
        "threshold_boundary": "thresholds fit on train probability scores and train calendar only(임계값은 학습 확률 점수와 학습 달력만 사용)",
        "leakage_risk": "validation/OOS threshold calibration is forbidden(검증/표본밖 임계값 보정 금지)",
        "data_hash_or_identity": source_integrity,
        "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
    }


def model_validation_record(best: dict[str, Any]) -> dict[str, Any]:
    return {
        "model_family": "fixed sklearn-to-ONNX probability tensor(고정 sklearn-to-ONNX 확률 텐서)",
        "target_and_label": "risk-quality path label with adverse excursion veto(역행폭 배제 위험 품질 경로 라벨)",
        "split_method": "fixed train/validation/OOS split(고정 학습/검증/표본밖 분할)",
        "selection_metric": "locked edge_margin target8 strict clue(고정 엣지 마진 목표8 엄격 단서)",
        "threshold_policy": "single train-only threshold, no grid(단일 학습 전용 임계값, 격자 없음)",
        "overfit_risk": "label variants pre-registered and decision policy locked(라벨 변형 사전 등록 및 결정 정책 고정)",
        "comparison_baseline": "argmax baseline rows and F15 primary reference(최대확률 기준선 행과 F15 1순위 참조)",
        "validation_judgment": "exploratory(탐색)",
        "best_candidate": best.get("candidate_id", "none"),
    }


def artifact_lineage_record() -> dict[str, Any]:
    return {
        "source_inputs": [f03b.DATASET_PATH.as_posix(), f03b.FEATURE_ORDER_PATH.as_posix(), STAGE_OPEN_SUMMARY.as_posix()],
        "producer": SCRIPT_PATH.as_posix(),
        "consumer": REPORT_PATH.as_posix(),
        "availability": "generated_ignored_with_manifest_for_models(모델은 생성되고 목록으로 추적)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
    }


def write_artifacts(
    result: dict[str, Any],
    final: dict[str, Any],
    variants: list[EdgeQualityVariant],
) -> dict[str, Path]:
    artifacts = {
        "variant_manifest": RUN_ROOT / "variant_manifest.csv",
        "score_contract_manifest": RUN_ROOT / "score_contract_manifest.csv",
        "threshold_manifest": RUN_ROOT / "threshold_manifest.csv",
        "label_distribution": RUN_ROOT / "label_distribution.csv",
        "argmax_baseline_metrics": RUN_ROOT / "argmax_baseline_metrics.csv",
        "model_metrics": RUN_ROOT / "model_metrics.csv",
        "subperiod_metrics": RUN_ROOT / "subperiod_metrics.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "candidate_summary": RUN_ROOT / "candidate_summary.csv",
        "density_transfer_audit": RUN_ROOT / "density_transfer_audit.csv",
        "target_diagnostics": RUN_ROOT / "target_diagnostics.json",
        "skipped": RUN_ROOT / "skipped.csv",
        "final_decision": RUN_ROOT / "final_decision.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_csv(artifacts["variant_manifest"], [asdict(variant) for variant in variants])
    write_csv(artifacts["score_contract_manifest"], result["score_contract_manifest"])
    write_csv(artifacts["threshold_manifest"], result["threshold_manifest"])
    write_csv(artifacts["label_distribution"], result["label_distribution"])
    write_csv(artifacts["argmax_baseline_metrics"], result["argmax_baseline_metrics"])
    write_csv(artifacts["model_metrics"], result["model_metrics"])
    write_csv(artifacts["subperiod_metrics"], result["subperiod_metrics"])
    write_csv(artifacts["classification_metrics"], result["classification_metrics"])
    write_csv(artifacts["onnx_parity"], result["onnx_parity"])
    write_csv(artifacts["candidate_summary"], result["candidate_summary"])
    write_csv(artifacts["density_transfer_audit"], result["density_transfer_audit"])
    write_csv(artifacts["skipped"], result["skipped"])
    write_json(artifacts["target_diagnostics"], result["target_diagnostics"])
    write_json(artifacts["final_decision"], final)
    write_json(artifacts["run_manifest"], {
        **final,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "stage_open_summary": artifact_identity(STAGE_OPEN_SUMMARY),
        "dataset": artifact_identity(f03b.DATASET_PATH),
        "feature_order": artifact_identity(f03b.FEATURE_ORDER_PATH),
        "artifacts": {key: path.as_posix() for key, path in artifacts.items()},
    })
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    text = f"""# Frontier16B Edge Quality Risk Veto Proxy Scout(프론티어16B 엣지 품질 위험 배제 프록시 탐색)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): 3개 risk-quality label variants(위험 품질 라벨 변형)를 학습하고 `{PRIMARY_CELL_ID}` 단일 decision cell(결정 칸)로 평가했습니다.

Effect(효과): F15(프론티어15)의 density transfer(빈도 전이)를 calibration clue(보정 단서)로만 쓰며, PF/DD/smoothness(수익 팩터/손실폭/매끄러움)가 함께 좋아지는지 확인했습니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `{final['candidate_row_count']}`
- strict rows(엄격 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- best candidate(최고 후보): `{best.get('candidate_id', 'none')}`
- validation PF/density/DD(검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- worst subperiod DD(최악 하위기간 손실폭): `{fmt(best.get('validation_oos_subperiod_worst_dd_risk_percent'))}%`

## Artifacts(산출물)

- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- threshold manifest(임계값 목록): `{artifacts['threshold_manifest'].as_posix()}`
- density transfer audit(빈도 전이 감사): `{artifacts['density_transfer_audit'].as_posix()}`
- argmax baseline metrics(최대확률 기준선 지표): `{artifacts['argmax_baseline_metrics'].as_posix()}`
- ONNX parity(온엑스 동등성): `{artifacts['onnx_parity'].as_posix()}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""
    f03b.write_text_sig(REPORT_PATH, text)


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(final))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(final, artifacts))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(final))
    upsert_csv_io(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    for row in ledger_rows(final):
        upsert_csv_io(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv_io(stage_ledger, "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): strict rows(엄격 행) `{final['strict_scout_clue_rows']}`, preserved rows(보존 행) `{final['preserved_clue_rows']}`, next run(다음 실행) `{final['next_run_id']}`.\n",
    )


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

Action(행동): Frontier16B(프론티어16B)가 locked edge_margin target8(고정 엣지 마진 목표8) proxy scout(프록시 탐색)를 실행했습니다.

Effect(효과): best candidate(최고 후보) `{best.get('candidate_id', 'none')}`의 PF-density-DD(수익 팩터-빈도-손실폭)를 기록했고, 같은 단계 안에서 score grid(점수 격자)를 확장하지 않았습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_candidate_row"]
    return f"""# Frontier16 Selection Status(프론티어16 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Latest run(최근 실행): `{RUN_ID}`

Best candidate(최고 후보): `{best.get('candidate_id', 'none')}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next action(다음 행동): `{final['next_run_id']}`

Key artifacts(핵심 산출물): `{artifacts['candidate_summary'].as_posix()}`, `{artifacts['density_transfer_audit'].as_posix()}`
"""


def review_index(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier16 Review Index(프론티어16 검토 색인)

Updated(갱신): {final['created_at_utc']}

- `{PARENT_RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용), guard manifest(가드 목록) registered(등록됨).
- `{RUN_ID}`: proxy scout(프록시 탐색), strict rows(엄격 행) `{final['strict_scout_clue_rows']}`, preserved rows(보존 행) `{final['preserved_clue_rows']}`.
- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier16B Required Gate Coverage Audit(프론티어16B 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- scope_completion_gate(범위 완료 게이트): 3 label variants(라벨 변형) x 3 model specs(모델 규격) x 1 locked cell(고정 칸) executed(실행됨).
- kpi_contract_audit(KPI 계약 감사): validation/OOS PF-density-DD and subperiod DD(검증/표본밖 수익 팩터-빈도-손실폭과 하위기간 손실폭) recorded(기록됨).
- data_integrity_gate(데이터 무결성 게이트): `{final['data_integrity']['integrity_judgment']}`
- model_validation_gate(모델 검증 게이트): `{final['model_validation']['validation_judgment']}`
- artifact_lineage_gate(산출물 계보 게이트): `{final['artifact_lineage']['lineage_judgment']}`
- tier_pair_gate(티어 쌍 게이트): Tier A separate(티어 A 분리) recorded(기록됨); Tier B/combined(티어 B/합산)은 missing_required(필수 누락)로 기록됨.
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음)
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "edge_quality_risk_veto_proxy_scout(엣지 품질 위험 배제 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};locked_cell={PRIMARY_CELL_ID};no_wfo_no_mt5_no_authority",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": "proxy_scout_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "primary_kpi": primary_kpi_text(final["best_candidate_row"]),
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "result_path": REPORT_PATH.as_posix(),
        "final_decision_path": artifacts["final_decision"].as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_candidate_row"]
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "edge_quality_risk_veto_proxy_scout(엣지 품질 위험 배제 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "locked_single_cell_train_only_threshold_no_wfo_no_mt5_no_authority(고정 단일 칸 학습 전용 임계값, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_edge_quality_proxy",
            "subrun_id": f"{RUN_ID}__tier_a_edge_quality_proxy",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "edge_quality_proxy_not_runtime(엣지 품질 프록시, 런타임 아님)",
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
            "primary_kpi": "missing_required_no_paired_source(필수 누락, 쌍 원천 없음)",
            "notes": "Tier B paired materialization not available(티어 B 쌍 물질화 없음)",
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
        f"cell={best.get('cell_id', '')};"
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
    header = read_csv_header_io(template_path)
    csv_path(path.parent).mkdir(parents=True, exist_ok=True)
    with csv_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def read_csv_header_io(path: Path) -> list[str]:
    with csv_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv_io(path: Path, key: str, row: dict[str, Any]) -> None:
    header = read_csv_header_io(path)
    rows: list[dict[str, str]] = []
    with csv_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for existing in csv.DictReader(handle):
            rows.append(dict(existing))
    normalized = {column: f03b.stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    csv_path(path.parent).mkdir(parents=True, exist_ok=True)
    with csv_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: f03b.stringify(item.get(column, "")) for column in header})


def csv_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32" and len(str(resolved)) >= 240:
        return io_path(path)
    return resolved


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
