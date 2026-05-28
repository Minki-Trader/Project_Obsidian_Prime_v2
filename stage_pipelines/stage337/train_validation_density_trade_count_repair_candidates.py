from __future__ import annotations

import csv
import json
import re
import sys
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

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.models.onnx_bridge import (  # noqa: E402
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage337 import review_validation_density_trade_count_repair_inputs as ed  # noqa: E402
from stage_pipelines.stage337 import train_guarded_transfer_density_control_repair_candidates as dz  # noqa: E402
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
STAGE_ID = ed.STAGE_ID
RUN_NUMBER = "run337EE"
RUN_ID = "run337EE_train_validation_density_trade_count_repair_candidates_without_db_v1"
PARENT_RUN_ID = ed.RUN_ID
NEXT_RUN_ID = "run337EF_review_validation_density_trade_count_repair_training_without_db_v1"
STATUS = "completed_stage337EE_validation_density_trade_count_repair_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5"
JUDGMENT = "eligible_extratrees_candidates_trained_with_onnx_parity_review_required"
DECISION = "stage337EE_open_run337EF_review_validation_density_trade_count_repair_training"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EE_validation_density_trade_count_repair_training_without_db_"
    "train_only_reviewed_weights_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ed.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEWS_DIR = ed.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EE_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337EE_training.md"
SELECTED_STATUS = ed.SELECTED_STATUS
STAGE_BRIEF = ed.STAGE_BRIEF
WORKSPACE_STATE = ed.WORKSPACE_STATE
CURRENT_STATE = ed.CURRENT_STATE
CHANGELOG = ed.CHANGELOG
RUN_REGISTRY = ed.RUN_REGISTRY
ALPHA_LEDGER = ed.ALPHA_LEDGER
ARTIFACT_REGISTRY = ed.ARTIFACT_REGISTRY
STAGE_LEDGER = ed.STAGE_LEDGER

ED_FINAL = ed.FINAL_DECISION
ED_GATES = ed.REQUIRED_GATE_AUDIT
ED_QUEUE = ed.EE_QUEUE
TRAINING_ELIGIBILITY = ed.TRAINING_ELIGIBILITY_MATRIX
TRAINING_FEATURE_EXCLUSION = ed.TRAINING_FEATURE_EXCLUSION
REPAIR_FRAME = ed.REPAIR_FRAME
TASK_MATRIX = ed.TASK_MATRIX
SOURCE_MODEL_INPUT = dz.SOURCE_MODEL_INPUT
FEATURE_SET_MATRIX = dz.FEATURE_SET_MATRIX
FIREWALL_CARRY = ed.FIREWALL_CARRY
GUARD_MATRIX = ed.GUARD_MATRIX

EE_TASK_MATRIX = RUN_DIR / "ee_training_task_matrix.csv"
FEATURE_COMPATIBILITY = RUN_DIR / "feature_input_compatibility.csv"
SAMPLE_WEIGHT_AUDIT = RUN_DIR / "sample_weight_audit.csv"
TRAINED_MODEL_MANIFEST = RUN_DIR / "trained_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "onnx_parity_matrix.csv"
CANDIDATE_CLASSIFICATION_SCORECARD = RUN_DIR / "candidate_classification_scorecard.csv"
PROXY_TRADE_SCORECARD = RUN_DIR / "proxy_trade_scorecard.csv"
NEGATIVE_CONTROL_SCORECARD = RUN_DIR / "negative_control_scorecard.csv"
DENSITY_GUARD_AUDIT = RUN_DIR / "density_guard_audit.csv"
RUNTIME_FIREWALL_REVIEW = RUN_DIR / "runtime_firewall_review.csv"
RELEASE_DISPOSITION = RUN_DIR / "training_release_disposition.csv"
EF_QUEUE = RUN_DIR / "run337EF_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    ED_FINAL,
    ED_GATES,
    ED_QUEUE,
    TRAINING_ELIGIBILITY,
    TRAINING_FEATURE_EXCLUSION,
    REPAIR_FRAME,
    TASK_MATRIX,
    SOURCE_MODEL_INPUT,
    FEATURE_SET_MATRIX,
    FIREWALL_CARRY,
    GUARD_MATRIX,
)
OUTPUT_FILES = (
    EE_TASK_MATRIX,
    FEATURE_COMPATIBILITY,
    SAMPLE_WEIGHT_AUDIT,
    TRAINED_MODEL_MANIFEST,
    ONNX_PARITY,
    CANDIDATE_CLASSIFICATION_SCORECARD,
    PROXY_TRADE_SCORECARD,
    NEGATIVE_CONTROL_SCORECARD,
    DENSITY_GUARD_AUDIT,
    RUNTIME_FIREWALL_REVIEW,
    RELEASE_DISPOSITION,
    EF_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
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

TASK_COLUMNS = (
    "task_id",
    "target_id",
    "cost_policy_id",
    "feature_set_id",
    "model_variant_id",
    "objective_contract_id",
    "feature_count",
    "feature_order_hash",
    "training_disposition",
    "claim_boundary",
)
FEATURE_COLUMNS = (
    "feature_set_id",
    "feature_count",
    "missing_count",
    "missing_features",
    "nonfinite_rows",
    "feature_order_hash",
    "claim_boundary",
)
WEIGHT_COLUMNS = (
    "task_id",
    "cost_policy_id",
    "objective_contract_id",
    "train_rows",
    "weight_column",
    "weight_min",
    "weight_mean",
    "weight_max",
    "nonfinite_weights",
    "claim_boundary",
)
MODEL_COLUMNS = (
    "model_id",
    "task_id",
    "target_id",
    "cost_policy_id",
    "feature_set_id",
    "model_variant_id",
    "objective_contract_id",
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
CLASS_COLUMNS = (
    "model_id",
    "task_id",
    "cost_policy_id",
    "feature_set_id",
    "model_variant_id",
    "objective_contract_id",
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
TRADE_COLUMNS = (
    "model_id",
    "task_id",
    "cost_policy_id",
    "feature_set_id",
    "model_variant_id",
    "objective_contract_id",
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
FIREWALL_COLUMNS = (
    "firewall_id",
    "blocked_action_or_claim",
    "blocked_reason",
    "review_status",
    "effect",
    "claim_boundary",
)
RELEASE_COLUMNS = (
    "model_id",
    "task_id",
    "validation_pf",
    "oos_pf",
    "validation_trade_count",
    "oos_trade_count",
    "validation_balanced_accuracy",
    "control_block_rows",
    "density_pressure_rows",
    "release_candidate_rows",
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


MODEL_VARIANTS = {
    "extratrees_depth7_leaf80_trade_lift": {"n_estimators": 144, "max_depth": 7, "min_samples_leaf": 80},
    "extratrees_depth6_leaf90_density_guard": {"n_estimators": 144, "max_depth": 6, "min_samples_leaf": 90},
    "extratrees_depth8_leaf100_payoff_tail": {"n_estimators": 180, "max_depth": 8, "min_samples_leaf": 100},
}
WEIGHT_COLUMNS_BY_OBJECTIVE = {
    "train_only_near_margin_trade_support": "near_margin_trade_support_weight",
    "train_only_density_tempered_class_prior": "density_tempered_weight",
    "train_only_payoff_tail_offense": "payoff_tail_offense_weight",
}


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def build_model(variant_id: str) -> ExtraTreesClassifier:
    spec = MODEL_VARIANTS[variant_id]
    return ExtraTreesClassifier(
        n_estimators=spec["n_estimators"],
        max_depth=spec["max_depth"],
        min_samples_leaf=spec["min_samples_leaf"],
        class_weight="balanced",
        random_state=337,
        n_jobs=-1,
    )


def read_eligible_tasks() -> list[dict[str, Any]]:
    task_by_id = {row["task_id"]: row for row in read_csv(TASK_MATRIX)}
    rows: list[dict[str, Any]] = []
    for row in read_csv(TRAINING_ELIGIBILITY):
        if row.get("training_eligibility_status") != "eligible_guarded_training":
            continue
        task = dict(task_by_id[row["task_id"]])
        variant_id = str(task["model_variant_id"])
        if variant_id not in MODEL_VARIANTS:
            continue
        task["model_config_id"] = variant_id
        task["weight_policy_id"] = str(task["objective_contract_id"])
        task["training_disposition"] = "queued_guarded_training_no_selection(방어 학습 대기, 선택 없음)"
        rows.append(task)
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
        "model_variant_id": task["model_variant_id"],
        "objective_contract_id": task["objective_contract_id"],
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
        "model_variant_id": task["model_variant_id"],
        "objective_contract_id": task["objective_contract_id"],
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
                "effect": "shifted/noise/block controls(이동/소음/차단 대조)를 선택 전 점수화한다.",
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


def sample_weights_for_task(repair_frame: pd.DataFrame, source: pd.DataFrame, task: Mapping[str, Any]) -> tuple[np.ndarray, dict[str, Any]]:
    weights = np.ones(len(source), dtype=np.float64)
    cost_policy = str(task["cost_policy_id"])
    objective = str(task["objective_contract_id"])
    weight_column = WEIGHT_COLUMNS_BY_OBJECTIVE[objective]
    scoped = repair_frame.loc[repair_frame["cost_policy_id"].astype(str).eq(cost_policy), ["source_row_id", weight_column]].copy()
    scoped = scoped.drop_duplicates("source_row_id").set_index("source_row_id")
    train_mask = source["split"].astype(str).eq("train")
    train_ids = source.loc[train_mask, "source_row_id"].astype(int).to_numpy()
    task_weights = scoped.reindex(train_ids)[weight_column].fillna(1.0).to_numpy(dtype=np.float64)
    task_weights = np.clip(task_weights, 0.25, 4.0)
    weights[train_ids] = task_weights
    audit = {
        "task_id": task["task_id"],
        "cost_policy_id": cost_policy,
        "objective_contract_id": objective,
        "train_rows": int(len(train_ids)),
        "weight_column": weight_column,
        "weight_min": float(task_weights.min()) if len(task_weights) else 0.0,
        "weight_mean": float(task_weights.mean()) if len(task_weights) else 0.0,
        "weight_max": float(task_weights.max()) if len(task_weights) else 0.0,
        "nonfinite_weights": int((~np.isfinite(task_weights)).sum()),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return weights, audit


def build_firewall_review() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv(FIREWALL_CARRY):
        rows.append(
            {
                "firewall_id": row.get("firewall_id", ""),
                "blocked_action_or_claim": row.get("blocked_action_or_claim", ""),
                "blocked_reason": row.get("blocked_reason", ""),
                "review_status": "active_no_release",
                "effect": "학습 결과가 선택/MT5/Forward(전진) 주장으로 번지는 것을 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_ef_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337EF_review_trained_candidates",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review trained validation-density/trade-count repair candidates(학습된 검증-밀도/거래수 수리 후보 검토).",
            "required_inputs": f"{rel(TRAINED_MODEL_MANIFEST)};{rel(ONNX_PARITY)};{rel(PROXY_TRADE_SCORECARD)}",
            "required_outputs": "candidate_training_review.csv;release_lock_review.csv",
            "blocked_if_missing": "model manifest, ONNX parity, scorecards(모델 목록, ONNX 동등성, 점수표).",
            "forbidden_action": "no selection or MT5 before EF review(EF 검토 전 선택/MT5 금지).",
            "effect": "학습 결과를 바로 운영 주장으로 넘기지 않고 검토한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337EF_review_density_controls",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review density pressure and negative controls(밀도 압력과 부정 대조 검토).",
            "required_inputs": f"{rel(DENSITY_GUARD_AUDIT)};{rel(NEGATIVE_CONTROL_SCORECARD)}",
            "required_outputs": "density_control_review.csv",
            "blocked_if_missing": "density/control scorecards(밀도/대조 점수표).",
            "forbidden_action": "no control relaxation(대조 완화 금지).",
            "effect": "EA 실패를 반복한 후보를 차단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def train_and_score() -> dict[str, Any]:
    io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    io_path(ONNX_DIR).mkdir(parents=True, exist_ok=True)
    source = dz.read_source_frame()
    feature_sets, compat_rows = dz.read_feature_sets(source)
    targets = dz.read_targets()
    tasks = read_eligible_tasks()
    repair_frame = pd.read_parquet(io_path(REPAIR_FRAME))
    split_masks = {split: source["split"].astype(str).eq(split).to_numpy() for split in ("train", "validation", "oos")}
    feature_by_id = {row["feature_set_id"]: row for row in feature_sets}
    target_by_cost = {str(row["cost_policy_id"]): row for row in targets}

    model_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    class_rows: list[dict[str, Any]] = []
    trade_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    release_rows: list[dict[str, Any]] = []
    weight_rows: list[dict[str, Any]] = []
    dynamic_artifacts: list[Path] = []

    for index, task in enumerate(tasks, start=1):
        feature_row = feature_by_id[str(task["feature_set_id"])]
        target = target_by_cost[str(task["cost_policy_id"])]
        features = feature_row["features"]
        x_all = source.loc[:, features].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float64)
        y_all = np.asarray(target["y"], dtype=np.int64)
        sample_weight, weight_audit = sample_weights_for_task(repair_frame, source, task)
        weight_rows.append(weight_audit)
        model = build_model(str(task["model_variant_id"]))
        train_idx = np.flatnonzero(split_masks["train"])
        model.fit(x_all[train_idx], y_all[train_idx], sample_weight=sample_weight[train_idx])
        model_key = f"ee{index:03d}"
        model_id = (
            f"{model_key}__{task['target_id']}__{task['cost_policy_id']}__{task['feature_set_id']}__"
            f"{task['model_variant_id']}__{task['objective_contract_id']}"
        )
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
        parity = check_onnxruntime_probability_parity(model, onnx_path, x_all[sample_idx], class_order=LABEL_ORDER)
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
                "model_variant_id": task["model_variant_id"],
                "objective_contract_id": task["objective_contract_id"],
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

        split_scores: dict[str, dict[str, Any]] = {}
        validation_control_blocks = 0
        for split in ("train", "validation", "oos"):
            idx = np.flatnonzero(split_masks[split])
            probs = ordered_sklearn_probabilities(model, x_all[idx], class_order=LABEL_ORDER)
            pred = np.asarray(LABEL_ORDER, dtype=np.int64)[probs.argmax(axis=1)]
            y_true = y_all[idx]
            class_score = score_classification(model_id, task, split, y_true, probs)
            trade_score = score_trades(model_id, task, split, pred, target["future_returns"][idx], target["cost_returns"][idx])
            class_rows.append(class_score)
            trade_rows.append(trade_score)
            split_scores[split] = {**class_score, **{f"trade_{key}": value for key, value in trade_score.items()}}
            if split in {"validation", "oos"}:
                controls = score_controls(model_id, task, split, pred, y_true, target["source_row_id"][idx], float(class_score["balanced_accuracy"]))
                control_rows.extend(controls)
                if split == "validation":
                    validation_control_blocks += sum(1 for row in controls if row["blocks_training_review"] == "true")

        validation = split_scores["validation"]
        oos = split_scores["oos"]
        blockers = ["EF_review_required_no_auto_release"]
        if float(validation["trade_profit_factor"]) < 1.05:
            blockers.append("validation_pf_below_1p05")
        if int(validation["trade_trade_count"]) < 500:
            blockers.append("validation_trade_count_below_500")
        if validation_control_blocks:
            blockers.append("negative_control_alignment")
        if float(oos["trade_profit_factor"]) > 1.5 and int(oos["trade_trade_count"]) < 100:
            blockers.append("thin_oos_pocket_quarantine")
        release_rows.append(
            {
                "model_id": model_id,
                "task_id": task["task_id"],
                "validation_pf": validation["trade_profit_factor"],
                "oos_pf": oos["trade_profit_factor"],
                "validation_trade_count": validation["trade_trade_count"],
                "oos_trade_count": oos["trade_trade_count"],
                "validation_balanced_accuracy": validation["balanced_accuracy"],
                "control_block_rows": validation_control_blocks,
                "density_pressure_rows": 0,
                "release_candidate_rows": 0,
                "release_disposition": "held_for_EF_review_no_selection",
                "release_blockers": ";".join(blockers),
                "next_condition": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    density_rows = build_density_rows(trade_rows)
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
        "tasks": tasks,
        "compat_rows": compat_rows,
        "weight_rows": weight_rows,
        "model_rows": model_rows,
        "parity_rows": parity_rows,
        "class_rows": class_rows,
        "trade_rows": trade_rows,
        "control_rows": control_rows,
        "density_rows": density_rows,
        "release_rows": release_rows,
        "firewall_rows": build_firewall_review(),
        "queue_rows": build_ef_queue(),
        "dynamic_artifacts": dynamic_artifacts,
    }


def best_by(rows: Sequence[Mapping[str, Any]], key: str) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(rows, key=lambda row: float(row.get(key) or 0))


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", "필수 ED/EC 입력이 있어야 학습이 닫힌다."),
        ("parent_ed_gates_passed", final["ed_failed_gate_rows"] == 0, str(final["ed_failed_gate_rows"]), "0", "부모 ED 검토 게이트가 통과해야 한다."),
        ("parent_next_action_matches", final["ed_next_action"] == RUN_ID, str(final["ed_next_action"]), RUN_ID, "라우팅이 EE로 정확히 이어졌는지 본다."),
        ("eligible_tasks_loaded", final["task_rows"] == 81, str(final["task_rows"]), "81", "ED가 허용한 작업만 학습한다."),
        ("trained_models_match_tasks", final["trained_models"] == final["task_rows"], f"{final['trained_models']}/{final['task_rows']}", "all", "모든 적격 작업이 학습됐는지 확인한다."),
        ("onnx_parity_all_passed", final["onnx_failed_rows"] == 0 and final["onnx_passed_rows"] == final["onnx_rows"], f"{final['onnx_passed_rows']}/{final['onnx_rows']}", "all", "Python/ONNX 확률 동등성을 확인한다."),
        ("validation_score_rows", final["validation_trade_rows"] == final["trained_models"], str(final["validation_trade_rows"]), "trained_models", "모든 후보에 검증 거래 점수가 있어야 한다."),
        ("release_locked", final["release_candidate_rows"] == 0 and final["candidate_selection"] == "not_run", f"release={final['release_candidate_rows']};selection={final['candidate_selection']}", "0/not_run", "EE는 학습만 하고 선택하지 않는다."),
        ("firewall_active", final["firewall_rows"] >= 5, str(final["firewall_rows"]), ">=5", "해제 금지 방화벽을 유지한다."),
        ("ef_queue_materialized", final["ef_queue_rows"] == 2, str(final["ef_queue_rows"]), "2", "EF 검토 큐를 연다."),
        (
            "no_forbidden_claim",
            final["threshold_tuning"] == "not_run"
            and final["candidate_selection"] == "not_run"
            and final["mt5_runtime_probe"] == "not_run"
            and final["goal_achieve"] == "not_claimed",
            f"threshold={final['threshold_tuning']};selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}",
            "not_run/not_claimed",
            "주장 경계를 보존한다.",
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
    data = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "sample_scope": f"tasks={final['task_rows']};trained={final['trained_models']};validation_rows={final['validation_trade_rows']}",
        "feature_label_boundary": "ED feature exclusion applied through fixed feature sets(ED 피처 제외 계약을 고정 피처 묶음으로 적용).",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in INPUT_FILES if path_exists(path) and io_path(path).is_file()},
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_family": "ExtraTreesClassifier(엑스트라 트리 분류기)",
        "trained_models": final["trained_models"],
        "onnx_parity": f"{final['onnx_passed_rows']}/{final['onnx_rows']}",
        "threshold_policy": "fixed_no_tuning(고정, 조정 없음)",
        "selection_metric": "none_review_required(없음, 검토 필요)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "best_validation_pf": final["best_validation_pf"],
        "best_validation_trade_count": final["best_validation_trade_count"],
        "best_oos_pf": final["best_oos_pf"],
        "best_oos_trade_count": final["best_oos_trade_count"],
        "release_candidate_rows": final["release_candidate_rows"],
        "next_review": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime = {
        "runtime_claim": "not_run_no_MT5(미실행, MT5 없음)",
        "onnx_materialized": final["onnx_rows"],
        "runtime_authority": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": JUDGMENT,
        "evidence_available": "trained models, ONNX parity, proxy scores, controls, density(학습 모델/ONNX 동등성/프록시 점수/대조/밀도).",
        "evidence_missing": "EF review, candidate selection, MT5, forward(EF 검토/후보 선택/MT5/전진).",
        "next_condition": NEXT_RUN_ID,
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
            rel(path): sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_with_boundary(경계 안에서 연결됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EE Training(337EE 학습)

## Conclusion(결론)

run337EE(337EE 실행)는 ED가 허용한 eligible ExtraTrees tasks(적격 ExtraTrees 작업) `{final["task_rows"]}`개를 학습하고 ONNX parity(ONNX 동등성)를 확인했다.

Action(행동): threshold tuning(임계값 조정), lot optimization(랏 최적화), candidate selection(후보 선택), MT5 probe(MT5 탐침)는 실행하지 않았다.

Effect(효과): 후보는 학습 산출물로만 남고, 다음 run337EF(337EF 실행)에서 validation PF/trade count/density/control(검증 PF/거래수/밀도/대조)을 검토한다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- trained_models(학습 모델): `{final["trained_models"]}`
- onnx_parity(ONNX 동등성): `{final["onnx_passed_rows"]}/{final["onnx_rows"]}`
- best_validation_pf(최고 검증 PF): `{final["best_validation_pf"]}`
- best_validation_trade_count(최고 검증 거래수): `{final["best_validation_trade_count"]}`
- best_oos_pf(최고 OOS PF): `{final["best_oos_pf"]}`
- best_oos_trade_count(최고 OOS 거래수): `{final["best_oos_trade_count"]}`
- release_candidate_rows(해제 후보 행): `{final["release_candidate_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337EE

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 적격 ExtraTrees 후보를 학습하고 ONNX 동등성을 확인했지만, 선택/MT5/Forward(전진)는 EF 검토 전 금지한다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(TRAINED_MODEL_MANIFEST)}`, `{rel(ONNX_PARITY)}`
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
        f"  Stage337 run337EE focus complete: validation-density/trade-count repair candidates(검증-밀도/거래수 수리 후보) `{final['trained_models']}`개를 학습했다. "
        "Effect(효과): 다음 run337EF에서 학습 결과를 선택 없이 검토한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337EE focus complete")
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
## Stage337 run337EE(337EE 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 적격 ExtraTrees 후보 `{final['trained_models']}`개와 ONNX `{final['onnx_passed_rows']}/{final['onnx_rows']}` 동등성을 만들었다. 선택/MT5/Forward/Goal(선택/MT5/전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337ED("
    if "## Stage337 run337EE(337EE 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_ee_training_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): trained repair candidates review(학습 수리 후보 검토)로 진행한다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337EE(337EE 실행) trained validation-density/trade-count repair candidates(검증-밀도/거래수 수리 후보). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337EE(337EE 실행) trained validation-density"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337EE trained validation-density/trade-count repair candidates(검증-밀도/거래수 수리 후보) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337EE trained validation-density"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "validation_density_trade_count_repair_training_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"trained={final['trained_models']};onnx={final['onnx_passed_rows']}/{final['onnx_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "training",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "training_no_selection_no_mt5",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "proxy_training_review_required",
        "scoreboard_lane": "model_validation_performance_attribution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_validation_pf={final['best_validation_pf']};best_oos_pf={final['best_oos_pf']}",
        "guardrail_kpi": "no_selection;no_mt5;no_forward;release_locked",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_performance_attribution_result_judgment",
        "evidence_scope": "eligible repair candidates trained",
        "kpi_scope": "proxy_training_review_required",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__training",
        "family": "model_validation_performance_attribution_result_judgment",
        "question": "do validation density trade-count repair candidates improve before EF review",
        "metric_scope": "validation_pf_trade_count_density_controls_onnx",
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
    artifacts: list[Path] = [
        write_csv(EE_TASK_MATRIX, TASK_COLUMNS, result["tasks"]),
        write_csv(FEATURE_COMPATIBILITY, FEATURE_COLUMNS, result["compat_rows"]),
        write_csv(SAMPLE_WEIGHT_AUDIT, WEIGHT_COLUMNS, result["weight_rows"]),
        write_csv(TRAINED_MODEL_MANIFEST, MODEL_COLUMNS, result["model_rows"]),
        write_csv(ONNX_PARITY, PARITY_COLUMNS, result["parity_rows"]),
        write_csv(CANDIDATE_CLASSIFICATION_SCORECARD, CLASS_COLUMNS, result["class_rows"]),
        write_csv(PROXY_TRADE_SCORECARD, TRADE_COLUMNS, result["trade_rows"]),
        write_csv(NEGATIVE_CONTROL_SCORECARD, CONTROL_COLUMNS, result["control_rows"]),
        write_csv(DENSITY_GUARD_AUDIT, DENSITY_COLUMNS, result["density_rows"]),
        write_csv(RUNTIME_FIREWALL_REVIEW, FIREWALL_COLUMNS, result["firewall_rows"]),
        write_csv(RELEASE_DISPOSITION, RELEASE_COLUMNS, result["release_rows"]),
        write_csv(EF_QUEUE, QUEUE_COLUMNS, result["queue_rows"]),
    ]
    artifacts.extend(result["dynamic_artifacts"])
    ed_final = read_json(ED_FINAL)
    validation_trade_rows = [row for row in result["trade_rows"] if row["split"] == "validation"]
    oos_trade_rows = [row for row in result["trade_rows"] if row["split"] == "oos"]
    best_validation = best_by(validation_trade_rows, "profit_factor")
    best_oos = best_by(oos_trade_rows, "profit_factor")
    onnx_passed = sum(1 for row in result["parity_rows"] if row["passed"] == "true")
    onnx_failed = len(result["parity_rows"]) - onnx_passed
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "ed_next_action": ed_final.get("next_action", ""),
        "ed_failed_gate_rows": sum(1 for row in read_csv(ED_GATES) if row.get("status") != "passed"),
        "missing_inputs": len(missing),
        "task_rows": len(result["tasks"]),
        "trained_models": len(result["model_rows"]),
        "onnx_rows": len(result["parity_rows"]),
        "onnx_passed_rows": onnx_passed,
        "onnx_failed_rows": onnx_failed,
        "validation_trade_rows": len(validation_trade_rows),
        "best_validation_model_id": best_validation.get("model_id", ""),
        "best_validation_pf": best_validation.get("profit_factor", 0),
        "best_validation_trade_count": best_validation.get("trade_count", 0),
        "best_oos_model_id": best_oos.get("model_id", ""),
        "best_oos_pf": best_oos.get("profit_factor", 0),
        "best_oos_trade_count": best_oos.get("trade_count", 0),
        "control_block_rows": sum(1 for row in result["control_rows"] if row["split"] == "validation" and row["blocks_training_review"] == "true"),
        "density_validation_pressure_rows": sum(1 for row in result["density_rows"] if row["split"] == "validation" and row["density_pressure_flag"] == "true"),
        "release_candidate_rows": 0,
        "firewall_rows": len(result["firewall_rows"]),
        "ef_queue_rows": len(result["queue_rows"]),
        "model_training": "completed_research_only",
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
                "onnx_parity": f"{onnx_passed}/{len(result['parity_rows'])}",
                "best_validation_pf": final["best_validation_pf"],
                "best_validation_trade_count": final["best_validation_trade_count"],
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
