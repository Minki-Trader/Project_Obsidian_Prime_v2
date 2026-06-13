from __future__ import annotations

import csv
import json
import math
import re
import sys
from dataclasses import dataclass
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
from stage_pipelines.stage_frontier_04 import frontier04b_path_aware_label_proxy_scout as f04b
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d


STAGE_ID = "stage_frontier_07__adverse_excursion_risk_shaped_labeling"
RUN_ID = "frontier07B_adverse_excursion_risk_label_proxy_scout_v1"
RUN_NUMBER = "frontier07B"
PARENT_RUN_ID = "frontier07A_stage_open_adverse_excursion_risk_shaped_labeling_v1"
NEXT_CLUE_RUN_ID = "frontier07C_grok_pre_expensive_risk_label_review_v1"
NEXT_REPAIR_RUN_ID = "frontier07C_risk_label_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"

F04D_REPORT = Path(
    "stages/stage_frontier_04__path_aware_cost_dd_event_labeling/"
    "03_reviews/frontier04D_trainable_path_label_onnx_probe_v1_report.md"
)
F06B_REPORT = Path(
    "stages/stage_frontier_06__selective_probability_abstention_signal_contract/"
    "03_reviews/frontier06B_selective_probability_abstention_signal_scout_v1_report.md"
)

LABEL_ORDER = f04d.LABEL_ORDER
LABEL_NAMES = f04d.LABEL_NAMES
HORIZON_BARS = 12
SCALE_QUANTILE = 0.90
SCOUT_DENSITY_LOW = 5.0
SCOUT_DENSITY_HIGH = 10.0
SCOUT_PF_FLOOR = 1.2
SCOUT_DD_SOFT_CEILING = 15.0
CLASS_BALANCE_MIN = 0.05
CLASS_BALANCE_MAX = 0.90
LEARNABILITY_VAL_BAL_ACC_FLOOR = 0.30
LEARNABILITY_VAL_MACRO_F1_FLOOR = 0.20
LEARNABILITY_TRANSFER_GAP_CEILING = 0.25

MODEL_ID_SHORT = {
    "logreg_l2_c0p5_plain_argmax": "lr_plain",
    "logreg_l2_c0p5_balanced_argmax": "lr_bal",
    "rf_depth5_leaf80_balanced_argmax": "rf_bal",
}


@dataclass(frozen=True)
class RiskLabelVariant:
    variant_id: str
    family_id: str
    family_semantics: str
    difference_from_f04: str
    horizon_bars: int
    scale_quantile: float
    base_scale_log_return: float
    long_target_multiplier: float
    short_target_multiplier: float
    long_cap_multiplier: float
    short_cap_multiplier: float
    score_threshold: float
    long_target_log_return: float
    short_target_log_return: float
    long_cap_log_return: float
    short_cap_log_return: float


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    full, raw, source_integrity = load_training_packet()
    feature_order = f04d.read_feature_order()
    variants = build_variants(full, raw)
    result = train_and_evaluate(full, raw, feature_order, variants)
    final = build_final(result, source_integrity, feature_order, variants)
    artifacts = write_artifacts(result, final, variants)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "strict_scout_clue_rows": final["strict_scout_clue_rows"],
        "preserved_clue_rows": final["preserved_clue_rows"],
        "best_candidate": final["best_candidate_row"].get("candidate_id"),
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def load_training_packet() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    aligned, raw, source_integrity = f04b.load_and_align()
    full = pd.read_parquet(io_path(f03b.DATASET_PATH)).sort_values("timestamp").reset_index(drop=True)
    required = {"timestamp", "split", "label", "label_class", "future_log_return_12"}
    missing = sorted(required - set(full.columns))
    if missing:
        raise RuntimeError(f"Dataset missing required columns: {missing}")
    full = full.merge(aligned[["timestamp", "raw_index"]], on="timestamp", how="left", validate="one_to_one")
    if full["raw_index"].isna().any():
        raise RuntimeError("Full model input failed raw_index merge.")
    full["raw_index"] = full["raw_index"].astype("int64")
    return full, raw, source_integrity


def build_variants(full: pd.DataFrame, raw: pd.DataFrame) -> list[RiskLabelVariant]:
    raw_indexes = full["raw_index"].astype("int64").to_numpy()
    log_close = raw["log_close"].to_numpy(dtype="float64")
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    fwd = log_close[raw_indexes + HORIZON_BARS] - log_close[raw_indexes]
    base_scale = float(np.nanquantile(np.abs(fwd[train_mask]), SCALE_QUANTILE))
    specs = [
        (
            "mae_mfe_balance",
            "MFE must clear target while MAE stays under cap(최대 유리 이동은 목표를 넘고 최대 불리 이동은 상한 아래여야 함)",
            "F04 is event-first target/stop; this scores survival before choosing direction(F04는 이벤트 우선 목표/손절이고, 여기는 생존 점수로 방향 선택)",
            [(1.00, 1.00, 0.45, 0.45, 0.45), (1.10, 1.10, 0.60, 0.60, 0.50), (1.25, 1.25, 0.75, 0.75, 0.60)],
        ),
        (
            "recovery_close_survival",
            "Close recovery must agree with bounded adverse path(종가 회복이 제한된 불리 경로와 일치해야 함)",
            "F04 labels first touch; this requires final recovery plus bounded path(F04는 첫 터치 라벨이고, 여기는 종가 회복과 경로 제한을 함께 요구)",
            [(0.75, 0.75, 0.55, 0.55, 0.35), (0.90, 0.90, 0.65, 0.65, 0.40), (1.10, 1.10, 0.75, 0.75, 0.45)],
        ),
        (
            "time_to_adverse_penalty",
            "Early adverse movement lowers the label score(초기 불리 이동은 라벨 점수를 낮춤)",
            "F04 treats stop hit as event; this grades how quickly adverse movement appears(F04는 손절 도달을 이벤트로 다루고, 여기는 불리 이동 속도를 점수화)",
            [(0.90, 0.90, 0.60, 0.60, 0.55), (1.05, 1.05, 0.70, 0.70, 0.65), (1.20, 1.20, 0.80, 0.80, 0.75)],
        ),
        (
            "side_asymmetric_caps",
            "Long and short receive different adverse caps(롱과 숏에 다른 불리 이동 상한 부여)",
            "F04 uses symmetric target/stop pairs; this tests side-specific loss shape(F04는 대칭 목표/손절 쌍이고, 여기는 방향별 손실 형상 시험)",
            [(1.00, 1.00, 0.55, 0.70, 0.50), (1.10, 0.90, 0.65, 0.55, 0.50), (0.90, 1.15, 0.50, 0.75, 0.55)],
        ),
    ]
    variants: list[RiskLabelVariant] = []
    for family_id, semantics, delta, family_specs in specs:
        for index, (long_target, short_target, long_cap, short_cap, score_threshold) in enumerate(family_specs, start=1):
            variant_id = (
                f"f07b_{family_id}_v{index}_"
                f"lt{long_target:.2f}_st{short_target:.2f}_lc{long_cap:.2f}_sc{short_cap:.2f}_q{int(SCALE_QUANTILE * 100)}"
            ).replace(".", "p")
            variants.append(
                RiskLabelVariant(
                    variant_id=variant_id,
                    family_id=family_id,
                    family_semantics=semantics,
                    difference_from_f04=delta,
                    horizon_bars=HORIZON_BARS,
                    scale_quantile=SCALE_QUANTILE,
                    base_scale_log_return=base_scale,
                    long_target_multiplier=long_target,
                    short_target_multiplier=short_target,
                    long_cap_multiplier=long_cap,
                    short_cap_multiplier=short_cap,
                    score_threshold=score_threshold,
                    long_target_log_return=base_scale * long_target,
                    short_target_log_return=base_scale * short_target,
                    long_cap_log_return=base_scale * long_cap,
                    short_cap_log_return=base_scale * short_cap,
                )
            )
    return variants


def train_and_evaluate(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    feature_order: list[str],
    variants: list[RiskLabelVariant],
) -> dict[str, Any]:
    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values.")
    path = path_arrays(full, raw, HORIZON_BARS)
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    sample_indices = np.concatenate([
        np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())[:256]
        for split in ("train", "validation", "oos")
    ])

    reference_metrics: list[dict[str, Any]] = []
    candidate_metrics: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    label_distribution_rows: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []

    label_v1_labels = pd.to_numeric(full["label_class"], errors="raise").to_numpy(dtype="int64")
    label_v1_rows = fit_label_target(
        full=full,
        x_all=x_all,
        labels=label_v1_labels,
        fwd_return=path["fwd_return"],
        variant=None,
        target_id="label_v1_argmax_reference",
        target_kind="reference_label_v1_argmax(참조 label_v1 최대확률)",
        train_mask=train_mask,
        sample_indices=sample_indices,
        model_prefix="ref_labelv1",
        model_dir=MODEL_DIR / "references",
        metric_rows=reference_metrics,
        classification_rows=classification_rows,
        parity_rows=parity_rows,
        skipped_rows=skipped_rows,
    )
    label_distribution_rows.extend(label_distribution(full, label_v1_labels, "label_v1_argmax_reference", "reference(참조)"))

    for variant_index, variant in enumerate(variants, start=1):
        labels, signal, diagnostics = build_risk_labels(path, variant)
        label_distribution_rows.extend(label_distribution(full, labels, variant.variant_id, "risk_label_candidate(위험 라벨 후보)"))
        oracle_metric_rows = evaluate_signal_rows(
            full,
            signal,
            path["fwd_return"],
            variant,
            "oracle_label_replay(오라클 라벨 재생)",
            "oracle_risk_label(오라클 위험 라벨)",
        )
        candidate_metrics.extend(oracle_metric_rows)
        fit_label_target(
            full=full,
            x_all=x_all,
            labels=labels,
            fwd_return=path["fwd_return"],
            variant=variant,
            target_id=variant.variant_id,
            target_kind="risk_label_candidate(위험 라벨 후보)",
            train_mask=train_mask,
            sample_indices=sample_indices,
            model_prefix=f"v{variant_index:02d}",
            model_dir=MODEL_DIR / f"v{variant_index:02d}",
            metric_rows=candidate_metrics,
            classification_rows=classification_rows,
            parity_rows=parity_rows,
            skipped_rows=skipped_rows,
            extra={f"diagnostic_{key}": value for key, value in diagnostics.items()},
        )

    references = build_reference_pack(label_v1_rows, reference_metrics)
    candidate_summary = build_candidate_summary(candidate_metrics, classification_rows, parity_rows, references)
    return {
        "reference_metrics": reference_metrics,
        "candidate_metrics": candidate_metrics,
        "classification_metrics": classification_rows,
        "onnx_parity": parity_rows,
        "label_distribution": label_distribution_rows,
        "skipped": skipped_rows,
        "candidate_summary": candidate_summary,
        "references": references,
    }


def path_arrays(full: pd.DataFrame, raw: pd.DataFrame, horizon: int) -> dict[str, np.ndarray]:
    raw_indexes = full["raw_index"].astype("int64").to_numpy()
    base = raw["log_close"].to_numpy(dtype="float64")[raw_indexes]
    log_close = raw["log_close"].to_numpy(dtype="float64")
    log_high = raw["log_high"].to_numpy(dtype="float64")
    log_low = raw["log_low"].to_numpy(dtype="float64")
    high_steps = np.vstack([log_high[raw_indexes + step] - base for step in range(1, horizon + 1)])
    low_steps = np.vstack([base - log_low[raw_indexes + step] for step in range(1, horizon + 1)])
    fwd_return = log_close[raw_indexes + horizon] - base
    return {
        "long_mfe": np.nanmax(high_steps, axis=0),
        "long_mae": np.nanmax(low_steps, axis=0),
        "short_mfe": np.nanmax(low_steps, axis=0),
        "short_mae": np.nanmax(high_steps, axis=0),
        "fwd_return": fwd_return,
        "high_steps": high_steps,
        "low_steps": low_steps,
    }


def build_risk_labels(path: dict[str, np.ndarray], variant: RiskLabelVariant) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    family = variant.family_id
    if family == "mae_mfe_balance":
        long_score = path["long_mfe"] / variant.long_target_log_return - 0.75 * path["long_mae"] / variant.long_cap_log_return
        short_score = path["short_mfe"] / variant.short_target_log_return - 0.75 * path["short_mae"] / variant.short_cap_log_return
        long_ok = (path["long_mfe"] >= variant.long_target_log_return) & (path["long_mae"] <= variant.long_cap_log_return) & (long_score >= variant.score_threshold)
        short_ok = (path["short_mfe"] >= variant.short_target_log_return) & (path["short_mae"] <= variant.short_cap_log_return) & (short_score >= variant.score_threshold)
    elif family == "recovery_close_survival":
        recovery_floor_long = 0.25 * variant.long_target_log_return
        recovery_floor_short = 0.25 * variant.short_target_log_return
        long_score = path["fwd_return"] / variant.long_target_log_return + 0.50 * (1.0 - path["long_mae"] / variant.long_cap_log_return)
        short_score = -path["fwd_return"] / variant.short_target_log_return + 0.50 * (1.0 - path["short_mae"] / variant.short_cap_log_return)
        long_ok = (path["long_mfe"] >= variant.long_target_log_return) & (path["fwd_return"] >= recovery_floor_long) & (path["long_mae"] <= variant.long_cap_log_return) & (long_score >= variant.score_threshold)
        short_ok = (path["short_mfe"] >= variant.short_target_log_return) & (path["fwd_return"] <= -recovery_floor_short) & (path["short_mae"] <= variant.short_cap_log_return) & (short_score >= variant.score_threshold)
    elif family == "time_to_adverse_penalty":
        long_penalty = adverse_time_penalty(path["low_steps"], variant.long_cap_log_return)
        short_penalty = adverse_time_penalty(path["high_steps"], variant.short_cap_log_return)
        long_score = path["long_mfe"] / variant.long_target_log_return - 0.60 * path["long_mae"] / variant.long_cap_log_return - 0.50 * long_penalty
        short_score = path["short_mfe"] / variant.short_target_log_return - 0.60 * path["short_mae"] / variant.short_cap_log_return - 0.50 * short_penalty
        long_ok = (path["long_mfe"] >= variant.long_target_log_return) & (long_score >= variant.score_threshold)
        short_ok = (path["short_mfe"] >= variant.short_target_log_return) & (short_score >= variant.score_threshold)
    elif family == "side_asymmetric_caps":
        long_score = path["long_mfe"] / variant.long_target_log_return - path["long_mae"] / variant.long_cap_log_return
        short_score = path["short_mfe"] / variant.short_target_log_return - path["short_mae"] / variant.short_cap_log_return
        long_ok = (path["long_mfe"] >= variant.long_target_log_return) & (path["long_mae"] <= variant.long_cap_log_return) & (long_score >= variant.score_threshold)
        short_ok = (path["short_mfe"] >= variant.short_target_log_return) & (path["short_mae"] <= variant.short_cap_log_return) & (short_score >= variant.score_threshold)
    else:
        raise ValueError(f"Unknown family: {family}")

    signal = np.zeros(len(path["fwd_return"]), dtype="int8")
    signal[long_ok & (long_score > short_score + 1e-12)] = 1
    signal[short_ok & (short_score > long_score + 1e-12)] = -1
    labels = np.where(signal < 0, 0, np.where(signal > 0, 2, 1)).astype("int64")
    diagnostics = {
        "oracle_long_count": int((signal == 1).sum()),
        "oracle_short_count": int((signal == -1).sum()),
        "oracle_flat_count": int((signal == 0).sum()),
        "mean_long_score": float(np.nanmean(long_score)),
        "mean_short_score": float(np.nanmean(short_score)),
    }
    return labels, signal, diagnostics


def adverse_time_penalty(step_values: np.ndarray, cap: float) -> np.ndarray:
    horizon, rows = step_values.shape
    first_hit = np.full(rows, horizon + 1, dtype="float64")
    for index in range(horizon):
        hit = (first_hit > horizon) & (step_values[index] >= cap)
        first_hit[hit] = index + 1
    penalty = np.zeros(rows, dtype="float64")
    hit = first_hit <= horizon
    penalty[hit] = (horizon + 1 - first_hit[hit]) / horizon
    return penalty


def fit_label_target(
    *,
    full: pd.DataFrame,
    x_all: np.ndarray,
    labels: np.ndarray,
    fwd_return: np.ndarray,
    variant: RiskLabelVariant | None,
    target_id: str,
    target_kind: str,
    train_mask: np.ndarray,
    sample_indices: np.ndarray,
    model_prefix: str,
    model_dir: Path,
    metric_rows: list[dict[str, Any]],
    classification_rows: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
    skipped_rows: list[dict[str, Any]],
    extra: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    train_classes = set(int(value) for value in labels[train_mask])
    missing = sorted(set(LABEL_ORDER) - train_classes)
    if missing:
        skipped_rows.append({
            "target_id": target_id,
            "target_kind": target_kind,
            "reason": f"missing_train_classes={missing}",
        })
        return []
    target_metric_rows: list[dict[str, Any]] = []
    for spec in f04d.MODEL_SPECS:
        short_model_id = MODEL_ID_SHORT.get(spec.model_id, spec.model_id[:12])
        model_instance_id = f"{model_prefix}_{short_model_id}"
        model = clone(spec.estimator)
        model.fit(x_all[train_mask], labels[train_mask])
        probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
        pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
        model_signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")

        io_path(model_dir).mkdir(parents=True, exist_ok=True)
        model_path = model_dir / f"{model_instance_id}.joblib"
        onnx_path = model_dir / f"{model_instance_id}.onnx"
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
        parity_rows.append({
            "target_id": target_id,
            "target_kind": target_kind,
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
        })
        for split in ("train", "validation", "oos"):
            split_mask = full["split"].astype(str).eq(split).to_numpy()
            y_true = labels[split_mask]
            y_pred = pred_label[split_mask]
            classification_rows.append({
                "target_id": target_id,
                "target_kind": target_kind,
                "model_id": spec.model_id,
                "model_instance_id": model_instance_id,
                "split": split,
                "rows": int(split_mask.sum()),
                "accuracy": float(accuracy_score(y_true, y_pred)),
                "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
                "macro_f1": float(f1_score(y_true, y_pred, labels=LABEL_ORDER, average="macro", zero_division=0)),
                "pred_short": int((y_pred == 0).sum()),
                "pred_flat": int((y_pred == 1).sum()),
                "pred_long": int((y_pred == 2).sum()),
                "true_short": int((y_true == 0).sum()),
                "true_flat": int((y_true == 1).sum()),
                "true_long": int((y_true == 2).sum()),
            })
        metric = evaluate_model_signal(full, model_signal, fwd_return, variant, target_id, target_kind, spec.model_id, model_instance_id)
        for row in metric:
            if extra:
                row.update(extra)
            metric_rows.append(row)
            target_metric_rows.append(row)
    return target_metric_rows


def evaluate_model_signal(
    full: pd.DataFrame,
    signal: np.ndarray,
    fwd_return: np.ndarray,
    variant: RiskLabelVariant | None,
    target_id: str,
    target_kind: str,
    model_id: str,
    model_instance_id: str,
) -> list[dict[str, Any]]:
    rows = []
    for split in ("train", "validation", "oos"):
        metric = f04b.evaluate_split(
            full,
            signal,
            fwd_return,
            split,
            metric_variant(variant, target_id),
            f"argmax_model_{target_id}(최대확률 모델 {target_id})",
            np.full(len(full), f"argmax_model_{target_id}(최대확률 모델)", dtype=object),
            np.zeros(len(full), dtype="int16"),
        )
        metric.update({
            "target_id": target_id,
            "target_kind": target_kind,
            "model_id": model_id,
            "model_instance_id": model_instance_id,
            "signal_contract": "argmax_only_no_threshold(최대확률 전용, 임계값 없음)",
            "label_family": variant.family_id if variant else "label_v1_reference",
            "family_semantics": variant.family_semantics if variant else "original_label_v1_reference(원래 라벨 v1 참조)",
            "difference_from_f04": variant.difference_from_f04 if variant else "not_applicable_reference(참조라 해당 없음)",
        })
        rows.append(metric)
    return rows


def evaluate_signal_rows(
    full: pd.DataFrame,
    signal: np.ndarray,
    fwd_return: np.ndarray,
    variant: RiskLabelVariant,
    target_kind: str,
    model_id: str,
) -> list[dict[str, Any]]:
    rows = []
    for split in ("train", "validation", "oos"):
        metric = f04b.evaluate_split(
            full,
            signal,
            fwd_return,
            split,
            metric_variant(variant, variant.variant_id),
            f"{target_kind}_{variant.variant_id}",
            np.full(len(full), f"{target_kind}_{variant.variant_id}", dtype=object),
            np.zeros(len(full), dtype="int16"),
        )
        metric.update({
            "target_id": variant.variant_id,
            "target_kind": target_kind,
            "model_id": model_id,
            "model_instance_id": "oracle_no_model(오라클, 모델 없음)",
            "signal_contract": "oracle_label_replay_not_runtime(오라클 라벨 재생, 런타임 아님)",
            "label_family": variant.family_id,
            "family_semantics": variant.family_semantics,
            "difference_from_f04": variant.difference_from_f04,
        })
        rows.append(metric)
    return rows


def metric_variant(variant: RiskLabelVariant | None, target_id: str) -> f04b.PathVariant:
    if variant is None:
        return f04b.PathVariant(
            variant_id=target_id,
            horizon_bars=HORIZON_BARS,
            target_multiplier=1.0,
            stop_multiplier=1.0,
            scale_quantile=SCALE_QUANTILE,
            target_log_return=1.0,
            stop_log_return=1.0,
            base_scale_log_return=1.0,
        )
    return f04b.PathVariant(
        variant_id=variant.variant_id,
        horizon_bars=variant.horizon_bars,
        target_multiplier=max(variant.long_target_multiplier, variant.short_target_multiplier),
        stop_multiplier=max(variant.long_cap_multiplier, variant.short_cap_multiplier),
        scale_quantile=variant.scale_quantile,
        target_log_return=max(variant.long_target_log_return, variant.short_target_log_return),
        stop_log_return=max(variant.long_cap_log_return, variant.short_cap_log_return),
        base_scale_log_return=variant.base_scale_log_return,
    )


def build_reference_pack(label_v1_rows: list[dict[str, Any]], reference_metrics: list[dict[str, Any]]) -> dict[str, Any]:
    label_v1 = pd.DataFrame(reference_metrics)
    argmax_rows = label_v1[label_v1["target_id"].eq("label_v1_argmax_reference")].copy()
    label_v1_best = best_model_summary(argmax_rows, "label_v1_argmax_reference")
    return {
        "label_v1_argmax": label_v1_best,
        "frontier04_locked_path_trainable": parse_report_reference(F04D_REPORT, "frontier04D_locked_path_argmax_reference"),
        "frontier06_best_selective": parse_report_reference(F06B_REPORT, "frontier06B_best_selective_reference"),
        "label_v1_metric_rows": len(label_v1_rows),
    }


def best_model_summary(rows: pd.DataFrame, reference_id: str) -> dict[str, Any]:
    if rows.empty:
        return {"reference_id": reference_id, "available": False}
    grouped = grouped_split_summary(rows)
    grouped["validation_oos_score_sum"] = grouped["validation_aspiration_distance_score"] + grouped["oos_aspiration_distance_score"]
    grouped = grouped.sort_values(["validation_oos_score_sum", "oos_dd_risk_percent", "oos_profit_factor"], ascending=[True, True, False])
    best = dict(grouped.iloc[0])
    best["reference_id"] = reference_id
    best["available"] = True
    return json_ready(best)


def build_candidate_summary(
    candidate_metrics: list[dict[str, Any]],
    classification_rows: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
    references: dict[str, Any],
) -> list[dict[str, Any]]:
    metrics = pd.DataFrame(candidate_metrics)
    if metrics.empty:
        return []
    model_rows = metrics[
        metrics["target_kind"].eq("risk_label_candidate(위험 라벨 후보)")
        & ~metrics["model_id"].astype(str).str.startswith("oracle")
    ].copy()
    grouped = grouped_split_summary(model_rows)
    classification = pd.DataFrame(classification_rows)
    parity = pd.DataFrame(parity_rows)
    label_ref = references["label_v1_argmax"]
    rows: list[dict[str, Any]] = []
    for _, row in grouped.iterrows():
        target_id = str(row["target_id"])
        model_instance_id = str(row["model_instance_id"])
        class_group = classification[
            classification["target_id"].eq(target_id)
            & classification["model_instance_id"].eq(model_instance_id)
        ]
        parity_group = parity[
            parity["target_id"].eq(target_id)
            & parity["model_instance_id"].eq(model_instance_id)
        ]
        class_info = class_learnability(class_group)
        parity_passed = bool(parity_group["parity_passed"].all()) if len(parity_group) else False
        summary = row.to_dict()
        summary.update(class_info)
        summary["candidate_id"] = f"{target_id}__{model_instance_id}"
        summary["parity_passed"] = parity_passed
        add_reference_deltas(summary, label_ref, "label_v1")
        add_reference_deltas(summary, references["frontier04_locked_path_trainable"], "frontier04")
        add_reference_deltas(summary, references["frontier06_best_selective"], "frontier06")
        density_band = all(SCOUT_DENSITY_LOW <= float(summary[f"{split}_trades_per_day"]) <= SCOUT_DENSITY_HIGH for split in ("validation", "oos"))
        pf_floor = all(float(summary[f"{split}_profit_factor"]) >= SCOUT_PF_FLOOR and float(summary[f"{split}_net_profit"]) > 0 for split in ("validation", "oos"))
        dd_soft = all(float(summary[f"{split}_dd_risk_percent"]) <= SCOUT_DD_SOFT_CEILING for split in ("validation", "oos"))
        labelv1_score_improve = bool(summary.get("validation_vs_label_v1_score_improvement", 0.0) > 0 and summary.get("oos_vs_label_v1_score_improvement", 0.0) > 0)
        labelv1_pf_improve = bool(summary.get("validation_vs_label_v1_pf_delta", -999.0) >= 0 and summary.get("oos_vs_label_v1_pf_delta", -999.0) >= 0)
        labelv1_dd_improve = bool(summary.get("validation_vs_label_v1_dd_delta", 999.0) <= 0 and summary.get("oos_vs_label_v1_dd_delta", 999.0) <= 0)
        strict = bool(
            parity_passed
            and class_info["learnability_pass"]
            and density_band
            and pf_floor
            and dd_soft
            and labelv1_score_improve
            and labelv1_pf_improve
            and labelv1_dd_improve
        )
        dd_only = bool(labelv1_dd_improve and not (density_band and pf_floor and labelv1_score_improve))
        preserved = bool(parity_passed and class_info["learnability_pass"] and (dd_only or labelv1_score_improve) and not strict)
        summary["density_target_band_pass"] = density_band
        summary["pf_floor_pass"] = pf_floor
        summary["dd_soft_pass"] = dd_soft
        summary["strict_scout_clue_pass"] = strict
        summary["dd_only_preserved_clue_flag"] = dd_only
        summary["preserved_clue_pass"] = preserved
        summary["validation_oos_score_sum"] = float(summary["validation_aspiration_distance_score"] + summary["oos_aspiration_distance_score"])
        rows.append(json_ready(summary))
    rows.sort(
        key=lambda item: (
            not bool(item["strict_scout_clue_pass"]),
            not bool(item["preserved_clue_pass"]),
            float(item["validation_oos_score_sum"]),
            -float(item["oos_profit_factor"]),
            float(item["oos_dd_risk_percent"]),
        )
    )
    return rows


def grouped_split_summary(rows: pd.DataFrame) -> pd.DataFrame:
    keys = [
        "target_id",
        "target_kind",
        "model_id",
        "model_instance_id",
        "label_family",
        "family_semantics",
        "difference_from_f04",
        "signal_contract",
    ]
    metric_cols = [
        "trade_count",
        "trades_per_day",
        "long_trade_count",
        "short_trade_count",
        "flat_count",
        "net_profit",
        "profit_factor",
        "expectancy",
        "win_rate",
        "max_drawdown_percent",
        "max_monthly_drawdown_percent",
        "dd_risk_percent",
        "underwater_ratio",
        "max_loss_streak",
        "equity_trend_r2",
        "density_axis_distance",
        "pf_axis_distance",
        "dd_axis_distance",
        "smoothness_axis_distance",
        "aspiration_distance_score",
    ]
    out: list[dict[str, Any]] = []
    for _, group in rows.groupby(keys, sort=False):
        item = {key: group.iloc[0][key] for key in keys}
        for split in ("train", "validation", "oos"):
            split_row = group[group["split"].eq(split)].iloc[0]
            for column in metric_cols:
                item[f"{split}_{column}"] = split_row[column]
        out.append(item)
    return pd.DataFrame(out)


def class_learnability(class_group: pd.DataFrame) -> dict[str, Any]:
    if class_group.empty:
        return {
            "train_balanced_accuracy": 0.0,
            "validation_balanced_accuracy": 0.0,
            "oos_balanced_accuracy": 0.0,
            "validation_macro_f1": 0.0,
            "transfer_gap": 999.0,
            "class_balance_pass": False,
            "learnability_pass": False,
        }
    rows = {str(row["split"]): row for _, row in class_group.iterrows()}
    train = rows["train"]
    validation = rows["validation"]
    oos = rows["oos"]
    true_counts = np.array([float(train["true_short"]), float(train["true_flat"]), float(train["true_long"])], dtype="float64")
    fractions = true_counts / max(float(true_counts.sum()), 1.0)
    class_balance_pass = bool(float(np.nanmin(fractions)) >= CLASS_BALANCE_MIN and float(np.nanmax(fractions)) <= CLASS_BALANCE_MAX)
    transfer_gap = float(train["balanced_accuracy"] - validation["balanced_accuracy"])
    learnability_pass = bool(
        class_balance_pass
        and float(validation["balanced_accuracy"]) >= LEARNABILITY_VAL_BAL_ACC_FLOOR
        and float(validation["macro_f1"]) >= LEARNABILITY_VAL_MACRO_F1_FLOOR
        and transfer_gap <= LEARNABILITY_TRANSFER_GAP_CEILING
    )
    return {
        "train_balanced_accuracy": float(train["balanced_accuracy"]),
        "validation_balanced_accuracy": float(validation["balanced_accuracy"]),
        "oos_balanced_accuracy": float(oos["balanced_accuracy"]),
        "validation_macro_f1": float(validation["macro_f1"]),
        "oos_macro_f1": float(oos["macro_f1"]),
        "transfer_gap": transfer_gap,
        "train_min_class_fraction": float(np.nanmin(fractions)),
        "train_max_class_fraction": float(np.nanmax(fractions)),
        "class_balance_pass": class_balance_pass,
        "learnability_pass": learnability_pass,
    }


def add_reference_deltas(row: dict[str, Any], reference: dict[str, Any], prefix: str) -> None:
    if not reference.get("available", False):
        row[f"{prefix}_reference_available"] = False
        return
    row[f"{prefix}_reference_available"] = True
    for split in ("validation", "oos"):
        ref_pf = float(reference.get(f"{split}_profit_factor", 0.0))
        ref_density = float(reference.get(f"{split}_trades_per_day", 0.0))
        ref_dd = float(reference.get(f"{split}_dd_risk_percent", 0.0))
        ref_score = float(reference.get(f"{split}_aspiration_distance_score", 0.0))
        row[f"{split}_vs_{prefix}_pf_delta"] = float(row[f"{split}_profit_factor"]) - ref_pf
        row[f"{split}_vs_{prefix}_density_delta"] = float(row[f"{split}_trades_per_day"]) - ref_density
        row[f"{split}_vs_{prefix}_dd_delta"] = float(row[f"{split}_dd_risk_percent"]) - ref_dd
        row[f"{split}_vs_{prefix}_score_improvement"] = ref_score - float(row[f"{split}_aspiration_distance_score"])


def parse_report_reference(path: Path, reference_id: str) -> dict[str, Any]:
    if not path_exists(path):
        return {"reference_id": reference_id, "available": False, "source_path": path.as_posix()}
    text = io_path(path).read_text(encoding="utf-8-sig")
    ref: dict[str, Any] = {
        "reference_id": reference_id,
        "available": True,
        "source_path": path.as_posix(),
        "source_sha256": sha256_file(path),
        "validation_aspiration_distance_score": 999.0,
        "oos_aspiration_distance_score": 999.0,
    }
    for split, label in (("validation", "validation|검증"), ("oos", "OOS|표본밖")):
        for line in text.splitlines():
            if not re.search(label, line, flags=re.IGNORECASE):
                continue
            values = re.findall(r"`([^`]+)`", line)
            if len(values) < 3:
                continue
            clean = [number_from_text(value) for value in values[:3]]
            if "PF/density/DD" in line or "수익 팩터/밀도/손실폭" in line:
                pf, density, dd = clean
            else:
                density, pf, dd = clean
            ref[f"{split}_trades_per_day"] = density
            ref[f"{split}_profit_factor"] = pf
            ref[f"{split}_dd_risk_percent"] = dd
            break
    for split in ("validation", "oos"):
        ref.setdefault(f"{split}_trades_per_day", 0.0)
        ref.setdefault(f"{split}_profit_factor", 0.0)
        ref.setdefault(f"{split}_dd_risk_percent", 999.0)
    return ref


def number_from_text(value: str) -> float:
    match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
    if not match:
        return 0.0
    return float(match.group(0))


def build_final(
    result: dict[str, Any],
    source_integrity: dict[str, Any],
    feature_order: list[str],
    variants: list[RiskLabelVariant],
) -> dict[str, Any]:
    candidates = result["candidate_summary"]
    strict_rows = int(sum(1 for row in candidates if row.get("strict_scout_clue_pass")))
    preserved_rows = int(sum(1 for row in candidates if row.get("preserved_clue_pass")))
    best = candidates[0] if candidates else {}
    if strict_rows:
        status = "risk_shaped_label_strict_scout_clue_no_authority"
        judgment = "scout_clue(탐색 단서)"
        next_run = NEXT_CLUE_RUN_ID
    elif preserved_rows:
        status = "risk_shaped_label_preserved_clue_no_authority"
        judgment = "preserved_clue(보존 단서)"
        next_run = NEXT_REPAIR_RUN_ID
    else:
        status = "risk_shaped_label_no_strict_clue_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run = NEXT_REPAIR_RUN_ID
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": utc_now(),
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run,
        "variant_family_count": len({variant.family_id for variant in variants}),
        "variant_count": len(variants),
        "model_family": "Frontier04D small sklearn model family(전선04D 작은 사이킷런 모델군)",
        "model_count_per_target": len(f04d.MODEL_SPECS),
        "candidate_row_count": len(candidates),
        "strict_scout_clue_rows": strict_rows,
        "preserved_clue_rows": preserved_rows,
        "best_candidate_row": best,
        "references": result["references"],
        "frontier07b_bounds": {
            "feature_set": "feature_set_v2 fixed(피처 세트 v2 고정)",
            "signal_contract": "argmax_only_no_threshold(최대확률 전용, 임계값 없음)",
            "variant_cap": "4 families x 3 variants = 12, below Grok cap(4개 군 x 3개 변형 = 12개, 그록 상한 아래)",
            "mandatory_references": "label_v1 argmax, F04 locked path trainable, F06 best selective(라벨v1 최대확률, F04 고정 경로 학습 참조, F06 최선 선택 참조)",
            "tier_b": "missing_required until paired source exists(쌍 원천 전까지 필수 누락)",
        },
        "data_integrity": {
            **source_integrity,
            "feature_label_boundary": (
                "future OHLC path is used only to create labels(미래 OHLC 경로는 라벨 생성에만 사용); "
                "model inputs remain fixed feature_set_v2 current/known features(모델 입력은 고정 피처 세트 v2의 현재/확정 피처)."
            ),
            "split_boundary": "labels are defined by train-calibrated scale; models fit train only; validation/OOS are read only(라벨은 학습 보정 스케일로 정의, 모델은 학습만 적합, 검증/표본밖은 판독 전용)",
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
        },
        "model_validation": {
            "selection_metric": "strict scout clue then preserved clue then validation+OOS distance(엄격 탐색 단서, 보존 단서, 검증+표본밖 거리 순)",
            "learnability_gate": "class balance, validation balanced accuracy, macro F1, transfer gap(클래스 균형, 검증 균형 정확도, 매크로 F1, 전달 격차)",
            "overfit_risk": "candidate ranking uses validation/OOS read, so no operating claim(후보 순위는 검증/표본밖 판독을 쓰므로 운영 주장 없음)",
            "validation_judgment": "exploratory(탐색)",
        },
        "runtime_parity": {
            "onnx_parity": "checked for each trained sklearn model(각 학습 사이킷런 모델에서 확인)",
            "runtime_claim_boundary": "research_only_no_mt5(연구 전용, MT5 없음)",
        },
        "artifact_lineage": {
            "source_inputs": [f03b.DATASET_PATH.as_posix(), f04b.RAW_US100.as_posix()],
            "producer": "stage_pipelines/stage_frontier_07/frontier07b_adverse_excursion_risk_label_proxy_scout.py",
            "consumer": next_run,
            "availability": "ignored_run_artifacts_with_tracked_report(무시 실행 산출물 + 추적 보고서)",
            "lineage_judgment": "connected_with_boundary(경계부 연결)",
        },
        "feature_order_hash": ordered_hash(feature_order),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_artifacts(result: dict[str, Any], final: dict[str, Any], variants: list[RiskLabelVariant]) -> dict[str, Path]:
    artifacts = {
        "variant_grid": RUN_ROOT / "risk_label_variant_grid.csv",
        "candidate_metrics": RUN_ROOT / "candidate_model_metrics.csv",
        "reference_metrics": RUN_ROOT / "reference_model_metrics.csv",
        "candidate_summary": RUN_ROOT / "candidate_summary.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "label_distribution": RUN_ROOT / "label_distribution.csv",
        "skipped": RUN_ROOT / "skipped_targets.csv",
        "integrity": RUN_ROOT / "integrity.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    pd.DataFrame([variant.__dict__ for variant in variants]).to_csv(io_path(artifacts["variant_grid"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["candidate_metrics"]).to_csv(io_path(artifacts["candidate_metrics"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["reference_metrics"]).to_csv(io_path(artifacts["reference_metrics"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["candidate_summary"]).to_csv(io_path(artifacts["candidate_summary"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["classification_metrics"]).to_csv(io_path(artifacts["classification_metrics"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["onnx_parity"]).to_csv(io_path(artifacts["onnx_parity"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["label_distribution"]).to_csv(io_path(artifacts["label_distribution"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["skipped"]).to_csv(io_path(artifacts["skipped"]), index=False, encoding="utf-8-sig")
    write_json(artifacts["integrity"], final["data_integrity"])
    final["artifact_lineage"]["artifact_paths"] = [path.as_posix() for path in artifacts.values()]
    manifest = {
        **final,
        "script_path": "stage_pipelines/stage_frontier_07/frontier07b_adverse_excursion_risk_label_proxy_scout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_07/frontier07b_adverse_excursion_risk_label_proxy_scout.py")),
        "artifacts": {
            name: {"path": path.as_posix(), "sha256": sha256_file(path)}
            for name, path in artifacts.items()
            if path_exists(path) and name != "run_manifest"
        },
        "models": [
            {
                "model_instance_id": row["model_instance_id"],
                "target_id": row["target_id"],
                "onnx_path": row["onnx_path"],
                "onnx_sha256": row["onnx_sha256"],
                "joblib_path": row["joblib_path"],
                "joblib_sha256": row["joblib_sha256"],
            }
            for row in result["onnx_parity"]
        ],
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }
    write_json(artifacts["run_manifest"], manifest)
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_candidate_row"]
    refs = final["references"]
    text = f"""# Frontier07B Adverse Excursion Risk Label Proxy Scout Report(전선07B 불리한 이동 위험 라벨 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): 4 label families(라벨군) x 3 variants(변형)로 adverse excursion risk-shaped labels(불리한 이동 위험 형성 라벨)을 만들고, fixed feature_set_v2(고정 피처 세트 v2)와 small ONNX-exportable models(작은 온엑스 내보내기 가능 모델)로 argmax-only(최대확률 전용) 학습/검증을 실행했습니다.

Effect(효과): Frontier04(전선04)의 event-first path grid(이벤트 우선 경로 격자)와 Frontier06(전선06)의 abstention threshold search(기권 임계값 탐색)를 반복하지 않고, label utility(라벨 효용)가 DD(drawdown, 손실폭)를 직접 낮출 수 있는지 확인했습니다.

## Best Candidate Read(최상위 후보 판독)

- candidate(후보): `{best.get('candidate_id', 'none')}`
- family(라벨군): `{best.get('label_family', 'none')}`
- strict_scout_clue_pass(엄격 탐색 단서 통과): `{best.get('strict_scout_clue_pass', False)}`
- preserved_clue_pass(보존 단서 통과): `{best.get('preserved_clue_pass', False)}`
- learnability_pass(학습 가능성 통과): `{best.get('learnability_pass', False)}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- ONNX parity(온엑스 동등성): `{best.get('parity_passed', False)}`

## Reference Comparison(참조 비교)

- label_v1 argmax(라벨v1 최대확률): validation/OOS PF(검증/표본밖 수익 팩터) `{fmt(refs['label_v1_argmax'].get('validation_profit_factor'))}` / `{fmt(refs['label_v1_argmax'].get('oos_profit_factor'))}`, DD(손실폭) `{fmt(refs['label_v1_argmax'].get('validation_dd_risk_percent'))}` / `{fmt(refs['label_v1_argmax'].get('oos_dd_risk_percent'))}`
- Frontier04 locked path trainable(전선04 고정 경로 학습 참조): validation/OOS PF(검증/표본밖 수익 팩터) `{fmt(refs['frontier04_locked_path_trainable'].get('validation_profit_factor'))}` / `{fmt(refs['frontier04_locked_path_trainable'].get('oos_profit_factor'))}`, DD(손실폭) `{fmt(refs['frontier04_locked_path_trainable'].get('validation_dd_risk_percent'))}` / `{fmt(refs['frontier04_locked_path_trainable'].get('oos_dd_risk_percent'))}`
- Frontier06 best selective(전선06 최선 선택 참조): validation/OOS PF(검증/표본밖 수익 팩터) `{fmt(refs['frontier06_best_selective'].get('validation_profit_factor'))}` / `{fmt(refs['frontier06_best_selective'].get('oos_profit_factor'))}`, DD(손실폭) `{fmt(refs['frontier06_best_selective'].get('validation_dd_risk_percent'))}` / `{fmt(refs['frontier06_best_selective'].get('oos_dd_risk_percent'))}`

## Result Boundary(결과 경계)

- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- Tier B/Tier A+B(티어 B/티어 A+B): missing_required(필수 누락)
- runtime boundary(런타임 경계): `{final['runtime_parity']['runtime_claim_boundary']}`

## Artifacts(산출물)

- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- model metrics(모델 지표): `{artifacts['candidate_metrics'].as_posix()}`
- reference metrics(참조 지표): `{artifacts['reference_metrics'].as_posix()}`
- classification metrics(분류 지표): `{artifacts['classification_metrics'].as_posix()}`
- ONNX parity(온엑스 동등성): `{artifacts['onnx_parity'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 결과 경계에 따라 Grok review(그록 검토) 또는 repair/closeout decision(수리/마감 결정)을 여는 것입니다. Effect(효과)는 DD-only improvement(손실폭만 개선)를 strict scout clue(엄격 탐색 단서)로 과장하지 않는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""
    write_text_sig(REPORT_PATH, text)


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    import yaml

    now = final["created_at_utc"]
    state = {
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
    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8")
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(final))
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(final))
    upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    for row in ledger_rows(final, artifacts):
        upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {now}: `{RUN_ID}` {final['judgment']}. Effect(효과): strict scout clue rows(엄격 탐색 단서 행) `{final['strict_scout_clue_rows']}`, next run(다음 실행) `{final['next_run_id']}`.\n",
    )
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{RUN_ID}`: adverse excursion risk-shaped label proxy scout(불리한 이동 위험 형성 라벨 프록시 탐색) recorded strict rows(엄격 행) `{final['strict_scout_clue_rows']}` and preserved rows(보존 행) `{final['preserved_clue_rows']}`. Effect(효과): DD-targeted label utility(손실폭 겨냥 라벨 효용)의 학습 가능성을 기록했습니다.\n",
    )
    if final["strict_scout_clue_rows"] == 0 and final["preserved_clue_rows"] == 0:
        f03b.append_once(
            f03b.NEGATIVE_RESULT_REGISTER,
            RUN_ID,
            f"- `{RUN_ID}`: risk-shaped labels did not create strict or preserved validation+OOS clue(위험 형성 라벨이 검증+표본밖 엄격/보존 단서를 만들지 못함). Effect(효과): label utility axis(라벨 효용 축)를 수리/마감 결정으로 넘깁니다.\n",
        )


def current_state_text(final: dict[str, Any]) -> str:
    best = final["best_candidate_row"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier07B(전선07B)는 adverse excursion risk-shaped label proxy scout(불리한 이동 위험 형성 라벨 프록시 탐색)를 완료했습니다.

Judgment(판정): `{final['judgment']}`

Best read(최상위 판독): `{best.get('candidate_id', 'none')}` with strict scout clue rows(엄격 탐색 단서 행) `{final['strict_scout_clue_rows']}` and preserved clue rows(보존 단서 행) `{final['preserved_clue_rows']}`.

Next action(다음 행동): `{final['next_run_id']}`. Action(행동)은 결과 경계에 맞게 Grok review(그록 검토) 또는 repair/closeout decision(수리/마감 결정)을 여는 것입니다. Effect(효과)는 DD-only improvement(손실폭만 개선)를 완성 후보처럼 과장하지 않는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_text(final: dict[str, Any]) -> str:
    return f"""# Stage Frontier 07 Selection Status(전선 07단계 선택 상태)

Updated(갱신): {final['created_at_utc']}

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Judgment(판정): `{final['judgment']}`

Strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`

Preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "risk_label_model_scout(위험 라벨 모델 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_authority",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["strict_scout_clue_rows"]),
        "claim_boundary": "risk_label_scout_onnx_parity_only_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_risk_label_model_scout",
        "subrun_id": f"{RUN_ID}__tier_a_risk_label_model_scout",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "risk_label_model_scout_not_runtime(위험 라벨 모델 탐색, 런타임 아님)",
        "primary_kpi": primary_kpi_text(best),
        "guardrail_kpi": "argmax_only_no_threshold_no_wfo_no_mt5_no_authority(최대확률 전용, 임계값/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "risk_label_model_scout_only(위험 라벨 모델 탐색 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can adverse-excursion risk labels train away drawdown-heavy entries?(불리한 이동 위험 라벨이 손실폭 큰 진입을 학습으로 줄일 수 있는가?)",
        "skill_family": "experiment_execution(실험 실행)",
        "lineage_summary": "frontier07a_stage_open_to_frontier07b_risk_label_model_scout(전선07A 단계 개방에서 전선07B 위험 라벨 모델 탐색)",
    }


def ledger_rows(final: dict[str, Any], artifacts: dict[str, Path]) -> list[dict[str, Any]]:
    best = final["best_candidate_row"]
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "risk_label_model_scout(위험 라벨 모델 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "argmax_only_no_threshold_no_wfo_no_mt5_no_authority(최대확률 전용, 임계값/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_risk_label_model_scout",
            "subrun_id": f"{RUN_ID}__tier_a_risk_label_model_scout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "risk_label_model_scout_not_runtime(위험 라벨 모델 탐색, 런타임 아님)",
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


def label_distribution(full: pd.DataFrame, labels: np.ndarray, target_id: str, target_kind: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        mask = full["split"].astype(str).eq(split).to_numpy()
        for label in LABEL_ORDER:
            rows.append({
                "target_id": target_id,
                "target_kind": target_kind,
                "split": split,
                "label": label,
                "label_name": LABEL_NAMES[label],
                "count": int((labels[mask] == label).sum()),
                "fraction": float((labels[mask] == label).mean()),
            })
    return rows


def primary_kpi_text(best: dict[str, Any]) -> str:
    return (
        f"best={best.get('candidate_id', 'none')};"
        f"strict={best.get('strict_scout_clue_pass', False)};"
        f"preserved={best.get('preserved_clue_pass', False)};"
        f"oos_pf={fmt(best.get('oos_profit_factor'))};"
        f"oos_density={fmt(best.get('oos_trades_per_day'))};"
        f"oos_dd={fmt(best.get('oos_dd_risk_percent'))}"
    )


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def upsert_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    with open(str(io_path(path)), "r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    with open(str(io_path(path)), "r", encoding="utf-8-sig", newline="") as handle:
        rows = [dict(existing) for existing in csv.DictReader(handle)]
    normalized = {column: stringify(row.get(column, "")) for column in header}
    rows = [existing for existing in rows if existing.get(key) != normalized.get(key)]
    rows.append(normalized)
    with open(str(io_path(path)), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: stringify(item.get(column, "")) for column in header})


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(number):
        return str(number)
    return f"{number:.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
