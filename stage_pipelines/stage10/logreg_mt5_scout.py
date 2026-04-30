from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.models.baseline_training import (  # noqa: E402
    BaselineTrainingConfig,
    load_feature_order,
    train_baseline_model,
)
from foundation.alpha.decision_views import (  # noqa: E402
    DECISION_CLASS_NO_TRADE,
    DECISION_LABEL_NO_TRADE,
    PROBABILITY_COLUMNS,
    REQUIRED_TIER_VIEWS,
    TIER_A,
    TIER_AB,
    TIER_B,
    TIER_COLUMN,
    ThresholdRule,
    apply_threshold_rule,
    build_paired_tier_records as _build_paired_tier_records,
    build_prediction_frame,
    build_tier_prediction_views,
    materialize_tier_prediction_views,
    normalize_tier_label,
    probability_matrix,
    prediction_view_metrics,
    select_threshold_from_sweep,
    sweep_threshold_rules,
    threshold_id as _threshold_id,
    threshold_rule_from_values,
    threshold_rule_payload,
    validate_threshold_rule,
)
from foundation.alpha import scout_runner as alpha_scout_runner  # noqa: E402
from foundation.control_plane import packet_writers  # noqa: E402
from foundation.control_plane.ledger import (  # noqa: E402
    io_path as _io_path,
    json_ready as _json_ready,
    path_exists as _path_exists,
)
from foundation.control_plane.mt5_kpi_records import (  # noqa: E402
    ROUTING_MODE_A_B_FALLBACK,
    ROUTING_MODE_A_ONLY,
    build_mt5_kpi_records,
    enrich_mt5_kpi_records_with_route_coverage,
    mt5_metrics_with_runtime_counts,
    routed_component_metrics,
)
from foundation.control_plane.routing_coverage import (  # noqa: E402
    SESSION_SLICE_DEFINITIONS,
    apply_session_slice,
    build_eval_route_coverage_summary,
    session_slice_payload,
)
from foundation.control_plane.tier_context import (  # noqa: E402
    TIER_B_CONTEXT_GROUPS,
    TIER_B_PARTIAL_CONTEXT_SUBTYPES,
    apply_tier_b_fallback_subtype_filter,
    classify_tier_b_partial_context,
    normalize_tier_b_fallback_allowed_subtypes,
    parse_tier_b_fallback_allowed_subtypes,
)
from foundation.control_plane.tier_context_materialization import (  # noqa: E402
    ROUTE_ROLE_A_PRIMARY,
    ROUTE_ROLE_B_FALLBACK,
    ROUTE_ROLE_NO_TIER,
    TIER_B_CORE_FEATURE_ORDER,
    TIER_B_PARTIAL_CONTEXT_DATASET_ID,
    TIER_B_PARTIAL_CONTEXT_FEATURE_SET_ID,
    TIER_B_PARTIAL_CONTEXT_POLICY_ID,
    build_tier_b_partial_context_frames,
)
from foundation.models.onnx_bridge import (  # noqa: E402
    _find_probability_output,
    _onnx_output_shape,
    check_onnxruntime_probability_parity,
    classifier_classes,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
    ordered_sklearn_probabilities,
)
from foundation.mt5 import runtime_artifacts as mt5_artifacts  # noqa: E402
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics  # noqa: E402
from foundation.mt5.mql5_compile import compile_mql5_ea, metaeditor_command_log_path  # noqa: E402
from foundation.mt5.runtime_artifacts import (  # noqa: E402
    EA_EXPERT_PATH,
    EA_SOURCE_PATH,
    EA_TESTER_SET_NAME,
    copy_to_common_files,
    export_mt5_feature_matrix_csv,
    mt5_runtime_module_hashes,
    sha256_file,
    sha256_file_lf_normalized,
    validate_feature_matrix,
    write_json,
)
from foundation.mt5.terminal_runner import (  # noqa: E402
    run_mt5_tester,
    validate_mt5_runtime_outputs,
    wait_for_mt5_runtime_outputs,
)
from foundation.mt5.tester_files import (  # noqa: E402
    TesterMaterializationConfig,
    materialize_tester_ini_file,
    materialize_tester_set_file,
)


STAGE_ID = "10_alpha_scout__default_split_model_threshold_scan"
RUN_NUMBER = "run01A"
RUN_ID = "run01A_logreg_threshold_mt5_scout_v1"
EXPLORATION_LABEL = "stage10_Model__LogReg_MT5Scout"
MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
TIER_B_MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_feature_set_v1_no_placeholder_top3_weights"
TIER_B_FEATURE_SET_ID = "feature_set_v1_no_placeholder_top3_weight_features"
FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"
DEFAULT_MODEL_INPUT_PATH = Path(
    "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
DEFAULT_FEATURE_ORDER_PATH = DEFAULT_MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
DEFAULT_TIER_B_MODEL_INPUT_PATH = Path(
    "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v1/model_input_dataset.parquet"
)
DEFAULT_TIER_B_FEATURE_ORDER_PATH = DEFAULT_TIER_B_MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
DEFAULT_RAW_ROOT = Path("data/raw/mt5_bars/m5")
DEFAULT_TRAINING_SUMMARY_PATH = Path(
    "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json"
)
DEFAULT_STAGE07_MODEL_PATH = Path(
    "stages/07_model_training_baseline__contract_preprocessing_smoke/02_runs/"
    "20260425_stage07_baseline_training_smoke_v1/model.joblib"
)
DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
STAGE_RUN_LEDGER_PATH = Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
DEFAULT_COMMON_FILES_ROOT = Path.home() / "AppData/Roaming/MetaQuotes/Terminal/Common/Files"
DEFAULT_TERMINAL_DATA_ROOT = REPO_ROOT.parents[2]
DEFAULT_TESTER_PROFILE_ROOT = REPO_ROOT.parents[1] / "Profiles" / "Tester"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/stage10/run01A_logreg_threshold_mt5_scout_v1"
MT5_RECORD_TIER_A_ONLY_PREFIX = "mt5_tier_a_only"
MT5_RECORD_TIER_B_FALLBACK_ONLY_PREFIX = "mt5_tier_b_fallback_only"


def default_common_run_root(run_id: str) -> str:
    return f"Project_Obsidian_Prime_v2/stage10/{run_id}"


def configure_run_identity(
    *,
    run_number: str,
    run_id: str,
    exploration_label: str,
    common_run_root: str | None = None,
) -> None:
    global RUN_NUMBER, RUN_ID, EXPLORATION_LABEL, DEFAULT_RUN_OUTPUT_ROOT, COMMON_RUN_ROOT

    RUN_NUMBER = run_number
    RUN_ID = run_id
    EXPLORATION_LABEL = exploration_label
    DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
    COMMON_RUN_ROOT = common_run_root or default_common_run_root(run_id)
    alpha_scout_runner.configure_run_identity(
        run_number=RUN_NUMBER,
        run_id=RUN_ID,
        exploration_label=EXPLORATION_LABEL,
        common_run_root=COMMON_RUN_ROOT,
        stage_id=STAGE_ID,
    )


configure_run_identity(
    run_number=RUN_NUMBER,
    run_id=RUN_ID,
    exploration_label=EXPLORATION_LABEL,
    common_run_root=COMMON_RUN_ROOT,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize a Stage 10 logistic MT5 scout payload.")
    parser.add_argument("--run-number", default=RUN_NUMBER)
    parser.add_argument("--run-id", default=RUN_ID)
    parser.add_argument("--exploration-label", default=EXPLORATION_LABEL)
    parser.add_argument("--common-run-root", default=None)
    parser.add_argument("--model-input-path", default=str(DEFAULT_MODEL_INPUT_PATH))
    parser.add_argument("--feature-order-path", default=str(DEFAULT_FEATURE_ORDER_PATH))
    parser.add_argument("--tier-b-model-input-path", default=str(DEFAULT_TIER_B_MODEL_INPUT_PATH))
    parser.add_argument("--tier-b-feature-order-path", default=str(DEFAULT_TIER_B_FEATURE_ORDER_PATH))
    parser.add_argument("--raw-root", default=str(DEFAULT_RAW_ROOT))
    parser.add_argument("--training-summary-path", default=str(DEFAULT_TRAINING_SUMMARY_PATH))
    parser.add_argument("--stage07-model-path", default=str(DEFAULT_STAGE07_MODEL_PATH))
    parser.add_argument("--run-output-root", default=None)
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--tier-column", default=TIER_COLUMN)
    parser.add_argument("--random-seed", type=int, default=10)
    parser.add_argument("--max-iter", type=int, default=2000)
    parser.add_argument("--parity-rows", type=int, default=128)
    parser.add_argument("--max-hold-bars", type=int, default=12)
    parser.add_argument("--tier-a-threshold-id", default=None)
    parser.add_argument("--tier-a-short-threshold", type=float, default=None)
    parser.add_argument("--tier-a-long-threshold", type=float, default=None)
    parser.add_argument("--tier-a-min-margin", type=float, default=None)
    parser.add_argument("--tier-b-threshold-id", default=None)
    parser.add_argument("--tier-b-short-threshold", type=float, default=None)
    parser.add_argument("--tier-b-long-threshold", type=float, default=None)
    parser.add_argument("--tier-b-min-margin", type=float, default=None)
    parser.add_argument("--disable-routed-fallback", action="store_true")
    parser.add_argument("--tier-b-fallback-allowed-subtypes", default=None)
    parser.add_argument("--session-slice-id", choices=sorted(SESSION_SLICE_DEFINITIONS), default=None)
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args()


def load_label_threshold(summary_path: Path) -> float:
    payload = json.loads(_io_path(summary_path).read_text(encoding="utf-8"))
    threshold = float(payload["threshold_log_return"])
    if not np.isfinite(threshold) or threshold <= 0:
        raise RuntimeError(f"Invalid label threshold in {summary_path}: {threshold}")
    return threshold


def build_paired_tier_records(
    tier_views: Mapping[str, pd.DataFrame],
    *,
    run_id: str | None = None,
    stage_id: str | None = None,
    base_path: str | Path | None = None,
    kpi_scope: str = "signal_probability_threshold",
    scoreboard_lane: str = "structural_scout",
    external_verification_status: str = "out_of_scope_by_claim",
) -> list[dict[str, Any]]:
    return _build_paired_tier_records(
        tier_views,
        run_id=run_id or RUN_ID,
        stage_id=stage_id or STAGE_ID,
        base_path=base_path,
        kpi_scope=kpi_scope,
        scoreboard_lane=scoreboard_lane,
        external_verification_status=external_verification_status,
    )


common_ref = alpha_scout_runner.common_ref
mt5_short_profile_ini_name = alpha_scout_runner.mt5_short_profile_ini_name
materialize_mt5_attempt_files = alpha_scout_runner.materialize_mt5_attempt_files
materialize_mt5_routed_attempt_files = alpha_scout_runner.materialize_mt5_routed_attempt_files
report_name_from_attempt = alpha_scout_runner.report_name_from_attempt
remove_existing_mt5_report_artifacts = alpha_scout_runner.remove_existing_mt5_report_artifacts
collect_mt5_strategy_report_artifacts = alpha_scout_runner.collect_mt5_strategy_report_artifacts
attach_mt5_report_metrics = alpha_scout_runner.attach_mt5_report_metrics

def run_stage10_logreg_mt5_scout(
    *,
    model_input_path: Path,
    feature_order_path: Path,
    tier_b_model_input_path: Path,
    tier_b_feature_order_path: Path,
    raw_root: Path,
    training_summary_path: Path,
    stage07_model_path: Path,
    run_output_root: Path,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    tier_column: str = TIER_COLUMN,
    random_seed: int = 10,
    max_iter: int = 2000,
    parity_rows: int = 128,
    max_hold_bars: int = 12,
    tier_a_threshold_rule: ThresholdRule | None = None,
    tier_b_threshold_rule: ThresholdRule | None = None,
    routed_fallback_enabled: bool = True,
    session_slice_id: str | None = None,
    tier_b_fallback_allowed_subtypes: Sequence[str] | None = None,
    attempt_mt5: bool = False,
    terminal_path: Path = Path(r"C:\Program Files\MetaTrader 5\terminal64.exe"),
    metaeditor_path: Path = Path(r"C:\Program Files\MetaTrader 5\MetaEditor64.exe"),
) -> dict[str, Any]:
    routing_mode = ROUTING_MODE_A_B_FALLBACK if routed_fallback_enabled else ROUTING_MODE_A_ONLY
    routing_detail = (
        "tier_a_primary_tier_b_partial_context_fallback"
        if routed_fallback_enabled
        else "tier_a_primary_no_fallback"
    )
    session_slice = session_slice_payload(session_slice_id)
    allowed_fallback_subtypes = normalize_tier_b_fallback_allowed_subtypes(tier_b_fallback_allowed_subtypes)
    tier_a_feature_order = load_feature_order(feature_order_path)
    tier_a_feature_hash = ordered_hash(tier_a_feature_order)
    if tier_a_feature_hash != FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {tier_a_feature_hash} != {FEATURE_ORDER_HASH}")

    stage04_tier_b_feature_order = load_feature_order(tier_b_feature_order_path)
    tier_b_feature_order = list(TIER_B_CORE_FEATURE_ORDER)
    missing_core_features = sorted(set(tier_b_feature_order).difference(stage04_tier_b_feature_order))
    if missing_core_features:
        raise RuntimeError(f"Tier B core feature order is missing Stage04 reference features: {missing_core_features}")
    tier_b_feature_hash = ordered_hash(tier_b_feature_order)
    label_threshold = load_label_threshold(training_summary_path)

    tier_a_frame = pd.read_parquet(_io_path(model_input_path))
    tier_a_frame["timestamp"] = pd.to_datetime(tier_a_frame["timestamp"], utc=True)
    tier_a_frame["route_role"] = ROUTE_ROLE_A_PRIMARY
    tier_a_frame["partial_context_subtype"] = "Tier_A_full_context"
    tier_a_frame["missing_feature_group_mask"] = "none"
    tier_a_frame["available_feature_group_mask"] = "macro|constituent|basket"
    tier_a_frame["tier_a_primary_available"] = True
    tier_a_frame["tier_a_full_feature_ready"] = True
    tier_a_frame["tier_b_core_ready"] = True
    tier_b_context = build_tier_b_partial_context_frames(
        raw_root=raw_root,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=tier_a_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=label_threshold,
    )
    tier_b_training_frame = tier_b_context["tier_b_training_frame"]
    tier_b_frame = tier_b_context["tier_b_fallback_frame"]
    no_tier_frame = tier_b_context["no_tier_frame"]
    route_coverage = tier_b_context["summary"]
    config = BaselineTrainingConfig(random_seed=random_seed, max_iter=max_iter)
    tier_a_model = joblib.load(_io_path(stage07_model_path))
    tier_b_model = train_baseline_model(tier_b_training_frame, list(tier_b_feature_order), config)

    _io_path(run_output_root).mkdir(parents=True, exist_ok=True)
    models_root = run_output_root / "models"
    predictions_root = run_output_root / "predictions"
    sweeps_root = run_output_root / "sweeps"
    mt5_root = run_output_root / "mt5"
    reports_root = run_output_root / "reports"

    tier_a_model_path = models_root / "tier_a_stage07_model.joblib"
    tier_b_model_path = models_root / "tier_b_logreg_core42_model.joblib"
    tier_b_feature_order_path_run = models_root / "tier_b_core42_feature_order.txt"
    tier_a_predictions_path = predictions_root / "tier_a_predictions.parquet"
    tier_b_predictions_path = predictions_root / "tier_b_predictions.parquet"
    no_tier_route_path = predictions_root / "no_tier_route_rows.parquet"
    route_coverage_path = predictions_root / "route_coverage_summary.json"
    combined_predictions_path = predictions_root / "tier_ab_combined_predictions.parquet"
    threshold_sweep_path = sweeps_root / "threshold_sweep_validation_combined.csv"
    tier_a_onnx_path = models_root / "tier_a_stage07_logreg.onnx"
    tier_b_onnx_path = models_root / "tier_b_logreg_core42_partial_context.onnx"

    validation_a = tier_a_frame.loc[tier_a_frame["split"].astype(str).eq("validation")].copy()
    validation_b = tier_b_frame.loc[tier_b_frame["split"].astype(str).eq("validation")].copy()
    values_a = validation_a.loc[:, list(tier_a_feature_order)].to_numpy(dtype="float64", copy=False)
    values_b = validation_b.loc[:, list(tier_b_feature_order)].to_numpy(dtype="float64", copy=False)
    validation_probabilities = np.vstack(
        [
            ordered_sklearn_probabilities(tier_a_model, values_a),
            ordered_sklearn_probabilities(tier_b_model, values_b),
        ]
    )
    validation_labels = np.concatenate(
        [
            validation_a["label_class"].astype("int64").to_numpy(),
            validation_b["label_class"].astype("int64").to_numpy(),
        ]
    )
    threshold_sweeps = {
        "tier_a_separate": sweep_threshold_rules(
            ordered_sklearn_probabilities(tier_a_model, values_a),
            validation_a["label_class"].astype("int64").to_numpy(),
        ),
        "tier_b_separate": sweep_threshold_rules(
            ordered_sklearn_probabilities(tier_b_model, values_b),
            validation_b["label_class"].astype("int64").to_numpy(),
        ),
        "tier_ab_combined": sweep_threshold_rules(
            validation_probabilities,
            validation_labels,
        ),
    }
    _io_path(sweeps_root).mkdir(parents=True, exist_ok=True)
    threshold_sweep_paths = {
        "tier_a_separate": sweeps_root / "threshold_sweep_validation_tier_a.csv",
        "tier_b_separate": sweeps_root / "threshold_sweep_validation_tier_b.csv",
        "tier_ab_combined": threshold_sweep_path,
    }
    for view_name, sweep in threshold_sweeps.items():
        sweep.to_csv(_io_path(threshold_sweep_paths[view_name]), index=False)
    threshold_sweep = threshold_sweeps["tier_ab_combined"]
    selected = select_threshold_from_sweep(threshold_sweep)
    selected_sweep_rule = ThresholdRule(
        threshold_id=str(selected["threshold_id"]),
        short_threshold=float(selected["short_threshold"]),
        long_threshold=float(selected["long_threshold"]),
        min_margin=float(selected["min_margin"]),
    )
    tier_a_rule = tier_a_threshold_rule or selected_sweep_rule
    tier_b_rule = tier_b_threshold_rule or tier_a_rule
    rule = tier_a_rule
    threshold_selection = dict(selected)
    threshold_selection.update(
        {
            "selection_source": "explicit_override" if tier_a_threshold_rule or tier_b_threshold_rule else "validation_combined_sweep",
            "threshold_id": (
                (
                    f"a_{tier_a_rule.threshold_id}__b_{tier_b_rule.threshold_id}__hold{int(max_hold_bars)}"
                    if routed_fallback_enabled
                    else f"a_{tier_a_rule.threshold_id}__b_disabled__hold{int(max_hold_bars)}"
                )
                + (f"__slice_{session_slice_id}" if session_slice_id else "")
                + (
                    "__bsub_" + "_".join(re.sub(r"[^A-Za-z0-9]+", "", subtype) for subtype in allowed_fallback_subtypes)
                    if allowed_fallback_subtypes
                    else ""
                )
            ),
            "selected_combined_sweep_rule": threshold_rule_payload(selected_sweep_rule),
            "tier_a_rule": threshold_rule_payload(tier_a_rule),
            "tier_b_fallback_rule": threshold_rule_payload(tier_b_rule),
            "routed_fallback_enabled": bool(routed_fallback_enabled),
            "session_slice": session_slice,
            "tier_b_fallback_allowed_subtypes": list(allowed_fallback_subtypes) if allowed_fallback_subtypes else None,
            "max_hold_bars": int(max_hold_bars),
            "short_threshold": tier_a_rule.short_threshold,
            "long_threshold": tier_a_rule.long_threshold,
            "min_margin": tier_a_rule.min_margin,
        }
    )

    tier_a_eval_frame = apply_session_slice(tier_a_frame, session_slice)
    tier_b_eval_frame_unfiltered = apply_session_slice(tier_b_frame, session_slice)
    tier_b_eval_frame, tier_b_filtered_out_frame = apply_tier_b_fallback_subtype_filter(
        tier_b_eval_frame_unfiltered,
        allowed_fallback_subtypes,
    )
    no_tier_eval_frame_base = apply_session_slice(no_tier_frame, session_slice)
    no_tier_eval_frame = (
        pd.concat([no_tier_eval_frame_base, tier_b_filtered_out_frame], ignore_index=True, sort=False)
        if not tier_b_filtered_out_frame.empty
        else no_tier_eval_frame_base
    )
    if tier_a_eval_frame.empty:
        raise RuntimeError(f"Tier A evaluation frame is empty for session slice: {session_slice_id}")
    route_coverage = build_eval_route_coverage_summary(
        base_summary=route_coverage,
        tier_a_eval_frame=tier_a_eval_frame,
        tier_b_eval_frame=tier_b_eval_frame,
        no_tier_eval_frame=no_tier_eval_frame,
        session_slice=session_slice,
        tier_b_filtered_out_frame=tier_b_filtered_out_frame,
        tier_b_allowed_subtypes=allowed_fallback_subtypes,
    )

    tier_a_predictions = build_prediction_frame(tier_a_model, tier_a_eval_frame, tier_a_feature_order, tier_a_rule)
    tier_b_predictions = build_prediction_frame(tier_b_model, tier_b_eval_frame, tier_b_feature_order, tier_b_rule)
    tier_a_predictions[tier_column] = TIER_A
    tier_b_predictions[tier_column] = TIER_B
    tier_a_predictions["feature_count"] = len(tier_a_feature_order)
    tier_b_predictions["feature_count"] = len(tier_b_feature_order)
    tier_a_predictions["feature_order_hash"] = tier_a_feature_hash
    tier_b_predictions["feature_order_hash"] = tier_b_feature_hash
    predictions = pd.concat([tier_a_predictions, tier_b_predictions], ignore_index=True)
    _io_path(predictions_root).mkdir(parents=True, exist_ok=True)
    tier_a_predictions.to_parquet(_io_path(tier_a_predictions_path), index=False)
    tier_b_predictions.to_parquet(_io_path(tier_b_predictions_path), index=False)
    no_tier_eval_frame.to_parquet(_io_path(no_tier_route_path), index=False)
    predictions.to_parquet(_io_path(combined_predictions_path), index=False)
    write_json(route_coverage_path, route_coverage)

    tier_views = build_tier_prediction_views(predictions, tier_column=tier_column)
    tier_outputs = materialize_tier_prediction_views(tier_views, predictions_root)
    tier_records = build_paired_tier_records(tier_views, base_path=predictions_root)

    _io_path(models_root).mkdir(parents=True, exist_ok=True)
    _io_path(tier_b_feature_order_path_run).write_text("\n".join(tier_b_feature_order) + "\n", encoding="utf-8")
    joblib.dump(tier_a_model, _io_path(tier_a_model_path))
    joblib.dump(tier_b_model, _io_path(tier_b_model_path))
    tier_a_onnx_export = export_sklearn_to_onnx_zipmap_disabled(
        tier_a_model, tier_a_onnx_path, feature_count=len(tier_a_feature_order)
    )
    tier_b_onnx_export = export_sklearn_to_onnx_zipmap_disabled(
        tier_b_model, tier_b_onnx_path, feature_count=len(tier_b_feature_order)
    )
    tier_a_parity_values = values_a[: max(1, min(parity_rows, len(values_a)))]
    tier_b_parity_values = values_b[: max(1, min(parity_rows, len(values_b)))]
    tier_a_onnx_parity = check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx_path, tier_a_parity_values)
    tier_b_onnx_parity = check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx_path, tier_b_parity_values)
    onnx_parity = {
        "passed": bool(tier_a_onnx_parity["passed"] and tier_b_onnx_parity["passed"]),
        "tier_a": tier_a_onnx_parity,
        "tier_b": tier_b_onnx_parity,
    }

    mt5_bundle = alpha_scout_runner.materialize_mt5_probe_bundle(
        run_output_root=run_output_root,
        common_files_root=common_files_root,
        terminal_data_root=terminal_data_root,
        tester_profile_root=tester_profile_root,
        mt5_root=mt5_root,
        tier_a_onnx_path=tier_a_onnx_path,
        tier_b_onnx_path=tier_b_onnx_path,
        tier_a_eval_frame=tier_a_eval_frame,
        tier_b_eval_frame=tier_b_eval_frame,
        tier_a_feature_order=tier_a_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        tier_a_feature_hash=tier_a_feature_hash,
        tier_b_feature_hash=tier_b_feature_hash,
        tier_a_rule=tier_a_rule,
        tier_b_rule=tier_b_rule,
        route_coverage=route_coverage,
        routed_fallback_enabled=routed_fallback_enabled,
        attempt_mt5=attempt_mt5,
        terminal_path=terminal_path,
        metaeditor_path=metaeditor_path,
        max_hold_bars=max_hold_bars,
        tier_a_only_prefix=MT5_RECORD_TIER_A_ONLY_PREFIX,
        tier_b_fallback_only_prefix=MT5_RECORD_TIER_B_FALLBACK_ONLY_PREFIX,
    )
    mt5_attempts = mt5_bundle["mt5_attempts"]
    common_copies = mt5_bundle["common_copies"]
    compile_payload = mt5_bundle["compile_payload"]
    mt5_execution_results = mt5_bundle["execution_results"]
    mt5_report_records = mt5_bundle["report_records"]
    mt5_kpi_records = mt5_bundle["kpi_records"]
    mt5_module_hashes = mt5_bundle["module_hashes"]

    return packet_writers.materialize_alpha_scout_run_outputs(
        run_id=RUN_ID,
        run_number=RUN_NUMBER,
        stage_id=STAGE_ID,
        exploration_label=EXPLORATION_LABEL,
        run_output_root=run_output_root,
        reports_root=reports_root,
        model_input_path=model_input_path,
        feature_order_path=feature_order_path,
        stage07_model_path=stage07_model_path,
        tier_b_model_input_path=tier_b_model_input_path,
        tier_b_feature_order_path=tier_b_feature_order_path,
        tier_a_model_path=tier_a_model_path,
        tier_b_model_path=tier_b_model_path,
        tier_a_predictions_path=tier_a_predictions_path,
        tier_b_predictions_path=tier_b_predictions_path,
        no_tier_route_path=no_tier_route_path,
        route_coverage_path=route_coverage_path,
        combined_predictions_path=combined_predictions_path,
        tier_b_feature_order_path_run=tier_b_feature_order_path_run,
        threshold_sweep_path=threshold_sweep_path,
        threshold_sweep_paths=threshold_sweep_paths,
        tier_a_onnx_export=tier_a_onnx_export,
        tier_b_onnx_export=tier_b_onnx_export,
        tier_outputs=tier_outputs,
        model_input_dataset_id=MODEL_INPUT_DATASET_ID,
        feature_set_id=FEATURE_SET_ID,
        tier_b_model_input_dataset_id=TIER_B_MODEL_INPUT_DATASET_ID,
        tier_b_feature_set_id=TIER_B_FEATURE_SET_ID,
        tier_b_partial_context_dataset_id=TIER_B_PARTIAL_CONTEXT_DATASET_ID,
        tier_b_partial_context_feature_set_id=TIER_B_PARTIAL_CONTEXT_FEATURE_SET_ID,
        tier_b_partial_context_policy_id=TIER_B_PARTIAL_CONTEXT_POLICY_ID,
        tier_a_feature_order=tier_a_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        tier_a_feature_hash=tier_a_feature_hash,
        tier_b_feature_hash=tier_b_feature_hash,
        route_coverage=route_coverage,
        threshold_selection=threshold_selection,
        threshold_sweep=threshold_sweep,
        threshold_sweeps=threshold_sweeps,
        tier_records=tier_records,
        onnx_parity=onnx_parity,
        mt5_attempts=mt5_attempts,
        common_copies=common_copies,
        mt5_report_records=mt5_report_records,
        mt5_kpi_records=mt5_kpi_records,
        mt5_module_hashes=mt5_module_hashes,
        compile_payload=compile_payload,
        mt5_execution_results=mt5_execution_results,
        attempt_mt5=attempt_mt5,
        max_hold_bars=max_hold_bars,
        routed_fallback_enabled=routed_fallback_enabled,
        routing_mode=routing_mode,
        routing_detail=routing_detail,
        allowed_fallback_subtypes=allowed_fallback_subtypes,
        session_slice_id=session_slice_id,
        tier_a_predictions_count=len(tier_a_predictions),
        tier_b_predictions_count=len(tier_b_predictions),
        no_tier_eval_count=len(no_tier_eval_frame),
        tier_a_rule=tier_a_rule,
        tier_b_rule=tier_b_rule,
        stage_run_ledger_path=STAGE_RUN_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_ALPHA_LEDGER_PATH,
        run_registry_path=RUN_REGISTRY_PATH,
        tier_a_only_prefix=MT5_RECORD_TIER_A_ONLY_PREFIX,
        tier_b_fallback_only_prefix=MT5_RECORD_TIER_B_FALLBACK_ONLY_PREFIX,
    )

def threshold_rule_from_cli(
    *,
    label: str,
    threshold_id: str | None,
    short_threshold: float | None,
    long_threshold: float | None,
    min_margin: float | None,
) -> ThresholdRule | None:
    values = (short_threshold, long_threshold, min_margin)
    if all(value is None for value in values):
        return None
    if any(value is None for value in values):
        raise ValueError(f"{label} threshold override requires short, long, and min-margin values.")
    return threshold_rule_from_values(
        threshold_id=threshold_id,
        short_threshold=float(short_threshold),
        long_threshold=float(long_threshold),
        min_margin=float(min_margin),
    )


def main() -> int:
    args = parse_args()
    configure_run_identity(
        run_number=args.run_number,
        run_id=args.run_id,
        exploration_label=args.exploration_label,
        common_run_root=args.common_run_root or default_common_run_root(args.run_id),
    )
    run_output_root = (
        Path(args.run_output_root)
        if args.run_output_root
        else Path("stages") / STAGE_ID / "02_runs" / args.run_id
    )
    tier_a_rule = threshold_rule_from_cli(
        label="Tier A",
        threshold_id=args.tier_a_threshold_id,
        short_threshold=args.tier_a_short_threshold,
        long_threshold=args.tier_a_long_threshold,
        min_margin=args.tier_a_min_margin,
    )
    tier_b_rule = threshold_rule_from_cli(
        label="Tier B",
        threshold_id=args.tier_b_threshold_id,
        short_threshold=args.tier_b_short_threshold,
        long_threshold=args.tier_b_long_threshold,
        min_margin=args.tier_b_min_margin,
    )
    payload = run_stage10_logreg_mt5_scout(
        model_input_path=Path(args.model_input_path),
        feature_order_path=Path(args.feature_order_path),
        tier_b_model_input_path=Path(args.tier_b_model_input_path),
        tier_b_feature_order_path=Path(args.tier_b_feature_order_path),
        raw_root=Path(args.raw_root),
        training_summary_path=Path(args.training_summary_path),
        stage07_model_path=Path(args.stage07_model_path),
        run_output_root=run_output_root,
        common_files_root=Path(args.common_files_root),
        terminal_data_root=Path(args.terminal_data_root),
        tester_profile_root=Path(args.tester_profile_root),
        tier_column=args.tier_column,
        random_seed=args.random_seed,
        max_iter=args.max_iter,
        parity_rows=args.parity_rows,
        max_hold_bars=args.max_hold_bars,
        tier_a_threshold_rule=tier_a_rule,
        tier_b_threshold_rule=tier_b_rule,
        routed_fallback_enabled=not args.disable_routed_fallback,
        session_slice_id=args.session_slice_id,
        tier_b_fallback_allowed_subtypes=parse_tier_b_fallback_allowed_subtypes(
            args.tier_b_fallback_allowed_subtypes
        ),
        attempt_mt5=args.attempt_mt5,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
    )
    print(json.dumps(_json_ready(payload), indent=2))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
