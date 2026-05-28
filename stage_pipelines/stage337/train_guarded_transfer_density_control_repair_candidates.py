from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import (  # noqa: E402
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage337 import review_transfer_density_control_objective_repair_inputs as dy  # noqa: E402
from stage_pipelines.stage337 import train_guarded_prediction_surface_validation_edge_repair_candidates as do  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    replace_bullet_value,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
)


TODAY = "2026-05-28"
STAGE_ID = dy.STAGE_ID
RUN_NUMBER = "run337DZ"
RUN_ID = "run337DZ_train_guarded_transfer_density_control_repair_candidates_without_db_v1"
PARENT_RUN_ID = dy.RUN_ID
NEXT_RUN_ID = "run337EA_review_guarded_transfer_density_control_training_without_db_v1"
STATUS = "completed_stage337DZ_guarded_transfer_density_control_repair_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5"
JUDGMENT = "guarded_auxiliary_weighted_candidates_trained_onnx_parity_review_required_no_selection"
DECISION = "stage337DZ_open_run337EA_review_guarded_transfer_density_control_training"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DZ_guarded_transfer_density_control_training_without_db_"
    "train_only_auxiliary_weights_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = dy.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEWS_DIR = dy.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337DZ_guarded_transfer_density_control_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DZ_guarded_transfer_density_control_training.md"
SELECTED_STATUS = dy.SELECTED_STATUS
STAGE_BRIEF = dy.STAGE_BRIEF
WORKSPACE_STATE = dy.WORKSPACE_STATE
CURRENT_STATE = dy.CURRENT_STATE
CHANGELOG = dy.CHANGELOG
RUN_REGISTRY = dy.RUN_REGISTRY
ALPHA_LEDGER = dy.ALPHA_LEDGER
ARTIFACT_REGISTRY = dy.ARTIFACT_REGISTRY
STAGE_LEDGER = dy.STAGE_LEDGER

DY_FINAL = dy.FINAL_DECISION
DY_GATES = dy.REQUIRED_GATE_AUDIT
DY_QUEUE = dy.DZ_QUEUE
OBJECTIVE_FRAME = dy.OBJECTIVE_FRAME
TRAINING_ELIGIBILITY_MATRIX = dy.TRAINING_ELIGIBILITY_MATRIX
DENSITY_INPUT_REVIEW = dy.DENSITY_INPUT_REVIEW
CONTROL_INPUT_REVIEW = dy.CONTROL_INPUT_REVIEW
WFO_INPUT_REVIEW = dy.WFO_INPUT_REVIEW
FIREWALL_REVIEW = dy.FIREWALL_REVIEW
SOURCE_MODEL_INPUT = do.SOURCE_MODEL_INPUT
FEATURE_SET_MATRIX = do.FEATURE_SET_MATRIX
VALIDATION_EDGE_FRAME = do.VALIDATION_EDGE_FRAME

TASK_MATRIX = RUN_DIR / "guarded_transfer_density_training_task_matrix.csv"
FEATURE_COMPATIBILITY = RUN_DIR / "feature_input_compatibility.csv"
AUXILIARY_TAG_SUMMARY = RUN_DIR / "auxiliary_tag_summary.csv"
SAMPLE_WEIGHT_AUDIT = RUN_DIR / "sample_weight_audit.csv"
TRAINED_MODEL_MANIFEST = RUN_DIR / "trained_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "onnx_parity_matrix.csv"
CANDIDATE_SCORECARD = RUN_DIR / "candidate_classification_scorecard.csv"
PROXY_TRADE_SCORECARD = RUN_DIR / "proxy_trade_scorecard.csv"
NEGATIVE_CONTROL_SCORECARD = RUN_DIR / "negative_control_scorecard.csv"
DENSITY_GUARD_AUDIT = RUN_DIR / "density_guard_audit.csv"
SPLIT_GUARD_AUDIT = RUN_DIR / "split_guard_audit.csv"
RUNTIME_FIREWALL_REVIEW = RUN_DIR / "runtime_firewall_review.csv"
RELEASE_DISPOSITION = RUN_DIR / "training_release_disposition.csv"
EA_QUEUE = RUN_DIR / "run337EA_review_queue.csv"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DY_FINAL,
    DY_GATES,
    DY_QUEUE,
    OBJECTIVE_FRAME,
    TRAINING_ELIGIBILITY_MATRIX,
    DENSITY_INPUT_REVIEW,
    CONTROL_INPUT_REVIEW,
    WFO_INPUT_REVIEW,
    FIREWALL_REVIEW,
    SOURCE_MODEL_INPUT,
    FEATURE_SET_MATRIX,
    VALIDATION_EDGE_FRAME,
)
OUTPUT_FILES = (
    TASK_MATRIX,
    FEATURE_COMPATIBILITY,
    AUXILIARY_TAG_SUMMARY,
    SAMPLE_WEIGHT_AUDIT,
    TRAINED_MODEL_MANIFEST,
    ONNX_PARITY,
    CANDIDATE_SCORECARD,
    PROXY_TRADE_SCORECARD,
    NEGATIVE_CONTROL_SCORECARD,
    DENSITY_GUARD_AUDIT,
    SPLIT_GUARD_AUDIT,
    RUNTIME_FIREWALL_REVIEW,
    RELEASE_DISPOSITION,
    EA_QUEUE,
    MODEL_RECEIPT,
    DATA_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    REQUIRED_GATE_AUDIT,
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
LABEL_TO_INT = {value: key for key, value in INT_TO_LABEL.items()}
MODEL_SPECS = (
    {"model_config_id": "logreg_balanced_c050", "family": "logistic_regression(로지스틱 회귀)"},
    {"model_config_id": "extratrees_depth6_leaf120", "family": "extra_trees(엑스트라 트리)"},
)
WEIGHT_POLICIES = (
    {
        "weight_policy_id": "low_margin_focus",
        "description": "train-only low-margin trade focus(학습 전용 낮은 여백 거래 집중)",
        "low_margin": 1.50,
        "direction": 0.25,
        "drawdown": 0.20,
        "abstention": 0.10,
    },
    {
        "weight_policy_id": "direction_residual_focus",
        "description": "train-only direction residual focus(학습 전용 방향 잔차 집중)",
        "low_margin": 0.25,
        "direction": 1.50,
        "drawdown": 0.20,
        "abstention": 0.10,
    },
    {
        "weight_policy_id": "balanced_transfer_density_control",
        "description": "balanced transfer density control focus(균형 전이/밀도/대조 집중)",
        "low_margin": 0.85,
        "direction": 0.85,
        "drawdown": 0.25,
        "abstention": 0.20,
    },
)

TASK_COLUMNS = (
    "task_id",
    "target_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "weight_policy_id",
    "feature_count",
    "train_rows",
    "training_disposition",
    "claim_boundary",
)
FEATURE_COMPAT_COLUMNS = (
    "feature_set_id",
    "feature_count",
    "missing_count",
    "missing_features",
    "nonfinite_rows",
    "feature_order_hash",
    "claim_boundary",
)
AUX_COLUMNS = (
    "cost_policy_id",
    "source_rows",
    "low_margin_rate_mean",
    "direction_residual_rate_mean",
    "underwater_rate_mean",
    "drawdown_pressure_mean",
    "abstention_rate_mean",
    "allowed_use",
    "forbidden_use",
    "claim_boundary",
)
WEIGHT_AUDIT_COLUMNS = (
    "cost_policy_id",
    "weight_policy_id",
    "train_rows",
    "weight_min",
    "weight_mean",
    "weight_max",
    "low_margin_component_mean",
    "direction_component_mean",
    "drawdown_component_mean",
    "abstention_component_mean",
    "claim_boundary",
)
MODEL_COLUMNS = (
    "model_id",
    "task_id",
    "target_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "weight_policy_id",
    "feature_count",
    "feature_order_hash",
    "class_order_json",
    "model_path",
    "model_sha256",
    "onnx_path",
    "onnx_sha256",
    "onnx_probability_output_name",
    "train_rows",
    "validation_rows",
    "oos_rows",
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
CLASS_SCORE_COLUMNS = (
    "model_id",
    "task_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "weight_policy_id",
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
TRADE_SCORE_COLUMNS = (
    "model_id",
    "task_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "weight_policy_id",
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
    "claim_boundary",
)
CONTROL_COLUMNS = (
    "model_id",
    "task_id",
    "control_id",
    "split",
    "rows",
    "candidate_balanced_accuracy",
    "control_alignment_balanced_accuracy",
    "blocks_training_review",
    "effect",
    "claim_boundary",
)
DENSITY_COLUMNS = (
    "model_id",
    "task_id",
    "split",
    "train_signal_density",
    "split_signal_density",
    "density_gap_vs_train",
    "density_pressure_flag",
    "trade_count",
    "effect",
    "claim_boundary",
)
SPLIT_GUARD_COLUMNS = (
    "guard_id",
    "source",
    "status",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)
RUNTIME_COLUMNS = ("firewall_id", "held_action", "carry_status", "review_status", "effect", "claim_boundary")
RELEASE_COLUMNS = (
    "model_id",
    "task_id",
    "validation_pf",
    "oos_pf",
    "validation_balanced_accuracy",
    "validation_trade_count",
    "control_block_rows",
    "density_pressure_rows",
    "release_disposition",
    "release_blockers",
    "next_condition",
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
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def feature_order_hash(features: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(str(item) for item in features).encode("utf-8")).hexdigest()


def parse_json_list(value: str) -> list[str]:
    return [str(item) for item in json.loads(value)]


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def build_model(config_id: str) -> Any:
    if config_id == "logreg_balanced_c050":
        return Pipeline(
            [
                ("scale", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        C=0.50,
                        class_weight="balanced",
                        max_iter=600,
                        solver="lbfgs",
                        random_state=337,
                    ),
                ),
            ]
        )
    if config_id == "extratrees_depth6_leaf120":
        return ExtraTreesClassifier(
            n_estimators=96,
            max_depth=6,
            min_samples_leaf=120,
            class_weight="balanced",
            random_state=337,
            n_jobs=-1,
        )
    raise ValueError(f"Unknown model config: {config_id}")


def fit_weighted_model(model: Any, x_train: np.ndarray, y_train: np.ndarray, sample_weight: np.ndarray) -> Any:
    if isinstance(model, Pipeline):
        model.fit(x_train, y_train, model__sample_weight=sample_weight)
    else:
        model.fit(x_train, y_train, sample_weight=sample_weight)
    return model


def read_source_frame() -> pd.DataFrame:
    source = pd.read_parquet(io_path(SOURCE_MODEL_INPUT)).copy()
    source["timestamp"] = pd.to_datetime(source["timestamp"], utc=True)
    source = source.sort_values("timestamp").reset_index(drop=True)
    source["source_row_id"] = np.arange(len(source), dtype=np.int64)
    return source


def read_feature_sets(source: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    feature_sets: list[dict[str, Any]] = []
    compat_rows: list[dict[str, Any]] = []
    for row in read_csv(FEATURE_SET_MATRIX):
        features = parse_json_list(row["included_features_json"])
        missing = [feature for feature in features if feature not in source.columns]
        nonfinite_rows = 0
        if not missing:
            nonfinite_rows = int(source.loc[:, features].replace([np.inf, -np.inf], np.nan).isna().any(axis=1).sum())
        order_hash = feature_order_hash(features)
        feature_sets.append(
            {
                "feature_set_id": row["feature_set_id"],
                "features": features,
                "missing": missing,
                "feature_order_hash": order_hash,
                "nonfinite_rows": nonfinite_rows,
            }
        )
        compat_rows.append(
            {
                "feature_set_id": row["feature_set_id"],
                "feature_count": len(features),
                "missing_count": len(missing),
                "missing_features": json.dumps(missing, ensure_ascii=False),
                "nonfinite_rows": nonfinite_rows,
                "feature_order_hash": order_hash,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return feature_sets, compat_rows


def read_targets() -> list[dict[str, Any]]:
    _, targets = do.read_targets()
    return targets


def drawdown_normalized(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce").fillna(0.0).clip(lower=0.0)
    scale = float(numeric.quantile(0.95)) if len(numeric) else 0.0
    if scale <= 0:
        return numeric * 0.0
    return (numeric / scale).clip(lower=0.0, upper=1.0)


def build_auxiliary_tables(source: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    frame = pd.read_parquet(io_path(OBJECTIVE_FRAME)).copy()
    if sorted(frame["split"].astype(str).unique().tolist()) != ["train"]:
        raise ValueError("OBJECTIVE_FRAME must be train-only")
    aggregate = (
        frame.groupby(["cost_policy_id", "source_row_id"], sort=True)
        .agg(
            low_margin_rate=("low_margin_trade_tag", "mean"),
            direction_residual_rate=("direction_residual_tag", "mean"),
            underwater_rate=("underwater_tag", "mean"),
            drawdown_pressure_mean=("drawdown_pressure_value", "mean"),
            abstention_rate=("abstention_candidate_tag", "mean"),
        )
        .reset_index()
    )
    aggregate["drawdown_pressure_norm"] = 0.0
    for cost_policy, group in aggregate.groupby("cost_policy_id", sort=False):
        aggregate.loc[group.index, "drawdown_pressure_norm"] = drawdown_normalized(group["drawdown_pressure_mean"]).to_numpy()
    summary_rows: list[dict[str, Any]] = []
    for cost_policy, group in aggregate.groupby("cost_policy_id", sort=True):
        summary_rows.append(
            {
                "cost_policy_id": cost_policy,
                "source_rows": int(group["source_row_id"].nunique()),
                "low_margin_rate_mean": float(group["low_margin_rate"].mean()),
                "direction_residual_rate_mean": float(group["direction_residual_rate"].mean()),
                "underwater_rate_mean": float(group["underwater_rate"].mean()),
                "drawdown_pressure_mean": float(group["drawdown_pressure_mean"].mean()),
                "abstention_rate_mean": float(group["abstention_rate"].mean()),
                "allowed_use": "train-only sample weight diagnostic(학습 전용 표본 가중치 진단)",
                "forbidden_use": "validation/OOS threshold or selector(검증/OOS 임계값 또는 선택기)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    missing_train_ids = set(source.loc[source["split"].astype(str).eq("train"), "source_row_id"].astype(int)) - set(aggregate["source_row_id"].astype(int))
    if missing_train_ids:
        raise ValueError(f"Auxiliary aggregate is missing train source ids: {len(missing_train_ids)}")
    return aggregate, summary_rows


def weights_for_policy(source: pd.DataFrame, aggregate: pd.DataFrame, cost_policy_id: str, weight_policy: Mapping[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    weights = np.ones(len(source), dtype=np.float64)
    group = aggregate.loc[aggregate["cost_policy_id"].astype(str).eq(str(cost_policy_id))].copy()
    group = group.set_index("source_row_id")
    train_ids = source.loc[source["split"].astype(str).eq("train"), "source_row_id"].astype(int).to_numpy()
    low = group.reindex(train_ids)["low_margin_rate"].fillna(0.0).to_numpy(dtype=np.float64)
    direction = group.reindex(train_ids)["direction_residual_rate"].fillna(0.0).to_numpy(dtype=np.float64)
    drawdown = group.reindex(train_ids)["drawdown_pressure_norm"].fillna(0.0).to_numpy(dtype=np.float64)
    abstention = group.reindex(train_ids)["abstention_rate"].fillna(0.0).to_numpy(dtype=np.float64)
    weighted = (
        1.0
        + float(weight_policy["low_margin"]) * low
        + float(weight_policy["direction"]) * direction
        + float(weight_policy["drawdown"]) * drawdown
        + float(weight_policy["abstention"]) * abstention
    )
    weighted = np.clip(weighted, 0.25, 4.0)
    weights[train_ids] = weighted
    audit = {
        "cost_policy_id": cost_policy_id,
        "weight_policy_id": weight_policy["weight_policy_id"],
        "train_rows": int(len(train_ids)),
        "weight_min": float(weighted.min()) if len(weighted) else 0.0,
        "weight_mean": float(weighted.mean()) if len(weighted) else 0.0,
        "weight_max": float(weighted.max()) if len(weighted) else 0.0,
        "low_margin_component_mean": float(low.mean()) if len(low) else 0.0,
        "direction_component_mean": float(direction.mean()) if len(direction) else 0.0,
        "drawdown_component_mean": float(drawdown.mean()) if len(drawdown) else 0.0,
        "abstention_component_mean": float(abstention.mean()) if len(abstention) else 0.0,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return weights, audit


def task_rows(targets: Sequence[Mapping[str, Any]], feature_sets: Sequence[Mapping[str, Any]], split_masks: Mapping[str, np.ndarray]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target in targets:
        for feature_set in feature_sets:
            if feature_set["missing"]:
                continue
            for model_spec in MODEL_SPECS:
                for weight_policy in WEIGHT_POLICIES:
                    task_id = "__".join(
                        [
                            target["target_id"],
                            feature_set["feature_set_id"],
                            model_spec["model_config_id"],
                            weight_policy["weight_policy_id"],
                        ]
                    )
                    rows.append(
                        {
                            "task_id": task_id,
                            "target_id": target["target_id"],
                            "cost_policy_id": target["cost_policy_id"],
                            "feature_set_id": feature_set["feature_set_id"],
                            "model_config_id": model_spec["model_config_id"],
                            "weight_policy_id": weight_policy["weight_policy_id"],
                            "feature_count": len(feature_set["features"]),
                            "train_rows": int(split_masks["train"].sum()),
                            "training_disposition": "queued_guarded_training_no_selection(방어 학습 대기, 선택 없음)",
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )
    return rows


def safe_log_loss(y_true: np.ndarray, probabilities: np.ndarray) -> float:
    try:
        return float(log_loss(y_true, probabilities, labels=LABEL_ORDER))
    except ValueError:
        return float("nan")


def safe_balanced(y_true: np.ndarray, pred: np.ndarray) -> float:
    if len(y_true) == 0 or len(np.unique(y_true)) < 2:
        return 0.0
    return float(balanced_accuracy_score(y_true, pred))


def max_drawdown(values: np.ndarray) -> float:
    if len(values) == 0:
        return 0.0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    return float(np.max(peak - curve))


def profit_factor(values: np.ndarray) -> float:
    positive = float(values[values > 0].sum())
    negative = abs(float(values[values < 0].sum()))
    if negative == 0:
        return 999.0 if positive > 0 else 0.0
    return positive / negative


def score_classification(model_id: str, task: Mapping[str, Any], split: str, y_true: np.ndarray, probs: np.ndarray) -> dict[str, Any]:
    pred = np.asarray(LABEL_ORDER, dtype=np.int64)[probs.argmax(axis=1)]
    pred_counts = {INT_TO_LABEL[int(key)]: int(value) for key, value in pd.Series(pred).value_counts().to_dict().items()}
    true_counts = {INT_TO_LABEL[int(key)]: int(value) for key, value in pd.Series(y_true).value_counts().to_dict().items()}
    return {
        "model_id": model_id,
        "task_id": task["task_id"],
        "cost_policy_id": task["cost_policy_id"],
        "feature_set_id": task["feature_set_id"],
        "model_config_id": task["model_config_id"],
        "weight_policy_id": task["weight_policy_id"],
        "split": split,
        "rows": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, pred)),
        "balanced_accuracy": safe_balanced(y_true, pred),
        "macro_f1": float(f1_score(y_true, pred, labels=LABEL_ORDER, average="macro", zero_division=0)),
        "log_loss": safe_log_loss(y_true, probs),
        "pred_counts_json": json.dumps(pred_counts, ensure_ascii=False, sort_keys=True),
        "true_counts_json": json.dumps(true_counts, ensure_ascii=False, sort_keys=True),
        "signal_density": float((pred != LABEL_TO_INT["flat"]).mean()),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def score_trades(model_id: str, task: Mapping[str, Any], split: str, pred: np.ndarray, future_returns: np.ndarray, cost_returns: np.ndarray) -> dict[str, Any]:
    direction = np.where(pred == LABEL_TO_INT["long"], 1.0, np.where(pred == LABEL_TO_INT["short"], -1.0, 0.0))
    is_trade = direction != 0
    pnl = np.where(is_trade, direction * future_returns - cost_returns, 0.0)
    trade_values = pnl[is_trade]
    trade_count = int(is_trade.sum())
    dd = max_drawdown(trade_values)
    net = float(trade_values.sum()) if trade_count else 0.0
    return {
        "model_id": model_id,
        "task_id": task["task_id"],
        "cost_policy_id": task["cost_policy_id"],
        "feature_set_id": task["feature_set_id"],
        "model_config_id": task["model_config_id"],
        "weight_policy_id": task["weight_policy_id"],
        "split": split,
        "trade_count": trade_count,
        "signal_density": float(is_trade.mean()),
        "net_log_return_after_cost": net,
        "profit_factor": profit_factor(trade_values),
        "expectancy": float(trade_values.mean()) if trade_count else 0.0,
        "max_drawdown": dd,
        "recovery_factor": (net / dd) if dd > 0 else (999.0 if net > 0 else 0.0),
        "long_count": int((pred == LABEL_TO_INT["long"]).sum()),
        "short_count": int((pred == LABEL_TO_INT["short"]).sum()),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def control_labels(control_id: str, y: np.ndarray, source_ids: np.ndarray) -> np.ndarray:
    if control_id == "shifted_return_control":
        return np.roll(y, 12)
    if control_id == "noise_label_control":
        return ((source_ids.astype(np.int64) * 1103515245 + 12345) % 3).astype(np.int64)
    if control_id == "block_shuffle_control":
        block = source_ids.astype(np.int64) // 288
        return ((y + block + 1) % 3).astype(np.int64)
    return y.copy()


def score_controls(model_id: str, task: Mapping[str, Any], split: str, pred: np.ndarray, y_true: np.ndarray, source_ids: np.ndarray, candidate_balanced: float) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for control_id in ("shifted_return_control", "noise_label_control", "block_shuffle_control"):
        y_control = control_labels(control_id, y_true, source_ids)
        alignment = safe_balanced(y_control, pred)
        rows.append(
            {
                "model_id": model_id,
                "task_id": task["task_id"],
                "control_id": control_id,
                "split": split,
                "rows": int(len(pred)),
                "candidate_balanced_accuracy": candidate_balanced,
                "control_alignment_balanced_accuracy": alignment,
                "blocks_training_review": "true" if split == "validation" and alignment >= max(0.45, candidate_balanced - 0.02) else "false",
                "effect": "scores shifted/noise/block controls before release(해제 전 이동/잡음/블록 대조 점수화)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_density_rows(trade_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    frame = pd.DataFrame(trade_rows)
    rows: list[dict[str, Any]] = []
    for model_id, group in frame.groupby("model_id", sort=False):
        train_density = float(group.loc[group["split"].eq("train"), "signal_density"].iloc[0])
        for split in ("validation", "oos"):
            split_row = group.loc[group["split"].eq(split)].iloc[0]
            split_density = float(split_row["signal_density"])
            gap = split_density - train_density
            rows.append(
                {
                    "model_id": model_id,
                    "task_id": str(split_row["task_id"]),
                    "split": split,
                    "train_signal_density": train_density,
                    "split_signal_density": split_density,
                    "density_gap_vs_train": gap,
                    "density_pressure_flag": "true" if abs(gap) >= 0.18 else "false",
                    "trade_count": int(split_row["trade_count"]),
                    "effect": "fixed density diagnostic only, no threshold search(고정 밀도 진단 전용, 임계값 탐색 없음)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def train_and_score() -> dict[str, Any]:
    io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    io_path(ONNX_DIR).mkdir(parents=True, exist_ok=True)
    source = read_source_frame()
    feature_sets, compat_rows = read_feature_sets(source)
    targets = read_targets()
    auxiliary, aux_summary = build_auxiliary_tables(source)
    split_masks = {split: source["split"].astype(str).eq(split).to_numpy() for split in ("train", "validation", "oos")}
    tasks = task_rows(targets, feature_sets, split_masks)
    feature_by_id = {row["feature_set_id"]: row for row in feature_sets}
    target_by_id = {row["target_id"]: row for row in targets}
    weight_by_id = {row["weight_policy_id"]: row for row in WEIGHT_POLICIES}

    model_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    class_score_rows: list[dict[str, Any]] = []
    trade_score_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    release_rows: list[dict[str, Any]] = []
    weight_rows: list[dict[str, Any]] = []
    dynamic_artifacts: list[Path] = []
    weight_cache: dict[tuple[str, str], tuple[np.ndarray, dict[str, Any]]] = {}

    for index, task in enumerate(tasks, start=1):
        feature_row = feature_by_id[task["feature_set_id"]]
        target = target_by_id[task["target_id"]]
        features = feature_row["features"]
        X_all = source.loc[:, features].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float64)
        y_all = np.asarray(target["y"], dtype=np.int64)
        weight_key = (task["cost_policy_id"], task["weight_policy_id"])
        if weight_key not in weight_cache:
            weight_cache[weight_key] = weights_for_policy(source, auxiliary, task["cost_policy_id"], weight_by_id[task["weight_policy_id"]])
            weight_rows.append(weight_cache[weight_key][1])
        sample_weight = weight_cache[weight_key][0]
        model = build_model(task["model_config_id"])
        train_idx = np.flatnonzero(split_masks["train"])
        fit_weighted_model(model, X_all[train_idx], y_all[train_idx], sample_weight[train_idx])
        model_key = f"dz{index:03d}"
        model_id = f"{model_key}__{task['target_id']}__{task['feature_set_id']}__{task['model_config_id']}__{task['weight_policy_id']}"
        model_path = MODEL_DIR / f"{model_key}.joblib"
        onnx_path = ONNX_DIR / f"{model_key}.onnx"
        joblib.dump(model, io_path(model_path))
        export_info = export_sklearn_to_onnx_zipmap_disabled(model, onnx_path, feature_count=len(features), drop_label_output=True)
        dynamic_artifacts.extend([model_path, onnx_path])
        sample_idx = np.concatenate(
            [
                np.flatnonzero(split_masks["train"])[:128],
                np.flatnonzero(split_masks["validation"])[:128],
                np.flatnonzero(split_masks["oos"])[:128],
            ]
        )
        parity = check_onnxruntime_probability_parity(model, onnx_path, X_all[sample_idx], class_order=LABEL_ORDER)
        parity_rows.append(
            {
                "model_id": model_id,
                "task_id": task["task_id"],
                "onnx_path": rel(onnx_path),
                "passed": str(bool(parity["passed"])).lower(),
                "rows": parity["rows"],
                "max_abs_diff": parity["max_abs_diff"],
                "mean_abs_diff": parity["mean_abs_diff"],
                "onnx_row_sum_max_abs_error": parity["onnx_row_sum_max_abs_error"],
                "input_name": parity["input_name"],
                "output_names": parity["output_names"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        model_rows.append(
            {
                "model_id": model_id,
                "task_id": task["task_id"],
                "target_id": task["target_id"],
                "cost_policy_id": task["cost_policy_id"],
                "feature_set_id": task["feature_set_id"],
                "model_config_id": task["model_config_id"],
                "weight_policy_id": task["weight_policy_id"],
                "feature_count": len(features),
                "feature_order_hash": feature_row["feature_order_hash"],
                "class_order_json": json.dumps(LABEL_ORDER),
                "model_path": rel(model_path),
                "model_sha256": sha256_file(model_path),
                "onnx_path": rel(onnx_path),
                "onnx_sha256": sha256_file(onnx_path),
                "onnx_probability_output_name": export_info["probability_output_name"],
                "train_rows": int(split_masks["train"].sum()),
                "validation_rows": int(split_masks["validation"].sum()),
                "oos_rows": int(split_masks["oos"].sum()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        split_score_by_name: dict[str, dict[str, Any]] = {}
        validation_control_blocks = 0
        for split in ("train", "validation", "oos"):
            idx = np.flatnonzero(split_masks[split])
            probs = ordered_sklearn_probabilities(model, X_all[idx], class_order=LABEL_ORDER)
            pred = np.asarray(LABEL_ORDER, dtype=np.int64)[probs.argmax(axis=1)]
            y_true = y_all[idx]
            class_score = score_classification(model_id, task, split, y_true, probs)
            trade_score = score_trades(model_id, task, split, pred, target["future_returns"][idx], target["cost_returns"][idx])
            class_score_rows.append(class_score)
            trade_score_rows.append(trade_score)
            split_score_by_name[split] = {**class_score, **{f"trade_{key}": value for key, value in trade_score.items()}}
            if split in {"validation", "oos"}:
                controls = score_controls(model_id, task, split, pred, y_true, target["source_row_id"][idx], float(class_score["balanced_accuracy"]))
                control_rows.extend(controls)
                if split == "validation":
                    validation_control_blocks += sum(1 for row in controls if row["blocks_training_review"] == "true")

        validation = split_score_by_name["validation"]
        oos = split_score_by_name["oos"]
        blockers: list[str] = ["EA_review_required_no_auto_release"]
        if float(validation["trade_profit_factor"]) < 1.05:
            blockers.append("validation_pf_below_1p05")
        if int(validation["trade_trade_count"]) < 500:
            blockers.append("validation_trade_count_below_500")
        if validation_control_blocks:
            blockers.append("negative_control_alignment")
        release_rows.append(
            {
                "model_id": model_id,
                "task_id": task["task_id"],
                "validation_pf": validation["trade_profit_factor"],
                "oos_pf": oos["trade_profit_factor"],
                "validation_balanced_accuracy": validation["balanced_accuracy"],
                "validation_trade_count": validation["trade_trade_count"],
                "control_block_rows": validation_control_blocks,
                "density_pressure_rows": 0,
                "release_disposition": "held_for_EA_review_no_selection",
                "release_blockers": ";".join(blockers),
                "next_condition": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    density_rows = build_density_rows(trade_score_rows)
    pressure_by_model: dict[str, int] = {}
    for row in density_rows:
        if row["split"] == "validation" and row["density_pressure_flag"] == "true":
            pressure_by_model[row["model_id"]] = pressure_by_model.get(row["model_id"], 0) + 1
    for row in release_rows:
        pressure_rows = pressure_by_model.get(row["model_id"], 0)
        row["density_pressure_rows"] = pressure_rows
        if pressure_rows:
            row["release_blockers"] = str(row["release_blockers"]) + ";validation_density_pressure"
    return {
        "source": source,
        "tasks": tasks,
        "compat_rows": compat_rows,
        "aux_summary": aux_summary,
        "weight_rows": sorted(weight_rows, key=lambda item: (item["cost_policy_id"], item["weight_policy_id"])),
        "model_rows": model_rows,
        "parity_rows": parity_rows,
        "class_score_rows": class_score_rows,
        "trade_score_rows": trade_score_rows,
        "control_rows": control_rows,
        "density_rows": density_rows,
        "release_rows": release_rows,
        "dynamic_artifacts": dynamic_artifacts,
        "source_rows": int(len(source)),
        "train_rows": int(split_masks["train"].sum()),
        "validation_rows": int(split_masks["validation"].sum()),
        "oos_rows": int(split_masks["oos"].sum()),
    }


def build_split_guard_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    dy_final = read_json(DY_FINAL)
    dy_gate_failed = sum(1 for row in read_csv(DY_GATES) if row.get("status") != "passed")
    wfo_rows = read_csv(WFO_INPUT_REVIEW)
    return [
        {
            "guard_id": "parent_next_action_matches",
            "source": rel(DY_FINAL),
            "status": "passed" if dy_final.get("next_action") == RUN_ID else "failed",
            "observed": str(dy_final.get("next_action", "")),
            "expected": RUN_ID,
            "effect": "continues DY queue(DY 대기열을 이어감)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "parent_gates_passed",
            "source": rel(DY_GATES),
            "status": "passed" if dy_gate_failed == 0 else "failed",
            "observed": str(dy_gate_failed),
            "expected": "0",
            "effect": "uses only reviewed DY inputs(검토된 DY 입력만 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "objective_frame_train_only",
            "source": rel(OBJECTIVE_FRAME),
            "status": "passed",
            "observed": f"train_rows={result['train_rows']}",
            "expected": "train_only",
            "effect": "prevents validation/OOS label feedback(검증/OOS 라벨 피드백 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "guard_id": "wfo_precheck_carried",
            "source": rel(WFO_INPUT_REVIEW),
            "status": "passed" if len(wfo_rows) > 0 else "failed",
            "observed": f"rows={len(wfo_rows)}",
            "expected": ">0",
            "effect": "keeps WFO/embargo as precondition(WFO/격리를 선행 조건으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_runtime_rows() -> list[dict[str, Any]]:
    rows = read_csv(FIREWALL_REVIEW)
    if not rows:
        return [
            {
                "firewall_id": "firewall_review_missing",
                "held_action": "all_runtime_actions",
                "carry_status": "missing_review",
                "review_status": "blocked_if_missing",
                "effect": "blocks runtime claims when firewall review is absent(방화벽 검토가 없으면 런타임 주장 차단)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    return [
        {
            "firewall_id": row.get("review_id", row.get("firewall_id", "")),
            "held_action": row.get("forbidden_use", row.get("held_action", "MT5/Forward/Goal")),
            "carry_status": "carried_forward_from_DY",
            "review_status": "preserved_no_runtime_claim",
            "effect": "keeps runtime and Forward claims closed(런타임과 전진 주장을 닫아 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in rows
    ]


def build_ea_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337EA_review_auxiliary_weighted_scorecards",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review auxiliary-weighted candidate scorecards(보조 가중 후보 점수표 검토)",
            "required_inputs": f"{rel(CANDIDATE_SCORECARD)};{rel(PROXY_TRADE_SCORECARD)}",
            "required_outputs": "guarded_transfer_density_training_review.csv",
            "blocked_if_missing": "candidate scorecards(후보 점수표)",
            "forbidden_action": "no candidate selection from DZ output(DZ 출력으로 후보 선택 금지)",
            "effect": "separates trained artifacts from selection(학습 산출물과 선택을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EA_review_onnx_parity",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review ONNX parity and feature order(ONNX 동등성과 피처 순서 검토)",
            "required_inputs": f"{rel(ONNX_PARITY)};{rel(FEATURE_COMPATIBILITY)}",
            "required_outputs": "onnx_parity_review.csv",
            "blocked_if_missing": "ONNX parity or feature compatibility(ONNX 동등성 또는 피처 적합성)",
            "forbidden_action": "no runtime package if parity fails(동등성 실패 시 런타임 패키지 금지)",
            "effect": "keeps Python/ONNX handoff honest(파이썬/ONNX 인계를 정직하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EA_review_controls_density_split",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review controls, density, and split guard(대조/밀도/분할 가드 검토)",
            "required_inputs": f"{rel(NEGATIVE_CONTROL_SCORECARD)};{rel(DENSITY_GUARD_AUDIT)};{rel(SPLIT_GUARD_AUDIT)}",
            "required_outputs": "control_density_split_review.csv",
            "blocked_if_missing": "control/density/split audits(대조/밀도/분할 감사)",
            "forbidden_action": "no release if controls or density block(대조 또는 밀도 차단 시 해제 금지)",
            "effect": "keeps overfit checks before promotion language(승격 표현 전에 과적합 검사를 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EA_preserve_runtime_firewall",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "preserve no-MT5/no-Forward firewall(무 MT5/무 전진 방화벽 보존)",
            "required_inputs": rel(RELEASE_DISPOSITION),
            "required_outputs": "training_runtime_disposition_review.csv",
            "blocked_if_missing": "release disposition(해제 처분)",
            "forbidden_action": "no MT5 probe or Forward claim(MT5 탐침 또는 전진 주장 금지)",
            "effect": "keeps runtime authority closed(런타임 권위를 닫아 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "required DY/source inputs exist(필수 DY/원천 입력 존재)"),
        ("parent_dy_gates_passed", final["dy_failed_gate_rows"] == 0, str(final["dy_failed_gate_rows"]), "0", "DY review usable(DY 검토 사용 가능)"),
        ("parent_next_action_matches", final["dy_next_action"] == RUN_ID, str(final["dy_next_action"]), RUN_ID, "continues DY queue(DY 대기열을 이어감)"),
        ("objective_frame_train_only", final["objective_split_values"] == ["train"], ",".join(final["objective_split_values"]), "train", "auxiliary tags are train-only(보조 태그가 학습 전용)"),
        ("feature_compatibility_clear", final["feature_missing_rows"] == 0, str(final["feature_missing_rows"]), "0", "feature sets available(피처 묶음 사용 가능)"),
        ("tasks_materialized", final["task_rows"] == 54, str(final["task_rows"]), "54", "3 cost policies x 3 feature sets x 2 models x 3 weight policies(3 비용 x 3 피처 x 2 모델 x 3 가중치)"),
        ("models_trained", final["trained_models"] == final["task_rows"], f"{final['trained_models']}/{final['task_rows']}", "all", "guarded models trained(방어 모델 학습 완료)"),
        ("onnx_parity_passed", final["onnx_parity_passed"] == final["onnx_parity_rows"] and final["onnx_parity_rows"] > 0, f"{final['onnx_parity_passed']}/{final['onnx_parity_rows']}", "all", "Python/ONNX parity passed(파이썬/ONNX 동등성 통과)"),
        ("scorecards_materialized", final["classification_score_rows"] == final["trained_models"] * 3 and final["trade_score_rows"] == final["trained_models"] * 3, f"class={final['classification_score_rows']};trade={final['trade_score_rows']}", "models*3", "train/validation/OOS scorecards exist(학습/검증/OOS 점수표 존재)"),
        ("negative_controls_scored", final["negative_control_rows"] == final["trained_models"] * 2 * 3, str(final["negative_control_rows"]), "models*2 splits*3 controls", "controls scored on validation/OOS(검증/OOS 대조 점수화)"),
        ("density_guard_materialized", final["density_guard_rows"] == final["trained_models"] * 2, str(final["density_guard_rows"]), "models*2", "density guard audited(밀도 가드 감사 완료)"),
        ("release_blocked", final["release_candidate_rows"] == 0 and final["auto_mt5_release_rows"] == 0, f"release={final['release_candidate_rows']};mt5={final['auto_mt5_release_rows']}", "0/0", "release and MT5 remain blocked(해제와 MT5 계속 차단)"),
        (
            "no_forbidden_claim",
            final["candidate_selection"] == "not_run"
            and final["mt5_runtime_probe"] == "not_run"
            and final["goal_achieve"] == "not_claimed",
            f"selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}",
            "not_run/not_claimed",
            "claim boundary preserved(주장 경계 보존)",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    model_receipt = {
        "model_family": "logreg_balanced_c050 and extratrees_depth6_leaf120(로지스틱 회귀와 엑스트라 트리)",
        "target_and_label": "fixed costed action labels with train-only auxiliary sample weights(고정 비용 반영 행동 라벨과 학습 전용 보조 표본 가중치)",
        "split_method": "train fit only; validation/OOS scoring only(학습 적합만 수행, 검증/OOS는 점수화만 수행)",
        "selection_metric": "none; all tasks trained and held for EA review(없음, 전체 작업 학습 후 EA 검토 보류)",
        "secondary_metrics": "proxy PF, balanced accuracy, shifted/noise/block controls, density, ONNX parity(프록시 PF/균형 정확도/이동·잡음·블록 대조/밀도/ONNX 동등성)",
        "threshold_policy": "argmax only, no threshold tuning(argmax 전용, 임계값 조정 없음)",
        "overfit_risk": "post-training choice from validation/OOS scorecards(학습 후 검증/OOS 점수표 선택 위험)",
        "calibration_risk": "scores are ranking diagnostics, not calibrated probabilities(점수는 보정 확률이 아니라 순위 진단)",
        "comparison_baseline": rel(DY_FINAL),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(SOURCE_MODEL_INPUT), rel(OBJECTIVE_FRAME), rel(VALIDATION_EDGE_FRAME)],
        "time_axis": "UTC closed M5 source rows with source_row_id alignment(UTC 종가 M5 원천 행과 source_row_id 정렬)",
        "sample_scope": f"source_rows={final['source_rows']};train={final['train_rows']};validation={final['validation_rows']};oos={final['oos_rows']}",
        "missing_or_duplicate_check": f"feature_missing_rows={final['feature_missing_rows']};feature_nonfinite_rows={final['feature_nonfinite_rows']}",
        "feature_label_boundary": "auxiliary tags are generated from train-only objective frame and used only as sample weights(보조 태그는 학습 전용 목표 프레임에서 만들고 표본 가중치로만 사용)",
        "split_boundary": "train-only fit, validation/OOS read-only(학습 전용 적합, 검증/OOS 읽기 전용)",
        "leakage_risk": "choosing a candidate after looking at validation/OOS proxy scorecards(검증/OOS 프록시 점수표를 본 뒤 후보를 고르는 위험)",
        "data_hash_or_identity": {
            rel(SOURCE_MODEL_INPUT): sha256_file(SOURCE_MODEL_INPUT),
            rel(OBJECTIVE_FRAME): sha256_file(OBJECTIVE_FRAME),
            rel(VALIDATION_EDGE_FRAME): sha256_file(VALIDATION_EDGE_FRAME),
        },
        "integrity_judgment": "usable_with_review_required",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"trained_models={final['trained_models']};best_validation_pf={final['best_validation_pf']};best_oos_pf={final['best_oos_pf']}",
        "comparison_baseline": rel(DY_FINAL),
        "likely_drivers": "sample weighting, feature set, model family, cost policy(표본 가중치/피처 묶음/모델 계열/비용 정책)",
        "segment_checks": f"control_block_rows={final['control_block_rows']};density_pressure_rows={final['density_pressure_rows']}",
        "trade_shape": f"best_validation_trades={final['best_validation_trade_count']};best_oos_trades={final['best_oos_trade_count']}",
        "alternative_explanations": "class imbalance, serial dependence, proxy cost mismatch, validation pocket noise(클래스 불균형/연속 의존/프록시 비용 불일치/검증 포켓 잡음)",
        "attribution_confidence": "medium_for_proxy_low_for_runtime(프록시는 중간, 런타임은 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime_receipt = {
        "research_path": rel(Path(__file__)),
        "runtime_path": "not_applicable_no_MT5_package(해당 없음, MT5 패키지 없음)",
        "shared_contract": "feature order, class order, ONNX probability output(피처 순서/클래스 순서/ONNX 확률 출력)",
        "known_differences": "no MT5 handoff or tester output in DZ(DZ에는 MT5 인계나 테스터 출력 없음)",
        "parity_check": f"{final['onnx_parity_passed']}/{final['onnx_parity_rows']} Python/ONNX rows(파이썬/ONNX 행)",
        "parity_identity": rel(ONNX_PARITY),
        "runtime_claim_boundary": "research-only(연구 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "trained models, ONNX parity, proxy scorecards, controls, density audit(학습 모델/ONNX 동등성/프록시 점수표/대조/밀도 감사)",
        "evidence_missing": "EA review, candidate selection decision, MT5, forward data(EA 검토/후보 선택 결정/MT5/전진 데이터)",
        "judgment_label": "training_materialized_review_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "모델은 만들었지만 아직 고른 것은 아니다. EA에서 대조와 밀도를 먼저 검토한다.",
    }
    paths = [
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(RUNTIME_RECEIPT, runtime_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in list(artifact_paths) + paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_training_outputs_with_tracked_report(무시된 학습 출력과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DZ Guarded Transfer Density Control Training(337DZ 방어 전이/밀도/대조 학습)

## Conclusion(결론)

run337DZ(337DZ 실행)는 DY에서 허용된 train-only auxiliary tags(학습 전용 보조 태그)를 sample weight(표본 가중치)로만 사용해 guarded action candidates(방어 행동 후보)를 학습했고 ONNX parity(ONNX 동등성)를 확인했다.

이 작업은 model training(모델 학습)이다. candidate selection(후보 선택), threshold tuning(임계값 조정), lot optimization(로트 최적화), MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 주장은 하지 않는다.

Effect(효과): 다음 run337EA(337EA 실행)는 scorecard/control/density/parity(점수표/대조/밀도/동등성)를 검토해 새 학습이 진짜 진전인지 또는 또 다른 과적합인지 판단한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- trained_models(학습 모델): `{final["trained_models"]}`
- onnx_parity(ONNX 동등성): `{final["onnx_parity_passed"]}/{final["onnx_parity_rows"]}`
- best_validation_pf(최고 검증 PF): `{final["best_validation_pf"]}`
- best_oos_pf(최고 OOS PF): `{final["best_oos_pf"]}`
- control_block_rows(대조 차단 행): `{final["control_block_rows"]}`
- density_pressure_rows(밀도 압력 행): `{final["density_pressure_rows"]}`
- release_candidate_rows(해제 후보 행): `{final["release_candidate_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DZ

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 방어 후보와 ONNX를 만들었지만 선택/MT5/Forward(전진)는 EA 검토 전까지 닫는다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(ONNX_PARITY)}`, `{rel(PROXY_TRADE_SCORECARD)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337DZ focus complete: guarded transfer/density/control repair training(방어 전이/밀도/대조 수리 학습)을 `{STATUS}`로 물질화했다. "
        f"Effect(효과): run337EA(337EA 실행)에서 scorecard/control/density/parity(점수표/대조/밀도/동등성)를 검토한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DZ focus complete")
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{NEXT_RUN_ID}`",
        "status": f"`{STATUS}`",
        "decision": f"`{DECISION}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current_text = replace_bullet_value(current_text, field_name, value)
    section = f"""
## Stage337 run337DZ(337DZ 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): train-only auxiliary weights(학습 전용 보조 가중치)로 ONNX 후보를 만들었지만 EA 검토 전 선택/MT5/Forward(전진)는 주장하지 않는다. Goal(목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DO("
    if "## Stage337 run337DZ(337DZ 실행)" not in current_text:
        current_text = current_text.replace(marker, section + "\n" + marker, 1) if marker in current_text else current_text.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{STATUS}`
- actual_mt5_execution(실제 MT5 실행): `not_run_dz_training_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): `다음은 guarded transfer/density/control training review(방어 전이/밀도/대조 학습 검토)이다.`
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337DZ(337DZ 실행) trained guarded transfer/density/control repair candidates(방어 전이/밀도/대조 수리 후보 학습). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DZ(337DZ 실행) trained guarded transfer"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DZ trained guarded transfer/density/control repair candidates(방어 전이/밀도/대조 수리 후보 학습) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DZ trained guarded transfer"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "guarded_transfer_density_control_training_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"models={final['trained_models']};onnx={final['onnx_parity_passed']}/{final['onnx_parity_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_training_model_validation_performance_attribution_runtime_parity",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__guarded_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "guarded_training",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "training_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "proxy_training_onnx_control_density",
        "scoreboard_lane": "model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_validation_pf={final['best_validation_pf']};best_oos_pf={final['best_oos_pf']}",
        "guardrail_kpi": "onnx_parity;controls;density;no_selection;no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__guarded_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_training_model_validation_performance_attribution_runtime_parity",
        "evidence_scope": "guarded candidates trained and ONNX exported",
        "kpi_scope": "proxy_scorecard_control_density_onnx",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__guarded_training",
        "family": "model_training_model_validation_performance_attribution_runtime_parity",
        "question": "do train-only auxiliary weights repair transfer density control failure without selection",
        "metric_scope": "trained_models_onnx_parity_proxy_pf_controls_density",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    artifacts = [
        upsert_csv(RUN_REGISTRY, "run_id", run_row),
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", alpha_row),
        upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_row),
    ]
    artifact_columns: list[str] = []
    artifact_rows: list[dict[str, str]] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            artifact_columns = list(reader.fieldnames or [])
            artifact_rows = [dict(row) for row in reader]
    if not artifact_columns:
        artifact_columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys and row.get("run_id") != RUN_ID]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    result = train_and_score()
    split_guard_rows = build_split_guard_rows(result)
    runtime_rows = build_runtime_rows()
    artifacts: list[Path] = [
        write_csv(TASK_MATRIX, TASK_COLUMNS, result["tasks"]),
        write_csv(FEATURE_COMPATIBILITY, FEATURE_COMPAT_COLUMNS, result["compat_rows"]),
        write_csv(AUXILIARY_TAG_SUMMARY, AUX_COLUMNS, result["aux_summary"]),
        write_csv(SAMPLE_WEIGHT_AUDIT, WEIGHT_AUDIT_COLUMNS, result["weight_rows"]),
        write_csv(TRAINED_MODEL_MANIFEST, MODEL_COLUMNS, result["model_rows"]),
        write_csv(ONNX_PARITY, PARITY_COLUMNS, result["parity_rows"]),
        write_csv(CANDIDATE_SCORECARD, CLASS_SCORE_COLUMNS, result["class_score_rows"]),
        write_csv(PROXY_TRADE_SCORECARD, TRADE_SCORE_COLUMNS, result["trade_score_rows"]),
        write_csv(NEGATIVE_CONTROL_SCORECARD, CONTROL_COLUMNS, result["control_rows"]),
        write_csv(DENSITY_GUARD_AUDIT, DENSITY_COLUMNS, result["density_rows"]),
        write_csv(SPLIT_GUARD_AUDIT, SPLIT_GUARD_COLUMNS, split_guard_rows),
        write_csv(RUNTIME_FIREWALL_REVIEW, RUNTIME_COLUMNS, runtime_rows),
        write_csv(RELEASE_DISPOSITION, RELEASE_COLUMNS, result["release_rows"]),
        write_csv(EA_QUEUE, QUEUE_COLUMNS, build_ea_queue()),
    ]
    artifacts.extend(result["dynamic_artifacts"])
    parity_passed = sum(1 for row in result["parity_rows"] if row["passed"] == "true")
    trade_frame = pd.DataFrame(result["trade_score_rows"])
    val_frame = trade_frame.loc[trade_frame["split"].eq("validation")]
    oos_frame = trade_frame.loc[trade_frame["split"].eq("oos")]
    best_validation = val_frame.sort_values("profit_factor", ascending=False).iloc[0].to_dict() if len(val_frame) else {}
    best_oos = oos_frame.sort_values("profit_factor", ascending=False).iloc[0].to_dict() if len(oos_frame) else {}
    control_blocks = sum(1 for row in result["control_rows"] if row["blocks_training_review"] == "true")
    density_pressure_rows = sum(1 for row in result["density_rows"] if row["density_pressure_flag"] == "true")
    release_candidates = sum(1 for row in result["release_rows"] if row["release_disposition"] != "held_for_EA_review_no_selection")
    objective_split_values = sorted(pd.read_parquet(io_path(OBJECTIVE_FRAME), columns=["split"])["split"].astype(str).unique().tolist())
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dy_next_action": read_json(DY_FINAL).get("next_action", ""),
        "dy_failed_gate_rows": sum(1 for row in read_csv(DY_GATES) if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "source_rows": result["source_rows"],
        "train_rows": result["train_rows"],
        "validation_rows": result["validation_rows"],
        "oos_rows": result["oos_rows"],
        "objective_split_values": objective_split_values,
        "task_rows": len(result["tasks"]),
        "trained_models": len(result["model_rows"]),
        "feature_missing_rows": sum(1 for row in result["compat_rows"] if int(row["missing_count"]) > 0),
        "feature_nonfinite_rows": sum(int(row["nonfinite_rows"]) for row in result["compat_rows"]),
        "auxiliary_tag_rows": len(result["aux_summary"]),
        "sample_weight_rows": len(result["weight_rows"]),
        "onnx_parity_rows": len(result["parity_rows"]),
        "onnx_parity_passed": parity_passed,
        "classification_score_rows": len(result["class_score_rows"]),
        "trade_score_rows": len(result["trade_score_rows"]),
        "negative_control_rows": len(result["control_rows"]),
        "control_block_rows": control_blocks,
        "density_guard_rows": len(result["density_rows"]),
        "density_pressure_rows": density_pressure_rows,
        "split_guard_rows": len(split_guard_rows),
        "runtime_firewall_rows": len(runtime_rows),
        "release_disposition_rows": len(result["release_rows"]),
        "release_candidate_rows": release_candidates,
        "auto_mt5_release_rows": 0,
        "best_validation_model_id": best_validation.get("model_id", ""),
        "best_validation_pf": float(best_validation.get("profit_factor", 0.0) or 0.0),
        "best_validation_trade_count": int(best_validation.get("trade_count", 0) or 0),
        "best_oos_model_id": best_oos.get("model_id", ""),
        "best_oos_pf": float(best_oos.get("profit_factor", 0.0) or 0.0),
        "best_oos_trade_count": int(best_oos.get("trade_count", 0) or 0),
        "model_training": "run_guarded_training",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "dynamic_artifacts": [rel(path) for path in result["dynamic_artifacts"]],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision_doc(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": "gate_failed", "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "trained_models": final["trained_models"],
                "onnx_parity": f"{final['onnx_parity_passed']}/{final['onnx_parity_rows']}",
                "best_validation_pf": final["best_validation_pf"],
                "best_oos_pf": final["best_oos_pf"],
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
