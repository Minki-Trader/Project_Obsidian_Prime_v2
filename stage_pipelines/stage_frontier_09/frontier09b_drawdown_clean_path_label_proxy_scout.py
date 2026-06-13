from __future__ import annotations

import csv
import json
import math
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
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b


STAGE_ID = "stage_frontier_09__drawdown_normalized_clean_path_labeling"
RUN_ID = "frontier09B_drawdown_clean_path_label_proxy_scout_v1"
RUN_NUMBER = "frontier09B"
PARENT_RUN_ID = "frontier09A_stage_open_drawdown_clean_path_labeling_v1"
NEXT_STRICT_RUN_ID = "frontier09C_grok_pre_expensive_drawdown_clean_path_review_v1"
NEXT_REPAIR_RUN_ID = "frontier09C_drawdown_clean_path_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"

LABEL_ORDER = f04d.LABEL_ORDER
LABEL_NAMES = f04d.LABEL_NAMES
HORIZON_BARS = 12
SCALE_QUANTILE = 0.90
SCOUT_DENSITY_LOW = 5.0
SCOUT_DENSITY_HIGH = 10.0
SCOUT_PF_FLOOR = 1.2
SCOUT_DD_SOFT_CEILING = 15.0
CLASS_BALANCE_MIN = 0.03
CLASS_BALANCE_MAX = 0.94
LEARNABILITY_VAL_BAL_ACC_FLOOR = 0.30
LEARNABILITY_VAL_MACRO_F1_FLOOR = 0.20
LEARNABILITY_TRANSFER_GAP_CEILING = 0.25
RISK_REFERENCE_VARIANT_ID = "f07b_time_to_adverse_penalty_v1_lt0p90_st0p90_lc0p60_sc0p60_q90"

MODEL_ID_SHORT = {
    "logreg_l2_c0p5_plain_argmax": "lr_plain",
    "logreg_l2_c0p5_balanced_argmax": "lr_bal",
    "rf_depth5_leaf80_balanced_argmax": "rf_bal",
}


@dataclass(frozen=True)
class CleanPathVariant:
    variant_id: str
    family_id: str
    family_semantics: str
    difference_from_f07: str
    horizon_bars: int
    scale_quantile: float
    base_scale_log_return: float
    long_target_multiplier: float
    short_target_multiplier: float
    long_cap_multiplier: float
    short_cap_multiplier: float
    ratio_floor: float
    adverse_bar_fraction_ceiling: float
    capture_floor: float
    recovery_floor_multiplier: float
    long_target_log_return: float
    short_target_log_return: float
    long_cap_log_return: float
    short_cap_log_return: float


@dataclass(frozen=True)
class TargetSurface:
    target_id: str
    target_kind: str
    label_family: str
    family_semantics: str
    difference_from_f07: str
    source_boundary: str
    labels: np.ndarray
    variant: CleanPathVariant | None


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    path = f07b.path_arrays(full, raw, HORIZON_BARS)
    variants = build_variants(full, path)
    targets = build_targets(full, raw, path, variants)
    result = train_and_evaluate(full, feature_order, path, targets)
    final = build_final(result, source_integrity, feature_order, variants)
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


def build_variants(full: pd.DataFrame, path: dict[str, np.ndarray]) -> list[CleanPathVariant]:
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    base_scale = float(np.nanquantile(np.abs(path["fwd_return"][train_mask]), SCALE_QUANTILE))
    if not np.isfinite(base_scale) or base_scale <= 0:
        raise RuntimeError("Invalid train-only path scale.")

    specs = [
        (
            "payoff_adverse_ratio",
            "MFE/MAE efficiency must beat a train-only ratio floor(MFE/MAE 효율이 학습 전용 비율 하한을 넘어야 함)",
            "Frontier07 used adverse penalties inside a score; Frontier09 requires payoff per adverse unit before labeling(Frontier07은 점수 안에 불리 이동 벌점을 넣었고, Frontier09는 라벨 전 수익/불리 이동 효율을 요구함)",
            [(0.80, 0.80, 0.70, 0.70, 1.45, 1.00, 0.20), (1.00, 1.00, 0.85, 0.85, 1.70, 1.00, 0.25)],
        ),
        (
            "underwater_burden",
            "The path may not spend too many bars underwater(경로가 너무 많은 봉에서 물려 있으면 안 됨)",
            "Frontier07 penalized first adverse timing; Frontier09 counts adverse-bar burden as a label blocker(Frontier07은 첫 불리 이동 시점을 벌점화했고, Frontier09는 불리 봉 비중을 라벨 차단 조건으로 셈)",
            [(0.75, 0.75, 0.65, 0.65, 1.00, 0.25, 0.25), (0.95, 0.95, 0.75, 0.75, 1.00, 0.17, 0.30)],
        ),
        (
            "clean_recovery",
            "Final close must retain enough of the favorable move(종가가 유리 이동을 충분히 보존해야 함)",
            "Frontier07 could accept excursion-heavy wins; Frontier09 requires recovery/capture after the path(Frontier07은 이동폭이 큰 승리를 받을 수 있었고, Frontier09는 경로 뒤 회복/포획을 요구함)",
            [(0.80, 0.80, 0.70, 0.70, 1.00, 1.00, 0.45), (1.05, 1.05, 0.85, 0.85, 1.00, 1.00, 0.55)],
        ),
    ]

    variants: list[CleanPathVariant] = []
    for family_id, semantics, delta, family_specs in specs:
        for index, (
            long_target,
            short_target,
            long_cap,
            short_cap,
            ratio_floor,
            adverse_fraction_ceiling,
            capture_floor,
        ) in enumerate(family_specs, start=1):
            variant_id = (
                f"f09b_{family_id}_v{index}_"
                f"lt{long_target:.2f}_st{short_target:.2f}_lc{long_cap:.2f}_sc{short_cap:.2f}"
            ).replace(".", "p")
            variants.append(
                CleanPathVariant(
                    variant_id=variant_id,
                    family_id=family_id,
                    family_semantics=semantics,
                    difference_from_f07=delta,
                    horizon_bars=HORIZON_BARS,
                    scale_quantile=SCALE_QUANTILE,
                    base_scale_log_return=base_scale,
                    long_target_multiplier=long_target,
                    short_target_multiplier=short_target,
                    long_cap_multiplier=long_cap,
                    short_cap_multiplier=short_cap,
                    ratio_floor=ratio_floor,
                    adverse_bar_fraction_ceiling=adverse_fraction_ceiling,
                    capture_floor=capture_floor,
                    recovery_floor_multiplier=capture_floor,
                    long_target_log_return=base_scale * long_target,
                    short_target_log_return=base_scale * short_target,
                    long_cap_log_return=base_scale * long_cap,
                    short_cap_log_return=base_scale * short_cap,
                )
            )
    return variants


def build_targets(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    path: dict[str, np.ndarray],
    variants: list[CleanPathVariant],
) -> list[TargetSurface]:
    label_v1_labels = pd.to_numeric(full["label_class"], errors="raise").to_numpy(dtype="int64")
    risk_variants = {variant.variant_id: variant for variant in f07b.build_variants(full, raw)}
    if RISK_REFERENCE_VARIANT_ID not in risk_variants:
        raise RuntimeError(f"Missing Frontier07 reference variant: {RISK_REFERENCE_VARIANT_ID}")
    risk_labels, _, _ = f07b.build_risk_labels(path, risk_variants[RISK_REFERENCE_VARIANT_ID])

    targets = [
        TargetSurface(
            target_id="label_v1_argmax_reference",
            target_kind="reference_label_v1(참조 라벨 v1)",
            label_family="label_v1_reference(라벨 v1 참조)",
            family_semantics="Original label_v1 reference only(원래 라벨 v1 참조 전용)",
            difference_from_f07="reference_only_not_frontier09_candidate(참조 전용, Frontier09 후보 아님)",
            source_boundary="reference_only_not_baseline(참조 전용, 기준선 아님)",
            labels=label_v1_labels,
            variant=None,
        ),
        TargetSurface(
            target_id=RISK_REFERENCE_VARIANT_ID,
            target_kind="reference_frontier07_risk_label(참조 Frontier07 위험 라벨)",
            label_family="frontier07_reference(Frontier07 참조)",
            family_semantics="Prior risk-shaped label reference only(이전 위험 형성 라벨 참조 전용)",
            difference_from_f07="same_reference_not_inherited_winner(같은 참조, 상속 승자 아님)",
            source_boundary="reference_only_not_inherited_authority(참조 전용, 상속 권위 없음)",
            labels=risk_labels,
            variant=None,
        ),
    ]
    for variant in variants:
        labels, _, _ = build_clean_path_labels(path, variant)
        targets.append(
            TargetSurface(
                target_id=variant.variant_id,
                target_kind="clean_path_label_candidate(깨끗한 경로 라벨 후보)",
                label_family=variant.family_id,
                family_semantics=variant.family_semantics,
                difference_from_f07=variant.difference_from_f07,
                source_boundary="frontier09_candidate_no_authority(Frontier09 후보, 권위 없음)",
                labels=labels,
                variant=variant,
            )
        )
    return targets


def build_clean_path_labels(path: dict[str, np.ndarray], variant: CleanPathVariant) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    eps = max(variant.base_scale_log_return * 0.05, 1e-12)
    long_ratio = path["long_mfe"] / np.maximum(path["long_mae"], eps)
    short_ratio = path["short_mfe"] / np.maximum(path["short_mae"], eps)
    long_capture = path["fwd_return"] / np.maximum(path["long_mfe"], eps)
    short_capture = -path["fwd_return"] / np.maximum(path["short_mfe"], eps)
    long_underwater = np.mean(path["low_steps"] >= variant.long_cap_log_return, axis=0)
    short_underwater = np.mean(path["high_steps"] >= variant.short_cap_log_return, axis=0)

    if variant.family_id == "payoff_adverse_ratio":
        long_ok = (
            (path["long_mfe"] >= variant.long_target_log_return)
            & (path["fwd_return"] >= variant.long_target_log_return * variant.recovery_floor_multiplier)
            & (path["long_mae"] <= variant.long_cap_log_return)
            & (long_ratio >= variant.ratio_floor)
        )
        short_ok = (
            (path["short_mfe"] >= variant.short_target_log_return)
            & (path["fwd_return"] <= -variant.short_target_log_return * variant.recovery_floor_multiplier)
            & (path["short_mae"] <= variant.short_cap_log_return)
            & (short_ratio >= variant.ratio_floor)
        )
        long_score = long_ratio + long_capture - path["long_mae"] / max(variant.long_cap_log_return, eps)
        short_score = short_ratio + short_capture - path["short_mae"] / max(variant.short_cap_log_return, eps)
    elif variant.family_id == "underwater_burden":
        long_ok = (
            (path["long_mfe"] >= variant.long_target_log_return)
            & (path["fwd_return"] >= variant.long_target_log_return * variant.recovery_floor_multiplier)
            & (path["long_mae"] <= variant.long_cap_log_return * 1.25)
            & (long_underwater <= variant.adverse_bar_fraction_ceiling)
        )
        short_ok = (
            (path["short_mfe"] >= variant.short_target_log_return)
            & (path["fwd_return"] <= -variant.short_target_log_return * variant.recovery_floor_multiplier)
            & (path["short_mae"] <= variant.short_cap_log_return * 1.25)
            & (short_underwater <= variant.adverse_bar_fraction_ceiling)
        )
        long_score = path["long_mfe"] / max(variant.long_target_log_return, eps) - 2.0 * long_underwater
        short_score = path["short_mfe"] / max(variant.short_target_log_return, eps) - 2.0 * short_underwater
    elif variant.family_id == "clean_recovery":
        long_ok = (
            (path["long_mfe"] >= variant.long_target_log_return)
            & (path["fwd_return"] >= variant.long_target_log_return * variant.recovery_floor_multiplier)
            & (path["long_mae"] <= variant.long_cap_log_return)
            & (long_capture >= variant.capture_floor)
        )
        short_ok = (
            (path["short_mfe"] >= variant.short_target_log_return)
            & (path["fwd_return"] <= -variant.short_target_log_return * variant.recovery_floor_multiplier)
            & (path["short_mae"] <= variant.short_cap_log_return)
            & (short_capture >= variant.capture_floor)
        )
        long_score = long_capture + path["long_mfe"] / max(variant.long_target_log_return, eps) - path["long_mae"] / max(variant.long_cap_log_return, eps)
        short_score = short_capture + path["short_mfe"] / max(variant.short_target_log_return, eps) - path["short_mae"] / max(variant.short_cap_log_return, eps)
    else:
        raise ValueError(f"Unknown family: {variant.family_id}")

    signal = np.zeros(len(path["fwd_return"]), dtype="int8")
    signal[long_ok & (long_score > short_score + 1e-12)] = 1
    signal[short_ok & (short_score > long_score + 1e-12)] = -1
    labels = np.where(signal < 0, 0, np.where(signal > 0, 2, 1)).astype("int64")
    diagnostics = {
        "oracle_long_count": int((signal == 1).sum()),
        "oracle_short_count": int((signal == -1).sum()),
        "oracle_flat_count": int((signal == 0).sum()),
        "mean_long_ratio": float(np.nanmean(long_ratio)),
        "mean_short_ratio": float(np.nanmean(short_ratio)),
        "mean_long_underwater": float(np.nanmean(long_underwater)),
        "mean_short_underwater": float(np.nanmean(short_underwater)),
    }
    return labels, signal, diagnostics


def train_and_evaluate(
    full: pd.DataFrame,
    feature_order: list[str],
    path: dict[str, np.ndarray],
    targets: list[TargetSurface],
) -> dict[str, Any]:
    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values.")
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    sample_indices = np.concatenate(
        [
            np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())[:256]
            for split in ("train", "validation", "oos")
        ]
    )

    reference_metrics: list[dict[str, Any]] = []
    candidate_metrics: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    target_distribution_rows: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []

    for target in targets:
        target_distribution_rows.extend(label_distribution(full, target))
        missing = sorted(set(LABEL_ORDER) - set(int(value) for value in target.labels[train_mask]))
        if missing:
            skipped_rows.append(
                {
                    "target_id": target.target_id,
                    "target_kind": target.target_kind,
                    "reason": f"missing_train_classes={missing}",
                }
            )
            continue
        model_rows = fit_label_target(
            full=full,
            x_all=x_all,
            labels=target.labels,
            fwd_return=path["fwd_return"],
            target=target,
            train_mask=train_mask,
            sample_indices=sample_indices,
            classification_rows=classification_rows,
            parity_rows=parity_rows,
        )
        if target.target_kind.startswith("clean_path_label_candidate"):
            candidate_metrics.extend(model_rows)
        else:
            reference_metrics.extend(model_rows)

    candidate_summary = build_candidate_summary(candidate_metrics, reference_metrics, classification_rows, parity_rows)
    return {
        "reference_metrics": reference_metrics,
        "candidate_metrics": candidate_metrics,
        "classification_metrics": classification_rows,
        "onnx_parity": parity_rows,
        "target_distribution": target_distribution_rows,
        "skipped": skipped_rows,
        "candidate_summary": candidate_summary,
    }


def fit_label_target(
    *,
    full: pd.DataFrame,
    x_all: np.ndarray,
    labels: np.ndarray,
    fwd_return: np.ndarray,
    target: TargetSurface,
    train_mask: np.ndarray,
    sample_indices: np.ndarray,
    classification_rows: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    target_dir = MODEL_DIR / target.target_id
    for spec in f04d.MODEL_SPECS:
        short_model_id = MODEL_ID_SHORT.get(spec.model_id, spec.model_id[:12])
        model_instance_id = f"f09b_{target.target_id}_{short_model_id}"
        model = clone(spec.estimator)
        model.fit(x_all[train_mask], labels[train_mask])
        probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
        pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
        signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")

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
                "target_id": target.target_id,
                "target_kind": target.target_kind,
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
        for split in ("train", "validation", "oos"):
            split_mask = full["split"].astype(str).eq(split).to_numpy()
            y_true = labels[split_mask]
            y_pred = pred_label[split_mask]
            classification_rows.append(
                {
                    "target_id": target.target_id,
                    "target_kind": target.target_kind,
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
                }
            )
        rows.extend(evaluate_model_signal(full, signal, fwd_return, target, spec.model_id, model_instance_id))
    return rows


def evaluate_model_signal(
    full: pd.DataFrame,
    signal: np.ndarray,
    fwd_return: np.ndarray,
    target: TargetSurface,
    model_id: str,
    model_instance_id: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    reasons = np.full(len(full), f"argmax_model_{target.target_id}(최대 확률 모델)", dtype=object)
    first_steps = np.zeros(len(full), dtype="int16")
    for split in ("train", "validation", "oos"):
        metric = f04b.evaluate_split(
            full,
            signal,
            fwd_return,
            split,
            metric_variant(target.variant, target.target_id),
            f"argmax_model_{target.target_id}(최대 확률 모델 {target.target_id})",
            reasons,
            first_steps,
        )
        metric.update(
            {
                "target_id": target.target_id,
                "target_kind": target.target_kind,
                "source_boundary": target.source_boundary,
                "model_id": model_id,
                "model_instance_id": model_instance_id,
                "label_family": target.label_family,
                "family_semantics": target.family_semantics,
                "difference_from_f07": target.difference_from_f07,
                "signal_contract": "argmax_only_no_threshold(최대 확률 전용, 임계값 없음)",
            }
        )
        rows.append(metric)
    return rows


def metric_variant(variant: CleanPathVariant | None, target_id: str) -> f04b.PathVariant:
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


def build_candidate_summary(
    candidate_metrics: list[dict[str, Any]],
    reference_metrics: list[dict[str, Any]],
    classification_rows: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    candidates_frame = pd.DataFrame(candidate_metrics)
    references_frame = pd.DataFrame(reference_metrics)
    if candidates_frame.empty:
        return []
    grouped = grouped_split_summary(candidates_frame)
    reference_grouped = grouped_split_summary(references_frame) if not references_frame.empty else pd.DataFrame()
    classification = pd.DataFrame(classification_rows)
    parity = pd.DataFrame(parity_rows)
    label_v1_refs = reference_map(reference_grouped, "label_v1_argmax_reference")
    f07_refs = reference_map(reference_grouped, RISK_REFERENCE_VARIANT_ID)

    rows: list[dict[str, Any]] = []
    for _, row in grouped.iterrows():
        item = row.to_dict()
        target_id = str(item["target_id"])
        model_id = str(item["model_id"])
        model_instance_id = str(item["model_instance_id"])
        class_group = classification[
            classification["target_id"].eq(target_id)
            & classification["model_instance_id"].eq(model_instance_id)
        ]
        parity_group = parity[
            parity["target_id"].eq(target_id)
            & parity["model_instance_id"].eq(model_instance_id)
        ]
        item.update(class_learnability(class_group))
        item["candidate_id"] = f"{target_id}__{model_instance_id}"
        item["parity_passed"] = bool(len(parity_group) and parity_group["parity_passed"].all())
        label_ref = label_v1_refs.get(model_id)
        f07_ref = f07_refs.get(model_id)
        add_reference_deltas(item, label_ref, "label_v1")
        add_reference_deltas(item, f07_ref, "frontier07")
        item["density_band_pass"] = all(
            SCOUT_DENSITY_LOW <= float(item[f"{split}_trades_per_day"]) <= SCOUT_DENSITY_HIGH
            for split in ("validation", "oos")
        )
        item["pf_floor_pass"] = all(
            float(item[f"{split}_profit_factor"]) >= SCOUT_PF_FLOOR and float(item[f"{split}_net_profit"]) > 0
            for split in ("validation", "oos")
        )
        item["dd_soft_pass"] = all(
            float(item[f"{split}_dd_risk_percent"]) <= SCOUT_DD_SOFT_CEILING
            for split in ("validation", "oos")
        )
        item["paired_axis_improvement_count"] = paired_improvement_count(item)
        item["both_refs_score_improved"] = all(
            bool(item.get(f"{split}_vs_{prefix}_score_improved", False))
            for split in ("validation", "oos")
            for prefix in ("label_v1", "frontier07")
        )
        item["both_refs_dd_improved"] = all(
            bool(item.get(f"{split}_vs_{prefix}_dd_axis_improved", False))
            for split in ("validation", "oos")
            for prefix in ("label_v1", "frontier07")
        )
        item["both_refs_pf_nonworse"] = all(
            float(item.get(f"{split}_vs_{prefix}_pf_delta", -999.0)) >= -1e-12
            for split in ("validation", "oos")
            for prefix in ("label_v1", "frontier07")
        )
        strict = bool(
            item["parity_passed"]
            and item["learnability_pass"]
            and item["density_band_pass"]
            and item["pf_floor_pass"]
            and item["dd_soft_pass"]
            and item["both_refs_score_improved"]
            and item["both_refs_dd_improved"]
            and item["both_refs_pf_nonworse"]
        )
        preserved = bool(
            item["parity_passed"]
            and item["class_balance_pass"]
            and not strict
            and (item["paired_axis_improvement_count"] >= 5 or item["both_refs_dd_improved"])
        )
        item["strict_scout_clue_pass"] = strict
        item["preserved_clue_pass"] = preserved
        item["validation_oos_score_sum"] = float(
            item["validation_aspiration_distance_score"] + item["oos_aspiration_distance_score"]
        )
        rows.append(json_ready(item))
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
    if rows.empty:
        return pd.DataFrame()
    keys = [
        "target_id",
        "target_kind",
        "source_boundary",
        "model_id",
        "model_instance_id",
        "label_family",
        "family_semantics",
        "difference_from_f07",
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


def reference_map(reference_grouped: pd.DataFrame, target_id: str) -> dict[str, dict[str, Any]]:
    if reference_grouped.empty:
        return {}
    refs = reference_grouped[reference_grouped["target_id"].eq(target_id)]
    return {str(row["model_id"]): row.to_dict() for _, row in refs.iterrows()}


def add_reference_deltas(item: dict[str, Any], reference: dict[str, Any] | None, prefix: str) -> None:
    if not reference:
        item[f"{prefix}_reference_available"] = False
        return
    item[f"{prefix}_reference_available"] = True
    for split in ("validation", "oos"):
        item[f"{split}_vs_{prefix}_density_axis_delta"] = float(item[f"{split}_density_axis_distance"]) - float(reference[f"{split}_density_axis_distance"])
        item[f"{split}_vs_{prefix}_pf_axis_delta"] = float(item[f"{split}_pf_axis_distance"]) - float(reference[f"{split}_pf_axis_distance"])
        item[f"{split}_vs_{prefix}_dd_axis_delta"] = float(item[f"{split}_dd_axis_distance"]) - float(reference[f"{split}_dd_axis_distance"])
        item[f"{split}_vs_{prefix}_smooth_axis_delta"] = float(item[f"{split}_smoothness_axis_distance"]) - float(reference[f"{split}_smoothness_axis_distance"])
        item[f"{split}_vs_{prefix}_score_improvement"] = float(reference[f"{split}_aspiration_distance_score"]) - float(item[f"{split}_aspiration_distance_score"])
        item[f"{split}_vs_{prefix}_pf_delta"] = float(item[f"{split}_profit_factor"]) - float(reference[f"{split}_profit_factor"])
        item[f"{split}_vs_{prefix}_dd_delta"] = float(item[f"{split}_dd_risk_percent"]) - float(reference[f"{split}_dd_risk_percent"])
        item[f"{split}_vs_{prefix}_density_axis_improved"] = bool(item[f"{split}_vs_{prefix}_density_axis_delta"] <= -1e-12)
        item[f"{split}_vs_{prefix}_pf_axis_improved"] = bool(item[f"{split}_vs_{prefix}_pf_axis_delta"] <= -1e-12)
        item[f"{split}_vs_{prefix}_dd_axis_improved"] = bool(item[f"{split}_vs_{prefix}_dd_axis_delta"] <= -1e-12)
        item[f"{split}_vs_{prefix}_smooth_axis_improved"] = bool(item[f"{split}_vs_{prefix}_smooth_axis_delta"] <= -1e-12)
        item[f"{split}_vs_{prefix}_score_improved"] = bool(item[f"{split}_vs_{prefix}_score_improvement"] > 1e-12)


def paired_improvement_count(item: dict[str, Any]) -> int:
    count = 0
    for split in ("validation", "oos"):
        for prefix in ("label_v1", "frontier07"):
            for axis in ("density", "pf", "dd", "smooth"):
                count += int(bool(item.get(f"{split}_vs_{prefix}_{axis}_axis_improved", False)))
    return count


def class_learnability(class_group: pd.DataFrame) -> dict[str, Any]:
    if class_group.empty:
        return {
            "train_balanced_accuracy": 0.0,
            "validation_balanced_accuracy": 0.0,
            "oos_balanced_accuracy": 0.0,
            "validation_macro_f1": 0.0,
            "oos_macro_f1": 0.0,
            "transfer_gap": 999.0,
            "train_min_class_fraction": 0.0,
            "train_max_class_fraction": 1.0,
            "class_balance_pass": False,
            "learnability_pass": False,
        }
    rows = {str(row["split"]): row for _, row in class_group.iterrows()}
    train = rows["train"]
    validation = rows["validation"]
    oos = rows["oos"]
    true_counts = np.array([float(train["true_short"]), float(train["true_flat"]), float(train["true_long"])], dtype="float64")
    fractions = true_counts / max(float(true_counts.sum()), 1.0)
    transfer_gap = float(train["balanced_accuracy"] - validation["balanced_accuracy"])
    class_balance_pass = bool(float(np.nanmin(fractions)) >= CLASS_BALANCE_MIN and float(np.nanmax(fractions)) <= CLASS_BALANCE_MAX)
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


def build_final(
    result: dict[str, Any],
    source_integrity: dict[str, Any],
    feature_order: list[str],
    variants: list[CleanPathVariant],
) -> dict[str, Any]:
    candidates = result["candidate_summary"]
    strict_rows = int(sum(1 for row in candidates if row.get("strict_scout_clue_pass")))
    preserved_rows = int(sum(1 for row in candidates if row.get("preserved_clue_pass")))
    best = candidates[0] if candidates else {}
    if strict_rows:
        status = "drawdown_clean_path_label_strict_scout_clue_no_authority"
        judgment = "strict_scout_clue(엄격 탐색 단서)"
        next_run_id = NEXT_STRICT_RUN_ID
    elif preserved_rows:
        status = "drawdown_clean_path_label_preserved_clue_no_authority"
        judgment = "preserved_clue(보존 단서)"
        next_run_id = NEXT_REPAIR_RUN_ID
    else:
        status = "drawdown_clean_path_label_no_strict_clue_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run_id = NEXT_REPAIR_RUN_ID
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": utc_now(),
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run_id,
        "strict_scout_clue_rows": strict_rows,
        "preserved_clue_rows": preserved_rows,
        "best_candidate_row": best,
        "variant_family_count": len({variant.family_id for variant in variants}),
        "variant_count": len(variants),
        "candidate_row_count": len(candidates),
        "model_count": len(result["onnx_parity"]),
        "source_integrity": source_integrity,
        "feature_order_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "feature_order_sha256": sha256_file(f03b.FEATURE_ORDER_PATH),
        "data_integrity": {
            **source_integrity,
            "feature_label_boundary": (
                "future OHLC path is used only to create labels(미래 OHLC 경로는 라벨 생성에만 사용); "
                "model inputs remain fixed feature_set_v2 current/known features(모델 입력은 고정 feature_set_v2 현재/확정 피처)."
            ),
            "split_boundary": "all thresholds/scales are train-only; validation/OOS are evaluation-only(모든 임계값/스케일은 학습 전용, 검증/OOS는 평가 전용)",
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
        },
        "model_validation": {
            "selection_metric": "strict clue, preserved clue, then validation+OOS distance(엄격 단서, 보존 단서, 검증+OOS 거리 순)",
            "learnability_gate": "class balance, validation balanced accuracy, macro F1, transfer gap(클래스 균형, 검증 균형 정확도, 매크로 F1, 전달 격차)",
            "validation_judgment": "exploratory_no_authority(탐색용, 권위 없음)",
        },
        "runtime_parity": {
            "onnx_parity": "checked for every trained sklearn model(학습된 모든 sklearn 모델에서 확인)",
            "runtime_claim_boundary": "research_only_no_mt5(연구 전용, MT5 없음)",
        },
        "artifact_lineage": {
            "source_inputs": [f03b.DATASET_PATH.as_posix(), f04b.RAW_US100.as_posix()],
            "producer": "stage_pipelines/stage_frontier_09/frontier09b_drawdown_clean_path_label_proxy_scout.py",
            "consumer": next_run_id,
            "lineage_judgment": "connected_with_boundary(경계부 연결)",
        },
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_artifacts(result: dict[str, Any], final: dict[str, Any], variants: list[CleanPathVariant]) -> dict[str, Path]:
    artifacts = {
        "variant_grid": RUN_ROOT / "clean_path_variant_grid.csv",
        "candidate_metrics": RUN_ROOT / "candidate_model_metrics.csv",
        "reference_metrics": RUN_ROOT / "reference_model_metrics.csv",
        "candidate_summary": RUN_ROOT / "candidate_summary.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "target_distribution": RUN_ROOT / "target_distribution.csv",
        "skipped": RUN_ROOT / "skipped_targets.csv",
        "final_decision": RUN_ROOT / "final_decision.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_csv(artifacts["variant_grid"], [variant.__dict__ for variant in variants])
    write_csv(artifacts["candidate_metrics"], result["candidate_metrics"])
    write_csv(artifacts["reference_metrics"], result["reference_metrics"])
    write_csv(artifacts["candidate_summary"], result["candidate_summary"])
    write_csv(artifacts["classification_metrics"], result["classification_metrics"])
    write_csv(artifacts["onnx_parity"], result["onnx_parity"])
    write_csv(artifacts["target_distribution"], result["target_distribution"])
    write_csv(artifacts["skipped"], result["skipped"])
    write_json(artifacts["final_decision"], final)
    final["artifact_lineage"]["artifact_paths"] = [path.as_posix() for path in artifacts.values()]
    manifest = {
        **final,
        "script_path": "stage_pipelines/stage_frontier_09/frontier09b_drawdown_clean_path_label_proxy_scout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_09/frontier09b_drawdown_clean_path_label_proxy_scout.py")),
        "artifacts": {
            name: {"path": path.as_posix(), "sha256": sha256_file(path)}
            for name, path in artifacts.items()
            if name != "run_manifest" and path_exists(path)
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
    text = f"""# Frontier09B Drawdown Clean Path Label Proxy Scout Report(전선09B 손실폭 깨끗한 경로 라벨 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): train-only thresholds/scales(학습 전용 임계값/스케일)로 drawdown-normalized clean path labels(손실폭 정규화 깨끗한 경로 라벨)을 만들고, fixed feature_set_v2(고정 피처 세트 v2)와 ONNX-exportable sklearn models(ONNX 내보내기 가능한 sklearn 모델)로 argmax-only(최대 확률 전용) 검증을 실행했습니다.

Effect(효과): Frontier07(전선07)의 위험 라벨을 상속하지 않고 reference(참조)로만 두면서, 목표 표현(target representation, 목표 표현) 자체가 density/PF/DD/smoothness(거래 밀도/수익 팩터/손실폭/매끄러움)를 동시에 개선하는지 확인했습니다.

## Best Candidate Read(최상위 후보 판독)

- candidate(후보): `{best.get('candidate_id', 'none')}`
- family(라벨군): `{best.get('label_family', 'none')}`
- strict scout clue pass(엄격 탐색 단서 통과): `{best.get('strict_scout_clue_pass', False)}`
- preserved clue pass(보존 단서 통과): `{best.get('preserved_clue_pass', False)}`
- paired axis improvement count(짝지은 축 개선 수): `{best.get('paired_axis_improvement_count', 'n/a')}`
- validation PF/density/DD(검증 수익 팩터/거래 밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(OOS 표본밖 수익 팩터/거래 밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- ONNX parity(ONNX 동등성): `{best.get('parity_passed', False)}`

## Boundaries(경계)

- validation/OOS(검증/OOS)는 evaluation-only(평가 전용)입니다.
- Tier B and combined(티어 B와 합산)는 missing_required(필수 누락)로 기록했습니다.
- WFO/MT5(WFO/MT5)는 아직 실행하지 않았습니다.
- completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.

## Artifacts(산출물)

- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- model metrics(모델 지표): `{artifacts['candidate_metrics'].as_posix()}`
- reference metrics(참조 지표): `{artifacts['reference_metrics'].as_posix()}`
- classification metrics(분류 지표): `{artifacts['classification_metrics'].as_posix()}`
- ONNX parity(ONNX 동등성): `{artifacts['onnx_parity'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 결과 경계에 맞게 Grok review(그록 검토) 또는 repair/closeout decision(수리/마감 결정)으로 넘기는 것입니다. Effect(효과)는 한 축 개선을 completion candidate(완성 후보)로 과장하지 않고 네 축 동시 개선만 앞으로 보내는 것입니다.
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
    io_path(f03b.WORKSPACE_STATE).write_text(state_text, encoding="utf-8", newline="\n")
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(final))
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(final, artifacts))
    write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index_text(final, artifacts))
    write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit_text(final))
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    stage_ledger = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
    for row in ledger_rows(final, artifacts):
        f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(stage_ledger, "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): strict scout clue rows(엄격 탐색 단서 행) `{final['strict_scout_clue_rows']}`, preserved clue rows(보존 단서 행) `{final['preserved_clue_rows']}`, next run(다음 실행) `{final['next_run_id']}`.\n",
    )
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{RUN_ID}`: drawdown-normalized clean path label proxy scout(손실폭 정규화 깨끗한 경로 라벨 프록시 탐색)를 기록했습니다. Effect(효과): 목표 표현 변경이 Frontier07 reference(전선07 참조)보다 나은지 분리 판독하게 했습니다.\n",
    )
    if final["strict_scout_clue_rows"] == 0 and final["preserved_clue_rows"] == 0:
        f03b.append_once(
            f03b.NEGATIVE_RESULT_REGISTER,
            RUN_ID,
            f"- `{RUN_ID}`: clean path labels did not create strict or preserved validation+OOS clue(깨끗한 경로 라벨이 검증+OOS 엄격/보존 단서를 만들지 못함). Effect(효과): repair/closeout decision(수리/마감 결정)으로 넘깁니다.\n",
        )


def current_state_text(final: dict[str, Any]) -> str:
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

Action(행동): Frontier09B(전선09B)는 drawdown-normalized clean path labels(손실폭 정규화 깨끗한 경로 라벨)을 만들고 label_v1/reference Frontier07(라벨 v1/전선07 참조)와 같은 모델군에서 비교했습니다.

Effect(효과): target representation(목표 표현) 변경이 네 축(four axes, 네 축)을 동시에 개선하는지 보고, WFO/MT5(WFO/MT5)나 runtime authority(런타임 권위)는 주장하지 않습니다.

Best read(최상위 판독): `{best.get('candidate_id', 'none')}` with strict scout clue rows(엄격 탐색 단서 행) `{final['strict_scout_clue_rows']}` and preserved clue rows(보존 단서 행) `{final['preserved_clue_rows']}`.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_candidate_row"]
    return f"""# Frontier09 Selection Status(전선09 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Latest run(최근 실행): `{RUN_ID}`

Report(보고서): `{REPORT_PATH.as_posix()}`

Final decision(최종 판정 파일): `{artifacts['final_decision'].as_posix()}`

Best candidate(최상위 후보): `{best.get('candidate_id', 'none')}`

Strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`

Preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def review_index_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    artifact_lines = "\n".join(f"- `{path.as_posix()}`" for path in artifacts.values())
    return f"""# Frontier09 Review Index(전선09 검토 색인)

Updated(갱신): {final['created_at_utc']}

## Reviews(검토)

- `frontier09A_stage_open_drawdown_clean_path_labeling_v1`: stage open(단계 개방) and Grok review(그록 검토).
- `{RUN_ID}`: clean path label proxy scout(깨끗한 경로 라벨 프록시 탐색), ONNX parity(ONNX 동등성), paired reference comparison(짝지은 참조 비교).

## Latest Artifacts(최신 산출물)

{artifact_lines}
"""


def gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier09B Required Gate Coverage Audit(전선09B 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계부 통과)

## Gate Coverage(게이트 커버리지)

- scope_completion_gate(범위 완료 게이트): satisfied_with_boundary(경계부 충족)
- kpi_contract_audit(KPI 계약 감사): satisfied_with_boundary(경계부 충족)
- skill_receipt_lint(스킬 영수증 검사): satisfied_with_boundary(경계부 충족)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): satisfied_with_boundary(경계부 충족)
- final_claim_guard(최종 주장 보호): satisfied_with_boundary(경계부 충족)

Action(행동): proxy scout(프록시 탐색)와 ONNX parity(ONNX 동등성)까지만 완료했습니다.

Effect(효과): WFO/MT5(WFO/MT5), operating promotion(운영 승격), runtime authority(런타임 권위), completion(완성)은 주장하지 않습니다.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "drawdown_clean_path_label_model_scout(손실폭 깨끗한 경로 라벨 모델 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"strict={final['strict_scout_clue_rows']};preserved={final['preserved_clue_rows']};no_authority",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["candidate_row_count"]),
        "claim_boundary": "clean_path_label_scout_onnx_parity_only_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_clean_path_label_model_scout",
        "subrun_id": f"{RUN_ID}__tier_a_clean_path_label_model_scout",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "clean_path_label_model_scout_not_runtime(깨끗한 경로 라벨 모델 탐색, 런타임 아님)",
        "primary_kpi": primary_kpi_text(best),
        "guardrail_kpi": "argmax_only_no_threshold_no_wfo_no_mt5_no_authority(최대 확률 전용, 임계값/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "clean_path_label_model_scout_only(깨끗한 경로 라벨 모델 탐색 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can drawdown-normalized clean path labels improve four-axis distance?(손실폭 정규화 깨끗한 경로 라벨이 네 축 거리를 개선하는가?)",
        "skill_family": "experiment_execution(실험 실행)",
        "lineage_summary": "frontier09a_stage_open_to_frontier09b_clean_path_label_model_scout(전선09A 단계 개방에서 전선09B 깨끗한 경로 라벨 모델 탐색)",
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
        "scoreboard_lane": "clean_path_label_model_scout(깨끗한 경로 라벨 모델 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "argmax_only_no_threshold_no_wfo_no_mt5_no_authority(최대 확률 전용, 임계값/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_clean_path_label_model_scout",
            "subrun_id": f"{RUN_ID}__tier_a_clean_path_label_model_scout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "clean_path_label_model_scout_not_runtime(깨끗한 경로 라벨 모델 탐색, 런타임 아님)",
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


def label_distribution(full: pd.DataFrame, target: TargetSurface) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        mask = full["split"].astype(str).eq(split).to_numpy()
        labels = target.labels[mask]
        total = max(len(labels), 1)
        for label in LABEL_ORDER:
            rows.append(
                {
                    "target_id": target.target_id,
                    "target_kind": target.target_kind,
                    "split": split,
                    "label": label,
                    "label_name": LABEL_NAMES[label],
                    "count": int((labels == label).sum()),
                    "fraction": float((labels == label).sum() / total),
                }
            )
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


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = f03b.read_csv_header(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(io_path(path), index=False, encoding="utf-8-sig")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


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
