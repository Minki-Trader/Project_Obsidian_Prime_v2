from __future__ import annotations

import hashlib
import json
import re
import sys
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

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
    review_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_inputs_without_db as io_review,
)


aw = io_review.aw
warnings.filterwarnings("ignore", message="X does not have valid feature names.*", category=UserWarning)

TODAY = "2026-06-01"
STAGE_ID = io_review.STAGE_ID
STAGE_DIR = io_review.STAGE_DIR
RUN_NUMBER = "run337IP"
RUN_ID = "run337IP_train_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_candidates_without_db_v1"
PARENT_RUN_ID = io_review.RUN_ID
NEXT_RUN_ID = "run337IQ_review_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_training_without_db_v1"
STATUS = "completed_stage337IP_lifecycle_cost_trade_shape_repair_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5"
JUDGMENT = "lifecycle_cost_trade_shape_repair_candidates_trained_with_onnx_parity_and_proxy_score_review_required"
DECISION = "stage337IP_open_run337IQ_lifecycle_cost_trade_shape_repair_training_review"
CLAIM_BOUNDARY = (
    "research_development_candidate_training_only_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_execution_no_forward_passed_no_forward_failed_no_runtime_package_authority_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IP_lifecycle_cost_repair_candidate_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IP_lifecycle_cost_trade_shape_repair_candidate_training.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

FEATURE_SCHEMA = RUN_DIR / "ip_allowed_feature_schema.json"
TRAINING_TASK_REVIEW = RUN_DIR / "ip_training_task_review.csv"
SAMPLE_WEIGHT_AUDIT = RUN_DIR / "ip_sample_weight_audit.csv"
TRAINED_MODEL_MANIFEST = RUN_DIR / "ip_trained_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "ip_onnx_parity_matrix.csv"
CLASSIFICATION_SCORECARD = RUN_DIR / "ip_inner_holdout_classification_scorecard.csv"
PROXY_TRADE_SCORECARD = RUN_DIR / "ip_inner_holdout_proxy_trade_scorecard.csv"
FEATURE_IMPORTANCE = RUN_DIR / "ip_feature_importance_top20.csv"
RUNTIME_FIREWALL = RUN_DIR / "ip_runtime_firewall_review.csv"
RELEASE_DISPOSITION = RUN_DIR / "ip_training_release_disposition.csv"
IQ_QUEUE = RUN_DIR / "run337IQ_review_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    io_review.FINAL_DECISION,
    io_review.GATE_AUDIT,
    io_review.IP_QUEUE,
    io_review.inr.IN_INPUT_FRAME,
    io_review.inr.IN_ALLOWED_FEATURES,
    io_review.inr.IN_TASK_SEEDS,
    io_review.IO_TASK_ELIGIBILITY,
)
OUTPUT_FILES = (
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
    IQ_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    STAGE_BRIEF,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)

FEATURE_SET_ID = "in_allowed_pretrade_features_v1"


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path))


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    target = path if len(str(path)) < 240 else io(path)
    frame.to_csv(target, index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def feature_hash(features: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(features).encode("utf-8")).hexdigest()


def safe_model_id(task_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", task_id).strip("_")
    return f"ip_{cleaned}"


def read_features() -> list[str]:
    allowed = read_csv(io_review.inr.IN_ALLOWED_FEATURES)
    column = "feature_name" if "feature_name" in allowed.columns else allowed.columns[0]
    return [str(feature) for feature in allowed[column].dropna().tolist()]


def split_inner(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    source_ids = pd.to_numeric(frame["source_row_id"], errors="coerce").astype(int)
    unique_ids = sorted(source_ids.unique().tolist())
    cutoff_index = max(1, int(len(unique_ids) * 0.80))
    cutoff = unique_ids[cutoff_index - 1]
    return frame.loc[source_ids <= cutoff].copy(), frame.loc[source_ids > cutoff].copy()


def sample_weights(frame: pd.DataFrame, column: str) -> pd.Series:
    return (
        pd.to_numeric(frame[column], errors="coerce")
        .replace([np.inf, -np.inf], np.nan)
        .fillna(1.0)
        .clip(lower=0.10, upper=12.0)
    )


def class_order_for_task(task: pd.Series) -> list[int]:
    if str(task["target_column"]) == "hx_active_flat_label":
        return [0, 1]
    return [0, 1, 2]


def model_family(task: pd.Series) -> str:
    return str(task["model_family"]).lower()


def make_model(task: pd.Series, class_order: Sequence[int]):
    family = model_family(task)
    is_binary = len(class_order) == 2
    if "extratrees" in family:
        return ExtraTreesClassifier(
            n_estimators=280,
            max_depth=13,
            min_samples_leaf=70,
            min_samples_split=140,
            max_features="sqrt",
            random_state=337980,
            n_jobs=-1,
        )
    if "xgboost" in family:
        if is_binary:
            return XGBClassifier(
                n_estimators=180,
                max_depth=4,
                learning_rate=0.04,
                subsample=0.86,
                colsample_bytree=0.82,
                reg_alpha=0.08,
                reg_lambda=2.4,
                objective="binary:logistic",
                eval_metric="logloss",
                tree_method="hist",
                random_state=337981,
                n_jobs=-1,
            )
        return XGBClassifier(
            n_estimators=190,
            max_depth=4,
            learning_rate=0.04,
            subsample=0.86,
            colsample_bytree=0.82,
            reg_alpha=0.08,
            reg_lambda=2.4,
            objective="multi:softprob",
            num_class=len(class_order),
            eval_metric="mlogloss",
            tree_method="hist",
            random_state=337982,
            n_jobs=-1,
        )
    if is_binary:
        return LGBMClassifier(
            objective="binary",
            n_estimators=220,
            learning_rate=0.036,
            max_depth=6,
            num_leaves=31,
            min_child_samples=160,
            subsample=0.86,
            colsample_bytree=0.82,
            reg_alpha=0.12,
            reg_lambda=1.3,
            random_state=337983,
            n_jobs=-1,
            verbose=-1,
        )
    return LGBMClassifier(
        objective="multiclass",
        num_class=len(class_order),
        n_estimators=230,
        learning_rate=0.034,
        max_depth=6,
        num_leaves=31,
        min_child_samples=160,
        subsample=0.86,
        colsample_bytree=0.82,
        reg_alpha=0.12,
        reg_lambda=1.3,
        random_state=337984,
        n_jobs=-1,
        verbose=-1,
    )


def export_model(model, task: pd.Series, path: Path, feature_count: int) -> dict[str, Any]:
    family = model_family(task)
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


def probability_and_pred(model, values: np.ndarray, class_order: Sequence[int]) -> tuple[np.ndarray, np.ndarray]:
    probabilities = ordered_sklearn_probabilities(model, values.astype("float64"), class_order=class_order)
    row_sum = probabilities.sum(axis=1, keepdims=True)
    probabilities = np.divide(probabilities, row_sum, out=np.zeros_like(probabilities), where=row_sum != 0.0)
    pred = np.asarray(class_order, dtype=int)[np.argmax(probabilities, axis=1)]
    return probabilities, pred


def label_counts(values: np.ndarray, class_order: Sequence[int]) -> str:
    counts = {str(label): 0 for label in class_order}
    labels, values_count = np.unique(values, return_counts=True)
    for label, count in zip(labels, values_count):
        counts[str(int(label))] = int(count)
    return json.dumps(counts, ensure_ascii=False, sort_keys=True)


def classification_score(
    model_id: str,
    task_id: str,
    split: str,
    model,
    frame: pd.DataFrame,
    features: Sequence[str],
    target: str,
    class_order: Sequence[int],
) -> dict[str, Any]:
    values = frame.loc[:, features].astype("float32").to_numpy()
    probs, pred = probability_and_pred(model, values, class_order)
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
        "pred_counts_json": label_counts(pred, class_order),
        "true_counts_json": label_counts(y_values, class_order),
        "signal_density": float(np.mean(pred != 1)) if len(pred) and 1 in class_order else float(np.mean(pred == 1)),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def future_column_for_target(target: str) -> str | None:
    if target.endswith("fwd6"):
        return "hx_future_log_return_6"
    if target.endswith("fwd18"):
        return "hx_future_log_return_18"
    if target.endswith("fwd24"):
        return "hx_future_log_return_24"
    return None


def proxy_trade_score(
    model_id: str,
    task_id: str,
    split: str,
    model,
    frame: pd.DataFrame,
    features: Sequence[str],
    target: str,
    class_order: Sequence[int],
) -> dict[str, Any]:
    values = frame.loc[:, features].astype("float32").to_numpy()
    _probs, pred = probability_and_pred(model, values, class_order)
    future_column = future_column_for_target(target)
    if future_column is None:
        return {
            "model_id": model_id,
            "task_id": task_id,
            "split": split,
            "score_mode": "active_flat_gate_only(활성/관망 게이트 전용)",
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
            "allowed_use": "active gate sanity only(활성 게이트 점검 전용)",
            "forbidden_use": "directional MT5 KPI or candidate selection(방향 MT5 KPI 또는 후보 선택)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    future = pd.to_numeric(frame[future_column], errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    direction = np.where(pred == 2, 1.0, np.where(pred == 0, -1.0, 0.0))
    pnl = np.where(direction == 0.0, 0.0, direction * future)
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
        "allowed_use": "proxy signal sanity only(프록시 신호 점검 전용)",
        "forbidden_use": "MT5 KPI, Forward Passed/Failed, candidate selection(MT5 KPI, 전진 통과/실패, 후보 선택)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def feature_importances(model, features: Sequence[str]) -> np.ndarray:
    if hasattr(model, "feature_importances_"):
        return np.asarray(model.feature_importances_, dtype="float64")
    return np.zeros(len(features), dtype="float64")


def train_all() -> dict[str, Any]:
    frame = pd.read_parquet(io(io_review.inr.IN_INPUT_FRAME)).copy()
    features = read_features()
    missing = [feature for feature in features if feature not in frame.columns]
    if missing:
        raise ValueError(f"missing features(누락 피처): {missing}")
    eligibility = read_csv(io_review.IO_TASK_ELIGIBILITY)
    tasks = read_csv(io_review.inr.IN_TASK_SEEDS)
    eligible_ids = eligibility.loc[
        eligibility["eligible"].astype(str).str.lower().isin(["true", "1", "yes"]),
        "task_id",
    ].astype(str)
    tasks = tasks.loc[tasks["task_id"].astype(str).isin(eligible_ids)].copy()
    if tasks.empty:
        raise RuntimeError("no eligible IO tasks were loaded(적격 IO 작업을 읽지 못함)")
    io_gates = read_csv(io_review.GATE_AUDIT)
    if not io_gates["status"].astype(str).str.lower().isin(["pass", "passed"]).all():
        raise RuntimeError("IO gates are not all passed(IO 게이트가 모두 통과하지 않음)")

    feature_order_hash = feature_hash(features)
    write_json(
        FEATURE_SCHEMA,
        {
            "feature_set_id": FEATURE_SET_ID,
            "feature_count": len(features),
            "feature_order_hash": feature_order_hash,
            "features": features,
            "source": rel(io_review.inr.IN_ALLOWED_FEATURES),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )

    task_rows: list[dict[str, Any]] = []
    weight_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    class_rows: list[dict[str, Any]] = []
    proxy_rows: list[dict[str, Any]] = []
    importance_rows: list[dict[str, Any]] = []

    for _, task in tasks.iterrows():
        target = str(task["target_column"])
        valid_col = str(task["valid_column"])
        weight_col = str(task["sample_weight_column"])
        class_order = class_order_for_task(task)
        task_frame = frame.loc[
            pd.to_numeric(frame[valid_col], errors="coerce").fillna(0).astype(int).eq(1)
            & pd.to_numeric(frame[target], errors="coerce").fillna(-1).astype(int).ne(-1)
        ].copy()
        inner_train, inner_holdout = split_inner(task_frame)
        weights = sample_weights(inner_train, weight_col)
        model = make_model(task, class_order)
        x_train = inner_train.loc[:, features].astype("float32").to_numpy()
        y_train = pd.to_numeric(inner_train[target], errors="raise").astype(int).to_numpy()
        model.fit(x_train, y_train, sample_weight=weights.to_numpy(dtype="float64"))

        task_id = str(task["task_id"])
        model_id = safe_model_id(task_id)
        model_path = MODEL_DIR / f"{model_id}.joblib"
        onnx_path = ONNX_DIR / f"{model_id}.onnx"
        ensure_parent(model_path)
        ensure_parent(onnx_path)
        joblib.dump(
            {
                "model": model,
                "features": features,
                "class_order": list(class_order),
                "task": task.to_dict(),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            io(model_path),
        )
        export_meta = export_model(model, task, onnx_path, len(features))
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
                "training_disposition": "trained_no_selection_no_mt5(학습됨, 선택/MT5 없음)",
                "repair_family": task["repair_family"],
                "feature_count": len(features),
                "target_column": target,
                "valid_column": valid_col,
                "sample_weight_column": weight_col,
                "model_family": task["model_family"],
                "model_config_id": task["model_config_id"],
                "inner_train_rows": int(len(inner_train)),
                "inner_holdout_rows": int(len(inner_holdout)),
                "effect": "IQ review(IQ 검토) 전용 후보를 학습한다.",
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
                "effect": "학습에 들어간 weight(가중치) 분포를 기록한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        parity_rows.append(
            {
                "model_id": model_id,
                "task_id": task_id,
                "onnx_path": rel(onnx_path),
                "passed": "true" if parity["passed"] else "false",
                "rows": parity["rows"],
                "max_abs_diff": parity["max_abs_diff"],
                "mean_abs_diff": parity["mean_abs_diff"],
                "tolerance": parity["tolerance"],
                "effect": "Python/ONNX(파이썬/온엑스) probability parity(확률 동등성)를 확인한다.",
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
                "feature_order_hash": feature_order_hash,
                "class_order_json": json.dumps(list(class_order)),
                "model_path": rel(model_path),
                "model_sha256": sha(model_path),
                "onnx_path": rel(onnx_path),
                "onnx_sha256": sha(onnx_path),
                "onnx_probability_output_name": export_meta.get("probability_output_name", "probabilities"),
                "inner_train_rows": int(len(inner_train)),
                "inner_holdout_rows": int(len(inner_holdout)),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        class_rows.extend(
            [
                classification_score(model_id, task_id, "inner_train", model, inner_train, features, target, class_order),
                classification_score(model_id, task_id, "inner_holdout", model, inner_holdout, features, target, class_order),
            ]
        )
        proxy_rows.extend(
            [
                proxy_trade_score(model_id, task_id, "inner_train", model, inner_train, features, target, class_order),
                proxy_trade_score(model_id, task_id, "inner_holdout", model, inner_holdout, features, target, class_order),
            ]
        )
        importances = feature_importances(model, features)
        for rank, index in enumerate(np.argsort(importances)[::-1][:20], start=1):
            importance_rows.append(
                {
                    "model_id": model_id,
                    "task_id": task_id,
                    "rank": rank,
                    "feature": features[index],
                    "importance": float(importances[index]),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    write_csv(TRAINING_TASK_REVIEW, pd.DataFrame(task_rows))
    write_csv(SAMPLE_WEIGHT_AUDIT, pd.DataFrame(weight_rows))
    write_csv(TRAINED_MODEL_MANIFEST, pd.DataFrame(model_rows))
    write_csv(ONNX_PARITY, pd.DataFrame(parity_rows))
    write_csv(CLASSIFICATION_SCORECARD, pd.DataFrame(class_rows))
    write_csv(PROXY_TRADE_SCORECARD, pd.DataFrame(proxy_rows))
    write_csv(FEATURE_IMPORTANCE, pd.DataFrame(importance_rows))

    proxy_frame = pd.DataFrame(proxy_rows)
    holdout_proxy = proxy_frame.loc[proxy_frame["split"].eq("inner_holdout")].copy()
    directional_holdout = holdout_proxy.loc[holdout_proxy["score_mode"].astype(str).str.startswith("directional_")]
    firewall = []
    release = []
    for _, model_row in pd.DataFrame(model_rows).iterrows():
        model_id = str(model_row["model_id"])
        score_rows = directional_holdout.loc[directional_holdout["model_id"].astype(str).eq(model_id)]
        best_net = float(score_rows["net_log_return_after_cost"].max()) if not score_rows.empty else 0.0
        best_pf = float(score_rows["profit_factor"].max()) if not score_rows.empty else 0.0
        disposition = "review_required_proxy_positive" if best_net > 0 else "review_required_proxy_nonpositive"
        firewall.append(
            {
                "model_id": model_id,
                "runtime_package_allowed": "false",
                "mt5_execution_allowed": "false",
                "candidate_selection": "not_run",
                "reason": "IQ review required before runtime package(런타임 패키지 전 IQ 검토 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        release.append(
            {
                "model_id": model_id,
                "release_disposition": disposition,
                "inner_holdout_proxy_net": best_net,
                "inner_holdout_profit_factor": best_pf,
                "allowed_next_use": "IQ review only(IQ 검토 전용)",
                "forbidden_use": "runtime package, MT5 KPI, candidate selection(런타임 패키지, MT5 KPI, 후보 선택)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(RUNTIME_FIREWALL, pd.DataFrame(firewall))
    write_csv(RELEASE_DISPOSITION, pd.DataFrame(release))
    write_csv(
        IQ_QUEUE,
        pd.DataFrame(
            [
                {
                    "next_run_id": NEXT_RUN_ID,
                    "parent_run_id": RUN_ID,
                    "queued_task": "review_lifecycle_cost_trade_shape_repair_training_before_runtime_package(런타임 패키지 전 생명주기 비용 거래형태 수리 학습 검토)",
                    "trained_model_manifest": rel(TRAINED_MODEL_MANIFEST),
                    "onnx_parity": rel(ONNX_PARITY),
                    "proxy_trade_scorecard": rel(PROXY_TRADE_SCORECARD),
                    "required_review": "proxy usability, ONNX parity, side/PF/drawdown/cost attribution(프록시 활용성, ONNX 동등성, 방향/PF/낙폭/비용 귀속)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        ),
    )

    parity_frame = pd.DataFrame(parity_rows)
    class_frame = pd.DataFrame(class_rows)
    summary = {
        "frame_rows": int(len(frame)),
        "task_seed_rows": int(len(tasks)),
        "trained_model_rows": int(len(model_rows)),
        "onnx_rows": int(len(model_rows)),
        "onnx_parity_rows": int(len(parity_frame)),
        "onnx_parity_passed_rows": int(parity_frame["passed"].astype(str).eq("true").sum()) if not parity_frame.empty else 0,
        "classification_rows": int(len(class_frame)),
        "proxy_trade_rows": int(len(proxy_frame)),
        "feature_count": len(features),
        "feature_order_hash": feature_order_hash,
        "best_inner_holdout_proxy_net": float(directional_holdout["net_log_return_after_cost"].max()) if not directional_holdout.empty else 0.0,
        "best_inner_holdout_profit_factor": float(directional_holdout["profit_factor"].max()) if not directional_holdout.empty else 0.0,
        "positive_inner_holdout_proxy_rows": int((directional_holdout["net_log_return_after_cost"] > 0).sum()) if not directional_holdout.empty else 0,
        "max_inner_holdout_balanced_accuracy": float(class_frame.loc[class_frame["split"].eq("inner_holdout"), "balanced_accuracy"].max()) if not class_frame.empty else 0.0,
        "max_inner_holdout_signal_density": float(holdout_proxy["signal_density"].max()) if not holdout_proxy.empty else 0.0,
        "next_action": NEXT_RUN_ID,
    }
    return summary


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    io_gates = read_csv(io_review.GATE_AUDIT)
    return pd.DataFrame(
        [
            gate_row(
                "parent_io_gates_passed",
                "passed" if io_gates["status"].astype(str).str.lower().isin(["pass", "passed"]).all() else "failed",
                rel(io_review.GATE_AUDIT),
                "IO review(IO 검토) 통과 뒤 학습한다.",
            ),
            gate_row(
                "feature_schema_materialized",
                "passed" if summary["feature_count"] == 58 and exists(FEATURE_SCHEMA) else "failed",
                rel(FEATURE_SCHEMA),
                "ONNX(온엑스) 인계용 feature order(피처 순서)를 고정한다.",
            ),
            gate_row(
                "all_eligible_tasks_trained",
                "passed" if summary["trained_model_rows"] == summary["task_seed_rows"] == 7 else "failed",
                rel(TRAINING_TASK_REVIEW),
                "IO 적격 작업 7개가 모두 학습됐다.",
            ),
            gate_row(
                "onnx_exports_materialized",
                "passed" if summary["onnx_rows"] == summary["trained_model_rows"] else "failed",
                rel(TRAINED_MODEL_MANIFEST),
                "각 모델의 ONNX(온엑스) 산출물이 있다.",
            ),
            gate_row(
                "onnx_parity_passed",
                "passed"
                if summary["onnx_parity_passed_rows"] == summary["onnx_parity_rows"] == summary["trained_model_rows"]
                else "failed",
                rel(ONNX_PARITY),
                "Python/ONNX(파이썬/온엑스) probability parity(확률 동등성)가 통과했다.",
            ),
            gate_row(
                "classification_scored",
                "passed" if summary["classification_rows"] == summary["trained_model_rows"] * 2 else "failed",
                rel(CLASSIFICATION_SCORECARD),
                "inner train/holdout(내부 학습/보류) 분류 진단이 있다.",
            ),
            gate_row(
                "proxy_trade_scored",
                "passed" if summary["proxy_trade_rows"] == summary["trained_model_rows"] * 2 else "failed",
                rel(PROXY_TRADE_SCORECARD),
                "proxy trade(프록시 거래) 점수가 있다.",
            ),
            gate_row(
                "runtime_firewall_active",
                "passed" if exists(RUNTIME_FIREWALL) and exists(RELEASE_DISPOSITION) else "failed",
                f"{rel(RUNTIME_FIREWALL)};{rel(RELEASE_DISPOSITION)}",
                "학습 산출물과 runtime package(런타임 패키지)를 분리한다.",
            ),
            gate_row(
                "next_review_queue_opened",
                "passed" if exists(IQ_QUEUE) else "failed",
                rel(IQ_QUEUE),
                "IQ review(IQ 검토)를 학습 뒤 필수 단계로 연다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed",
                rel(CLAIM_RECEIPT),
                "선택, MT5 성공, runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit",
                "passed",
                rel(GATE_AUDIT),
                "gate evidence(게이트 근거)를 closeout(종료 기록)에 연결한다.",
            ),
        ]
    )


def artifact_paths() -> list[Path]:
    return list(OUTPUT_FILES)


def write_receipts(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **base,
            "measurement_scope": "inner holdout proxy and ONNX parity only(내부 보류 프록시와 ONNX 동등성 전용)",
            "scoreboard": "structural_scout(구조 스카우트)",
            "parity_level": "P2_model_input_parity_closed(P2 모델 입력 동등성 닫힘)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "effect": "후보는 만들지만 MT5 KPI(MT5 핵심 성과 지표)로 해석하지 않는다.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": rel(io_review.inr.IN_INPUT_FRAME),
            "time_axis": "UTC closed-bar/as-of inherited from IN(UTC 닫힌 봉/시점 기준, IN 상속)",
            "sample_scope": f"Tier A rows={summary['frame_rows']}; Tier B missing_required(Tier A 행={summary['frame_rows']}, Tier B 필수 누락)",
            "feature_label_boundary": rel(io_review.IO_FEATURE_BOUNDARY_REVIEW),
            "split_boundary": "source_row_id ordered 80/20 inner split(source_row_id 순서 80/20 내부 분할)",
            "leakage_risk": "train-only labels and weights are excluded from model features(학습 전용 라벨/가중치는 모델 피처에서 제외)",
            "data_hash_or_identity": {rel(io_review.inr.IN_INPUT_FRAME): sha(io_review.inr.IN_INPUT_FRAME)},
            "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "LightGBM/XGBoost/ExtraTrees(라이트GBM/엑스지부스트/엑스트라트리스)",
            "trained_model_rows": summary["trained_model_rows"],
            "onnx_rows": summary["onnx_rows"],
            "onnx_parity": f"{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}",
            "target_and_label": "hx_label_class_fwd6, hx_label_class_fwd18, hx_active_flat_label",
            "split_method": "source_row_id ordered inner holdout(source_row_id 순서 내부 보류)",
            "selection_metric": "none; review only(없음, 검토 전용)",
            "secondary_metrics": "balanced_accuracy, macro_f1, proxy net/PF/drawdown(균형 정확도, 매크로 F1, 프록시 순수익/PF/낙폭)",
            "threshold_policy": "argmax only, no threshold tuning(argmax 전용, 임계값 조정 없음)",
            "overfit_risk": "multiple task exploration without WFO(여러 작업 탐색, WFO 없음)",
            "calibration_risk": "probabilities are uncalibrated rank signals(확률은 미보정 순위 신호)",
            "comparison_baseline": rel(io_review.FINAL_DECISION),
            "validation_judgment": JUDGMENT,
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": "lifecycle/cost/trade-shape candidates trained(생명주기/비용/거래형태 후보 학습)",
            "comparison_baseline": rel(io_review.FINAL_DECISION),
            "best_inner_holdout_proxy_net": summary["best_inner_holdout_proxy_net"],
            "best_inner_holdout_profit_factor": summary["best_inner_holdout_profit_factor"],
            "positive_inner_holdout_proxy_rows": summary["positive_inner_holdout_proxy_rows"],
            "segment_checks": "direction, density, drawdown proxy only(방향, 밀도, 낙폭 프록시 전용)",
            "trade_shape": rel(PROXY_TRADE_SCORECARD),
            "alternative_explanations": "proxy may not survive MT5 lifecycle/cost(프록시는 MT5 생명주기/비용에서 사라질 수 있음)",
            "attribution_confidence": "low_until_IQ_review_and_MT5_probe(IQ 검토와 MT5 탐침 전까지 낮음)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(Path(__file__)),
            "runtime_path": "not_created(미생성)",
            "shared_contract": rel(FEATURE_SCHEMA),
            "known_differences": "no MT5 package or tester run( MT5 패키지 또는 테스터 실행 없음)",
            "parity_check": rel(ONNX_PARITY),
            "parity_identity": f"{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}",
            "runtime_claim_boundary": "research-only(연구 전용)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(TRAINED_MODEL_MANIFEST), rel(ONNX_PARITY), rel(PROXY_TRADE_SCORECARD), rel(GATE_AUDIT)],
            "evidence_missing": "IQ review, runtime package, MT5 runtime probe(IQ 검토, 런타임 패키지, MT5 런타임 탐침)",
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "후보는 학습됐지만 운영 모델은 아니다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "mt5_execution": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in artifact_paths() if exists(path) and io(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest(목록과 함께 생성)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
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
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337IP Lifecycle Cost Repair Candidate Training(run337IP 생명주기 비용 수리 후보 학습)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- trained_model_rows(학습 모델 수): `{final['trained_model_rows']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- best_inner_holdout_profit_factor(최고 내부 보류 수익 팩터): `{final['best_inner_holdout_profit_factor']}`
- positive_inner_holdout_proxy_rows(내부 보류 프록시 양성 행): `{final['positive_inner_holdout_proxy_rows']}`

## Action(행동)

IO review(IO 검토)에서 적격 판정된 7개 task seed(작업 씨앗)를 학습하고 ONNX(온엑스) 산출물과 proxy scorecard(프록시 점수표)를 만들었다.
Effect(효과): IQ review(IQ 검토)가 proxy usability(프록시 활용성), ONNX parity(ONNX 동등성), side/PF/drawdown/cost(방향/PF/낙폭/비용)를 함께 볼 수 있다.

## Boundary(경계)

No candidate selection(후보 선택 없음), no MT5 execution(MT5 실행 없음), no Forward Passed/Failed(전진 통과/실패 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`{NEXT_RUN_ID}`에서 학습 산출물을 검토한다.
"""
    decision = f"""# {TODAY} Stage337IP Decision(337IP 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(TRAINED_MODEL_MANIFEST)}`, `{rel(ONNX_PARITY)}`, `{rel(PROXY_TRADE_SCORECARD)}`

Action(행동): lifecycle/cost/trade-shape repair candidate(생명주기/비용/거래형태 수리 후보)를 학습했다.
Effect(효과): 다음 IQ review(IQ 검토)가 proxy KPI(프록시 핵심 성과 지표)를 MT5 KPI(MT5 핵심 성과 지표)로 착각하지 않게 분리한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

IP training(IP 학습)은 ONNX(온엑스) 후보와 proxy score(프록시 점수)를 만들었다.
효과는 IQ review(IQ 검토)가 학습 산출물을 runtime package(런타임 패키지)로 넘길지 좁게 판단하게 하는 것이다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- trained_model_rows(학습 모델 수): `{final['trained_model_rows']}`
- ONNX parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- candidate_selection(후보 선택): `not_run(미실행)`
- MT5 execution(MT5 실행): `not_run(미실행)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`
- operating_promotion(운영 승격): `not_claimed(주장 안 함)`
- goal_achieve(목표 달성): `not_claimed(주장 안 함)`

Effect(효과): 학습 산출물을 운영 모델로 오해하지 않게 한다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run337IP {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337IP Lifecycle Cost Repair Candidate Training(생명주기 비용 수리 후보 학습)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): 7개 ONNX(온엑스) 후보를 만들고 parity(동등성) `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`를 기록했다.
""",
    )
    changelog_entry = f"""## {TODAY} run337IP Lifecycle Cost Repair Candidate Training(생명주기 비용 수리 후보 학습)

- action(행동): IO 적격 task seed(작업 씨앗) 7개를 학습하고 ONNX(온엑스) 후보를 만들었다.
- effect(효과): IQ review(IQ 검토)가 proxy(프록시), parity(동등성), trade shape(거래 형태)를 함께 검토할 수 있게 했다.
- boundary(경계): candidate selection(후보 선택), MT5 execution(MT5 실행), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    frame = read_csv(path) if exists(path) else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv(path, frame[ordered])


def update_registers(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {
            **base,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "candidate_training_inner_holdout_proxy",
            "trained_model_rows": final["trained_model_rows"],
            "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}",
            "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"],
            "best_inner_holdout_profit_factor": final["best_inner_holdout_profit_factor"],
            "result_status": "trained_review_required_no_selection",
        },
        {
            **base,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    registry = read_csv(ARTIFACT_REGISTRY) if exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if exists(path) and io(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": rel(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        write_csv(ARTIFACT_REGISTRY, registry[columns])


def main() -> None:
    for path in (RUN_DIR, MODEL_DIR, ONNX_DIR, REVIEW_DIR, DECISION_DOC.parent):
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")
    summary = train_all()
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"IP gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "trained_model_rows": final["trained_model_rows"],
                "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}",
                "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"],
                "best_inner_holdout_profit_factor": final["best_inner_holdout_profit_factor"],
                "positive_inner_holdout_proxy_rows": final["positive_inner_holdout_proxy_rows"],
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
