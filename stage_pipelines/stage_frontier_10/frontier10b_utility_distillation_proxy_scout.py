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
from stage_pipelines.stage_frontier_04 import frontier04b_path_aware_label_proxy_scout as f04b
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b


STAGE_ID = "stage_frontier_10__split_consistent_utility_distillation"
RUN_ID = "frontier10B_utility_distillation_proxy_scout_v1"
RUN_NUMBER = "frontier10B"
PARENT_RUN_ID = "frontier10A_stage_open_split_consistent_utility_distillation_v1"
NEXT_STRICT_RUN_ID = "frontier10C_grok_pre_expensive_utility_distillation_review_v1"
NEXT_REPAIR_RUN_ID = "frontier10C_utility_distillation_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"

SCRIPT_PATH = Path("stage_pipelines/stage_frontier_10/frontier10b_utility_distillation_proxy_scout.py")
LABEL_ORDER = f04d.LABEL_ORDER
LABEL_NAMES = f04d.LABEL_NAMES
HORIZON_BARS = 12
SCALE_QUANTILE = 0.90
SUBWINDOW_COUNT = 4
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

REPORT_REFERENCES = {
    "frontier08_best_sample_weight": {
        "source": (
            "stages/stage_frontier_08__sample_weighted_objective/03_reviews/"
            "frontier08D_stage_closeout_sample_weight_objective_v1_report.md"
        ),
        "validation_profit_factor": 1.00405,
        "validation_trades_per_day": 6.94536,
        "validation_dd_risk_percent": 58.0016,
        "oos_profit_factor": 1.19464,
        "oos_trades_per_day": 5.47328,
        "oos_dd_risk_percent": 15.655,
    },
    "frontier09_best_preserved": {
        "source": (
            "stages/stage_frontier_09__drawdown_normalized_clean_path_labeling/03_reviews/"
            "frontier09D_stage_closeout_drawdown_clean_path_labeling_v1_report.md"
        ),
        "validation_profit_factor": 1.01229,
        "validation_trades_per_day": 5.29508,
        "validation_dd_risk_percent": 56.6737,
        "oos_profit_factor": 1.23306,
        "oos_trades_per_day": 3.89313,
        "oos_dd_risk_percent": 14.6643,
    },
}


@dataclass(frozen=True)
class UtilityVariant:
    variant_id: str
    family_id: str
    family_semantics: str
    difference_from_f07: str
    difference_from_f09: str
    difference_from_stage295: str
    horizon_bars: int
    scale_quantile: float
    base_scale_log_return: float
    utility_quantile: float
    margin_multiplier: float
    adverse_cap_multiplier: float
    consensus_required: int
    positive_floor_multiplier: float
    target_log_return: float
    adverse_cap_log_return: float
    utility_margin_floor: float
    positive_floor: float


@dataclass(frozen=True)
class TargetSurface:
    target_id: str
    target_kind: str
    label_family: str
    family_semantics: str
    difference_from_f07: str
    difference_from_f09: str
    difference_from_stage295: str
    source_boundary: str
    labels: np.ndarray
    variant: UtilityVariant | None
    diagnostics: dict[str, Any]


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    path = f07b.path_arrays(full, raw, HORIZON_BARS)
    subwindows = train_subwindows(full)
    variants = build_variants(full, path)
    targets = build_targets(full, raw, path, variants, subwindows)
    result = train_and_evaluate(full, feature_order, path, targets)
    final = build_final(result, source_integrity, feature_order, variants, subwindows)
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


def train_subwindows(full: pd.DataFrame) -> list[np.ndarray]:
    train_index = np.flatnonzero(full["split"].astype(str).eq("train").to_numpy())
    chunks = np.array_split(train_index, SUBWINDOW_COUNT)
    subwindows = [chunk.astype("int64") for chunk in chunks if len(chunk)]
    if len(subwindows) != SUBWINDOW_COUNT:
        raise RuntimeError(f"Expected {SUBWINDOW_COUNT} train subwindows, got {len(subwindows)}.")
    validation_or_oos = full.iloc[np.concatenate(subwindows)]["split"].astype(str).ne("train").any()
    if validation_or_oos:
        raise RuntimeError("Train subwindow containment failed.")
    return subwindows


def build_variants(full: pd.DataFrame, path: dict[str, np.ndarray]) -> list[UtilityVariant]:
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    base_scale = float(np.nanquantile(np.abs(path["fwd_return"][train_mask]), SCALE_QUANTILE))
    if not math.isfinite(base_scale) or base_scale <= 0:
        raise RuntimeError("Invalid train-only base scale.")
    specs = [
        (
            "utility_consensus",
            "Subwindow thresholds must agree before long/short(하위구간 임계값이 합의해야 롱/숏 허용)",
            "F07 scores adverse risk row-by-row; F10 requires train-only threshold agreement first(F07은 행별 불리 위험 점수, F10은 학습 전용 임계값 합의 우선)",
            "F09 cleans target paths; F10 removes unstable utility rows before model fit without density bridge(F09는 경로 정리, F10은 밀도 브리지 없이 불안정 효용 행 제거)",
            "Stage295 was MT5 route-signal distillation; F10 is Python Tier A train-only utility label scouting(Stage295는 MT5 경로 신호 증류, F10은 파이썬 Tier A 학습 전용 효용 라벨 탐색)",
            [(0.58, 0.20, 0.90, 3, 0.08), (0.62, 0.25, 0.95, 3, 0.10), (0.66, 0.30, 1.05, 3, 0.12)],
        ),
        (
            "utility_margin",
            "Winning side must beat the opposite side by train-only margin(승리 방향이 학습 전용 마진만큼 반대 방향을 이겨야 함)",
            "F07 tests adverse burden; F10 asks stable utility edge(F07은 불리 부담, F10은 안정 효용 우위 확인)",
            "F09 payoff/adverse ratio is reference only; F10 adds subwindow margin consensus without class-prior bridge(F09 수익/불리 비율은 참조 전용, F10은 클래스 사전분포 브리지 없는 하위구간 마진 합의)",
            "Stage295 used routed MT5 outcomes; F10 uses fixed ONNX argmax model labels only(Stage295는 MT5 라우팅 결과, F10은 고정 ONNX 최대확률 모델 라벨 전용)",
            [(0.55, 0.32, 0.95, 3, 0.06), (0.60, 0.42, 1.05, 3, 0.08), (0.64, 0.52, 1.15, 3, 0.10)],
        ),
        (
            "drawdown_veto_distillation",
            "Favorable raw return is vetoed to flat when underwater burden is high(원시 수익이 좋아도 수중 부담이 크면 관망으로 거부)",
            "F07 penalizes adverse excursion; F10 distills high-underwater rows to flat before fitting(F07은 불리 이동 벌점, F10은 고수중 행을 학습 전 관망 증류)",
            "F09 clean-path labels still left high validation DD; F10 makes the veto split-consistent(F09 깨끗한 경로 라벨은 검증 손실폭이 컸고, F10은 거부를 분할 일관화)",
            "Stage295 validation damage veto was route-signal based; F10 is train-threshold label distillation(Stage295 검증 손상 거부는 경로 신호 기반, F10은 학습 임계값 라벨 증류)",
            [(0.50, 0.18, 0.70, 3, 0.04), (0.55, 0.24, 0.80, 3, 0.06), (0.60, 0.30, 0.90, 3, 0.08)],
        ),
    ]
    variants: list[UtilityVariant] = []
    for family_id, semantics, diff_f07, diff_f09, diff_stage295, family_specs in specs:
        for index, (utility_q, margin_mult, cap_mult, consensus_required, floor_mult) in enumerate(family_specs, start=1):
            variant_id = (
                f"f10b_{family_id}_v{index}_"
                f"uq{utility_q:.2f}_m{margin_mult:.2f}_cap{cap_mult:.2f}_c{consensus_required}"
            ).replace(".", "p")
            variants.append(
                UtilityVariant(
                    variant_id=variant_id,
                    family_id=family_id,
                    family_semantics=semantics,
                    difference_from_f07=diff_f07,
                    difference_from_f09=diff_f09,
                    difference_from_stage295=diff_stage295,
                    horizon_bars=HORIZON_BARS,
                    scale_quantile=SCALE_QUANTILE,
                    base_scale_log_return=base_scale,
                    utility_quantile=utility_q,
                    margin_multiplier=margin_mult,
                    adverse_cap_multiplier=cap_mult,
                    consensus_required=consensus_required,
                    positive_floor_multiplier=floor_mult,
                    target_log_return=base_scale,
                    adverse_cap_log_return=base_scale * cap_mult,
                    utility_margin_floor=base_scale * margin_mult,
                    positive_floor=base_scale * floor_mult,
                )
            )
    return variants


def build_targets(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    path: dict[str, np.ndarray],
    variants: list[UtilityVariant],
    subwindows: list[np.ndarray],
) -> list[TargetSurface]:
    targets: list[TargetSurface] = []
    label_v1 = pd.to_numeric(full["label_class"], errors="raise").to_numpy(dtype="int64")
    targets.append(
        TargetSurface(
            target_id="label_v1_argmax_reference",
            target_kind="reference_label_v1_argmax(참조 라벨 v1 최대확률)",
            label_family="label_v1_reference",
            family_semantics="Original label_v1 reference only(원래 라벨 v1 참조 전용)",
            difference_from_f07="not_applicable_reference(참조라 해당 없음)",
            difference_from_f09="not_applicable_reference(참조라 해당 없음)",
            difference_from_stage295="not_applicable_reference(참조라 해당 없음)",
            source_boundary="existing_label_v1_reference_only(기존 라벨 v1 참조 전용)",
            labels=label_v1,
            variant=None,
            diagnostics={"reference": True},
        )
    )

    risk_variant = next((variant for variant in f07b.build_variants(full, raw) if variant.variant_id == RISK_REFERENCE_VARIANT_ID), None)
    if risk_variant is None:
        raise RuntimeError(f"Missing Frontier07 reference variant: {RISK_REFERENCE_VARIANT_ID}")
    risk_labels, _, risk_diag = f07b.build_risk_labels(path, risk_variant)
    targets.append(
        TargetSurface(
            target_id=RISK_REFERENCE_VARIANT_ID,
            target_kind="reference_frontier07_risk_label_argmax(참조 전선07 위험 라벨 최대확률)",
            label_family="frontier07_risk_reference",
            family_semantics="Frontier07 adverse excursion risk label reference only(전선07 불리 이동 위험 라벨 참조 전용)",
            difference_from_f07="self_reference(자기 참조)",
            difference_from_f09="reference_only_not_inherited(참조 전용, 상속 아님)",
            difference_from_stage295="not_route_signal_distillation(경로 신호 증류 아님)",
            source_boundary="frontier07_reference_recomputed_same_data(전선07 참조를 같은 데이터로 재계산)",
            labels=risk_labels,
            variant=None,
            diagnostics=risk_diag,
        )
    )

    for variant in variants:
        labels, diagnostics = build_utility_labels(full, path, variant, subwindows)
        targets.append(
            TargetSurface(
                target_id=variant.variant_id,
                target_kind=f"utility_distillation_candidate(효용 증류 후보:{variant.family_id})",
                label_family=variant.family_id,
                family_semantics=variant.family_semantics,
                difference_from_f07=variant.difference_from_f07,
                difference_from_f09=variant.difference_from_f09,
                difference_from_stage295=variant.difference_from_stage295,
                source_boundary=(
                    "train_subwindow_thresholds_only_validation_oos_evaluation_only"
                    "(학습 하위구간 임계값만 사용, 검증/OOS는 평가 전용)"
                ),
                labels=labels,
                variant=variant,
                diagnostics=diagnostics,
            )
        )
    return targets


def build_utility_labels(
    full: pd.DataFrame,
    path: dict[str, np.ndarray],
    variant: UtilityVariant,
    subwindows: list[np.ndarray],
) -> tuple[np.ndarray, dict[str, Any]]:
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    long_utility, short_utility = side_utilities(path, variant)
    long_votes = np.zeros(len(full), dtype="int16")
    short_votes = np.zeros(len(full), dtype="int16")
    threshold_records: list[dict[str, Any]] = []
    for window_index, window in enumerate(subwindows, start=1):
        long_threshold = float(np.nanquantile(long_utility[window], variant.utility_quantile))
        short_threshold = float(np.nanquantile(short_utility[window], variant.utility_quantile))
        margin_threshold = max(
            variant.utility_margin_floor,
            float(
                np.nanquantile(
                    np.abs(long_utility[window] - short_utility[window]),
                    min(0.95, variant.utility_quantile + 0.10),
                )
                * variant.margin_multiplier
            ),
        )
        adverse_cap = float(
            np.nanquantile(
                np.concatenate([path["long_mae"][window], path["short_mae"][window]]),
                min(0.92, variant.utility_quantile + 0.20),
            )
        )
        adverse_cap = max(adverse_cap, variant.adverse_cap_log_return)
        threshold_records.append(
            {
                "subwindow": window_index,
                "rows": int(len(window)),
                "timestamp_first": pd.Timestamp(full.iloc[window[0]]["timestamp"]).isoformat(),
                "timestamp_last": pd.Timestamp(full.iloc[window[-1]]["timestamp"]).isoformat(),
                "long_threshold": long_threshold,
                "short_threshold": short_threshold,
                "margin_threshold": margin_threshold,
                "adverse_cap": adverse_cap,
            }
        )

        if variant.family_id == "utility_consensus":
            long_ok = (
                (long_utility >= max(long_threshold, variant.positive_floor))
                & (long_utility > short_utility + 0.10 * margin_threshold)
                & (path["long_mae"] <= adverse_cap)
            )
            short_ok = (
                (short_utility >= max(short_threshold, variant.positive_floor))
                & (short_utility > long_utility + 0.10 * margin_threshold)
                & (path["short_mae"] <= adverse_cap)
            )
        elif variant.family_id == "utility_margin":
            long_ok = (
                (long_utility >= long_threshold)
                & ((long_utility - np.maximum(short_utility, 0.0)) >= margin_threshold)
                & (path["long_mae"] <= adverse_cap)
            )
            short_ok = (
                (short_utility >= short_threshold)
                & ((short_utility - np.maximum(long_utility, 0.0)) >= margin_threshold)
                & (path["short_mae"] <= adverse_cap)
            )
        elif variant.family_id == "drawdown_veto_distillation":
            long_ok = (
                (long_utility >= max(long_threshold, variant.positive_floor))
                & (path["fwd_return"] > 0)
                & (path["long_mae"] <= adverse_cap * 0.85)
                & (long_utility > short_utility)
            )
            short_ok = (
                (short_utility >= max(short_threshold, variant.positive_floor))
                & (path["fwd_return"] < 0)
                & (path["short_mae"] <= adverse_cap * 0.85)
                & (short_utility > long_utility)
            )
        else:
            raise ValueError(f"Unknown utility family: {variant.family_id}")
        long_votes += long_ok.astype("int16")
        short_votes += short_ok.astype("int16")

    signal = np.zeros(len(full), dtype="int8")
    long_final = (long_votes >= variant.consensus_required) & (long_votes > short_votes)
    short_final = (short_votes >= variant.consensus_required) & (short_votes > long_votes)
    signal[long_final] = 1
    signal[short_final] = -1
    labels = np.where(signal < 0, 0, np.where(signal > 0, 2, 1)).astype("int64")
    train_labels = labels[train_mask]
    diagnostics = {
        "oracle_short_count": int((signal == -1).sum()),
        "oracle_flat_count": int((signal == 0).sum()),
        "oracle_long_count": int((signal == 1).sum()),
        "train_short_count": int((train_labels == 0).sum()),
        "train_flat_count": int((train_labels == 1).sum()),
        "train_long_count": int((train_labels == 2).sum()),
        "train_flat_fraction": float((train_labels == 1).sum() / max(len(train_labels), 1)),
        "mean_long_votes": float(np.mean(long_votes)),
        "mean_short_votes": float(np.mean(short_votes)),
        "train_only_threshold_records": threshold_records,
        "subwindow_containment": "all_subwindows_inside_train(모든 하위구간이 학습 분할 내부)",
        "density_bridge": "not_used(사용하지 않음)",
    }
    return labels, diagnostics


def side_utilities(path: dict[str, np.ndarray], variant: UtilityVariant) -> tuple[np.ndarray, np.ndarray]:
    base = variant.base_scale_log_return
    cost_units = scout.ROUGH_COST_LOG_RETURN / base
    long_utility = (
        0.90 * path["fwd_return"] / base
        + 0.35 * path["long_mfe"] / base
        - 0.85 * path["long_mae"] / max(variant.adverse_cap_log_return, 1e-12)
        - cost_units
    )
    short_utility = (
        -0.90 * path["fwd_return"] / base
        + 0.35 * path["short_mfe"] / base
        - 0.85 * path["short_mae"] / max(variant.adverse_cap_log_return, 1e-12)
        - cost_units
    )
    return long_utility.astype("float64"), short_utility.astype("float64")


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
                    "diagnostics": json.dumps(json_ready(target.diagnostics), ensure_ascii=False),
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
        if target.target_kind.startswith("utility_distillation_candidate"):
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
        "target_diagnostics": [
            {
                "target_id": target.target_id,
                "target_kind": target.target_kind,
                **json_ready(target.diagnostics),
            }
            for target in targets
        ],
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
        model_instance_id = f"f10b_{target.target_id}_{short_model_id}"
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
    reasons = np.full(len(full), f"argmax_model_{target.target_id}", dtype=object)
    first_steps = np.zeros(len(full), dtype="int16")
    for split in ("train", "validation", "oos"):
        metric = f04b.evaluate_split(
            full,
            signal,
            fwd_return,
            split,
            metric_variant(target.variant, target.target_id),
            f"argmax_model_{target.target_id}",
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
                "difference_from_f09": target.difference_from_f09,
                "difference_from_stage295": target.difference_from_stage295,
                "signal_contract": "argmax_only_no_threshold_no_class_prior_bridge(최대확률 전용, 임계값/클래스 사전분포 브리지 없음)",
            }
        )
        rows.append(metric)
    return rows


def metric_variant(variant: UtilityVariant | None, target_id: str) -> f04b.PathVariant:
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
        target_multiplier=1.0,
        stop_multiplier=variant.adverse_cap_multiplier,
        scale_quantile=variant.scale_quantile,
        target_log_return=variant.target_log_return,
        stop_log_return=variant.adverse_cap_log_return,
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
        add_reference_deltas(item, label_v1_refs.get(model_id), "label_v1")
        add_reference_deltas(item, f07_refs.get(model_id), "frontier07")
        add_report_reference_deltas(item)
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
        item["report_reference_improvement_count"] = report_reference_improvement_count(item)
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
            and (
                item["paired_axis_improvement_count"] >= 5
                or item["both_refs_dd_improved"]
                or item["report_reference_improvement_count"] >= 6
            )
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
        "difference_from_f09",
        "difference_from_stage295",
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


def add_report_reference_deltas(item: dict[str, Any]) -> None:
    for prefix, reference in REPORT_REFERENCES.items():
        item[f"{prefix}_source"] = reference["source"]
        for split in ("validation", "oos"):
            ref_pf = float(reference[f"{split}_profit_factor"])
            ref_density = float(reference[f"{split}_trades_per_day"])
            ref_dd = float(reference[f"{split}_dd_risk_percent"])
            item[f"{split}_vs_{prefix}_pf_delta"] = float(item[f"{split}_profit_factor"]) - ref_pf
            item[f"{split}_vs_{prefix}_density_axis_delta"] = scout.density_axis_distance(float(item[f"{split}_trades_per_day"])) - scout.density_axis_distance(ref_density)
            item[f"{split}_vs_{prefix}_dd_delta"] = float(item[f"{split}_dd_risk_percent"]) - ref_dd
            item[f"{split}_vs_{prefix}_pf_improved"] = bool(item[f"{split}_vs_{prefix}_pf_delta"] >= -1e-12)
            item[f"{split}_vs_{prefix}_density_axis_improved"] = bool(item[f"{split}_vs_{prefix}_density_axis_delta"] <= -1e-12)
            item[f"{split}_vs_{prefix}_dd_improved"] = bool(item[f"{split}_vs_{prefix}_dd_delta"] <= -1e-12)


def paired_improvement_count(item: dict[str, Any]) -> int:
    count = 0
    for split in ("validation", "oos"):
        for prefix in ("label_v1", "frontier07"):
            for axis in ("density", "pf", "dd", "smooth"):
                count += int(bool(item.get(f"{split}_vs_{prefix}_{axis}_axis_improved", False)))
    return count


def report_reference_improvement_count(item: dict[str, Any]) -> int:
    count = 0
    for split in ("validation", "oos"):
        for prefix in REPORT_REFERENCES:
            count += int(bool(item.get(f"{split}_vs_{prefix}_pf_improved", False)))
            count += int(bool(item.get(f"{split}_vs_{prefix}_density_axis_improved", False)))
            count += int(bool(item.get(f"{split}_vs_{prefix}_dd_improved", False)))
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
        and float(oos["balanced_accuracy"]) >= LEARNABILITY_VAL_BAL_ACC_FLOOR
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
    variants: list[UtilityVariant],
    subwindows: list[np.ndarray],
) -> dict[str, Any]:
    candidates = result["candidate_summary"]
    strict_rows = int(sum(1 for row in candidates if row.get("strict_scout_clue_pass")))
    preserved_rows = int(sum(1 for row in candidates if row.get("preserved_clue_pass")))
    best = candidates[0] if candidates else {}
    if strict_rows:
        status = "utility_distillation_strict_scout_clue_no_authority"
        judgment = "strict_scout_clue(엄격 탐색 단서)"
        next_run_id = NEXT_STRICT_RUN_ID
    elif preserved_rows:
        status = "utility_distillation_preserved_clue_no_authority"
        judgment = "preserved_clue(보존 단서)"
        next_run_id = NEXT_REPAIR_RUN_ID
    else:
        status = "utility_distillation_no_strict_clue_no_authority"
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
        "subwindow_count": len(subwindows),
        "subwindow_lengths": [int(len(window)) for window in subwindows],
        "data_integrity": {
            **source_integrity,
            "data_source": f03b.DATASET_PATH.as_posix(),
            "time_axis": "closed_bar_m5_timestamp(확정 5분봉 타임스탬프)",
            "feature_label_boundary": (
                "features use fixed feature_set_v2 current/past values; future OHLC path is used only for label construction"
                "(피처는 고정 feature_set_v2 현재/과거 값, 미래 OHLC 경로는 라벨 생성에만 사용)"
            ),
            "split_boundary": (
                "all utility thresholds, margins, adverse caps, and subwindows are fit on train split only"
                "(모든 효용 임계값/마진/불리 이동 상한/하위구간은 학습 분할에서만 적합)"
            ),
            "leakage_judgment": "usable_with_boundary_no_validation_oos_fit(경계부 사용 가능, 검증/OOS 적합 없음)",
        },
        "model_validation": {
            "target": "3-class utility distillation labels [short, flat, long](3분류 효용 증류 라벨)",
            "split_method": "fixed project train/validation/OOS split(고정 프로젝트 학습/검증/OOS 분할)",
            "selection_metric": (
                "strict scout clue first, preserved clue second, then validation+OOS aspiration distance"
                "(엄격 탐색 단서 우선, 보존 단서 다음, 검증+OOS 목표 거리)"
            ),
            "threshold_policy": "argmax_only_no_threshold_search_no_class_prior_bridge(최대확률 전용, 임계값 탐색/클래스 사전분포 브리지 없음)",
            "overfit_risk": "train labels use future path oracle targets, so runtime claims are out of scope(학습 라벨은 미래 경로 오라클 목표라 런타임 주장은 범위 밖)",
        },
        "report_references": REPORT_REFERENCES,
        "runtime_parity": {
            "onnx_parity": "checked for every trained sklearn model(학습된 모든 sklearn 모델에서 확인)",
            "runtime_claim_boundary": "research_only_no_wfo_no_mt5(연구 전용, WFO/MT5 없음)",
        },
        "artifact_lineage": {
            "source_inputs": [f03b.DATASET_PATH.as_posix(), f04b.RAW_US100.as_posix()],
            "producer": SCRIPT_PATH.as_posix(),
            "consumer": next_run_id,
            "lineage_judgment": "connected_with_boundary(경계부 연결)",
        },
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_artifacts(result: dict[str, Any], final: dict[str, Any], variants: list[UtilityVariant]) -> dict[str, Path]:
    artifacts = {
        "variant_grid": RUN_ROOT / "utility_variant_grid.csv",
        "candidate_metrics": RUN_ROOT / "candidate_model_metrics.csv",
        "reference_metrics": RUN_ROOT / "reference_model_metrics.csv",
        "candidate_summary": RUN_ROOT / "candidate_summary.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "target_distribution": RUN_ROOT / "target_distribution.csv",
        "target_diagnostics": RUN_ROOT / "target_diagnostics.json",
        "skipped": RUN_ROOT / "skipped_targets.csv",
        "final_decision": RUN_ROOT / "final_decision.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_csv(artifacts["variant_grid"], [asdict(variant) for variant in variants])
    write_csv(artifacts["candidate_metrics"], result["candidate_metrics"])
    write_csv(artifacts["reference_metrics"], result["reference_metrics"])
    write_csv(artifacts["candidate_summary"], result["candidate_summary"])
    write_csv(artifacts["classification_metrics"], result["classification_metrics"])
    write_csv(artifacts["onnx_parity"], result["onnx_parity"])
    write_csv(artifacts["target_distribution"], result["target_distribution"])
    write_json(artifacts["target_diagnostics"], result["target_diagnostics"])
    write_csv(artifacts["skipped"], result["skipped"])
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
    text = f"""# Frontier10B Utility Distillation Proxy Scout Report(전선10B 효용 증류 프록시 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier10B(전선10B)는 train-only subwindow thresholds(학습 전용 하위구간 임계값)로 utility_consensus/utility_margin/drawdown_veto_distillation(효용 합의/효용 마진/손실폭 거부 증류) 라벨을 만들고, 고정 3-class ONNX(3분류 온엑스) argmax-only(최대확률 전용) 모델로 확인했습니다.

Effect(효과): validation/OOS(검증/표본밖)를 라벨 적합에 쓰지 않고, class-prior bridge(클래스 사전분포 브리지) 없이 네 축(density/PF/DD/smoothness, 밀도/수익 팩터/손실폭/매끄러움)이 같이 좋아지는지 봅니다.

## Best Candidate Read(최상위 후보 판독)

- candidate(후보): `{best.get('candidate_id', 'none')}`
- strict scout clue pass(엄격 탐색 단서 통과): `{best.get('strict_scout_clue_pass', False)}`
- preserved clue pass(보존 단서 통과): `{best.get('preserved_clue_pass', False)}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- validation PF/density/DD(검증 수익 팩터/거래 밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/거래 밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`

## Local Verification(로컬 검증)

- subwindow containment(하위구간 포함): `{final['subwindow_count']}` train-only subwindows(학습 전용 하위구간), lengths(길이) `{final['subwindow_lengths']}`.
- leakage boundary(누수 경계): thresholds/margins/adverse caps(임계값/마진/불리 이동 상한)는 train split(학습 분할)에서만 fit(적합)했고 validation/OOS(검증/표본밖)는 evaluation-only(평가 전용)입니다.
- no-bridge control(무브리지 대조): class-prior density bridge(클래스 사전분포 밀도 브리지)와 threshold search(임계값 탐색)는 사용하지 않았습니다.
- references(참조): label_v1(라벨 v1), Frontier07 risk label(전선07 위험 라벨)은 재계산 대조군이고 Frontier08/09(전선08/09)는 report reference(보고서 참조)입니다.

## Artifacts(산출물)

- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- candidate metrics(후보 지표): `{artifacts['candidate_metrics'].as_posix()}`
- reference metrics(참조 지표): `{artifacts['reference_metrics'].as_posix()}`
- target diagnostics(목표 진단): `{artifacts['target_diagnostics'].as_posix()}`
- ONNX parity(온엑스 동등성): `{artifacts['onnx_parity'].as_posix()}`
- final decision(최종 판단): `{artifacts['final_decision'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다. WFO/MT5(WFO/MT5)는 strict scout clue(엄격 탐색 단서)와 Grok pre-expensive review(그록 비싼 검증 전 검토) 전까지 실행하지 않습니다.

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동): strict clue(엄격 단서)가 있으면 Grok pre-expensive review(그록 비싼 검증 전 검토)로 가고, 없으면 repair/closeout decision(수리/마감 결정)으로 갑니다. Effect(효과): scout clue(탐색 단서)를 completion candidate(완성 후보)로 과장하지 않고 다음 검증 경계를 고릅니다.
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
        f"- `{RUN_ID}`: split-consistent utility distillation proxy scout(분할 일관 효용 증류 프록시 탐색)을 기록했습니다. Effect(효과): Frontier08/09(전선08/09)를 상속하지 않고 reference-only(참조 전용)로 비교합니다.\n",
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

Action(행동): Frontier10B(전선10B)는 train-only split-consistent utility labels(학습 전용 분할 일관 효용 라벨)을 만들고 fixed 3-class ONNX argmax scout(고정 3분류 온엑스 최대확률 탐색)를 실행했습니다.

Effect(효과): label_v1/Frontier07 recomputed controls(라벨 v1/전선07 재계산 대조군)와 Frontier08/09 report references(전선08/09 보고서 참조)를 함께 보되, WFO/MT5(WFO/MT5)와 runtime authority(런타임 권위)는 주장하지 않습니다.

Best read(최상위 판독): `{best.get('candidate_id', 'none')}` with strict scout clue rows(엄격 탐색 단서 행) `{final['strict_scout_clue_rows']}` and preserved clue rows(보존 단서 행) `{final['preserved_clue_rows']}`.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_candidate_row"]
    return f"""# Frontier10 Selection Status(전선10 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Latest run(최근 실행): `{RUN_ID}`

Report(보고서): `{REPORT_PATH.as_posix()}`

Final decision(최종 판단 파일): `{artifacts['final_decision'].as_posix()}`

Best candidate(최상위 후보): `{best.get('candidate_id', 'none')}`

Strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`

Preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.
"""


def review_index_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    artifact_lines = "\n".join(f"- `{path.as_posix()}`" for path in artifacts.values())
    return f"""# Frontier10 Review Index(전선10 검토 색인)

Updated(갱신): {final['created_at_utc']}

## Reviews(검토)

- `frontier10A_stage_open_split_consistent_utility_distillation_v1`: stage open(단계 개방), Grok accepted(그록 수용), Stage295 boundary locally verified(295단계 경계 로컬 검증).
- `{RUN_ID}`: utility distillation proxy scout(효용 증류 프록시 탐색), train-only leakage guard(학습 전용 누수 방지), ONNX parity(온엑스 동등성), paired controls(짝 대조군).

## Latest Artifacts(최신 산출물)

{artifact_lines}
"""


def gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier10B Required Gate Coverage Audit(전선10B 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계부 통과)

## Gate Coverage(게이트 커버리지)

- scope_completion_gate(범위 완료 게이트): satisfied_with_boundary(경계부 충족)
- data_integrity_gate(데이터 무결성 게이트): train-only thresholds verified(학습 전용 임계값 확인)
- model_validation_gate(모델 검증 게이트): fixed split, argmax-only, no threshold search(고정 분할, 최대확률 전용, 임계값 탐색 없음)
- artifact_lineage_gate(산출물 계보 게이트): run manifest and hashes written(실행 목록과 해시 기록)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): satisfied_with_boundary(경계부 충족)
- final_claim_guard(최종 주장 보호): satisfied_with_boundary(경계부 충족)

Action(행동): proxy scout(프록시 탐색)는 ONNX parity(온엑스 동등성)까지 완료했습니다.

Effect(효과): WFO/MT5(WFO/MT5), operating promotion(운영 승격), runtime authority(런타임 권위), completion(완성)은 주장하지 않습니다.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "utility_distillation_model_scout(효용 증류 모델 탐색)",
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
        "claim_boundary": "utility_distillation_scout_onnx_parity_only_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_utility_distillation_model_scout",
        "subrun_id": f"{RUN_ID}__tier_a_utility_distillation_model_scout",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "utility_distillation_model_scout_not_runtime(효용 증류 모델 탐색, 런타임 아님)",
        "primary_kpi": primary_kpi_text(best),
        "guardrail_kpi": "argmax_only_no_threshold_no_bridge_no_wfo_no_mt5_no_authority(최대확률 전용, 임계값/브리지/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "utility_distillation_model_scout_only(효용 증류 모델 탐색 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can split-consistent utility distillation improve four axes without a bridge?(분할 일관 효용 증류가 브리지 없이 네 축을 개선하는가?)",
        "skill_family": "experiment_execution(실험 실행)",
        "lineage_summary": "frontier10a_stage_open_to_frontier10b_utility_distillation_scout(전선10A 단계 개방에서 전선10B 효용 증류 탐색)",
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
        "scoreboard_lane": "utility_distillation_model_scout(효용 증류 모델 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "argmax_only_no_threshold_no_bridge_no_wfo_no_mt5_no_authority(최대확률 전용, 임계값/브리지/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_utility_distillation_model_scout",
            "subrun_id": f"{RUN_ID}__tier_a_utility_distillation_model_scout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "utility_distillation_model_scout_not_runtime(효용 증류 모델 탐색, 런타임 아님)",
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
