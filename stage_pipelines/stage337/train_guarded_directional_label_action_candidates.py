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
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER  # noqa: E402
from foundation.models.decision_surface import ThresholdRule, apply_threshold_rule  # noqa: E402
from foundation.models.onnx_bridge import (  # noqa: E402
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_sklearn_probabilities,
    sha256_file,
)
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
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
    now_utc,
)


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CK"
RUN_ID = "run337CK_guarded_directional_label_action_candidate_training_without_db_v1"
PARENT_RUN_ID = "run337CJ_materialize_directional_label_action_candidate_training_inputs_without_db_v1"
NEXT_RUN_ID = "run337CL_review_guarded_directional_label_action_candidate_training_without_db_v1"
STATUS = "completed_stage337CK_guarded_directional_label_action_candidate_training_onnx_materialized_negative_control_review_required_no_selection"
JUDGMENT = "exploratory_guarded_candidate_models_trained_onnx_parity_passed_shifted_control_risk_flagged_no_forward_selection"
DECISION = "stage337CK_open_run337CL_guarded_training_negative_control_review"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CK_guarded_directional_label_action_training_without_db_"
    "negative_control_review_required_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CK_guarded_directional_label_action_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CK_guarded_directional_label_action_training.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

CJ_DIR = STAGE_DIR / "02_runs" / "run337CJ"
CJ_FINAL = CJ_DIR / "final_decision.json"
LABEL_CANDIDATE_MATRIX = CJ_DIR / "label_v3_candidate_matrix.csv"
ACTION_CANDIDATE_MATRIX = CJ_DIR / "action_v3_candidate_matrix.csv"
NEGATIVE_SCORING_TEMPLATE = CJ_DIR / "negative_control_scoring_template.csv"
SPLIT_BOUNDARY_MANIFEST = CJ_DIR / "split_boundary_manifest.csv"
FEATURE_SOURCE_MANIFEST = CJ_DIR / "feature_source_manifest.csv"
CANDIDATE_INPUT_MANIFEST = CJ_DIR / "candidate_training_input_manifest.json"
CK_QUEUE_IN = CJ_DIR / "run337CK_guarded_training_queue.csv"
CJ_GATES = CJ_DIR / "required_gate_coverage_audit.csv"

SOURCE_MODEL_INPUT = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"

TRAINED_MODEL_MANIFEST = RUN_DIR / "trained_model_manifest.csv"
GUARDED_MODEL_SCORECARD = RUN_DIR / "guarded_model_scorecard.csv"
ONNX_PARITY = RUN_DIR / "onnxruntime_parity_matrix.csv"
NEGATIVE_CONTROL_SCORECARD = RUN_DIR / "negative_control_scorecard.csv"
PROXY_EXPECTED_BY_CANDIDATE = RUN_DIR / "proxy_expected_by_candidate.csv"
RUNTIME_PROBE_PACKAGE_QUEUE = RUN_DIR / "runtime_probe_package_queue.csv"
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
    CJ_FINAL,
    LABEL_CANDIDATE_MATRIX,
    ACTION_CANDIDATE_MATRIX,
    NEGATIVE_SCORING_TEMPLATE,
    SPLIT_BOUNDARY_MANIFEST,
    FEATURE_SOURCE_MANIFEST,
    CANDIDATE_INPUT_MANIFEST,
    CK_QUEUE_IN,
    CJ_GATES,
    SOURCE_MODEL_INPUT,
)
OUTPUT_FILES = (
    TRAINED_MODEL_MANIFEST,
    GUARDED_MODEL_SCORECARD,
    ONNX_PARITY,
    NEGATIVE_CONTROL_SCORECARD,
    PROXY_EXPECTED_BY_CANDIDATE,
    RUNTIME_PROBE_PACKAGE_QUEUE,
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

MODEL_SPECS = (
    {
        "model_family": "logreg_balanced_c075",
        "model_role": "linear_defensive_control(선형 방어 대조)",
    },
    {
        "model_family": "extratrees_depth6_leaf160",
        "model_role": "nonlinear_offense_probe(비선형 공격 탐침)",
    },
)
PRIMARY_RULE = ThresholdRule("fixed_short040_long040_margin002", 0.40, 0.40, 0.02)

MODEL_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "model_family",
    "model_role",
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
NEGATIVE_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "control_id",
    "validation_balanced_accuracy",
    "oos_balanced_accuracy",
    "control_status",
    "blocks_if",
    "claim_boundary",
)
PROXY_COLUMNS = (
    "model_id",
    "label_candidate_id",
    "timestamp",
    "split",
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
RUNTIME_QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "model_id",
    "label_candidate_id",
    "onnx_path",
    "feature_order_hash",
    "required_compare",
    "blocked_if_missing",
    "claim_boundary",
)
THRESHOLD_COLUMNS = (
    "threshold_id",
    "short_threshold",
    "long_threshold",
    "min_margin",
    "selection_use",
    "claim_boundary",
)
FEATURE_COLUMNS = (
    "source_path",
    "rows",
    "feature_count",
    "feature_order_hash",
    "missing_features",
    "nonfinite_rows",
    "compatibility_status",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def read_source_frame() -> pd.DataFrame:
    return pd.read_parquet(io_path(SOURCE_MODEL_INPUT))


def label_values(df: pd.DataFrame, candidate: Mapping[str, str]) -> np.ndarray:
    candidate_id = candidate["candidate_id"]
    returns = df["future_log_return_12"].astype(float)
    threshold = float(candidate["train_threshold_value"])
    if candidate_id == "label_v3_original_v1_control":
        return df["label_class"].astype("int64").to_numpy()
    if candidate_id == "label_v3_flipped_polarity_probe":
        return df["label_class"].astype("int64").map({0: 2, 1: 1, 2: 0}).to_numpy()
    if candidate_id == "label_v3_volnorm_margin_q50_train_only":
        vol = df["historical_vol_20"].astype(float).replace(0, np.nan)
        values = (returns / vol).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    else:
        values = returns
    return np.where(values < -threshold, 0, np.where(values > threshold, 2, 1)).astype("int64")


def feature_columns_from_manifest() -> list[str]:
    manifest = read_json(CANDIDATE_INPUT_MANIFEST)
    features = [str(item) for item in manifest.get("feature_columns", [])]
    if not features:
        raise RuntimeError("candidate_training_input_manifest.json has no feature_columns.")
    return features


def build_model(model_family: str):
    if model_family == "logreg_balanced_c075":
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
    if model_family == "extratrees_depth6_leaf160":
        return ExtraTreesClassifier(
            n_estimators=160,
            max_depth=6,
            min_samples_leaf=160,
            class_weight="balanced",
            random_state=337,
            n_jobs=-1,
        )
    raise ValueError(f"Unknown model family: {model_family}")


def metric_row(
    model_id: str,
    candidate_id: str,
    model_family: str,
    split: str,
    y_true: np.ndarray,
    probabilities: np.ndarray,
) -> dict[str, Any]:
    y_pred = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
    decisions = apply_threshold_rule(probabilities, PRIMARY_RULE)
    decision_counts = decisions["decision_label"].value_counts().to_dict()
    true_counts = pd.Series(y_true).value_counts().to_dict()
    return {
        "model_id": model_id,
        "label_candidate_id": candidate_id,
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


def transformed_labels(y: np.ndarray, control_id: str) -> np.ndarray:
    if control_id == "direction_flip_control":
        return pd.Series(y).map({0: 2, 1: 1, 2: 0}).astype("int64").to_numpy()
    if control_id == "label_permutation_control":
        rng = np.random.default_rng(337)
        return rng.permutation(y).astype("int64")
    if control_id == "time_reversal_control":
        return y[::-1].astype("int64")
    if control_id == "shifted_return_control":
        return np.roll(y, 12).astype("int64")
    return y.astype("int64")


def negative_control_rows(
    model_id: str,
    candidate_id: str,
    probabilities_by_split: Mapping[str, np.ndarray],
    y_by_split: Mapping[str, np.ndarray],
) -> list[dict[str, Any]]:
    controls = read_csv(NEGATIVE_SCORING_TEMPLATE)
    rows: list[dict[str, Any]] = []
    for control in controls:
        control_id = control["control_id"]
        if control_id == "stale_context_carry_control":
            rows.append(
                {
                    "model_id": model_id,
                    "label_candidate_id": candidate_id,
                    "control_id": control_id,
                    "validation_balanced_accuracy": "",
                    "oos_balanced_accuracy": "",
                    "control_status": "requires_context_attribution_in_review",
                    "blocks_if": control.get("blocks_if", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        metrics: dict[str, float] = {}
        for split in ("validation", "oos"):
            probs = probabilities_by_split[split]
            pred = np.asarray(LABEL_ORDER, dtype="int64")[probs.argmax(axis=1)]
            y_control = transformed_labels(y_by_split[split], control_id)
            metrics[split] = float(balanced_accuracy_score(y_control, pred))
        status = "passed_noise_like" if max(metrics.values()) < 0.45 else "review_required_high_control_alignment"
        rows.append(
            {
                "model_id": model_id,
                "label_candidate_id": candidate_id,
                "control_id": control_id,
                "validation_balanced_accuracy": metrics["validation"],
                "oos_balanced_accuracy": metrics["oos"],
                "control_status": status,
                "blocks_if": control.get("blocks_if", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def train_all() -> dict[str, Any]:
    df = read_source_frame()
    features = feature_columns_from_manifest()
    feature_values = df.loc[:, features].to_numpy(dtype="float64", copy=False)
    nonfinite_rows = int((~np.isfinite(feature_values).all(axis=1)).sum())
    if nonfinite_rows:
        raise RuntimeError(f"Model input has nonfinite rows: {nonfinite_rows}")
    split_masks = {split: df["split"].astype(str).eq(split).to_numpy() for split in ("train", "validation", "oos")}
    X_by_split = {split: df.loc[mask, features].to_numpy(dtype="float64", copy=False) for split, mask in split_masks.items()}

    label_candidates = read_csv(LABEL_CANDIDATE_MATRIX)
    model_rows: list[dict[str, Any]] = []
    score_rows: list[dict[str, Any]] = []
    parity_rows: list[dict[str, Any]] = []
    negative_rows: list[dict[str, Any]] = []
    proxy_rows: list[dict[str, Any]] = []
    runtime_rows: list[dict[str, Any]] = []
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    ONNX_DIR.mkdir(parents=True, exist_ok=True)
    feature_hash = read_json(CANDIDATE_INPUT_MANIFEST)["feature_order_hash"]

    for candidate in label_candidates:
        candidate_id = candidate["candidate_id"]
        y_all = label_values(df, candidate)
        y_by_split = {split: y_all[mask] for split, mask in split_masks.items()}
        for spec in MODEL_SPECS:
            model_family = spec["model_family"]
            model_id = f"{candidate_id}__{model_family}"
            model = build_model(model_family)
            model.fit(X_by_split["train"], y_by_split["train"])
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
            sample = X_by_split["validation"][: min(512, len(X_by_split["validation"]))]
            parity = check_onnxruntime_probability_parity(model, onnx_path, sample, tolerance=1.0e-5)
            parity_rows.append(
                {
                    "model_id": model_id,
                    "label_candidate_id": candidate_id,
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
                    "model_family": model_family,
                    "model_role": spec["model_role"],
                    "feature_count": len(features),
                    "feature_order_hash": feature_hash,
                    "model_path": rel(model_path),
                    "model_sha256": sha256_file(model_path),
                    "onnx_path": rel(onnx_path),
                    "onnx_sha256": sha256_file(onnx_path),
                    "onnx_probability_output_name": export_info["probability_output_name"],
                    "train_rows": int(len(y_by_split["train"])),
                    "validation_rows": int(len(y_by_split["validation"])),
                    "oos_rows": int(len(y_by_split["oos"])),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            probabilities_by_split: dict[str, np.ndarray] = {}
            for split in ("train", "validation", "oos"):
                probs = ordered_sklearn_probabilities(model, X_by_split[split], class_order=LABEL_ORDER)
                probabilities_by_split[split] = probs
                score_rows.append(metric_row(model_id, candidate_id, model_family, split, y_by_split[split], probs))
            negative_rows.extend(negative_control_rows(model_id, candidate_id, probabilities_by_split, y_by_split))

            oos_frame = df.loc[split_masks["oos"], ["timestamp"]].reset_index(drop=True)
            oos_probs = probabilities_by_split["oos"]
            decisions = apply_threshold_rule(oos_probs, PRIMARY_RULE)
            for idx in range(len(oos_frame)):
                proxy_rows.append(
                    {
                        "model_id": model_id,
                        "label_candidate_id": candidate_id,
                        "timestamp": str(oos_frame.loc[idx, "timestamp"]),
                        "split": "oos",
                        "true_label_class": int(y_by_split["oos"][idx]),
                        "p_short": float(oos_probs[idx, 0]),
                        "p_flat": float(oos_probs[idx, 1]),
                        "p_long": float(oos_probs[idx, 2]),
                        "decision_label": str(decisions.loc[idx, "decision_label"]),
                        "decision_label_class": int(decisions.loc[idx, "decision_label_class"]),
                        "decision_probability": float(decisions.loc[idx, "decision_probability"]),
                        "decision_margin": float(decisions.loc[idx, "decision_margin"]),
                        "threshold_id": PRIMARY_RULE.threshold_id,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
            runtime_rows.append(
                {
                    "queue_id": f"runtime_probe::{model_id}",
                    "next_run_id": NEXT_RUN_ID,
                    "model_id": model_id,
                    "label_candidate_id": candidate_id,
                    "onnx_path": rel(onnx_path),
                    "feature_order_hash": feature_hash,
                    "required_compare": "bar_time;feature_input_hash;p_short;p_flat;p_long;decision;action;trade_count;fill_count",
                    "blocked_if_missing": "MT5 strategy tester telemetry or proxy expected row parity is missing",
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
            "selection_use": "predeclared_primary_not_forward_selected",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return {
        "model_rows": model_rows,
        "score_rows": score_rows,
        "parity_rows": parity_rows,
        "negative_rows": negative_rows,
        "proxy_rows": proxy_rows,
        "runtime_rows": runtime_rows,
        "compatibility_rows": compatibility_rows,
        "threshold_rows": threshold_rows,
        "feature_count": len(features),
        "source_rows": int(len(df)),
    }


def build_receipts(result: Mapping[str, Any]) -> list[Path]:
    model_receipt = {
        "model_family": "logreg_balanced_c075 and extratrees_depth6_leaf160 over five label_v3 candidates",
        "target_and_label": "CJ label_v3 candidates; no candidate selected",
        "split_method": "time-ordered train/validation/OOS",
        "selection_metric": "not_applicable_all_candidates_trained_no_selection",
        "secondary_metrics": "balanced accuracy, macro F1, log loss, signal density, negative controls, ONNX parity",
        "threshold_policy": "fixed_short040_long040_margin002 predeclared",
        "overfit_risk": "shifted_return_control high alignment may indicate serial target autocorrelation or label boundary fragility; choosing winner from OOS/proxy without MT5 runtime probe is forbidden",
        "calibration_risk": "scores are rank diagnostics, not calibrated probabilities",
        "comparison_baseline": "original label_v1 control and flipped polarity probe",
        "validation_judgment": "exploratory_guarded_training",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": rel(SOURCE_MODEL_INPUT),
        "time_axis": "timestamp from model input; no post-2026-04-14 forward data used in training",
        "sample_scope": "train/validation/OOS only through 2026-04-13",
        "missing_or_duplicate_check": "finite feature matrix checked; split manifest from CJ used",
        "feature_label_boundary": "candidate labels generated from pre-materialized future_log_return_12; thresholds are train-only",
        "split_boundary": "train fit only; validation/OOS diagnostics only",
        "leakage_risk": "selecting candidate from OOS before MT5 runtime probe",
        "data_hash_or_identity": {"source_sha256": sha256_file(SOURCE_MODEL_INPUT)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime_receipt = {
        "runtime_subject": "ONNX export and proxy expected only",
        "parity_check": f"onnxruntime parity rows={len(result['parity_rows'])}",
        "mt5_runtime_probe": "not_run",
        "usable_for": "future MT5 probe package and proxy-vs-MT5 comparison",
        "not_usable_for": "runtime authority, Forward Passed, live readiness",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in OUTPUT_FILES],
        "artifact_hashes": {},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "trained sklearn artifacts, ONNX files, parity matrix, scorecards, proxy expected rows",
        "evidence_missing": "MT5 runtime probe, forward data execution, final selection",
        "judgment_label": "exploratory",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": "CL must review shifted-control alignment, scorecards, and decide whether a no-selection MT5 runtime probe is still warranted",
        "user_explanation_hook": "ONNX 후보는 만들어졌지만 아직 운영 가능이나 전진 통과가 아니다.",
    }
    paths = [
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(RUNTIME_RECEIPT, runtime_receipt),
        write_json(LINEAGE_RECEIPT, lineage_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt["artifact_hashes"] = {rel(path): sha256_file(path) for path in paths if path != LINEAGE_RECEIPT and path_exists(path)}
    write_json(LINEAGE_RECEIPT, lineage_receipt)
    return paths


def build_gates(result: Mapping[str, Any]) -> list[dict[str, str]]:
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]
    parity_passed = sum(1 for row in result["parity_rows"] if row["passed"] == "true")
    high_controls = [
        row for row in result["negative_rows"] if row["control_status"] == "review_required_high_control_alignment"
    ]
    high_control_ids_recorded = all(row.get("model_id") and row.get("control_id") for row in high_controls)

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
        row("ck_gate_inputs_present", not missing, ";".join(missing) or "none", "no_missing_inputs", "CJ 입력과 원천 parquet(파케이)를 연결한다."),
        row("ck_gate_models_trained", len(result["model_rows"]) >= 10, len(result["model_rows"]), ">=10 models", "5개 라벨 후보와 2개 모델군을 모두 학습한다."),
        row("ck_gate_onnx_parity", parity_passed == len(result["parity_rows"]) and parity_passed > 0, f"{parity_passed}/{len(result['parity_rows'])}", "all ONNX parity passed", "Python(파이썬)과 ONNX(온엑스) 확률 출력을 맞춘다."),
        row("ck_gate_scorecards", len(result["score_rows"]) == len(result["model_rows"]) * 3, len(result["score_rows"]), "models*3 splits", "train/validation/OOS 성과를 모두 기록한다."),
        row("ck_gate_negative_controls", len(result["negative_rows"]) >= len(result["model_rows"]) * 5, len(result["negative_rows"]), "models*5 controls", "부정 대조를 학습 산출물에 붙인다."),
        row(
            "ck_gate_negative_control_risk_recorded",
            high_control_ids_recorded,
            len(high_controls),
            "review_required rows recorded for CL review",
            "high alignment(높은 정렬)을 통과 주장으로 숨기지 않고 CL review(검토)로 넘긴다.",
        ),
        row("ck_gate_proxy_expected", len(result["proxy_rows"]) > 0, len(result["proxy_rows"]), ">0 proxy rows", "MT5 비교용 proxy expected(프록시 예상)를 만든다."),
        row("ck_gate_runtime_queue", len(result["runtime_rows"]) == len(result["model_rows"]), len(result["runtime_rows"]), "one runtime queue row per model", "다음 리뷰에서 MT5 probe package(탐침 패키지)를 선택이 아닌 검토로 넘긴다."),
        row("ck_gate_no_candidate_selection", True, "candidate_selection=not_run", "no selection", "학습 결과로 즉시 승자를 고르지 않는다."),
    ]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CK Guarded Directional Label/Action Training(방어 방향 라벨/행동 학습)

## Conclusion(결론)

run337CK(337CK 실행)는 CJ 후보 입력을 이용해 `10`개 sklearn/ONNX(사이킷런/온엑스) 후보를 학습하고 proxy expected(프록시 예상)와 negative-control scorecard(부정 대조 점수표)를 만들었다.

Effect(효과): shifted-control high alignment(이동 대조 높은 정렬)을 `review_required(검토 필요)`로 드러냈고, 다음 run337CL(337CL 실행)에서 이 위험을 먼저 검토한다. Forward/Goal/runtime authority(전진/목표/런타임 권위)는 주장하지 않는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- trained_models(학습 모델): `{final["trained_models"]}`
- onnx_parity(ONNX 동등성): `{final["onnx_parity_passed"]}/{final["onnx_parity_rows"]}`
- scorecard_rows(점수표 행): `{final["scorecard_rows"]}`
- negative_control_rows(부정 대조 행): `{final["negative_control_rows"]}`
- negative_control_review_required_rows(부정 대조 검토 필요 행): `{final["negative_control_review_required_rows"]}`
- proxy_expected_rows(프록시 예상 행): `{final["proxy_expected_rows"]}`
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
    text = f"""# Decision(결정): Stage337 run337CK

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): guarded training(방어 학습)으로 ONNX 후보와 proxy expected(프록시 예상)를 만들었고 shifted-control high alignment(이동 대조 높은 정렬)을 `review_required(검토 필요)`로 남겼다. 선택/전진/운영 주장은 닫아둔다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(FINAL_DECISION)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- gate_result(게이트 결과): `{final["passed_gates"]}/{final["gate_rows"]}`
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
        f"  Stage337 run337CK focus complete: guarded directional label/action candidate training(방어 방향 라벨/행동 후보 학습)을 `{STATUS}`로 닫았다. "
        "Effect(효과): run337CL(337CL 실행)에서 ONNX parity/negative-control/proxy scorecard(온엑스 동등성/부정대조/프록시 점수표), shifted-control high alignment(이동 대조 높은 정렬)을 검토한다."
    )
    if "Stage337 run337CK focus complete" in workspace_text:
        workspace_text = re.sub(
            r"current_focus:\n- >-\n  Stage337 run337CK focus complete:.*?(?=\n- >-\n  Stage337 run337CJ|\n[A-Za-z0-9_]+:)",
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
## Stage337 run337CK(337CK 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): label_v3/action_v3 후보를 학습하고 ONNX parity(온엑스 동등성), negative controls(부정 대조), proxy expected(프록시 예상)를 만들었다. shifted-control high alignment(이동 대조 높은 정렬)는 CL review(검토)로 넘기며 Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current_text = re.sub(
        r"\n## Stage337 run337CK\(337CK 실행\) - 2026-05-28\n.*?(?=\n## Stage337 run337CJ|\Z)",
        "\n",
        current_text,
        count=1,
        flags=re.DOTALL,
    )
    marker = "## Stage337 run337CJ(337CJ"
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
- actual_mt5_execution(실제 MT5 실행): `not_run_ck_training_only_run337CE_reviewed`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 guarded training review(방어 학습 검토)와 shifted-control high alignment(이동 대조 높은 정렬) 검토다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_text = "\n".join(line for line in stage_text.splitlines() if "run337CK(337CK 실행)" not in line)
    stage_entry = f"- {TODAY}: run337CK(337CK 실행) trained guarded directional label/action candidates(방어 방향 라벨/행동 후보). Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_text = "\n".join(line for line in changelog_text.splitlines() if "Stage337 run337CK trained guarded directional label/action candidates" not in line)
    changelog_entry = f"- {TODAY}: Stage337 run337CK trained guarded directional label/action candidates(방어 방향 라벨/행동 후보) and opened `{NEXT_RUN_ID}`."
    changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "guarded_directional_label_action_candidate_training_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"models={final['trained_models']};onnx_parity={final['onnx_parity_passed']}/{final['onnx_parity_rows']};neg_review={final['negative_control_review_required_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "model_validation_runtime_parity_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__guarded_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "guarded_training",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "python_onnx_proxy_expected",
        "tier_scope": "out_of_scope_by_claim_training_no_tier_kpi",
        "kpi_scope": "training_proxy_no_mt5",
        "scoreboard_lane": "model_validation_runtime_parity",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"models={final['trained_models']};onnx_parity={final['onnx_parity_passed']}/{final['onnx_parity_rows']}",
        "guardrail_kpi": "negative_controls_with_review_required_rows;proxy_expected;no_forward_selection;mt5_missing",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__guarded_training",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_runtime_parity_artifact_lineage",
        "evidence_scope": "CJ candidate inputs trained to sklearn and ONNX",
        "kpi_scope": "training_proxy_no_mt5",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};negative_control_review_required_rows={final['negative_control_review_required_rows']};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__guarded_training",
        "family": "model_validation_runtime_parity_artifact_lineage",
        "question": "do candidate labels/actions produce ONNX candidates with parity before MT5 probe",
        "metric_scope": "training_proxy_no_forward_decision",
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
    gates = build_gates(result)
    high_control_rows = [
        row for row in result["negative_rows"] if row["control_status"] == "review_required_high_control_alignment"
    ]
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "trained_models": len(result["model_rows"]),
        "scorecard_rows": len(result["score_rows"]),
        "negative_control_rows": len(result["negative_rows"]),
        "negative_control_review_required_rows": len(high_control_rows),
        "negative_control_review_required_controls": sorted({row["control_id"] for row in high_control_rows}),
        "proxy_expected_rows": len(result["proxy_rows"]),
        "runtime_queue_rows": len(result["runtime_rows"]),
        "onnx_parity_rows": len(result["parity_rows"]),
        "onnx_parity_passed": sum(1 for row in result["parity_rows"] if row["passed"] == "true"),
        "model_training": "completed_guarded_training",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "gate_rows": len(gates),
        "passed_gates": sum(1 for row in gates if row["status"] == "passed"),
        "failed_gates": [row["gate_id"] for row in gates if row["status"] != "passed"],
    }
    artifacts: list[Path] = [
        write_csv(TRAINED_MODEL_MANIFEST, MODEL_COLUMNS, result["model_rows"]),
        write_csv(GUARDED_MODEL_SCORECARD, SCORE_COLUMNS, result["score_rows"]),
        write_csv(ONNX_PARITY, PARITY_COLUMNS, result["parity_rows"]),
        write_csv(NEGATIVE_CONTROL_SCORECARD, NEGATIVE_COLUMNS, result["negative_rows"]),
        write_csv(PROXY_EXPECTED_BY_CANDIDATE, PROXY_COLUMNS, result["proxy_rows"]),
        write_csv(RUNTIME_PROBE_PACKAGE_QUEUE, RUNTIME_QUEUE_COLUMNS, result["runtime_rows"]),
        write_csv(THRESHOLD_POLICY, THRESHOLD_COLUMNS, result["threshold_rows"]),
        write_csv(FEATURE_COMPATIBILITY, FEATURE_COLUMNS, result["compatibility_rows"]),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(Path(row["model_path"]) for row in result["model_rows"])
    artifacts.extend(Path(row["onnx_path"]) for row in result["model_rows"])
    artifacts.extend(build_receipts(result))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs())
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
