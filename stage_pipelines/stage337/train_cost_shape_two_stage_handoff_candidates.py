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
RUN_NUMBER = "run337DE"
RUN_ID = "run337DE_train_cost_shape_two_stage_handoff_candidates_without_db_v1"
PARENT_RUN_ID = "run337DD_materialize_cost_shape_two_stage_handoff_repair_inputs_without_db_v1"
NEXT_RUN_ID = "run337DF_review_cost_shape_two_stage_handoff_training_without_db_v1"
STATUS = "completed_stage337DE_cost_shape_two_stage_handoff_candidates_trained_review_required_no_selection_no_mt5"
JUDGMENT = "guarded_two_stage_cost_shape_candidates_trained_review_required"
DECISION = "stage337DE_open_run337DF_review_cost_shape_two_stage_handoff_training"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DE_cost_shape_two_stage_handoff_training_without_db_"
    "no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_no_forward_passed_"
    "no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_"
    "no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337DE_cost_shape_two_stage_handoff_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DE_cost_shape_two_stage_handoff_training.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

MODEL_INPUT = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
DD_DIR = STAGE_DIR / "02_runs" / "run337DD"
DD_FINAL = DD_DIR / "final_decision.json"
DD_GATES = DD_DIR / "required_gate_coverage_audit.csv"
DD_POINT_COST = DD_DIR / "point_cost_identity_sidecar.csv"
DD_STAGE1 = DD_DIR / "stage1_cost_tradeability_label_frame.parquet"
DD_STAGE2 = DD_DIR / "stage2_payoff_rank_handoff_frame.parquet"
DD_HANDOFF = DD_DIR / "two_stage_handoff_manifest.json"
DD_FIREWALL = DD_DIR / "control_firewall_audit.csv"
DD_QUEUE = DD_DIR / "run337DE_training_queue.csv"
CZ_FEATURE_SET = STAGE_DIR / "02_runs" / "run337CZ" / "feature_set_matrix.csv"

TASK_MATRIX = RUN_DIR / "two_stage_training_task_matrix.csv"
FEATURE_COMPATIBILITY = RUN_DIR / "feature_input_compatibility.csv"
TRAINED_MODEL_MANIFEST = RUN_DIR / "trained_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "onnx_parity_matrix.csv"
MODEL_SCORECARD = RUN_DIR / "model_metric_scorecard.csv"
SINGLE_COST_CURVE = RUN_DIR / "single_model_cost_curve_scorecard.csv"
RANK_REVIEW = RUN_DIR / "rank_monotonicity_review.csv"
TWO_STAGE_PAIR_SCORECARD = RUN_DIR / "two_stage_pair_scorecard.csv"
RUNTIME_DISPOSITION = RUN_DIR / "runtime_release_disposition.csv"
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
    MODEL_INPUT,
    DD_FINAL,
    DD_GATES,
    DD_POINT_COST,
    DD_STAGE1,
    DD_STAGE2,
    DD_HANDOFF,
    DD_FIREWALL,
    DD_QUEUE,
    CZ_FEATURE_SET,
)
OUTPUT_FILES = (
    TASK_MATRIX,
    FEATURE_COMPATIBILITY,
    TRAINED_MODEL_MANIFEST,
    ONNX_PARITY,
    MODEL_SCORECARD,
    SINGLE_COST_CURVE,
    RANK_REVIEW,
    TWO_STAGE_PAIR_SCORECARD,
    RUNTIME_DISPOSITION,
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
TARGET_FAMILIES = (
    "stage1_cost_gate(1단계 비용 게이트)",
    "stage2_payoff_rank5(2단계 보상 순위5)",
    "stage2_final_action(2단계 최종 행동)",
)
LABEL_MAPS = {
    "stage1_cost_gate(1단계 비용 게이트)": {"abstain": 0, "tradeable": 1},
    "stage2_payoff_rank5(2단계 보상 순위5)": {"rank_0": 0, "rank_1": 1, "rank_2": 2, "rank_3": 3, "rank_4": 4},
    "stage2_final_action(2단계 최종 행동)": {"short": 0, "flat": 1, "long": 2},
}
INT_TO_LABELS = {family: {value: key for key, value in mapping.items()} for family, mapping in LABEL_MAPS.items()}

TASK_COLUMNS = (
    "task_id",
    "target_id",
    "target_family",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "feature_count",
    "training_disposition",
    "claim_boundary",
)
FEATURE_COMPAT_COLUMNS = (
    "feature_set_id",
    "feature_count",
    "missing_features",
    "missing_count",
    "nonfinite_rows",
    "feature_order_hash",
    "claim_boundary",
)
MODEL_COLUMNS = (
    "model_id",
    "task_id",
    "target_id",
    "target_family",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "feature_count",
    "feature_order_hash",
    "class_order_json",
    "class_label_json",
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
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
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
COST_COLUMNS = (
    "model_id",
    "task_id",
    "target_family",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "split",
    "trade_count",
    "signal_density",
    "net_log_return_after_cost",
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
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "split",
    "bucket_0_mean_score",
    "bucket_1_mean_score",
    "bucket_2_mean_score",
    "bucket_3_mean_score",
    "bucket_4_mean_score",
    "monotonic_status",
    "claim_boundary",
)
PAIR_COLUMNS = (
    "pair_id",
    "stage1_model_id",
    "stage2_model_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "split",
    "trade_count",
    "signal_density",
    "net_log_return_after_cost",
    "profit_factor",
    "expectancy",
    "max_drawdown",
    "recovery_factor",
    "pair_status",
    "blocks_runtime_probe",
    "claim_boundary",
)
RUNTIME_COLUMNS = (
    "policy_id",
    "pair_id",
    "stage1_model_id",
    "stage2_model_id",
    "cost_policy_id",
    "feature_set_id",
    "model_config_id",
    "validation_status",
    "oos_status",
    "mt5_probe_disposition",
    "release_blockers",
    "next_condition",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")
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


def feature_order_hash(features: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(str(item) for item in features).encode("utf-8")).hexdigest()


def parse_json_list(value: str) -> list[str]:
    parsed = json.loads(value)
    return [str(item) for item in parsed]


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def read_source_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(MODEL_INPUT)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    frame["source_row_id"] = np.arange(len(frame), dtype=np.int64)
    return frame


def read_feature_sets(source: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows = read_csv(CZ_FEATURE_SET)
    feature_sets: list[dict[str, Any]] = []
    compat_rows: list[dict[str, Any]] = []
    for row in rows:
        features = parse_json_list(row["included_features_json"])
        missing = [feature for feature in features if feature not in source.columns]
        nonfinite_rows = 0
        if not missing:
            nonfinite_rows = int(source.loc[:, features].replace([np.inf, -np.inf], np.nan).isna().any(axis=1).sum())
        feature_sets.append(
            {
                "feature_set_id": row["feature_set_id"],
                "features": features,
                "feature_order_hash": feature_order_hash(features),
                "missing": missing,
                "nonfinite_rows": nonfinite_rows,
            }
        )
        compat_rows.append(
            {
                "feature_set_id": row["feature_set_id"],
                "feature_count": len(features),
                "missing_features": json.dumps(missing, ensure_ascii=False),
                "missing_count": len(missing),
                "nonfinite_rows": nonfinite_rows,
                "feature_order_hash": feature_order_hash(features),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return feature_sets, compat_rows


def build_model(config_id: str) -> Any:
    if config_id == "logreg_balanced_c075":
        return Pipeline(
            [
                ("scale", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        C=0.75,
                        class_weight="balanced",
                        max_iter=1000,
                        solver="lbfgs",
                        random_state=337,
                    ),
                ),
            ]
        )
    if config_id == "extratrees_depth6_leaf160":
        return ExtraTreesClassifier(
            n_estimators=160,
            max_depth=6,
            min_samples_leaf=160,
            class_weight="balanced",
            random_state=337,
            n_jobs=-1,
        )
    raise ValueError(f"Unknown model config: {config_id}")


def safe_log_loss(y_true: np.ndarray, probabilities: np.ndarray, class_order: Sequence[int]) -> float:
    try:
        return float(log_loss(y_true, probabilities, labels=list(class_order)))
    except ValueError:
        return float("nan")


def safe_balanced(y_true: np.ndarray, pred: np.ndarray) -> float:
    if len(np.unique(y_true)) < 2 or len(np.unique(pred)) < 1:
        return 0.0
    return float(balanced_accuracy_score(y_true, pred))


def labels_to_int(series: pd.Series, family: str) -> np.ndarray:
    mapping = LABEL_MAPS[family]
    return series.astype(str).map(mapping).fillna(0).to_numpy(dtype=np.int64)


def class_order_for(family: str) -> list[int]:
    return sorted(LABEL_MAPS[family].values())


def label_name(family: str, value: int) -> str:
    return INT_TO_LABELS[family].get(int(value), str(value))


def build_targets(stage1: pd.DataFrame, stage2: pd.DataFrame) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = []
    cost_policies = sorted(stage1["cost_policy_id"].astype(str).unique())
    for cost_policy in cost_policies:
        s1 = stage1.loc[stage1["cost_policy_id"].astype(str).eq(cost_policy)].sort_values("source_row_id")
        s2 = stage2.loc[stage2["cost_policy_id"].astype(str).eq(cost_policy)].sort_values("source_row_id")
        targets.append(
            {
                "target_id": f"stage1_cost_gate__{cost_policy}",
                "target_family": "stage1_cost_gate(1단계 비용 게이트)",
                "cost_policy_id": cost_policy,
                "label_source": "stage1_label",
                "y": labels_to_int(s1["stage1_label"], "stage1_cost_gate(1단계 비용 게이트)"),
            }
        )
        targets.append(
            {
                "target_id": f"stage2_payoff_rank5__{cost_policy}",
                "target_family": "stage2_payoff_rank5(2단계 보상 순위5)",
                "cost_policy_id": cost_policy,
                "label_source": "stage2_rank_label",
                "y": labels_to_int(s2["stage2_rank_label"], "stage2_payoff_rank5(2단계 보상 순위5)"),
            }
        )
        targets.append(
            {
                "target_id": f"stage2_final_action__{cost_policy}",
                "target_family": "stage2_final_action(2단계 최종 행동)",
                "cost_policy_id": cost_policy,
                "label_source": "final_action_label",
                "y": labels_to_int(s2["final_action_label"], "stage2_final_action(2단계 최종 행동)"),
            }
        )
    return targets


def build_task_rows(targets: Sequence[Mapping[str, Any]], feature_sets: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target in targets:
        for feature_set in feature_sets:
            if feature_set["missing"]:
                continue
            for model_spec in MODEL_SPECS:
                task_id = "__".join([target["target_id"], feature_set["feature_set_id"], model_spec["model_config_id"]])
                rows.append(
                    {
                        "task_id": task_id,
                        "target_id": target["target_id"],
                        "target_family": target["target_family"],
                        "cost_policy_id": target["cost_policy_id"],
                        "feature_set_id": feature_set["feature_set_id"],
                        "model_config_id": model_spec["model_config_id"],
                        "feature_count": len(feature_set["features"]),
                        "training_disposition": "queued_for_guarded_training(방어 학습 대기)",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
    return rows


def score_split(
    model_id: str,
    task: Mapping[str, Any],
    split: str,
    y_true: np.ndarray,
    probabilities: np.ndarray,
    class_order: Sequence[int],
) -> dict[str, Any]:
    pred = np.asarray(class_order, dtype=np.int64)[probabilities.argmax(axis=1)]
    pred_counts = {label_name(task["target_family"], key): int(value) for key, value in pd.Series(pred).value_counts().to_dict().items()}
    true_counts = {label_name(task["target_family"], key): int(value) for key, value in pd.Series(y_true).value_counts().to_dict().items()}
    signal_density = 0.0
    if task["target_family"].startswith("stage2_final_action"):
        signal_density = float((pred != LABEL_MAPS[task["target_family"]]["flat"]).mean())
    elif task["target_family"].startswith("stage1_cost_gate"):
        signal_density = float((pred == LABEL_MAPS[task["target_family"]]["tradeable"]).mean())
    return {
        "model_id": model_id,
        "task_id": task["task_id"],
        "target_id": task["target_id"],
        "target_family": task["target_family"],
        "cost_policy_id": task["cost_policy_id"],
        "feature_set_id": task["feature_set_id"],
        "model_config_id": task["model_config_id"],
        "split": split,
        "rows": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, pred)),
        "balanced_accuracy": safe_balanced(y_true, pred),
        "macro_f1": float(f1_score(y_true, pred, labels=list(class_order), average="macro")),
        "log_loss": safe_log_loss(y_true, probabilities, class_order),
        "pred_counts_json": json.dumps(pred_counts, ensure_ascii=False, sort_keys=True),
        "true_counts_json": json.dumps(true_counts, ensure_ascii=False, sort_keys=True),
        "signal_density": signal_density,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def max_drawdown(values: np.ndarray) -> float:
    if len(values) == 0:
        return 0.0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    return float(np.max(peak - curve))


def action_returns(action_int: np.ndarray, exact_returns: np.ndarray, cost_return: np.ndarray) -> np.ndarray:
    short = LABEL_MAPS["stage2_final_action(2단계 최종 행동)"]["short"]
    long = LABEL_MAPS["stage2_final_action(2단계 최종 행동)"]["long"]
    raw = np.where(action_int == long, exact_returns, np.where(action_int == short, -exact_returns, 0.0))
    trade_mask = (action_int == long) | (action_int == short)
    return raw - np.where(trade_mask, cost_return, 0.0)


def cost_stats(values: np.ndarray, trade_mask: np.ndarray) -> tuple[int, float, float, float, float, float, float]:
    trade_values = values[trade_mask]
    gross_profit = float(trade_values[trade_values > 0].sum()) if len(trade_values) else 0.0
    gross_loss = float(-trade_values[trade_values < 0].sum()) if len(trade_values) else 0.0
    pf = gross_profit / gross_loss if gross_loss > 0 else (float("inf") if gross_profit > 0 else 0.0)
    total = float(values.sum())
    expectancy = float(trade_values.mean()) if len(trade_values) else 0.0
    dd = max_drawdown(values)
    recovery = total / dd if dd > 0 else 0.0
    return int(trade_mask.sum()), float(trade_mask.mean()) if len(trade_mask) else 0.0, total, pf, expectancy, dd, recovery


def single_cost_row(
    model_id: str,
    task: Mapping[str, Any],
    split: str,
    pred: np.ndarray,
    stage1_split: pd.DataFrame,
) -> dict[str, Any]:
    cost_return = pd.to_numeric(stage1_split["round_trip_spread_return"], errors="coerce").fillna(0.0).to_numpy()
    cost_return += pd.to_numeric(stage1_split["extra_cost_return"], errors="coerce").fillna(0.0).to_numpy()
    exact = pd.to_numeric(stage1_split["exact_future_log_return_12"], errors="coerce").fillna(0.0).to_numpy()
    values = action_returns(pred, exact, cost_return)
    flat = LABEL_MAPS["stage2_final_action(2단계 최종 행동)"]["flat"]
    trade_mask = pred != flat
    trade_count, density, total, pf, expectancy, dd, recovery = cost_stats(values, trade_mask)
    status = "passed_cost_shape" if trade_count >= 50 and total > 0 and pf >= 1.05 else "block_cost_shape"
    return {
        "model_id": model_id,
        "task_id": task["task_id"],
        "target_family": task["target_family"],
        "cost_policy_id": task["cost_policy_id"],
        "feature_set_id": task["feature_set_id"],
        "model_config_id": task["model_config_id"],
        "split": split,
        "trade_count": trade_count,
        "signal_density": density,
        "net_log_return_after_cost": total,
        "profit_factor": pf,
        "expectancy": expectancy,
        "max_drawdown": dd,
        "recovery_factor": recovery,
        "cost_status": status,
        "blocks_runtime_probe": str(status != "passed_cost_shape").lower(),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def rank_review_row(model_id: str, task: Mapping[str, Any], split: str, pred: np.ndarray, stage2_split: pd.DataFrame) -> dict[str, Any]:
    score = pd.to_numeric(stage2_split["stage2_payoff_score"], errors="coerce").fillna(0.0).to_numpy()
    means = [float(score[pred == bucket].mean()) if np.any(pred == bucket) else 0.0 for bucket in range(5)]
    monotonic = all(means[i] <= means[i + 1] for i in range(4)) and means[-1] > 0.0
    return {
        "model_id": model_id,
        "task_id": task["task_id"],
        "cost_policy_id": task["cost_policy_id"],
        "feature_set_id": task["feature_set_id"],
        "model_config_id": task["model_config_id"],
        "split": split,
        "bucket_0_mean_score": means[0],
        "bucket_1_mean_score": means[1],
        "bucket_2_mean_score": means[2],
        "bucket_3_mean_score": means[3],
        "bucket_4_mean_score": means[4],
        "monotonic_status": "passed_rank_monotonic" if monotonic else "block_rank_not_monotonic",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def pair_cost_row(
    pair_id: str,
    stage1_model_id: str,
    stage2_model_id: str,
    cost_policy_id: str,
    feature_set_id: str,
    model_config_id: str,
    split: str,
    stage1_pred: np.ndarray,
    stage2_pred: np.ndarray,
    stage1_split: pd.DataFrame,
) -> dict[str, Any]:
    pass_value = LABEL_MAPS["stage1_cost_gate(1단계 비용 게이트)"]["tradeable"]
    flat = LABEL_MAPS["stage2_final_action(2단계 최종 행동)"]["flat"]
    final_action = np.where(stage1_pred == pass_value, stage2_pred, flat)
    cost_return = pd.to_numeric(stage1_split["round_trip_spread_return"], errors="coerce").fillna(0.0).to_numpy()
    cost_return += pd.to_numeric(stage1_split["extra_cost_return"], errors="coerce").fillna(0.0).to_numpy()
    exact = pd.to_numeric(stage1_split["exact_future_log_return_12"], errors="coerce").fillna(0.0).to_numpy()
    values = action_returns(final_action, exact, cost_return)
    trade_mask = final_action != flat
    trade_count, density, total, pf, expectancy, dd, recovery = cost_stats(values, trade_mask)
    status = "passed_pair_cost_shape" if trade_count >= 50 and total > 0 and pf >= 1.05 else "block_pair_cost_shape"
    return {
        "pair_id": pair_id,
        "stage1_model_id": stage1_model_id,
        "stage2_model_id": stage2_model_id,
        "cost_policy_id": cost_policy_id,
        "feature_set_id": feature_set_id,
        "model_config_id": model_config_id,
        "split": split,
        "trade_count": trade_count,
        "signal_density": density,
        "net_log_return_after_cost": total,
        "profit_factor": pf,
        "expectancy": expectancy,
        "max_drawdown": dd,
        "recovery_factor": recovery,
        "pair_status": status,
        "blocks_runtime_probe": str(status != "passed_pair_cost_shape").lower(),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def run_training() -> dict[str, Any]:
    io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    io_path(ONNX_DIR).mkdir(parents=True, exist_ok=True)
    source = read_source_frame()
    feature_sets, feature_compat = read_feature_sets(source)
    stage1 = pd.read_parquet(io_path(DD_STAGE1)).sort_values(["cost_policy_id", "source_row_id"]).reset_index(drop=True)
    stage2 = pd.read_parquet(io_path(DD_STAGE2)).sort_values(["cost_policy_id", "source_row_id"]).reset_index(drop=True)
    targets = build_targets(stage1, stage2)
    task_rows = build_task_rows(targets, feature_sets)
    write_csv(TASK_MATRIX, TASK_COLUMNS, task_rows)
    write_csv(FEATURE_COMPATIBILITY, FEATURE_COMPAT_COLUMNS, feature_compat)

    split_masks = {split: source["split"].astype(str).eq(split).to_numpy() for split in ("train", "validation", "oos")}
    target_by_id = {target["target_id"]: target for target in targets}
    feature_by_id = {row["feature_set_id"]: row for row in feature_sets}
    stage1_by_policy = {policy: frame.sort_values("source_row_id").reset_index(drop=True) for policy, frame in stage1.groupby("cost_policy_id")}
    stage2_by_policy = {policy: frame.sort_values("source_row_id").reset_index(drop=True) for policy, frame in stage2.groupby("cost_policy_id")}

    model_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    score_rows: list[dict[str, Any]] = []
    cost_rows: list[dict[str, Any]] = []
    rank_rows: list[dict[str, Any]] = []
    predictions: dict[tuple[str, str], dict[str, np.ndarray]] = {}
    dynamic_artifacts: list[Path] = []

    for index, task in enumerate(task_rows, start=1):
        target = target_by_id[task["target_id"]]
        feature_row = feature_by_id[task["feature_set_id"]]
        features = feature_row["features"]
        family = task["target_family"]
        class_order = class_order_for(family)
        X_all = source.loc[:, features].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float64)
        y_all = np.asarray(target["y"], dtype=np.int64)
        train_idx = np.flatnonzero(split_masks["train"])
        model = build_model(task["model_config_id"])
        model.fit(X_all[train_idx], y_all[train_idx])
        model_key = f"de{index:03d}"
        model_id = f"{model_key}__{task['target_id']}__{task['feature_set_id']}__{task['model_config_id']}"
        model_path = MODEL_DIR / f"{model_key}.joblib"
        onnx_path = ONNX_DIR / f"{model_key}.onnx"
        joblib.dump(model, io_path(model_path))
        export_sklearn_to_onnx_zipmap_disabled(model, onnx_path, feature_count=len(features), drop_label_output=True)
        dynamic_artifacts.extend([model_path, onnx_path])
        sample_idx = np.concatenate([np.flatnonzero(split_masks["train"])[:128], np.flatnonzero(split_masks["validation"])[:128], np.flatnonzero(split_masks["oos"])[:128]])
        parity = check_onnxruntime_probability_parity(model, onnx_path, X_all[sample_idx], class_order=class_order)
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
                "target_family": family,
                "cost_policy_id": task["cost_policy_id"],
                "feature_set_id": task["feature_set_id"],
                "model_config_id": task["model_config_id"],
                "feature_count": len(features),
                "feature_order_hash": feature_order_hash(features),
                "class_order_json": json.dumps(class_order, ensure_ascii=False),
                "class_label_json": json.dumps(INT_TO_LABELS[family], ensure_ascii=False, sort_keys=True),
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
        predictions[(model_id, "all")] = {}
        for split in ("train", "validation", "oos"):
            idx = np.flatnonzero(split_masks[split])
            probs = ordered_sklearn_probabilities(model, X_all[idx], class_order=class_order)
            pred = np.asarray(class_order, dtype=np.int64)[probs.argmax(axis=1)]
            predictions[(model_id, split)] = {"pred": pred}
            score_rows.append(score_split(model_id, task, split, y_all[idx], probs, class_order))
            if family.startswith("stage2_final_action"):
                cost_rows.append(single_cost_row(model_id, task, split, pred, stage1_by_policy[task["cost_policy_id"]].iloc[idx]))
            if family.startswith("stage2_payoff_rank5"):
                rank_rows.append(rank_review_row(model_id, task, split, pred, stage2_by_policy[task["cost_policy_id"]].iloc[idx]))

    pair_rows: list[dict[str, Any]] = []
    runtime_rows: list[dict[str, Any]] = []
    model_by_key = {
        (
            row["target_family"],
            row["cost_policy_id"],
            row["feature_set_id"],
            row["model_config_id"],
        ): row["model_id"]
        for row in model_rows
    }
    pair_index = 0
    for cost_policy in sorted(stage1_by_policy):
        for feature_set in sorted({row["feature_set_id"] for row in model_rows}):
            for model_spec in MODEL_SPECS:
                model_config_id = model_spec["model_config_id"]
                stage1_model = model_by_key.get(("stage1_cost_gate(1단계 비용 게이트)", cost_policy, feature_set, model_config_id))
                stage2_model = model_by_key.get(("stage2_final_action(2단계 최종 행동)", cost_policy, feature_set, model_config_id))
                if not stage1_model or not stage2_model:
                    continue
                pair_index += 1
                pair_id = f"pair{pair_index:03d}__{cost_policy}__{feature_set}__{model_config_id}"
                split_results: dict[str, dict[str, Any]] = {}
                for split in ("train", "validation", "oos"):
                    idx = np.flatnonzero(split_masks[split])
                    row = pair_cost_row(
                        pair_id,
                        stage1_model,
                        stage2_model,
                        cost_policy,
                        feature_set,
                        model_config_id,
                        split,
                        predictions[(stage1_model, split)]["pred"],
                        predictions[(stage2_model, split)]["pred"],
                        stage1_by_policy[cost_policy].iloc[idx],
                    )
                    pair_rows.append(row)
                    split_results[split] = row
                validation = split_results["validation"]
                oos = split_results["oos"]
                blockers = []
                if validation["pair_status"] != "passed_pair_cost_shape":
                    blockers.append("validation_pair_cost_shape_block")
                if oos["pair_status"] != "passed_pair_cost_shape":
                    blockers.append("oos_pair_cost_shape_block")
                if validation["trade_count"] < 50:
                    blockers.append("validation_trade_floor_block")
                disposition = "held_for_review"
                runtime_rows.append(
                    {
                        "policy_id": f"policy::{pair_index:03d}",
                        "pair_id": pair_id,
                        "stage1_model_id": stage1_model,
                        "stage2_model_id": stage2_model,
                        "cost_policy_id": cost_policy,
                        "feature_set_id": feature_set,
                        "model_config_id": model_config_id,
                        "validation_status": validation["pair_status"],
                        "oos_status": oos["pair_status"],
                        "mt5_probe_disposition": disposition,
                        "release_blockers": ";".join(blockers) if blockers else "review_required_no_auto_release",
                        "next_condition": NEXT_RUN_ID,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )

    artifacts = [
        TASK_MATRIX,
        FEATURE_COMPATIBILITY,
        write_csv(TRAINED_MODEL_MANIFEST, MODEL_COLUMNS, model_rows),
        write_csv(ONNX_PARITY, PARITY_COLUMNS, parity_rows),
        write_csv(MODEL_SCORECARD, SCORE_COLUMNS, score_rows),
        write_csv(SINGLE_COST_CURVE, COST_COLUMNS, cost_rows),
        write_csv(RANK_REVIEW, RANK_COLUMNS, rank_rows),
        write_csv(TWO_STAGE_PAIR_SCORECARD, PAIR_COLUMNS, pair_rows),
        write_csv(RUNTIME_DISPOSITION, RUNTIME_COLUMNS, runtime_rows),
    ]
    artifacts.extend(dynamic_artifacts)
    return {
        "source": source,
        "task_rows": task_rows,
        "feature_compat_rows": feature_compat,
        "model_rows": model_rows,
        "parity_rows": parity_rows,
        "score_rows": score_rows,
        "cost_rows": cost_rows,
        "rank_rows": rank_rows,
        "pair_rows": pair_rows,
        "runtime_rows": runtime_rows,
        "artifacts": artifacts,
    }


def gate_row(gate_id: str, ok: bool, observed: Any, expected: Any, effect: str) -> dict[str, str]:
    return {
        "gate_id": gate_id,
        "status": "passed" if ok else "failed",
        "observed": str(observed),
        "expected": str(expected),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        gate_row("de_gate_parent_points_to_de", final["dd_next_action"] == RUN_ID, final["dd_next_action"], RUN_ID, "DD next_action(다음 행동)과 DE 실행을 맞춘다."),
        gate_row("de_gate_trained_models_present", final["trained_models"] > 0, final["trained_models"], ">0", "후보 모델이 실제로 학습됐는지 확인한다."),
        gate_row("de_gate_onnx_parity", final["onnx_parity_passed"] == final["onnx_parity_rows"] and final["onnx_parity_rows"] > 0, f"{final['onnx_parity_passed']}/{final['onnx_parity_rows']}", "all", "Python/ONNX(파이썬/온엑스) 출력을 맞춘다."),
        gate_row("de_gate_feature_compatibility", final["feature_missing_rows"] == 0, final["feature_missing_rows"], 0, "피처 순서와 입력 호환성을 지킨다."),
        gate_row("de_gate_score_rows", final["score_rows"] > 0, final["score_rows"], ">0", "분할별 모델 성능을 기록한다."),
        gate_row("de_gate_pair_rows", final["pair_rows"] > 0, final["pair_rows"], ">0", "1단계/2단계 쌍의 비용 곡선을 만든다."),
        gate_row("de_gate_runtime_held", final["runtime_release_rows"] == 0, final["runtime_release_rows"], 0, "학습 직후 MT5 해제를 막는다."),
        gate_row("de_gate_rank_review", final["rank_review_rows"] > 0, final["rank_review_rows"], ">0", "순위 신호 단조성 검토를 남긴다."),
        gate_row("de_gate_no_selection", final["candidate_selection"] == "not_run", final["candidate_selection"], "not_run", "후보 선택을 다음 리뷰로 넘긴다."),
        gate_row("de_gate_no_mt5_probe", final["mt5_runtime_probe"] == "not_run", final["mt5_runtime_probe"], "not_run", "MT5 탐침을 리뷰 전 실행하지 않는다."),
    ]


def best_metric(rows: Sequence[Mapping[str, Any]], family: str, split: str) -> float:
    vals = [float(row["balanced_accuracy"]) for row in rows if row["target_family"] == family and row["split"] == split]
    return max(vals) if vals else 0.0


def best_pair_metric(rows: Sequence[Mapping[str, Any]], split: str, key: str) -> float:
    vals = [float(row[key]) for row in rows if row["split"] == split and math.isfinite(float(row[key]))]
    return max(vals) if vals else 0.0


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    model_receipt = {
        "model_family": "logistic_regression and extra_trees(로지스틱 회귀와 엑스트라 트리)",
        "target_and_label": "stage1 cost gate, stage2 payoff rank5, stage2 final action(1단계 비용 게이트, 2단계 보상 순위5, 2단계 최종 행동)",
        "split_method": "existing train/validation/oos, no threshold tuning(기존 학습/검증/OOS, 임계값 튜닝 없음)",
        "selection_metric": "not_applicable_no_selection(선택 없음)",
        "secondary_metrics": "ONNX parity, pair cost curve, rank monotonicity(ONNX 동등성, 쌍 비용 곡선, 순위 단조성)",
        "threshold_policy": "labels from DD train-only materialization(DD 학습 전용 물질화 라벨)",
        "overfit_risk": "choosing pair by validation/OOS pocket(검증/OOS 포켓으로 쌍 선택)",
        "calibration_risk": "scores are classifier outputs, not live calibrated probabilities(점수는 분류기 출력이지 실거래 보정 확률 아님)",
        "comparison_baseline": PARENT_RUN_ID,
        "validation_judgment": "training_completed_review_required",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(MODEL_INPUT), rel(DD_STAGE1), rel(DD_STAGE2), rel(DD_POINT_COST), rel(CZ_FEATURE_SET)],
        "time_axis": "inherits DD raw close identity and existing closed M5 split(DD 원천 종가 정체성과 기존 닫힌 M5 분할 상속)",
        "sample_scope": f"rows={final['source_rows']}; train/validation/oos",
        "missing_or_duplicate_check": f"feature_missing_rows={final['feature_missing_rows']}",
        "feature_label_boundary": "features from model input, labels from DD target frames(피처는 모델 입력, 라벨은 DD 타깃 프레임)",
        "split_boundary": "train fit only; validation/oos scoring only(학습 분할로만 fit, 검증/OOS는 채점만)",
        "leakage_risk": "pair selection before DF review(DF 리뷰 전 쌍 선택)",
        "data_hash_or_identity": {"model_input": sha256_file(MODEL_INPUT), "stage1": sha256_file(DD_STAGE1), "stage2": sha256_file(DD_STAGE2)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "attribution_subject": RUN_ID,
        "best_stage1_validation_balanced": final["best_stage1_validation_balanced"],
        "best_stage2_action_validation_balanced": final["best_stage2_action_validation_balanced"],
        "best_pair_validation_pf": final["best_pair_validation_pf"],
        "best_pair_oos_pf": final["best_pair_oos_pf"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime_receipt = {
        "runtime_subject": RUN_ID,
        "onnx_parity": f"{final['onnx_parity_passed']}/{final['onnx_parity_rows']}",
        "mt5_runtime_probe": "not_run",
        "runtime_release": "not_run_all_held_for_review(미실행, 전부 검토 보류)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "trained models, ONNX parity, metrics, pair scorecard(학습 모델, ONNX 동등성, 지표, 쌍 점수표)",
        "evidence_missing": "DF review, candidate decision, proxy/MT5 parity, MT5 probe(DF 리뷰, 후보 판정, 프록시/MT5 동등성, MT5 탐침)",
        "judgment_label": "training_completed_review_required",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "모델은 학습됐지만 선택이나 운영 판정은 아직 아닙니다.",
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
        "artifact_paths": [rel(path) for path in artifact_paths] + [rel(path) for path in paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_model_outputs_with_manifest_and_tracked_report(무시된 모델 산출물, 목록과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DE Cost Shape Two-Stage Handoff Training(비용 곡선 2단계 인계 학습)

## Conclusion(결론)

run337DE(337DE 실행)는 DD 입력으로 stage1 cost gate(1단계 비용 게이트), stage2 payoff rank(2단계 보상 순위), stage2 final action(2단계 최종 행동) 후보를 학습했다. ONNX parity(ONNX 동등성)는 `{final["onnx_parity_passed"]}/{final["onnx_parity_rows"]}`로 통과했다.

Effect(효과): 다음 run337DF(337DF 실행)에서 모델 품질, 비용 곡선, 순위 단조성, 쌍 인계 결과를 리뷰한다. 이번 실행은 candidate selection(후보 선택), MT5 probe(MT5 탐침), Forward/Goal(전진/목표)을 주장하지 않는다.

## Result(결과)

- trained_models(학습 모델): `{final["trained_models"]}`
- task_rows(작업 행): `{final["task_rows"]}`
- score_rows(점수 행): `{final["score_rows"]}`
- pair_rows(쌍 점수 행): `{final["pair_rows"]}`
- runtime_release_rows(런타임 해제 행): `{final["runtime_release_rows"]}`
- best_stage1_validation_balanced(최고 1단계 검증 균형정확도): `{final["best_stage1_validation_balanced"]}`
- best_stage2_action_validation_balanced(최고 2단계 행동 검증 균형정확도): `{final["best_stage2_action_validation_balanced"]}`
- best_pair_validation_pf(최고 쌍 검증 PF): `{final["best_pair_validation_pf"]}`
- best_pair_oos_pf(최고 쌍 OOS PF): `{final["best_pair_oos_pf"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- threshold_tuning(임계값 튜닝): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DE

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): cost shape two-stage handoff(비용 곡선 2단계 인계) 후보를 학습하고 DF 리뷰로 넘긴다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(TWO_STAGE_PAIR_SCORECARD)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337DE focus complete: cost shape two-stage handoff candidates(비용 곡선 2단계 인계 후보)를 `{STATUS}`로 학습했다. "
        f"Effect(효과): run337DF(337DF 실행)에서 ONNX parity/cost curve/rank/pair attribution(ONNX 동등성/비용 곡선/순위/쌍 귀속)을 검토한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DE focus complete")
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
## Stage337 run337DE(337DE 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): stage1/stage2 cost-shape handoff(1/2단계 비용 곡선 인계) 후보 `{final["trained_models"]}`개를 학습했고 ONNX parity(ONNX 동등성)를 확인했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DD(337DD"
    if "## Stage337 run337DE(337DE 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_de_training_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 cost shape two-stage handoff training review(비용 곡선 2단계 인계 학습 검토)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337DE(337DE 실행) trained cost shape two-stage handoff candidates(비용 곡선 2단계 인계 후보). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DE(337DE 실행) trained cost shape"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DE trained cost shape two-stage handoff candidates(비용 곡선 2단계 인계 후보) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DE trained cost shape"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "cost_shape_two_stage_handoff_training_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"trained_models={final['trained_models']};onnx={final['onnx_parity_passed']}/{final['onnx_parity_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_performance_attribution_runtime_parity_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__two_stage_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "two_stage_training",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "training_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "model_metrics_pair_proxy_cost",
        "scoreboard_lane": "model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_pair_validation_pf={final['best_pair_validation_pf']};best_pair_oos_pf={final['best_pair_oos_pf']}",
        "guardrail_kpi": "onnx_parity;no_selection;no_mt5;runtime_held",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__two_stage_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_performance_attribution_runtime_parity_artifact_lineage",
        "evidence_scope": "DD inputs trained into two-stage cost-shape candidates",
        "kpi_scope": "model_metrics_pair_proxy_cost_no_mt5",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__two_stage_training",
        "family": "model_validation_performance_attribution_runtime_parity_artifact_lineage",
        "question": "can two-stage cost-shape labels train candidates without runtime release",
        "metric_scope": "onnx_parity_model_metrics_pair_cost_curve",
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
    dd_final = read_json(DD_FINAL)
    result = run_training()
    parity_passed = sum(1 for row in result["parity_rows"] if str(row["passed"]).lower() == "true")
    runtime_release_rows = sum(1 for row in result["runtime_rows"] if row["mt5_probe_disposition"] != "held_for_review")
    feature_missing_rows = sum(1 for row in result["feature_compat_rows"] if int(row["missing_count"]) > 0)
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "dd_next_action": dd_final.get("next_action", ""),
        "source_rows": int(len(result["source"])),
        "task_rows": len(result["task_rows"]),
        "trained_models": len(result["model_rows"]),
        "onnx_parity_rows": len(result["parity_rows"]),
        "onnx_parity_passed": parity_passed,
        "feature_missing_rows": feature_missing_rows,
        "score_rows": len(result["score_rows"]),
        "single_cost_rows": len(result["cost_rows"]),
        "rank_review_rows": len(result["rank_rows"]),
        "pair_rows": len(result["pair_rows"]),
        "runtime_rows": len(result["runtime_rows"]),
        "runtime_release_rows": runtime_release_rows,
        "best_stage1_validation_balanced": best_metric(result["score_rows"], "stage1_cost_gate(1단계 비용 게이트)", "validation"),
        "best_stage2_action_validation_balanced": best_metric(result["score_rows"], "stage2_final_action(2단계 최종 행동)", "validation"),
        "best_stage2_rank_validation_balanced": best_metric(result["score_rows"], "stage2_payoff_rank5(2단계 보상 순위5)", "validation"),
        "best_pair_validation_pf": best_pair_metric(result["pair_rows"], "validation", "profit_factor"),
        "best_pair_oos_pf": best_pair_metric(result["pair_rows"], "oos", "profit_factor"),
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
    artifacts = list(result["artifacts"])
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
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
