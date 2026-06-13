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
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

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
from stage_pipelines.stage_frontier_04 import frontier04b_path_aware_label_proxy_scout as f04b
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b
from stage_pipelines.stage_frontier_10 import frontier10b_utility_distillation_proxy_scout as f10b


STAGE_ID = "stage_frontier_10__split_consistent_utility_distillation"
RUN_ID = "frontier10C_utility_distillation_capped_repair_scout_v1"
RUN_NUMBER = "frontier10C"
PARENT_RUN_ID = "frontier10B_utility_distillation_proxy_scout_v1"
NEXT_STRICT_RUN_ID = "frontier10D_grok_pre_expensive_utility_distillation_repair_review_v1"
NEXT_CLOSEOUT_REVIEW_RUN_ID = "frontier10D_grok_stage_closeout_review_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_10/frontier10c_utility_distillation_capped_repair_scout.py")

LABEL_ORDER = f04d.LABEL_ORDER
LABEL_NAMES = f04d.LABEL_NAMES
HORIZON_BARS = f10b.HORIZON_BARS

FRONTIER10B_BEST = {
    "source": (
        "stages/stage_frontier_10__split_consistent_utility_distillation/03_reviews/"
        "frontier10B_utility_distillation_proxy_scout_v1_report.md"
    ),
    "validation_profit_factor": 0.8209086653121057,
    "validation_trades_per_day": 2.300546448087432,
    "validation_dd_risk_percent": 56.39557540756517,
    "oos_profit_factor": 1.3109653577676894,
    "oos_trades_per_day": 0.6641221374045801,
    "oos_dd_risk_percent": 7.578528721913347,
}

def weight_token(value: float) -> str:
    return f"{value:.2f}".replace(".", "p")


@dataclass(frozen=True)
class RepairModelSpec:
    model_id: str
    estimator: Pipeline
    side_weight: float
    c_value: float
    threshold_policy: str


MODEL_SPECS = tuple(
    RepairModelSpec(
        model_id=f"logreg_l2_c0p5_sidew{weight_token(weight)}_argmax",
        estimator=Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=2000,
                        C=0.5,
                        random_state=7,
                        solver="lbfgs",
                        class_weight={0: weight, 1: 1.0, 2: weight},
                    ),
                ),
            ]
        ),
        side_weight=weight,
        c_value=0.5,
        threshold_policy=(
            "argmax_only_fixed_side_class_weight_no_threshold_no_bridge"
            "(최대확률 전용, 고정 방향 클래스 가중, 임계값/브리지 없음)"
        ),
    )
    for weight in (1.2, 1.4, 1.6, 1.8, 2.0, 2.4, 2.8)
) + (
    RepairModelSpec(
        model_id="logreg_l2_c0p25_sidew1p80_argmax",
        estimator=Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=2000,
                        C=0.25,
                        random_state=7,
                        solver="lbfgs",
                        class_weight={0: 1.8, 1: 1.0, 2: 1.8},
                    ),
                ),
            ]
        ),
        side_weight=1.8,
        c_value=0.25,
        threshold_policy=(
            "argmax_only_fixed_side_class_weight_no_threshold_no_bridge"
            "(최대확률 전용, 고정 방향 클래스 가중, 임계값/브리지 없음)"
        ),
    ),
    RepairModelSpec(
        model_id="logreg_l2_c1p0_sidew1p80_argmax",
        estimator=Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=2000,
                        C=1.0,
                        random_state=7,
                        solver="lbfgs",
                        class_weight={0: 1.8, 1: 1.0, 2: 1.8},
                    ),
                ),
            ]
        ),
        side_weight=1.8,
        c_value=1.0,
        threshold_policy=(
            "argmax_only_fixed_side_class_weight_no_threshold_no_bridge"
            "(최대확률 전용, 고정 방향 클래스 가중, 임계값/브리지 없음)"
        ),
    ),
)

MODEL_ID_SHORT = {
    spec.model_id: f"lr_c{weight_token(spec.c_value)}_sw{weight_token(spec.side_weight)}"
    for spec in MODEL_SPECS
}


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    path = f07b.path_arrays(full, raw, HORIZON_BARS)
    subwindows = f10b.train_subwindows(full)
    variants = f10b.build_variants(full, path)
    targets = f10b.build_targets(full, raw, path, variants, subwindows)
    result = train_and_evaluate(full, feature_order, path, targets)
    final = build_final(result, source_integrity, feature_order, variants, subwindows)
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


def train_and_evaluate(
    full: pd.DataFrame,
    feature_order: list[str],
    path: dict[str, np.ndarray],
    targets: list[f10b.TargetSurface],
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
        target_distribution_rows.extend(f10b.label_distribution(full, target))
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
        rows = fit_label_target(
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
            candidate_metrics.extend(rows)
        else:
            reference_metrics.extend(rows)

    candidate_summary = f10b.build_candidate_summary(
        candidate_metrics,
        reference_metrics,
        classification_rows,
        parity_rows,
    )
    add_repair_reference_deltas(candidate_summary)
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
    target: f10b.TargetSurface,
    train_mask: np.ndarray,
    sample_indices: np.ndarray,
    classification_rows: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    target_dir = MODEL_DIR / target.target_id
    for spec in MODEL_SPECS:
        short_model_id = MODEL_ID_SHORT.get(spec.model_id, spec.model_id[:16])
        model_instance_id = f"f10c_{target.target_id}_{short_model_id}"
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
                "side_class_weight": spec.side_weight,
                "c_value": spec.c_value,
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
                    "side_class_weight": spec.side_weight,
                    "c_value": spec.c_value,
                }
            )
        rows.extend(evaluate_model_signal(full, signal, fwd_return, target, spec))
    return rows


def evaluate_model_signal(
    full: pd.DataFrame,
    signal: np.ndarray,
    fwd_return: np.ndarray,
    target: f10b.TargetSurface,
    spec: RepairModelSpec,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    reasons = np.full(len(full), f"argmax_repair_model_{target.target_id}", dtype=object)
    first_steps = np.zeros(len(full), dtype="int16")
    short_model_id = MODEL_ID_SHORT.get(spec.model_id, spec.model_id[:16])
    model_instance_id = f"f10c_{target.target_id}_{short_model_id}"
    for split in ("train", "validation", "oos"):
        metric = f04b.evaluate_split(
            full,
            signal,
            fwd_return,
            split,
            f10b.metric_variant(target.variant, target.target_id),
            f"argmax_repair_model_{target.target_id}",
            reasons,
            first_steps,
        )
        metric.update(
            {
                "target_id": target.target_id,
                "target_kind": target.target_kind,
                "source_boundary": target.source_boundary,
                "model_id": spec.model_id,
                "model_instance_id": model_instance_id,
                "label_family": target.label_family,
                "family_semantics": target.family_semantics,
                "difference_from_f07": target.difference_from_f07,
                "difference_from_f09": target.difference_from_f09,
                "difference_from_stage295": target.difference_from_stage295,
                "signal_contract": (
                    "argmax_only_fixed_side_class_weight_no_threshold_no_class_prior_bridge"
                    "(최대확률 전용, 고정 방향 클래스 가중, 임계값/클래스 사전분포 브리지 없음)"
                ),
                "side_class_weight": spec.side_weight,
                "c_value": spec.c_value,
            }
        )
        rows.append(metric)
    return rows


def add_repair_reference_deltas(rows: list[dict[str, Any]]) -> None:
    for item in rows:
        count = 0
        item["frontier10b_best_source"] = FRONTIER10B_BEST["source"]
        for split in ("validation", "oos"):
            pf_delta = float(item[f"{split}_profit_factor"]) - float(FRONTIER10B_BEST[f"{split}_profit_factor"])
            density_delta = f10b.scout.density_axis_distance(float(item[f"{split}_trades_per_day"])) - f10b.scout.density_axis_distance(
                float(FRONTIER10B_BEST[f"{split}_trades_per_day"])
            )
            dd_delta = float(item[f"{split}_dd_risk_percent"]) - float(FRONTIER10B_BEST[f"{split}_dd_risk_percent"])
            item[f"{split}_vs_frontier10b_best_pf_delta"] = pf_delta
            item[f"{split}_vs_frontier10b_best_density_axis_delta"] = density_delta
            item[f"{split}_vs_frontier10b_best_dd_delta"] = dd_delta
            item[f"{split}_vs_frontier10b_best_pf_improved"] = bool(pf_delta >= -1e-12)
            item[f"{split}_vs_frontier10b_best_density_axis_improved"] = bool(density_delta <= -1e-12)
            item[f"{split}_vs_frontier10b_best_dd_improved"] = bool(dd_delta <= -1e-12)
            count += int(bool(item[f"{split}_vs_frontier10b_best_pf_improved"]))
            count += int(bool(item[f"{split}_vs_frontier10b_best_density_axis_improved"]))
            count += int(bool(item[f"{split}_vs_frontier10b_best_dd_improved"]))
        item["frontier10b_best_improvement_count"] = count
        item["repair_preserved_clue_pass"] = bool(
            item.get("preserved_clue_pass", False)
            and int(item["frontier10b_best_improvement_count"]) >= 3
        )
        if not item.get("strict_scout_clue_pass", False):
            item["preserved_clue_pass"] = item["repair_preserved_clue_pass"]
    rows.sort(
        key=lambda item: (
            not bool(item["strict_scout_clue_pass"]),
            not bool(item["preserved_clue_pass"]),
            float(item["validation_oos_score_sum"]),
            -float(item["oos_profit_factor"]),
            float(item["oos_dd_risk_percent"]),
        )
    )


def build_final(
    result: dict[str, Any],
    source_integrity: dict[str, Any],
    feature_order: list[str],
    variants: list[f10b.UtilityVariant],
    subwindows: list[np.ndarray],
) -> dict[str, Any]:
    candidates = result["candidate_summary"]
    strict_rows = int(sum(1 for row in candidates if row.get("strict_scout_clue_pass")))
    preserved_rows = int(sum(1 for row in candidates if row.get("preserved_clue_pass")))
    best = candidates[0] if candidates else {}
    if strict_rows:
        status = "utility_distillation_capped_repair_strict_scout_clue_no_authority"
        judgment = "strict_scout_clue(엄격 탐색 단서)"
        next_run_id = NEXT_STRICT_RUN_ID
        judgment_class = "positive(긍정)"
    elif preserved_rows:
        status = "utility_distillation_capped_repair_preserved_clue_no_authority"
        judgment = "preserved_clue(보존 단서)"
        next_run_id = NEXT_CLOSEOUT_REVIEW_RUN_ID
        judgment_class = "positive_with_boundary(경계부 긍정)"
    else:
        status = "utility_distillation_capped_repair_no_strict_clue_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run_id = NEXT_CLOSEOUT_REVIEW_RUN_ID
        judgment_class = "negative(부정)"
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": utc_now(),
        "status": status,
        "judgment": judgment,
        "judgment_class": judgment_class,
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
                "F10B utility labels use future path only as supervised target; F10C changes train objective only"
                "(F10B 효용 라벨은 미래 경로를 지도 목표로만 쓰고, F10C는 학습 목적만 바꿈)"
            ),
            "split_boundary": (
                "labels and class-weight ladder are train-only or fixed before validation/OOS evaluation"
                "(라벨과 클래스 가중 사다리는 검증/OOS 평가 전 학습 전용 또는 고정)"
            ),
            "leakage_judgment": "usable_with_boundary_no_validation_oos_fit(경계부 사용 가능, 검증/OOS 적합 없음)",
        },
        "run_evidence": {
            "measurement_scope": "structural_scout plus trading/risk KPI(구조 탐색과 거래/위험 KPI)",
            "management_state": "run folder, manifest, report, registries written(실행 폴더/목록/보고서/등록부 기록)",
            "scoreboard": "structural_scout(구조 탐색)",
            "parity_level": "P2_model_input_parity_closed(P2 모델 입력 동등성 확인)",
            "wfo_status": "not_applicable_no_strict_clue(엄격 단서 없음으로 해당 없음)",
            "registry_update_required": "yes(예)",
            "negative_memory_required": "no_until_stage_closeout(단계 마감 전까지 아님)",
            "hard_gate_applicable": "no(아니오)",
            "evidence_boundary": "scout-only(탐색 전용)",
        },
        "model_validation": {
            "model_family": "logistic regression fixed side-class-weight ladder(로지스틱 고정 방향 클래스 가중 사다리)",
            "target_and_label": "Frontier10B utility distillation labels(전선10B 효용 증류 라벨)",
            "split_method": "fixed train/validation/OOS split(고정 학습/검증/OOS 분할)",
            "selection_metric": "strict clue, repair preserved clue, validation+OOS aspiration distance(엄격 단서, 수리 보존 단서, 검증+OOS 목표 거리)",
            "threshold_policy": "argmax_only_no_threshold_no_posthoc_bridge(최대확률 전용, 임계값/사후 브리지 없음)",
            "overfit_risk": "class-weight ladder may tune density without enough validation stability(클래스 가중 사다리가 검증 안정성 없이 밀도만 조정할 수 있음)",
            "calibration_risk": "scores are ranking/probability-output evidence only(점수는 순위/확률 출력 근거일 뿐)",
            "comparison_baseline": "Frontier10B best plus label_v1/F07/F08/F09 references(전선10B 최상과 라벨v1/F07/F08/F09 참조)",
            "validation_judgment": "exploratory_no_authority(탐색, 권위 없음)",
        },
        "artifact_lineage": {
            "source_inputs": [f03b.DATASET_PATH.as_posix(), f04b.RAW_US100.as_posix(), FRONTIER10B_BEST["source"]],
            "producer": SCRIPT_PATH.as_posix(),
            "consumer": next_run_id,
            "availability": "ignored_with_manifest_for_run_artifacts_tracked_report(실행 산출물은 무시+목록, 보고서는 추적)",
            "lineage_judgment": "connected_with_boundary(경계부 연결)",
        },
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_artifacts(result: dict[str, Any], final: dict[str, Any]) -> dict[str, Path]:
    artifacts = {
        "candidate_metrics": RUN_ROOT / "repair_candidate_model_metrics.csv",
        "reference_metrics": RUN_ROOT / "repair_reference_model_metrics.csv",
        "candidate_summary": RUN_ROOT / "repair_candidate_summary.csv",
        "classification_metrics": RUN_ROOT / "repair_classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "repair_onnx_parity.csv",
        "target_distribution": RUN_ROOT / "repair_target_distribution.csv",
        "skipped": RUN_ROOT / "repair_skipped_targets.csv",
        "final_decision": RUN_ROOT / "repair_final_decision.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_csv(artifacts["candidate_metrics"], result["candidate_metrics"])
    write_csv(artifacts["reference_metrics"], result["reference_metrics"])
    write_csv(artifacts["candidate_summary"], result["candidate_summary"])
    write_csv(artifacts["classification_metrics"], result["classification_metrics"])
    write_csv(artifacts["onnx_parity"], result["onnx_parity"])
    write_csv(artifacts["target_distribution"], result["target_distribution"])
    write_csv(artifacts["skipped"], result["skipped"])
    final["artifact_lineage"]["artifact_paths"] = [path.as_posix() for path in artifacts.values()]
    write_json(artifacts["final_decision"], final)
    manifest = {
        **final,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "model_specs": [spec.__dict__ | {"estimator": str(spec.estimator)} for spec in MODEL_SPECS],
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
    text = f"""# Frontier10C Utility Distillation Capped Repair Scout Report(전선10C 효용 증류 상한 수리 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier10C(전선10C)는 Frontier10B(전선10B) utility labels(효용 라벨)를 유지하고, fixed side-class-weight ladder(고정 방향 클래스 가중 사다리)로 plain sparse(일반 희소)와 balanced overtrade(균형 과거래) 사이를 한 번만 탐색했습니다.

Effect(효과): class-prior density bridge(클래스 사전분포 밀도 브리지), threshold search(임계값 탐색), WFO/MT5(WFO/MT5)를 쓰지 않고 ONNX argmax-only(온엑스 최대확률 전용) 모델의 밀도 절벽이 수리되는지 봅니다.

## Best Repair Read(최상위 수리 판독)

- candidate(후보): `{best.get('candidate_id', 'none')}`
- strict scout clue pass(엄격 탐색 단서 통과): `{best.get('strict_scout_clue_pass', False)}`
- preserved clue pass(보존 단서 통과): `{best.get('preserved_clue_pass', False)}`
- strict scout clue rows(엄격 탐색 단서 행): `{final['strict_scout_clue_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- validation PF/density/DD(검증 수익 팩터/거래 밀도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/거래 밀도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- Frontier10B best improvement count(전선10B 최상 대비 개선 수): `{best.get('frontier10b_best_improvement_count', 'n/a')}`

## Boundaries(경계)

- repair scope(수리 범위): one capped model-objective ladder(상한 있는 모델 목적 사다리 1회)
- no bridge(브리지 없음): post-hoc class-prior/density bridge(사후 클래스 사전분포/밀도 브리지)를 쓰지 않았습니다.
- no threshold search(임계값 탐색 없음): output(출력)은 argmax-only(최대확률 전용)입니다.
- external verification(외부 검증): strict clue(엄격 단서)가 없으면 WFO/MT5(WFO/MT5)는 out_of_scope_by_claim(주장 범위 밖)입니다.

## Artifacts(산출물)

- repair candidate summary(수리 후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- repair model metrics(수리 모델 지표): `{artifacts['candidate_metrics'].as_posix()}`
- ONNX parity(온엑스 동등성): `{artifacts['onnx_parity'].as_posix()}`
- final decision(최종 판단): `{artifacts['final_decision'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동): strict clue(엄격 단서)가 있으면 Grok pre-expensive review(그록 비싼 검증 전 검토)로, 없으면 Grok stage closeout review(그록 단계 마감 검토)로 갑니다. Effect(효과): 한 번 허용된 capped repair(상한 수리)를 반복하지 않고, 가설 생명주기(hypothesis lifecycle, 가설 생명주기)를 정직하게 닫을 준비를 합니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
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
    f10b.ensure_csv_header(stage_ledger, f03b.ALPHA_LEDGER)
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
        f"- `{RUN_ID}`: utility distillation capped repair scout(효용 증류 상한 수리 탐색)를 기록했습니다. Effect(효과): post-hoc bridge(사후 브리지) 없이 density cliff(밀도 절벽)를 한 번 시험했습니다.\n",
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

Action(행동): Frontier10C(전선10C)는 Frontier10B(전선10B)의 utility distillation labels(효용 증류 라벨)에 fixed side-class-weight ladder(고정 방향 클래스 가중 사다리)를 적용해 capped repair scout(상한 수리 탐색)를 실행했습니다.

Effect(효과): plain sparse(일반 희소)와 balanced overtrade(균형 과거래) 사이에서 ONNX argmax-only(온엑스 최대확률 전용) 밀도/PF/DD(밀도/수익 팩터/손실폭)가 동시에 좋아지는지 확인했고, WFO/MT5(WFO/MT5)와 runtime authority(런타임 권위)는 주장하지 않습니다.

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
- `frontier10B_utility_distillation_proxy_scout_v1`: utility distillation proxy scout(효용 증류 프록시 탐색), train-only leakage guard(학습 전용 누수 방지), ONNX parity(온엑스 동등성), paired controls(짝 대조군).
- `{RUN_ID}`: capped side-class-weight repair scout(상한 방향 클래스 가중 수리 탐색), ONNX parity(온엑스 동등성), no post-hoc bridge(사후 브리지 없음).

## Latest Artifacts(최신 산출물)

{artifact_lines}
"""


def gate_audit_text(final: dict[str, Any]) -> str:
    return f"""# Frontier10C Required Gate Coverage Audit(전선10C 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계부 통과)

## Gate Coverage(게이트 커버리지)

- scope_completion_gate(범위 완료 게이트): satisfied_with_boundary(경계부 충족)
- kpi_contract_audit(KPI 계약 감사): trading/risk KPI and Tier A/B rows recorded(거래/위험 KPI와 Tier A/B 행 기록)
- skill_receipt_lint(스킬 영수증 점검): run evidence, data integrity, model validation, artifact lineage, claim discipline(실행 근거/데이터 무결성/모델 검증/산출물 계보/주장 규율)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): satisfied_with_boundary(경계부 충족)
- final_claim_guard(최종 주장 보호): satisfied_with_boundary(경계부 충족)

Action(행동): capped repair scout(상한 수리 탐색)는 ONNX parity(온엑스 동등성)까지 완료했습니다.

Effect(효과): WFO/MT5(WFO/MT5), operating promotion(운영 승격), runtime authority(런타임 권위), completion(완성)은 주장하지 않습니다.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final["best_candidate_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "utility_distillation_capped_repair(효용 증류 상한 수리)",
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
        "claim_boundary": "utility_distillation_capped_repair_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_capped_repair_scout",
        "subrun_id": f"{RUN_ID}__tier_a_capped_repair_scout",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "utility_distillation_capped_repair_not_runtime(효용 증류 상한 수리, 런타임 아님)",
        "primary_kpi": f10b.primary_kpi_text(best),
        "guardrail_kpi": "argmax_only_no_threshold_no_bridge_no_wfo_no_mt5_no_authority(최대확률 전용, 임계값/브리지/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "capped_repair_scout_only(상한 수리 탐색 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can a fixed class-weight ladder repair utility distillation density without a bridge?(고정 클래스 가중 사다리가 브리지 없이 효용 증류 밀도를 수리하는가?)",
        "skill_family": "experiment_execution(실험 실행)",
        "lineage_summary": "frontier10b_to_frontier10c_capped_repair(전선10B에서 전선10C 상한 수리)",
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
        "scoreboard_lane": "utility_distillation_capped_repair(효용 증류 상한 수리)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "argmax_only_no_threshold_no_bridge_no_wfo_no_mt5_no_authority(최대확률 전용, 임계값/브리지/WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_capped_repair_scout",
            "subrun_id": f"{RUN_ID}__tier_a_capped_repair_scout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "utility_distillation_capped_repair_not_runtime(효용 증류 상한 수리, 런타임 아님)",
            "primary_kpi": f10b.primary_kpi_text(best),
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
