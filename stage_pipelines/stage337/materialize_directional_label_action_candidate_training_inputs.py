from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    csv_value,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    replace_bullet_value,
    sha256_file,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
    now_utc,
)


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337CJ"
RUN_ID = "run337CJ_materialize_directional_label_action_candidate_training_inputs_without_db_v1"
PARENT_RUN_ID = "run337CI_review_directional_label_action_policy_repair_inputs_without_db_v1"
NEXT_RUN_ID = "run337CK_guarded_directional_label_action_candidate_training_without_db_v1"
STATUS = "completed_stage337CJ_directional_label_action_candidate_training_inputs_materialized_no_training_no_selection"
JUDGMENT = "candidate_training_inputs_materialized_with_train_only_label_thresholds_and_forward_selection_firewall"
DECISION = "stage337CJ_open_run337CK_guarded_directional_label_action_candidate_training"
CLAIM_BOUNDARY = (
    "research_development_only_stage337CJ_directional_label_action_candidate_training_inputs_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
CI_DIR = STAGE_DIR / "02_runs" / "run337CI"
CH_DIR = STAGE_DIR / "02_runs" / "run337CH"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337CJ_directional_label_action_candidate_training_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337CJ_directional_label_action_candidate_training_inputs.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

SOURCE_MODEL_INPUT = ROOT / "data" / "processed" / "model_inputs" / "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58" / "model_input_dataset.parquet"
SOURCE_TRAINING = ROOT / "data" / "processed" / "training_datasets" / "label_v1_fwd12_split_v1_proxyw58" / "training_dataset.parquet"

CI_FINAL = CI_DIR / "final_decision.json"
CI_INPUT_REVIEW = CI_DIR / "input_review_matrix.csv"
CI_OVERFIT_REVIEW = CI_DIR / "no_overfit_gate_review.csv"
CI_RUNTIME_REVIEW = CI_DIR / "proxy_mt5_usability_review.csv"
CI_LINEAGE_REVIEW = CI_DIR / "data_lineage_review.csv"
CI_QUEUE = CI_DIR / "run337CJ_candidate_training_input_materialization_queue.csv"
CI_GATES = CI_DIR / "required_gate_coverage_audit.csv"

CH_POLARITY = CH_DIR / "polarity_audit_plan.csv"
CH_LABEL = CH_DIR / "label_v3_input_contract.csv"
CH_ACTION = CH_DIR / "action_v3_input_contract.csv"
CH_NEGATIVE = CH_DIR / "negative_control_plan.csv"
CH_FIREWALL = CH_DIR / "forward_selection_firewall.csv"
CH_RUNTIME = CH_DIR / "runtime_probe_requirement.csv"
CH_CURVE = CH_DIR / "curve_quality_measurement_plan.csv"

LABEL_CANDIDATE_MATRIX = RUN_DIR / "label_v3_candidate_matrix.csv"
ACTION_CANDIDATE_MATRIX = RUN_DIR / "action_v3_candidate_matrix.csv"
NEGATIVE_SCORING_TEMPLATE = RUN_DIR / "negative_control_scoring_template.csv"
SPLIT_BOUNDARY_MANIFEST = RUN_DIR / "split_boundary_manifest.csv"
FEATURE_SOURCE_MANIFEST = RUN_DIR / "feature_source_manifest.csv"
CANDIDATE_INPUT_MANIFEST = RUN_DIR / "candidate_training_input_manifest.json"
CK_QUEUE = RUN_DIR / "run337CK_guarded_training_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    CI_FINAL,
    CI_INPUT_REVIEW,
    CI_OVERFIT_REVIEW,
    CI_RUNTIME_REVIEW,
    CI_LINEAGE_REVIEW,
    CI_QUEUE,
    CI_GATES,
    CH_POLARITY,
    CH_LABEL,
    CH_ACTION,
    CH_NEGATIVE,
    CH_FIREWALL,
    CH_RUNTIME,
    CH_CURVE,
    SOURCE_MODEL_INPUT,
)
OUTPUT_FILES = (
    LABEL_CANDIDATE_MATRIX,
    ACTION_CANDIDATE_MATRIX,
    NEGATIVE_SCORING_TEMPLATE,
    SPLIT_BOUNDARY_MANIFEST,
    FEATURE_SOURCE_MANIFEST,
    CANDIDATE_INPUT_MANIFEST,
    CK_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
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

LABEL_COLUMNS = (
    "candidate_id",
    "candidate_family",
    "source_dataset",
    "target_formula",
    "threshold_policy",
    "train_threshold_value",
    "train_rows",
    "validation_rows",
    "oos_rows",
    "train_short",
    "train_flat",
    "train_long",
    "validation_short",
    "validation_flat",
    "validation_long",
    "oos_short",
    "oos_flat",
    "oos_long",
    "forward_use",
    "negative_controls_required",
    "claim_boundary",
)
ACTION_COLUMNS = (
    "action_candidate_id",
    "linked_label_candidates",
    "required_score_inputs",
    "entry_rule",
    "exit_rule",
    "density_floor",
    "cost_stress_required",
    "runtime_parity_required",
    "forbidden_shortcut",
    "claim_boundary",
)
NEGATIVE_COLUMNS = (
    "scoring_template_id",
    "control_id",
    "applies_to_label_candidates",
    "procedure",
    "expected_behavior",
    "required_splits",
    "blocks_if",
    "claim_boundary",
)
SPLIT_COLUMNS = (
    "split",
    "row_count",
    "start_timestamp",
    "end_timestamp",
    "labelable_rows",
    "short_rows",
    "flat_rows",
    "long_rows",
    "time_axis",
    "claim_boundary",
)
FEATURE_COLUMNS = (
    "source_id",
    "path",
    "rows",
    "columns",
    "feature_count",
    "feature_order_hash",
    "timestamp_column",
    "label_column",
    "split_column",
    "sha256",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_shortcut",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def read_source_frame():
    import pandas as pd

    return pd.read_parquet(io_path(SOURCE_MODEL_INPUT))


def label_from_return(values, threshold: float):
    import numpy as np

    labels = np.where(values < -threshold, "short", np.where(values > threshold, "long", "flat"))
    return labels


def counts_by_split(df, labels) -> dict[str, dict[str, int]]:
    import pandas as pd

    frame = pd.DataFrame({"split": df["split"].astype(str), "candidate_label": labels})
    output: dict[str, dict[str, int]] = {}
    for split in ("train", "validation", "oos"):
        subset = frame.loc[frame["split"].eq(split), "candidate_label"]
        counts = subset.value_counts(dropna=False).to_dict()
        output[split] = {
            "rows": int(subset.shape[0]),
            "short": int(counts.get("short", 0)),
            "flat": int(counts.get("flat", 0)),
            "long": int(counts.get("long", 0)),
        }
    return output


def feature_order_hash(columns: Sequence[str]) -> str:
    payload = "\n".join(columns).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def model_feature_columns(df) -> list[str]:
    excluded = {
        "timestamp",
        "symbol",
        "future_timestamp",
        "future_log_return_12",
        "label",
        "label_class",
        "label_id",
        "split",
        "split_id",
        "horizon_bars",
        "horizon_minutes",
    }
    return [str(column) for column in df.columns if str(column) not in excluded]


def summarize_inputs() -> dict[str, Any]:
    df = read_source_frame()
    ci_final = read_json(CI_FINAL)
    missing = [rel(path) for path in INPUT_FILES if not path_exists(path)]
    train = df.loc[df["split"].astype(str).eq("train")]
    abs_train = train["future_log_return_12"].abs()
    thresholds = {
        "q33_existing_style_train_only": float(abs_train.quantile(0.33)),
        "q40_cost_margin_train_only": float(abs_train.quantile(0.40)),
        "q50_cost_margin_train_only": float(abs_train.quantile(0.50)),
    }
    vol = df["historical_vol_20"].astype(float).replace(0, float("nan"))
    norm_return = df["future_log_return_12"].astype(float) / vol
    train_norm = norm_return.loc[df["split"].astype(str).eq("train")].abs().dropna()
    thresholds["volnorm_q50_train_only"] = float(train_norm.quantile(0.50)) if not train_norm.empty else float("nan")
    features = model_feature_columns(df)
    return {
        "df": df,
        "ci_final": ci_final,
        "missing_inputs": missing,
        "ci_next_action": ci_final.get("next_action", ""),
        "ci_failed_gates": ci_final.get("failed_gates", []),
        "thresholds": thresholds,
        "feature_columns": features,
        "feature_order_hash": feature_order_hash(features),
        "source_rows": int(df.shape[0]),
        "source_columns": int(df.shape[1]),
    }


def build_label_candidates(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    df = summary["df"]
    returns = df["future_log_return_12"].astype(float)
    thresholds = summary["thresholds"]
    original = df["label"].astype(str).to_numpy()
    flipped = df["label"].astype(str).map({"short": "long", "long": "short", "flat": "flat"}).to_numpy()
    candidates = [
        (
            "label_v3_original_v1_control",
            "polarity_baseline_control",
            original,
            "existing label_v1 class from training contract",
            "frozen_existing_threshold_from_source_contract",
            thresholds["q33_existing_style_train_only"],
        ),
        (
            "label_v3_flipped_polarity_probe",
            "direction_polarity_probe",
            flipped,
            "short and long labels mirrored; flat unchanged; diagnostic branch only",
            "no_forward_selection_original_vs_flipped",
            thresholds["q33_existing_style_train_only"],
        ),
        (
            "label_v3_cost_margin_q40_train_only",
            "lifecycle_cost_margin",
            label_from_return(returns, thresholds["q40_cost_margin_train_only"]),
            "future_log_return_12 with train-only q40 deadzone",
            "train_abs_return_quantile_q40_only",
            thresholds["q40_cost_margin_train_only"],
        ),
        (
            "label_v3_cost_margin_q50_train_only",
            "lifecycle_cost_margin",
            label_from_return(returns, thresholds["q50_cost_margin_train_only"]),
            "future_log_return_12 with train-only q50 deadzone",
            "train_abs_return_quantile_q50_only",
            thresholds["q50_cost_margin_train_only"],
        ),
    ]
    if math.isfinite(thresholds["volnorm_q50_train_only"]):
        vol = df["historical_vol_20"].astype(float).replace(0, float("nan"))
        norm_return = (returns / vol).fillna(0.0)
        candidates.append(
            (
                "label_v3_volnorm_margin_q50_train_only",
                "volatility_normalized_margin",
                label_from_return(norm_return, thresholds["volnorm_q50_train_only"]),
                "future_log_return_12 divided by historical_vol_20 with train-only q50 deadzone",
                "train_abs_volnorm_return_quantile_q50_only",
                thresholds["volnorm_q50_train_only"],
            )
        )
    output: list[dict[str, Any]] = []
    for candidate_id, family, labels, formula, threshold_policy, threshold in candidates:
        counts = counts_by_split(df, labels)
        output.append(
            {
                "candidate_id": candidate_id,
                "candidate_family": family,
                "source_dataset": rel(SOURCE_MODEL_INPUT),
                "target_formula": formula,
                "threshold_policy": threshold_policy,
                "train_threshold_value": threshold,
                "train_rows": counts["train"]["rows"],
                "validation_rows": counts["validation"]["rows"],
                "oos_rows": counts["oos"]["rows"],
                "train_short": counts["train"]["short"],
                "train_flat": counts["train"]["flat"],
                "train_long": counts["train"]["long"],
                "validation_short": counts["validation"]["short"],
                "validation_flat": counts["validation"]["flat"],
                "validation_long": counts["validation"]["long"],
                "oos_short": counts["oos"]["short"],
                "oos_flat": counts["oos"]["flat"],
                "oos_long": counts["oos"]["long"],
                "forward_use": "reject_only_no_selection",
                "negative_controls_required": "shifted_return;direction_flip;label_permutation;time_reversal;stale_context_carry",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_action_candidates(label_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    label_ids = ";".join(row["candidate_id"] for row in label_rows)
    return [
        {
            "action_candidate_id": "action_v3_transition_margin_hold12_template",
            "linked_label_candidates": label_ids,
            "required_score_inputs": "p_short;p_flat;p_long;previous_decision;feature_ready",
            "entry_rule": "enter only on signal transition with fixed margin declared by CK before training",
            "exit_rule": "max_hold_bars=12; opposite/flat signal diagnostics logged but not tuned in CJ",
            "density_floor": "CK must report trades/day and sparse/fail label before ONNX packaging",
            "cost_stress_required": "cost0,cost1,cost2,cost5,cost10",
            "runtime_parity_required": "proxy-MT5 row parity and trade/fill parity before runtime claims",
            "forbidden_shortcut": "no session/hour/month/side deletion from forward losses",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "action_candidate_id": "action_v3_cost_margin_abstention_template",
            "linked_label_candidates": label_ids,
            "required_score_inputs": "top_direction_score;runner_up_score;flat_score;fixed_cost_margin",
            "entry_rule": "abstain when direction score does not clear fixed predeclared cost-margin rule",
            "exit_rule": "same max_hold_bars=12 lifecycle template",
            "density_floor": "abstention cannot reduce trade count below floor without sparse/failed label",
            "cost_stress_required": "cost2 primary, cost5/cost10 fragility stress",
            "runtime_parity_required": "proxy expected vs MT5 telemetry comparison required",
            "forbidden_shortcut": "no forward threshold search disguised as abstention",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "action_candidate_id": "action_v3_original_threshold_control_template",
            "linked_label_candidates": "label_v3_original_v1_control",
            "required_score_inputs": "p_short;p_flat;p_long;decision_label",
            "entry_rule": "baseline fixed-threshold decision control for comparison only",
            "exit_rule": "same hold12 lifecycle template",
            "density_floor": "must not be promoted from proxy-only KPI",
            "cost_stress_required": "cost0,cost2,cost5",
            "runtime_parity_required": "same row parity requirement",
            "forbidden_shortcut": "no selecting control because one split looks better",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_negative_template(label_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    label_ids = ";".join(row["candidate_id"] for row in label_rows)
    controls = read_csv(CH_NEGATIVE)
    output = []
    for control in controls:
        output.append(
            {
                "scoring_template_id": f"score_{control.get('control_id', 'control')}",
                "control_id": control.get("control_id", ""),
                "applies_to_label_candidates": label_ids,
                "procedure": control.get("procedure", ""),
                "expected_behavior": control.get("expected_behavior", ""),
                "required_splits": "train;validation;oos;forward_reject_only_when_available",
                "blocks_if": control.get("blocks_if", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_split_manifest(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    df = summary["df"]
    output: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        subset = df.loc[df["split"].astype(str).eq(split)].copy()
        labels = subset["label"].astype(str).value_counts(dropna=False).to_dict()
        output.append(
            {
                "split": split,
                "row_count": int(subset.shape[0]),
                "start_timestamp": str(subset["timestamp"].min()),
                "end_timestamp": str(subset["timestamp"].max()),
                "labelable_rows": int(subset["future_log_return_12"].notna().sum()),
                "short_rows": int(labels.get("short", 0)),
                "flat_rows": int(labels.get("flat", 0)),
                "long_rows": int(labels.get("long", 0)),
                "time_axis": "timestamp is broker-clock/bar-close aligned key from existing model input; forward post-2026-04-14 is not used in CJ",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def build_feature_manifest(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "source_id": "model_input_feature_set_v2_mt5_price_proxy_58",
            "path": rel(SOURCE_MODEL_INPUT),
            "rows": summary["source_rows"],
            "columns": summary["source_columns"],
            "feature_count": len(summary["feature_columns"]),
            "feature_order_hash": summary["feature_order_hash"],
            "timestamp_column": "timestamp",
            "label_column": "label/label_class/future_log_return_12",
            "split_column": "split",
            "sha256": sha256_file(SOURCE_MODEL_INPUT),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_ck_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337CK_guarded_candidate_training",
            "next_run_id": NEXT_RUN_ID,
            "task": "train guarded scout models on CJ candidate label/action inputs and materialize proxy expected plus negative-control scorecards",
            "required_inputs": ";".join(rel(path) for path in (LABEL_CANDIDATE_MATRIX, ACTION_CANDIDATE_MATRIX, NEGATIVE_SCORING_TEMPLATE, SPLIT_BOUNDARY_MANIFEST, FEATURE_SOURCE_MANIFEST, CANDIDATE_INPUT_MANIFEST)),
            "required_outputs": "guarded_model_scorecard.csv;negative_control_scorecard.csv;proxy_expected_by_candidate.csv;runtime_probe_package_queue.csv",
            "blocked_if_missing": "missing split boundary, feature source hash, negative-control template, or no-forward-selection firewall",
            "forbidden_shortcut": "do not use forward data for model/threshold/action selection; do not optimize lot; do not claim Forward Passed",
            "effect": "후보 입력을 실제 guarded training(방어 학습)으로 넘기되, 선택/운영 주장은 닫아둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_candidate_manifest(summary: Mapping[str, Any], label_rows: Sequence[Mapping[str, Any]], action_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_model_input": rel(SOURCE_MODEL_INPUT),
        "source_training_dataset": rel(SOURCE_TRAINING),
        "source_rows": summary["source_rows"],
        "feature_columns": summary["feature_columns"],
        "feature_order_hash": summary["feature_order_hash"],
        "thresholds_train_only": summary["thresholds"],
        "label_candidates": [row["candidate_id"] for row in label_rows],
        "action_candidates": [row["action_candidate_id"] for row in action_rows],
        "forward_use": "reject_only_no_selection",
        "model_training": "not_run",
        "candidate_selection": "not_run",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_receipts(summary: Mapping[str, Any], manifest: Mapping[str, Any]) -> list[Path]:
    data_receipt = {
        "data_source": rel(SOURCE_MODEL_INPUT),
        "time_axis": "timestamp is existing model-input bar-close alignment key; no post-2026-04-14 forward data used in CJ",
        "sample_scope": "US100 M5 model input rows 2022-09-01 through 2026-04-13 across train/validation/OOS",
        "missing_or_duplicate_check": "CJ checks split row counts and labelable rows; CK must re-check before training",
        "feature_label_boundary": "candidate labels derive from future_log_return_12 already materialized under label contract; train-only thresholds use train split only",
        "split_boundary": "train/validation/OOS time-ordered; forward is reject-only and absent from candidate threshold fitting",
        "leakage_risk": "using validation/OOS/forward to choose threshold or polarity",
        "data_hash_or_identity": {rel(SOURCE_MODEL_INPUT): sha256_file(SOURCE_MODEL_INPUT), "feature_order_hash": summary["feature_order_hash"]},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "not_trained_in_run337CJ; CK queued for guarded scouts",
        "target_and_label": "label_v3 candidate matrix from original/flipped/cost-margin/volnorm train-only thresholds",
        "split_method": "time-ordered train/validation/OOS; no random shuffle; forward reject-only",
        "selection_metric": "not_applicable_no_selection",
        "secondary_metrics": "negative controls, density floor, cost ladder, runtime parity, curve quality",
        "threshold_policy": "candidate thresholds computed on train only; no forward threshold tuning",
        "overfit_risk": "choosing candidate from validation/OOS/forward after seeing KPI",
        "calibration_risk": "future model scores are rank diagnostics until calibrated",
        "comparison_baseline": "label_v3_original_v1_control plus flipped polarity probe",
        "validation_judgment": "exploratory_candidate_input_materialization",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in (LABEL_CANDIDATE_MATRIX, ACTION_CANDIDATE_MATRIX, NEGATIVE_SCORING_TEMPLATE, SPLIT_BOUNDARY_MANIFEST, FEATURE_SOURCE_MANIFEST, CANDIDATE_INPUT_MANIFEST, CK_QUEUE, REPORT_PATH)],
        "artifact_hashes": {},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_with_manifest_for_02_runs; tracked_reports_and_registers",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "candidate label/action matrices, split manifest, feature source manifest, negative-control scoring template, CK queue",
        "evidence_missing": "no model training, no proxy expected, no MT5 runtime probe, no forward decision",
        "judgment_label": "exploratory",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": "CK must train guarded scouts and report negative-control/proxy expected scorecards before MT5 package",
        "user_explanation_hook": "후보 학습 입력은 만들어졌지만 아직 모델 학습이나 수익 주장은 아니다.",
    }
    paths = [
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(LINEAGE_RECEIPT, lineage_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt["artifact_hashes"] = {rel(path): sha256_file(path) for path in paths if path != LINEAGE_RECEIPT and path_exists(path)}
    write_json(LINEAGE_RECEIPT, lineage_receipt)
    return paths


def build_gates(summary: Mapping[str, Any], rows: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[dict[str, str]]:
    def row(gate_id: str, ok: bool, observed: Any, expected: str, effect: str) -> dict[str, str]:
        return {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "observed": str(observed),
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    thresholds = summary["thresholds"]
    finite_thresholds = all(math.isfinite(float(value)) for value in thresholds.values())
    return [
        row("cj_gate_inputs_present", not summary["missing_inputs"], ";".join(summary["missing_inputs"]) or "none", "no_missing_inputs", "CI/CH 산출물과 실제 모델 입력을 연결한다."),
        row("cj_gate_parent_points_to_cj", summary["ci_next_action"] == RUN_ID, summary["ci_next_action"], RUN_ID, "현재 실행이 CI next_action(다음 행동)과 맞는다."),
        row("cj_gate_ci_gates_clean", not summary["ci_failed_gates"], ";".join(summary["ci_failed_gates"]) or "none", "no_failed_ci_gates", "실패한 리뷰 위에서 후보 입력을 만들지 않는다."),
        row("cj_gate_source_dataset_loaded", summary["source_rows"] == 46650 and len(summary["feature_columns"]) >= 58, f"rows={summary['source_rows']};features={len(summary['feature_columns'])}", "46650 rows and >=58 features", "실제 학습 입력 정체성을 확인한다."),
        row("cj_gate_train_only_thresholds", finite_thresholds, json.dumps(json_ready(thresholds), ensure_ascii=False, sort_keys=True), "finite train-only thresholds", "라벨 후보 임계값을 train split(학습 분할)에서만 만든다."),
        row("cj_gate_label_candidates", len(rows["label"]) >= 4, len(rows["label"]), ">=4 label candidates", "original/flip/cost/volnorm 후보를 비교 가능하게 한다."),
        row("cj_gate_action_candidates", len(rows["action"]) >= 3, len(rows["action"]), ">=3 action candidates", "학습 후 행동 정책 비교 틀을 만든다."),
        row("cj_gate_negative_templates", len(rows["negative"]) >= 5, len(rows["negative"]), ">=5 negative templates", "부정 대조 채점이 학습 전부터 붙는다."),
        row("cj_gate_split_manifest", len(rows["split"]) == 3 and sum(int(item["row_count"]) for item in rows["split"]) == summary["source_rows"], f"rows={sum(int(item['row_count']) for item in rows['split'])}", "3 splits sum to source rows", "분할 경계가 데이터 행수와 맞는다."),
        row("cj_gate_no_training_or_selection", True, "model_training=not_run;candidate_selection=not_run", "no_training_no_selection", "CJ를 후보 입력 물질화로만 닫는다."),
    ]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337CJ Candidate Training Inputs(후보 학습 입력)

## Conclusion(결론)

run337CJ(337CJ 실행)는 실제 model input parquet(모델 입력 파케이)를 읽어 label_v3/action_v3 candidate training inputs(후보 학습 입력)를 물질화했다.

Effect(효과): 다음 run337CK(337CK 실행)는 새 모델을 학습하더라도 train-only thresholds(학습 전용 임계값), negative controls(부정 대조), split boundary(분할 경계), proxy-MT5 runtime requirement(프록시-MT5 런타임 요구사항)를 함께 들고 시작한다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- source_rows(원천 행): `{final["source_rows"]}`
- feature_count(피처 수): `{final["feature_count"]}`
- label_candidate_rows(라벨 후보 행): `{final["label_candidate_rows"]}`
- action_candidate_rows(행동 후보 행): `{final["action_candidate_rows"]}`
- negative_template_rows(부정 대조 템플릿 행): `{final["negative_template_rows"]}`
- split_rows(분할 행): `{final["split_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337CJ

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): 실제 model input parquet(모델 입력 파케이)에서 후보 라벨/행동 학습 입력을 만들고 CK 방어 학습을 연다.
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
    workspace_text = workspace_text.replace(f"current_run_id: {RUN_ID}", f"current_run_id: {NEXT_RUN_ID}", 1)
    focus_entry = (
        "current_focus:\n- >-\n"
        f"  Stage337 run337CJ focus complete: directional label/action candidate training inputs(방향 라벨/행동 후보 학습 입력)를 `{STATUS}`로 물질화했다. "
        "Effect(효과): run337CK(337CK 실행)에서 guarded candidate training(방어 후보 학습)을 실행한다."
    )
    if "Stage337 run337CJ focus complete" not in workspace_text:
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
## Stage337 run337CJ(337CJ 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 실제 model input parquet(모델 입력 파케이)에서 label/action candidate training inputs(라벨/행동 후보 학습 입력), split manifest(분할 목록), negative scoring template(부정 대조 채점 틀)을 만들었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337CJ(337CJ 실행)" not in current_text:
        marker = "## Stage337 run337CI(337CI"
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
- actual_mt5_execution(실제 MT5 실행): `not_run_cj_input_materialization_only_run337CE_reviewed`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 guarded candidate training(방어 후보 학습)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = f"- {TODAY}: run337CJ(337CJ 실행) materialized directional label/action candidate training inputs(방향 라벨/행동 후보 학습 입력). Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    if stage_entry not in stage_text:
        stage_text = stage_text.rstrip() + "\n" + stage_entry + "\n"
    artifacts.append(write_text_preserving(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337CJ materialized directional label/action candidate training inputs(방향 라벨/행동 후보 학습 입력) and opened `{NEXT_RUN_ID}`."
    if changelog_entry not in changelog_text:
        changelog_text = changelog_text.rstrip() + "\n" + changelog_entry + "\n"
    artifacts.append(write_text_preserving(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "directional_label_action_candidate_training_input_materialization_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__candidate_training_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "candidate_training_inputs",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "candidate_input_materialization",
        "tier_scope": "out_of_scope_by_claim_input_materialization_no_tier_kpi",
        "kpi_scope": "candidate_input_no_training",
        "scoreboard_lane": "data_integrity_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": "source_rows=46650;label_candidates_materialized",
        "guardrail_kpi": "train_only_thresholds;negative_controls;no_forward_selection",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__candidate_training_inputs",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "actual model input parquet plus CI/CH contracts",
        "kpi_scope": "candidate_input_no_training",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__candidate_training_inputs",
        "family": "data_integrity_model_validation_artifact_lineage",
        "question": "are candidate training inputs materialized without forward selection",
        "metric_scope": "candidate_input_no_forward_decision",
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
    summary = summarize_inputs()
    label_rows = build_label_candidates(summary)
    action_rows = build_action_candidates(label_rows)
    negative_rows = build_negative_template(label_rows)
    split_rows = build_split_manifest(summary)
    feature_rows = build_feature_manifest(summary)
    queue_rows = build_ck_queue()
    manifest = build_candidate_manifest(summary, label_rows, action_rows)
    rows = {
        "label": label_rows,
        "action": action_rows,
        "negative": negative_rows,
        "split": split_rows,
        "feature": feature_rows,
        "queue": queue_rows,
    }
    gates = build_gates(summary, rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "source_rows": summary["source_rows"],
        "source_columns": summary["source_columns"],
        "feature_count": len(summary["feature_columns"]),
        "feature_order_hash": summary["feature_order_hash"],
        "label_candidate_rows": len(label_rows),
        "action_candidate_rows": len(action_rows),
        "negative_template_rows": len(negative_rows),
        "split_rows": len(split_rows),
        "queue_rows": len(queue_rows),
        "model_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
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
        write_csv(LABEL_CANDIDATE_MATRIX, LABEL_COLUMNS, label_rows),
        write_csv(ACTION_CANDIDATE_MATRIX, ACTION_COLUMNS, action_rows),
        write_csv(NEGATIVE_SCORING_TEMPLATE, NEGATIVE_COLUMNS, negative_rows),
        write_csv(SPLIT_BOUNDARY_MANIFEST, SPLIT_COLUMNS, split_rows),
        write_csv(FEATURE_SOURCE_MANIFEST, FEATURE_COLUMNS, feature_rows),
        write_json(CANDIDATE_INPUT_MANIFEST, manifest),
        write_csv(CK_QUEUE, QUEUE_COLUMNS, queue_rows),
        write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
        write_json(FINAL_DECISION, final),
        write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
    ]
    artifacts.extend(build_receipts(summary, manifest))
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs())
    artifacts.extend(update_registers(artifacts))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
