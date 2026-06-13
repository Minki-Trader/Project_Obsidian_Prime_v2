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
from sklearn.ensemble import RandomForestClassifier
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


STAGE_ID = "stage_frontier_04__path_aware_cost_dd_event_labeling"
RUN_ID = "frontier04D_trainable_path_label_onnx_probe_v1"
RUN_NUMBER = "frontier04D"
PARENT_RUN_ID = "frontier04C_grok_pre_trainable_transfer_review_v1"
SOURCE_PROXY_RUN_ID = "frontier04B_path_aware_label_proxy_scout_v1"
NEXT_PARTIAL_RUN_ID = "frontier04E_trainable_transfer_repair_or_second_probe_v1"
NEXT_COLLAPSE_RUN_ID = "frontier04E_oracle_to_model_collapse_closeout_decision_v1"

LOCKED_VARIANT_ID = "f04b_path_h12_t1p20_s0p80_trainp90"
LABEL_ORDER = [0, 1, 2]
LABEL_NAMES = {0: "short", 1: "flat", 2: "long"}

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MODEL_DIR = RUN_ROOT / "models"
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"

F04B_RUN_ROOT = STAGE_ROOT / "02_runs" / SOURCE_PROXY_RUN_ID
F04B_TOP = F04B_RUN_ROOT / "top.csv"
F04B_INTEGRITY = F04B_RUN_ROOT / "integrity.json"
F04B_MANIFEST = F04B_RUN_ROOT / "run_manifest.json"


@dataclass(frozen=True)
class ModelSpec:
    model_id: str
    estimator: Pipeline
    threshold_policy: str


MODEL_SPECS = (
    ModelSpec(
        model_id="logreg_l2_c0p5_plain_argmax",
        estimator=Pipeline(
            [
                ("scaler", StandardScaler()),
                ("classifier", LogisticRegression(max_iter=2000, C=0.5, random_state=7, solver="lbfgs")),
            ]
        ),
        threshold_policy="argmax_no_threshold(최대 확률, 임계값 없음)",
    ),
    ModelSpec(
        model_id="logreg_l2_c0p5_balanced_argmax",
        estimator=Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(max_iter=2000, C=0.5, random_state=7, solver="lbfgs", class_weight="balanced"),
                ),
            ]
        ),
        threshold_policy="argmax_no_threshold_class_weight_balanced(최대 확률, 균형 가중)",
    ),
    ModelSpec(
        model_id="rf_depth5_leaf80_balanced_argmax",
        estimator=RandomForestClassifier(
            n_estimators=80,
            max_depth=5,
            min_samples_leaf=80,
            class_weight="balanced_subsample",
            random_state=7,
            n_jobs=-1,
        ),
        threshold_policy="argmax_no_threshold_small_tree_balanced(최대 확률, 작은 트리 균형 가중)",
    ),
)


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    full, raw, variant, proxy_metrics, integrity = load_training_packet()
    labels, proxy_signal, fwd_return = build_locked_labels(full, raw, variant)
    feature_order = read_feature_order()
    result = train_and_evaluate(full, feature_order, labels, proxy_signal, fwd_return, variant, proxy_metrics)
    final = build_final(result, proxy_metrics, integrity, feature_order)
    artifacts = write_artifacts(full, feature_order, labels, result, final, integrity)
    write_report(final, artifacts)
    update_registries(final, artifacts)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "best_model_id": final["best_model_id"],
        "partial_transfer_rows": final["partial_transfer_rows"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def load_training_packet() -> tuple[pd.DataFrame, pd.DataFrame, f04b.PathVariant, dict[str, Any], dict[str, Any]]:
    aligned, raw, _ = f04b.load_and_align()
    variants = {variant.variant_id: variant for variant in f04b.build_variants(aligned, raw)}
    if LOCKED_VARIANT_ID not in variants:
        raise RuntimeError(f"Missing locked variant: {LOCKED_VARIANT_ID}")
    full = pd.read_parquet(io_path(f03b.DATASET_PATH)).sort_values("timestamp").reset_index(drop=True)
    full = full.merge(aligned[["timestamp", "raw_index"]], on="timestamp", how="left", validate="one_to_one")
    if full["raw_index"].isna().any():
        raise RuntimeError("Full model input failed raw_index merge.")
    full["raw_index"] = full["raw_index"].astype("int64")
    proxy_metrics = read_proxy_metrics()
    integrity = read_json(F04B_INTEGRITY)
    return full, raw, variants[LOCKED_VARIANT_ID], proxy_metrics, integrity


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
    proxy_signal: np.ndarray,
    fwd_return: np.ndarray,
    variant: f04b.PathVariant,
    proxy_metrics: dict[str, Any],
) -> dict[str, Any]:
    x_all = full[feature_order].astype("float64").to_numpy()
    if not np.isfinite(x_all).all():
        raise RuntimeError("Feature matrix contains NaN or infinite values.")
    train_mask = full["split"].astype(str).eq("train").to_numpy()
    missing = sorted(set(LABEL_ORDER) - set(int(v) for v in labels[train_mask]))
    if missing:
        raise RuntimeError(f"Train labels missing classes: {missing}")
    model_rows: list[dict[str, Any]] = []
    class_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    retention_rows: list[dict[str, Any]] = []
    sample_indices = np.concatenate(
        [
            np.flatnonzero(full["split"].astype(str).eq(split).to_numpy())[:256]
            for split in ("train", "validation", "oos")
        ]
    )
    for spec in MODEL_SPECS:
        model = clone(spec.estimator)
        model.fit(x_all[train_mask], labels[train_mask])
        probabilities = ordered_sklearn_probabilities(model, x_all, class_order=LABEL_ORDER)
        pred_label = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
        model_signal = np.where(pred_label == 0, -1, np.where(pred_label == 2, 1, 0)).astype("int8")
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
        parity_rows.append(
            {
                "model_id": spec.model_id,
                "onnx_path": onnx_path.as_posix(),
                "onnx_sha256": export_meta["sha256"],
                "parity_passed": bool(parity["passed"]),
                "parity_max_abs_diff": parity["max_abs_diff"],
                "parity_mean_abs_diff": parity["mean_abs_diff"],
                "rows_checked": parity["rows"],
                "input_name": parity["input_name"],
                "output_names": "|".join(parity["output_names"]),
            }
        )
        reasons = np.full(len(full), f"model_argmax_{spec.model_id}(모델 최대 확률)", dtype=object)
        first_steps = np.zeros(len(full), dtype="int16")
        for split in ("train", "validation", "oos"):
            split_mask = full["split"].astype(str).eq(split).to_numpy()
            y_true = labels[split_mask]
            y_pred = pred_label[split_mask]
            class_rows.append(
                {
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
                f"model_surface_{spec.model_id}(모델 표면)",
                reasons,
                first_steps,
            )
            metric["model_id"] = spec.model_id
            metric["threshold_policy"] = spec.threshold_policy
            model_rows.append(metric)
            proxy_split = proxy_metrics[split]
            density_retention = safe_ratio(metric["trades_per_day"], proxy_split["trades_per_day"])
            pf_retention = safe_ratio(metric["profit_factor"], proxy_split["profit_factor"])
            retention_rows.append(
                {
                    "model_id": spec.model_id,
                    "split": split,
                    "model_trades_per_day": metric["trades_per_day"],
                    "proxy_trades_per_day": proxy_split["trades_per_day"],
                    "density_retention": density_retention,
                    "model_profit_factor": metric["profit_factor"],
                    "proxy_profit_factor": proxy_split["profit_factor"],
                    "pf_retention": pf_retention,
                    "model_dd_risk_percent": metric["dd_risk_percent"],
                    "proxy_dd_risk_percent": proxy_split["dd_risk_percent"],
                    "dd_delta_percent": metric["dd_risk_percent"] - proxy_split["dd_risk_percent"],
                    "partial_transfer_pass": bool(
                        split in {"validation", "oos"}
                        and density_retention >= 0.50
                        and metric["profit_factor"] > 1.0
                        and metric["dd_risk_percent"] <= proxy_split["dd_risk_percent"] + 10.0
                    ),
                }
            )
    return {
        "model_metrics": model_rows,
        "classification_metrics": class_rows,
        "parity": parity_rows,
        "retention": retention_rows,
        "label_distribution": label_distribution(full, labels),
    }


def build_final(
    result: dict[str, Any],
    proxy_metrics: dict[str, Any],
    integrity: dict[str, Any],
    feature_order: list[str],
) -> dict[str, Any]:
    retention = pd.DataFrame(result["retention"])
    model_metrics = pd.DataFrame(result["model_metrics"])
    parity = pd.DataFrame(result["parity"])
    grouped: list[dict[str, Any]] = []
    for model_id, group in retention.groupby("model_id", sort=False):
        val = group.loc[group["split"].eq("validation")].iloc[0]
        oos = group.loc[group["split"].eq("oos")].iloc[0]
        mm_val = model_metrics.loc[model_metrics["model_id"].eq(model_id) & model_metrics["split"].eq("validation")].iloc[0]
        mm_oos = model_metrics.loc[model_metrics["model_id"].eq(model_id) & model_metrics["split"].eq("oos")].iloc[0]
        parity_row = parity.loc[parity["model_id"].eq(model_id)].iloc[0]
        partial = bool(val["partial_transfer_pass"] and oos["partial_transfer_pass"] and parity_row["parity_passed"])
        grouped.append(
            {
                "model_id": model_id,
                "partial_transfer_pass": partial,
                "validation_density_retention": float(val["density_retention"]),
                "oos_density_retention": float(oos["density_retention"]),
                "validation_profit_factor": float(mm_val["profit_factor"]),
                "oos_profit_factor": float(mm_oos["profit_factor"]),
                "validation_trades_per_day": float(mm_val["trades_per_day"]),
                "oos_trades_per_day": float(mm_oos["trades_per_day"]),
                "validation_dd_risk_percent": float(mm_val["dd_risk_percent"]),
                "oos_dd_risk_percent": float(mm_oos["dd_risk_percent"]),
                "validation_dd_delta_percent": float(val["dd_delta_percent"]),
                "oos_dd_delta_percent": float(oos["dd_delta_percent"]),
                "parity_passed": bool(parity_row["parity_passed"]),
                "score": float(val["density_retention"] + oos["density_retention"] + min(mm_val["profit_factor"], 5.0) / 5.0 + min(mm_oos["profit_factor"], 5.0) / 5.0),
            }
        )
    score = pd.DataFrame(grouped).sort_values(["partial_transfer_pass", "score"], ascending=[False, False])
    best = dict(score.iloc[0]) if len(score) else {}
    partial_rows = int(score["partial_transfer_pass"].sum()) if len(score) else 0
    if partial_rows:
        status = "partial_trainable_transfer_clue_no_authority"
        judgment = "trainable_transfer_probe_result(학습 가능 전달 탐침 결과)"
        next_run = NEXT_PARTIAL_RUN_ID
    else:
        status = "oracle_to_model_transfer_collapse_no_authority"
        judgment = "negative_memory_candidate(부정 기억 후보)"
        next_run = NEXT_COLLAPSE_RUN_ID
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
        "model_count": len(MODEL_SPECS),
        "partial_transfer_rows": partial_rows,
        "best_model_id": str(best.get("model_id", "none")),
        "best_model_row": json_ready(best),
        "model_validation": {
            "model_family": "sklearn LogisticRegression plus small RandomForest(사이킷런 로지스틱 회귀와 작은 랜덤포레스트)",
            "target_and_label": "predict path label class short/flat/long from locked Frontier04B event label(전선04B 고정 이벤트 라벨의 숏/플랫/롱 예측)",
            "split_method": "fixed train/validation/OOS split(고정 학습/검증/표본밖 분할)",
            "selection_metric": "partial transfer pass then retention score(부분 전달 통과 후 유지율 점수)",
            "threshold_policy": "argmax only, no searched threshold(최대 확률 전용, 탐색 임계값 없음)",
            "overfit_risk": "single seed surface and train-only model fitting; no WFO(단일 씨앗 표면과 학습 분할 적합, WFO 없음)",
            "calibration_risk": "probabilities are classifier scores, not economic probabilities(확률은 분류 점수이지 경제 확률 아님)",
            "comparison_baseline": "Frontier04B oracle proxy metrics(전선04B 오라클 프록시 지표)",
            "validation_judgment": "exploratory(탐색)",
        },
        "runtime_parity": {
            "research_path": "stage_pipelines/stage_frontier_04/frontier04d_trainable_path_label_onnx_probe.py",
            "runtime_path": "not_applicable_no_mt5_handoff(해당 없음, MT5 인계 없음)",
            "shared_contract": "feature_set_v2 order, label order [short, flat, long], ONNX probability tensor(피처 순서, 라벨 순서, 온엑스 확률 텐서)",
            "known_differences": "no EA, no Strategy Tester, no live-like handoff(EA/전략 테스터/실거래 유사 인계 없음)",
            "parity_check": "onnxruntime probability parity against sklearn(사이킷런 대비 온엑스런타임 확률 동등성)",
            "runtime_claim_boundary": "research_only(연구 전용)",
        },
        "data_integrity": integrity,
        "feature_order_hash": ordered_hash(feature_order),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_artifacts(
    full: pd.DataFrame,
    feature_order: list[str],
    labels: np.ndarray,
    result: dict[str, Any],
    final: dict[str, Any],
    integrity: dict[str, Any],
) -> dict[str, Path]:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    paths = {
        "model_metrics": RUN_ROOT / "model_metrics.csv",
        "classification_metrics": RUN_ROOT / "classification.csv",
        "retention": RUN_ROOT / "retention.csv",
        "parity": RUN_ROOT / "onnx_parity.csv",
        "label_distribution": RUN_ROOT / "label_distribution.csv",
        "locked_label_manifest": RUN_ROOT / "label_manifest.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
    }
    pd.DataFrame(result["model_metrics"]).to_csv(io_path(paths["model_metrics"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["classification_metrics"]).to_csv(io_path(paths["classification_metrics"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["retention"]).to_csv(io_path(paths["retention"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["parity"]).to_csv(io_path(paths["parity"]), index=False, encoding="utf-8-sig")
    pd.DataFrame(result["label_distribution"]).to_csv(io_path(paths["label_distribution"]), index=False, encoding="utf-8-sig")
    write_json(paths["locked_label_manifest"], {
        "locked_variant_id": LOCKED_VARIANT_ID,
        "label_order": LABEL_ORDER,
        "label_names": LABEL_NAMES,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "model_input_dataset": f03b.DATASET_PATH.as_posix(),
        "model_input_dataset_sha256": sha256_file(f03b.DATASET_PATH),
        "feature_order": f03b.FEATURE_ORDER_PATH.as_posix(),
        "feature_order_sha256": sha256_file(f03b.FEATURE_ORDER_PATH),
        "feature_order_hash": ordered_hash(feature_order),
        "f04b_integrity": integrity,
        "rows": int(len(full)),
        "label_counts": {LABEL_NAMES[key]: int((labels == key).sum()) for key in LABEL_ORDER},
    })
    manifest = {
        **final,
        "script_path": "stage_pipelines/stage_frontier_04/frontier04d_trainable_path_label_onnx_probe.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_04/frontier04d_trainable_path_label_onnx_probe.py")),
        "outputs": {
            key: {"path": path.as_posix(), "sha256": sha256_file(path)}
            for key, path in paths.items()
            if key != "run_manifest"
        },
        "models": [
            {
                "model_id": spec.model_id,
                "onnx_path": (MODEL_DIR / f"{spec.model_id}.onnx").as_posix(),
                "onnx_sha256": sha256_file(MODEL_DIR / f"{spec.model_id}.onnx"),
                "joblib_path": (MODEL_DIR / f"{spec.model_id}.joblib").as_posix(),
                "joblib_sha256": sha256_file(MODEL_DIR / f"{spec.model_id}.joblib"),
            }
            for spec in MODEL_SPECS
        ],
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }
    write_json(paths["run_manifest"], manifest)
    return paths


def write_report(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    best = final["best_model_row"]
    text = f"""# Frontier04D Trainable Path Label ONNX Probe(전선04D 학습 가능 경로 라벨 온엑스 탐침)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): locked variant(고정 변형) `{LOCKED_VARIANT_ID}` 하나만 라벨로 쓰고, LogisticRegression(로지스틱 회귀) 2개 설정과 small RandomForest(작은 랜덤포레스트) 1개 설정을 train/validation/OOS(학습/검증/표본밖) 고정 분할에서 학습했습니다.

Effect(효과): Frontier04B(전선04B)의 oracle proxy(오라클 프록시)가 feature_set_v2(피처 세트 v2)로 얼마나 전달되는지 density/PF/DD retention(밀도/수익 팩터/손실폭 유지율)로 확인했습니다.

## Best Model Read(최상위 모델 판독)

- model(모델): `{final['best_model_id']}`
- partial_transfer_pass(부분 전달 통과): `{best.get('partial_transfer_pass')}`
- validation density/PF/DD(검증 밀도/수익 팩터/손실폭): `{fmt(best.get('validation_trades_per_day'))}/day` / `{fmt(best.get('validation_profit_factor'))}` / `{fmt(best.get('validation_dd_risk_percent'))}%`
- OOS density/PF/DD(표본밖 밀도/수익 팩터/손실폭): `{fmt(best.get('oos_trades_per_day'))}/day` / `{fmt(best.get('oos_profit_factor'))}` / `{fmt(best.get('oos_dd_risk_percent'))}%`
- validation/OOS density retention(검증/표본밖 밀도 유지율): `{fmt(best.get('validation_density_retention'))}` / `{fmt(best.get('oos_density_retention'))}`
- ONNX parity(온엑스 동등성): `{best.get('parity_passed')}`

## Required Boundaries(필수 경계)

- model_validation(모델 검증): `{final['model_validation']['validation_judgment']}`
- runtime_claim_boundary(런타임 주장 경계): `{final['runtime_parity']['runtime_claim_boundary']}`
- no WFO/MT5(WFO/MT5 없음): satisfied(충족)
- threshold_policy(임계값 정책): `{final['model_validation']['threshold_policy']}`

## Artifacts(산출물)

- retention(유지율): `{artifacts['retention'].as_posix()}`
- model metrics(모델 지표): `{artifacts['model_metrics'].as_posix()}`
- ONNX parity(온엑스 동등성): `{artifacts['parity'].as_posix()}`
- label manifest(라벨 목록): `{artifacts['locked_label_manifest'].as_posix()}`

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 이 탐침 결과를 repair/second probe/closeout(수리/2차 탐침/마감) 결정으로 넘기는 것입니다. Effect(효과)는 모델 전달이 약하면 broad sweep(넓은 반복 탐색)으로 도망가지 않고 stage lifecycle(단계 생명주기)을 정직하게 좁히는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""
    write_text_sig(REPORT_PATH, text)


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    import yaml

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
        "updated_at_utc": final["created_at_utc"],
    }
    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8")
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(final))
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final, artifacts))
    row = ledger_row(final)
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): next run(다음 실행)은 `{final['next_run_id']}`입니다.\n",
    )


def current_state_text(final: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier04D(전선04D)는 locked path label(고정 경로 라벨)의 trainable ONNX probe(학습 가능 온엑스 탐침)를 완료했습니다.

Judgment(판정): `{final['judgment']}`

Best read(최상위 판독): `{final['best_model_id']}` with partial_transfer_rows(부분 전달 행) `{final['partial_transfer_rows']}`.

Next action(다음 행동): `{final['next_run_id']}`. Action(행동)은 repair/second probe/closeout decision(수리/2차 탐침/마감 결정)을 여는 것입니다. Effect(효과)는 oracle-to-model transfer(오라클→모델 전달) 결과를 과장하지 않고 다음 경계를 정하는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    best = final["best_model_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "trainable_onnx_probe(학습 가능 온엑스 탐침)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"partial_transfer_rows={final['partial_transfer_rows']};best={final['best_model_id']};no_authority",
        "work_family": "model_validation(모델 검증)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": str(final["partial_transfer_rows"]),
        "claim_boundary": "trainable_probe_no_wfo_no_mt5_no_runtime_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__trainable_probe",
        "subrun_id": f"{RUN_ID}__trainable_probe",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "trainable_transfer_probe_no_runtime(학습 가능 전달 탐침, 런타임 아님)",
        "primary_kpi": (
            f"best={final['best_model_id']};partial={best.get('partial_transfer_pass')};"
            f"val_pf={fmt(best.get('validation_profit_factor'))};oos_pf={fmt(best.get('oos_profit_factor'))};"
            f"oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk_percent'))}"
        ),
        "guardrail_kpi": "onnx_parity_only_no_wfo_no_mt5_no_authority(온엑스 동등성만, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "source_run_id": SOURCE_PROXY_RUN_ID,
        "artifact_path": artifacts["run_manifest"].as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "python_trainable_probe_only(파이썬 학습 가능 탐침 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Can the locked path label transfer into a trainable ONNX model?(고정 경로 라벨이 학습 가능 온엑스 모델로 전달되는가?)",
        "skill_family": "model_validation(모델 검증)",
        "lineage_summary": "frontier04b_oracle_proxy_to_frontier04d_onnx_probe(전선04B 오라클 프록시에서 전선04D 온엑스 탐침)",
    }


def ledger_row(final: dict[str, Any]) -> dict[str, Any]:
    best = final["best_model_row"]
    return {
        "ledger_row_id": f"{RUN_ID}__trainable_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__trainable_probe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "trainable_transfer_probe_no_runtime(학습 가능 전달 탐침, 런타임 아님)",
        "scoreboard_lane": "trainable_onnx_probe(학습 가능 온엑스 탐침)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": (
            f"best={final['best_model_id']};partial={best.get('partial_transfer_pass')};"
            f"val_pf={fmt(best.get('validation_profit_factor'))};val_density={fmt(best.get('validation_trades_per_day'))};"
            f"val_dd={fmt(best.get('validation_dd_risk_percent'))};oos_pf={fmt(best.get('oos_profit_factor'))};"
            f"oos_density={fmt(best.get('oos_trades_per_day'))};oos_dd={fmt(best.get('oos_dd_risk_percent'))}"
        ),
        "guardrail_kpi": "onnx_parity_only_no_wfo_no_mt5_no_authority(온엑스 동등성만, WFO/MT5/권위 없음)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖, MT5 없음)",
        "notes": f"partial_transfer_rows={final['partial_transfer_rows']};next={final['next_run_id']};no_authority",
    }


def read_feature_order() -> list[str]:
    features = [line.strip() for line in io_path(f03b.FEATURE_ORDER_PATH).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if ordered_hash(features) != f03b.EXPECTED_FEATURE_HASH:
        raise RuntimeError("Feature order hash mismatch.")
    return features


def read_proxy_metrics() -> dict[str, Any]:
    with io_path(F04B_TOP).open("r", encoding="utf-8-sig", newline="") as handle:
        row = next(csv.DictReader(handle))
    if row["variant_id"] != LOCKED_VARIANT_ID:
        raise RuntimeError(f"Top row is not locked variant: {row['variant_id']}")
    out: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        out[split] = {
            "trades_per_day": float(row[f"{split}_trades_per_day"]),
            "profit_factor": float(row[f"{split}_profit_factor"]),
            "dd_risk_percent": float(row[f"{split}_dd_risk_percent"]),
            "trade_count": int(float(row[f"{split}_trade_count"])),
        }
    return out


def label_distribution(full: pd.DataFrame, labels: np.ndarray) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        mask = full["split"].astype(str).eq(split).to_numpy()
        for label in LABEL_ORDER:
            rows.append(
                {
                    "split": split,
                    "label": label,
                    "label_name": LABEL_NAMES[label],
                    "count": int((labels[mask] == label).sum()),
                    "fraction": float((labels[mask] == label).mean()),
                }
            )
    return rows


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def safe_ratio(value: Any, base: Any) -> float:
    denominator = float(base)
    if not math.isfinite(denominator) or denominator <= 0:
        return 0.0
    number = float(value)
    if not math.isfinite(number):
        return 0.0
    return number / denominator


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
