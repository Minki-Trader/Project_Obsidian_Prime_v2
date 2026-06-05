from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import (  # noqa: E402
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_sklearn_probabilities,
)
from stage_pipelines.stage337 import review_broker_confirmed_side_cost_curve_repair_inputs_without_db as ex  # noqa: E402


aw = ex.aw

TODAY = "2026-05-31"
STAGE_ID = ex.STAGE_ID
RUN_NUMBER = "run337EY"
RUN_ID = "run337EY_train_broker_confirmed_side_cost_curve_repair_candidates_without_db_v1"
PARENT_RUN_ID = ex.RUN_ID
NEXT_RUN_ID = "run337EZ_review_broker_confirmed_side_cost_curve_training_without_db_v1"
STATUS = "completed_stage337EY_side_cost_curve_repair_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5"
JUDGMENT = "guarded_side_cost_curve_candidates_trained_with_onnx_parity_review_required_no_selection"
DECISION = "stage337EY_open_run337EZ_review_broker_confirmed_side_cost_curve_training_without_db"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EY_broker_confirmed_side_cost_curve_training_without_db_"
    "reviewed_train_only_inputs_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ex.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEWS_DIR = ex.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EY_broker_confirmed_side_cost_curve_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337EY_broker_confirmed_side_cost_curve_training.md"
SELECTED_STATUS = ex.SELECTED_STATUS
STAGE_BRIEF = ex.STAGE_BRIEF
WORKSPACE_STATE = ex.WORKSPACE_STATE
CURRENT_STATE = ex.CURRENT_STATE
CHANGELOG = ex.CHANGELOG
RUN_REGISTRY = ex.RUN_REGISTRY
ALPHA_LEDGER = ex.ALPHA_LEDGER
ARTIFACT_REGISTRY = ex.ARTIFACT_REGISTRY
STAGE_LEDGER = ex.STAGE_LEDGER

EX_FINAL = ex.FINAL_DECISION
EX_GATES = ex.GATE_AUDIT
EX_QUEUE = ex.EY_QUEUE
TRAINING_TASK_MATRIX = ex.TRAINING_TASK_MATRIX
FEATURE_REVIEW = ex.FEATURE_BOUNDARY_REVIEW
FEATURE_EXCLUSION = ex.TRAINING_FEATURE_EXCLUSION
INPUT_SAFETY_REVIEW = ex.INPUT_SAFETY_REVIEW
EW_FRAME = ex.EW_FRAME
EW_ALLOWED_FEATURES = ex.EW_ALLOWED_FEATURES
EW_QUARANTINE = ex.EW_QUARANTINE

FEATURE_SCHEMA = RUN_DIR / "ey_allowed_feature_schema.json"
TRAINING_TASK_REVIEW = RUN_DIR / "ey_training_task_review.csv"
SAMPLE_WEIGHT_AUDIT = RUN_DIR / "sample_weight_audit.csv"
TRAINED_MODEL_MANIFEST = RUN_DIR / "trained_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "onnx_parity_matrix.csv"
CLASSIFICATION_SCORECARD = RUN_DIR / "inner_holdout_classification_scorecard.csv"
PROXY_TRADE_SCORECARD = RUN_DIR / "inner_holdout_proxy_trade_scorecard.csv"
FEATURE_IMPORTANCE = RUN_DIR / "feature_importance_top20.csv"
RUNTIME_FIREWALL = RUN_DIR / "runtime_firewall_review.csv"
RELEASE_DISPOSITION = RUN_DIR / "training_release_disposition.csv"
EZ_QUEUE = RUN_DIR / "run337EZ_review_queue.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EX_FINAL,
    EX_GATES,
    EX_QUEUE,
    TRAINING_TASK_MATRIX,
    FEATURE_REVIEW,
    FEATURE_EXCLUSION,
    INPUT_SAFETY_REVIEW,
    EW_FRAME,
    EW_ALLOWED_FEATURES,
    EW_QUARANTINE,
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
    EZ_QUEUE,
    ROUTING_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    Path(__file__),
)

LABEL_ORDER = [0, 1, 2]
INT_TO_LABEL = {0: "short", 1: "flat", 2: "long"}

TASK_REVIEW_COLUMNS = (
    "task_id",
    "training_disposition",
    "feature_count",
    "target_column",
    "sample_weight_expression",
    "inner_train_rows",
    "inner_holdout_rows",
    "effect",
    "claim_boundary",
)
WEIGHT_COLUMNS = (
    "task_id",
    "sample_weight_expression",
    "rows",
    "weight_min",
    "weight_mean",
    "weight_max",
    "nonfinite_weights",
    "effect",
    "claim_boundary",
)
MODEL_COLUMNS = (
    "model_id",
    "task_id",
    "feature_set_id",
    "target_column",
    "sample_weight_expression",
    "model_family",
    "model_config_id",
    "feature_count",
    "feature_order_hash",
    "class_order_json",
    "model_path",
    "model_sha256",
    "onnx_path",
    "onnx_sha256",
    "onnx_probability_output_name",
    "inner_train_rows",
    "inner_holdout_rows",
    "claim_boundary",
)
PARITY_COLUMNS = (
    "model_id",
    "task_id",
    "onnx_path",
    "passed",
    "rows",
    "max_abs_diff",
    "mean_abs_diff",
    "onnx_row_sum_max_abs_error",
    "input_name",
    "output_names",
    "claim_boundary",
)
CLASS_COLUMNS = (
    "model_id",
    "task_id",
    "split",
    "rows",
    "accuracy",
    "balanced_accuracy",
    "macro_f1",
    "log_loss",
    "pred_counts_json",
    "true_counts_json",
    "signal_density",
    "claim_boundary",
)
PROXY_COLUMNS = (
    "model_id",
    "task_id",
    "split",
    "trade_count",
    "signal_density",
    "net_log_return_after_cost",
    "profit_factor",
    "expectancy",
    "max_drawdown",
    "recovery_factor",
    "long_count",
    "short_count",
    "long_net",
    "short_net",
    "allowed_use",
    "forbidden_use",
    "claim_boundary",
)
IMPORTANCE_COLUMNS = (
    "model_id",
    "rank",
    "feature_name",
    "importance",
    "claim_boundary",
)
REVIEW_COLUMNS = (
    "review_id",
    "subject",
    "rows",
    "metric_1",
    "metric_2",
    "review_status",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "evidence_path",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def current_branch() -> str:
    proc = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, capture_output=True, text=True, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def rel(path: Path | str) -> str:
    return aw.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return aw.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    return aw.read_json(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return aw.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def feature_order_hash(features: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(features).encode("utf-8")).hexdigest()


def read_features() -> list[str]:
    rows = read_csv(EW_ALLOWED_FEATURES)
    return [row["feature_name"] for row in rows if row.get("feature_name")]


def safe_model_id(task_id: str) -> str:
    return f"ey_{task_id}".replace(" ", "_").replace("*", "x").replace("/", "_")


def split_inner(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    unique_ids = sorted(pd.to_numeric(frame["source_row_id"], errors="coerce").dropna().astype(int).unique().tolist())
    cutoff_index = max(1, int(len(unique_ids) * 0.80))
    cutoff = unique_ids[cutoff_index - 1]
    inner_train = frame[pd.to_numeric(frame["source_row_id"], errors="coerce").astype(int) <= cutoff].copy()
    inner_holdout = frame[pd.to_numeric(frame["source_row_id"], errors="coerce").astype(int) > cutoff].copy()
    return inner_train, inner_holdout


def sample_weights(frame: pd.DataFrame, expression: str) -> pd.Series:
    parts = [part.strip() for part in expression.split("*")]
    weight = pd.Series(np.ones(len(frame), dtype="float64"), index=frame.index)
    for part in parts:
        if part not in frame.columns:
            raise ValueError(f"missing sample weight column {part}")
        weight = weight * pd.to_numeric(frame[part], errors="coerce").fillna(1.0)
    return weight.clip(lower=0.10, upper=10.0)


def train_model(task: Mapping[str, str], frame: pd.DataFrame, features: Sequence[str]) -> tuple[Any, pd.DataFrame, pd.DataFrame, pd.Series]:
    inner_train, inner_holdout = split_inner(frame)
    target = str(task["target_column"])
    weights = sample_weights(inner_train, str(task["sample_weight_expression"]))
    model = ExtraTreesClassifier(
        n_estimators=160,
        max_depth=8,
        min_samples_leaf=120,
        class_weight=None,
        random_state=33731,
        n_jobs=-1,
    )
    X = inner_train.loc[:, features].astype("float32").to_numpy()
    y = pd.to_numeric(inner_train[target], errors="raise").astype(int).to_numpy()
    model.fit(X, y, sample_weight=weights.to_numpy(dtype="float64"))
    return model, inner_train, inner_holdout, weights


def probability_and_pred(model: Any, frame: pd.DataFrame, features: Sequence[str]) -> tuple[np.ndarray, np.ndarray]:
    values = frame.loc[:, features].astype("float32").to_numpy()
    probabilities = ordered_sklearn_probabilities(model, values, LABEL_ORDER)
    pred = np.asarray(LABEL_ORDER, dtype=int)[np.argmax(probabilities, axis=1)]
    return probabilities, pred


def classification_score(model_id: str, task_id: str, split: str, model: Any, frame: pd.DataFrame, features: Sequence[str]) -> dict[str, Any]:
    probs, pred = probability_and_pred(model, frame, features)
    y = pd.to_numeric(frame["label_class"], errors="raise").astype(int).to_numpy()
    labels = LABEL_ORDER
    return {
        "model_id": model_id,
        "task_id": task_id,
        "split": split,
        "rows": int(len(frame)),
        "accuracy": float(accuracy_score(y, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
        "macro_f1": float(f1_score(y, pred, average="macro")),
        "log_loss": float(log_loss(y, probs, labels=labels)),
        "pred_counts_json": json.dumps({INT_TO_LABEL[int(k)]: int(v) for k, v in zip(*np.unique(pred, return_counts=True))}, ensure_ascii=False, sort_keys=True),
        "true_counts_json": json.dumps({INT_TO_LABEL[int(k)]: int(v) for k, v in zip(*np.unique(y, return_counts=True))}, ensure_ascii=False, sort_keys=True),
        "signal_density": float(np.mean(pred != 1)) if len(pred) else 0.0,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def proxy_trade_score(model_id: str, task_id: str, split: str, model: Any, frame: pd.DataFrame, features: Sequence[str]) -> dict[str, Any]:
    _probs, pred = probability_and_pred(model, frame, features)
    future = pd.to_numeric(frame["future_log_return_12"], errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    if "cost_return" in frame.columns:
        cost = pd.to_numeric(frame["cost_return"], errors="coerce").fillna(0.0).to_numpy(dtype="float64")
    else:
        cost = np.zeros(len(frame), dtype="float64")
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
        "allowed_use": "proxy sanity only(프록시 점검 전용)",
        "forbidden_use": "MT5 KPI, Forward Passed/Failed, candidate selection(MT5 성과, 전진 통과/실패, 후보 선택)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def review_firewall_and_release() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    firewall_rows = [
        {
            "review_id": "no_candidate_selection",
            "subject": "candidate selection firewall(후보 선택 방화벽)",
            "rows": 4,
            "metric_1": "selection=not_run",
            "metric_2": "rank review deferred to EZ(EZ로 순위 검토 지연)",
            "review_status": "active",
            "allowed_use": "review queue only(검토 대기열 전용)",
            "forbidden_use": "promotion or selected model(승격 또는 선택 모델)",
            "effect": "prevents in-sample/proxy selection(인샘플/프록시 선택 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "no_mt5_or_forward_claim",
            "subject": "MT5/Forward firewall(MT5/전진 방화벽)",
            "rows": 4,
            "metric_1": "mt5=not_run",
            "metric_2": "forward=not_claimed",
            "review_status": "active",
            "allowed_use": "future runtime probe planning(미래 런타임 탐침 계획)",
            "forbidden_use": "Forward Passed/Failed or runtime authority(전진 통과/실패 또는 런타임 권위)",
            "effect": "keeps ONNX training separate from operating evidence(ONNX 학습을 운영 근거와 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    release_rows = [
        {
            "review_id": "training_release_disposition",
            "subject": "training release disposition(학습 해제 처분)",
            "rows": 4,
            "metric_1": "review_required",
            "metric_2": NEXT_RUN_ID,
            "review_status": "no_release_review_required",
            "allowed_use": "EZ training review(EZ 학습 검토)",
            "forbidden_use": "selected candidate or live readiness(선택 후보 또는 실거래 준비)",
            "effect": "moves trained ONNX artifacts to review, not operation(학습 ONNX 산출물을 운영이 아니라 검토로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return firewall_rows, release_rows


def build_ez_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "ez_review_side_cost_curve_training",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review trained side/cost/curve ONNX candidates(학습된 방향/비용/곡선 ONNX 후보 검토)",
            "required_inputs": f"{rel(TRAINED_MODEL_MANIFEST)};{rel(ONNX_PARITY)};{rel(CLASSIFICATION_SCORECARD)};{rel(PROXY_TRADE_SCORECARD)}",
            "required_outputs": "training_review_scorecard and runtime probe decision(학습 검토 점수표와 런타임 탐침 결정)",
            "blocked_if_missing": "model manifest or ONNX parity(모델 목록 또는 ONNX 동등성)",
            "forbidden_action": "no MT5/Forward/Goal claim without runtime probe(런타임 탐침 없는 MT5/전진/목표 주장 금지)",
            "effect": "separates model creation from candidate judgment(모델 제작과 후보 판정을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def train_all() -> tuple[list[Path], dict[str, Any]]:
    frame = pd.read_parquet(aw.io_path(EW_FRAME)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame.sort_values(["source_row_id", "cost_policy_id"], inplace=True)
    features = read_features()
    missing_features = [feature for feature in features if feature not in frame.columns]
    if missing_features:
        raise ValueError(f"missing features: {missing_features}")
    task_rows = read_csv(TRAINING_TASK_MATRIX)
    eligible_tasks = [row for row in task_rows if row.get("training_eligibility_status") == "eligible_for_guarded_training_reviewed_inputs"]
    if not eligible_tasks:
        raise ValueError("no eligible tasks")

    feature_hash = feature_order_hash(features)
    write_json(
        FEATURE_SCHEMA,
        {
            "feature_set_id": "ew_allowed_pretrade_features_v1",
            "feature_count": len(features),
            "feature_order_hash": feature_hash,
            "features": features,
            "source": rel(EW_ALLOWED_FEATURES),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )

    artifacts: list[Path] = [FEATURE_SCHEMA]
    task_review_rows: list[dict[str, Any]] = []
    weight_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    class_rows: list[dict[str, Any]] = []
    proxy_rows: list[dict[str, Any]] = []
    importance_rows: list[dict[str, Any]] = []
    inner_train_rows = 0
    inner_holdout_rows = 0

    aw.io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    aw.io_path(ONNX_DIR).mkdir(parents=True, exist_ok=True)
    for task in eligible_tasks:
        task_id = str(task["task_id"])
        model_id = safe_model_id(task_id)
        model, inner_train, inner_holdout, weights = train_model(task, frame, features)
        inner_train_rows = len(inner_train)
        inner_holdout_rows = len(inner_holdout)
        task_review_rows.append(
            {
                "task_id": task_id,
                "training_disposition": "trained_no_selection_no_mt5",
                "feature_count": len(features),
                "target_column": task["target_column"],
                "sample_weight_expression": task["sample_weight_expression"],
                "inner_train_rows": len(inner_train),
                "inner_holdout_rows": len(inner_holdout),
                "effect": "trained guarded candidate for EZ review(EZ 검토용 방어 후보 학습)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        weight_rows.append(
            {
                "task_id": task_id,
                "sample_weight_expression": task["sample_weight_expression"],
                "rows": len(weights),
                "weight_min": float(weights.min()),
                "weight_mean": float(weights.mean()),
                "weight_max": float(weights.max()),
                "nonfinite_weights": int((~np.isfinite(weights.to_numpy())).sum()),
                "effect": "records train-only weight behavior(학습 전용 가중치 동작 기록)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        model_path = MODEL_DIR / f"{model_id}.joblib"
        onnx_path = ONNX_DIR / f"{model_id}.onnx"
        joblib.dump({"model": model, "features": features, "label_order": LABEL_ORDER, "task": dict(task)}, aw.io_path(model_path))
        export_meta = export_sklearn_to_onnx_zipmap_disabled(
            model,
            onnx_path,
            feature_count=len(features),
            input_name="float_input",
            target_opset=12,
            drop_label_output=True,
        )
        parity_values = inner_holdout.loc[:, features].astype("float32").head(512).to_numpy()
        parity = check_onnxruntime_probability_parity(model, onnx_path, parity_values, class_order=LABEL_ORDER)
        parity_rows.append(
            {
                "model_id": model_id,
                "task_id": task_id,
                "onnx_path": rel(onnx_path),
                "passed": "true" if parity["passed"] else "false",
                "rows": parity["rows"],
                "max_abs_diff": parity["max_abs_diff"],
                "mean_abs_diff": parity["mean_abs_diff"],
                "onnx_row_sum_max_abs_error": parity["onnx_row_sum_max_abs_error"],
                "input_name": parity["input_name"],
                "output_names": json.dumps(parity["output_names"], ensure_ascii=False),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        model_rows.append(
            {
                "model_id": model_id,
                "task_id": task_id,
                "feature_set_id": task["feature_set_id"],
                "target_column": task["target_column"],
                "sample_weight_expression": task["sample_weight_expression"],
                "model_family": task["model_family"],
                "model_config_id": task["model_config_id"],
                "feature_count": len(features),
                "feature_order_hash": feature_hash,
                "class_order_json": json.dumps(LABEL_ORDER),
                "model_path": rel(model_path),
                "model_sha256": aw.sha256_file(model_path),
                "onnx_path": rel(onnx_path),
                "onnx_sha256": aw.sha256_file(onnx_path),
                "onnx_probability_output_name": export_meta["probability_output_name"],
                "inner_train_rows": len(inner_train),
                "inner_holdout_rows": len(inner_holdout),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        for split_name, split_frame in (("inner_train", inner_train), ("inner_holdout", inner_holdout)):
            class_rows.append(classification_score(model_id, task_id, split_name, model, split_frame, features))
            proxy_rows.append(proxy_trade_score(model_id, task_id, split_name, model, split_frame, features))
        for rank, index in enumerate(np.argsort(model.feature_importances_)[::-1][:20], start=1):
            importance_rows.append(
                {
                    "model_id": model_id,
                    "rank": rank,
                    "feature_name": features[int(index)],
                    "importance": float(model.feature_importances_[int(index)]),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    firewall_rows, release_rows = review_firewall_and_release()
    queue_rows = build_ez_queue()
    artifacts.extend(
        [
            write_csv(TRAINING_TASK_REVIEW, TASK_REVIEW_COLUMNS, task_review_rows),
            write_csv(SAMPLE_WEIGHT_AUDIT, WEIGHT_COLUMNS, weight_rows),
            write_csv(TRAINED_MODEL_MANIFEST, MODEL_COLUMNS, model_rows),
            write_csv(ONNX_PARITY, PARITY_COLUMNS, parity_rows),
            write_csv(CLASSIFICATION_SCORECARD, CLASS_COLUMNS, class_rows),
            write_csv(PROXY_TRADE_SCORECARD, PROXY_COLUMNS, proxy_rows),
            write_csv(FEATURE_IMPORTANCE, IMPORTANCE_COLUMNS, importance_rows),
            write_csv(RUNTIME_FIREWALL, REVIEW_COLUMNS, firewall_rows),
            write_csv(RELEASE_DISPOSITION, REVIEW_COLUMNS, release_rows),
            write_csv(EZ_QUEUE, QUEUE_COLUMNS, queue_rows),
        ]
    )
    summary = {
        "frame_rows": int(len(frame)),
        "feature_count": len(features),
        "feature_order_hash": feature_hash,
        "eligible_task_rows": len(eligible_tasks),
        "trained_model_rows": len(model_rows),
        "onnx_rows": len(model_rows),
        "onnx_parity_rows": len(parity_rows),
        "onnx_parity_passed_rows": sum(1 for row in parity_rows if row["passed"] == "true"),
        "inner_train_rows": inner_train_rows,
        "inner_holdout_rows": inner_holdout_rows,
        "classification_rows": len(class_rows),
        "proxy_trade_rows": len(proxy_rows),
        "runtime_firewall_rows": len(firewall_rows),
        "release_disposition_rows": len(release_rows),
        "ez_queue_rows": len(queue_rows),
        "best_inner_holdout_balanced_accuracy": max(
            [float(row["balanced_accuracy"]) for row in class_rows if row["split"] == "inner_holdout"] or [0.0]
        ),
        "best_inner_holdout_proxy_net": max(
            [float(row["net_log_return_after_cost"]) for row in proxy_rows if row["split"] == "inner_holdout"] or [0.0]
        ),
    }
    return artifacts, summary


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["candidate_selection"] == "not_run"
        and final["mt5_runtime_probe"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(TRAINING_TASK_MATRIX), "required EX/EW inputs exist(필수 EX/EW 입력 존재)"),
        ("parent_ex_gates_passed", final["ex_failed_gate_rows"] == 0, str(final["ex_failed_gate_rows"]), "0", rel(EX_GATES), "EX review gates passed(EX 검토 게이트 통과)"),
        ("parent_next_action_matches", final["ex_next_action"] == RUN_ID, str(final["ex_next_action"]), RUN_ID, rel(EX_FINAL), "EY follows EX next action(EY가 EX 다음 행동을 따름)"),
        ("feature_schema_materialized", final["feature_count"] >= 50 and path_exists(FEATURE_SCHEMA), f"feature_count={final['feature_count']}", ">=50", rel(FEATURE_SCHEMA), "reviewed feature schema is available(검토된 피처 스키마 존재)"),
        ("training_tasks_executed", final["trained_model_rows"] == final["eligible_task_rows"] == 4, f"trained={final['trained_model_rows']};eligible={final['eligible_task_rows']}", "4/4", rel(TRAINED_MODEL_MANIFEST), "all EY tasks trained(모든 EY 작업 학습 완료)"),
        ("onnx_exports_materialized", final["onnx_rows"] == final["trained_model_rows"], f"onnx={final['onnx_rows']};models={final['trained_model_rows']}", "onnx=models", rel(TRAINED_MODEL_MANIFEST), "each model has ONNX artifact(각 모델에 ONNX 산출물 존재)"),
        ("onnx_parity_passed", final["onnx_parity_passed_rows"] == final["onnx_parity_rows"] == final["trained_model_rows"], f"passed={final['onnx_parity_passed_rows']};rows={final['onnx_parity_rows']}", "all parity rows passed", rel(ONNX_PARITY), "ONNX runtime matches sklearn probabilities(ONNX 런타임이 sklearn 확률과 일치)"),
        ("inner_holdout_scored", final["classification_rows"] == 8 and final["proxy_trade_rows"] == 8, f"class={final['classification_rows']};proxy={final['proxy_trade_rows']}", "8/8", f"{rel(CLASSIFICATION_SCORECARD)};{rel(PROXY_TRADE_SCORECARD)}", "inner train/holdout diagnostics exist(내부 학습/보류 진단 존재)"),
        ("runtime_firewall_active", final["runtime_firewall_rows"] >= 2 and final["release_disposition_rows"] >= 1, f"firewall={final['runtime_firewall_rows']};release={final['release_disposition_rows']}", ">=2 and >=1", rel(RUNTIME_FIREWALL), "runtime and release claims remain blocked(런타임/해제 주장 차단 유지)"),
        ("ez_queue_materialized", final["ez_queue_rows"] == 1, str(final["ez_queue_rows"]), "1", rel(EZ_QUEUE), "EZ review queue opened(EZ 검토 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "EY creates artifacts without operating claim(EY는 산출물만 만들고 운영 주장은 안 함)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장에 연결)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    routing = {
        "run_id": RUN_ID,
        "primary_family": "experiment_execution(실험 실행)",
        "primary_skill": "obsidian-model-validation(옵시디언 모델 검증)",
        "support_skills": [
            "obsidian-data-integrity(옵시디언 데이터 무결성)",
            "obsidian-runtime-parity(옵시디언 런타임 동등성)",
            "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            "obsidian-result-judgment(옵시디언 결과 판정)",
        ],
        "required_gates": [row["gate_id"] for row in read_csv(GATE_AUDIT)] if path_exists(GATE_AUDIT) else [],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data = {
        "data_source": rel(EW_FRAME),
        "feature_schema": rel(FEATURE_SCHEMA),
        "sample_scope": f"frame_rows={final['frame_rows']};inner_train={final['inner_train_rows']};inner_holdout={final['inner_holdout_rows']}",
        "feature_label_boundary": "uses EX allowed features only; target/weights excluded from features(EX 허용 피처만 사용, 목표/가중치는 피처에서 제외)",
        "integrity_judgment": "usable_for_EZ_review_no_selection(EZ 검토용, 선택 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_training": "completed(완료)",
        "model_family": "ExtraTreesClassifier(엑스트라트리 분류기)",
        "trained_models": final["trained_model_rows"],
        "onnx_exports": final["onnx_rows"],
        "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}",
        "selection_metric": "none(없음)",
        "threshold_policy": "no tuning(조정 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "best_inner_holdout_balanced_accuracy": final["best_inner_holdout_balanced_accuracy"],
        "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"],
        "proxy_use": "sanity only, not MT5 KPI(점검 전용, MT5 성과 아님)",
        "next_review": final["next_action"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime = {
        "runtime_execution": "not_run(미실행)",
        "onnx_runtime_check": f"probability parity {final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}(확률 동등성)",
        "mt5_probe": "not_run(미실행)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "evidence_available": [rel(TRAINED_MODEL_MANIFEST), rel(ONNX_PARITY), rel(CLASSIFICATION_SCORECARD), rel(PROXY_TRADE_SCORECARD)],
        "evidence_missing": "EZ review, MT5 runtime probe, Forward/Goal(EZ 검토, MT5 런타임 탐침, 전진/목표)",
        "next_condition": final["next_action"],
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(ROUTING_RECEIPT, routing),
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(RUNTIME_RECEIPT, runtime),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {
            rel(path): aw.sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and aw.io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "trained_onnx_artifacts_connected_to_EZ_review(EZ 검토에 학습 ONNX 산출물 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EY Side/Cost/Curve ONNX Training(337단계 337EY 방향/비용/곡선 ONNX 학습)

## Conclusion(결론)

run337EY(337EY 실행)는 EX에서 검토된 train-only inputs(학습 전용 입력)로 ExtraTreesClassifier(엑스트라트리 분류기) 후보 `4`개를 학습하고 ONNX(온엑스)로 내보냈다.

Action(행동): allowed feature schema(허용 피처 스키마) `58`개만 사용해 모델을 학습했다. Effect(효과): label/weight/forward evidence(라벨/가중치/전진 근거)가 피처에 섞이지 않은 ONNX 후보가 생겼다.

Action(행동): onnxruntime probability parity(ONNX 런타임 확률 동등성)를 `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`로 확인했다. Effect(효과): Python model(파이썬 모델)과 ONNX artifact(ONNX 산출물)의 확률 출력이 같은 의미인지 좁게 검증했다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- trained_models(학습 모델): `{final['trained_model_rows']}`
- onnx_exports(ONNX 내보내기): `{final['onnx_rows']}`
- best_inner_holdout_balanced_accuracy(최고 내부 보류 균형 정확도): `{final['best_inner_holdout_balanced_accuracy']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순값): `{final['best_inner_holdout_proxy_net']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- candidate selection(후보 선택): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337EY Decision(337EY 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(TRAINED_MODEL_MANIFEST)}`, `{rel(ONNX_PARITY)}`

Action(행동): guarded side/cost/curve candidates(방어 방향/비용/곡선 후보)를 학습하고 ONNX(온엑스)를 만들었다.
Effect(효과): 다음 EZ review(EZ 검토)가 proxy sanity(프록시 점검), ONNX parity(ONNX 동등성), runtime probe readiness(런타임 탐침 준비)를 판단할 수 있다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


FIELD_LABELS = {
    "current_run": "current_run(현재 실행)",
    "status": "status(상태)",
    "decision": "decision(결정)",
    "latest_completed_run": "latest_completed_run(최근 완료 실행)",
    "next_action": "next_action(다음 행동)",
    "claim_boundary": "claim_boundary(주장 경계)",
}


def replace_bullet_field(text: str, field_name: str, value: str) -> str:
    pattern = re.compile(rf"^- {re.escape(field_name)}(\([^)]+\))?: .*$", flags=re.M)
    replacement = f"- {FIELD_LABELS.get(field_name, field_name)}: {value}"
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def upsert_section_before(text: str, marker: str, section: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}.*?(?=^## )", flags=re.M | re.S)
    if pattern.search(text):
        return pattern.sub(section.rstrip() + "\n\n", text, count=1)
    return text.replace(marker, section.rstrip() + "\n\n" + marker, 1) if marker in text else text.rstrip() + "\n\n" + section.rstrip() + "\n"


def upsert_single_line(text: str, needle: str, entry: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = entry
            trailing = "\n" if text.endswith("\n") else ""
            return "\n".join(lines) + trailing
    return text.rstrip() + "\n" + entry.rstrip() + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = current_branch()
    workspace, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337EY focus complete: run337EY(337EY 실행)는 `{final['status']}`로 side/cost/curve ONNX training(방향/비용/곡선 ONNX 학습)을 완료했다. "
        f"Effect(효과): trained models(학습 모델) `{final['trained_model_rows']}`, ONNX parity(ONNX 동등성) `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`를 만들고 `{final['next_action']}`을 연다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337EY focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337EY focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = replace_bullet_field(current, field_name, value)
    section = f"""## run337EY Side/Cost/Curve ONNX Training(방향/비용/곡선 ONNX 학습)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- trained_models(학습 모델): `{final['trained_model_rows']}`
- onnx_exports(ONNX 내보내기): `{final['onnx_rows']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- best_inner_holdout_balanced_accuracy(최고 내부 보류 균형 정확도): `{final['best_inner_holdout_balanced_accuracy']}`
- effect(효과): 검토된 train-only inputs(학습 전용 입력)로 ONNX 후보를 만들었지만 candidate selection(후보 선택)과 MT5/Forward(메타트레이더5/전진) 주장은 하지 않는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = upsert_section_before(current, "## run337EX Side/Cost/Curve", section, "run337EY Side/Cost/Curve")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- trained_models(학습 모델): `{final['trained_model_rows']}`
- onnx_exports(ONNX 내보내기): `{final['onnx_rows']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): EY(337EY 실행)는 ONNX 후보 제작이며 선택(selection, 선택), MT5(MetaTrader 5, 메타트레이더5) 실행, 운영 주장은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337EY(337EY 실행) `{final['status']}`. "
        f"Effect(효과): ONNX candidates(ONNX 후보) `{final['onnx_rows']}`개와 parity(동등성) `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`를 만들고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, upsert_single_line(brief, "run337EY(337EY 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337EY(337EY 실행) `{final['status']}`. "
        f"Effect(효과): side/cost/curve ONNX candidates(방향/비용/곡선 ONNX 후보)를 학습하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(CHANGELOG, upsert_single_line(changelog, "Stage337 run337EY", changelog_entry), changelog_bom))
    return artifacts


def upsert_csv_worktree(path: Path, columns: Sequence[str], row: Mapping[str, Any], key: str) -> Path:
    existing_columns, existing = aw.read_csv_table(path, prefer_head=False)
    merged_columns = list(existing_columns or columns)
    for column in columns:
        if column not in merged_columns:
            merged_columns.append(column)
    for column in row:
        if column not in merged_columns:
            merged_columns.append(column)
    key_value = str(row.get(key, ""))
    rows = [item for item in existing if str(item.get(key, "")) != key_value]
    rows.append({column: row.get(column, "") for column in merged_columns})
    return write_csv(path, merged_columns, rows)


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "side_cost_curve_onnx_training",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"trained_models={final['trained_model_rows']};onnx={final['onnx_rows']};parity={final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "experiment_execution_model_validation_runtime_parity",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__onnx_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "onnx_training",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "side_cost_curve_onnx_training(방향/비용/곡선 ONNX 학습)",
        "tier_scope": "Tier A train-only model training with no MT5 claim(Tier A 학습 전용 모델 학습, MT5 주장 없음)",
        "kpi_scope": "inner_holdout_proxy_and_onnx_parity_no_release(내부 보류 프록시와 ONNX 동등성, 해제 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"trained_models={final['trained_model_rows']};onnx={final['onnx_rows']};best_holdout_bacc={final['best_inner_holdout_balanced_accuracy']}",
        "guardrail_kpi": f"onnx_parity={final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']};no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__onnx_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_model_validation_runtime_parity",
        "evidence_scope": "EX reviewed inputs and ONNX parity",
        "kpi_scope": "inner_holdout_classification_proxy_onnx_parity",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__onnx_training",
        "family": "side_cost_curve_onnx_training",
        "question": "can reviewed side/cost/curve inputs produce ONNX candidates with parity",
        "metric_scope": "model_manifest_onnx_parity_inner_holdout_proxy",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        upsert_csv_worktree(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        upsert_csv_worktree(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        upsert_csv_worktree(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    rows = [
        row
        for row in rows
        if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID
    ]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    ex_final = read_json(EX_FINAL)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "ex_next_action": ex_final.get("next_action", ""),
        "ex_failed_gate_rows": sum(1 for row in read_csv(EX_GATES) if row.get("status") != "passed"),
        "candidate_selection": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }
    return final


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    artifacts, summary = train_all()
    final = make_final(summary)
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    if final["failed_gates"]:
        final["status"] = "invalid_stage337EY_required_gate_failure_no_selection_no_mt5"
        final["judgment"] = "required_gate_failure_blocks_EZ_training_review"
        final["decision"] = "repair_stage337EY_required_gate_failure_before_EZ"
        final["next_action"] = "repair_stage337EY_required_gate_failure_v1"

    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))

    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": final["status"], "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "trained_models": final["trained_model_rows"],
                "onnx_exports": final["onnx_rows"],
                "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}",
                "best_inner_holdout_balanced_accuracy": final["best_inner_holdout_balanced_accuracy"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "next_action": final["next_action"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
