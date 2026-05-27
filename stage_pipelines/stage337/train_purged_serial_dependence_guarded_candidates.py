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
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.baseline_training import LABEL_ORDER  # noqa: E402
from foundation.models.decision_surface import ThresholdRule, apply_threshold_rule  # noqa: E402
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
RUN_NUMBER = "run337CO"
RUN_ID = "run337CO_train_purged_serial_dependence_guarded_candidates_without_db_v1"
PARENT_RUN_ID = "run337CN_materialize_serial_dependence_label_boundary_repair_inputs_without_db_v1"
NEXT_RUN_ID = "run337CP_review_purged_serial_dependence_guarded_training_controls_without_db_v1"
STATUS = "completed_stage337CO_purged_serial_dependence_guarded_training_onnx_materialized_control_review_required_no_selection"
JUDGMENT = "exploratory_purged_guarded_models_trained_onnx_parity_control_review_required_no_forward_selection"
DECISION = "stage337CO_open_run337CP_review_purged_serial_dependence_guarded_training_controls"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CO_purged_serial_dependence_guarded_training_without_db_"
    "diagnostic_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CO_purged_guarded_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CO_purged_guarded_training.md"
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
CN_FINAL = CN_DIR / "final_decision.json"
CN_GATES = CN_DIR / "required_gate_coverage_audit.csv"
CN_REPAIR_INPUT_MANIFEST = CN_DIR / "repair_input_manifest.json"
CN_LABEL_FRAME = CN_DIR / "candidate_label_frame.parquet"
CN_PURGED_MEMBERSHIP = CN_DIR / "purged_embargo_split_membership.parquet"
CN_SHIFT_CONTROL_FRAME = CN_DIR / "label_shift_control_frame.parquet"
CN_BLOCK_MANIFEST = CN_DIR / "block_permutation_control_manifest.csv"
CN_TASK_MATRIX = CN_DIR / "materialized_training_task_matrix.csv"
CN_QUEUE = CN_DIR / "run337CO_guarded_training_queue.csv"

TRAINED_MODEL_MANIFEST = RUN_DIR / "purged_trained_model_manifest.csv"
MODEL_SCORECARD = RUN_DIR / "purged_guarded_model_scorecard.csv"
ONNX_PARITY = RUN_DIR / "onnxruntime_parity_matrix.csv"
CONTROL_SCORECARD = RUN_DIR / "nonoverlap_control_scorecard.csv"
PROXY_EXPECTED = RUN_DIR / "purged_proxy_expected_by_model.csv"
RUNTIME_DISPOSITION = RUN_DIR / "runtime_probe_disposition.csv"
THRESHOLD_POLICY = RUN_DIR / "decision_threshold_policy.csv"
FEATURE_COMPATIBILITY = RUN_DIR / "feature_input_compatibility.csv"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CN_FINAL,
    CN_GATES,
    CN_REPAIR_INPUT_MANIFEST,
    CN_LABEL_FRAME,
    CN_PURGED_MEMBERSHIP,
    CN_SHIFT_CONTROL_FRAME,
    CN_BLOCK_MANIFEST,
    CN_TASK_MATRIX,
    CN_QUEUE,
    SOURCE_MODEL_INPUT,
    CANDIDATE_INPUT_MANIFEST,
)
OUTPUT_FILES = (
    TRAINED_MODEL_MANIFEST,
    MODEL_SCORECARD,
    ONNX_PARITY,
    CONTROL_SCORECARD,
    PROXY_EXPECTED,
    RUNTIME_DISPOSITION,
    THRESHOLD_POLICY,
    FEATURE_COMPATIBILITY,
    MODEL_RECEIPT,
    DATA_RECEIPT,
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
    "model_id",
    "label_candidate_id",
    "contract_id",
    "model_family",
    "split",
    "rows",
    "accuracy",
    "balanced_accuracy",
    "macro_f1",
    "log_loss",
    "mean_p_short",
    "mean_p_flat",
    "mean_p_long",
    "decision_short",
    "decision_long",
    "decision_no_trade",
    "signal_density",
    "true_short",
    "true_flat",
    "true_long",
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
    "model_id",
    "label_candidate_id",
    "contract_id",
    "control_id",
    "control_family",
    "validation_rows",
    "oos_rows",
    "validation_control_balanced_accuracy",
    "oos_control_balanced_accuracy",
    "validation_actual_balanced_accuracy",
    "oos_actual_balanced_accuracy",
    "oos_control_minus_actual",
    "control_status",
    "blocks_runtime_probe",
    "pass_condition",
    "claim_boundary",
)
PROXY_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "contract_id",
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
    "threshold_id",
    "claim_boundary",
)
RUNTIME_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "contract_id",
    "onnx_path",
    "mt5_probe_disposition",
    "blocking_controls",
    "next_condition",
    "claim_boundary",
)
THRESHOLD_COLUMNS = ("threshold_id", "short_threshold", "long_threshold", "min_margin", "selection_use", "claim_boundary")
FEATURE_COLUMNS = ("source_path", "rows", "feature_count", "feature_order_hash", "missing_features", "nonfinite_rows", "compatibility_status", "claim_boundary")
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")

PRIMARY_RULE = ThresholdRule("fixed_short040_long040_margin002", 0.40, 0.40, 0.02)
MODEL_FAMILIES = ("logreg_balanced_c075", "extratrees_depth6_leaf160")
SHIFT_PASS_LIMITS = {"label_shift_gap24_control": 0.45, "label_shift_gap48_control": 0.42}
DAY_BLOCK_MAX = 0.40


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


def shift_arrays(control_frame: pd.DataFrame, source_rows: int) -> dict[tuple[str, str], tuple[np.ndarray, np.ndarray]]:
    controls: dict[tuple[str, str], tuple[np.ndarray, np.ndarray]] = {}
    for (control_id, candidate_id), group in control_frame.groupby(["control_id", "label_candidate_id"], sort=True):
        group = group.sort_values("source_row_id")
        if int(group.shape[0]) != source_rows:
            raise RuntimeError(f"Shift control row count mismatch for {control_id}/{candidate_id}: {group.shape[0]}")
        controls[(str(control_id), str(candidate_id))] = (
            group["control_label_class"].to_numpy(dtype=np.int64),
            group["usable"].astype(bool).to_numpy(),
        )
    return controls


def block_seed_map(block_manifest: Sequence[Mapping[str, str]]) -> dict[tuple[str, str, str], int]:
    return {
        (row["control_id"], row["split"], row["block_id"]): int(row["permutation_seed"])
        for row in block_manifest
    }


def metric_row(
    model_id: str,
    candidate_id: str,
    contract_id: str,
    model_family: str,
    split: str,
    y_true: np.ndarray,
    probabilities: np.ndarray,
) -> dict[str, Any]:
    y_pred = np.asarray(LABEL_ORDER, dtype=np.int64)[probabilities.argmax(axis=1)]
    decisions = apply_threshold_rule(probabilities, PRIMARY_RULE)
    decision_counts = decisions["decision_label"].value_counts().to_dict()
    true_counts = pd.Series(y_true).value_counts().to_dict()
    return {
        "model_id": model_id,
        "label_candidate_id": candidate_id,
        "contract_id": contract_id,
        "model_family": model_family,
        "split": split,
        "rows": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=LABEL_ORDER, average="macro")),
        "log_loss": float(log_loss(y_true, probabilities, labels=LABEL_ORDER)),
        "mean_p_short": float(probabilities[:, 0].mean()),
        "mean_p_flat": float(probabilities[:, 1].mean()),
        "mean_p_long": float(probabilities[:, 2].mean()),
        "decision_short": int(decision_counts.get("short", 0)),
        "decision_long": int(decision_counts.get("long", 0)),
        "decision_no_trade": int(decision_counts.get("no_trade", 0)),
        "signal_density": float((decisions["decision_label"] != "no_trade").mean()),
        "true_short": int(true_counts.get(0, 0)),
        "true_flat": int(true_counts.get(1, 0)),
        "true_long": int(true_counts.get(2, 0)),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def split_metric(y_true: np.ndarray, y_pred: np.ndarray, mask: np.ndarray) -> tuple[int, float]:
    rows = int(mask.sum())
    if rows < 3:
        return rows, 0.0
    return rows, float(balanced_accuracy_score(y_true[mask], y_pred[mask]))


def permuted_block_labels(
    df: pd.DataFrame,
    y: np.ndarray,
    mask: np.ndarray,
    split: str,
    control_id: str,
    seeds: Mapping[tuple[str, str, str], int],
) -> np.ndarray:
    labels = y.copy()
    selected = df.loc[mask, ["source_row_id", "timestamp"]].copy()
    if control_id == "day_block_permutation_control":
        selected["block_id"] = selected["timestamp"].dt.strftime("%Y-%m-%d")
        default_seed = 337241
    else:
        iso = selected["timestamp"].dt.isocalendar()
        selected["block_id"] = iso["year"].astype(str) + "-W" + iso["week"].astype(str).str.zfill(2)
        default_seed = 337481
    for idx, (block_id, group) in enumerate(selected.groupby("block_id", sort=True)):
        source_ids = group["source_row_id"].to_numpy(dtype=np.int64)
        seed = int(seeds.get((control_id, split, str(block_id)), default_seed + idx))
        rng = np.random.default_rng(seed)
        labels[source_ids] = rng.permutation(labels[source_ids])
    return labels


def control_status(control_id: str, validation_control: float, oos_control: float, validation_actual: float, oos_actual: float) -> tuple[str, bool, str]:
    if control_id in SHIFT_PASS_LIMITS:
        limit = SHIFT_PASS_LIMITS[control_id]
        passed = validation_control < validation_actual and oos_control < oos_actual and max(validation_control, oos_control) < limit
        condition = f"control below actual and below {limit:.2f}(대조가 실제보다 낮고 {limit:.2f} 미만)"
        return ("passed_control_weakened" if passed else "block_shift_control_not_weakened", not passed, condition)
    if control_id == "day_block_permutation_control":
        passed = max(validation_control, oos_control) < DAY_BLOCK_MAX
        condition = f"balanced_accuracy near random below {DAY_BLOCK_MAX:.2f}(무작위 근처 {DAY_BLOCK_MAX:.2f} 미만)"
        return ("passed_block_randomized" if passed else "review_block_control_alignment", not passed, condition)
    if control_id == "week_block_permutation_control":
        passed = validation_control < validation_actual and oos_control < oos_actual
        condition = "control below actual(대조가 실제보다 낮음)"
        return ("passed_week_block_below_actual" if passed else "review_week_block_alignment", not passed, condition)
    raise ValueError(f"Unknown control_id: {control_id}")


def score_controls(
    model_id: str,
    candidate_id: str,
    contract_id: str,
    df: pd.DataFrame,
    y: np.ndarray,
    split_values: np.ndarray,
    predictions: Mapping[str, np.ndarray],
    split_indices: Mapping[str, np.ndarray],
    shift_map: Mapping[tuple[str, str], tuple[np.ndarray, np.ndarray]],
    seeds: Mapping[tuple[str, str, str], int],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    actual_scores = {}
    for split in ("validation", "oos"):
        idx = split_indices[split]
        actual_scores[split] = float(balanced_accuracy_score(y[idx], predictions[split]))

    for control_id in ("label_shift_gap24_control", "label_shift_gap48_control"):
        control_y, usable = shift_map[(control_id, candidate_id)]
        metrics = {}
        actual_same_rows = {}
        for split in ("validation", "oos"):
            idx = split_indices[split]
            mask_full = np.zeros(len(y), dtype=bool)
            mask_full[idx] = True
            usable_mask = mask_full & usable & (split_values == split)
            local_rows = np.flatnonzero(usable_mask)
            if len(local_rows) < 3:
                metrics[split] = (len(local_rows), 0.0)
                actual_same_rows[split] = 0.0
                continue
            pred_local = predictions[split][np.isin(idx, local_rows)]
            metrics[split] = (len(local_rows), float(balanced_accuracy_score(control_y[local_rows], pred_local)))
            actual_same_rows[split] = float(balanced_accuracy_score(y[local_rows], pred_local))
        status, blocks, condition = control_status(
            control_id,
            metrics["validation"][1],
            metrics["oos"][1],
            actual_same_rows["validation"],
            actual_same_rows["oos"],
        )
        rows.append(
            {
                "model_id": model_id,
                "label_candidate_id": candidate_id,
                "contract_id": contract_id,
                "control_id": control_id,
                "control_family": "split_local_shift(분할 내부 이동)",
                "validation_rows": metrics["validation"][0],
                "oos_rows": metrics["oos"][0],
                "validation_control_balanced_accuracy": metrics["validation"][1],
                "oos_control_balanced_accuracy": metrics["oos"][1],
                "validation_actual_balanced_accuracy": actual_same_rows["validation"],
                "oos_actual_balanced_accuracy": actual_same_rows["oos"],
                "oos_control_minus_actual": metrics["oos"][1] - actual_same_rows["oos"],
                "control_status": status,
                "blocks_runtime_probe": str(blocks).lower(),
                "pass_condition": condition,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for control_id in ("day_block_permutation_control", "week_block_permutation_control"):
        metrics = {}
        for split in ("validation", "oos"):
            idx = split_indices[split]
            mask = split_values == split
            permuted = permuted_block_labels(df, y, mask, split, control_id, seeds)
            if len(idx) < 3:
                metrics[split] = (len(idx), 0.0)
            else:
                metrics[split] = (len(idx), float(balanced_accuracy_score(permuted[idx], predictions[split])))
        status, blocks, condition = control_status(
            control_id,
            metrics["validation"][1],
            metrics["oos"][1],
            actual_scores["validation"],
            actual_scores["oos"],
        )
        rows.append(
            {
                "model_id": model_id,
                "label_candidate_id": candidate_id,
                "contract_id": contract_id,
                "control_id": control_id,
                "control_family": "block_permutation(블록 순열)",
                "validation_rows": metrics["validation"][0],
                "oos_rows": metrics["oos"][0],
                "validation_control_balanced_accuracy": metrics["validation"][1],
                "oos_control_balanced_accuracy": metrics["oos"][1],
                "validation_actual_balanced_accuracy": actual_scores["validation"],
                "oos_actual_balanced_accuracy": actual_scores["oos"],
                "oos_control_minus_actual": metrics["oos"][1] - actual_scores["oos"],
                "control_status": status,
                "blocks_runtime_probe": str(blocks).lower(),
                "pass_condition": condition,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    shift_blocks = [row["control_id"] for row in rows if str(row["blocks_runtime_probe"]) == "true" and row["control_id"].startswith("label_shift")]
    rows.append(
        {
            "model_id": model_id,
            "label_candidate_id": candidate_id,
            "contract_id": contract_id,
            "control_id": "purged_adjacent_split_control",
            "control_family": "purged_boundary(제거 경계)",
            "validation_rows": len(split_indices["validation"]),
            "oos_rows": len(split_indices["oos"]),
            "validation_control_balanced_accuracy": "",
            "oos_control_balanced_accuracy": "",
            "validation_actual_balanced_accuracy": actual_scores["validation"],
            "oos_actual_balanced_accuracy": actual_scores["oos"],
            "oos_control_minus_actual": "",
            "control_status": "passed_shift_controls_clear" if not shift_blocks else "block_shift_controls_not_clear",
            "blocks_runtime_probe": str(bool(shift_blocks)).lower(),
            "pass_condition": "all shifted controls clear before MT5 probe(모든 이동 대조 통과 전 MT5 탐침 금지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def train_all() -> dict[str, Any]:
    df = read_source_frame()
    source_manifest = read_json(CANDIDATE_INPUT_MANIFEST)
    features = [str(item) for item in source_manifest.get("feature_columns", [])]
    if not features:
        raise RuntimeError("candidate_training_input_manifest.json has no feature_columns.")
    X = df.loc[:, features].to_numpy(dtype=np.float64, copy=False)
    nonfinite_rows = int((~np.isfinite(X).all(axis=1)).sum())
    if nonfinite_rows:
        raise RuntimeError(f"Model input has nonfinite rows: {nonfinite_rows}")

    label_map = label_arrays(read_parquet(CN_LABEL_FRAME), len(df))
    member_map = membership_arrays(read_parquet(CN_PURGED_MEMBERSHIP), len(df))
    shift_map = shift_arrays(read_parquet(CN_SHIFT_CONTROL_FRAME), len(df))
    seeds = block_seed_map(read_csv(CN_BLOCK_MANIFEST))
    task_rows = read_csv(CN_TASK_MATRIX)

    model_rows: list[dict[str, Any]] = []
    score_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, Any]] = []
    proxy_rows: list[dict[str, Any]] = []
    runtime_rows: list[dict[str, Any]] = []
    feature_hash = str(source_manifest.get("feature_order_hash", ""))
    io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    io_path(ONNX_DIR).mkdir(parents=True, exist_ok=True)

    for task in task_rows:
        candidate_id = task["label_candidate_id"]
        contract_id = task["contract_id"]
        model_family = task["model_family"]
        if model_family not in MODEL_FAMILIES:
            raise RuntimeError(f"Unexpected model family: {model_family}")
        y = label_map[candidate_id]
        split_values = member_map[contract_id]
        split_indices = {split: np.flatnonzero(split_values == split) for split in ("train", "validation", "oos")}
        model_id = f"{candidate_id}__{contract_id}__{model_family}"
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

        probabilities_by_split: dict[str, np.ndarray] = {}
        predictions_by_split: dict[str, np.ndarray] = {}
        for split in ("train", "validation", "oos"):
            idx = split_indices[split]
            probs = ordered_sklearn_probabilities(model, X[idx], class_order=LABEL_ORDER)
            probabilities_by_split[split] = probs
            predictions_by_split[split] = np.asarray(LABEL_ORDER, dtype=np.int64)[probs.argmax(axis=1)]
            score_rows.append(metric_row(model_id, candidate_id, contract_id, model_family, split, y[idx], probs))
        control_rows.extend(
            score_controls(
                model_id,
                candidate_id,
                contract_id,
                df,
                y,
                split_values,
                predictions_by_split,
                split_indices,
                shift_map,
                seeds,
            )
        )

        oos_idx = split_indices["oos"]
        oos_probs = probabilities_by_split["oos"]
        decisions = apply_threshold_rule(oos_probs, PRIMARY_RULE)
        for local_idx, source_row_id in enumerate(oos_idx):
            proxy_rows.append(
                {
                    "model_id": model_id,
                    "label_candidate_id": candidate_id,
                    "contract_id": contract_id,
                    "source_row_id": int(source_row_id),
                    "timestamp": str(df.loc[source_row_id, "timestamp"]),
                    "effective_split": "oos",
                    "true_label_class": int(y[source_row_id]),
                    "p_short": float(oos_probs[local_idx, 0]),
                    "p_flat": float(oos_probs[local_idx, 1]),
                    "p_long": float(oos_probs[local_idx, 2]),
                    "decision_label": str(decisions.loc[local_idx, "decision_label"]),
                    "decision_label_class": int(decisions.loc[local_idx, "decision_label_class"]),
                    "decision_probability": float(decisions.loc[local_idx, "decision_probability"]),
                    "decision_margin": float(decisions.loc[local_idx, "decision_margin"]),
                    "threshold_id": PRIMARY_RULE.threshold_id,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    control_by_model: dict[str, list[str]] = {}
    for row in control_rows:
        if str(row.get("blocks_runtime_probe")) == "true":
            control_by_model.setdefault(row["model_id"], []).append(row["control_id"])
    onnx_by_model = {row["model_id"]: row["onnx_path"] for row in model_rows}
    for row in model_rows:
        blocking = sorted(set(control_by_model.get(row["model_id"], [])))
        runtime_rows.append(
            {
                "model_id": row["model_id"],
                "label_candidate_id": row["label_candidate_id"],
                "contract_id": row["contract_id"],
                "onnx_path": onnx_by_model[row["model_id"]],
                "mt5_probe_disposition": "held_negative_control_review_required" if blocking else "review_ready_no_mt5_claim",
                "blocking_controls": ";".join(blocking),
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
    threshold_rows = [
        {
            "threshold_id": PRIMARY_RULE.threshold_id,
            "short_threshold": PRIMARY_RULE.short_threshold,
            "long_threshold": PRIMARY_RULE.long_threshold,
            "min_margin": PRIMARY_RULE.min_margin,
            "selection_use": "predeclared_primary_not_forward_selected(사전 선언, 전진 선택 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return {
        "model_rows": model_rows,
        "score_rows": score_rows,
        "parity_rows": parity_rows,
        "control_rows": control_rows,
        "proxy_rows": proxy_rows,
        "runtime_rows": runtime_rows,
        "compatibility_rows": compatibility_rows,
        "threshold_rows": threshold_rows,
        "feature_count": len(features),
        "source_rows": int(len(df)),
        "task_rows": len(task_rows),
    }


def build_gates(result: Mapping[str, Any]) -> list[dict[str, str]]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]
    cn_final = read_json(CN_FINAL)
    parity_passed = sum(1 for row in result["parity_rows"] if row["passed"] == "true")
    blocking_controls = [row for row in result["control_rows"] if str(row.get("blocks_runtime_probe")) == "true"]

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
        row("co_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CN materialized inputs(CN 물질화 입력)를 연결했다."),
        row("co_gate_parent_points_to_co", cn_final.get("next_action", "") == RUN_ID, cn_final.get("next_action", ""), RUN_ID, "CN next_action(다음 행동)과 CO run(실행)이 맞는다."),
        row("co_gate_task_rows", result["task_rows"] == 40, result["task_rows"], "40", "5 labels(라벨) x 4 purge contracts(제거 계약) x 2 model families(모델군)를 모두 학습 대상으로 삼았다."),
        row("co_gate_models_trained", len(result["model_rows"]) == 40, len(result["model_rows"]), "40", "purged guarded models(제거 방어 모델)를 모두 만들었다."),
        row("co_gate_scorecards", len(result["score_rows"]) == 120, len(result["score_rows"]), "models*3 splits", "train/validation/OOS(학습/검증/실외표본) 성과를 모두 기록했다."),
        row("co_gate_onnx_parity", parity_passed == len(result["parity_rows"]) and parity_passed == 40, f"{parity_passed}/{len(result['parity_rows'])}", "40/40", "Python(파이썬)과 ONNX(온엑스) 확률 출력을 맞췄다."),
        row("co_gate_nonoverlap_controls", len(result["control_rows"]) == 200, len(result["control_rows"]), "models*5 controls", "shift/block/purged controls(이동/블록/제거 대조)를 모두 기록했다."),
        row("co_gate_control_risk_recorded", all(row.get("model_id") and row.get("control_id") for row in blocking_controls), len(blocking_controls), "blocking rows named if present", "대조 위험을 숨기지 않고 review(검토) 입력으로 넘긴다."),
        row("co_gate_runtime_disposition", len(result["runtime_rows"]) == 40, len(result["runtime_rows"]), "40", "MT5 probe(MT5 탐침) 여부를 모델별로 보류/검토로 나눴다."),
        row("co_gate_no_selection_or_mt5", True, "selection=not_run;mt5=not_run;threshold_tuning=not_run", "no selection/MT5/tuning", "CO는 학습과 대조 기록만 수행한다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    model_receipt = {
        "model_family": "logreg_balanced_c075 and extratrees_depth6_leaf160(로지스틱/엑스트라트리)",
        "target_and_label": "CN candidate labels(CN 후보 라벨) under purged memberships(제거 소속)",
        "split_method": "purged/embargo train-validation-OOS(제거/격리 학습-검증-실외표본)",
        "selection_metric": "not_applicable_all_tasks_trained_no_selection(해당 없음, 전 작업 학습, 선택 없음)",
        "secondary_metrics": "balanced accuracy(균형 정확도), macro F1(매크로 F1), signal density(신호 밀도), non-overlap controls(비중첩 대조), ONNX parity(온엑스 동등성)",
        "threshold_policy": "fixed_short040_long040_margin002 unchanged(고정 임계값, 변경 없음)",
        "overfit_risk": "using purge gap or control result as model selector(제거 간격이나 대조 결과를 모델 선택자로 쓰는 위험)",
        "calibration_risk": "scores are ranking diagnostics, not calibrated probabilities(점수는 순위 진단이지 보정 확률 아님)",
        "comparison_baseline": "CK unpurged guarded training and CL shifted-control risk(CK 미제거 학습과 CL 이동 대조 위험)",
        "validation_judgment": "exploratory_control_review_required(탐색, 대조 검토 필요)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "timestamp(시각) and source_row_id(원천 행 ID) from CN; no new forward data(새 전진 데이터 없음)",
        "sample_scope": "existing train/validation/OOS through 2026-04-13(기존 학습/검증/실외표본)",
        "missing_or_duplicate_check": "finite feature matrix checked; generated views repeat source_row_id by task(피처 유한성 확인, 생성 보기는 작업별 반복 정상)",
        "feature_label_boundary": "CN labels and split-local controls reused without relabeling(CN 라벨과 분할 내부 대조 재사용, 재라벨 없음)",
        "split_boundary": "effective_split from purged membership(제거 소속의 유효 분할)",
        "leakage_risk": "choosing a winner from OOS/control pocket(OOS/대조 포켓으로 승자 선택하는 위험)",
        "data_hash_or_identity": {"source_sha256": final["source_sha256"], "source_rows": final["source_rows"]},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime_receipt = {
        "runtime_subject": "ONNX export and runtime disposition only(온엑스 내보내기와 런타임 처분만)",
        "parity_check": f"onnxruntime parity rows={final['onnx_parity_passed']}/{final['onnx_parity_rows']}",
        "mt5_runtime_probe": "not_run",
        "usable_for": "CP review(CP 검토) and possible future MT5 package only",
        "not_usable_for": "runtime authority(런타임 권위), Forward Passed(전진 통과), live readiness(실거래 준비)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "trained models(학습 모델), ONNX parity(온엑스 동등성), scorecards(점수표), non-overlap controls(비중첩 대조), runtime disposition(런타임 처분)",
        "evidence_missing": "CP review(CP 검토), MT5 runtime probe(MT5 런타임 탐침), forward decision(전진 판정)",
        "judgment_label": "exploratory(탐색)",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "모델은 만들었지만 대조가 통과했는지 리뷰하기 전에는 운영이나 전진 판정을 말하지 않는다.",
    }
    receipt_paths = [
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(DATA_RECEIPT, data_receipt),
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
        "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipt_paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return receipt_paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CO Purged Guarded Training(제거 방어 학습)

## Conclusion(결론)

run337CO(337CO 실행)는 CN materialized inputs(CN 물질화 입력)으로 `40`개 diagnostic model(진단 모델)을 학습하고 sklearn/ONNX(사이킷런/온엑스) parity(동등성), scorecard(점수표), non-overlap control(비중첩 대조), runtime disposition(런타임 처분)을 만들었다.

Effect(효과): 다음 run337CP(337CP 실행)는 성과가 좋은 모델을 고르는 단계가 아니라 control clearance(대조 통과)와 blocking reason(차단 이유)을 검토하는 단계다. Forward/Goal/runtime authority(전진/목표/런타임 권위)는 주장하지 않는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- trained_models(학습 모델): `{final["trained_models"]}`
- scorecard_rows(점수표 행): `{final["scorecard_rows"]}`
- onnx_parity(온엑스 동등성): `{final["onnx_parity_passed"]}/{final["onnx_parity_rows"]}`
- nonoverlap_control_rows(비중첩 대조 행): `{final["control_rows"]}`
- blocking_control_rows(차단 대조 행): `{final["blocking_control_rows"]}`
- runtime_held_rows(런타임 보류 행): `{final["runtime_held_rows"]}`
- proxy_expected_rows(프록시 예상 행): `{final["proxy_expected_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- model_training(모델 학습): `diagnostic_run`
- candidate_selection(후보 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CO

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): purged guarded training(제거 방어 학습)과 non-overlap controls(비중첩 대조)를 만들고 CP review(CP 검토)를 열었다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(CONTROL_SCORECARD)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{final["passed_gates"]}/{final["gate_rows"]}`
- runtime_held_rows(런타임 보류 행): `{final["runtime_held_rows"]}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs() -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337CO focus complete: purged guarded training(제거 방어 학습)을 `{STATUS}`로 닫았다. "
        "Effect(효과): run337CP(337CP 실행)에서 non-overlap controls(비중첩 대조)와 runtime disposition(런타임 처분)을 검토한다."
    )
    if "Stage337 run337CO focus complete" in workspace_text:
        workspace_text = re.sub(
            r"current_focus:\n- >-\n  Stage337 run337CO focus complete:.*?(?=\n- >-\n  Stage337 run337CN|\n[A-Za-z0-9_]+:)",
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
## Stage337 run337CO(337CO 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): purged guarded training(제거 방어 학습), ONNX parity(온엑스 동등성), non-overlap controls(비중첩 대조), runtime disposition(런타임 처분)을 만들었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current_text = re.sub(
        r"\n## Stage337 run337CO\(337CO 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CN|\Z)",
        "\n",
        current_text,
        count=1,
        flags=re.DOTALL,
    )
    marker = "## Stage337 run337CN(337CN"
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
- actual_mt5_execution(실제 MT5 실행): `not_run_co_control_review_required`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 purged guarded training control review(제거 방어 학습 대조 검토)다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337CO(337CO 실행)" not in line)
    stage_entry = (
        f"- {TODAY}: run337CO(337CO 실행) trained purged guarded candidates(제거 방어 후보). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text.rstrip() + "\n" + stage_entry + "\n", stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(line for line in changelog_text.splitlines() if "Stage337 run337CO trained purged guarded candidates" not in line)
    changelog_entry = f"- {TODAY}: Stage337 run337CO trained purged guarded candidates(제거 방어 후보) and opened `{NEXT_RUN_ID}`."
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text.rstrip() + "\n" + changelog_entry + "\n", changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "purged_serial_dependence_guarded_training_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"models={final['trained_models']};onnx_parity={final['onnx_parity_passed']}/{final['onnx_parity_rows']};blocking_controls={final['blocking_control_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_data_integrity_runtime_parity_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__purged_guarded_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "purged_guarded_training",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "purged_guarded_training",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "training_and_control_diagnostics_no_selection",
        "scoreboard_lane": "model_validation_control_diagnostics",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"models={final['trained_models']};control_rows={final['control_rows']};runtime_held={final['runtime_held_rows']}",
        "guardrail_kpi": "onnx_parity;nonoverlap_controls;no_selection;no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__purged_guarded_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_data_integrity_runtime_parity_artifact_lineage",
        "evidence_scope": "CN repair inputs trained under purged memberships",
        "kpi_scope": "training_and_control_diagnostics_no_selection",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};runtime_held_rows={final['runtime_held_rows']};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__purged_guarded_training",
        "family": "model_validation_data_integrity_runtime_parity_artifact_lineage",
        "question": "do purged serial-dependence guarded candidates survive non-overlap controls",
        "metric_scope": "model_scorecard_onnx_parity_nonoverlap_controls",
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
    io_path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    io_path(ONNX_DIR).mkdir(parents=True, exist_ok=True)
    result = train_all()
    blocking_control_rows = [row for row in result["control_rows"] if str(row.get("blocks_runtime_probe")) == "true"]
    runtime_held_rows = [row for row in result["runtime_rows"] if row["mt5_probe_disposition"] == "held_negative_control_review_required"]
    parity_passed = sum(1 for row in result["parity_rows"] if row["passed"] == "true")
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "trained_models": len(result["model_rows"]),
        "scorecard_rows": len(result["score_rows"]),
        "onnx_parity_rows": len(result["parity_rows"]),
        "onnx_parity_passed": parity_passed,
        "control_rows": len(result["control_rows"]),
        "blocking_control_rows": len(blocking_control_rows),
        "blocking_control_ids": sorted({row["control_id"] for row in blocking_control_rows}),
        "proxy_expected_rows": len(result["proxy_rows"]),
        "runtime_disposition_rows": len(result["runtime_rows"]),
        "runtime_held_rows": len(runtime_held_rows),
        "task_rows": result["task_rows"],
        "source_rows": result["source_rows"],
        "source_sha256": sha256_file(SOURCE_MODEL_INPUT),
        "model_training": "diagnostic_run",
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
    gates = build_gates(result)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]

    artifacts: list[Path] = [
        write_csv(TRAINED_MODEL_MANIFEST, MODEL_COLUMNS, result["model_rows"]),
        write_csv(MODEL_SCORECARD, SCORE_COLUMNS, result["score_rows"]),
        write_csv(ONNX_PARITY, PARITY_COLUMNS, result["parity_rows"]),
        write_csv(CONTROL_SCORECARD, CONTROL_COLUMNS, result["control_rows"]),
        write_csv(PROXY_EXPECTED, PROXY_COLUMNS, result["proxy_rows"]),
        write_csv(RUNTIME_DISPOSITION, RUNTIME_COLUMNS, result["runtime_rows"]),
        write_csv(THRESHOLD_POLICY, THRESHOLD_COLUMNS, result["threshold_rows"]),
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
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs())
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
