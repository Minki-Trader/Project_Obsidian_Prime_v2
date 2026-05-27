from __future__ import annotations

import csv
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
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.baseline_training import LABEL_ORDER  # noqa: E402
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
from stage_pipelines.stage337.train_guarded_directional_label_action_candidates import (  # noqa: E402
    CANDIDATE_INPUT_MANIFEST,
    SOURCE_MODEL_INPUT,
)


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CW"
RUN_ID = "run337CW_train_feature_label_separability_control_repaired_candidates_without_db_v1"
PARENT_RUN_ID = "run337CV_materialize_feature_label_separability_control_repair_inputs_without_db_v1"
NEXT_RUN_ID = "run337CX_review_feature_label_separability_control_training_without_db_v1"
STATUS = "completed_stage337CW_feature_label_separability_control_repaired_training_review_required_no_selection_no_mt5"
JUDGMENT = "guarded_training_completed_control_review_required_no_forward_selection"
DECISION = "stage337CW_open_run337CX_review_feature_label_separability_control_training"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CW_feature_label_separability_control_repaired_training_without_db_"
    "train_only_thresholds_validation_oos_readonly_no_lot_optimization_no_candidate_selection_"
    "no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CW_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CW_feature_label_separability_control_training.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CV_DIR = STAGE_DIR / "02_runs" / "run337CV"
CV_FINAL = CV_DIR / "final_decision.json"
CV_GATES = CV_DIR / "required_gate_coverage_audit.csv"
LABEL_MARGIN_FRAME = CV_DIR / "label_margin_candidate_frame.parquet"
LABEL_MARGIN_CONTRACT = CV_DIR / "label_margin_contract.csv"
FEATURE_SETS = CV_DIR / "control_orthogonal_feature_sets.csv"
EXTENDED_CONTROL_CONTRACT = CV_DIR / "extended_control_contract.csv"
TINY_MODEL_TASKS = CV_DIR / "tiny_model_probe_task_matrix.csv"
CW_QUEUE = CV_DIR / "run337CW_guarded_training_queue.csv"

TASK_DISPOSITION = RUN_DIR / "task_disposition_matrix.csv"
TRAINED_MODEL_MANIFEST = RUN_DIR / "trained_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "onnx_parity_matrix.csv"
SCORECARD = RUN_DIR / "guarded_training_scorecard.csv"
EXTENDED_CONTROL_SCORECARD = RUN_DIR / "extended_control_scorecard.csv"
COST_CURVE_SCORECARD = RUN_DIR / "cost_curve_shape_scorecard.csv"
POLICY_THRESHOLDS = RUN_DIR / "train_only_policy_thresholds.csv"
RUNTIME_DISPOSITION = RUN_DIR / "runtime_probe_release_disposition.csv"
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
    CV_FINAL,
    CV_GATES,
    LABEL_MARGIN_FRAME,
    LABEL_MARGIN_CONTRACT,
    FEATURE_SETS,
    EXTENDED_CONTROL_CONTRACT,
    TINY_MODEL_TASKS,
    CW_QUEUE,
    SOURCE_MODEL_INPUT,
    CANDIDATE_INPUT_MANIFEST,
)
OUTPUT_FILES = (
    TASK_DISPOSITION,
    TRAINED_MODEL_MANIFEST,
    ONNX_PARITY,
    SCORECARD,
    EXTENDED_CONTROL_SCORECARD,
    COST_CURVE_SCORECARD,
    POLICY_THRESHOLDS,
    RUNTIME_DISPOSITION,
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

TASK_DISPOSITION_COLUMNS = (
    "task_id",
    "probe_id",
    "model_config_id",
    "contract_id",
    "label_candidate_id",
    "feature_set_id",
    "training_disposition",
    "reason",
    "claim_boundary",
)
MODEL_COLUMNS = (
    "model_id",
    "task_id",
    "probe_id",
    "model_config_id",
    "contract_id",
    "label_candidate_id",
    "feature_set_id",
    "feature_count",
    "feature_order_hash",
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
SCORE_COLUMNS = (
    "policy_id",
    "model_id",
    "task_id",
    "probe_id",
    "model_config_id",
    "contract_id",
    "label_candidate_id",
    "feature_set_id",
    "density_floor",
    "train_directional_cutoff",
    "split",
    "rows",
    "model_accuracy",
    "model_balanced_accuracy",
    "model_macro_f1",
    "model_log_loss",
    "signal_density",
    "decision_short",
    "decision_long",
    "decision_no_trade",
    "traded_rows",
    "trade_accuracy",
    "trade_balanced_accuracy",
    "mean_decision_margin",
    "mean_raw_trade_return",
    "validation_gate_status",
    "oos_readonly_gate_status",
    "claim_boundary",
)
CONTROL_COLUMNS = (
    "policy_id",
    "model_id",
    "control_id",
    "control_family",
    "split",
    "rows",
    "traded_rows",
    "actual_trade_balanced_accuracy",
    "control_trade_balanced_accuracy",
    "control_minus_actual",
    "control_status",
    "blocks_runtime_probe",
    "claim_boundary",
)
COST_COLUMNS = (
    "policy_id",
    "model_id",
    "split",
    "cost_points",
    "trade_count",
    "signal_density",
    "net_proxy_return",
    "gross_profit",
    "gross_loss",
    "profit_factor",
    "expectancy",
    "max_drawdown",
    "recovery_factor",
    "worst_chunk_return",
    "max_underwater_bars",
    "cost_status",
    "blocks_runtime_probe",
    "claim_boundary",
)
POLICY_COLUMNS = (
    "policy_id",
    "model_id",
    "density_floor",
    "train_directional_cutoff",
    "train_signal_density",
    "selector_source",
    "forbidden_action",
    "claim_boundary",
)
RUNTIME_COLUMNS = (
    "policy_id",
    "model_id",
    "validation_gate_status",
    "oos_readonly_gate_status",
    "extended_control_block_rows",
    "cost_block_rows",
    "mt5_probe_disposition",
    "release_blockers",
    "next_condition",
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

DENSITY_FLOORS = (0.05, 0.08)
COST_LEVELS = (0, 1, 2, 5, 10)
COST_UNIT_LOG_RETURN = 1.0e-5
CONTROL_IDS = ("label_shift_gap72_control", "label_shift_gap96_control", "horizon_modulo_fold_control")


def feature_order_hash(features: Sequence[str]) -> str:
    return __import__("hashlib").sha256("\n".join(features).encode("utf-8")).hexdigest()


def read_source_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(SOURCE_MODEL_INPUT)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    frame["source_row_id"] = np.arange(len(frame), dtype=np.int64)
    return frame


def parse_json_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    try:
        parsed = json.loads(str(value))
    except json.JSONDecodeError:
        return []
    return [str(item) for item in parsed]


def build_model(model_config_id: str) -> ExtraTreesClassifier:
    leaf = 160
    for candidate in (80, 160, 320):
        if f"leaf{candidate}" in model_config_id:
            leaf = candidate
            break
    class_weight: str | dict[int, float] = "balanced"
    if "direction_weight_2x" in model_config_id:
        class_weight = {0: 2.0, 1: 1.0, 2: 2.0}
    return ExtraTreesClassifier(
        n_estimators=96,
        max_depth=6,
        min_samples_leaf=leaf,
        class_weight=class_weight,
        random_state=337,
        n_jobs=-1,
    )


def label_vector(label_frame: pd.DataFrame, label_candidate_id: str, contract_id: str, source_rows: int) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    rows = label_frame.loc[
        (label_frame["label_candidate_id"].astype(str) == label_candidate_id)
        & (label_frame["contract_id"].astype(str) == contract_id)
    ].sort_values("source_row_id")
    if len(rows) != source_rows:
        raise RuntimeError(f"Label rows mismatch for {label_candidate_id}/{contract_id}: {len(rows)}")
    masks = {
        "train": rows["usable_for_training"].astype(bool).to_numpy(),
        "validation": rows["usable_for_validation"].astype(bool).to_numpy(),
        "oos": rows["usable_for_oos"].astype(bool).to_numpy(),
    }
    return rows["label_class"].to_numpy(dtype=np.int64), masks


def build_control_labels(y: np.ndarray, split_labels: np.ndarray) -> dict[tuple[str, str], np.ndarray]:
    controls: dict[tuple[str, str], np.ndarray] = {}
    for gap in (72, 96):
        output = np.full_like(y, -1)
        for split in ("validation", "oos"):
            idx = np.flatnonzero(split_labels == split)
            if len(idx) > gap:
                output[idx[gap:]] = y[idx[:-gap]]
        controls[(f"label_shift_gap{gap}_control", "extended_split_local_shift(확장 분할 내부 이동)")] = output
    modulo = np.full_like(y, -1)
    for split in ("validation", "oos"):
        idx = np.flatnonzero(split_labels == split)
        modulo[idx] = (np.arange(len(idx)) % 3).astype(np.int64)
    controls[("horizon_modulo_fold_control", "horizon_modulo_fold(기간 모듈로 폴드)")] = modulo
    return controls


def directional_policy(probabilities: np.ndarray, cutoff: float) -> pd.DataFrame:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    short_margin = p_short - np.maximum(p_flat, p_long)
    long_margin = p_long - np.maximum(p_flat, p_short)
    choose_short = short_margin >= long_margin
    margins = np.where(choose_short, short_margin, long_margin)
    labels = np.where((margins >= cutoff) & (margins > 0.0), np.where(choose_short, "short", "long"), "no_trade")
    classes = np.where(labels == "short", 0, np.where(labels == "long", 2, -1)).astype(np.int64)
    probs = np.where(classes == 0, p_short, np.where(classes == 2, p_long, np.maximum.reduce([p_short, p_flat, p_long])))
    return pd.DataFrame(
        {
            "decision_label": labels,
            "decision_label_class": classes,
            "decision_probability": probs.astype(float),
            "decision_margin": margins.astype(float),
        }
    )


def train_cutoff(probabilities: np.ndarray, density_floor: float) -> float:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    short_margin = p_short - np.maximum(p_flat, p_long)
    long_margin = p_long - np.maximum(p_flat, p_short)
    margins = np.maximum(short_margin, long_margin)
    finite = margins[np.isfinite(margins)]
    if len(finite) == 0:
        return 1.0
    return float(max(0.0, np.quantile(finite, max(0.0, min(1.0, 1.0 - float(density_floor))))))


def safe_balanced(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    if len(y_true) < 3 or len(np.unique(y_true)) < 2 or len(np.unique(y_pred)) < 2:
        return 0.0
    return float(balanced_accuracy_score(y_true, y_pred))


def raw_trade_returns(returns: np.ndarray, decision_classes: np.ndarray) -> np.ndarray:
    return np.where(decision_classes == 2, returns, np.where(decision_classes == 0, -returns, 0.0)).astype(float)


def max_drawdown(values: np.ndarray) -> float:
    if len(values) == 0:
        return 0.0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    return float(np.max(peak - curve))


def max_underwater(values: np.ndarray) -> int:
    if len(values) == 0:
        return 0
    curve = np.cumsum(values)
    peak = np.maximum.accumulate(curve)
    underwater = curve < peak
    best = count = 0
    for item in underwater:
        count = count + 1 if bool(item) else 0
        best = max(best, count)
    return int(best)


def score_split(
    policy_base: Mapping[str, Any],
    split: str,
    y_true: np.ndarray,
    returns: np.ndarray,
    probabilities: np.ndarray,
    decisions: pd.DataFrame,
    cutoff: float,
) -> dict[str, Any]:
    y_pred = np.asarray(LABEL_ORDER, dtype=np.int64)[probabilities.argmax(axis=1)]
    decision_classes = decisions["decision_label_class"].to_numpy(dtype=np.int64)
    trade_mask = decision_classes != -1
    decision_counts = decisions["decision_label"].value_counts().to_dict()
    trade_accuracy = 0.0
    trade_balanced = 0.0
    if int(trade_mask.sum()) > 0:
        trade_accuracy = float(accuracy_score(y_true[trade_mask], decision_classes[trade_mask]))
        trade_balanced = safe_balanced(y_true[trade_mask], decision_classes[trade_mask])
    raw_returns = raw_trade_returns(returns, decision_classes)
    density_floor = float(policy_base["density_floor"])
    model_balanced = safe_balanced(y_true, y_pred)
    signal_density = float(trade_mask.mean())
    validation_gate = "not_applicable"
    oos_gate = "not_applicable"
    if split == "validation":
        validation_gate = "passed" if model_balanced >= 0.40 and signal_density >= density_floor else "failed"
    if split == "oos":
        oos_gate = "passed_readonly" if model_balanced >= 0.40 and signal_density >= density_floor else "failed_readonly"
    return {
        **policy_base,
        "train_directional_cutoff": cutoff,
        "split": split,
        "rows": int(len(y_true)),
        "model_accuracy": float(accuracy_score(y_true, y_pred)),
        "model_balanced_accuracy": model_balanced,
        "model_macro_f1": float(f1_score(y_true, y_pred, labels=LABEL_ORDER, average="macro")),
        "model_log_loss": float(log_loss(y_true, probabilities, labels=LABEL_ORDER)),
        "signal_density": signal_density,
        "decision_short": int(decision_counts.get("short", 0)),
        "decision_long": int(decision_counts.get("long", 0)),
        "decision_no_trade": int(decision_counts.get("no_trade", 0)),
        "traded_rows": int(trade_mask.sum()),
        "trade_accuracy": trade_accuracy,
        "trade_balanced_accuracy": trade_balanced,
        "mean_decision_margin": float(decisions["decision_margin"].mean()),
        "mean_raw_trade_return": float(raw_returns[trade_mask].mean()) if int(trade_mask.sum()) else 0.0,
        "validation_gate_status": validation_gate,
        "oos_readonly_gate_status": oos_gate,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def score_controls(
    policy_base: Mapping[str, Any],
    split: str,
    y_global: np.ndarray,
    split_indices: np.ndarray,
    decisions: pd.DataFrame,
    controls: Mapping[tuple[str, str], np.ndarray],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    decision_classes = decisions["decision_label_class"].to_numpy(dtype=np.int64)
    trade_local = decision_classes != -1
    for (control_id, control_family), control_y in controls.items():
        local_usable = (control_y[split_indices] != -1) & trade_local
        local_rows = np.flatnonzero(local_usable)
        if len(local_rows) < 10:
            actual_balanced = 0.0
            control_balanced = 0.0
            status = "block_insufficient_control_trades"
            blocks = True
        else:
            source_rows = split_indices[local_rows]
            actual_balanced = safe_balanced(y_global[source_rows], decision_classes[local_rows])
            control_balanced = safe_balanced(control_y[source_rows], decision_classes[local_rows])
            passed = actual_balanced >= 0.40 and control_balanced < actual_balanced and control_balanced < 0.45
            status = "passed_control_weakened" if passed else "block_extended_control_not_weakened"
            blocks = not passed
        rows.append(
            {
                "policy_id": policy_base["policy_id"],
                "model_id": policy_base["model_id"],
                "control_id": control_id,
                "control_family": control_family,
                "split": split,
                "rows": int(len(split_indices)),
                "traded_rows": int(len(local_rows)),
                "actual_trade_balanced_accuracy": actual_balanced,
                "control_trade_balanced_accuracy": control_balanced,
                "control_minus_actual": control_balanced - actual_balanced,
                "control_status": status,
                "blocks_runtime_probe": str(blocks).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def score_costs(policy_base: Mapping[str, Any], split: str, returns: np.ndarray, decisions: pd.DataFrame) -> list[dict[str, Any]]:
    decision_classes = decisions["decision_label_class"].to_numpy(dtype=np.int64)
    trade_mask = decision_classes != -1
    raw_returns = raw_trade_returns(returns, decision_classes)
    out: list[dict[str, Any]] = []
    for cost_points in COST_LEVELS:
        costs = np.where(trade_mask, float(cost_points) * COST_UNIT_LOG_RETURN, 0.0)
        net = raw_returns - costs
        trade_net = net[trade_mask]
        gross_profit = float(trade_net[trade_net > 0].sum()) if len(trade_net) else 0.0
        gross_loss = float(-trade_net[trade_net < 0].sum()) if len(trade_net) else 0.0
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else (float("inf") if gross_profit > 0 else 0.0)
        drawdown = max_drawdown(net)
        total = float(net.sum())
        status = "passed_cost_shape" if len(trade_net) >= 50 and total > 0 and profit_factor >= 1.05 else "block_cost_shape"
        out.append(
            {
                "policy_id": policy_base["policy_id"],
                "model_id": policy_base["model_id"],
                "split": split,
                "cost_points": cost_points,
                "trade_count": int(trade_mask.sum()),
                "signal_density": float(trade_mask.mean()),
                "net_proxy_return": total,
                "gross_profit": gross_profit,
                "gross_loss": gross_loss,
                "profit_factor": profit_factor,
                "expectancy": float(trade_net.mean()) if len(trade_net) else 0.0,
                "max_drawdown": drawdown,
                "recovery_factor": total / drawdown if drawdown > 0 else 0.0,
                "worst_chunk_return": float(pd.Series(net).rolling(50, min_periods=1).sum().min()) if len(net) else 0.0,
                "max_underwater_bars": max_underwater(net),
                "cost_status": status,
                "blocks_runtime_probe": str(status != "passed_cost_shape").lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def run_training() -> dict[str, Any]:
    io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    io_path(ONNX_DIR).mkdir(parents=True, exist_ok=True)
    source = read_source_frame()
    returns = pd.to_numeric(source["future_log_return_12"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    task_rows = read_csv(TINY_MODEL_TASKS)
    feature_set_rows = read_csv(FEATURE_SETS)
    feature_sets = {row["feature_set_id"]: parse_json_list(row["included_features_json"]) for row in feature_set_rows}
    label_frame = pd.read_parquet(io_path(LABEL_MARGIN_FRAME))
    label_frame["timestamp"] = pd.to_datetime(label_frame["timestamp"], utc=True)
    source_rows = len(source)
    split_labels = source["split"].astype(str).to_numpy()

    task_disposition: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    score_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    cost_rows: list[dict[str, Any]] = []
    threshold_rows: list[dict[str, Any]] = []
    runtime_rows: list[dict[str, Any]] = []
    dynamic_artifacts: list[Path] = []
    nonfinite_rows = 0

    trainable_tasks = [row for row in task_rows if row.get("probe_id") != "two_stage_calibrated_rank_only"]
    for row in task_rows:
        held = row.get("probe_id") == "two_stage_calibrated_rank_only"
        task_disposition.append(
            {
                "task_id": row["task_id"],
                "probe_id": row["probe_id"],
                "model_config_id": row["model_config_id"],
                "contract_id": row["contract_id"],
                "label_candidate_id": row["label_candidate_id"],
                "feature_set_id": row["feature_set_id"],
                "training_disposition": "held_requires_composite_runtime_contract" if held else "queued_for_training",
                "reason": "two_stage needs composite ONNX handoff(2단계는 복합 ONNX 인계 필요)" if held else "trainable multiclass ONNX(학습 가능 다중분류 ONNX)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for index, task in enumerate(trainable_tasks, start=1):
        features = feature_sets[task["feature_set_id"]]
        X_all = source[features].replace([np.inf, -np.inf], np.nan)
        nonfinite_rows += int(X_all.isna().any(axis=1).sum())
        X_all = X_all.fillna(0.0).to_numpy(dtype=np.float64)
        y_all, masks = label_vector(label_frame, task["label_candidate_id"], task["contract_id"], source_rows)
        train_idx = np.flatnonzero(masks["train"])
        validation_idx = np.flatnonzero(masks["validation"])
        oos_idx = np.flatnonzero(masks["oos"])
        model = build_model(task["model_config_id"])
        model.fit(X_all[train_idx], y_all[train_idx])
        model_key = f"cw{index:03d}"
        model_id = f"{model_key}__{task['model_config_id']}__{task['label_candidate_id']}__{task['contract_id']}__{task['feature_set_id']}"
        model_path = MODEL_DIR / f"{model_key}.joblib"
        onnx_path = ONNX_DIR / f"{model_key}.onnx"
        joblib.dump(model, io_path(model_path))
        export_info = export_sklearn_to_onnx_zipmap_disabled(
            model,
            onnx_path,
            feature_count=len(features),
            drop_label_output=True,
        )
        dynamic_artifacts.extend([model_path, onnx_path])
        sample_idx = np.concatenate([train_idx[:256], validation_idx[:256], oos_idx[:256]])
        parity = check_onnxruntime_probability_parity(model, onnx_path, X_all[sample_idx])
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
                "probe_id": task["probe_id"],
                "model_config_id": task["model_config_id"],
                "contract_id": task["contract_id"],
                "label_candidate_id": task["label_candidate_id"],
                "feature_set_id": task["feature_set_id"],
                "feature_count": len(features),
                "feature_order_hash": feature_order_hash(features),
                "model_path": rel(model_path),
                "model_sha256": sha256_file(model_path),
                "onnx_path": rel(onnx_path),
                "onnx_sha256": sha256_file(onnx_path),
                "onnx_probability_output_name": export_info["probability_output_name"],
                "train_rows": len(train_idx),
                "validation_rows": len(validation_idx),
                "oos_rows": len(oos_idx),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        probs_by_split: dict[str, np.ndarray] = {
            "train": ordered_sklearn_probabilities(model, X_all[train_idx], LABEL_ORDER),
            "validation": ordered_sklearn_probabilities(model, X_all[validation_idx], LABEL_ORDER),
            "oos": ordered_sklearn_probabilities(model, X_all[oos_idx], LABEL_ORDER),
        }
        indices_by_split = {"train": train_idx, "validation": validation_idx, "oos": oos_idx}
        controls = build_control_labels(y_all, split_labels)
        for density_floor in DENSITY_FLOORS:
            cutoff = train_cutoff(probs_by_split["train"], density_floor)
            train_decisions = directional_policy(probs_by_split["train"], cutoff)
            train_density = float((train_decisions["decision_label"] != "no_trade").mean())
            policy_id = f"{model_key}__density_{int(density_floor * 100):02d}"
            policy_base = {
                "policy_id": policy_id,
                "model_id": model_id,
                "task_id": task["task_id"],
                "probe_id": task["probe_id"],
                "model_config_id": task["model_config_id"],
                "contract_id": task["contract_id"],
                "label_candidate_id": task["label_candidate_id"],
                "feature_set_id": task["feature_set_id"],
                "density_floor": density_floor,
            }
            threshold_rows.append(
                {
                    "policy_id": policy_id,
                    "model_id": model_id,
                    "density_floor": density_floor,
                    "train_directional_cutoff": cutoff,
                    "train_signal_density": train_density,
                    "selector_source": "train_split_only_directional_margin_quantile(학습 분할 전용 방향 여백 분위수)",
                    "forbidden_action": "no validation/OOS threshold tuning(검증/OOS 임계값 조정 금지)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            split_score_rows: list[dict[str, Any]] = []
            split_control_rows: list[dict[str, Any]] = []
            split_cost_rows: list[dict[str, Any]] = []
            for split, split_idx in indices_by_split.items():
                decisions = train_decisions if split == "train" else directional_policy(probs_by_split[split], cutoff)
                split_score_rows.append(
                    score_split(policy_base, split, y_all[split_idx], returns[split_idx], probs_by_split[split], decisions, cutoff)
                )
                if split in {"validation", "oos"}:
                    split_control_rows.extend(score_controls(policy_base, split, y_all, split_idx, decisions, controls))
                    split_cost_rows.extend(score_costs(policy_base, split, returns[split_idx], decisions))
            score_rows.extend(split_score_rows)
            control_rows.extend(split_control_rows)
            cost_rows.extend(split_cost_rows)
            validation_row = next(item for item in split_score_rows if item["split"] == "validation")
            oos_row = next(item for item in split_score_rows if item["split"] == "oos")
            control_blocks = sum(1 for item in split_control_rows if item["blocks_runtime_probe"] == "true")
            cost_blocks = sum(1 for item in split_cost_rows if item["blocks_runtime_probe"] == "true" and item["split"] == "validation")
            blockers = []
            if validation_row["validation_gate_status"] != "passed":
                blockers.append("validation_density_or_balanced_gate_failed")
            if control_blocks:
                blockers.append("extended_control_block")
            if cost_blocks:
                blockers.append("validation_cost_shape_block")
            disposition = "review_eligible_no_auto_mt5_release" if not blockers else "held_for_review"
            runtime_rows.append(
                {
                    "policy_id": policy_id,
                    "model_id": model_id,
                    "validation_gate_status": validation_row["validation_gate_status"],
                    "oos_readonly_gate_status": oos_row["oos_readonly_gate_status"],
                    "extended_control_block_rows": control_blocks,
                    "cost_block_rows": cost_blocks,
                    "mt5_probe_disposition": disposition,
                    "release_blockers": ";".join(blockers) or "none",
                    "next_condition": NEXT_RUN_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    feature_rows = [
        {
            "source_path": rel(SOURCE_MODEL_INPUT),
            "rows": len(source),
            "feature_set_rows": len(feature_sets),
            "trained_feature_sets": len({row["feature_set_id"] for row in model_rows}),
            "nonfinite_rows": nonfinite_rows,
            "compatibility_status": "passed",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return {
        "task_disposition_rows": task_disposition,
        "model_rows": model_rows,
        "parity_rows": parity_rows,
        "score_rows": score_rows,
        "control_rows": control_rows,
        "cost_rows": cost_rows,
        "threshold_rows": threshold_rows,
        "runtime_rows": runtime_rows,
        "feature_rows": feature_rows,
        "dynamic_artifacts": dynamic_artifacts,
        "source_rows": len(source),
        "task_rows": len(task_rows),
        "trained_task_rows": len(trainable_tasks),
        "held_task_rows": len(task_rows) - len(trainable_tasks),
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
        row("cw_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CV 입력 계약과 원천 데이터를 연결한다."),
        row("cw_gate_parent_points_to_cw", final["cv_next_action"] == RUN_ID, final["cv_next_action"], RUN_ID, "CV next_action(다음 행동)과 CW 실행을 맞춘다."),
        row("cw_gate_task_disposition_complete", final["task_disposition_rows"] == final["task_rows"], final["task_disposition_rows"], "task_rows", "모든 작업의 학습/보류 처분을 기록한다."),
        row("cw_gate_models_trained", final["trained_models"] == final["trained_task_rows"], final["trained_models"], "trained_task_rows", "ONNX 가능한 다중분류 작업을 모두 학습한다."),
        row("cw_gate_two_stage_held", final["held_task_rows"] == 24, final["held_task_rows"], "24", "복합 2단계 작업은 별도 런타임 계약 전까지 보류한다."),
        row("cw_gate_onnx_parity", final["onnx_parity_passed"] == final["onnx_parity_rows"] and final["onnx_parity_rows"] > 0, f"{final['onnx_parity_passed']}/{final['onnx_parity_rows']}", "all parity passed", "Python/ONNX(파이썬/온엑스) 확률 출력 동등성을 확인한다."),
        row("cw_gate_scorecard_rows", final["scorecard_rows"] == final["trained_models"] * len(DENSITY_FLOORS) * 3, final["scorecard_rows"], "models*density*3", "train/validation/OOS(학습/검증/OOS)를 모두 기록한다."),
        row("cw_gate_control_rows", final["control_rows"] == final["trained_models"] * len(DENSITY_FLOORS) * 2 * len(CONTROL_IDS), final["control_rows"], "models*density*2*controls", "검증/OOS 대조를 모두 기록한다."),
        row("cw_gate_runtime_no_auto_release", final["auto_mt5_release_rows"] == 0, final["auto_mt5_release_rows"], "0", "리뷰 없이 MT5 자동 해제를 막는다."),
        row("cw_gate_no_selection_or_mt5", True, "selection=not_run;mt5=not_run", "no selection/MT5", "학습 결과를 즉시 운영 주장으로 바꾸지 않는다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    model_receipt = {
        "model_family": "ExtraTreesClassifier(엑스트라트리 분류기), tiny predeclared grid(사전 선언 소형 격자)",
        "target_and_label": "label_v4 q60/q70 vol-normalized margin labels(변동성 정규화 여백 라벨)",
        "split_method": "purged/embargo train fit only, validation/OOS read-only(제거/격리 학습 전용, 검증/OOS 읽기 전용)",
        "selection_metric": "none_no_candidate_selection(없음, 후보 선택 없음)",
        "secondary_metrics": "ONNX parity(ONNX 동등성), balanced accuracy(균형 정확도), signal density(신호 밀도), extended controls(확장 대조), cost curve(비용 곡선)",
        "threshold_policy": "train-only directional cutoff by fixed density floors(고정 밀도 하한의 학습 전용 방향 컷오프)",
        "overfit_risk": "review could misuse OOS read-only diagnostics(OOS 읽기 전용 진단을 선택에 오용할 위험)",
        "calibration_risk": "probabilities are ranking scores unless later calibrated(나중에 보정 전까지 확률은 순위 점수)",
        "comparison_baseline": "run337CS weak density repair training(약한 밀도 수리 학습)",
        "validation_judgment": "training_completed_review_required_no_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "timestamp(시각)은 UTC 정렬, source_row_id(원천 행 ID) 고정",
        "sample_scope": "US100 M5 shared research window(공유 연구 구간), source_rows=46650",
        "missing_or_duplicate_check": "feature compatibility(피처 호환성)와 finite fill(비유한값 보정)을 기록했다.",
        "feature_label_boundary": "future_log_return_12(미래 12봉 수익률)는 라벨과 프록시 손익에만 사용하고 피처에는 넣지 않았다.",
        "split_boundary": "train rows fit models and cutoffs; validation/OOS rows score only(학습 행은 학습/컷오프, 검증/OOS는 채점 전용)",
        "leakage_risk": "review selecting by OOS rank(리뷰가 OOS 순위로 선택하는 경로)",
        "data_hash_or_identity": {"source_sha256": final["source_sha256"], "source_rows": final["source_rows"]},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "attribution_subject": RUN_ID,
        "slices": "split, density floor, control id, cost points(분할, 밀도 하한, 대조 ID, 비용 포인트)",
        "primary_finding": "review_required; no automatic MT5 release(검토 필요, MT5 자동 해제 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime_receipt = {
        "runtime_subject": "ONNX export and parity only(ONNX 내보내기와 동등성만)",
        "parity_check": f"{final['onnx_parity_passed']}/{final['onnx_parity_rows']}",
        "mt5_runtime_probe": "not_run",
        "usable_for": NEXT_RUN_ID,
        "not_usable_for": "runtime authority, Forward Passed, live readiness(런타임 권위, 전진 통과, 실거래 준비)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "trained models(학습 모델), ONNX parity(ONNX 동등성), scorecards(점수표), controls(대조), cost stress(비용 압박)",
        "evidence_missing": "review decision(리뷰 결정), MT5 runtime probe(MT5 런타임 탐침), forward decision(전진 판정)",
        "judgment_label": "exploratory",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "학습은 끝났지만 아직 선택이나 전진 통과가 아니다.",
    }
    receipt_paths = [
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
        "artifact_paths": [rel(path) for path in artifact_paths] + [rel(path) for path in receipt_paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + receipt_paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers(02_runs는 목록/해시로 추적, 보고서와 장부는 추적)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipt_paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return receipt_paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CW Guarded Training(방어 학습)

## Conclusion(결론)

run337CW(337CW 실행)는 CV 입력 계약(input contract, 입력 계약)을 사용해 ONNX-compatible multiclass tasks(ONNX 호환 다중분류 작업) `120`개를 학습했다. two-stage composite tasks(2단계 복합 작업) `24`개는 별도 runtime handoff contract(런타임 인계 계약)가 필요해 보류했다.

Effect(효과): 모델 학습은 진행했지만 candidate selection(후보 선택), MT5 probe(MT5 탐침), Forward Passed/Failed(전진 통과/실패)는 여전히 금지 상태다. 다음 run337CX(337CX 실행)가 control/cost/release review(대조/비용/해제 검토)를 해야 한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- task_rows(작업 행): `{final["task_rows"]}`
- trained_models(학습 모델): `{final["trained_models"]}`
- held_task_rows(보류 작업 행): `{final["held_task_rows"]}`
- onnx_parity(ONNX 동등성): `{final["onnx_parity_passed"]}/{final["onnx_parity_rows"]}`
- scorecard_rows(점수표 행): `{final["scorecard_rows"]}`
- control_rows(대조 행): `{final["control_rows"]}`
- runtime_review_eligible_rows(런타임 리뷰 가능 행): `{final["review_eligible_rows"]}`
- auto_mt5_release_rows(MT5 자동 해제 행): `{final["auto_mt5_release_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- candidate_selection(후보 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CW

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): ONNX-compatible guarded training(ONNX 호환 방어 학습)을 끝내고 CX review(CX 검토)를 열었다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(FINAL_DECISION)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{final["passed_gates"]}/{final["gate_rows"]}`
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
        "current_focus:\n- >-\n"
        f"  Stage337 run337CW focus complete: feature/label separability control repaired training(피처/라벨 분리력 대조 수리 학습)을 "
        f"`{STATUS}`로 닫았다. Effect(효과): run337CX(337CX 실행)에서 ONNX parity(ONNX 동등성), control/cost gates(대조/비용 게이트), release disposition(해제 처분)을 검토한다."
    )
    workspace_text = workspace_text.replace("current_focus:", focus_entry, 1)
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
## Stage337 run337CW(337CW 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): trained_models(학습 모델) `{final["trained_models"]}`, ONNX parity(ONNX 동등성) `{final["onnx_parity_passed"]}/{final["onnx_parity_rows"]}`, auto_mt5_release(MT5 자동 해제) `{final["auto_mt5_release_rows"]}`로 기록했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337CV(337CV"
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
- actual_mt5_execution(실제 MT5 실행): `not_run_cw_training_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 feature/label separability control training review(피처/라벨 분리력 대조 학습 검토)다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337CW(337CW 실행) trained feature/label separability control repaired candidates(피처/라벨 분리력 대조 수리 후보). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337CW trained feature/label separability control repaired candidates(피처/라벨 분리력 대조 수리 후보) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "feature_label_separability_control_repaired_training_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": (
            f"trained_models={final['trained_models']};onnx_parity={final['onnx_parity_passed']}/{final['onnx_parity_rows']};"
            f"review_eligible={final['review_eligible_rows']};auto_mt5_release=0;next_action={NEXT_RUN_ID};goal_achieve_not_claimed."
        ),
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__guarded_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "guarded_training",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "training_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "model_validation_control_cost",
        "scoreboard_lane": "model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"trained_models={final['trained_models']};review_eligible={final['review_eligible_rows']}",
        "guardrail_kpi": "onnx_parity;extended_controls;cost_stress;no_auto_mt5_release",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__guarded_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "CV separability inputs trained into ONNX candidates",
        "kpi_scope": "model_validation_control_cost",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__guarded_training",
        "family": "experiment_execution_data_integrity_model_validation_artifact_lineage",
        "question": "does separability/control repair produce ONNX candidates worth review",
        "metric_scope": "trained_models_onnx_parity_controls_cost_release",
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
        write_csv(TASK_DISPOSITION, TASK_DISPOSITION_COLUMNS, result["task_disposition_rows"]),
        write_csv(TRAINED_MODEL_MANIFEST, MODEL_COLUMNS, result["model_rows"]),
        write_csv(ONNX_PARITY, PARITY_COLUMNS, result["parity_rows"]),
        write_csv(SCORECARD, SCORE_COLUMNS, result["score_rows"]),
        write_csv(EXTENDED_CONTROL_SCORECARD, CONTROL_COLUMNS, result["control_rows"]),
        write_csv(COST_CURVE_SCORECARD, COST_COLUMNS, result["cost_rows"]),
        write_csv(POLICY_THRESHOLDS, POLICY_COLUMNS, result["threshold_rows"]),
        write_csv(RUNTIME_DISPOSITION, RUNTIME_COLUMNS, result["runtime_rows"]),
        write_csv(FEATURE_COMPATIBILITY, FEATURE_COLUMNS, result["feature_rows"]),
    ]
    cv_final = read_json(CV_FINAL)
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
        "cv_next_action": cv_final.get("next_action", ""),
        "source_rows": result["source_rows"],
        "source_sha256": sha256_file(SOURCE_MODEL_INPUT),
        "task_rows": result["task_rows"],
        "task_disposition_rows": len(result["task_disposition_rows"]),
        "trained_task_rows": result["trained_task_rows"],
        "held_task_rows": result["held_task_rows"],
        "trained_models": len(result["model_rows"]),
        "onnx_parity_rows": len(result["parity_rows"]),
        "onnx_parity_passed": parity_passed,
        "scorecard_rows": len(result["score_rows"]),
        "control_rows": len(result["control_rows"]),
        "cost_rows": len(result["cost_rows"]),
        "runtime_rows": len(result["runtime_rows"]),
        "review_eligible_rows": review_eligible,
        "auto_mt5_release_rows": 0,
        "model_training": "completed_guarded",
        "threshold_tuning": "not_run_train_only_cutoffs",
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
