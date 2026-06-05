from __future__ import annotations

import hashlib
import json
import math
import re
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
from stage_pipelines.stage337 import execute_broker_confirmed_side_cost_curve_mt5_runtime_probe_without_db as fb  # noqa: E402
from stage_pipelines.stage337 import materialize_broker_confirmed_side_cost_curve_runtime_probe_package_without_db as fa  # noqa: E402
from stage_pipelines.stage337 import review_runtime_positive_side_stability_pf_recovery_drawdown_repair_inputs_without_db as fv  # noqa: E402


aw = fv.aw
STATE_OWNER = fv.fu.ft.fs.fq

TODAY = "2026-05-31"
STAGE_ID = fv.STAGE_ID
RUN_NUMBER = "run337FW"
RUN_ID = "run337FW_train_runtime_positive_side_stability_pf_recovery_drawdown_repair_candidates_without_db_v1"
PARENT_RUN_ID = fv.RUN_ID
NEXT_RUN_ID = "run337FX_review_runtime_positive_side_stability_pf_recovery_drawdown_training_without_db_v1"
STATUS = "completed_stage337FW_side_stability_pf_recovery_drawdown_repair_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5"
JUDGMENT = "guarded_side_stability_pf_recovery_drawdown_repair_candidates_trained_with_onnx_parity_review_required_no_selection"
DECISION = "stage337FW_open_run337FX_review_side_stability_pf_recovery_drawdown_training_without_db"
CLAIM_BOUNDARY = (
    "research_development_only_stage337FW_side_stability_pf_recovery_drawdown_repair_training_without_db_"
    "reviewed_train_only_inputs_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = fv.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEWS_DIR = fv.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337FW_side_stability_pf_recovery_drawdown_repair_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337FW_side_stability_pf_recovery_drawdown_repair_training.md"
SELECTED_STATUS = STATE_OWNER.SELECTED_STATUS
STAGE_BRIEF = STATE_OWNER.STAGE_BRIEF
WORKSPACE_STATE = STATE_OWNER.WORKSPACE_STATE
CURRENT_STATE = STATE_OWNER.CURRENT_STATE
CHANGELOG = STATE_OWNER.CHANGELOG
RUN_REGISTRY = STATE_OWNER.RUN_REGISTRY
ALPHA_LEDGER = STATE_OWNER.ALPHA_LEDGER
ARTIFACT_REGISTRY = STATE_OWNER.ARTIFACT_REGISTRY
STAGE_LEDGER = STATE_OWNER.STAGE_LEDGER

FV_FINAL = fv.FINAL_DECISION
FV_GATES = fv.GATE_AUDIT
FV_QUEUE = fv.FW_QUEUE
FV_INPUT_REVIEW = fv.INPUT_REVIEW
FV_WEIGHT_REVIEW = fv.WEIGHT_REVIEW
TASK_ELIGIBILITY = fv.TASK_ELIGIBILITY
FV_NEGATIVE = fv.NEGATIVE_CONTROL_REVIEW
FU_FRAME = fv.FU_FRAME
FU_ALLOWED_FEATURES = fv.FU_ALLOWED_FEATURES
FU_WEIGHT_AUDIT = fv.FU_WEIGHT_AUDIT
FU_FEATURE_BOUNDARY = fv.FU_FEATURE_BOUNDARY

FEATURE_SCHEMA = RUN_DIR / "fw_allowed_feature_schema.json"
TRAINING_TASK_REVIEW = RUN_DIR / "fw_training_task_review.csv"
SAMPLE_WEIGHT_AUDIT = RUN_DIR / "sample_weight_audit.csv"
TRAINED_MODEL_MANIFEST = RUN_DIR / "trained_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "onnx_parity_matrix.csv"
CLASSIFICATION_SCORECARD = RUN_DIR / "inner_holdout_classification_scorecard.csv"
PROXY_TRADE_SCORECARD = RUN_DIR / "inner_holdout_proxy_trade_scorecard.csv"
FEATURE_IMPORTANCE = RUN_DIR / "feature_importance_top20.csv"
RUNTIME_FIREWALL = RUN_DIR / "runtime_firewall_review.csv"
RELEASE_DISPOSITION = RUN_DIR / "training_release_disposition.csv"
FX_QUEUE = RUN_DIR / "run337FX_review_queue.csv"
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
    FV_FINAL,
    FV_GATES,
    FV_QUEUE,
    FV_INPUT_REVIEW,
    FV_WEIGHT_REVIEW,
    TASK_ELIGIBILITY,
    FV_NEGATIVE,
    FU_FRAME,
    FU_ALLOWED_FEATURES,
    FU_WEIGHT_AUDIT,
    FU_FEATURE_BOUNDARY,
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
    FX_QUEUE,
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
    RUN_REGISTRY,
    ALPHA_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)

LABEL_ORDER = [0, 1, 2]
INT_TO_LABEL = {0: "short", 1: "flat", 2: "long"}
FEATURE_SET_ID = "fu_allowed_pretrade_features_v1"

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
IMPORTANCE_COLUMNS = ("model_id", "rank", "feature_name", "importance", "claim_boundary")
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
GATE_COLUMNS = ("gate_id", "status", "evidence_path", "observed", "expected", "effect", "claim_boundary")


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
    rows = read_csv(FU_ALLOWED_FEATURES)
    features = [row.get("feature_name") or row.get("feature") or "" for row in rows]
    return [feature for feature in features if feature]


def safe_model_id(task_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", task_id).strip("_")
    return f"fw_{cleaned}"


def split_inner(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    row_ids = pd.to_numeric(frame["source_row_id"], errors="coerce").dropna().astype(int)
    unique_ids = sorted(row_ids.unique().tolist())
    cutoff_index = max(1, int(len(unique_ids) * 0.80))
    cutoff = unique_ids[cutoff_index - 1]
    source_ids = pd.to_numeric(frame["source_row_id"], errors="coerce").astype(int)
    inner_train = frame[source_ids <= cutoff].copy()
    inner_holdout = frame[source_ids > cutoff].copy()
    return inner_train, inner_holdout


def sample_weights(frame: pd.DataFrame, expression: str) -> pd.Series:
    parts = [part.strip() for part in expression.split("*") if part.strip()]
    weight = pd.Series(np.ones(len(frame), dtype="float64"), index=frame.index)
    for part in parts:
        if part not in frame.columns:
            raise ValueError(f"missing sample weight column {part}")
        weight = weight * pd.to_numeric(frame[part], errors="coerce").fillna(1.0)
    return weight.replace([np.inf, -np.inf], np.nan).fillna(1.0).clip(lower=0.10, upper=10.0)


def train_model(task: Mapping[str, str], frame: pd.DataFrame, features: Sequence[str]) -> tuple[Any, pd.DataFrame, pd.DataFrame, pd.Series]:
    inner_train, inner_holdout = split_inner(frame)
    target = str(task["target_column"])
    weights = sample_weights(inner_train, str(task["sample_weight_expression"]))
    model = ExtraTreesClassifier(
        n_estimators=160,
        max_depth=8,
        min_samples_leaf=120,
        class_weight=None,
        random_state=33741,
        n_jobs=-1,
    )
    x_values = inner_train.loc[:, features].astype("float32").to_numpy()
    y_values = pd.to_numeric(inner_train[target], errors="raise").astype(int).to_numpy()
    model.fit(x_values, y_values, sample_weight=weights.to_numpy(dtype="float64"))
    return model, inner_train, inner_holdout, weights


def probability_and_pred(model: Any, frame: pd.DataFrame, features: Sequence[str]) -> tuple[np.ndarray, np.ndarray]:
    values = frame.loc[:, features].astype("float32").to_numpy()
    probabilities = ordered_sklearn_probabilities(model, values, LABEL_ORDER)
    pred = np.asarray(LABEL_ORDER, dtype=int)[np.argmax(probabilities, axis=1)]
    return probabilities, pred


def label_counts(values: np.ndarray) -> str:
    return json.dumps({INT_TO_LABEL[int(k)]: int(v) for k, v in zip(*np.unique(values, return_counts=True))}, ensure_ascii=False, sort_keys=True)


def classification_score(model_id: str, task_id: str, split: str, model: Any, frame: pd.DataFrame, features: Sequence[str]) -> dict[str, Any]:
    probs, pred = probability_and_pred(model, frame, features)
    y_values = pd.to_numeric(frame["label_class"], errors="raise").astype(int).to_numpy()
    return {
        "model_id": model_id,
        "task_id": task_id,
        "split": split,
        "rows": int(len(frame)),
        "accuracy": float(accuracy_score(y_values, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_values, pred)),
        "macro_f1": float(f1_score(y_values, pred, average="macro")),
        "log_loss": float(log_loss(y_values, probs, labels=LABEL_ORDER)),
        "pred_counts_json": label_counts(pred),
        "true_counts_json": label_counts(y_values),
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
        "allowed_use": "signal sanity only(신호 점검 전용)",
        "forbidden_use": "MT5 KPI, Forward Passed/Failed, candidate selection(MT5 핵심 성과 지표, 전진 통과/실패, 후보 선택)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def review_firewall_and_release(model_rows: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    firewall_rows = [
        {
            "review_id": "no_candidate_selection",
            "subject": "candidate selection firewall(후보 선택 방화벽)",
            "rows": model_rows,
            "metric_1": "selection=not_run",
            "metric_2": "rank review deferred to FX(FX로 순위 검토 지연)",
            "review_status": "active",
            "allowed_use": "FX review queue only(FX 검토 대기열 전용)",
            "forbidden_use": "promotion or selected model(승격 또는 선택 모델)",
            "effect": "prevents proxy-only selection(프록시만 보고 선택하는 일을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "no_mt5_or_forward_claim",
            "subject": "MT5/Forward firewall(MT5/전진 방화벽)",
            "rows": model_rows,
            "metric_1": "mt5=not_run",
            "metric_2": "forward=not_claimed",
            "review_status": "active",
            "allowed_use": "future runtime probe planning(향후 런타임 탐침 계획)",
            "forbidden_use": "Forward Passed/Failed or runtime authority(전진 통과/실패 또는 런타임 권위)",
            "effect": "keeps ONNX training separate from operating evidence(ONNX 학습과 운영 근거를 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "no_threshold_or_lot_tuning",
            "subject": "threshold and lot firewall(임계값과 랏 방화벽)",
            "rows": model_rows,
            "metric_1": "threshold_tuning=not_run",
            "metric_2": "lot_optimization=not_run",
            "review_status": "active",
            "allowed_use": "fixed argmax review only(고정 argmax 검토 전용)",
            "forbidden_use": "in-sample threshold or lot optimization(표본 내부 임계값 또는 랏 최적화)",
            "effect": "reduces overfit path before FX review(FX 검토 전 과적합 경로를 줄임)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    release_rows = [
        {
            "review_id": "training_release_disposition",
            "subject": "training release disposition(학습 해제 처분)",
            "rows": model_rows,
            "metric_1": "review_required",
            "metric_2": NEXT_RUN_ID,
            "review_status": "no_release_review_required",
            "allowed_use": "FX training review(FX 학습 검토)",
            "forbidden_use": "selected candidate or live readiness(선택 후보 또는 실거래 준비)",
            "effect": "moves trained ONNX artifacts to review, not operation(학습 ONNX 산출물을 운영이 아니라 검토로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return firewall_rows, release_rows


def build_fx_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "fx001_review_side_stability_pf_recovery_drawdown_training",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review five trained side-stability repair ONNX candidates and decide runtime probe package(학습된 방향 안정 수리 ONNX 후보 5개를 검토하고 런타임 탐침 패키지를 결정)",
            "required_inputs": f"{rel(TRAINED_MODEL_MANIFEST)};{rel(ONNX_PARITY)};{rel(CLASSIFICATION_SCORECARD)};{rel(PROXY_TRADE_SCORECARD)}",
            "required_outputs": "training review scorecard, runtime probe package decision(학습 검토 점수표, 런타임 탐침 패키지 결정)",
            "blocked_if_missing": "model manifest or ONNX parity(모델 목록 또는 ONNX 동등성)",
            "forbidden_action": "MT5/Forward/Goal claim without runtime probe(런타임 탐침 없는 MT5/전진/목표 주장)",
            "effect": "separates model creation from candidate judgment(모델 생성과 후보 판정을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def eligible_task_rows() -> list[dict[str, str]]:
    rows = read_csv(TASK_ELIGIBILITY)
    return [row for row in rows if str(row.get("eligibility_status", "")).startswith("eligible_for_guarded_training")]


def train_all() -> tuple[list[Path], dict[str, Any]]:
    frame = pd.read_parquet(aw.io_path(FU_FRAME)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame.sort_values(["source_row_id", "cost_policy_id"], inplace=True)
    features = read_features()
    missing_features = [feature for feature in features if feature not in frame.columns]
    if missing_features:
        raise ValueError(f"missing features: {missing_features}")
    tasks = eligible_task_rows()
    if not tasks:
        raise ValueError("no eligible tasks")
    for task in tasks:
        for column in (task.get("target_column", ""), task.get("sample_weight_expression", "")):
            if column and column not in frame.columns:
                raise ValueError(f"task {task.get('task_id')} references missing column {column}")

    feature_hash = feature_order_hash(features)
    write_json(
        FEATURE_SCHEMA,
        {
            "feature_set_id": FEATURE_SET_ID,
            "feature_count": len(features),
            "feature_order_hash": feature_hash,
            "features": features,
            "source": rel(FU_ALLOWED_FEATURES),
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
    for task in tasks:
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
                "effect": "trained guarded candidate for FX review(FX 검토용 방어 후보 학습)",
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
                "effect": "records train-only sample weight behavior(학습 전용 표본 가중치 동작 기록)",
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
                "feature_set_id": FEATURE_SET_ID,
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

    firewall_rows, release_rows = review_firewall_and_release(len(model_rows))
    queue_rows = build_fx_queue()
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
            write_csv(FX_QUEUE, QUEUE_COLUMNS, queue_rows),
        ]
    )
    summary = {
        "frame_rows": int(len(frame)),
        "feature_count": len(features),
        "feature_order_hash": feature_hash,
        "eligible_task_rows": len(tasks),
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
        "fx_queue_rows": len(queue_rows),
        "best_inner_holdout_balanced_accuracy": max([float(row["balanced_accuracy"]) for row in class_rows if row["split"] == "inner_holdout"] or [0.0]),
        "best_inner_holdout_proxy_net": max([float(row["net_log_return_after_cost"]) for row in proxy_rows if row["split"] == "inner_holdout"] or [0.0]),
    }
    return artifacts, summary


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    fv_final = read_json(FV_FINAL)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "fv_next_action": fv_final.get("next_action", ""),
        "fv_failed_gate_rows": sum(1 for row in read_csv(FV_GATES) if row.get("status") != "passed"),
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["candidate_selection"] == "not_run"
        and final["mt5_runtime_probe"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(TASK_ELIGIBILITY), "required FV/FU inputs exist(필수 FV/FU 입력 존재)"),
        ("parent_fv_gates_passed", final["fv_failed_gate_rows"] == 0, str(final["fv_failed_gate_rows"]), "0", rel(FV_GATES), "FV review gates passed(FV 검토 게이트 통과)"),
        ("parent_next_action_matches", final["fv_next_action"] == RUN_ID, str(final["fv_next_action"]), RUN_ID, rel(FV_FINAL), "FW follows FV next action(FW가 FV 다음 행동을 따름)"),
        ("feature_schema_materialized", final["feature_count"] == 58 and path_exists(FEATURE_SCHEMA), f"feature_count={final['feature_count']}", "58", rel(FEATURE_SCHEMA), "reviewed feature schema is available(검토된 피처 스키마 존재)"),
        ("training_tasks_executed", final["trained_model_rows"] == final["eligible_task_rows"] == 5, f"trained={final['trained_model_rows']};eligible={final['eligible_task_rows']}", "5/5", rel(TRAINED_MODEL_MANIFEST), "all FW tasks trained(모든 FW 작업 학습 완료)"),
        ("onnx_exports_materialized", final["onnx_rows"] == final["trained_model_rows"], f"onnx={final['onnx_rows']};models={final['trained_model_rows']}", "onnx=models", rel(TRAINED_MODEL_MANIFEST), "each model has ONNX artifact(각 모델 ONNX 산출물 존재)"),
        ("onnx_parity_passed", final["onnx_parity_passed_rows"] == final["onnx_parity_rows"] == final["trained_model_rows"], f"passed={final['onnx_parity_passed_rows']};rows={final['onnx_parity_rows']}", "all parity rows passed", rel(ONNX_PARITY), "ONNX runtime matches sklearn probabilities(ONNX 런타임이 sklearn 확률과 일치)"),
        ("inner_holdout_scored", final["classification_rows"] == 10 and final["proxy_trade_rows"] == 10, f"class={final['classification_rows']};proxy={final['proxy_trade_rows']}", "10/10", f"{rel(CLASSIFICATION_SCORECARD)};{rel(PROXY_TRADE_SCORECARD)}", "inner train/holdout diagnostics exist(내부 학습/보류 진단 존재)"),
        ("runtime_firewall_active", final["runtime_firewall_rows"] >= 3 and final["release_disposition_rows"] >= 1, f"firewall={final['runtime_firewall_rows']};release={final['release_disposition_rows']}", ">=3 and >=1", rel(RUNTIME_FIREWALL), "runtime and release claims remain blocked(런타임과 해제 주장을 차단 유지)"),
        ("fx_queue_materialized", final["fx_queue_rows"] == 1, str(final["fx_queue_rows"]), "1", rel(FX_QUEUE), "FX review queue opened(FX 검토 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "FW creates artifacts without operating claim(FW는 산출물만 만들고 운영 주장은 하지 않음)"),
        ("required_gate_coverage_audit", True, "all required gates listed(모든 필수 게이트 열거)", "present", rel(GATE_AUDIT), "completion claim tied to gates(완료 주장을 게이트에 연결)"),
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
    data = {
        "data_source": rel(FU_FRAME),
        "feature_schema": rel(FEATURE_SCHEMA),
        "time_axis": "timestamp is UTC closed-bar train-only order(timestamp는 UTC 확정봉 학습 전용 순서)",
        "sample_scope": f"frame_rows={final['frame_rows']};inner_train={final['inner_train_rows']};inner_holdout={final['inner_holdout_rows']}",
        "feature_label_boundary": "uses FU reviewed features only; targets and FT weights excluded from model features(FU 검토 피처만 사용, 목표와 FT 가중치는 모델 피처에서 제외)",
        "split_boundary": "source_row_id ordered 80/20 inner split, no forward claim(source_row_id 순서 80/20 내부 분할, 전진 주장 없음)",
        "leakage_risk": "proxy labels and weights exist in frame but not feature schema(프록시 라벨과 가중치는 프레임에 있지만 피처 스키마에는 없음)",
        "data_hash_or_identity": aw.sha256_file(FU_FRAME) if path_exists(FU_FRAME) else "",
        "integrity_judgment": "usable_for_FX_review_no_selection(FX 검토용 사용 가능, 선택 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_training": "completed(완료)",
        "model_family": "ExtraTreesClassifier(엑스트라트리스 분류기)",
        "target_and_label": "label_class with five FT sample-weight expressions(label_class와 FT 표본 가중치 표현 5개)",
        "split_method": "inner holdout only, no WFO or MT5 yet(내부 보류만, WFO 또는 MT5 아직 없음)",
        "selection_metric": "none(없음)",
        "threshold_policy": "fixed argmax, no tuning(고정 argmax, 조정 없음)",
        "trained_models": final["trained_model_rows"],
        "onnx_exports": final["onnx_rows"],
        "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}",
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "observed_change": "five FT repair weighted ONNX candidates trained(FT 수리 가중 ONNX 후보 5개 학습)",
        "comparison_baseline": "FV eligible input review(FV 적격 입력 검토)",
        "best_inner_holdout_balanced_accuracy": final["best_inner_holdout_balanced_accuracy"],
        "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"],
        "segment_checks": "train/holdout, direction counts, proxy trade shape(학습/보류, 방향 수, 프록시 거래 형태)",
        "proxy_use": "sanity only, not MT5 KPI(점검 전용, MT5 핵심 성과 지표 아님)",
        "attribution_confidence": "low_until_FX_and_MT5_review(FX와 MT5 검토 전까지 낮음)",
        "next_probe": final["next_action"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime = {
        "runtime_execution": "not_run(실행 안 함)",
        "onnx_runtime_check": f"probability parity {final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}(확률 동등성)",
        "mt5_probe": "not_run(실행 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "evidence_available": [rel(TRAINED_MODEL_MANIFEST), rel(ONNX_PARITY), rel(CLASSIFICATION_SCORECARD), rel(PROXY_TRADE_SCORECARD)],
        "evidence_missing": "FX review, MT5 runtime probe, Forward/Goal(FX 검토, MT5 런타임 탐침, 전진/목표)",
        "next_condition": final["next_action"],
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
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
        "availability": "generated_with_manifest(목록과 함께 생성)",
        "lineage_judgment": "trained_onnx_artifacts_connected_to_FX_review(FX 검토에 학습 ONNX 산출물 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337FW Runtime Positive Clue Blend ONNX Training(337단계 337FW 런타임 긍정 단서 혼합 ONNX 학습)

## Conclusion(결론)

Action(행동): FV reviewed train-only inputs(FV 검토 학습 전용 입력)로 ExtraTreesClassifier(엑스트라트리스 분류기) 후보 `5`개를 학습하고 ONNX(온엑스)로 내보냈다. Effect(효과): 다음 FX review(FX 검토)가 실제 모델 산출물, ONNX parity(ONNX 동등성), proxy score(프록시 점수)를 검토할 수 있다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- trained_models(학습 모델): `{final['trained_model_rows']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- best_inner_holdout_balanced_accuracy(최고 내부 보류 균형 정확도): `{final['best_inner_holdout_balanced_accuracy']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Boundary(경계): FW(337FW 실행)는 training and ONNX materialization(학습과 ONNX 물질화)만 했다. MT5 execution(MT5 실행), candidate selection(후보 선택), Forward/Goal(전진/목표), runtime authority(런타임 권위)는 모두 `not_claimed`다.

Next action(다음 행동): `{final['next_action']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337FW Decision(337FW 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(TRAINED_MODEL_MANIFEST)}`, `{rel(ONNX_PARITY)}`, `{rel(PROXY_TRADE_SCORECARD)}`

Action(행동): 5개 guarded ONNX candidates(방어 ONNX 후보)를 만들었다.
Effect(효과): FX review(FX 검토) 전까지 후보 선택이나 운영 승격은 닫힌 상태로 유지한다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {fa.ey.current_branch()}")
    focus = (
        "- >-\n"
        f"  Stage337 run337FW focus complete: run337FW(337FW 실행)는 `{final['status']}`로 guarded ONNX training(방어 ONNX 학습)을 완료했다. "
        f"Effect(효과): trained models(학습 모델) `{final['trained_model_rows']}`, ONNX parity(ONNX 동등성) `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337FW focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337FW focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
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
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337FW Runtime Positive Clue Blend ONNX Training(런타임 긍정 단서 혼합 ONNX 학습)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- trained_models(학습 모델): `{final['trained_model_rows']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): FV 검토를 통과한 5개 작업을 ONNX 후보로 만들고 FX review(FX 검토)를 열었다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337FV Input Review", section, "run337FW Runtime Positive Clue Blend ONNX Training")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- trained_models(학습 모델): `{final['trained_model_rows']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): FW(337FW 실행)는 training(학습)과 ONNX materialization(ONNX 물질화)만 완료했고 MT5 execution(MT5 실행), operating selection(운영 선택)은 하지 않았다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_entry = f"- {TODAY}: run337FW(337FW 실행) `{final['status']}`. Effect(효과): 5개 guarded ONNX candidates(방어 ONNX 후보)를 학습하고 ONNX parity(ONNX 동등성) `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`를 확인해 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, fb.upsert_single_line(brief, "run337FW(337FW 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337FW(337FW 실행) `{final['status']}`. Effect(효과): side-stability PF/recovery/drawdown repair(방향 안정 PF/회복/낙폭 수리) ONNX 후보 5개를 만들고 FX review(FX 검토)를 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    artifacts.append(aw.write_text_lossless(CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337FW", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "side_stability_pf_recovery_drawdown_repair_onnx_training",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"trained={final['trained_model_rows']};onnx_parity={final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "experiment_execution_model_validation_runtime_parity",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__onnx_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "onnx_training",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "side_stability_pf_recovery_drawdown_repair_onnx_training(방향 안정 PF/회복/낙폭 수리 ONNX 학습)",
        "tier_scope": "Tier A train-only model training; Tier B out_of_scope_by_claim(Tier A 학습 전용 모델 학습, Tier B 주장 범위 밖)",
        "kpi_scope": "inner_holdout_proxy_and_onnx_parity_no_release(내부 보류 프록시와 ONNX 동등성, 해제 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"trained_models={final['trained_model_rows']};best_proxy={final['best_inner_holdout_proxy_net']}",
        "guardrail_kpi": "onnx_parity;no_selection;no_mt5;no_forward",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__onnx_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_model_validation_runtime_parity",
        "evidence_scope": "FV reviewed inputs and FU train-only frame",
        "kpi_scope": "inner_holdout_proxy_no_mt5",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__onnx_training",
        "family": "side_stability_pf_recovery_drawdown_repair_training",
        "question": "do FT blend/PF/recovery/drawdown weights produce reviewable ONNX candidates",
        "metric_scope": "onnx_parity_inner_holdout_proxy",
        "primary_artifact": rel(TRAINED_MODEL_MANIFEST),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID]
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
        row = {
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
        rows.append({column: row.get(column, "") for column in columns})
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


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
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
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

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "trained_model_rows": final["trained_model_rows"],
                "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}",
                "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"],
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
