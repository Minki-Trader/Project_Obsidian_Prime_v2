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


STAGE_ID = "stage_frontier_06__selective_probability_abstention_signal_contract"
RUN_ID = "frontier06B_selective_probability_abstention_signal_scout_v1"
RUN_NUMBER = "frontier06B"
PARENT_RUN_ID = "frontier06A_stage_open_selective_probability_abstention_signal_contract_v1"
NEXT_CLUE_RUN_ID = "frontier06C_grok_pre_expensive_signal_contract_review_v1"
NEXT_NEGATIVE_RUN_ID = "frontier06C_signal_contract_closeout_decision_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"

LOCKED_VARIANT_ID = f04d.LOCKED_VARIANT_ID
LABEL_ORDER = f04d.LABEL_ORDER
LABEL_NAMES = f04d.LABEL_NAMES

SCORE_KINDS = ("directional_prob", "directional_margin", "directional_vs_flat")
FLAT_MAX_VALUES = (1.01, 0.65, 0.55)
MARGIN_FLOORS = (0.0, 0.03, 0.06)
TRAIN_DENSITY_TARGETS = (4.0, 6.0, 8.0, 10.0, 12.0)
SCOUT_DENSITY_FLOOR = 4.0
SCOUT_DENSITY_TARGET_LOW = 5.0
SCOUT_DENSITY_TARGET_HIGH = 10.0
SCOUT_PF_FLOOR = 1.2
SCOUT_DD_SOFT_CEILING = 15.0


@dataclass(frozen=True)
class SignalRule:
    rule_id: str
    model_id: str
    score_kind: str
    flat_max: float
    margin_floor: float
    train_density_target: float
    score_threshold: float
    train_candidate_count: int


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    full, raw, variant, source_integrity = load_training_packet()
    labels, _, fwd_return = build_locked_labels(full, raw, variant)
    feature_order = f04d.read_feature_order()
    result = train_and_evaluate(full, feature_order, labels, fwd_return, variant)
    final = build_final(result, source_integrity, feature_order)
    artifacts = write_artifacts(result, final)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "best_rule_id": final["best_rule_row"].get("rule_id"),
        "scout_clue_rows": final["scout_clue_rows"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def load_training_packet() -> tuple[pd.DataFrame, pd.DataFrame, f04b.PathVariant, dict[str, Any]]:
    aligned, raw, source_integrity = f04b.load_and_align()
    variants = {variant.variant_id: variant for variant in f04b.build_variants(aligned, raw)}
    if LOCKED_VARIANT_ID not in variants:
        raise RuntimeError(f"Missing locked variant: {LOCKED_VARIANT_ID}")
    full = pd.read_parquet(io_path(f03b.DATASET_PATH)).sort_values("timestamp").reset_index(drop=True)
    full = full.merge(aligned[["timestamp", "raw_index"]], on="timestamp", how="left", validate="one_to_one")
    if full["raw_index"].isna().any():
        raise RuntimeError("Full model input failed raw_index merge.")
    full["raw_index"] = full["raw_index"].astype("int64")
    return full, raw, variants[LOCKED_VARIANT_ID], source_integrity


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


def train_and_evaluate(
    full: pd.DataFrame,
    feature_order: list[str],
    labels: np.ndarray,
    fwd_return: np.ndarray,
    variant: f04b.PathVariant,
) -> dict[str, Any]:
    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values.")
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    missing = sorted(set(LABEL_ORDER) - set(int(v) for v in labels[train_mask]))
    if missing:
        raise RuntimeError(f"Train labels missing classes: {missing}")

    baseline_rows: list[dict[str, Any]] = []
    rule_rows: list[dict[str, Any]] = []
    rule_summary_rows: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    sample_indices = np.concatenate([
        np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())[:256]
        for split in ("train", "validation", "oos")
    ])
    train_days = scout.count_scope_days(full.loc[train_mask, "timestamp"])
    for spec in f04d.MODEL_SPECS:
        model = clone(spec.estimator)
        model.fit(x_all[train_mask], labels[train_mask])
        probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
        pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
        argmax_signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")

        model_path = MODEL_DIR / f"{spec.model_id}.joblib"
        onnx_path = MODEL_DIR / f"{spec.model_id}.onnx"
        io_path(model_path.parent).mkdir(parents=True, exist_ok=True)
        joblib.dump(model, io_path(model_path))
        export_meta = export_sklearn_to_onnx_zipmap_disabled(
            model,
            onnx_path,
            feature_count=len(feature_order),
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
            "model_id": spec.model_id,
            "onnx_path": onnx_path.as_posix(),
            "onnx_sha256": export_meta["sha256"],
            "parity_passed": bool(parity["passed"]),
            "parity_max_abs_diff": parity["max_abs_diff"],
            "parity_mean_abs_diff": parity["mean_abs_diff"],
            "rows_checked": parity["rows"],
        })
        for split in ("train", "validation", "oos"):
            split_mask = full["split"].astype(str).eq(split).to_numpy()
            y_true = labels[split_mask]
            y_pred = pred_label[split_mask]
            classification_rows.append({
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
            })
            metric = f04b.evaluate_split(
                full,
                argmax_signal,
                fwd_return,
                split,
                variant,
                f"argmax_baseline_{spec.model_id}(최대 확률 기준)",
                np.full(len(full), "argmax_baseline(최대 확률 기준)", dtype=object),
                np.zeros(len(full), dtype="int16"),
            )
            metric["model_id"] = spec.model_id
            metric["rule_id"] = f"argmax_baseline__{spec.model_id}"
            metric["signal_contract"] = "argmax_baseline(최대 확률 기준)"
            baseline_rows.append(metric)

        rules = fit_rules_from_train(full, probabilities, spec.model_id, train_days)
        for rule in rules:
            signal = apply_rule(probabilities, rule)
            for split in ("train", "validation", "oos"):
                metric = f04b.evaluate_split(
                    full,
                    signal,
                    fwd_return,
                    split,
                    variant,
                    f"selective_abstention_{rule.rule_id}(선택 기권)",
                    np.full(len(full), f"selective_abstention_{rule.rule_id}(선택 기권)", dtype=object),
                    np.zeros(len(full), dtype="int16"),
                )
                metric.update(as_rule_dict(rule))
                metric["signal_contract"] = "selective_probability_abstention(선택적 확률 기권)"
                rule_rows.append(metric)
            rule_summary_rows.append(summarize_rule(full, rule, signal))
    return {
        "baseline_metrics": baseline_rows,
        "rule_metrics": rule_rows,
        "rule_summary": rule_summary_rows,
        "classification_metrics": classification_rows,
        "parity": parity_rows,
        "rule_comparison": build_rule_comparison(baseline_rows, rule_rows, parity_rows),
        "label_distribution": f04d.label_distribution(full, labels),
    }


def fit_rules_from_train(full: pd.DataFrame, probabilities: np.ndarray, model_id: str, train_days: int) -> list[SignalRule]:
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    directional_margin = np.abs(p_long - p_short)
    rules: list[SignalRule] = []
    for score_kind in SCORE_KINDS:
        scores = score_values(probabilities, score_kind)
        for flat_max in FLAT_MAX_VALUES:
            for margin_floor in MARGIN_FLOORS:
                candidate_mask = train_mask & (p_flat <= flat_max) & (directional_margin >= margin_floor)
                candidate_scores = scores[candidate_mask]
                if candidate_scores.size == 0:
                    continue
                for density_target in TRAIN_DENSITY_TARGETS:
                    target_count = max(1, int(math.ceil(density_target * max(train_days, 1))))
                    if target_count >= candidate_scores.size:
                        threshold = float(np.nanmin(candidate_scores))
                    else:
                        threshold = float(np.partition(candidate_scores, -target_count)[-target_count])
                    rule_id = (
                        f"{model_id}__{score_kind}__flat{flat_max:.2f}__margin{margin_floor:.2f}__d{density_target:.1f}"
                    ).replace(".", "p")
                    rules.append(SignalRule(
                        rule_id=rule_id,
                        model_id=model_id,
                        score_kind=score_kind,
                        flat_max=flat_max,
                        margin_floor=margin_floor,
                        train_density_target=density_target,
                        score_threshold=threshold,
                        train_candidate_count=int(candidate_scores.size),
                    ))
    return rules


def score_values(probabilities: np.ndarray, score_kind: str) -> np.ndarray:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    max_directional = np.maximum(p_short, p_long)
    if score_kind == "directional_prob":
        return max_directional
    if score_kind == "directional_margin":
        return np.abs(p_long - p_short)
    if score_kind == "directional_vs_flat":
        return max_directional - p_flat
    raise ValueError(f"Unknown score kind: {score_kind}")


def apply_rule(probabilities: np.ndarray, rule: SignalRule) -> np.ndarray:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    directional_margin = np.abs(p_long - p_short)
    scores = score_values(probabilities, rule.score_kind)
    direction = np.where(p_long > p_short, 1, -1).astype("int8")
    active = (p_flat <= rule.flat_max) & (directional_margin >= rule.margin_floor) & (scores >= rule.score_threshold)
    signal = np.zeros(len(probabilities), dtype="int8")
    signal[active] = direction[active]
    return signal


def summarize_rule(full: pd.DataFrame, rule: SignalRule, signal: np.ndarray) -> dict[str, Any]:
    row = as_rule_dict(rule)
    for split in ("train", "validation", "oos"):
        mask = full["split"].astype(str).eq(split).to_numpy()
        days = scout.count_scope_days(full.loc[mask, "timestamp"])
        trades = int((signal[mask] != 0).sum())
        row[f"{split}_trade_count"] = trades
        row[f"{split}_trades_per_day"] = float(trades / days) if days else 0.0
        row[f"{split}_long_count"] = int((signal[mask] == 1).sum())
        row[f"{split}_short_count"] = int((signal[mask] == -1).sum())
    return row


def build_rule_comparison(
    baseline_rows: list[dict[str, Any]],
    rule_rows: list[dict[str, Any]],
    parity_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    baseline = pd.DataFrame(baseline_rows)
    rules = pd.DataFrame(rule_rows)
    parity = pd.DataFrame(parity_rows)
    rows: list[dict[str, Any]] = []
    for rule_id, group in rules.groupby("rule_id", sort=False):
        model_id = str(group["model_id"].iloc[0])
        row: dict[str, Any] = {
            "rule_id": rule_id,
            "model_id": model_id,
            "score_kind": str(group["score_kind"].iloc[0]),
            "flat_max": float(group["flat_max"].iloc[0]),
            "margin_floor": float(group["margin_floor"].iloc[0]),
            "train_density_target": float(group["train_density_target"].iloc[0]),
            "score_threshold": float(group["score_threshold"].iloc[0]),
        }
        score_improvements: list[float] = []
        for split in ("validation", "oos"):
            base = baseline[(baseline["model_id"].eq(model_id)) & (baseline["split"].eq(split))].iloc[0]
            current = group[group["split"].eq(split)].iloc[0]
            base_score = float(base["aspiration_distance_score"])
            current_score = float(current["aspiration_distance_score"])
            row[f"{split}_base_score"] = base_score
            row[f"{split}_rule_score"] = current_score
            row[f"{split}_score_improvement"] = base_score - current_score
            row[f"{split}_score_improvement_ratio"] = safe_ratio(base_score - current_score, base_score)
            row[f"{split}_base_density"] = float(base["trades_per_day"])
            row[f"{split}_rule_density"] = float(current["trades_per_day"])
            row[f"{split}_base_pf"] = float(base["profit_factor"])
            row[f"{split}_rule_pf"] = float(current["profit_factor"])
            row[f"{split}_base_dd"] = float(base["dd_risk_percent"])
            row[f"{split}_rule_dd"] = float(current["dd_risk_percent"])
            row[f"{split}_net_profit"] = float(current["net_profit"])
            row[f"{split}_density_floor_pass"] = bool(float(current["trades_per_day"]) >= SCOUT_DENSITY_FLOOR)
            row[f"{split}_density_target_band"] = bool(SCOUT_DENSITY_TARGET_LOW <= float(current["trades_per_day"]) <= SCOUT_DENSITY_TARGET_HIGH)
            row[f"{split}_pf_floor_pass"] = bool(float(current["profit_factor"]) >= SCOUT_PF_FLOOR and float(current["net_profit"]) > 0)
            row[f"{split}_dd_soft_pass"] = bool(float(current["dd_risk_percent"]) <= SCOUT_DD_SOFT_CEILING)
            score_improvements.append(base_score - current_score)
        parity_row = parity[parity["model_id"].eq(model_id)].iloc[0]
        both_floor = bool(row["validation_density_floor_pass"] and row["oos_density_floor_pass"])
        both_pf = bool(row["validation_pf_floor_pass"] and row["oos_pf_floor_pass"])
        both_dd = bool(row["validation_dd_soft_pass"] and row["oos_dd_soft_pass"])
        both_improve = bool(row["validation_score_improvement"] > 0 and row["oos_score_improvement"] > 0)
        strict = bool(parity_row["parity_passed"] and both_floor and both_pf and both_dd and both_improve)
        row["combined_score_improvement"] = float(sum(score_improvements))
        row["combined_score_improvement_ratio"] = safe_ratio(row["combined_score_improvement"], row["validation_base_score"] + row["oos_base_score"])
        row["parity_passed"] = bool(parity_row["parity_passed"])
        row["strict_scout_clue_pass"] = strict
        row["partial_axis_gain"] = bool((row["validation_score_improvement"] > 0) or (row["oos_score_improvement"] > 0))
        row["low_density_cherrypick_flag"] = bool((row["validation_rule_density"] < SCOUT_DENSITY_FLOOR) or (row["oos_rule_density"] < SCOUT_DENSITY_FLOOR))
        rows.append(row)
    return rows


def build_final(result: dict[str, Any], source_integrity: dict[str, Any], feature_order: list[str]) -> dict[str, Any]:
    comparison = pd.DataFrame(result["rule_comparison"])
    comparison = comparison.sort_values(
        ["strict_scout_clue_pass", "combined_score_improvement_ratio", "oos_rule_pf", "oos_rule_dd"],
        ascending=[False, False, False, True],
    )
    clue_rows = int(comparison["strict_scout_clue_pass"].sum()) if len(comparison) else 0
    partial_rows = int(comparison["partial_axis_gain"].sum()) if len(comparison) else 0
    best = dict(comparison.iloc[0]) if len(comparison) else {}
    if clue_rows:
        status = "selective_abstention_scout_clue_no_authority"
        judgment = "scout_clue(탐색 단서)"
        next_run = NEXT_CLUE_RUN_ID
    else:
        status = "selective_abstention_no_strict_clue_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run = NEXT_NEGATIVE_RUN_ID
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": utc_now(),
        "status": status,
        "judgment": judgment,
        "next_run_id": next_run,
        "locked_variant_id": LOCKED_VARIANT_ID,
        "model_count": len(f04d.MODEL_SPECS),
        "signal_rule_count": len(result["rule_comparison"]),
        "scout_clue_rows": clue_rows,
        "partial_axis_gain_rows": partial_rows,
        "best_rule_row": json_ready(best),
        "model_validation": {
            "model_family": "same Frontier04D sklearn LogisticRegression plus small RandomForest(전선04D와 같은 사이킷런 로지스틱 회귀와 작은 랜덤포레스트)",
            "target_and_label": "fixed Frontier04B path label reference target(전선04B 고정 경로 라벨 참조 목표)",
            "split_method": "fixed train/validation/OOS chronological split(고정 시간순 학습/검증/표본밖 분할)",
            "selection_metric": "strict scout clue then combined four-axis distance improvement(엄격 탐색 단서 후 네 축 거리 개선)",
            "secondary_metrics": "density, PF, DD, net profit, balanced accuracy, ONNX parity(밀도, 수익 팩터, 손실폭, 순수익, 균형 정확도, 온엑스 동등성)",
            "threshold_policy": "train-only calibrated score thresholds, no validation/OOS fitting(학습 전용 점수 임계값, 검증/표본밖 적합 없음)",
            "overfit_risk": "broad signal grid may still select train score artifacts(넓은 신호 격자도 학습 점수 산출물에 과적합 가능)",
            "calibration_risk": "probabilities are ranking scores, not calibrated probability truth(확률은 순위 점수이지 보정 확률 진실 아님)",
            "comparison_baseline": "same model argmax baseline(같은 모델 최대 확률 기준)",
            "validation_judgment": "exploratory(탐색)",
        },
        "data_integrity": {
            **source_integrity,
            "feature_label_boundary": (
                "signal rules use model probabilities from current closed-bar features only(신호 규칙은 현재 확정봉 피처에서 나온 모델 확률만 사용); "
                "thresholds are fit on train split only(임계값은 학습 분할에서만 적합)."
            ),
            "split_boundary": "train threshold fit; validation/OOS evaluation only(학습 임계값 적합, 검증/표본밖 평가 전용)",
            "leakage_risk": "validation/OOS rule selection after seeing summary is the main selection-bias risk(요약을 본 뒤 검증/표본밖 규칙 선택이 주요 선택 편향 위험)",
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
        },
        "runtime_parity": {
            "parity_check": "ONNXRuntime probability parity against sklearn for each model(각 모델의 사이킷런 대비 온엑스런타임 확률 동등성)",
            "runtime_claim_boundary": "research_only_no_mt5(연구 전용, MT5 없음)",
        },
        "artifact_lineage": {
            "source_inputs": [f03b.DATASET_PATH.as_posix(), f04b.RAW_US100.as_posix()],
            "producer": "stage_pipelines/stage_frontier_06/frontier06b_selective_probability_abstention_signal_scout.py",
            "consumer": next_run,
            "artifact_paths": [],
            "availability": "ignored_run_artifacts_with_tracked_report(무시 실행 산출물 + 추적 보고서)",
            "lineage_judgment": "connected_with_boundary(경계부 연결)",
        },
        "feature_order_hash": ordered_hash(feature_order),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_artifacts(result: dict[str, Any], final: dict[str, Any]) -> dict[str, Path]:
    artifacts = {
        "baseline_metrics": RUN_ROOT / "argmax_baseline_metrics.csv",
        "rule_metrics": RUN_ROOT / "signal_rule_metrics.csv",
        "rule_summary": RUN_ROOT / "signal_rule_summary.csv",
        "rule_comparison": RUN_ROOT / "signal_rule_comparison.csv",
        "classification_metrics": RUN_ROOT / "classification_metrics.csv",
        "onnx_parity": RUN_ROOT / "onnx_parity.csv",
        "label_distribution": RUN_ROOT / "label_distribution.csv",
        "integrity": RUN_ROOT / "integrity.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    pd.DataFrame(result["baseline_metrics"]).to_csv(io_path(artifacts["baseline_metrics"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["rule_metrics"]).to_csv(io_path(artifacts["rule_metrics"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["rule_summary"]).to_csv(io_path(artifacts["rule_summary"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["rule_comparison"]).to_csv(io_path(artifacts["rule_comparison"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["classification_metrics"]).to_csv(io_path(artifacts["classification_metrics"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["parity"]).to_csv(io_path(artifacts["onnx_parity"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["label_distribution"]).to_csv(io_path(artifacts["label_distribution"]), index=False, encoding="utf-8-sig")
    write_json(artifacts["integrity"], final["data_integrity"])
    final["artifact_lineage"]["artifact_paths"] = [path.as_posix() for path in artifacts.values()]
    manifest = {
        **final,
        "script_path": "stage_pipelines/stage_frontier_06/frontier06b_selective_probability_abstention_signal_scout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_06/frontier06b_selective_probability_abstention_signal_scout.py")),
        "artifacts": {
            name: {"path": path.as_posix(), "sha256": sha256_file(path)}
            for name, path in artifacts.items()
            if path_exists(path) and name != "run_manifest"
        },
        "signal_grid": {
            "score_kinds": SCORE_KINDS,
            "flat_max_values": FLAT_MAX_VALUES,
            "margin_floors": MARGIN_FLOORS,
            "train_density_targets": TRAIN_DENSITY_TARGETS,
            "rule_count_cap": len(SCORE_KINDS) * len(FLAT_MAX_VALUES) * len(MARGIN_FLOORS) * len(TRAIN_DENSITY_TARGETS) * len(f04d.MODEL_SPECS),
        },
    }
    write_json(artifacts["run_manifest"], manifest)
    return artifacts


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final.get("best_rule_row", {})
    text = f"""# Frontier06B Selective Probability Abstention Signal Scout Report(전선06B 선택적 확률 기권 신호 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): same model probabilities(같은 모델 확률)에 train-only calibrated abstention rules(학습 전용 보정 기권 규칙)을 적용하고 argmax baseline(최대 확률 기준)과 비교했습니다.

Effect(효과): label/feature/model(라벨/피처/모델)을 바꾸지 않고 output-to-trade signal contract(출력-거래 신호 계약)만 바꿔 overtrading/DD failure(과다거래/손실폭 실패)를 줄일 수 있는지 확인했습니다.

## Best Rule Read(최상위 규칙 판독)

- rule(규칙): `{best.get('rule_id')}`
- model(모델): `{best.get('model_id')}`
- score kind(점수 종류): `{best.get('score_kind')}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_rule_pf'))}` / `{fmt(best.get('validation_rule_density'))}/day` / `{fmt(best.get('validation_rule_dd'))}%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_rule_pf'))}` / `{fmt(best.get('oos_rule_density'))}/day` / `{fmt(best.get('oos_rule_dd'))}%`
- strict scout clue pass(엄격 탐색 단서 통과): `{best.get('strict_scout_clue_pass')}`
- scout clue rows(탐색 단서 행): `{final['scout_clue_rows']}`

## Boundaries(경계)

- threshold policy(임계값 정책): `{final['model_validation']['threshold_policy']}`
- probability meaning(확률 의미): `{final['model_validation']['calibration_risk']}`
- runtime boundary(런타임 경계): `{final['runtime_parity']['runtime_claim_boundary']}`
- Tier B/Tier A+B(티어 B/티어 A+B): missing_required(필수 누락) rows are recorded in ledgers(장부에 기록됨).

## Artifacts(산출물)

- rule comparison(규칙 비교): `{artifacts['rule_comparison'].as_posix()}`
- rule metrics(규칙 지표): `{artifacts['rule_metrics'].as_posix()}`
- argmax baseline(최대 확률 기준): `{artifacts['baseline_metrics'].as_posix()}`
- ONNX parity(온엑스 동등성): `{artifacts['onnx_parity'].as_posix()}`
- run manifest(실행 목록): `{artifacts['run_manifest'].as_posix()}`

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 scout result(탐색 결과)를 Grok review(그록 검토) 또는 closeout decision(마감 결정)으로 넘기는 것입니다. Effect(효과)는 threshold micro-search(임계값 미세탐색)로 새지 않고 stage lifecycle(단계 생명주기)을 유지하는 것입니다.

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
        f"- `{RUN_ID}`: selective probability abstention signal scout(선택적 확률 기권 신호 탐색) recorded `{final['scout_clue_rows']}` strict scout clue rows(엄격 탐색 단서 행). Effect(효과): output-to-trade contract(출력-거래 계약)의 가치 여부를 기록했습니다.\n",
    )
    if final["scout_clue_rows"] == 0:
        f03b.append_once(
            f03b.NEGATIVE_RESULT_REGISTER,
            RUN_ID,
            f"- `{RUN_ID}`: selective abstention signal contract did not produce strict validation+OOS scout clue(선택적 기권 신호 계약이 검증+표본밖 엄격 탐색 단서를 만들지 못함). Effect(효과): unbounded threshold micro-search(무제한 임계값 미세탐색)를 막고 closeout decision(마감 결정)으로 넘깁니다.\n",
        )


def current_state_text(final: dict[str, Any]) -> str:
    best = final.get("best_rule_row", {})
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier06B(전선06B)는 selective probability abstention signal scout(선택적 확률 기권 신호 탐색)를 완료했습니다.

Judgment(판정): `{final['judgment']}`

Best read(최상위 판독): `{best.get('rule_id', 'none')}` with scout_clue_rows(탐색 단서 행) `{final['scout_clue_rows']}`.

Next action(다음 행동): `{final['next_run_id']}`. Action(행동)은 result boundary(결과 경계)에 맞게 Grok review(그록 검토) 또는 closeout decision(마감 결정)을 여는 것입니다. Effect(효과)는 threshold micro-search(임계값 미세탐색)를 반복하지 않는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final.get("best_rule_row", {})
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "signal_contract_scout(신호 계약 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"scout_clue_rows={final['scout_clue_rows']};partial_axis_gain_rows={final['partial_axis_gain_rows']};no_authority",
        "work_family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["scout_clue_rows"]),
        "claim_boundary": "signal_scout_onnx_parity_only_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__tier_a_signal_contract_scout",
        "subrun_id": f"{RUN_ID}__tier_a_signal_contract_scout",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "signal_contract_model_scout_not_runtime(신호 계약 모델 탐색, 런타임 아님)",
        "primary_kpi": f"best={best.get('rule_id', 'none')};oos_pf={fmt(best.get('oos_rule_pf'))};oos_density={fmt(best.get('oos_rule_density'))};oos_dd={fmt(best.get('oos_rule_dd'))}",
        "guardrail_kpi": "train_only_thresholds_no_wfo_no_mt5_no_authority(학습 전용 임계값, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "signal_contract_scout_only(신호 계약 탐색 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can train-only selective abstention improve weak path-label model signals?(학습 전용 선택 기권이 약한 경로 라벨 모델 신호를 개선하는가?)",
        "skill_family": "experiment_execution(실험 실행)",
        "lineage_summary": "model_probabilities_to_selective_signal_contract_metrics(모델 확률에서 선택 신호 계약 지표)",
    }


def ledger_rows(final: dict[str, Any], artifacts: dict[str, Path]) -> list[dict[str, Any]]:
    best = final.get("best_rule_row", {})
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "signal_contract_scout(신호 계약 탐색)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "train_only_thresholds_no_wfo_no_mt5_no_authority(학습 전용 임계값, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_signal_contract_scout",
            "subrun_id": f"{RUN_ID}__tier_a_signal_contract_scout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "signal_contract_model_scout_not_runtime(신호 계약 모델 탐색, 런타임 아님)",
            "primary_kpi": f"best={best.get('rule_id', 'none')};oos_pf={fmt(best.get('oos_rule_pf'))};oos_density={fmt(best.get('oos_rule_density'))};oos_dd={fmt(best.get('oos_rule_dd'))}",
            "notes": f"scout_clue_rows={final['scout_clue_rows']};no_authority",
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


def as_rule_dict(rule: SignalRule) -> dict[str, Any]:
    return {
        "rule_id": rule.rule_id,
        "model_id": rule.model_id,
        "score_kind": rule.score_kind,
        "flat_max": rule.flat_max,
        "margin_floor": rule.margin_floor,
        "train_density_target": rule.train_density_target,
        "score_threshold": rule.score_threshold,
        "train_candidate_count": rule.train_candidate_count,
    }


def safe_ratio(value: Any, base: Any) -> float:
    try:
        numerator = float(value)
        denominator = float(base)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(numerator) or not math.isfinite(denominator) or abs(denominator) < 1e-12:
        return 0.0
    return numerator / denominator


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
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
