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
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_04 import frontier04b_path_aware_label_proxy_scout as f04b
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d


STAGE_ID = "stage_frontier_05__closed_bar_path_precursor_feature_surface"
RUN_ID = "frontier05B_closed_bar_path_precursor_feature_scout_v1"
RUN_NUMBER = "frontier05B"
PARENT_RUN_ID = "frontier05A_stage_open_closed_bar_path_precursor_feature_surface_v1"
SOURCE_PROXY_RUN_ID = "frontier04B_path_aware_label_proxy_scout_v1"
NEXT_CLUE_RUN_ID = "frontier05C_grok_pre_expensive_feature_surface_review_v1"
NEXT_NEGATIVE_RUN_ID = "frontier05C_feature_surface_repair_or_closeout_decision_v1"

LOCKED_VARIANT_ID = f04d.LOCKED_VARIANT_ID
LABEL_ORDER = f04d.LABEL_ORDER
LABEL_NAMES = f04d.LABEL_NAMES

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    full, raw, variant, proxy_metrics, source_integrity = load_training_packet()
    labels, proxy_signal, fwd_return = build_locked_labels(full, raw, variant)
    feature_order = f04d.read_feature_order()
    precursor_frame, feature_manifest = build_precursor_features(full, raw)
    result = train_and_evaluate(
        full=full,
        feature_order=feature_order,
        precursor_frame=precursor_frame,
        labels=labels,
        proxy_signal=proxy_signal,
        fwd_return=fwd_return,
        variant=variant,
        proxy_metrics=proxy_metrics,
    )
    final = build_final(result, source_integrity, feature_order, feature_manifest)
    artifacts = write_artifacts(full, precursor_frame, result, final, feature_manifest)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "run_id": RUN_ID,
                    "best_arm_id": final["best_row"].get("arm_id"),
                    "best_model_id": final["best_row"].get("model_id"),
                    "improvement_pass_rows": final["improvement_pass_rows"],
                    "next_run_id": final["next_run_id"],
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def load_training_packet() -> tuple[pd.DataFrame, pd.DataFrame, f04b.PathVariant, dict[str, Any], dict[str, Any]]:
    aligned, raw, source_integrity = f04b.load_and_align()
    variants = {variant.variant_id: variant for variant in f04b.build_variants(aligned, raw)}
    if LOCKED_VARIANT_ID not in variants:
        raise RuntimeError(f"Missing locked variant: {LOCKED_VARIANT_ID}")
    full = pd.read_parquet(io_path(f03b.DATASET_PATH)).sort_values("timestamp").reset_index(drop=True)
    full = full.merge(aligned[["timestamp", "raw_index"]], on="timestamp", how="left", validate="one_to_one")
    if full["raw_index"].isna().any():
        raise RuntimeError("Full model input failed raw_index merge.")
    full["raw_index"] = full["raw_index"].astype("int64")
    return full, raw, variants[LOCKED_VARIANT_ID], f04d.read_proxy_metrics(), source_integrity


def build_locked_labels(
    full: pd.DataFrame,
    raw: pd.DataFrame,
    variant: f04b.PathVariant,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    signal, _, _ = f04b.path_event_signal(full[["timestamp", "split", "raw_index"]].copy(), raw, variant)
    labels = np.where(signal < 0, 0, np.where(signal > 0, 2, 1)).astype("int64")
    raw_indexes = full["raw_index"].astype("int64").to_numpy()
    log_close = raw["log_close"].to_numpy(dtype="float64")
    fwd_return = log_close[raw_indexes + variant.horizon_bars] - log_close[raw_indexes]
    return labels, signal.astype("int8"), fwd_return


def build_precursor_features(full: pd.DataFrame, raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    raw_indexes = full["raw_index"].astype("int64").to_numpy()
    open_ = raw["open"].astype("float64").to_numpy()
    high = raw["high"].astype("float64").to_numpy()
    low = raw["low"].astype("float64").to_numpy()
    close = raw["close"].astype("float64").to_numpy()
    log_close = raw["log_close"].astype("float64").to_numpy()

    price_range = np.maximum(high - low, 1e-12)
    body = close - open_
    upper_wick = high - np.maximum(open_, close)
    lower_wick = np.minimum(open_, close) - low
    upper_wick_frac = upper_wick / price_range
    lower_wick_frac = lower_wick / price_range
    body_frac = body / price_range
    body_abs_frac = np.abs(body) / price_range
    close_pos = (close - low) / price_range
    tail_balance = lower_wick_frac - upper_wick_frac

    prev_close = np.roll(close, 1)
    prev_close[0] = close[0]
    true_range = np.maximum.reduce([high - low, np.abs(high - prev_close), np.abs(low - prev_close)])
    log_return_1 = np.diff(log_close, prepend=log_close[0])
    abs_return_1 = np.abs(log_return_1)

    range_ratio = (high - low) / np.maximum(close, 1e-12)
    atr14 = roll_mean(true_range / np.maximum(close, 1e-12), 14)
    atr14 = np.maximum(atr14, 1e-12)

    up_reach_6 = (close - roll_min(low, 6)) / np.maximum(close * atr14, 1e-12)
    down_reach_6 = (roll_max(high, 6) - close) / np.maximum(close * atr14, 1e-12)
    up_reach_12 = (close - roll_min(low, 12)) / np.maximum(close * atr14, 1e-12)
    down_reach_12 = (roll_max(high, 12) - close) / np.maximum(close * atr14, 1e-12)

    raw_features = {
        "f05_upper_wick_frac_1": upper_wick_frac,
        "f05_lower_wick_frac_1": lower_wick_frac,
        "f05_body_frac_1": body_frac,
        "f05_body_abs_frac_1": body_abs_frac,
        "f05_close_pos_range_1": close_pos,
        "f05_upper_wick_mean_6": roll_mean(upper_wick_frac, 6),
        "f05_lower_wick_mean_6": roll_mean(lower_wick_frac, 6),
        "f05_tail_balance_sum_6": roll_sum(tail_balance, 6),
        "f05_abs_tail_imbalance_mean_6": roll_mean(np.abs(tail_balance), 6),
        "f05_up_reach_atr_6": up_reach_6,
        "f05_down_reach_atr_6": down_reach_6,
        "f05_reach_asymmetry_6": up_reach_6 - down_reach_6,
        "f05_up_reach_atr_12": up_reach_12,
        "f05_down_reach_atr_12": down_reach_12,
        "f05_reach_asymmetry_12": up_reach_12 - down_reach_12,
        "f05_range_mean_6_over_30": roll_mean(range_ratio, 6) / np.maximum(roll_mean(range_ratio, 30), 1e-12),
        "f05_range_mean_12_over_50": roll_mean(range_ratio, 12) / np.maximum(roll_mean(range_ratio, 50), 1e-12),
        "f05_return_vol_6_over_30": roll_std(log_return_1, 6) / np.maximum(roll_std(log_return_1, 30), 1e-12),
        "f05_abs_return_1_over_abs_mean_12": abs_return_1 / np.maximum(roll_mean(abs_return_1, 12), 1e-12),
        "f05_range_percentile_50": roll_last_percentile(range_ratio, 50),
    }
    selected = {name: np.asarray(values, dtype="float64")[raw_indexes] for name, values in raw_features.items()}
    frame = pd.DataFrame(selected)
    if not np.isfinite(frame.to_numpy(dtype="float64")).all():
        bad_columns = [column for column in frame.columns if not np.isfinite(frame[column].to_numpy(dtype="float64")).all()]
        raise RuntimeError(f"Precursor feature matrix contains NaN or infinite values: {bad_columns}")
    manifest = {
        "feature_surface_id": "f05_closed_bar_path_precursor_v1",
        "feature_count": len(frame.columns),
        "feature_names": list(frame.columns),
        "feature_families": [
            "wick_body_pressure_and_tail_clustering(꼬리/몸통 압력과 꼬리 군집)",
            "recent_excursion_asymmetry(최근 진폭 비대칭)",
            "volatility_compression_expansion(변동성 수축/확장)",
        ],
        "boundary": "right-aligned current/prior closed US100 M5 OHLC only(우측 정렬 현재/과거 확정 US100 5분봉 OHLC 전용)",
        "raw_index_min": int(raw_indexes.min()),
        "raw_index_max": int(raw_indexes.max()),
        "row_count": int(len(frame)),
        "feature_order_hash": ordered_hash(list(frame.columns)),
    }
    return frame, manifest


def roll_mean(values: np.ndarray, window: int) -> np.ndarray:
    return pd.Series(values).rolling(window, min_periods=window).mean().to_numpy(dtype="float64")


def roll_sum(values: np.ndarray, window: int) -> np.ndarray:
    return pd.Series(values).rolling(window, min_periods=window).sum().to_numpy(dtype="float64")


def roll_std(values: np.ndarray, window: int) -> np.ndarray:
    return pd.Series(values).rolling(window, min_periods=window).std(ddof=0).to_numpy(dtype="float64")


def roll_min(values: np.ndarray, window: int) -> np.ndarray:
    return pd.Series(values).rolling(window, min_periods=window).min().to_numpy(dtype="float64")


def roll_max(values: np.ndarray, window: int) -> np.ndarray:
    return pd.Series(values).rolling(window, min_periods=window).max().to_numpy(dtype="float64")


def roll_last_percentile(values: np.ndarray, window: int) -> np.ndarray:
    def percentile(arr: np.ndarray) -> float:
        return float(np.count_nonzero(arr <= arr[-1]) / len(arr))

    return pd.Series(values).rolling(window, min_periods=window).apply(percentile, raw=True).to_numpy(dtype="float64")


def train_and_evaluate(
    full: pd.DataFrame,
    feature_order: list[str],
    precursor_frame: pd.DataFrame,
    labels: np.ndarray,
    proxy_signal: np.ndarray,
    fwd_return: np.ndarray,
    variant: f04b.PathVariant,
    proxy_metrics: dict[str, Any],
) -> dict[str, Any]:
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    missing = sorted(set(LABEL_ORDER) - set(int(v) for v in labels[train_mask]))
    if missing:
        raise RuntimeError(f"Train labels missing classes: {missing}")

    base_x = full[feature_order].astype("float64").to_numpy()
    aug_x = np.hstack([base_x, precursor_frame.astype("float64").to_numpy()])
    if not np.isfinite(base_x).all() or not np.isfinite(aug_x).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values.")

    arms = {
        "v2_only(피처세트v2단독)": {"x": base_x, "feature_count": len(feature_order), "extra_feature_count": 0},
        "v2_plus_f05_precursors(피처세트v2+전선05선행피처)": {
            "x": aug_x,
            "feature_count": aug_x.shape[1],
            "extra_feature_count": precursor_frame.shape[1],
        },
    }
    sample_indices = np.concatenate(
        [
            np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())[:256]
            for split in ("train", "validation", "oos")
        ]
    )
    model_rows: list[dict[str, Any]] = []
    class_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    retention_rows: list[dict[str, Any]] = []
    for arm_id, arm in arms.items():
        x_all = arm["x"]
        for spec in f04d.MODEL_SPECS:
            model = clone(spec.estimator)
            model.fit(x_all[train_mask], labels[train_mask])
            probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
            pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
            model_signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")
            safe_arm = arm_id.split("(")[0]
            model_path = MODEL_DIR / safe_arm / f"{spec.model_id}.joblib"
            onnx_path = MODEL_DIR / safe_arm / f"{spec.model_id}.onnx"
            io_path(model_path.parent).mkdir(parents=True, exist_ok=True)
            joblib.dump(model, io_path(model_path))
            export_meta = export_sklearn_to_onnx_zipmap_disabled(
                model,
                onnx_path,
                feature_count=int(arm["feature_count"]),
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
                    "arm_id": arm_id,
                    "model_id": spec.model_id,
                    "onnx_path": onnx_path.as_posix(),
                    "onnx_sha256": export_meta["sha256"],
                    "parity_passed": bool(parity["passed"]),
                    "parity_max_abs_diff": parity["max_abs_diff"],
                    "parity_mean_abs_diff": parity["mean_abs_diff"],
                    "rows_checked": parity["rows"],
                    "feature_count": int(arm["feature_count"]),
                }
            )
            reasons = np.full(len(full), f"model_argmax_{safe_arm}_{spec.model_id}(모델 최대 확률)", dtype=object)
            first_steps = np.zeros(len(full), dtype="int16")
            for split in ("train", "validation", "oos"):
                split_mask = full["split"].astype(str).eq(split).to_numpy()
                y_true = labels[split_mask]
                y_pred = pred_label[split_mask]
                class_rows.append(
                    {
                        "arm_id": arm_id,
                        "model_id": spec.model_id,
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
                metric = f04b.evaluate_split(
                    full,
                    model_signal,
                    fwd_return,
                    split,
                    variant,
                    f"{arm_id}_{spec.model_id}(모델 표면)",
                    reasons,
                    first_steps,
                )
                metric["arm_id"] = arm_id
                metric["model_id"] = spec.model_id
                metric["threshold_policy"] = spec.threshold_policy
                metric["feature_count"] = int(arm["feature_count"])
                metric["extra_feature_count"] = int(arm["extra_feature_count"])
                model_rows.append(metric)
                proxy_split = proxy_metrics[split]
                retention_rows.append(
                    {
                        "arm_id": arm_id,
                        "model_id": spec.model_id,
                        "split": split,
                        "model_trades_per_day": metric["trades_per_day"],
                        "proxy_trades_per_day": proxy_split["trades_per_day"],
                        "density_retention": safe_ratio(metric["trades_per_day"], proxy_split["trades_per_day"]),
                        "model_profit_factor": metric["profit_factor"],
                        "proxy_profit_factor": proxy_split["profit_factor"],
                        "pf_retention": safe_ratio(metric["profit_factor"], proxy_split["profit_factor"]),
                        "model_dd_risk_percent": metric["dd_risk_percent"],
                        "proxy_dd_risk_percent": proxy_split["dd_risk_percent"],
                        "dd_delta_percent": metric["dd_risk_percent"] - proxy_split["dd_risk_percent"],
                    }
                )
    return {
        "model_metrics": model_rows,
        "classification_metrics": class_rows,
        "parity": parity_rows,
        "retention": retention_rows,
        "arm_comparison": build_arm_comparison(model_rows, parity_rows),
        "label_distribution": f04d.label_distribution(full, labels),
    }


def build_arm_comparison(model_rows: list[dict[str, Any]], parity_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metrics = pd.DataFrame(model_rows)
    parity = pd.DataFrame(parity_rows)
    rows: list[dict[str, Any]] = []
    base_arm = "v2_only(피처세트v2단독)"
    aug_arm = "v2_plus_f05_precursors(피처세트v2+전선05선행피처)"
    for model_id in metrics["model_id"].drop_duplicates():
        entry: dict[str, Any] = {"model_id": model_id}
        for split in ("validation", "oos"):
            base = metrics[(metrics["arm_id"].eq(base_arm)) & (metrics["model_id"].eq(model_id)) & (metrics["split"].eq(split))].iloc[0]
            aug = metrics[(metrics["arm_id"].eq(aug_arm)) & (metrics["model_id"].eq(model_id)) & (metrics["split"].eq(split))].iloc[0]
            base_score = float(base["aspiration_distance_score"])
            aug_score = float(aug["aspiration_distance_score"])
            entry[f"{split}_base_score"] = base_score
            entry[f"{split}_aug_score"] = aug_score
            entry[f"{split}_score_improvement"] = base_score - aug_score
            entry[f"{split}_score_improvement_ratio"] = safe_ratio(base_score - aug_score, base_score)
            entry[f"{split}_base_pf"] = float(base["profit_factor"])
            entry[f"{split}_aug_pf"] = float(aug["profit_factor"])
            entry[f"{split}_base_density"] = float(base["trades_per_day"])
            entry[f"{split}_aug_density"] = float(aug["trades_per_day"])
            entry[f"{split}_base_dd"] = float(base["dd_risk_percent"])
            entry[f"{split}_aug_dd"] = float(aug["dd_risk_percent"])
        aug_parity = parity[(parity["arm_id"].eq(aug_arm)) & (parity["model_id"].eq(model_id))].iloc[0]
        combined_base = entry["validation_base_score"] + entry["oos_base_score"]
        combined_aug = entry["validation_aug_score"] + entry["oos_aug_score"]
        combined_ratio = safe_ratio(combined_base - combined_aug, combined_base)
        pass_flag = bool(
            aug_parity["parity_passed"]
            and combined_ratio >= 0.10
            and entry["validation_aug_dd"] <= entry["validation_base_dd"] + 2.0
            and entry["oos_aug_dd"] <= entry["oos_base_dd"] + 2.0
            and (entry["validation_aug_pf"] >= entry["validation_base_pf"] or entry["oos_aug_pf"] >= entry["oos_base_pf"])
        )
        entry.update(
            {
                "combined_base_score": combined_base,
                "combined_aug_score": combined_aug,
                "combined_score_improvement": combined_base - combined_aug,
                "combined_score_improvement_ratio": combined_ratio,
                "augmented_parity_passed": bool(aug_parity["parity_passed"]),
                "feature_surface_improvement_pass": pass_flag,
            }
        )
        rows.append(entry)
    return rows


def build_final(
    result: dict[str, Any],
    source_integrity: dict[str, Any],
    feature_order: list[str],
    feature_manifest: dict[str, Any],
) -> dict[str, Any]:
    comparison = pd.DataFrame(result["arm_comparison"]).sort_values(
        ["feature_surface_improvement_pass", "combined_score_improvement_ratio"],
        ascending=[False, False],
    )
    improvement_rows = int(comparison["feature_surface_improvement_pass"].sum()) if len(comparison) else 0
    best_comparison = dict(comparison.iloc[0]) if len(comparison) else {}
    metrics = pd.DataFrame(result["model_metrics"])
    best_arm = "v2_plus_f05_precursors(피처세트v2+전선05선행피처)" if improvement_rows else "v2_only(피처세트v2단독)"
    best_model = best_comparison.get("model_id", "none")
    best_metric = metrics[
        metrics["arm_id"].eq(best_arm)
        & metrics["model_id"].eq(best_model)
        & metrics["split"].eq("oos")
    ]
    best_row = dict(best_metric.iloc[0]) if len(best_metric) else {"arm_id": best_arm, "model_id": best_model}
    if improvement_rows:
        status = "feature_surface_scout_clue_no_authority"
        judgment = "scout_clue(탐색 단서)"
        next_run = NEXT_CLUE_RUN_ID
    else:
        status = "feature_surface_no_transfer_improvement_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run = NEXT_NEGATIVE_RUN_ID
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "created_at_utc": utc_now(),
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run,
        "locked_variant_id": LOCKED_VARIANT_ID,
        "model_count": len(f04d.MODEL_SPECS),
        "arm_count": 2,
        "improvement_pass_rows": improvement_rows,
        "best_row": json_ready(best_row),
        "best_comparison": json_ready(best_comparison),
        "feature_manifest": feature_manifest,
        "model_validation": {
            "model_family": "same Frontier04D sklearn LogisticRegression plus small RandomForest(전선04D와 같은 사이킷런 로지스틱 회귀와 작은 랜덤포레스트)",
            "target_and_label": "fixed Frontier04B path label class short/flat/long(전선04B 고정 경로 라벨 숏/플랫/롱)",
            "split_method": "fixed train/validation/OOS chronological split(고정 시간순 학습/검증/표본밖 분할)",
            "selection_metric": "augmented versus baseline aspiration-distance improvement(증강 대비 기준 목표거리 개선)",
            "secondary_metrics": "balanced accuracy, macro F1, density, PF, max DD, ONNX parity(균형 정확도, 매크로 F1, 밀도, 수익 팩터, 최대 손실폭, 온엑스 동등성)",
            "threshold_policy": "argmax only, no searched threshold(최대 확률 전용, 탐색 임계값 없음)",
            "overfit_risk": "handcrafted precursor features may overfit the single locked path label(수제 선행 피처가 단일 고정 경로 라벨에 과적합 가능)",
            "calibration_risk": "probabilities are classifier scores, not economic probabilities(확률은 분류 점수이지 경제 확률 아님)",
            "comparison_baseline": "feature_set_v2 only arm on identical labels/splits(동일 라벨/분할의 피처 세트 v2 단독 비교군)",
            "validation_judgment": "exploratory(탐색)",
        },
        "data_integrity": {
            **source_integrity,
            "feature_label_boundary": (
                "precursor features use current/prior closed raw OHLC only(선행 피처는 현재/과거 확정 원천 OHLC만 사용); "
                "fixed label uses future OHLC as supervised target only(고정 라벨은 지도학습 목표로만 미래 OHLC 사용)."
            ),
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
        },
        "runtime_parity": {
            "parity_check": "ONNXRuntime probability parity against sklearn for every arm/model(모든 비교군/모델의 사이킷런 대비 온엑스런타임 확률 동등성)",
            "runtime_claim_boundary": "research_only_no_mt5(연구 전용, MT5 없음)",
        },
        "artifact_lineage": {
            "source_inputs": [f03b.DATASET_PATH.as_posix(), f04b.RAW_US100.as_posix(), f04d.F04B_TOP.as_posix()],
            "producer": "stage_pipelines/stage_frontier_05/frontier05b_closed_bar_path_precursor_feature_scout.py",
            "consumer": next_run,
            "artifact_paths": [],
            "availability": "ignored_run_artifacts_with_tracked_report(무시 실행 산출물 + 추적 보고서)",
            "lineage_judgment": "connected_with_boundary(경계부 연결)",
        },
        "feature_order_hash": ordered_hash(feature_order),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_artifacts(
    full: pd.DataFrame,
    precursor_frame: pd.DataFrame,
    result: dict[str, Any],
    final: dict[str, Any],
    feature_manifest: dict[str, Any],
) -> dict[str, Path]:
    artifacts = {
        "feature_manifest": RUN_ROOT / "feature_manifest.json",
        "precursor_summary": RUN_ROOT / "precursor_feature_summary.csv",
        "model_metrics": RUN_ROOT / "model_metrics.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "retention": RUN_ROOT / "retention.csv",
        "arm_comparison": RUN_ROOT / "arm_comparison.csv",
        "label_distribution": RUN_ROOT / "label_distribution.csv",
        "integrity": RUN_ROOT / "integrity.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    write_json(artifacts["feature_manifest"], feature_manifest)
    precursor_frame.describe().T.reset_index(names="feature").to_csv(io_path(artifacts["precursor_summary"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["model_metrics"]).to_csv(io_path(artifacts["model_metrics"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["classification_metrics"]).to_csv(io_path(artifacts["classification_metrics"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["parity"]).to_csv(io_path(artifacts["onnx_parity"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["retention"]).to_csv(io_path(artifacts["retention"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["arm_comparison"]).to_csv(io_path(artifacts["arm_comparison"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["label_distribution"]).to_csv(io_path(artifacts["label_distribution"]), index=False, encoding="utf-8-sig")
    write_json(artifacts["integrity"], final["data_integrity"])
    final["artifact_lineage"]["artifact_paths"] = [path.as_posix() for path in artifacts.values()]
    manifest = {
        **final,
        "script_path": "stage_pipelines/stage_frontier_05/frontier05b_closed_bar_path_precursor_feature_scout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_05/frontier05b_closed_bar_path_precursor_feature_scout.py")),
        "artifacts": {
            name: {"path": path.as_posix(), "sha256": sha256_file(path)}
            for name, path in artifacts.items()
            if path_exists(path) and name != "run_manifest"
        },
        "model_specs": [asdict(spec) | {"estimator": str(spec.estimator)} for spec in f04d.MODEL_SPECS],
        "input_rows": int(len(full)),
        "precursor_feature_count": int(precursor_frame.shape[1]),
    }
    write_json(artifacts["run_manifest"], manifest)
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final.get("best_row", {})
    comp = final.get("best_comparison", {})
    text = f"""# Frontier05B Closed-Bar Path Precursor Feature Scout Report(전선05B 확정봉 경로 선행 피처 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): feature_set_v2 only arm(피처 세트 v2 단독 비교군)과 feature_set_v2 plus closed-bar path precursors arm(피처 세트 v2 + 확정봉 경로 선행 피처 비교군)을 같은 locked path label(고정 경로 라벨), rows(행), split(분할), model specs(모델 설정)에서 학습했습니다.

Effect(효과): Frontier04(전선04)의 oracle-to-model transfer collapse(오라클에서 모델 전달 붕괴)가 feature surface bottleneck(피처 표면 병목) 때문인지 통제 비교(controlled comparison, 통제 비교)로 확인했습니다.

## Best Read(최상위 판독)

- best arm(최상위 비교군): `{best.get('arm_id')}`
- best model(최상위 모델): `{best.get('model_id')}`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{fmt(best.get('profit_factor'))}` / `{fmt(best.get('trades_per_day'))}/day` / `{fmt(best.get('dd_risk_percent'))}%`
- improvement pass rows(개선 통과 행): `{final['improvement_pass_rows']}`

## Best Arm Comparison(최상위 비교군 비교)

- model(모델): `{comp.get('model_id', 'none')}`
- validation score improvement ratio(검증 점수 개선 비율): `{fmt(comp.get('validation_score_improvement_ratio'))}`
- OOS score improvement ratio(표본밖 점수 개선 비율): `{fmt(comp.get('oos_score_improvement_ratio'))}`
- combined score improvement ratio(합산 점수 개선 비율): `{fmt(comp.get('combined_score_improvement_ratio'))}`
- feature_surface_improvement_pass(피처 표면 개선 통과): `{comp.get('feature_surface_improvement_pass')}`

## Data Integrity(데이터 무결성)

- integrity_judgment(무결성 판정): `{final['data_integrity']['integrity_judgment']}`
- time_axis(시간축): {final['data_integrity']['time_axis']}
- feature_label_boundary(피처-라벨 경계): {final['data_integrity']['feature_label_boundary']}
- leakage_risk(누수 위험): {final['data_integrity']['leakage_risk']}

## Artifacts(산출물)

- arm comparison(비교군 비교): `{artifacts['arm_comparison'].as_posix()}`
- model metrics(모델 지표): `{artifacts['model_metrics'].as_posix()}`
- ONNX parity(온엑스 동등성): `{artifacts['onnx_parity'].as_posix()}`
- feature manifest(피처 목록): `{artifacts['feature_manifest'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 결과에 따라 Grok pre-expensive review(그록 사전 고비용 검토) 또는 repair/closeout decision(수리/마감 결정)으로 넘기는 것입니다. Effect(효과)는 scout clue(탐색 단서)를 WFO/MT5(워크포워드/메타트레이더5) 주장으로 과장하지 않는 것입니다.

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
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    for row in ledger_rows(final, artifacts):
        f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {now}: `{RUN_ID}` {final['judgment']}. Effect(효과): next run(다음 실행)은 `{final['next_run_id']}`입니다.\n",
    )
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{RUN_ID}`: closed-bar path precursor feature scout(확정봉 경로 선행 피처 탐색) recorded `{final['improvement_pass_rows']}` improvement pass rows(개선 통과 행). Effect(효과): feature bottleneck(피처 병목) 여부를 기준/증강 비교로 기록했습니다.\n",
    )
    if final["improvement_pass_rows"] == 0:
        f03b.append_once(
            f03b.NEGATIVE_RESULT_REGISTER,
            RUN_ID,
            f"- `{RUN_ID}`: closed-bar precursor augmentation did not pass controlled improvement criteria(확정봉 선행 피처 증강이 통제 개선 기준을 통과하지 못함). Effect(효과): label threshold sweep(라벨 임계값 탐색) 없이 repair/closeout decision(수리/마감 결정)으로 넘깁니다.\n",
        )


def current_state_text(final: dict[str, Any]) -> str:
    best = final.get("best_row", {})
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier05B(전선05B)는 closed-bar path precursor feature scout(확정봉 경로 선행 피처 탐색)를 완료했습니다.

Judgment(판정): `{final['judgment']}`

Best read(최상위 판독): `{best.get('arm_id', 'none')}` / `{best.get('model_id', 'none')}` with improvement_pass_rows(개선 통과 행) `{final['improvement_pass_rows']}`.

Next action(다음 행동): `{final['next_run_id']}`. Action(행동)은 결과 경계에 맞게 Grok pre-expensive review(그록 사전 고비용 검토) 또는 repair/closeout decision(수리/마감 결정)을 여는 것입니다. Effect(효과)는 scout result(탐색 결과)를 운영 주장(operating claim, 운영 주장)으로 과장하지 않는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final.get("best_row", {})
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "feature_surface_scout(피처 표면 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"improvement_pass_rows={final['improvement_pass_rows']};no_authority",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["improvement_pass_rows"]),
        "claim_boundary": "model_scout_onnx_parity_only_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_feature_surface_scout",
        "subrun_id": f"{RUN_ID}__tier_a_feature_surface_scout",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "feature_surface_model_scout_not_runtime(피처 표면 모델 탐색, 런타임 아님)",
        "primary_kpi": (
            f"best_arm={best.get('arm_id', 'none')};best_model={best.get('model_id', 'none')};"
            f"oos_pf={fmt(best.get('profit_factor'))};oos_density={fmt(best.get('trades_per_day'))};"
            f"oos_dd={fmt(best.get('dd_risk_percent'))}"
        ),
        "guardrail_kpi": "onnx_parity_only_no_wfo_no_mt5_no_authority(온엑스 동등성만, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "source_run_id": SOURCE_PROXY_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "feature_surface_model_scout_only(피처 표면 모델 탐색 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can closed-bar path precursor features improve path-label learnability?(확정봉 경로 선행 피처가 경로 라벨 학습 가능성을 개선하는가?)",
        "skill_family": "experiment_execution(실험 실행)",
        "lineage_summary": "raw_ohlc_to_closed_bar_precursors_to_model_metrics(원천 OHLC에서 확정봉 선행 피처와 모델 지표)",
    }


def ledger_rows(final: dict[str, Any], artifacts: dict[str, Path]) -> list[dict[str, Any]]:
    best = final.get("best_row", {})
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "feature_surface_scout(피처 표면 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "onnx_parity_only_no_wfo_no_mt5_no_authority(온엑스 동등성만, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_feature_surface_scout",
            "subrun_id": f"{RUN_ID}__tier_a_feature_surface_scout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "feature_surface_model_scout_not_runtime(피처 표면 모델 탐색, 런타임 아님)",
            "primary_kpi": (
                f"best_arm={best.get('arm_id', 'none')};best_model={best.get('model_id', 'none')};"
                f"oos_pf={fmt(best.get('profit_factor'))};oos_density={fmt(best.get('trades_per_day'))};"
                f"oos_dd={fmt(best.get('dd_risk_percent'))}"
            ),
            "notes": f"improvement_pass_rows={final['improvement_pass_rows']};no_authority",
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


def safe_ratio(value: Any, base: Any) -> float:
    try:
        numerator = float(value)
        denominator = float(base)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(numerator) or not math.isfinite(denominator) or abs(denominator) < 1e-12:
        return 0.0
    return numerator / denominator


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


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
