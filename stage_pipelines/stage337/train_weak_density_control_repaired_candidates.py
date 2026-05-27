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
    build_model,
)


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CS"
RUN_ID = "run337CS_train_weak_density_control_repaired_candidates_without_db_v1"
PARENT_RUN_ID = "run337CR_materialize_weak_density_control_alignment_repair_inputs_without_db_v1"
NEXT_RUN_ID = "run337CT_review_weak_density_control_repaired_candidates_without_db_v1"
STATUS = "completed_stage337CS_weak_density_control_repaired_training_review_required_no_selection_no_mt5"
JUDGMENT = "limited_density_repair_training_completed_release_lock_review_required_no_forward_selection"
DECISION = "stage337CS_open_run337CT_review_weak_density_control_repaired_candidates"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CS_weak_density_control_repaired_training_without_db_"
    "train_only_density_policy_no_validation_oos_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_probe_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CS_weak_density_control_repaired_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CS_weak_density_control_repaired_training.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CN_DIR = STAGE_DIR / "02_runs" / "run337CN"
CN_LABEL_FRAME = CN_DIR / "candidate_label_frame.parquet"
CN_PURGED_MEMBERSHIP = CN_DIR / "purged_embargo_split_membership.parquet"
CR_DIR = STAGE_DIR / "02_runs" / "run337CR"
CR_FINAL = CR_DIR / "final_decision.json"
CR_GATES = CR_DIR / "required_gate_coverage_audit.csv"
CR_DENSITY_POLICY = CR_DIR / "train_only_density_policy_grid.csv"
CR_EXTENDED_SHIFT = CR_DIR / "extended_shift_control_frame.parquet"
CR_COST_CONTRACT = CR_DIR / "cost_curve_shape_gate_contract.csv"
CR_MT5_LOCK = CR_DIR / "mt5_probe_release_lock.csv"
CR_COMPARE_CONTRACT = CR_DIR / "proxy_mt5_required_compare_contract.csv"
CR_CS_QUEUE = CR_DIR / "run337CS_guarded_training_queue.csv"
CP_WEAKNESS = STAGE_DIR / "02_runs" / "run337CP" / "review_ready_weakness_matrix.csv"

TRAINED_MODEL_MANIFEST = RUN_DIR / "repaired_trained_model_manifest.csv"
REPAIRED_SCORECARD = RUN_DIR / "repaired_model_scorecard.csv"
ONNX_PARITY = RUN_DIR / "onnx_parity_matrix.csv"
EXTENDED_CONTROL_SCORECARD = RUN_DIR / "extended_control_scorecard.csv"
COST_CURVE_SCORECARD = RUN_DIR / "cost_curve_shape_scorecard.csv"
POLICY_DAY_CONCENTRATION = RUN_DIR / "policy_day_concentration_matrix.csv"
PROXY_EXPECTED = RUN_DIR / "repaired_proxy_expected_by_policy.csv"
RUNTIME_DISPOSITION = RUN_DIR / "runtime_probe_release_disposition.csv"
TRAIN_ONLY_POLICY_THRESHOLDS = RUN_DIR / "train_only_policy_thresholds.csv"
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
    CR_FINAL,
    CR_GATES,
    CR_DENSITY_POLICY,
    CR_EXTENDED_SHIFT,
    CR_COST_CONTRACT,
    CR_MT5_LOCK,
    CR_COMPARE_CONTRACT,
    CR_CS_QUEUE,
    CP_WEAKNESS,
    CN_LABEL_FRAME,
    CN_PURGED_MEMBERSHIP,
    SOURCE_MODEL_INPUT,
    CANDIDATE_INPUT_MANIFEST,
)
OUTPUT_FILES = (
    TRAINED_MODEL_MANIFEST,
    REPAIRED_SCORECARD,
    ONNX_PARITY,
    EXTENDED_CONTROL_SCORECARD,
    COST_CURVE_SCORECARD,
    POLICY_DAY_CONCENTRATION,
    PROXY_EXPECTED,
    RUNTIME_DISPOSITION,
    TRAIN_ONLY_POLICY_THRESHOLDS,
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

MODEL_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "contract_id",
    "model_family",
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
SCORE_COLUMNS = (
    "policy_id",
    "model_id",
    "label_candidate_id",
    "contract_id",
    "model_family",
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
PARITY_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "contract_id",
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
CONTROL_COLUMNS = (
    "policy_id",
    "model_id",
    "label_candidate_id",
    "contract_id",
    "density_floor",
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
    "max_day_trade_share",
    "cost_status",
    "blocks_runtime_probe",
    "claim_boundary",
)
DAY_COLUMNS = (
    "policy_id",
    "model_id",
    "split",
    "date",
    "rows",
    "traded_rows",
    "day_trade_share",
    "decision_short",
    "decision_long",
    "net_proxy_return",
    "claim_boundary",
)
PROXY_COLUMNS = (
    "policy_id",
    "model_id",
    "label_candidate_id",
    "contract_id",
    "density_floor",
    "source_row_id",
    "timestamp",
    "effective_split",
    "true_label_class",
    "p_short",
    "p_flat",
    "p_long",
    "decision_label",
    "decision_label_class",
    "decision_probability",
    "decision_margin",
    "raw_trade_return",
    "policy_threshold_id",
    "claim_boundary",
)
RUNTIME_COLUMNS = (
    "policy_id",
    "model_id",
    "label_candidate_id",
    "contract_id",
    "density_floor",
    "onnx_path",
    "mt5_probe_disposition",
    "release_blockers",
    "next_condition",
    "claim_boundary",
)
POLICY_THRESHOLD_COLUMNS = (
    "policy_id",
    "model_id",
    "density_floor",
    "train_directional_cutoff",
    "train_signal_density",
    "selector_source",
    "forbidden_action",
    "claim_boundary",
)
FEATURE_COLUMNS = ("source_path", "rows", "feature_count", "feature_order_hash", "missing_features", "nonfinite_rows", "compatibility_status", "claim_boundary")
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")

COST_LEVELS = (0, 1, 2, 5, 10)
COST_UNIT_LOG_RETURN = 1.0e-5


def read_source_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(SOURCE_MODEL_INPUT)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    frame["source_row_id"] = np.arange(len(frame), dtype=np.int64)
    return frame


def read_parquet(path: Path) -> pd.DataFrame:
    return pd.read_parquet(io_path(path))


def label_arrays(label_frame: pd.DataFrame, source_rows: int) -> dict[str, np.ndarray]:
    labels: dict[str, np.ndarray] = {}
    for candidate_id, group in label_frame.groupby("label_candidate_id", sort=True):
        group = group.sort_values("source_row_id")
        if int(group.shape[0]) != source_rows:
            raise RuntimeError(f"Label frame row count mismatch for {candidate_id}: {group.shape[0]}")
        labels[str(candidate_id)] = group["label_class"].to_numpy(dtype=np.int64)
    return labels


def membership_arrays(membership: pd.DataFrame, source_rows: int) -> dict[str, np.ndarray]:
    contracts: dict[str, np.ndarray] = {}
    for contract_id, group in membership.groupby("contract_id", sort=True):
        group = group.sort_values("source_row_id")
        if int(group.shape[0]) != source_rows:
            raise RuntimeError(f"Membership row count mismatch for {contract_id}: {group.shape[0]}")
        contracts[str(contract_id)] = group["effective_split"].astype(str).to_numpy()
    return contracts


def extended_control_arrays(control_frame: pd.DataFrame, source_rows: int) -> dict[tuple[str, str], tuple[np.ndarray, np.ndarray, str]]:
    controls: dict[tuple[str, str], tuple[np.ndarray, np.ndarray, str]] = {}
    for (control_id, candidate_id), group in control_frame.groupby(["control_id", "label_candidate_id"], sort=True):
        group = group.sort_values("source_row_id")
        if int(group.shape[0]) != source_rows:
            raise RuntimeError(f"Extended control row count mismatch for {control_id}/{candidate_id}: {group.shape[0]}")
        family = str(group["control_family"].iloc[0])
        controls[(str(control_id), str(candidate_id))] = (
            group["control_label_class"].to_numpy(dtype=np.int64),
            group["usable"].astype(bool).to_numpy(),
            family,
        )
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
    quantile = max(0.0, min(1.0, 1.0 - float(density_floor)))
    return float(max(0.0, np.quantile(finite, quantile)))


def safe_balanced(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    if len(y_true) < 3 or len(np.unique(y_true)) < 2 or len(np.unique(y_pred)) < 2:
        return 0.0
    return float(balanced_accuracy_score(y_true, y_pred))


def raw_trade_returns(returns: np.ndarray, decision_classes: np.ndarray) -> np.ndarray:
    return np.where(decision_classes == 2, returns, np.where(decision_classes == 0, -returns, 0.0)).astype(float)


def score_policy_split(
    policy: Mapping[str, str],
    model_family: str,
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
    density_floor = float(policy["density_floor"])
    validation_gate = "not_applicable"
    oos_gate = "not_applicable"
    model_balanced = safe_balanced(y_true, y_pred)
    signal_density = float(trade_mask.mean())
    if split == "validation":
        validation_gate = "passed" if model_balanced >= 0.40 and signal_density >= density_floor else "failed"
    if split == "oos":
        oos_gate = "passed_readonly" if model_balanced >= 0.40 and signal_density >= density_floor else "failed_readonly"
    return {
        "policy_id": policy["policy_id"],
        "model_id": policy["source_model_id"],
        "label_candidate_id": policy["label_candidate_id"],
        "contract_id": policy["contract_id"],
        "model_family": model_family,
        "density_floor": density_floor,
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


def score_extended_controls(
    policy: Mapping[str, str],
    split: str,
    y: np.ndarray,
    split_indices: np.ndarray,
    decisions: pd.DataFrame,
    controls: Mapping[tuple[str, str], tuple[np.ndarray, np.ndarray, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    decision_classes = decisions["decision_label_class"].to_numpy(dtype=np.int64)
    trade_local = decision_classes != -1
    for control_id in ("label_shift_gap72_control", "label_shift_gap96_control", "horizon_modulo_fold_control"):
        control_y, usable, family = controls[(control_id, policy["label_candidate_id"])]
        usable_local = usable[split_indices] & trade_local & (control_y[split_indices] != -1)
        local_rows = np.flatnonzero(usable_local)
        if len(local_rows) < 10:
            actual_balanced = 0.0
            control_balanced = 0.0
            status = "block_insufficient_control_trades"
            blocks = True
        else:
            source_rows = split_indices[local_rows]
            actual_balanced = safe_balanced(y[source_rows], decision_classes[local_rows])
            control_balanced = safe_balanced(control_y[source_rows], decision_classes[local_rows])
            passed = actual_balanced >= 0.40 and control_balanced < actual_balanced and control_balanced < 0.45
            status = "passed_control_weakened" if passed else "block_extended_control_not_weakened"
            blocks = not passed
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "model_id": policy["source_model_id"],
                "label_candidate_id": policy["label_candidate_id"],
                "contract_id": policy["contract_id"],
                "density_floor": float(policy["density_floor"]),
                "control_id": control_id,
                "control_family": family,
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


def curve_stats(values: np.ndarray, dates: np.ndarray, trade_mask: np.ndarray) -> tuple[float, float, float, float, float]:
    if len(values) == 0:
        return 0.0, 0.0, 0.0, 0.0, 0.0
    equity = np.cumsum(values)
    running_high = np.maximum.accumulate(equity)
    drawdown = running_high - equity
    max_drawdown = float(drawdown.max()) if len(drawdown) else 0.0
    chunks = np.array_split(values, min(20, max(1, len(values))))
    worst_chunk = float(min(float(chunk.sum()) for chunk in chunks)) if chunks else 0.0
    underwater = equity < running_high
    max_underwater = 0
    current = 0
    for flag in underwater:
        current = current + 1 if bool(flag) else 0
        max_underwater = max(max_underwater, current)
    if int(trade_mask.sum()) == 0:
        max_day_share = 0.0
    else:
        day_counts = pd.Series(dates[trade_mask]).value_counts()
        max_day_share = float(day_counts.max() / int(trade_mask.sum())) if len(day_counts) else 0.0
    return max_drawdown, worst_chunk, float(max_underwater), max_day_share, float(equity[-1]) if len(equity) else 0.0


def score_cost_curve(
    policy: Mapping[str, str],
    split: str,
    returns: np.ndarray,
    dates: np.ndarray,
    decisions: pd.DataFrame,
) -> list[dict[str, Any]]:
    decision_classes = decisions["decision_label_class"].to_numpy(dtype=np.int64)
    trade_mask = decision_classes != -1
    raw_values = raw_trade_returns(returns, decision_classes)
    rows: list[dict[str, Any]] = []
    base_net = None
    for cost_points in COST_LEVELS:
        cost_values = raw_values.copy()
        cost_values[trade_mask] -= float(cost_points) * COST_UNIT_LOG_RETURN
        net = float(cost_values.sum())
        base_net = net if base_net is None else base_net
        gross_profit = float(cost_values[cost_values > 0].sum())
        gross_loss = float(-cost_values[cost_values < 0].sum())
        if gross_loss > 0:
            profit_factor = gross_profit / gross_loss
        elif gross_profit > 0:
            profit_factor = math.inf
        else:
            profit_factor = 0.0
        max_dd, worst_chunk, max_underwater, max_day_share, _ = curve_stats(cost_values, dates, trade_mask)
        recovery = net / max_dd if max_dd > 0 else (math.inf if net > 0 else 0.0)
        expectancy = net / int(trade_mask.sum()) if int(trade_mask.sum()) else 0.0
        smooth_cost = cost_points == 0 or (base_net is not None and (net <= base_net + 1.0e-12))
        passed = int(trade_mask.sum()) >= 10 and smooth_cost and max_day_share <= 0.35
        if cost_points in (0, 1, 2):
            passed = passed and net > 0.0
        status = "passed_proxy_cost_shape" if passed else "block_proxy_cost_shape"
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "model_id": policy["source_model_id"],
                "split": split,
                "cost_points": int(cost_points),
                "trade_count": int(trade_mask.sum()),
                "signal_density": float(trade_mask.mean()),
                "net_proxy_return": net,
                "gross_profit": gross_profit,
                "gross_loss": gross_loss,
                "profit_factor": profit_factor,
                "expectancy": expectancy,
                "max_drawdown": max_dd,
                "recovery_factor": recovery,
                "worst_chunk_return": worst_chunk,
                "max_underwater_bars": max_underwater,
                "max_day_trade_share": max_day_share,
                "cost_status": status,
                "blocks_runtime_probe": str(not passed).lower(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def day_concentration_rows(
    policy: Mapping[str, str],
    split: str,
    returns: np.ndarray,
    dates: np.ndarray,
    decisions: pd.DataFrame,
) -> list[dict[str, Any]]:
    frame = decisions.copy()
    frame["date"] = dates
    frame["raw_trade_return"] = raw_trade_returns(returns, frame["decision_label_class"].to_numpy(dtype=np.int64))
    total_trades = int((frame["decision_label"] != "no_trade").sum())
    rows: list[dict[str, Any]] = []
    for date, group in frame.groupby("date", sort=True):
        trades = int((group["decision_label"] != "no_trade").sum())
        counts = group["decision_label"].value_counts().to_dict()
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "model_id": policy["source_model_id"],
                "split": split,
                "date": date,
                "rows": int(group.shape[0]),
                "traded_rows": trades,
                "day_trade_share": float(trades / total_trades) if total_trades else 0.0,
                "decision_short": int(counts.get("short", 0)),
                "decision_long": int(counts.get("long", 0)),
                "net_proxy_return": float(group["raw_trade_return"].sum()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def train_and_score() -> dict[str, Any]:
    df = read_source_frame()
    source_manifest = read_json(CANDIDATE_INPUT_MANIFEST)
    features = [str(item) for item in source_manifest.get("feature_columns", [])]
    if not features:
        raise RuntimeError("candidate_training_input_manifest.json has no feature_columns.")
    X = df.loc[:, features].to_numpy(dtype=np.float64, copy=False)
    nonfinite_rows = int((~np.isfinite(X).all(axis=1)).sum())
    if nonfinite_rows:
        raise RuntimeError(f"Model input has nonfinite rows: {nonfinite_rows}")
    returns_all = df["future_log_return_12"].astype(float).to_numpy()
    dates_all = df["timestamp"].dt.strftime("%Y-%m-%d").to_numpy()

    label_map = label_arrays(read_parquet(CN_LABEL_FRAME), len(df))
    member_map = membership_arrays(read_parquet(CN_PURGED_MEMBERSHIP), len(df))
    controls = extended_control_arrays(read_parquet(CR_EXTENDED_SHIFT), len(df))
    policy_rows = read_csv(CR_DENSITY_POLICY)
    weak_rows = read_csv(CP_WEAKNESS)
    weak_by_model = {row["model_id"]: row for row in weak_rows}
    policies_by_model: dict[str, list[Mapping[str, str]]] = {}
    for policy in policy_rows:
        source_model = policy["source_model_id"]
        if source_model not in weak_by_model:
            raise RuntimeError(f"Policy references unknown weak model: {source_model}")
        policies_by_model.setdefault(source_model, []).append(policy)

    io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    io_path(ONNX_DIR).mkdir(parents=True, exist_ok=True)

    model_rows: list[dict[str, Any]] = []
    score_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    cost_rows: list[dict[str, Any]] = []
    day_rows: list[dict[str, Any]] = []
    proxy_rows: list[dict[str, Any]] = []
    runtime_rows: list[dict[str, Any]] = []
    threshold_rows: list[dict[str, Any]] = []
    feature_hash = str(source_manifest.get("feature_order_hash", ""))

    for model_id, policies in sorted(policies_by_model.items()):
        weak = weak_by_model[model_id]
        candidate_id = weak["label_candidate_id"]
        contract_id = weak["contract_id"]
        model_family = weak["model_family"]
        y = label_map[candidate_id]
        split_values = member_map[contract_id]
        split_indices = {split: np.flatnonzero(split_values == split) for split in ("train", "validation", "oos")}
        model = build_model(model_family)
        model.fit(X[split_indices["train"]], y[split_indices["train"]])
        model_path = MODEL_DIR / f"{model_id}.joblib"
        onnx_path = ONNX_DIR / f"{model_id}.onnx"
        joblib.dump(model, io_path(model_path))
        export_info = export_sklearn_to_onnx_zipmap_disabled(
            model,
            onnx_path,
            feature_count=len(features),
            target_opset=12,
            drop_label_output=True,
        )
        sample = X[split_indices["validation"]][: min(512, len(split_indices["validation"]))]
        parity = check_onnxruntime_probability_parity(model, onnx_path, sample, tolerance=1.0e-5)
        parity_rows.append(
            {
                "model_id": model_id,
                "label_candidate_id": candidate_id,
                "contract_id": contract_id,
                "onnx_path": rel(onnx_path),
                "passed": str(bool(parity["passed"])).lower(),
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
                "label_candidate_id": candidate_id,
                "contract_id": contract_id,
                "model_family": model_family,
                "feature_count": len(features),
                "feature_order_hash": feature_hash,
                "model_path": rel(model_path),
                "model_sha256": sha256_file(model_path),
                "onnx_path": rel(onnx_path),
                "onnx_sha256": sha256_file(onnx_path),
                "onnx_probability_output_name": export_info["probability_output_name"],
                "train_rows": int(len(split_indices["train"])),
                "validation_rows": int(len(split_indices["validation"])),
                "oos_rows": int(len(split_indices["oos"])),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        probabilities_by_split = {
            split: ordered_sklearn_probabilities(model, X[idx], class_order=LABEL_ORDER)
            for split, idx in split_indices.items()
        }
        for policy in sorted(policies, key=lambda row: float(row["density_floor"])):
            density_floor = float(policy["density_floor"])
            cutoff = train_cutoff(probabilities_by_split["train"], density_floor)
            train_decisions = directional_policy(probabilities_by_split["train"], cutoff)
            threshold_rows.append(
                {
                    "policy_id": policy["policy_id"],
                    "model_id": model_id,
                    "density_floor": density_floor,
                    "train_directional_cutoff": cutoff,
                    "train_signal_density": float((train_decisions["decision_label"] != "no_trade").mean()),
                    "selector_source": "train_split_only_directional_margin_quantile(학습 분할 전용 방향 마진 분위수)",
                    "forbidden_action": "no validation/OOS threshold tuning(검증/OOS 임계값 조정 금지)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            split_decisions: dict[str, pd.DataFrame] = {}
            for split in ("train", "validation", "oos"):
                idx = split_indices[split]
                probs = probabilities_by_split[split]
                decisions = directional_policy(probs, cutoff)
                split_decisions[split] = decisions
                split_returns = returns_all[idx]
                split_dates = dates_all[idx]
                score_rows.append(score_policy_split(policy, model_family, split, y[idx], split_returns, probs, decisions, cutoff))
                if split in ("validation", "oos"):
                    control_rows.extend(score_extended_controls(policy, split, y, idx, decisions, controls))
                    cost_rows.extend(score_cost_curve(policy, split, split_returns, split_dates, decisions))
                    day_rows.extend(day_concentration_rows(policy, split, split_returns, split_dates, decisions))
                if split == "oos":
                    raw_returns = raw_trade_returns(split_returns, decisions["decision_label_class"].to_numpy(dtype=np.int64))
                    for local_idx, source_row_id in enumerate(idx):
                        proxy_rows.append(
                            {
                                "policy_id": policy["policy_id"],
                                "model_id": model_id,
                                "label_candidate_id": candidate_id,
                                "contract_id": contract_id,
                                "density_floor": density_floor,
                                "source_row_id": int(source_row_id),
                                "timestamp": str(df.loc[source_row_id, "timestamp"]),
                                "effective_split": "oos",
                                "true_label_class": int(y[source_row_id]),
                                "p_short": float(probs[local_idx, 0]),
                                "p_flat": float(probs[local_idx, 1]),
                                "p_long": float(probs[local_idx, 2]),
                                "decision_label": str(decisions.loc[local_idx, "decision_label"]),
                                "decision_label_class": int(decisions.loc[local_idx, "decision_label_class"]),
                                "decision_probability": float(decisions.loc[local_idx, "decision_probability"]),
                                "decision_margin": float(decisions.loc[local_idx, "decision_margin"]),
                                "raw_trade_return": float(raw_returns[local_idx]),
                                "policy_threshold_id": policy["policy_id"],
                                "claim_boundary": CLAIM_BOUNDARY,
                            }
                        )

            validation_score = next(row for row in score_rows if row["policy_id"] == policy["policy_id"] and row["split"] == "validation")
            oos_score = next(row for row in score_rows if row["policy_id"] == policy["policy_id"] and row["split"] == "oos")
            policy_controls = [row for row in control_rows if row["policy_id"] == policy["policy_id"] and row["blocks_runtime_probe"] == "true"]
            policy_costs = [row for row in cost_rows if row["policy_id"] == policy["policy_id"] and row["split"] == "oos" and row["blocks_runtime_probe"] == "true"]
            blockers: list[str] = []
            if validation_score["validation_gate_status"] != "passed":
                blockers.append("validation_density_or_balanced_gate_failed")
            if oos_score["oos_readonly_gate_status"] != "passed_readonly":
                blockers.append("oos_readonly_density_or_balanced_gate_failed")
            if policy_controls:
                blockers.append("extended_control_block")
            if policy_costs:
                blockers.append("proxy_cost_curve_block")
            if parity["passed"] is not True:
                blockers.append("onnx_parity_failed")
            disposition = "release_review_ready_no_mt5_executed" if not blockers else "held_by_cs_release_lock"
            runtime_rows.append(
                {
                    "policy_id": policy["policy_id"],
                    "model_id": model_id,
                    "label_candidate_id": candidate_id,
                    "contract_id": contract_id,
                    "density_floor": density_floor,
                    "onnx_path": rel(onnx_path),
                    "mt5_probe_disposition": disposition,
                    "release_blockers": ";".join(sorted(set(blockers))) or "none",
                    "next_condition": NEXT_RUN_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    compatibility_rows = [
        {
            "source_path": rel(SOURCE_MODEL_INPUT),
            "rows": int(len(df)),
            "feature_count": len(features),
            "feature_order_hash": feature_hash,
            "missing_features": "",
            "nonfinite_rows": nonfinite_rows,
            "compatibility_status": "passed",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return {
        "model_rows": model_rows,
        "score_rows": score_rows,
        "parity_rows": parity_rows,
        "control_rows": control_rows,
        "cost_rows": cost_rows,
        "day_rows": day_rows,
        "proxy_rows": proxy_rows,
        "runtime_rows": runtime_rows,
        "threshold_rows": threshold_rows,
        "compatibility_rows": compatibility_rows,
        "feature_count": len(features),
        "source_rows": int(len(df)),
        "policy_rows": len(policy_rows),
        "weak_rows": len(weak_rows),
    }


def build_gates(result: Mapping[str, Any]) -> list[dict[str, str]]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]
    cr_final = read_json(CR_FINAL)
    parity_passed = sum(1 for row in result["parity_rows"] if row["passed"] == "true")
    runtime_released = [row for row in result["runtime_rows"] if row["mt5_probe_disposition"] == "release_review_ready_no_mt5_executed"]

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
        row("cs_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CR/CN/CP evidence(근거)를 연결했다."),
        row("cs_gate_parent_points_to_cs", cr_final.get("next_action", "") == RUN_ID, cr_final.get("next_action", ""), RUN_ID, "CR next_action(다음 행동)과 CS run(실행)이 맞는다."),
        row("cs_gate_policy_grid", result["policy_rows"] == 16, result["policy_rows"], "16", "train-only density policies(학습 전용 밀도 정책)를 모두 사용했다."),
        row("cs_gate_models_trained", len(result["model_rows"]) == 4, len(result["model_rows"]), "4", "weak model source(약한 모델 원천) 4개를 제한 재학습했다."),
        row("cs_gate_scorecard_rows", len(result["score_rows"]) == 48, len(result["score_rows"]), "policy_rows*3 splits", "정책별 학습/검증/OOS 점수표를 만들었다."),
        row("cs_gate_onnx_parity", parity_passed == 4 and len(result["parity_rows"]) == 4, f"{parity_passed}/{len(result['parity_rows'])}", "4/4", "Python/ONNX(파이썬/온엑스) 확률 동등성을 확인했다."),
        row("cs_gate_extended_controls", len(result["control_rows"]) == 96, len(result["control_rows"]), "policy_rows*3 controls*2 splits", "확장 이동 대조를 정책별로 기록했다."),
        row("cs_gate_cost_curve_rows", len(result["cost_rows"]) == 160, len(result["cost_rows"]), "policy_rows*5 costs*2 splits", "비용/곡선 압박을 정책별로 기록했다."),
        row("cs_gate_runtime_disposition", len(result["runtime_rows"]) == 16, len(result["runtime_rows"]), "16", "MT5 release disposition(MT5 해제 처분)을 정책별로 남겼다."),
        row("cs_gate_no_mt5_forward_goal", True, "mt5=not_run;forward=not_claimed;goal=not_claimed", "no MT5/Forward/Goal", "CS는 학습/진단만 수행한다."),
        row("cs_gate_release_lock_enforced", len(runtime_released) == 0, len(runtime_released), "0 release rows before CT review", "release lock(해제 잠금)을 CT 검토 전 유지한다."),
    ]


def write_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "source timestamp sorted by existing M5 bar order(기존 M5 봉 순서로 원천 시각 정렬)",
        "sample_scope": "existing Stage337 train/validation/OOS rows; no new forward data(기존 Stage337 학습/검증/OOS 행, 새 전진 데이터 없음)",
        "missing_or_duplicate_check": "source rows and policy rows gate-checked(원천 행과 정책 행을 게이트로 확인)",
        "feature_label_boundary": "labels from CN reused; density cutoff from train split only(CN 라벨 재사용, 밀도 절단값은 학습 분할 전용)",
        "split_boundary": "validation/OOS are read-only gates, not threshold sources(검증/OOS는 읽기 전용 게이트, 임계값 원천 아님)",
        "leakage_risk": "using validation/OOS to choose density policy after scoring(채점 뒤 검증/OOS로 밀도 정책 선택)",
        "data_hash_or_identity": {"source_sha256": final["source_sha256"], "source_rows": final["source_rows"]},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "extratrees_depth6_leaf160 weak-density repair lane(약한 밀도 수리 축)",
        "target_and_label": "label_v3_volnorm_margin_q50_train_only under purged embargo contracts(제거/격리 계약의 volnorm q50 라벨)",
        "split_method": "purged embargo train/validation/OOS with train-only density cutoff(제거/격리 분할과 학습 전용 밀도 절단값)",
        "selection_metric": "none_no_candidate_selection(없음, 후보 선택 아님)",
        "secondary_metrics": "validation/OOS balanced accuracy, density, extended controls, cost curve, ONNX parity(검증/OOS 균형 정확도, 밀도, 확장 대조, 비용 곡선, 온엑스 동등성)",
        "threshold_policy": "train-only directional margin quantile per density floor(밀도 하한별 학습 전용 방향 마진 분위수)",
        "overfit_risk": "choosing the best density after OOS read(OOS 판독 뒤 최고 밀도 선택)",
        "calibration_risk": "probabilities used as ranking scores, not calibrated probabilities(확률은 보정 확률이 아니라 순위 점수로 사용)",
        "comparison_baseline": "CP weak models and CR repair policy grid(CP 약한 모델과 CR 수리 정책 격자)",
        "validation_judgment": "release_lock_review_required(해제 잠금 검토 필요)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": "density policy scorecards and proxy cost curves materialized(밀도 정책 점수표와 프록시 비용 곡선 물질화)",
        "comparison_baseline": "CP weak density review(CP 약한 밀도 검토)",
        "likely_drivers": "train-only cutoff changes traded rows, not model probabilities(학습 전용 절단값이 거래 행만 바꾸고 모델 확률은 바꾸지 않음)",
        "segment_checks": "day concentration, long/short action, cost ladder, extended controls(일 집중도, 롱/숏 행동, 비용 사다리, 확장 대조)",
        "trade_shape": f"policy_rows={final['policy_rows']}; runtime_release_rows={final['runtime_release_rows']}",
        "alternative_explanations": "weak classifier, stale feature carry, calendar concentration(약한 분류기, 낡은 피처 이월, 달력 집중)",
        "attribution_confidence": "medium_diagnostic_only(중간, 진단 전용)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime_receipt = {
        "runtime_subject": RUN_ID,
        "parity_check": f"onnxruntime parity rows={final['onnx_parity_passed']}/{final['onnx_parity_rows']}",
        "mt5_probe": "not_run_release_lock_held(MT5 탐침 없음, 해제 잠금 유지)",
        "proxy_mt5_compare_contract": rel(CR_COMPARE_CONTRACT),
        "release_rows": final["runtime_release_rows"],
        "runtime_judgment": "no_runtime_authority_review_required(런타임 권위 없음, 검토 필요)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "trained models, ONNX parity, policy scorecards, extended controls, cost curves, release disposition(학습 모델, 온엑스 동등성, 정책 점수표, 확장 대조, 비용 곡선, 해제 처분)",
        "evidence_missing": "MT5 runtime probe and CT review(MT5 런타임 탐침과 CT 검토)",
        "judgment_label": "exploratory_release_lock_review_required(탐색, 해제 잠금 검토 필요)",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "정책과 모델은 만들었지만, MT5로 보낼 권한은 아직 없다.",
    }
    receipt_paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
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
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers(02_runs는 목록/해시로 추적, 보고서와 장부는 저장소 추적)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipt_paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return receipt_paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CS Weak Density/Control Repaired Training(약한 밀도/대조 수리 학습)

## Conclusion(결론)

run337CS(337CS 실행)는 run337CR(337CR 실행)의 train-only density policy(학습 전용 밀도 정책)로 4개 weak model(약한 모델)과 16개 policy view(정책 보기)를 학습/채점했다.

Effect(효과): density cutoff(밀도 절단값)는 train split(학습 분할)에서만 만들었고 validation/OOS(검증/OOS)는 읽기 전용 gate(게이트)로만 썼다. MT5 probe(MT5 탐침), Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 주장하지 않는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- trained_models(학습 모델): `{final["trained_models"]}`
- policy_rows(정책 행): `{final["policy_rows"]}`
- scorecard_rows(점수표 행): `{final["scorecard_rows"]}`
- extended_control_rows(확장 대조 행): `{final["extended_control_rows"]}`
- cost_curve_rows(비용 곡선 행): `{final["cost_curve_rows"]}`
- onnx_parity(온엑스 동등성): `{final["onnx_parity_passed"]}/{final["onnx_parity_rows"]}`
- runtime_release_rows(MT5 해제 후보 행): `{final["runtime_release_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- candidate_selection(후보 선택): `not_run`
- validation/OOS threshold tuning(검증/OOS 임계값 조정): `not_run`
- lot_optimization(랏 최적화): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CS

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): train-only density repair training(학습 전용 밀도 수리 학습)을 만들고 CT review(CT 검토)를 열었다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(RUNTIME_DISPOSITION)}`, `{rel(COST_CURVE_SCORECARD)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{final["passed_gates"]}/{final["gate_rows"]}`
- MT5 probe(MT5 탐침): `not_run`
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
        f"  Stage337 run337CS focus complete: weak density/control repaired training(약한 밀도/대조 수리 학습)을 `{STATUS}`로 닫았다. "
        "Effect(효과): run337CT(337CT 실행)에서 release lock(해제 잠금), density/cost/control 결과를 검토한다."
    )
    if "Stage337 run337CS focus complete" in workspace_text:
        workspace_text = re.sub(
            r"current_focus:\n- >-\n  Stage337 run337CS focus complete:.*?(?=\n- >-\n  Stage337 run337CR|\n[A-Za-z0-9_]+:)",
            focus_entry,
            workspace_text,
            count=1,
            flags=re.DOTALL,
        )
    else:
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
## Stage337 run337CS(337CS 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): trained_models(학습 모델) `{final['trained_models']}`, policy_rows(정책 행) `{final['policy_rows']}`, release_rows(해제 후보 행) `{final['runtime_release_rows']}`를 기록했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current_text = re.sub(
        r"\n## Stage337 run337CS\(337CS 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CR|\Z)",
        "\n",
        current_text,
        count=1,
        flags=re.DOTALL,
    )
    marker = "## Stage337 run337CR(337CR"
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
- actual_mt5_execution(실제 MT5 실행): `held_by_cs_release_lock_no_mt5`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 weak density/control repaired training review(약한 밀도/대조 수리 학습 검토)다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337CS(337CS 실행)" not in line)
    stage_entry = (
        f"- {TODAY}: run337CS(337CS 실행) trained weak density/control repaired candidates(약한 밀도/대조 수리 후보). "
        f"Status(상태) `{STATUS}`. Release rows(해제 후보 행) `{final['runtime_release_rows']}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(line for line in changelog_text.splitlines() if "Stage337 run337CS trained weak density/control repaired candidates" not in line)
    changelog_entry = f"- {TODAY}: Stage337 run337CS trained weak density/control repaired candidates(약한 밀도/대조 수리 후보) and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "weak_density_control_repaired_training_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"models={final['trained_models']};policy_rows={final['policy_rows']};release_rows={final['runtime_release_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_data_integrity_performance_attribution_runtime_parity",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__density_repair_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "density_repair_training",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "limited_training_and_release_lock",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "training_diagnostics_no_selection",
        "scoreboard_lane": "model_validation_runtime_parity",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"models={final['trained_models']};scorecard_rows={final['scorecard_rows']};release_rows={final['runtime_release_rows']}",
        "guardrail_kpi": "train_only_density;extended_controls;cost_curve;onnx_parity;no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__density_repair_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_data_integrity_performance_attribution_runtime_parity",
        "evidence_scope": "CR repair inputs converted to limited training diagnostics",
        "kpi_scope": "training_diagnostics_no_selection",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};runtime_release_rows={final['runtime_release_rows']};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__density_repair_training",
        "family": "model_validation_data_integrity_performance_attribution_runtime_parity",
        "question": "do weak density/control repaired policies survive train-only density and release locks",
        "metric_scope": "scorecard_extended_controls_cost_curve_onnx_parity_release_lock",
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
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    result = train_and_score()
    gates = build_gates(result)
    parity_passed = sum(1 for row in result["parity_rows"] if row["passed"] == "true")
    runtime_release_rows = [row for row in result["runtime_rows"] if row["mt5_probe_disposition"] == "release_review_ready_no_mt5_executed"]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "source_rows": result["source_rows"],
        "source_sha256": sha256_file(SOURCE_MODEL_INPUT),
        "feature_count": result["feature_count"],
        "weak_rows": result["weak_rows"],
        "policy_rows": result["policy_rows"],
        "trained_models": len(result["model_rows"]),
        "scorecard_rows": len(result["score_rows"]),
        "onnx_parity_rows": len(result["parity_rows"]),
        "onnx_parity_passed": parity_passed,
        "extended_control_rows": len(result["control_rows"]),
        "extended_control_block_rows": sum(1 for row in result["control_rows"] if row["blocks_runtime_probe"] == "true"),
        "cost_curve_rows": len(result["cost_rows"]),
        "cost_curve_block_rows": sum(1 for row in result["cost_rows"] if row["blocks_runtime_probe"] == "true"),
        "proxy_expected_rows": len(result["proxy_rows"]),
        "runtime_disposition_rows": len(result["runtime_rows"]),
        "runtime_release_rows": len(runtime_release_rows),
        "runtime_held_rows": len(result["runtime_rows"]) - len(runtime_release_rows),
        "model_training": "limited_train_only_density_repair",
        "validation_oos_threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]

    artifacts: list[Path] = [
        write_csv(TRAINED_MODEL_MANIFEST, MODEL_COLUMNS, result["model_rows"]),
        write_csv(REPAIRED_SCORECARD, SCORE_COLUMNS, result["score_rows"]),
        write_csv(ONNX_PARITY, PARITY_COLUMNS, result["parity_rows"]),
        write_csv(EXTENDED_CONTROL_SCORECARD, CONTROL_COLUMNS, result["control_rows"]),
        write_csv(COST_CURVE_SCORECARD, COST_COLUMNS, result["cost_rows"]),
        write_csv(POLICY_DAY_CONCENTRATION, DAY_COLUMNS, result["day_rows"]),
        write_csv(PROXY_EXPECTED, PROXY_COLUMNS, result["proxy_rows"]),
        write_csv(RUNTIME_DISPOSITION, RUNTIME_COLUMNS, result["runtime_rows"]),
        write_csv(TRAIN_ONLY_POLICY_THRESHOLDS, POLICY_THRESHOLD_COLUMNS, result["threshold_rows"]),
        write_csv(FEATURE_COMPATIBILITY, FEATURE_COLUMNS, result["compatibility_rows"]),
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
    artifacts.extend(write_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
