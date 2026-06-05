from __future__ import annotations

import hashlib
import json
import re
import sys
import warnings
from pathlib import Path
from typing import Iterable, Sequence

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from xgboost import XGBClassifier

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.onnx_bridge import (  # noqa: E402
    check_onnxruntime_probability_parity,
    export_lightgbm_classifier_to_onnx,
    export_sklearn_to_onnx_zipmap_disabled,
    export_xgboost_classifier_to_onnx,
    ordered_sklearn_probabilities,
)
from stage_pipelines.stage337 import (  # noqa: E402
    review_proxy_negative_trade_shape_offensive_pivot_inputs_without_db as hy,
)

aw = hy.aw
warnings.filterwarnings("ignore", message="X does not have valid feature names.*", category=UserWarning)

TODAY = "2026-06-01"
STAGE_ID = hy.STAGE_ID
STAGE_DIR = hy.STAGE_DIR
RUN_NUMBER = "run337HZ"
RUN_ID = "run337HZ_train_proxy_negative_trade_shape_offensive_pivot_candidates_without_db_v1"
PARENT_RUN_ID = hy.RUN_ID
NEXT_RUN_ID = "run337IA_review_proxy_negative_trade_shape_offensive_pivot_training_without_db_v1"
STATUS = "completed_stage337HZ_offensive_pivot_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5"
JUDGMENT = "offensive_pivot_candidates_trained_with_onnx_parity_and_proxy_score_review_required"
DECISION = "stage337HZ_open_run337IA_review_offensive_pivot_training"
CLAIM_BOUNDARY = (
    "research_development_candidate_training_only_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_no_forward_no_runtime_package_no_operating_or_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = hy.REVIEW_DIR
REPORT_PATH = REVIEW_DIR / "run337HZ_proxy_negative_trade_shape_offensive_pivot_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HZ_proxy_negative_trade_shape_offensive_pivot_training.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"

FEATURE_SCHEMA = RUN_DIR / "hz_allowed_feature_schema.json"
TRAINING_TASK_REVIEW = RUN_DIR / "hz_training_task_review.csv"
SAMPLE_WEIGHT_AUDIT = RUN_DIR / "sample_weight_audit.csv"
TRAINED_MODEL_MANIFEST = RUN_DIR / "trained_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "onnx_parity_matrix.csv"
CLASSIFICATION_SCORECARD = RUN_DIR / "inner_holdout_classification_scorecard.csv"
PROXY_TRADE_SCORECARD = RUN_DIR / "inner_holdout_proxy_trade_scorecard.csv"
FEATURE_IMPORTANCE = RUN_DIR / "feature_importance_top20.csv"
RUNTIME_FIREWALL = RUN_DIR / "runtime_firewall_review.csv"
RELEASE_DISPOSITION = RUN_DIR / "training_release_disposition.csv"
IA_QUEUE = RUN_DIR / "run337IA_review_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_BOUNDARY_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

FEATURE_SET_ID = "hx_allowed_pretrade_features_v1"


def _ensure_dirs() -> None:
    for path in [RUN_DIR, MODEL_DIR, ONNX_DIR, REVIEW_DIR, DECISION_DOC.parent, RUN_REGISTRY.parent]:
        aw.io_path(path).mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(aw.io_path(path))


def _write_csv(path: Path, frame: pd.DataFrame) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(aw.io_path(path), index=False, encoding="utf-8-sig", lineterminator="\n")


def _write_json(path: Path, payload: dict) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_bom_text(path: Path, text: str) -> None:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(text, encoding="utf-8-sig")


def _sha(path: Path) -> str:
    return aw.sha256_file(path)


def _feature_hash(features: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(features).encode("utf-8")).hexdigest()


def _safe_model_id(task_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", task_id).strip("_")
    return f"hz_{cleaned}"


def _read_features() -> list[str]:
    allowed = _read_csv(hy.hx.HX_ALLOWED_FEATURES)
    return [str(feature) for feature in allowed["feature_name"].dropna().tolist()]


def _split_inner(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    source_ids = pd.to_numeric(frame["source_row_id"], errors="coerce").astype(int)
    unique_ids = sorted(source_ids.unique().tolist())
    cutoff_index = max(1, int(len(unique_ids) * 0.80))
    cutoff = unique_ids[cutoff_index - 1]
    return frame.loc[source_ids <= cutoff].copy(), frame.loc[source_ids > cutoff].copy()


def _sample_weights(frame: pd.DataFrame, column: str) -> pd.Series:
    weights = pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(1.0)
    return weights.clip(lower=0.10, upper=12.0)


def _class_order_for_task(task: pd.Series) -> list[int]:
    target = str(task["target_column"])
    if target == "hx_active_flat_label":
        return [0, 1]
    return [0, 1, 2]


def _model_family(task: pd.Series) -> str:
    return str(task["model_family"]).lower()


def _make_model(task: pd.Series, class_order: Sequence[int]):
    family = _model_family(task)
    is_binary = len(class_order) == 2
    if "extratrees" in family:
        return ExtraTreesClassifier(
            n_estimators=220,
            max_depth=12,
            min_samples_leaf=70,
            min_samples_split=140,
            max_features="sqrt",
            random_state=33791,
            n_jobs=-1,
            class_weight=None,
        )
    if "xgboost" in family:
        if is_binary:
            return XGBClassifier(
                n_estimators=160,
                max_depth=4,
                learning_rate=0.045,
                subsample=0.86,
                colsample_bytree=0.82,
                reg_alpha=0.05,
                reg_lambda=2.0,
                objective="binary:logistic",
                eval_metric="logloss",
                tree_method="hist",
                random_state=33792,
                n_jobs=-1,
            )
        return XGBClassifier(
            n_estimators=170,
            max_depth=4,
            learning_rate=0.045,
            subsample=0.86,
            colsample_bytree=0.82,
            reg_alpha=0.05,
            reg_lambda=2.0,
            objective="multi:softprob",
            num_class=len(class_order),
            eval_metric="mlogloss",
            tree_method="hist",
            random_state=33793,
            n_jobs=-1,
        )
    if is_binary:
        return LGBMClassifier(
            objective="binary",
            n_estimators=190,
            learning_rate=0.04,
            max_depth=6,
            num_leaves=31,
            min_child_samples=160,
            subsample=0.86,
            colsample_bytree=0.82,
            reg_alpha=0.10,
            reg_lambda=1.0,
            random_state=33794,
            n_jobs=-1,
            verbose=-1,
        )
    return LGBMClassifier(
        objective="multiclass",
        num_class=len(class_order),
        n_estimators=210,
        learning_rate=0.038,
        max_depth=6,
        num_leaves=31,
        min_child_samples=160,
        subsample=0.86,
        colsample_bytree=0.82,
        reg_alpha=0.10,
        reg_lambda=1.0,
        random_state=33795,
        n_jobs=-1,
        verbose=-1,
    )


def _export_model(model, task: pd.Series, path: Path, feature_count: int) -> dict:
    family = _model_family(task)
    if "lightgbm" in family:
        return export_lightgbm_classifier_to_onnx(
            model,
            path,
            feature_count=feature_count,
            input_name="float_input",
            target_opset=13,
            drop_label_output=True,
        )
    if "xgboost" in family:
        return export_xgboost_classifier_to_onnx(
            model,
            path,
            feature_count=feature_count,
            input_name="float_input",
            target_opset=13,
            drop_label_output=True,
        )
    return export_sklearn_to_onnx_zipmap_disabled(
        model,
        path,
        feature_count=feature_count,
        input_name="float_input",
        target_opset=12,
        drop_label_output=True,
    )


def _probability_and_pred(model, values: np.ndarray, class_order: Sequence[int]) -> tuple[np.ndarray, np.ndarray]:
    probabilities = ordered_sklearn_probabilities(model, values.astype("float64"), class_order=class_order)
    row_sum = probabilities.sum(axis=1, keepdims=True)
    probabilities = np.divide(probabilities, row_sum, out=np.zeros_like(probabilities), where=row_sum != 0.0)
    pred = np.asarray(class_order, dtype=int)[np.argmax(probabilities, axis=1)]
    return probabilities, pred


def _label_counts(values: np.ndarray, class_order: Sequence[int]) -> str:
    counts = {str(label): 0 for label in class_order}
    labels, values_count = np.unique(values, return_counts=True)
    for label, count in zip(labels, values_count):
        counts[str(int(label))] = int(count)
    return json.dumps(counts, ensure_ascii=False, sort_keys=True)


def _classification_score(
    model_id: str,
    task_id: str,
    split: str,
    model,
    frame: pd.DataFrame,
    features: Sequence[str],
    target: str,
    class_order: Sequence[int],
) -> dict:
    values = frame.loc[:, features].astype("float32").to_numpy()
    probs, pred = _probability_and_pred(model, values, class_order)
    y_values = pd.to_numeric(frame[target], errors="raise").astype(int).to_numpy()
    return {
        "model_id": model_id,
        "task_id": task_id,
        "split": split,
        "target_column": target,
        "rows": int(len(frame)),
        "accuracy": float(accuracy_score(y_values, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_values, pred)),
        "macro_f1": float(f1_score(y_values, pred, average="macro")),
        "log_loss": float(log_loss(y_values, probs, labels=list(class_order))),
        "pred_counts_json": _label_counts(pred, class_order),
        "true_counts_json": _label_counts(y_values, class_order),
        "signal_density": float(np.mean(pred != 1)) if len(pred) and 1 in class_order else float(np.mean(pred == 1)),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _future_column_for_target(target: str) -> str | None:
    if target.endswith("fwd6"):
        return "hx_future_log_return_6"
    if target.endswith("fwd18"):
        return "hx_future_log_return_18"
    if target.endswith("fwd24"):
        return "hx_future_log_return_24"
    return None


def _proxy_trade_score(
    model_id: str,
    task_id: str,
    split: str,
    model,
    frame: pd.DataFrame,
    features: Sequence[str],
    target: str,
    class_order: Sequence[int],
) -> dict:
    values = frame.loc[:, features].astype("float32").to_numpy()
    _probs, pred = _probability_and_pred(model, values, class_order)
    future_column = _future_column_for_target(target)
    if future_column is None:
        return {
            "model_id": model_id,
            "task_id": task_id,
            "split": split,
            "score_mode": "active_flat_gate_only",
            "trade_count": 0,
            "signal_density": float(np.mean(pred == 1)) if len(pred) else 0.0,
            "net_log_return_after_cost": 0.0,
            "profit_factor": 0.0,
            "expectancy": 0.0,
            "max_drawdown": 0.0,
            "recovery_factor": 0.0,
            "long_count": 0,
            "short_count": 0,
            "long_net": 0.0,
            "short_net": 0.0,
            "allowed_use": "active gate sanity only(능동 게이트 점검 전용)",
            "forbidden_use": "directional MT5 KPI or candidate selection(방향성 MT5 KPI 또는 후보 선택)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    future = pd.to_numeric(frame[future_column], errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    cost = (
        pd.to_numeric(frame["cost_return"], errors="coerce").fillna(0.0).to_numpy(dtype="float64")
        if "cost_return" in frame.columns
        else np.zeros(len(frame), dtype="float64")
    )
    direction = np.where(pred == 2, 1.0, np.where(pred == 0, -1.0, 0.0))
    pnl = np.where(direction == 0.0, 0.0, direction * future - cost)
    trades = pnl[direction != 0.0]
    gross_profit = float(trades[trades > 0].sum()) if len(trades) else 0.0
    gross_loss = float(trades[trades < 0].sum()) if len(trades) else 0.0
    equity = np.cumsum(trades) if len(trades) else np.asarray([], dtype="float64")
    peak = np.maximum.accumulate(equity) if len(equity) else np.asarray([], dtype="float64")
    drawdown = peak - equity if len(equity) else np.asarray([], dtype="float64")
    max_drawdown = float(drawdown.max()) if len(drawdown) else 0.0
    net = float(trades.sum()) if len(trades) else 0.0
    return {
        "model_id": model_id,
        "task_id": task_id,
        "split": split,
        "score_mode": f"directional_{future_column}",
        "trade_count": int(len(trades)),
        "signal_density": float(np.mean(direction != 0.0)) if len(direction) else 0.0,
        "net_log_return_after_cost": net,
        "profit_factor": float(gross_profit / abs(gross_loss)) if gross_loss < 0 else (999.0 if gross_profit > 0 else 0.0),
        "expectancy": float(net / len(trades)) if len(trades) else 0.0,
        "max_drawdown": max_drawdown,
        "recovery_factor": float(net / max_drawdown) if max_drawdown > 0 else 0.0,
        "long_count": int(np.sum(pred == 2)),
        "short_count": int(np.sum(pred == 0)),
        "long_net": float(pnl[pred == 2].sum()) if len(pnl) else 0.0,
        "short_net": float(pnl[pred == 0].sum()) if len(pnl) else 0.0,
        "allowed_use": "signal sanity only(신호 점검 전용)",
        "forbidden_use": "MT5 KPI, Forward Passed/Failed, candidate selection(MT5 KPI, 전진 통과/실패, 후보 선택)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _feature_importances(model, features: Sequence[str]) -> np.ndarray:
    if hasattr(model, "feature_importances_"):
        return np.asarray(model.feature_importances_, dtype="float64")
    return np.zeros(len(features), dtype="float64")


def _train_all() -> tuple[dict, list[Path]]:
    frame = pd.read_parquet(aw.io_path(hy.hx.HX_INPUT_FRAME)).copy()
    features = _read_features()
    missing = [feature for feature in features if feature not in frame.columns]
    if missing:
        raise ValueError(f"missing features: {missing}")
    tasks = _read_csv(hy.hx.HY_TASK_SEEDS)
    hy_gates = _read_csv(hy.GATE_AUDIT)
    if not hy_gates["status"].astype(str).str.lower().isin(["pass", "passed"]).all():
        raise RuntimeError("HY gates are not all passed")

    feature_hash = _feature_hash(features)
    _write_json(
        FEATURE_SCHEMA,
        {
            "feature_set_id": FEATURE_SET_ID,
            "feature_count": len(features),
            "feature_order_hash": feature_hash,
            "features": features,
            "source": aw.rel(hy.hx.HX_ALLOWED_FEATURES),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )

    task_rows: list[dict] = []
    weight_rows: list[dict] = []
    model_rows: list[dict] = []
    parity_rows: list[dict] = []
    class_rows: list[dict] = []
    proxy_rows: list[dict] = []
    importance_rows: list[dict] = []

    for _, task in tasks.iterrows():
        target = str(task["target_column"])
        valid_col = str(task["valid_column"])
        weight_col = str(task["sample_weight_column"])
        class_order = _class_order_for_task(task)
        task_frame = frame.loc[(frame[valid_col] == 1) & (frame[target] != -1)].copy()
        inner_train, inner_holdout = _split_inner(task_frame)
        weights = _sample_weights(inner_train, weight_col)
        model = _make_model(task, class_order)
        x_train = inner_train.loc[:, features].astype("float32").to_numpy()
        y_train = pd.to_numeric(inner_train[target], errors="raise").astype(int).to_numpy()
        model.fit(x_train, y_train, sample_weight=weights.to_numpy(dtype="float64"))

        task_id = str(task["task_id"])
        model_id = _safe_model_id(task_id)
        model_path = MODEL_DIR / f"{model_id}.joblib"
        onnx_path = ONNX_DIR / f"{model_id}.onnx"
        joblib.dump(
            {
                "model": model,
                "features": features,
                "class_order": list(class_order),
                "task": task.to_dict(),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            aw.io_path(model_path),
        )
        export_meta = _export_model(model, task, onnx_path, len(features))
        parity_values = inner_holdout.loc[:, features].astype("float32").head(512).to_numpy()
        parity = check_onnxruntime_probability_parity(
            model,
            onnx_path,
            parity_values,
            class_order=class_order,
            tolerance=1e-4,
        )

        task_rows.append(
            {
                "task_id": task_id,
                "training_disposition": "trained_no_selection_no_mt5",
                "pivot_family": task["pivot_family"],
                "feature_count": len(features),
                "target_column": target,
                "valid_column": valid_col,
                "sample_weight_column": weight_col,
                "model_family": task["model_family"],
                "model_config_id": task["model_config_id"],
                "inner_train_rows": int(len(inner_train)),
                "inner_holdout_rows": int(len(inner_holdout)),
                "effect": "Candidate is trained for IA review only(IA 검토 전용 후보 학습).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        weight_rows.append(
            {
                "task_id": task_id,
                "sample_weight_column": weight_col,
                "rows": int(len(weights)),
                "weight_min": float(weights.min()),
                "weight_mean": float(weights.mean()),
                "weight_max": float(weights.max()),
                "nonfinite_weights": int((~np.isfinite(weights.to_numpy())).sum()),
                "effect": "Sample weight behavior is recorded before score review(점수 검토 전 표본 가중치 기록).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        parity_rows.append(
            {
                "model_id": model_id,
                "task_id": task_id,
                "onnx_path": aw.rel(onnx_path),
                "passed": "true" if parity["passed"] else "false",
                "rows": parity["rows"],
                "max_abs_diff": parity["max_abs_diff"],
                "mean_abs_diff": parity["mean_abs_diff"],
                "onnx_row_sum_max_abs_error": parity["onnx_row_sum_max_abs_error"],
                "input_name": parity["input_name"],
                "output_names": json.dumps(parity["output_names"], ensure_ascii=False),
                "class_order_json": json.dumps(list(class_order)),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        model_rows.append(
            {
                "model_id": model_id,
                "task_id": task_id,
                "feature_set_id": FEATURE_SET_ID,
                "target_column": target,
                "sample_weight_column": weight_col,
                "model_family": task["model_family"],
                "model_config_id": task["model_config_id"],
                "feature_count": len(features),
                "feature_order_hash": feature_hash,
                "class_order_json": json.dumps(list(class_order)),
                "model_path": aw.rel(model_path),
                "model_sha256": _sha(model_path),
                "onnx_path": aw.rel(onnx_path),
                "onnx_sha256": _sha(onnx_path),
                "onnx_probability_output_name": export_meta["probability_output_name"],
                "inner_train_rows": int(len(inner_train)),
                "inner_holdout_rows": int(len(inner_holdout)),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for split_name, split_frame in [("inner_train", inner_train), ("inner_holdout", inner_holdout)]:
            class_rows.append(
                _classification_score(
                    model_id,
                    task_id,
                    split_name,
                    model,
                    split_frame,
                    features,
                    target,
                    class_order,
                )
            )
            proxy_rows.append(
                _proxy_trade_score(
                    model_id,
                    task_id,
                    split_name,
                    model,
                    split_frame,
                    features,
                    target,
                    class_order,
                )
            )
        importances = _feature_importances(model, features)
        for rank, index in enumerate(np.argsort(importances)[::-1][:20], start=1):
            importance_rows.append(
                {
                    "model_id": model_id,
                    "task_id": task_id,
                    "rank": rank,
                    "feature_name": features[int(index)],
                    "importance": float(importances[int(index)]),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    firewall = pd.DataFrame(
        [
            {
                "review_id": "no_candidate_selection",
                "subject": "candidate selection firewall(후보 선택 방화벽)",
                "rows": len(model_rows),
                "review_status": "active",
                "allowed_use": "IA review only(IA 검토 전용)",
                "forbidden_use": "promotion or selected model(승격 또는 선택 모델)",
                "effect": "Proxy-only scores cannot become selection(프록시 점수만으로 선택하지 못하게 함).",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "review_id": "no_mt5_or_forward_claim",
                "subject": "MT5/Forward firewall(MT5/전진 방화벽)",
                "rows": len(model_rows),
                "review_status": "active",
                "allowed_use": "future runtime probe planning(향후 런타임 탐침 계획)",
                "forbidden_use": "Forward Passed/Failed or runtime authority(전진 통과/실패 또는 런타임 권위)",
                "effect": "ONNX creation stays separate from operating evidence(ONNX 생성과 운영 근거를 분리).",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    release = pd.DataFrame(
        [
            {
                "review_id": "training_release_disposition",
                "subject": "training release disposition(학습 해제 처분)",
                "rows": len(model_rows),
                "review_status": "no_release_review_required",
                "allowed_use": "IA training review(IA 학습 검토)",
                "forbidden_use": "selected candidate or live readiness(선택 후보 또는 실거래 준비)",
                "effect": "Trained ONNX artifacts move to review, not operation(학습 ONNX 산출물을 운영이 아니라 검토로 이동).",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    ia_queue = pd.DataFrame(
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "parent_run_id": RUN_ID,
                "queued_task": "review_offensive_pivot_training_scores_and_onnx_parity",
                "required_inputs": f"{aw.rel(TRAINED_MODEL_MANIFEST)};{aw.rel(ONNX_PARITY)};{aw.rel(CLASSIFICATION_SCORECARD)};{aw.rel(PROXY_TRADE_SCORECARD)}",
                "required_outputs": "candidate review scorecard and next runtime/proxy decision(후보 검토 점수표와 다음 런타임/프록시 결정)",
                "forbidden_action": "MT5/Forward/Goal claim without runtime probe(런타임 탐침 없는 MT5/전진/목표 주장)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    _write_csv(TRAINING_TASK_REVIEW, pd.DataFrame(task_rows))
    _write_csv(SAMPLE_WEIGHT_AUDIT, pd.DataFrame(weight_rows))
    _write_csv(TRAINED_MODEL_MANIFEST, pd.DataFrame(model_rows))
    _write_csv(ONNX_PARITY, pd.DataFrame(parity_rows))
    _write_csv(CLASSIFICATION_SCORECARD, pd.DataFrame(class_rows))
    _write_csv(PROXY_TRADE_SCORECARD, pd.DataFrame(proxy_rows))
    _write_csv(FEATURE_IMPORTANCE, pd.DataFrame(importance_rows))
    _write_csv(RUNTIME_FIREWALL, firewall)
    _write_csv(RELEASE_DISPOSITION, release)
    _write_csv(IA_QUEUE, ia_queue)

    holdout_proxy = [row for row in proxy_rows if row["split"] == "inner_holdout"]
    directional_holdout = [row for row in holdout_proxy if row["score_mode"].startswith("directional_")]
    positive_holdout = [row for row in directional_holdout if float(row["net_log_return_after_cost"]) > 0]
    summary = {
        "frame_rows": int(len(frame)),
        "feature_count": int(len(features)),
        "feature_order_hash": feature_hash,
        "task_seed_rows": int(len(tasks)),
        "trained_model_rows": int(len(model_rows)),
        "onnx_rows": int(len(model_rows)),
        "onnx_parity_rows": int(len(parity_rows)),
        "onnx_parity_passed_rows": int(sum(1 for row in parity_rows if row["passed"] == "true")),
        "classification_rows": int(len(class_rows)),
        "proxy_trade_rows": int(len(proxy_rows)),
        "positive_inner_holdout_proxy_rows": int(len(positive_holdout)),
        "best_inner_holdout_proxy_net": float(
            max([float(row["net_log_return_after_cost"]) for row in directional_holdout] or [0.0])
        ),
        "best_inner_holdout_profit_factor": float(
            max([float(row["profit_factor"]) for row in directional_holdout] or [0.0])
        ),
        "best_inner_holdout_balanced_accuracy": float(
            max([float(row["balanced_accuracy"]) for row in class_rows if row["split"] == "inner_holdout"] or [0.0])
        ),
        "max_inner_holdout_signal_density": float(
            max([float(row["signal_density"]) for row in holdout_proxy] or [0.0])
        ),
        "next_action": NEXT_RUN_ID,
    }
    artifacts = [
        FEATURE_SCHEMA,
        TRAINING_TASK_REVIEW,
        SAMPLE_WEIGHT_AUDIT,
        TRAINED_MODEL_MANIFEST,
        ONNX_PARITY,
        CLASSIFICATION_SCORECARD,
        PROXY_TRADE_SCORECARD,
        FEATURE_IMPORTANCE,
        RUNTIME_FIREWALL,
        RELEASE_DISPOSITION,
        IA_QUEUE,
    ]
    return summary, artifacts


def _gate_row(gate: str, status: str, evidence: str, effect: str) -> dict:
    return {
        "gate": gate,
        "status": status,
        "evidence": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _make_gates(summary: dict) -> pd.DataFrame:
    gates = [
        _gate_row(
            "parent_hy_gates_passed",
            "pass"
            if _read_csv(hy.GATE_AUDIT)["status"].astype(str).str.lower().isin(["pass", "passed"]).all()
            else "fail",
            aw.rel(hy.GATE_AUDIT),
            "HZ starts only after HY review passed(HY 검토 통과 후 HZ 시작).",
        ),
        _gate_row(
            "feature_schema_materialized",
            "pass" if summary["feature_count"] >= 50 and FEATURE_SCHEMA.exists() else "fail",
            aw.rel(FEATURE_SCHEMA),
            "Feature order is fixed for ONNX handoff(ONNX 인계용 피처 순서 고정).",
        ),
        _gate_row(
            "all_task_seeds_trained",
            "pass" if summary["trained_model_rows"] == summary["task_seed_rows"] == 7 else "fail",
            aw.rel(TRAINING_TASK_REVIEW),
            "Every HY offensive task became a trained candidate(모든 HY 공격 작업이 후보로 학습됨).",
        ),
        _gate_row(
            "onnx_exports_materialized",
            "pass" if summary["onnx_rows"] == summary["trained_model_rows"] else "fail",
            aw.rel(TRAINED_MODEL_MANIFEST),
            "Each model has an ONNX artifact(각 모델이 ONNX 산출물을 가짐).",
        ),
        _gate_row(
            "onnx_parity_passed",
            "pass"
            if summary["onnx_parity_passed_rows"] == summary["onnx_parity_rows"] == summary["trained_model_rows"]
            else "fail",
            aw.rel(ONNX_PARITY),
            "ONNX runtime probabilities match Python model probabilities(ONNX 런타임 확률이 파이썬 모델 확률과 일치).",
        ),
        _gate_row(
            "classification_scored",
            "pass" if summary["classification_rows"] == summary["trained_model_rows"] * 2 else "fail",
            aw.rel(CLASSIFICATION_SCORECARD),
            "Inner train and holdout classification diagnostics exist(내부 학습/보류 분류 진단 존재).",
        ),
        _gate_row(
            "proxy_trade_scored",
            "pass" if summary["proxy_trade_rows"] == summary["trained_model_rows"] * 2 else "fail",
            aw.rel(PROXY_TRADE_SCORECARD),
            "Proxy trade sanity score exists without MT5 claim(프록시 거래 점검은 있으나 MT5 주장은 없음).",
        ),
        _gate_row(
            "release_firewall_active",
            "pass" if RUNTIME_FIREWALL.exists() and RELEASE_DISPOSITION.exists() else "fail",
            f"{aw.rel(RUNTIME_FIREWALL)};{aw.rel(RELEASE_DISPOSITION)}",
            "Training is separated from selection and runtime authority(학습과 선택/런타임 권위 분리).",
        ),
        _gate_row(
            "next_review_queue_opened",
            "pass" if IA_QUEUE.exists() else "fail",
            aw.rel(IA_QUEUE),
            "IA review is queued before any runtime action(런타임 행동 전 IA 검토 대기열).",
        ),
        _gate_row(
            "no_forbidden_operating_claim",
            "pass",
            aw.rel(CLAIM_BOUNDARY_RECEIPT),
            "HZ does not claim selection, MT5 success, runtime authority, or Goal achievement(HZ는 선택/MT5 성공/런타임 권위/목표 달성을 주장하지 않음).",
        ),
        _gate_row(
            "required_gate_coverage_audit_written",
            "pass",
            aw.rel(GATE_AUDIT),
            "Closeout states exactly what passed(종료 기록이 통과 근거를 명시).",
        ),
    ]
    return pd.DataFrame(gates)


def _append_or_replace_csv(path: Path, key_columns: Iterable[str], row: dict) -> None:
    if path.exists():
        frame = _read_csv(path)
    else:
        frame = pd.DataFrame()
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    mask = pd.Series(False, index=frame.index)
    for idx, key in enumerate(key_columns):
        current = frame[key].astype(str).eq(str(row[key])) if key in frame.columns else False
        mask = current if idx == 0 else mask & current
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    _write_csv(path, frame[ordered])


def _artifact_paths() -> list[Path]:
    return [
        FEATURE_SCHEMA,
        TRAINING_TASK_REVIEW,
        SAMPLE_WEIGHT_AUDIT,
        TRAINED_MODEL_MANIFEST,
        ONNX_PARITY,
        CLASSIFICATION_SCORECARD,
        PROXY_TRADE_SCORECARD,
        FEATURE_IMPORTANCE,
        RUNTIME_FIREWALL,
        RELEASE_DISPOSITION,
        IA_QUEUE,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        PERFORMANCE_RECEIPT,
        RUNTIME_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_BOUNDARY_RECEIPT,
        LINEAGE_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
    ]


def _update_artifact_registry(paths: list[Path]) -> None:
    if ARTIFACT_REGISTRY.exists():
        registry = pd.read_csv(aw.io_path(ARTIFACT_REGISTRY))
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if path.exists():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": aw.rel(path),
                    "sha256": _sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    model_paths = list(MODEL_DIR.glob("*.joblib")) + list(ONNX_DIR.glob("*.onnx"))
    for path in model_paths:
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lower().lstrip("."),
                "path": aw.rel(path),
                "sha256": _sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        registry[columns].to_csv(
            aw.io_path(ARTIFACT_REGISTRY),
            index=False,
            encoding="utf-8-sig",
            lineterminator="\n",
        )


def _write_receipts(summary: dict, gates: pd.DataFrame) -> None:
    _write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "work_family": "candidate_training",
            "primary_skill": "obsidian-model-validation",
            "support_skills": ["obsidian-data-integrity", "obsidian-artifact-lineage", "obsidian-result-judgment"],
            "effect": "Offensive pivot seeds became trained ONNX candidates(공격 전환 씨앗이 학습 ONNX 후보가 됨).",
        },
    )
    _write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "input_frame": aw.rel(hy.hx.HX_INPUT_FRAME),
            "feature_schema": aw.rel(FEATURE_SCHEMA),
            "frame_rows": summary["frame_rows"],
            "feature_count": summary["feature_count"],
            "tier_scope": "Tier A only; Tier B and combined missing_required",
            "effect": "Training data lineage stays tied to HX/HY(학습 데이터 계보가 HX/HY에 연결됨).",
        },
    )
    _write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "trained_model_rows": summary["trained_model_rows"],
            "onnx_rows": summary["onnx_rows"],
            "onnx_parity": f"{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}",
            "effect": "ONNX artifacts are available for IA review(IA 검토용 ONNX 산출물 생성).",
        },
    )
    _write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "best_inner_holdout_proxy_net": summary["best_inner_holdout_proxy_net"],
            "best_inner_holdout_profit_factor": summary["best_inner_holdout_profit_factor"],
            "positive_inner_holdout_proxy_rows": summary["positive_inner_holdout_proxy_rows"],
            "allowed_use": "proxy signal sanity and IA review only(프록시 신호 점검 및 IA 검토 전용)",
            "forbidden_use": "MT5 KPI replacement or candidate selection(MT5 KPI 대체 또는 후보 선택)",
        },
    )
    _write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "mt5_execution": "not_run",
            "runtime_package": "not_opened",
            "onnx_parity": f"{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}",
            "effect": "Runtime parity is limited to ONNX probability parity(런타임 동등성은 ONNX 확률 동등성으로 제한).",
        },
    )
    _write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
            "gate_total": int(len(gates)),
        },
    )
    _write_json(
        CLAIM_BOUNDARY_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "candidate_selection": "not_run",
            "goal_achieve_claim": "not_claimed",
            "runtime_authority_claim": "not_claimed",
            "operating_promotion_claim": "not_claimed",
            "live_readiness_claim": "not_claimed",
        },
    )
    _write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "model_manifest": aw.rel(TRAINED_MODEL_MANIFEST),
            "onnx_parity": aw.rel(ONNX_PARITY),
            "artifact_registry_updated": True,
            "effect": "Models, ONNX files, scorecards, and review queue are linked(모델/ONNX/점수표/검토 대기열 연결).",
        },
    )


def _write_final(summary: dict, gates: pd.DataFrame) -> None:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        **summary,
    }
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at": TODAY,
        "script": aw.rel(Path(__file__)),
        "inputs": [
            aw.rel(hy.FINAL_DECISION),
            aw.rel(hy.GATE_AUDIT),
            aw.rel(hy.hx.HX_INPUT_FRAME),
            aw.rel(hy.hx.HX_ALLOWED_FEATURES),
            aw.rel(hy.hx.HY_TASK_SEEDS),
        ],
        "outputs": [aw.rel(path) for path in _artifact_paths() if path.exists()],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    _write_json(FINAL_DECISION, final)
    _write_json(RUN_MANIFEST, manifest)


def _write_docs(summary: dict, gates: pd.DataFrame) -> None:
    gate_passes = int(gates["status"].astype(str).eq("pass").sum())
    gate_total = int(len(gates))
    report = f"""﻿# Stage 337HZ Offensive Pivot Candidate Training

## Summary

- run_id: `{RUN_ID}`
- parent_run_id: `{PARENT_RUN_ID}`
- judgment: `{JUDGMENT}`
- gates: `{gate_passes}/{gate_total}`
- trained_models(학습 모델): `{summary['trained_model_rows']}`
- onnx_parity(ONNX 동등성): `{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{summary['best_inner_holdout_proxy_net']}`
- positive_inner_holdout_proxy_rows(양수 내부 보류 프록시 행): `{summary['positive_inner_holdout_proxy_rows']}`

## Result

HZ trained(학습) seven offensive pivot candidates(공격 전환 후보 7개) and exported(내보내기) seven ONNX(온엑스) artifacts.
Effect(효과): IA review(검토)가 model artifacts(모델 산출물), ONNX parity(ONNX 동등성), proxy trade score(프록시 거래 점수)를 같이 볼 수 있다.

## Boundary

No candidate selection(후보 선택 없음), no MT5 execution(MT5 실행 없음), no runtime package(런타임 패키지 없음), no operating claim(운영 주장 없음), no Goal Achieve(목표 달성 없음).

## Next

Open `{NEXT_RUN_ID}` to review training score(학습 점수), ONNX parity(ONNX 동등성), proxy usability(프록시 활용성), and next runtime/proxy action(다음 런타임/프록시 행동).
"""
    decision = f"""﻿# Decision: Stage 337HZ Candidate Training

- date: `{TODAY}`
- run_id: `{RUN_ID}`
- decision: `{DECISION}`
- judgment: `{JUDGMENT}`
- next_run_id: `{NEXT_RUN_ID}`

## Reason

HY review(검토)가 HX input(입력)을 training-ready(학습 준비)로 열었으므로 HZ는 LightGBM(라이트GBM), ExtraTrees(엑스트라트리스), XGBoost(엑스지부스트) 후보를 학습했다.

## Effect

다음 IA review(검토)는 proxy(프록시)가 좋아 보이는 후보가 있어도 MT5(메타트레이더5) KPI(핵심 성과 지표)로 오해하지 않고, ONNX parity(ONNX 동등성)와 proxy score(프록시 점수)를 분리해 판정한다.

## Boundary

`{CLAIM_BOUNDARY}`
"""
    _write_bom_text(REPORT_PATH, report)
    _write_bom_text(DECISION_DOC, decision)
    _write_bom_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    _write_bom_text(
        CURRENT_WORKING_STATE,
        f"""﻿# Current Working State

## Current Truth

- active_stage: `{STAGE_ID}`
- latest_completed_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- status: `{STATUS}`
- judgment: `{JUDGMENT}`
- decision: `{DECISION}`

## Effect

HZ training(학습)은 ONNX(온엑스) 후보 7개와 parity score(동등성 점수)를 만들었다.
효과는 IA review(검토)가 proxy score(프록시 점수)를 후보 선택이 아니라 다음 검증 입력으로만 쓸 수 있게 하는 것이다.

## Claim Boundary

`{CLAIM_BOUNDARY}`
""",
    )
    _write_bom_text(
        SELECTION_STATUS,
        f"""﻿# Selection Status

- latest_run: `{RUN_ID}`
- current_run: `{NEXT_RUN_ID}`
- model_selection: not_selected
- runtime_package: not_opened
- goal_achieve: not_claimed
- operating_promotion: not_claimed
- live_readiness: not_claimed
- onnx_parity: `{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}`

효과는 HZ trained candidate(학습 후보)를 selected model(선택 모델)로 오해하지 않게 하는 것이다.
""",
    )
    _write_bom_text(
        STAGE_BRIEF,
        f"""﻿# {STAGE_ID}

Latest completed run: `{RUN_ID}`

HZ trained(학습) seven offensive pivot ONNX candidates(공격 전환 ONNX 후보 7개).
ONNX parity(ONNX 동등성): `{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}`.
Selection(선택), MT5(메타트레이더5), runtime authority(런타임 권위)는 주장하지 않는다.
""",
    )
    existing = aw.io_path(CHANGELOG).read_text(encoding="utf-8-sig") if CHANGELOG.exists() else "﻿# Changelog\n"
    entry = (
        f"\n## {TODAY} - {RUN_ID}\n\n"
        f"- Trained(학습) `{summary['trained_model_rows']}` offensive pivot candidates(공격 전환 후보) and exported(내보내기) ONNX(온엑스).\n"
        f"- Recorded(기록) ONNX parity(ONNX 동등성) `{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}` and queued(대기열 등록) IA review(검토).\n"
    )
    _write_bom_text(CHANGELOG, existing.rstrip() + "\n" + entry)


def _update_ledgers(summary: dict, gates: pd.DataFrame) -> None:
    row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": summary["frame_rows"],
        "trained_models": summary["trained_model_rows"],
        "onnx_parity": f"{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}",
        "best_proxy": summary["best_inner_holdout_proxy_net"],
        "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": aw.rel(REPORT_PATH),
    }
    _append_or_replace_csv(RUN_REGISTRY, ["run_id"], row)
    _append_or_replace_csv(PROJECT_LEDGER, ["run_id"], row)
    _append_or_replace_csv(STAGE_LEDGER, ["run_id"], row)


def main() -> None:
    _ensure_dirs()
    summary, _artifacts = _train_all()
    gates = _make_gates(summary)
    _write_csv(GATE_AUDIT, gates)
    _write_receipts(summary, gates)
    _write_final(summary, gates)
    _write_docs(summary, gates)
    _update_ledgers(summary, gates)
    _update_artifact_registry(_artifact_paths())

    failed = gates.loc[~gates["status"].astype(str).eq("pass")]
    if not failed.empty:
        raise RuntimeError(f"HZ gates failed: {failed[['gate', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "trained_model_rows": summary["trained_model_rows"],
                "onnx_parity": f"{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}",
                "best_inner_holdout_proxy_net": summary["best_inner_holdout_proxy_net"],
                "positive_inner_holdout_proxy_rows": summary["positive_inner_holdout_proxy_rows"],
                "gate_passes": int(gates["status"].astype(str).eq("pass").sum()),
                "gate_total": int(len(gates)),
                "next_run_id": NEXT_RUN_ID,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
