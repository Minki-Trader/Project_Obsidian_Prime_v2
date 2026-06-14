from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict
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
from stage_pipelines.stage_frontier_14 import frontier14b_daily_session_opportunity_budget_proxy_scout as f14b


STAGE_ID = "stage_frontier_15__score_threshold_density_controlled_onnx_scout"
RUN_ID = "frontier15B_score_threshold_density_controlled_proxy_scout_v1"
RUN_NUMBER = "frontier15B"
PARENT_RUN_ID = "frontier15A_stage_open_score_threshold_density_controlled_onnx_scout_v1"
NEXT_STRICT_RUN_ID = "frontier15C_grok_pre_expensive_score_threshold_density_review_v1"
NEXT_REPAIR_RUN_ID = "frontier15C_score_threshold_density_repair_or_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_15/frontier15b_score_threshold_density_controlled_proxy_scout.py")
STAGE_OPEN_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "stage_open_summary.json"

LABEL_ORDER = f04d.LABEL_ORDER
LABEL_NAMES = f12b.LABEL_NAMES
PRIMARY_CELL_ID = "edge_margin__target8"
SCORE_CONTRACT_IDS = ("edge_margin", "side_gap", "utility_tilt")
DENSITY_TARGETS = (5, 8, 10)


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    stage_open = read_json(STAGE_OPEN_SUMMARY)
    full, raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    variants = f14b.build_variants()
    result = train_and_evaluate(full, raw, feature_order, variants)
    final = build_final(created_at, result, variants, source_integrity, feature_order, stage_open)
    artifacts = write_artifacts(result, final, variants)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "primary_strict_scout_clue_rows": final["primary_strict_scout_clue_rows"],
        "secondary_strict_like_rows": final["secondary_strict_like_rows"],
        "preserved_clue_rows": final["preserved_clue_rows"],
        "best_candidate": final["best_candidate_row"].get("candidate_id"),
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def train_and_evaluate(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    feature_order: list[str],
    variants: list[f14b.OpportunityVariant],
) -> dict[str, Any]:
    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values(피처 행렬에 NaN 또는 무한대가 있습니다).")
    split_series = full["split"].astype(str)
    train_mask = split_series.eq("train").to_numpy()
    sample_indices = np.concatenate([
        np.flatnonzero(split_series.eq(split).to_numpy())[:256]
        for split in ("train", "validation", "oos")
    ])
    model_metrics: list[dict[str, Any]] = []
    subperiod_metrics: list[dict[str, Any]] = []
    argmax_baseline_metrics: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    distribution_rows: list[dict[str, Any]] = []
    threshold_rows: list[dict[str, Any]] = []
    skipped_rows: list[dict[str, Any]] = []
    target_diagnostics: list[dict[str, Any]] = []
    label_model_density_rows: list[dict[str, Any]] = []

    for variant in variants:
        path = f14b.opportunity_path_arrays(full, raw, variant)
        labels, oracle_signal, diagnostics = f14b.build_opportunity_labels(full, path, variant)
        target_diagnostics.append({"target_id": variant.variant_id, **json_ready(asdict(variant)), **diagnostics})
        distribution_rows.extend(f12b.label_distribution(full, labels, variant))
        missing = sorted(set(LABEL_ORDER) - set(int(value) for value in labels[train_mask]))
        if missing:
            skipped_rows.append({
                "target_id": variant.variant_id,
                "reason": f"missing_train_classes={missing}",
                "label_boundary": "pre_registered_f14_opportunity_label_control(사전 등록 F14 기회 라벨 통제)",
            })
            continue
        for spec in f04d.MODEL_SPECS:
            model_short = f12b.MODEL_ID_SHORT.get(spec.model_id, spec.model_id[:10])
            candidate_base = f"{variant.variant_id}__{model_short}"
            model_instance_id = f"f15b_{candidate_base}"
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
            argmax_rows = f12b.evaluate_all_splits(
                full,
                argmax_signal,
                path["fwd_return"],
                variant,
                "f14_matched_argmax_baseline_signal(F14 대응 최대확률 기준 신호)",
                argmax_id,
                model_id=spec.model_id,
                model_instance_id=model_instance_id,
            )
            for row in argmax_rows:
                row.update({
                    "score_contract_id": "argmax_baseline",
                    "cell_id": "argmax_baseline",
                    "target_density_per_day": "",
                    "threshold_value": "",
                    "is_primary_cell": False,
                    "signal_contract": "argmax_only_no_threshold(최대확률만 사용, 임계값 없음)",
                })
            argmax_baseline_metrics.extend(argmax_rows)
            label_model_density_rows.extend(enrich_density_rows(
                f14b.density_gap_rows(full, oracle_signal, argmax_signal, variant, argmax_id, spec.model_id, model_instance_id),
                "argmax_baseline",
                "",
                "argmax_baseline",
                False,
                "",
            ))

            for cell in score_contract_manifest_rows():
                score = score_values(probabilities, cell["score_contract_id"])
                direction = np.where(probabilities[:, 0] >= probabilities[:, 2], -1, 1).astype("int8")
                threshold_info = fit_train_threshold(full, score, train_mask, int(cell["target_density_per_day"]))
                threshold = float(threshold_info["threshold_value"])
                selected = np.isfinite(score) & (score >= threshold)
                threshold_signal = np.where(selected, direction, 0).astype("int8")
                candidate_id = f"{candidate_base}__{cell['score_contract_id']}__target{cell['target_density_per_day']}"
                threshold_rows.append({
                    "candidate_id": candidate_id,
                    "target_id": variant.variant_id,
                    "model_id": spec.model_id,
                    "model_instance_id": model_instance_id,
                    **cell,
                    **threshold_info,
                    "actual_all_selected_count": int(selected.sum()),
                    "threshold_policy": "train_scores_calendar_only_no_pnl(학습 점수와 달력만 사용, 손익 미사용)",
                })
                parity_rows.append({
                    "candidate_id": candidate_id,
                    **cell,
                    **parity_base,
                })
                classification_rows.extend(enrich_classification_rows(
                    f12b.classification_metrics(full, labels, pred_label, variant, spec.model_id, model_instance_id, candidate_id),
                    cell,
                ))
                split_rows = f12b.evaluate_all_splits(
                    full,
                    threshold_signal,
                    path["fwd_return"],
                    variant,
                    "score_threshold_model_signal(점수 임계값 모델 신호)",
                    candidate_id,
                    model_id=spec.model_id,
                    model_instance_id=model_instance_id,
                )
                model_metrics.extend(enrich_metric_rows(split_rows, cell, threshold))
                sub_rows = evaluate_threshold_subperiods(
                    full,
                    threshold_signal,
                    path["fwd_return"],
                    variant,
                    candidate_id,
                    spec.model_id,
                    model_instance_id,
                )
                subperiod_metrics.extend(enrich_metric_rows(sub_rows, cell, threshold))
                label_model_density_rows.extend(enrich_density_rows(
                    f14b.density_gap_rows(full, oracle_signal, threshold_signal, variant, candidate_id, spec.model_id, model_instance_id),
                    cell["score_contract_id"],
                    cell["cell_id"],
                    cell["target_density_per_day"],
                    bool(cell["is_primary_cell"]),
                    threshold,
                ))

    candidate_summary = build_threshold_candidate_summary(
        model_metrics,
        subperiod_metrics,
        parity_rows,
        classification_rows,
        threshold_rows,
    )
    return {
        "model_metrics": model_metrics,
        "subperiod_metrics": subperiod_metrics,
        "argmax_baseline_metrics": argmax_baseline_metrics,
        "classification_metrics": classification_rows,
        "onnx_parity": parity_rows,
        "label_distribution": distribution_rows,
        "threshold_manifest": threshold_rows,
        "score_contract_manifest": score_contract_manifest_rows(),
        "skipped": skipped_rows,
        "target_diagnostics": target_diagnostics,
        "candidate_summary": candidate_summary,
        "label_model_density_gap": label_model_density_rows,
    }


def score_contract_manifest_rows() -> list[dict[str, Any]]:
    contracts = {
        "edge_margin": {
            "score_expression": "max(p_short, p_long) - p_flat",
            "decision_meaning": "model confidence over flat(무거래 대비 모델 확신)",
        },
        "side_gap": {
            "score_expression": "abs(p_long - p_short)",
            "decision_meaning": "directional separation(방향 분리도)",
        },
        "utility_tilt": {
            "score_expression": "max(p_short, p_long) - 0.5 * p_flat",
            "decision_meaning": "milder flat penalty(완만한 무거래 벌점)",
        },
    }
    rows: list[dict[str, Any]] = []
    for contract_id in SCORE_CONTRACT_IDS:
        for target in DENSITY_TARGETS:
            cell_id = f"{contract_id}__target{target}"
            rows.append({
                "score_contract_id": contract_id,
                "cell_id": cell_id,
                "target_density_per_day": target,
                "is_primary_cell": cell_id == PRIMARY_CELL_ID,
                "score_expression": contracts[contract_id]["score_expression"],
                "decision_meaning": contracts[contract_id]["decision_meaning"],
                "threshold_fit_policy": "train_probability_scores_plus_train_calendar_only(학습 확률 점수와 학습 달력만 사용)",
                "selection_rule": "primary_cell_only_for_forward_trigger(1순위 칸만 전진 트리거)",
            })
    return rows


def score_values(probabilities: np.ndarray, score_contract_id: str) -> np.ndarray:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    p_side = np.maximum(p_short, p_long)
    if score_contract_id == "edge_margin":
        return p_side - p_flat
    if score_contract_id == "side_gap":
        return np.abs(p_long - p_short)
    if score_contract_id == "utility_tilt":
        return p_side - 0.5 * p_flat
    raise ValueError(f"Unknown score contract: {score_contract_id}")


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
    if math.isfinite(threshold):
        equal_count = int(np.isclose(train_score, threshold, rtol=0.0, atol=1e-12).sum())
        above_count = int((train_score > threshold).sum())
    else:
        equal_count = 0
        above_count = int(selected_train.sum())
    return {
        "threshold_value": threshold,
        "train_days_in_scope": int(days),
        "target_train_trade_count": int(target_count),
        "actual_train_selected_count": int(selected_train.sum()),
        "actual_train_selected_density_per_day": float(selected_train.sum() / days) if days else 0.0,
        "train_threshold_equal_count": equal_count,
        "train_threshold_above_count": above_count,
        "train_threshold_tie_policy": "numeric_threshold_score_greater_equal(숫자 임계값 이상 선택)",
    }


def evaluate_threshold_subperiods(
    full: pd.DataFrame,
    signal: np.ndarray,
    fwd_return: np.ndarray,
    variant: f14b.OpportunityVariant,
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
                    "subperiod_score_threshold_model_signal(하위기간 점수 임계값 모델 신호)",
                    candidate_id,
                    model_id,
                    model_instance_id,
                    split=split,
                    granularity=granularity,
                    period=str(period),
                ))
    return rows


def enrich_metric_rows(rows: list[dict[str, Any]], cell: dict[str, Any], threshold: float) -> list[dict[str, Any]]:
    for row in rows:
        row.update({
            "score_contract_id": cell["score_contract_id"],
            "cell_id": cell["cell_id"],
            "target_density_per_day": cell["target_density_per_day"],
            "is_primary_cell": bool(cell["is_primary_cell"]),
            "threshold_value": threshold,
            "signal_contract": "score_threshold_train_only(학습 전용 점수 임계값)",
        })
    return rows


def enrich_classification_rows(rows: list[dict[str, Any]], cell: dict[str, Any]) -> list[dict[str, Any]]:
    for row in rows:
        row.update({
            "score_contract_id": cell["score_contract_id"],
            "cell_id": cell["cell_id"],
            "target_density_per_day": cell["target_density_per_day"],
            "is_primary_cell": bool(cell["is_primary_cell"]),
        })
    return rows


def enrich_density_rows(
    rows: list[dict[str, Any]],
    score_contract_id: str,
    cell_id: str,
    target_density_per_day: Any,
    is_primary_cell: bool,
    threshold_value: Any,
) -> list[dict[str, Any]]:
    for row in rows:
        row.update({
            "score_contract_id": score_contract_id,
            "cell_id": cell_id,
            "target_density_per_day": target_density_per_day,
            "is_primary_cell": is_primary_cell,
            "threshold_value": threshold_value,
        })
    return rows


def build_threshold_candidate_summary(
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
        raw_strict = bool(row.get("strict_scout_clue_pass"))
        is_primary = bool(threshold.get("is_primary_cell"))
        row.update({
            "score_contract_id": threshold.get("score_contract_id", ""),
            "cell_id": threshold.get("cell_id", ""),
            "target_density_per_day": threshold.get("target_density_per_day", ""),
            "is_primary_cell": is_primary,
            "threshold_value": threshold.get("threshold_value", ""),
            "actual_train_selected_density_per_day": threshold.get("actual_train_selected_density_per_day", ""),
            "target_train_trade_count": threshold.get("target_train_trade_count", ""),
            "actual_train_selected_count": threshold.get("actual_train_selected_count", ""),
            "raw_strict_scout_clue_pass": raw_strict,
            "secondary_strict_like_pass": bool(raw_strict and not is_primary),
            "strict_scout_clue_pass": bool(raw_strict and is_primary),
            "strict_scout_clue_pass_for_forward": bool(raw_strict and is_primary),
            "preserved_clue_pass": bool(row.get("preserved_clue_pass") or (raw_strict and not is_primary)),
            "signal_contract": "score_threshold_train_only(학습 전용 점수 임계값)",
        })
        enriched.append(row)
    enriched.sort(key=lambda item: (
        not bool(item["strict_scout_clue_pass"]),
        not bool(item["secondary_strict_like_pass"]),
        not bool(item["preserved_clue_pass"]),
        float(item.get("shape_duration_score", 999999.0)),
    ))
    return json_ready(enriched)


def build_final(
    created_at: str,
    result: dict[str, Any],
    variants: list[f14b.OpportunityVariant],
    source_integrity: dict[str, Any],
    feature_order: list[str],
    stage_open: dict[str, Any],
) -> dict[str, Any]:
    candidate_summary = result["candidate_summary"]
    strict_rows = [row for row in candidate_summary if row.get("strict_scout_clue_pass")]
    secondary_rows = [row for row in candidate_summary if row.get("secondary_strict_like_pass")]
    preserved_rows = [row for row in candidate_summary if row.get("preserved_clue_pass")]
    primary_rows = [row for row in candidate_summary if row.get("is_primary_cell")]
    best = candidate_summary[0] if candidate_summary else {}
    best_primary = primary_rows[0] if primary_rows else {}
    if strict_rows:
        status = "score_threshold_primary_strict_scout_clue_no_authority"
        judgment = "strict_scout_clue_candidate(엄격 탐색 단서 후보)"
        next_run_id = NEXT_STRICT_RUN_ID
    elif preserved_rows or secondary_rows:
        status = "score_threshold_preserved_clue_no_authority"
        judgment = "preserved_clue_candidate(보존 단서 후보)"
        next_run_id = NEXT_REPAIR_RUN_ID
    else:
        status = "score_threshold_no_strict_clue_no_authority"
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
        "primary_cell_id": PRIMARY_CELL_ID,
        "primary_strict_scout_clue_rows": len(strict_rows),
        "secondary_strict_like_rows": len(secondary_rows),
        "preserved_clue_rows": len(preserved_rows),
        "candidate_row_count": len(candidate_summary),
        "primary_cell_row_count": len(primary_rows),
        "best_candidate_row": best,
        "best_primary_cell_row": best_primary,
        "variant_count": len(variants),
        "model_count": len(f04d.MODEL_SPECS),
        "score_cell_count": len(score_contract_manifest_rows()),
        "stage_open_status": stage_open.get("status", ""),
        "source_integrity": source_integrity,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "data_integrity": data_integrity_record(source_integrity),
        "model_validation": model_validation_record(best),
        "artifact_lineage": artifact_lineage_record(),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "wfo_status": "not_run_requires_grok_pre_expensive_if_primary_strict(1순위 엄격 단서가 있으면 그록 비싼 검증 전 검토 필요)",
        "mt5_status": "not_run_proxy_only_no_runtime_authority(프록시 전용, 런타임 권위 없음)",
    }


def data_integrity_record(source_integrity: dict[str, Any]) -> dict[str, Any]:
    return {
        "data_source": f03b.DATASET_PATH.as_posix(),
        "time_axis": "US100 M5 closed-bar timestamp order(US100 5분봉 확정봉 시각 순서)",
        "sample_scope": "Tier A train/validation/OOS fixed split(티어 A 학습/검증/표본밖 고정 분할)",
        "feature_label_boundary": "features use closed bars; labels use F14 future path as supervised target only(피처는 확정봉, 라벨은 F14 미래 경로를 감독 목표로만 사용)",
        "threshold_boundary": "thresholds fit on train probability scores and train calendar only(임계값은 학습 확률 점수와 학습 달력만 사용)",
        "leakage_risk": "validation/OOS threshold calibration is forbidden(검증/표본밖 임계값 보정 금지)",
        "data_hash_or_identity": source_integrity,
        "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
    }


def model_validation_record(best: dict[str, Any]) -> dict[str, Any]:
    return {
        "model_family": "fixed sklearn-to-ONNX probability tensor(고정 sklearn-to-ONNX 확률 텐서)",
        "target_and_label": "F14 daily/session opportunity budget labels as control(F14 일/세션 기회 예산 라벨을 통제로 사용)",
        "split_method": "fixed train/validation/OOS split(고정 학습/검증/표본밖 분할)",
        "selection_metric": "primary cell strict clue, secondary cells preserved only(1순위 칸 엄격 단서, 보조 칸은 보존만)",
        "threshold_policy": "frozen 9-cell train-only density thresholds(고정 9칸 학습 전용 빈도 임계값)",
        "overfit_risk": "score cells are pre-registered, no validation/OOS threshold selection(점수 칸 사전 등록, 검증/표본밖 임계값 선택 없음)",
        "calibration_risk": "probability scores are classifier scores, not economic probabilities(확률 점수는 분류기 점수이지 경제 확률이 아님)",
        "comparison_baseline": "F14-matched argmax baseline rows(F14 대응 최대확률 기준행)",
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
    variants: list[f14b.OpportunityVariant],
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
        "label_model_density_gap": RUN_ROOT / "label_model_density_gap.csv",
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
    write_csv(artifacts["label_model_density_gap"], result["label_model_density_gap"])
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
    primary = final["best_primary_cell_row"]
    text = f"""# Frontier15B Score Threshold Density Controlled Proxy Scout(프론티어15B 점수 임계값 빈도 통제 프록시 탐색)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F14(프론티어14) opportunity labels(기회 라벨)을 control(통제)로 두고, ONNX probability score threshold(온엑스 확률 점수 임계값) 9칸을 학습 전용 빈도 기준으로 평가했습니다.

Effect(효과): argmax baseline(최대확률 기준행)과 score threshold signal(점수 임계값 신호)을 나란히 기록해 density cliff(빈도 절벽)가 decision contract(결정 계약)에서 고쳐지는지 확인했습니다.

## Result Summary(결과 요약)

- candidate rows(후보 행): `{final['candidate_row_count']}`
- primary strict rows(1순위 엄격 행): `{final['primary_strict_scout_clue_rows']}`
- secondary strict-like rows(보조 엄격 유사 행): `{final['secondary_strict_like_rows']}`
- preserved clue rows(보존 단서 행): `{final['preserved_clue_rows']}`
- best candidate(최고 후보): `{best.get('candidate_id', 'none')}`
- best validation PF/density/DD(최고 검증 수익 팩터/빈도/손실폭): `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_trades_per_day'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- best OOS PF/density/DD(최고 표본밖 수익 팩터/빈도/손실폭): `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_trades_per_day'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- best primary candidate(최고 1순위 후보): `{primary.get('candidate_id', 'none')}`
- primary validation/OOS PF-density-DD(1순위 검증/표본밖 수익 팩터-빈도-손실폭): `{fmt(primary.get('validation_profit_factor'))}` / `{fmt(primary.get('validation_trades_per_day'))}` / `{fmt(primary.get('validation_dd_risk_percent'))}%` and `{fmt(primary.get('oos_profit_factor'))}` / `{fmt(primary.get('oos_trades_per_day'))}` / `{fmt(primary.get('oos_dd_risk_percent'))}%`

## Artifacts(산출물)

- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
- threshold manifest(임계값 목록): `{artifacts['threshold_manifest'].as_posix()}`
- argmax baseline metrics(최대확률 기준 지표): `{artifacts['argmax_baseline_metrics'].as_posix()}`
- label/model density gap(라벨/모델 빈도 격차): `{artifacts['label_model_density_gap'].as_posix()}`
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
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): primary strict rows(1순위 엄격 행) `{final['primary_strict_scout_clue_rows']}`, secondary strict-like rows(보조 엄격 유사 행) `{final['secondary_strict_like_rows']}`, next run(다음 실행) `{final['next_run_id']}`.\n",
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
    primary = final["best_primary_cell_row"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): Frontier15B(프론티어15B)는 score threshold signal contract(점수 임계값 신호 계약) 9칸을 proxy scout(프록시 탐색)로 실행했습니다.

Effect(효과): best candidate(최고 후보) `{best.get('candidate_id', 'none')}`와 primary cell(1순위 칸) `{primary.get('candidate_id', 'none')}`의 PF-density-DD(수익 팩터-빈도-손실폭)를 분리해 기록했습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_candidate_row"]
    primary = final["best_primary_cell_row"]
    return f"""# Frontier15 Selection Status(프론티어15 선택 상태)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Latest run(최근 실행): `{RUN_ID}`

Best candidate(최고 후보): `{best.get('candidate_id', 'none')}`

Best primary cell candidate(최고 1순위 칸 후보): `{primary.get('candidate_id', 'none')}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next action(다음 행동): `{final['next_run_id']}`

Key artifacts(핵심 산출물): `{artifacts['candidate_summary'].as_posix()}`, `{artifacts['threshold_manifest'].as_posix()}`
"""


def review_index(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier15 Review Index(프론티어15 검토 색인)

Updated(갱신): {final['created_at_utc']}

- `{PARENT_RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용).
- `{RUN_ID}`: proxy scout(프록시 탐색), primary strict rows(1순위 엄격 행) `{final['primary_strict_scout_clue_rows']}`, secondary strict-like rows(보조 엄격 유사 행) `{final['secondary_strict_like_rows']}`.
- candidate summary(후보 요약): `{artifacts['candidate_summary'].as_posix()}`
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier15B Required Gate Coverage Audit(프론티어15B 필수 게이트 커버리지 감사)

Updated(갱신): {final['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- scope_completion_gate(범위 완료 게이트): frozen 9-cell score grid(고정 9칸 점수 격자) executed(실행됨).
- kpi_contract_audit(KPI 계약 감사): validation/OOS PF-density-DD and subperiod DD(검증/표본밖 수익 팩터-빈도-손실폭과 하위기간 손실폭) recorded(기록됨).
- data_integrity_gate(데이터 무결성 게이트): `{final['data_integrity']['integrity_judgment']}`
- model_validation_gate(모델 검증 게이트): `{final['model_validation']['validation_judgment']}`
- artifact_lineage_gate(산출물 계보 게이트): `{final['artifact_lineage']['lineage_judgment']}`
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음)
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "score_threshold_density_controlled_proxy_scout(점수 임계값 빈도 통제 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"primary_strict={final['primary_strict_scout_clue_rows']};secondary_strict_like={final['secondary_strict_like_rows']};no_wfo_no_mt5_no_authority",
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
        "scoreboard_lane": "score_threshold_density_controlled_proxy_scout(점수 임계값 빈도 통제 프록시 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "frozen_9_cell_train_only_threshold_no_wfo_no_mt5_no_authority(고정 9칸 학습 전용 임계값, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_score_threshold_proxy",
            "subrun_id": f"{RUN_ID}__tier_a_score_threshold_proxy",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "score_threshold_proxy_not_runtime(점수 임계값 프록시, 런타임 아님)",
            "primary_kpi": primary_kpi_text(best),
            "notes": f"primary_strict={final['primary_strict_scout_clue_rows']};secondary_strict_like={final['secondary_strict_like_rows']};no_authority",
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
        f"cell={best.get('cell_id', '')};"
        f"primary={best.get('is_primary_cell', False)};"
        f"strict={best.get('strict_scout_clue_pass', False)};"
        f"secondary_strict_like={best.get('secondary_strict_like_pass', False)};"
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
