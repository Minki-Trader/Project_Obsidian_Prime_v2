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
from foundation.models.baseline_training import LABEL_ORDER  # noqa: E402
from foundation.models.onnx_bridge import (  # noqa: E402
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_sklearn_probabilities,
)
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
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337DA"
RUN_ID = "run337DA_train_objective_feature_contract_pivot_candidates_without_db_v1"
PARENT_RUN_ID = "run337CZ_materialize_objective_feature_contract_pivot_inputs_without_db_v1"
NEXT_RUN_ID = "run337DB_review_objective_feature_contract_pivot_training_without_db_v1"
STATUS = "completed_stage337DA_objective_feature_contract_pivot_candidates_trained_review_required_no_selection_no_mt5"
JUDGMENT = "guarded_objective_feature_pivot_training_completed_review_required_no_forward_selection"
DECISION = "stage337DA_open_run337DB_review_objective_feature_contract_pivot_training"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DA_objective_feature_contract_pivot_training_without_db_"
    "train_only_inputs_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337DA_objective_feature_contract_pivot_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DA_objective_feature_contract_pivot_training.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

SOURCE_MODEL_INPUT = (
    ROOT
    / "data"
    / "processed"
    / "model_inputs"
    / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
    / "model_input_dataset.parquet"
)
CZ_DIR = STAGE_DIR / "02_runs" / "run337CZ"
CZ_FINAL = CZ_DIR / "final_decision.json"
CZ_GATES = CZ_DIR / "required_gate_coverage_audit.csv"
CZ_QUEUE = CZ_DIR / "run337DA_guarded_training_queue.csv"
COST_TRADEABILITY_LABEL_FRAME = CZ_DIR / "cost_tradeability_label_frame.parquet"
PAYOFF_RANK_LABEL_FRAME = CZ_DIR / "payoff_rank_label_frame.parquet"
CONTROL_RESIDUAL_LABEL_FRAME = CZ_DIR / "control_residual_label_frame.parquet"
CONTROL_SIDECAR_MATRIX = CZ_DIR / "control_sidecar_matrix.csv"
FEATURE_CONTRACT_MANIFEST = CZ_DIR / "feature_contract_manifest.json"
TWO_STAGE_HANDOFF_MANIFEST = CZ_DIR / "two_stage_handoff_manifest.json"
OBJECTIVE_INPUT_MANIFEST = CZ_DIR / "objective_feature_input_manifest.json"

TASK_MATRIX = RUN_DIR / "objective_feature_training_task_matrix.csv"
TRAINED_MODEL_MANIFEST = RUN_DIR / "trained_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "onnx_parity_matrix.csv"
TRAINING_SCORECARD = RUN_DIR / "objective_training_scorecard.csv"
CONTROL_SCORECARD = RUN_DIR / "control_residual_scorecard.csv"
COST_CURVE_SCORECARD = RUN_DIR / "cost_curve_scorecard.csv"
RANK_MONOTONICITY_REVIEW = RUN_DIR / "rank_monotonicity_review.csv"
RUNTIME_DISPOSITION = RUN_DIR / "runtime_release_disposition.csv"
PROXY_EXPECTED = RUN_DIR / "proxy_expected_by_objective.csv"
FEATURE_COMPATIBILITY = RUN_DIR / "feature_input_compatibility.csv"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    SOURCE_MODEL_INPUT,
    CZ_FINAL,
    CZ_GATES,
    CZ_QUEUE,
    COST_TRADEABILITY_LABEL_FRAME,
    PAYOFF_RANK_LABEL_FRAME,
    CONTROL_RESIDUAL_LABEL_FRAME,
    CONTROL_SIDECAR_MATRIX,
    FEATURE_CONTRACT_MANIFEST,
    TWO_STAGE_HANDOFF_MANIFEST,
    OBJECTIVE_INPUT_MANIFEST,
)
OUTPUT_FILES = (
    TASK_MATRIX,
    TRAINED_MODEL_MANIFEST,
    ONNX_PARITY,
    TRAINING_SCORECARD,
    CONTROL_SCORECARD,
    COST_CURVE_SCORECARD,
    RANK_MONOTONICITY_REVIEW,
    RUNTIME_DISPOSITION,
    PROXY_EXPECTED,
    FEATURE_COMPATIBILITY,
    MODEL_RECEIPT,
    DATA_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
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

MODEL_SPECS = (
    {"model_config_id": "logreg_balanced_c075", "family": "logistic_regression(로지스틱 회귀)"},
    {"model_config_id": "extratrees_depth6_leaf160", "family": "extra_trees(엑스트라 트리)"},
)
COST_LEVELS = (0, 2, 5)
LABEL_TO_INT = {"short": 0, "flat": 1, "long": 2, "low": 0, "mid": 1, "high": 2}
INT_TO_LABEL = {0: "short", 1: "flat", 2: "long"}
CONTROL_COLUMNS = {
    "label_shift_gap72_control": "gap72_control_label",
    "label_shift_gap96_control": "gap96_control_label",
    "horizon_modulo_fold_control": "modulo_control_label",
}

TASK_COLUMNS = (
    "task_id",
    "target_id",
    "target_family",
    "target_source",
    "cost_contract_id",
    "control_id",
    "feature_set_id",
    "model_config_id",
    "feature_count",
    "training_disposition",
    "claim_boundary",
)
MODEL_COLUMNS = (
    "model_id",
    "task_id",
    "target_id",
    "target_family",
    "feature_set_id",
    "model_config_id",
    "feature_count",
    "feature_order_hash",
    "model_path",
    "model_sha256",
    "onnx_path",
    "onnx_sha256",
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
SCORE_COLUMNS = (
    "model_id",
    "task_id",
    "target_id",
    "target_family",
    "split",
    "rows",
    "accuracy",
    "balanced_accuracy",
    "macro_f1",
    "log_loss",
    "pred_short",
    "pred_flat",
    "pred_long",
    "true_short",
    "true_flat",
    "true_long",
    "signal_density",
    "claim_boundary",
)
CONTROL_SCORE_COLUMNS = (
    "model_id",
    "task_id",
    "target_id",
    "target_family",
    "control_id",
    "split",
    "actual_balanced_accuracy",
    "control_balanced_accuracy",
    "control_minus_actual",
    "control_status",
    "blocks_runtime_probe",
    "claim_boundary",
)
COST_COLUMNS = (
    "model_id",
    "task_id",
    "target_id",
    "target_family",
    "split",
    "cost_points",
    "trade_count",
    "signal_density",
    "net_proxy_return",
    "profit_factor",
    "expectancy",
    "max_drawdown",
    "recovery_factor",
    "cost_status",
    "blocks_runtime_probe",
    "claim_boundary",
)
RANK_COLUMNS = (
    "model_id",
    "task_id",
    "target_id",
    "split",
    "bucket_0_mean_future_abs_return",
    "bucket_1_mean_future_abs_return",
    "bucket_2_mean_future_abs_return",
    "monotonic_status",
    "claim_boundary",
)
RUNTIME_COLUMNS = (
    "policy_id",
    "model_id",
    "task_id",
    "target_family",
    "validation_gate_status",
    "extended_control_block_rows",
    "cost_block_rows",
    "rank_monotonicity_status",
    "mt5_probe_disposition",
    "release_blockers",
    "next_condition",
    "claim_boundary",
)
PROXY_COLUMNS = (
    "model_id",
    "task_id",
    "target_id",
    "target_family",
    "timestamp",
    "split",
    "p_short_or_low",
    "p_flat_or_mid",
    "p_long_or_high",
    "predicted_class",
    "predicted_label",
    "claim_boundary",
)
FEATURE_COLUMNS = (
    "source_path",
    "rows",
    "feature_set_rows",
    "trained_feature_sets",
    "nonfinite_rows",
    "compatibility_status",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def feature_order_hash(features: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(features).encode("utf-8")).hexdigest()


def read_source_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(SOURCE_MODEL_INPUT)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    frame["source_row_id"] = np.arange(len(frame), dtype=np.int64)
    return frame


def parse_feature_sets() -> list[dict[str, Any]]:
    manifest = read_json(FEATURE_CONTRACT_MANIFEST)
    rows = manifest.get("feature_sets") or []
    if not rows:
        raise RuntimeError("feature_contract_manifest.json has no feature_sets.")
    return [dict(row) for row in rows]


def build_model(model_config_id: str) -> Any:
    if model_config_id == "logreg_balanced_c075":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        C=0.75,
                        class_weight="balanced",
                        max_iter=1500,
                        random_state=337,
                        solver="lbfgs",
                    ),
                ),
            ]
        )
    if model_config_id == "extratrees_depth6_leaf160":
        return ExtraTreesClassifier(
            n_estimators=96,
            max_depth=6,
            min_samples_leaf=160,
            class_weight="balanced",
            random_state=337,
            n_jobs=-1,
        )
    raise ValueError(f"Unknown model_config_id: {model_config_id}")


def safe_balanced(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    if len(y_true) < 3 or len(np.unique(y_true)) < 2 or len(np.unique(y_pred)) < 2:
        return 0.0
    return float(balanced_accuracy_score(y_true, y_pred))


def safe_log_loss(y_true: np.ndarray, probabilities: np.ndarray) -> float:
    try:
        return float(log_loss(y_true, probabilities, labels=LABEL_ORDER))
    except ValueError:
        return float("nan")


def label_series_to_int(values: pd.Series) -> np.ndarray:
    return values.astype(str).map(LABEL_TO_INT).fillna(1).astype("int64").to_numpy()


def payoff_rank_to_3class(values: pd.Series) -> np.ndarray:
    buckets = pd.to_numeric(values, errors="coerce").fillna(1).astype("int64")
    return np.where(buckets <= 1, 0, np.where(buckets >= 3, 2, 1)).astype("int64")


def build_target_specs(cost_labels: pd.DataFrame, payoff_labels: pd.DataFrame, residual_labels: pd.DataFrame) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for cost_contract_id in sorted(cost_labels["cost_contract_id"].astype(str).unique()):
        rows = cost_labels.loc[cost_labels["cost_contract_id"].astype(str).eq(cost_contract_id)].sort_values("source_row_id")
        specs.append(
            {
                "target_id": f"cost_direction__{cost_contract_id}",
                "target_family": "cost_direction(비용 방향)",
                "target_source": rel(COST_TRADEABILITY_LABEL_FRAME),
                "cost_contract_id": cost_contract_id,
                "control_id": "",
                "source_row_id": rows["source_row_id"].to_numpy(dtype=np.int64),
                "y": label_series_to_int(rows["direction_label"]),
            }
        )
    for cost_contract_id in sorted(payoff_labels["cost_contract_id"].astype(str).unique()):
        rows = payoff_labels.loc[payoff_labels["cost_contract_id"].astype(str).eq(cost_contract_id)].sort_values("source_row_id")
        specs.append(
            {
                "target_id": f"payoff_rank3__{cost_contract_id}",
                "target_family": "payoff_rank3(보상 3분위 순위)",
                "target_source": rel(PAYOFF_RANK_LABEL_FRAME),
                "cost_contract_id": cost_contract_id,
                "control_id": "",
                "source_row_id": rows["source_row_id"].to_numpy(dtype=np.int64),
                "y": payoff_rank_to_3class(rows["payoff_rank_bucket"]),
            }
        )
    for control_id in sorted(residual_labels["control_id"].astype(str).unique()):
        rows = residual_labels.loc[residual_labels["control_id"].astype(str).eq(control_id)].sort_values("source_row_id")
        specs.append(
            {
                "target_id": f"control_residual__{control_id}",
                "target_family": "control_residual_direction(대조 잔차 방향)",
                "target_source": rel(CONTROL_RESIDUAL_LABEL_FRAME),
                "cost_contract_id": "cost2_primary_abstention",
                "control_id": control_id,
                "source_row_id": rows["source_row_id"].to_numpy(dtype=np.int64),
                "y": label_series_to_int(rows["residual_direction_label"]),
            }
        )
    return specs


def verify_target_alignment(spec: Mapping[str, Any], source_rows: int) -> None:
    row_ids = np.asarray(spec["source_row_id"], dtype=np.int64)
    if len(row_ids) != source_rows or not np.array_equal(row_ids, np.arange(source_rows, dtype=np.int64)):
        raise RuntimeError(f"Target alignment failed for {spec['target_id']}.")


def score_split(
    model_id: str,
    task_id: str,
    target_id: str,
    target_family: str,
    split: str,
    y_true: np.ndarray,
    probabilities: np.ndarray,
) -> dict[str, Any]:
    pred = np.asarray(LABEL_ORDER, dtype=np.int64)[probabilities.argmax(axis=1)]
    pred_counts = pd.Series(pred).value_counts().to_dict()
    true_counts = pd.Series(y_true).value_counts().to_dict()
    return {
        "model_id": model_id,
        "task_id": task_id,
        "target_id": target_id,
        "target_family": target_family,
        "split": split,
        "rows": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, pred)),
        "balanced_accuracy": safe_balanced(y_true, pred),
        "macro_f1": float(f1_score(y_true, pred, labels=LABEL_ORDER, average="macro")),
        "log_loss": safe_log_loss(y_true, probabilities),
        "pred_short": int(pred_counts.get(0, 0)),
        "pred_flat": int(pred_counts.get(1, 0)),
        "pred_long": int(pred_counts.get(2, 0)),
        "true_short": int(true_counts.get(0, 0)),
        "true_flat": int(true_counts.get(1, 0)),
        "true_long": int(true_counts.get(2, 0)),
        "signal_density": float((pred != 1).mean()),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def control_scores(
    model_id: str,
    task_id: str,
    target_id: str,
    target_family: str,
    split: str,
    y_true: np.ndarray,
    pred: np.ndarray,
    sidecar_split: pd.DataFrame,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for control_id, column in CONTROL_COLUMNS.items():
        control_y = label_series_to_int(sidecar_split[column])
        actual_balanced = safe_balanced(y_true, pred)
        control_balanced = safe_balanced(control_y, pred)
        passed = control_balanced < actual_balanced and control_balanced < 0.45
        rows.append(
            {
                "model_id": model_id,
                "task_id": task_id,
                "target_id": target_id,
                "target_family": target_family,
                "control_id": control_id,
                "split": split,
                "actual_balanced_accuracy": actual_balanced,
                "control_balanced_accuracy": control_balanced,
                "control_minus_actual": control_balanced - actual_balanced,
                "control_status": "passed_control_weakened" if passed else "block_control_alignment",
                "blocks_runtime_probe": str(not passed).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def trade_returns(future_returns: np.ndarray, pred: np.ndarray) -> np.ndarray:
    return np.where(pred == 2, future_returns, np.where(pred == 0, -future_returns, 0.0)).astype(float)


def max_drawdown(values: np.ndarray) -> float:
    if len(values) == 0:
        return 0.0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    return float(np.max(peak - curve))


def cost_rows(
    model_id: str,
    task_id: str,
    target_id: str,
    target_family: str,
    split: str,
    future_returns: np.ndarray,
    pred: np.ndarray,
    cost_unit: float,
) -> list[dict[str, Any]]:
    if target_family.startswith("payoff_rank3"):
        return [
            {
                "model_id": model_id,
                "task_id": task_id,
                "target_id": target_id,
                "target_family": target_family,
                "split": split,
                "cost_points": "",
                "trade_count": 0,
                "signal_density": 0.0,
                "net_proxy_return": 0.0,
                "profit_factor": 0.0,
                "expectancy": 0.0,
                "max_drawdown": 0.0,
                "recovery_factor": 0.0,
                "cost_status": "out_of_scope_rank_target(순위 타깃 단독 비용 곡선 제외)",
                "blocks_runtime_probe": "true",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    raw = trade_returns(future_returns, pred)
    trade_mask = pred != 1
    out: list[dict[str, Any]] = []
    for cost_points in COST_LEVELS:
        net = raw - (float(cost_points) * float(cost_unit) * trade_mask.astype(float))
        trade_net = net[trade_mask]
        gross_profit = float(trade_net[trade_net > 0].sum()) if len(trade_net) else 0.0
        gross_loss = float(-trade_net[trade_net < 0].sum()) if len(trade_net) else 0.0
        pf = gross_profit / gross_loss if gross_loss > 0 else (float("inf") if gross_profit > 0 else 0.0)
        dd = max_drawdown(net)
        total = float(net.sum())
        status = "passed_cost_shape" if len(trade_net) >= 50 and total > 0 and pf >= 1.05 else "block_cost_shape"
        out.append(
            {
                "model_id": model_id,
                "task_id": task_id,
                "target_id": target_id,
                "target_family": target_family,
                "split": split,
                "cost_points": cost_points,
                "trade_count": int(trade_mask.sum()),
                "signal_density": float(trade_mask.mean()),
                "net_proxy_return": total,
                "profit_factor": pf,
                "expectancy": float(trade_net.mean()) if len(trade_net) else 0.0,
                "max_drawdown": dd,
                "recovery_factor": total / dd if dd > 0 else 0.0,
                "cost_status": status,
                "blocks_runtime_probe": str(status != "passed_cost_shape").lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def rank_rows(
    model_id: str,
    task_id: str,
    target_id: str,
    target_family: str,
    split: str,
    future_abs_returns: np.ndarray,
    pred: np.ndarray,
) -> list[dict[str, Any]]:
    if not target_family.startswith("payoff_rank3"):
        return []
    means = []
    for bucket in (0, 1, 2):
        values = future_abs_returns[pred == bucket]
        means.append(float(values.mean()) if len(values) else 0.0)
    monotonic = means[0] <= means[1] <= means[2] and means[2] > 0
    return [
        {
            "model_id": model_id,
            "task_id": task_id,
            "target_id": target_id,
            "split": split,
            "bucket_0_mean_future_abs_return": means[0],
            "bucket_1_mean_future_abs_return": means[1],
            "bucket_2_mean_future_abs_return": means[2],
            "monotonic_status": "passed_rank_monotonic" if monotonic else "block_rank_not_monotonic",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_tasks(target_specs: Sequence[Mapping[str, Any]], feature_sets: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target in target_specs:
        for feature_set in feature_sets:
            features = [str(item) for item in feature_set["included_features_json"]]
            for model_spec in MODEL_SPECS:
                task_id = "__".join([target["target_id"], str(feature_set["feature_set_id"]), model_spec["model_config_id"]])
                rows.append(
                    {
                        "task_id": task_id,
                        "target_id": target["target_id"],
                        "target_family": target["target_family"],
                        "target_source": target["target_source"],
                        "cost_contract_id": target["cost_contract_id"],
                        "control_id": target["control_id"],
                        "feature_set_id": feature_set["feature_set_id"],
                        "model_config_id": model_spec["model_config_id"],
                        "feature_count": len(features),
                        "training_disposition": "queued_for_guarded_training",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return rows


def run_training() -> dict[str, Any]:
    io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    io_path(ONNX_DIR).mkdir(parents=True, exist_ok=True)
    source = read_source_frame()
    cost_labels = pd.read_parquet(io_path(COST_TRADEABILITY_LABEL_FRAME))
    payoff_labels = pd.read_parquet(io_path(PAYOFF_RANK_LABEL_FRAME))
    residual_labels = pd.read_parquet(io_path(CONTROL_RESIDUAL_LABEL_FRAME))
    sidecar = pd.read_csv(io_path(CONTROL_SIDECAR_MATRIX))
    sidecar = sidecar.sort_values("source_row_id").reset_index(drop=True)
    feature_sets = parse_feature_sets()
    target_specs = build_target_specs(cost_labels, payoff_labels, residual_labels)
    for spec in target_specs:
        verify_target_alignment(spec, len(source))
    task_rows = build_tasks(target_specs, feature_sets)
    task_by_id = {row["task_id"]: row for row in task_rows}
    target_by_id = {spec["target_id"]: spec for spec in target_specs}
    feature_by_id = {row["feature_set_id"]: row for row in feature_sets}
    split_masks = {split: source["split"].astype(str).eq(split).to_numpy() for split in ("train", "validation", "oos")}
    future_returns = pd.to_numeric(source["future_log_return_12"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    future_abs = np.abs(future_returns)
    manifest = read_json(OBJECTIVE_INPUT_MANIFEST)
    cost_unit = float(manifest.get("cost_proxy", {}).get("cost_point_to_return_unit_proxy") or 0.0)

    model_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    score_rows: list[dict[str, Any]] = []
    control_rows_out: list[dict[str, Any]] = []
    cost_rows_out: list[dict[str, Any]] = []
    rank_rows_out: list[dict[str, Any]] = []
    runtime_rows: list[dict[str, Any]] = []
    proxy_rows: list[dict[str, Any]] = []
    dynamic_artifacts: list[Path] = []
    nonfinite_rows = 0

    for index, task in enumerate(task_rows, start=1):
        target = target_by_id[task["target_id"]]
        feature_row = feature_by_id[task["feature_set_id"]]
        features = [str(item) for item in feature_row["included_features_json"]]
        X_df = source.loc[:, features].replace([np.inf, -np.inf], np.nan)
        nonfinite_rows += int(X_df.isna().any(axis=1).sum())
        X_all = X_df.fillna(0.0).to_numpy(dtype=np.float64)
        y_all = np.asarray(target["y"], dtype=np.int64)
        train_idx = np.flatnonzero(split_masks["train"])
        model = build_model(task["model_config_id"])
        model.fit(X_all[train_idx], y_all[train_idx])
        model_key = f"da{index:03d}"
        model_id = f"{model_key}__{task['target_id']}__{task['feature_set_id']}__{task['model_config_id']}"
        model_path = MODEL_DIR / f"{model_key}.joblib"
        onnx_path = ONNX_DIR / f"{model_key}.onnx"
        joblib.dump(model, io_path(model_path))
        export_sklearn_to_onnx_zipmap_disabled(model, onnx_path, feature_count=len(features), drop_label_output=True)
        dynamic_artifacts.extend([model_path, onnx_path])
        sample_idx = np.concatenate([np.flatnonzero(split_masks["train"])[:128], np.flatnonzero(split_masks["validation"])[:128], np.flatnonzero(split_masks["oos"])[:128]])
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
                "target_family": task["target_family"],
                "feature_set_id": task["feature_set_id"],
                "model_config_id": task["model_config_id"],
                "feature_count": len(features),
                "feature_order_hash": feature_order_hash(features),
                "model_path": rel(model_path),
                "model_sha256": sha256_file(model_path),
                "onnx_path": rel(onnx_path),
                "onnx_sha256": sha256_file(onnx_path),
                "train_rows": int(split_masks["train"].sum()),
                "validation_rows": int(split_masks["validation"].sum()),
                "oos_rows": int(split_masks["oos"].sum()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        validation_blocks = 0
        validation_cost_blocks = 0
        rank_statuses: list[str] = []
        validation_gate = "failed_validation_quality"
        for split in ("train", "validation", "oos"):
            idx = np.flatnonzero(split_masks[split])
            probs = ordered_sklearn_probabilities(model, X_all[idx], class_order=LABEL_ORDER)
            pred = np.asarray(LABEL_ORDER, dtype=np.int64)[probs.argmax(axis=1)]
            score = score_split(model_id, task["task_id"], task["target_id"], task["target_family"], split, y_all[idx], probs)
            score_rows.append(score)
            if split == "validation" and score["balanced_accuracy"] >= 0.40:
                validation_gate = "passed_validation_balanced"
            if split in {"validation", "oos"}:
                sidecar_split = sidecar.loc[sidecar["split"].astype(str).eq(split)].sort_values("source_row_id")
                controls = control_scores(model_id, task["task_id"], task["target_id"], task["target_family"], split, y_all[idx], pred, sidecar_split)
                control_rows_out.extend(controls)
                if split == "validation":
                    validation_blocks += sum(1 for row in controls if row["blocks_runtime_probe"] == "true")
            costs = cost_rows(model_id, task["task_id"], task["target_id"], task["target_family"], split, future_returns[idx], pred, cost_unit)
            cost_rows_out.extend(costs)
            if split == "validation":
                validation_cost_blocks += sum(1 for row in costs if row["blocks_runtime_probe"] == "true")
            ranks = rank_rows(model_id, task["task_id"], task["target_id"], task["target_family"], split, future_abs[idx], pred)
            rank_rows_out.extend(ranks)
            if split == "validation" and ranks:
                rank_statuses.extend(row["monotonic_status"] for row in ranks)
            if split == "oos":
                timestamps = source.loc[idx, "timestamp"].astype(str).to_numpy()
                for local_idx in range(len(idx)):
                    proxy_rows.append(
                        {
                            "model_id": model_id,
                            "task_id": task["task_id"],
                            "target_id": task["target_id"],
                            "target_family": task["target_family"],
                            "timestamp": timestamps[local_idx],
                            "split": "oos",
                            "p_short_or_low": probs[local_idx, 0],
                            "p_flat_or_mid": probs[local_idx, 1],
                            "p_long_or_high": probs[local_idx, 2],
                            "predicted_class": int(pred[local_idx]),
                            "predicted_label": INT_TO_LABEL[int(pred[local_idx])],
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )
        rank_status = ";".join(rank_statuses) if rank_statuses else "not_applicable"
        blockers = []
        if validation_gate != "passed_validation_balanced":
            blockers.append("validation_balanced_below_0p40")
        if validation_blocks:
            blockers.append("control_alignment_block")
        if validation_cost_blocks:
            blockers.append("cost_shape_block")
        if "block_rank_not_monotonic" in rank_status:
            blockers.append("rank_not_monotonic")
        runtime_rows.append(
            {
                "policy_id": f"policy::{model_key}",
                "model_id": model_id,
                "task_id": task["task_id"],
                "target_family": task["target_family"],
                "validation_gate_status": validation_gate,
                "extended_control_block_rows": validation_blocks,
                "cost_block_rows": validation_cost_blocks,
                "rank_monotonicity_status": rank_status,
                "mt5_probe_disposition": "review_eligible_no_auto_mt5_release" if not blockers else "held_for_review",
                "release_blockers": ";".join(blockers) or "none",
                "next_condition": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    feature_rows = [
        {
            "source_path": rel(SOURCE_MODEL_INPUT),
            "rows": int(len(source)),
            "feature_set_rows": len(feature_sets),
            "trained_feature_sets": len({row["feature_set_id"] for row in model_rows}),
            "nonfinite_rows": nonfinite_rows,
            "compatibility_status": "passed_with_zero_fill_recorded" if nonfinite_rows else "passed",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return {
        "task_rows": task_rows,
        "model_rows": model_rows,
        "parity_rows": parity_rows,
        "score_rows": score_rows,
        "control_rows": control_rows_out,
        "cost_rows": cost_rows_out,
        "rank_rows": rank_rows_out,
        "runtime_rows": runtime_rows,
        "proxy_rows": proxy_rows,
        "feature_rows": feature_rows,
        "dynamic_artifacts": dynamic_artifacts,
        "source_rows": int(len(source)),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]

    def row(gate_id: str, ok: bool, observed: Any, expected: str, effect: str) -> dict[str, str]:
        return {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": str(observed),
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    return [
        row("da_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CZ 입력과 원천 데이터를 연결한다."),
        row("da_gate_parent_points_to_da", final["cz_next_action"] == RUN_ID, final["cz_next_action"], RUN_ID, "CZ next_action(다음 행동)과 DA 실행을 맞춘다."),
        row("da_gate_tasks_materialized", final["task_rows"] == 42, final["task_rows"], "42", "7개 타깃 x 3개 피처 x 2개 모델을 고정한다."),
        row("da_gate_models_trained", final["trained_models"] == final["task_rows"], final["trained_models"], "task_rows", "모든 사전 선언 작업을 학습한다."),
        row("da_gate_onnx_parity", final["onnx_parity_passed"] == final["onnx_parity_rows"] and final["onnx_parity_rows"] > 0, f"{final['onnx_parity_passed']}/{final['onnx_parity_rows']}", "all parity passed", "Python/ONNX(파이썬/온엑스) 확률 출력을 맞춘다."),
        row("da_gate_scorecard_rows", final["scorecard_rows"] == final["trained_models"] * 3, final["scorecard_rows"], "models*3 splits", "train/validation/OOS(학습/검증/OOS) 점수를 모두 남긴다."),
        row("da_gate_control_rows", final["control_rows"] == final["trained_models"] * 2 * 3, final["control_rows"], "models*validation_oos*3 controls", "검증/OOS 대조 점수를 모두 남긴다."),
        row("da_gate_proxy_expected_rows", final["proxy_expected_rows"] == final["trained_models"] * 7584, final["proxy_expected_rows"], "models*oos_rows", "프록시 예상값을 모델별 OOS 행으로 남긴다."),
        row("da_gate_no_auto_mt5", final["auto_mt5_release_rows"] == 0, final["auto_mt5_release_rows"], "0", "검토 없이 MT5 탐침을 열지 않는다."),
        row("da_gate_no_selection", True, "candidate_selection=not_run;mt5=not_run", "no selection/MT5", "학습 결과를 즉시 운영 주장으로 바꾸지 않는다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    model_receipt = {
        "model_family": "logreg_balanced_c075 and extratrees_depth6_leaf160(로지스틱 회귀와 엑스트라 트리)",
        "target_and_label": "cost direction, payoff rank3, control residual direction(비용 방향, 보상 3분위, 대조 잔차 방향)",
        "split_method": "existing time split, train fit only(기존 시간 분할, 학습 적합 전용)",
        "selection_metric": "not_applicable_all_tasks_trained_no_selection(전체 작업 학습, 선택 없음)",
        "secondary_metrics": "balanced accuracy, control alignment, cost curve, rank monotonicity, ONNX parity(균형 정확도, 대조 정렬, 비용 곡선, 순위 단조성, ONNX 동등성)",
        "threshold_policy": "no threshold tuning; argmax diagnostic only(임계값 조정 없음, argmax 진단 전용)",
        "overfit_risk": "choosing from validation/OOS pockets after review(검증/OOS 포켓을 보고 선택하는 위험)",
        "calibration_risk": "model scores are rank diagnostics, not calibrated probability(모델 점수는 순위 진단이며 보정 확률 아님)",
        "comparison_baseline": PARENT_RUN_ID,
        "validation_judgment": "exploratory_training_review_required",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": rel(SOURCE_MODEL_INPUT),
        "time_axis": "timestamp UTC from source model input(원천 모델 입력의 UTC 시각)",
        "sample_scope": f"rows={final['source_rows']}; no post-2026-04-14 training data(2026-04-14 이후 학습 데이터 없음)",
        "missing_or_duplicate_check": "feature compatibility row records zero-fill count(피처 호환 행이 결측 대체 수를 기록)",
        "feature_label_boundary": "future_log_return_12 used only through CZ labels(future_log_return_12는 CZ 라벨로만 사용)",
        "split_boundary": "train fit; validation/OOS diagnostic only(학습 적합, 검증/OOS 진단 전용)",
        "leakage_risk": "review-driven model or feature selection(검토 기반 모델/피처 선택 위험)",
        "data_hash_or_identity": {rel(SOURCE_MODEL_INPUT): sha256_file(SOURCE_MODEL_INPUT)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": "new objective families trained after CX/CY/CZ(새 목표 계열 학습)",
        "comparison_baseline": PARENT_RUN_ID,
        "likely_drivers": "target objective, feature contract, model family(타깃 목표, 피처 계약, 모델 계열)",
        "segment_checks": "split, control, cost, rank monotonicity(분할, 대조, 비용, 순위 단조성)",
        "trade_shape": "proxy cost curve only; no MT5 fills(프록시 비용 곡선 전용, MT5 체결 없음)",
        "alternative_explanations": "serial dependence, stale feature carry, rank target non-directionality(연속 의존, 낡은 피처 이월, 순위 타깃 비방향성)",
        "attribution_confidence": "low_until_DB_review_and_MT5_probe(DB 검토와 MT5 탐침 전 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime_receipt = {
        "runtime_subject": "ONNX parity only; no MT5 runtime probe(ONNX 동등성 전용, MT5 런타임 탐침 없음)",
        "parity_check": f"{final['onnx_parity_passed']}/{final['onnx_parity_rows']}",
        "mt5_runtime_probe": "not_run",
        "usable_for": "DB review and possible no-selection probe package(DB 검토와 선택 없는 탐침 패키지 가능성)",
        "not_usable_for": "runtime authority, Forward Passed, live readiness(런타임 권위, 전진 통과, 실거래 준비)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "trained models, ONNX parity, scorecards, proxy expected(학습 모델, ONNX 동등성, 점수표, 프록시 예상값)",
        "evidence_missing": "DB review, MT5 runtime probe, forward execution(DB 검토, MT5 런타임 탐침, 전진 실행)",
        "judgment_label": "exploratory_training_completed_review_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "학습은 됐지만 아직 고를 단계가 아니라 실패 축을 먼저 리뷰해야 한다.",
    }
    paths = [
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(RUNTIME_RECEIPT, runtime_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifact_paths] + [rel(path) for path in paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_run_outputs_with_manifest_and_tracked_report(무시 실행 산출물은 목록으로 연결, 보고서는 추적)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DA Objective/Feature Training(목표/피처 학습)

## Conclusion(결론)

run337DA(337DA 실행)는 CZ objective/feature pivot inputs(목표/피처 전환 입력)로 `42`개 guarded candidates(방어 후보)를 학습하고 ONNX parity(ONNX 동등성)를 확인했다.

Effect(효과): 이제 DB review(DB 검토)에서 validation quality(검증 품질), control residual(대조 잔차), cost curve(비용 곡선), rank monotonicity(순위 단조성)를 분해할 수 있다. 아직 candidate selection(후보 선택), MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 주장은 없다.

## Result(결과)

- trained_models(학습 모델): `{final["trained_models"]}`
- ONNX parity(ONNX 동등성): `{final["onnx_parity_passed"]}/{final["onnx_parity_rows"]}`
- scorecard_rows(점수표 행): `{final["scorecard_rows"]}`
- control_rows(대조 행): `{final["control_rows"]}`
- cost_rows(비용 행): `{final["cost_rows"]}`
- rank_rows(순위 행): `{final["rank_rows"]}`
- review_eligible_rows(검토 가능 행): `{final["review_eligible_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- threshold_tuning(임계값 조정): `not_run`
- candidate_selection(후보 선택): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DA

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): ONNX 후보를 만들었지만 선택하지 않고 DB review(DB 검토)로 넘긴다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(FINAL_DECISION)}`
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
    workspace_text = re.sub(
        r"- >-\n  Stage337 run337DA focus complete:.*?(?=\n- >-|\n[A-Za-z0-9_]+:|\Z)",
        "",
        workspace_text,
        flags=re.S,
    )
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337DA focus complete: objective/feature contract pivot candidates(목표/피처 계약 전환 후보)를 "
        f"`{STATUS}`로 학습했다. Effect(효과): run337DB(337DB 실행)에서 validation/control/cost/rank/ONNX parity(검증/대조/비용/순위/ONNX 동등성)를 검토한다.\n"
    )
    workspace_text = workspace_text.replace("current_focus:\n", focus_entry, 1)
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
    current_text = re.sub(
        r"\n## Stage337 run337DA\(337DA 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CZ|\n## |\Z)",
        "\n",
        current_text,
        flags=re.S,
    )
    section = f"""
## Stage337 run337DA(337DA 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): guarded candidates(방어 후보) `42`개를 학습하고 ONNX parity(ONNX 동등성)를 확인했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337CZ(337CZ"
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
- actual_mt5_execution(실제 MT5 실행): `not_run_da_training_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 DA training review(DA 학습 검토)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337DA(337DA 실행) trained objective/feature" not in line)
    stage_entry = (
        f"- {TODAY}: run337DA(337DA 실행) trained objective/feature contract pivot candidates(목표/피처 계약 전환 후보). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(line for line in changelog_text.splitlines() if "Stage337 run337DA trained objective/feature" not in line)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DA trained objective/feature contract pivot candidates(목표/피처 계약 전환 후보) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "objective_feature_contract_pivot_training_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"trained_models={final['trained_models']};onnx={final['onnx_parity_passed']}/{final['onnx_parity_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_execution_model_validation_data_integrity_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__objective_feature_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "objective_feature_training",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "training_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "model_validation_control_cost_rank",
        "scoreboard_lane": "model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"trained_models={final['trained_models']};review_eligible={final['review_eligible_rows']}",
        "guardrail_kpi": "onnx_parity;controls;cost;no_mt5;no_selection",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__objective_feature_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_model_validation_data_integrity_artifact_lineage",
        "evidence_scope": "CZ inputs trained into guarded ONNX candidates",
        "kpi_scope": "model_validation_control_cost_rank",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__objective_feature_training",
        "family": "experiment_execution_model_validation_data_integrity_artifact_lineage",
        "question": "do objective feature pivot inputs train ONNX candidates without selection",
        "metric_scope": "training_scorecard_onnx_control_cost_rank",
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
    result = run_training()
    artifacts: list[Path] = [
        write_csv(TASK_MATRIX, TASK_COLUMNS, result["task_rows"]),
        write_csv(TRAINED_MODEL_MANIFEST, MODEL_COLUMNS, result["model_rows"]),
        write_csv(ONNX_PARITY, PARITY_COLUMNS, result["parity_rows"]),
        write_csv(TRAINING_SCORECARD, SCORE_COLUMNS, result["score_rows"]),
        write_csv(CONTROL_SCORECARD, CONTROL_SCORE_COLUMNS, result["control_rows"]),
        write_csv(COST_CURVE_SCORECARD, COST_COLUMNS, result["cost_rows"]),
        write_csv(RANK_MONOTONICITY_REVIEW, RANK_COLUMNS, result["rank_rows"]),
        write_csv(RUNTIME_DISPOSITION, RUNTIME_COLUMNS, result["runtime_rows"]),
        write_csv(PROXY_EXPECTED, PROXY_COLUMNS, result["proxy_rows"]),
        write_csv(FEATURE_COMPATIBILITY, FEATURE_COLUMNS, result["feature_rows"]),
    ]
    cz_final = read_json(CZ_FINAL)
    parity_passed = sum(1 for row in result["parity_rows"] if row["passed"] == "true")
    review_eligible = sum(1 for row in result["runtime_rows"] if row["mt5_probe_disposition"] == "review_eligible_no_auto_mt5_release")
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "cz_next_action": cz_final.get("next_action", ""),
        "source_rows": result["source_rows"],
        "task_rows": len(result["task_rows"]),
        "trained_models": len(result["model_rows"]),
        "onnx_parity_rows": len(result["parity_rows"]),
        "onnx_parity_passed": parity_passed,
        "scorecard_rows": len(result["score_rows"]),
        "control_rows": len(result["control_rows"]),
        "cost_rows": len(result["cost_rows"]),
        "rank_rows": len(result["rank_rows"]),
        "runtime_rows": len(result["runtime_rows"]),
        "proxy_expected_rows": len(result["proxy_rows"]),
        "review_eligible_rows": review_eligible,
        "auto_mt5_release_rows": 0,
        "model_training": "completed_guarded",
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
    artifacts.extend(result["dynamic_artifacts"])
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
