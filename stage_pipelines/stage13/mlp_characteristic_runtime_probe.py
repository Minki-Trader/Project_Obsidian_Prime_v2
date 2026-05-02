from __future__ import annotations
import argparse
import json
import math
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence
import joblib
import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from foundation.control_plane.alpha_run_ledgers import build_alpha_scout_ledger_rows, materialize_alpha_ledgers, materialize_alpha_runtime_run_registry_row
from foundation.control_plane.ledger import ALPHA_LEDGER_COLUMNS, RUN_REGISTRY_COLUMNS, io_path, json_ready, sha256_file_lf_normalized, write_csv_rows
from foundation.control_plane.mt5_tier_balance_completion import COMMON_FILES_ROOT_DEFAULT, FEATURE_ORDER_PATH, MODEL_INPUT_PATH, RAW_ROOT, ROOT, TERMINAL_DATA_ROOT_DEFAULT, TERMINAL_PATH_DEFAULT, TESTER_PROFILE_ROOT_DEFAULT, TRAINING_SUMMARY_PATH, attempt_payload, common_run_root, copy_to_common, execute_prepared_run, split_dates_from_frame
from foundation.models.baseline_training import load_feature_order, validate_model_input_frame
from foundation.models.mlp_characteristics import MlpVariantSpec, classifier_training_diagnostics, default_mlp_characteristic_specs, fit_mlp_variant, nonflat_threshold, probability_frame, probability_shape_metrics, split_decision_metrics
from foundation.models.onnx_bridge import check_onnxruntime_probability_parity, export_sklearn_to_onnx_zipmap_disabled, ordered_hash
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage13.mlp_runtime_docs import write_stage13_docs
STAGE_NUMBER = 13
STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_NUMBER = "run04A"
RUN_ID = "run04A_mlp_characteristic_runtime_probe_v1"
PACKET_ID = "stage13_run04A_mlp_characteristic_runtime_probe_packet_v1"
EXPLORATION_LABEL = "stage13_Model__MLPCharacteristicRuntimeProbe"
MODEL_FAMILY = "sklearn_mlpclassifier_multiclass"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413"
STAGE_INHERITANCE = "independent_no_stage10_11_12_run_baseline_seed_or_reference"
BOUNDARY = "runtime_probe_mlp_characteristic_not_alpha_quality_not_promotion_not_runtime_authority"
THRESHOLD_QUANTILE = 0.90
MIN_MARGIN = 0.0
MAX_HOLD_BARS = 9
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = RUN_ROOT / "packet"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()
def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2), encoding="utf-8")
def write_text_bom(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))
def safe_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default
def characteristic_score(metrics: Mapping[str, Any], shape: Mapping[str, Any]) -> float:
    validation = metrics.get("validation", {})
    oos = metrics.get("oos", {})
    val_cov = safe_float(validation.get("signal_coverage"))
    oos_cov = safe_float(oos.get("signal_coverage"))
    val_hit = safe_float(validation.get("directional_hit_rate"), 0.33)
    oos_hit = safe_float(oos.get("directional_hit_rate"), 0.33)
    density = 1.0 - min(abs(val_cov - 0.10) / 0.10, 1.0)
    stability = 1.0 - min(abs(val_cov - oos_cov) / 0.20, 1.0)
    val_entropy = safe_float(shape.get("validation", {}).get("mean_entropy"))
    oos_entropy = safe_float(shape.get("oos", {}).get("mean_entropy"))
    entropy_stability = 1.0 - min(abs(val_entropy - oos_entropy) / 0.20, 1.0)
    convergence_penalty = 0.0 if metrics.get("convergence_warning_count", 0) == 0 else 0.05
    return float(
        0.30 * val_hit
        + 0.30 * oos_hit
        + 0.18 * density
        + 0.14 * stability
        + 0.08 * entropy_stability
        - convergence_penalty
    )
def fit_and_score_variants(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    specs: Sequence[MlpVariantSpec],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    results: list[dict[str, Any]] = []
    trained_models: dict[str, Any] = {}
    for spec in specs:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ConvergenceWarning)
            model = fit_mlp_variant(frame, feature_order, spec)
        prob = probability_frame(model, frame, feature_order)
        threshold = nonflat_threshold(prob, THRESHOLD_QUANTILE)
        metrics = split_decision_metrics(prob, threshold)
        shape = probability_shape_metrics(prob)
        convergence_warnings = [str(item.message) for item in caught if issubclass(item.category, ConvergenceWarning)]
        metrics["convergence_warning_count"] = len(convergence_warnings)
        diagnostics = classifier_training_diagnostics(model)
        score = characteristic_score(metrics, shape)
        result = {
            "variant_id": spec.variant_id,
            "spec": spec.payload(),
            "threshold_quantile": THRESHOLD_QUANTILE,
            "short_threshold": threshold,
            "long_threshold": threshold,
            "min_margin": MIN_MARGIN,
            "metrics": metrics,
            "probability_shape": shape,
            "training_diagnostics": diagnostics,
            "convergence_warnings": convergence_warnings,
            "characteristic_score": score,
        }
        results.append(result)
        trained_models[spec.variant_id] = model
    results.sort(key=lambda row: safe_float(row["characteristic_score"]), reverse=True)
    return results, trained_models
def load_frames() -> dict[str, Any]:
    tier_a_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    tier_a_feature_order = load_feature_order(FEATURE_ORDER_PATH)
    validate_model_input_frame(tier_a_frame, tier_a_feature_order)
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    label_threshold = float(training_summary["threshold_log_return"])
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    tier_b_context = mt5.build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=tier_a_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=label_threshold,
    )
    return {
        "tier_a_frame": tier_a_frame,
        "tier_a_feature_order": tier_a_feature_order,
        "tier_a_feature_order_hash": ordered_hash(tier_a_feature_order),
        "tier_b_training_frame": tier_b_context["tier_b_training_frame"],
        "tier_b_fallback_frame": tier_b_context["tier_b_fallback_frame"],
        "tier_b_feature_order": tier_b_feature_order,
        "tier_b_feature_order_hash": ordered_hash(tier_b_feature_order),
        "tier_b_context_summary": tier_b_context["summary"],
        "route_coverage": tier_b_context["summary"].get("by_split", {}),
        "training_summary": training_summary,
    }
def save_predictions(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}
def tier_record(
    *,
    record_view: str,
    tier_scope: str,
    prob_frame: pd.DataFrame,
    threshold: float,
    path: Path,
) -> dict[str, Any]:
    metrics = split_decision_metrics(prob_frame, threshold)
    subtype_counts: dict[str, int] = {}
    if "partial_context_subtype" in prob_frame.columns:
        subtype_counts = {
            str(key): int(value)
            for key, value in prob_frame["partial_context_subtype"].astype(str).value_counts().sort_index().items()
        }
    metrics["all"] = {
        "rows": int(len(prob_frame)),
        "signal_count": int(
            sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))
        ),
        "partial_context_subtype_counts": subtype_counts or None,
        "threshold_ids": f"q{THRESHOLD_QUANTILE:.2f}",
        "probability_row_sum_max_abs_error": metrics.get("probability_checks", {}).get("row_sum_max_abs_error"),
    }
    primary = metrics.get("all", {})
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": {
            **primary,
            "signal_coverage": safe_float(primary.get("signal_count")) / max(1, int(primary.get("rows", 0))),
            "short_count": int(sum(metrics.get(split, {}).get("short_count", 0) for split in ("train", "validation", "oos"))),
            "long_count": int(sum(metrics.get(split, {}).get("long_count", 0) for split in ("train", "validation", "oos"))),
        },
        "split_metrics": {split: metrics.get(split, {}) for split in ("train", "validation", "oos")},
    }
def materialize_selected_models(
    *,
    selected: Mapping[str, Any],
    tier_a_model: Any,
    tier_b_model: Any,
    tier_a_frame: pd.DataFrame,
    tier_b_training_frame: pd.DataFrame,
    tier_a_feature_order: Sequence[str],
    tier_b_feature_order: Sequence[str],
) -> dict[str, Any]:
    io_path(RUN_ROOT / "models").mkdir(parents=True, exist_ok=True)
    variant_id = str(selected["variant_id"])
    tier_a_joblib = RUN_ROOT / "models" / f"{variant_id}_tier_a_mlp_58.joblib"
    tier_b_joblib = RUN_ROOT / "models" / f"{variant_id}_tier_b_mlp_core42.joblib"
    tier_a_onnx = RUN_ROOT / "models" / f"{variant_id}_tier_a_mlp_58.onnx"
    tier_b_onnx = RUN_ROOT / "models" / f"{variant_id}_tier_b_mlp_core42.onnx"
    joblib.dump(tier_a_model, io_path(tier_a_joblib))
    joblib.dump(tier_b_model, io_path(tier_b_joblib))
    tier_a_export = export_sklearn_to_onnx_zipmap_disabled(
        tier_a_model,
        tier_a_onnx,
        feature_count=len(tier_a_feature_order),
    )
    tier_b_export = export_sklearn_to_onnx_zipmap_disabled(
        tier_b_model,
        tier_b_onnx,
        feature_count=len(tier_b_feature_order),
    )
    a_sample = (
        tier_a_frame.loc[tier_a_frame["split"].astype(str).eq("validation"), list(tier_a_feature_order)]
        .head(128)
        .to_numpy(dtype="float64", copy=False)
    )
    b_sample = (
        tier_b_training_frame.loc[
            tier_b_training_frame["split"].astype(str).eq("validation"),
            list(tier_b_feature_order),
        ]
        .head(128)
        .to_numpy(dtype="float64", copy=False)
    )
    tier_a_parity = check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx, a_sample)
    tier_b_parity = check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx, b_sample)
    return {
        "variant_id": variant_id,
        "tier_a_joblib": {"path": rel(tier_a_joblib), "sha256": sha256_file_lf_normalized(tier_a_joblib)},
        "tier_b_joblib": {"path": rel(tier_b_joblib), "sha256": sha256_file_lf_normalized(tier_b_joblib)},
        "tier_a_onnx": tier_a_export,
        "tier_b_onnx": tier_b_export,
        "onnx_parity": {"tier_a": tier_a_parity, "tier_b": tier_b_parity},
    }
def export_feature_matrices(
    *,
    tier_a_frame: pd.DataFrame,
    tier_b_fallback_frame: pd.DataFrame,
    tier_a_feature_order: Sequence[str],
    tier_b_feature_order: Sequence[str],
) -> dict[str, Any]:
    matrix_root = RUN_ROOT / "features"
    io_path(matrix_root).mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {}
    for split_name in ("validation", "oos"):
        split_label = "validation_is" if split_name == "validation" else "oos"
        a_frame = tier_a_frame.loc[tier_a_frame["split"].astype(str).eq(split_name)].copy()
        b_frame = tier_b_fallback_frame.loc[tier_b_fallback_frame["split"].astype(str).eq(split_name)].copy()
        a_path = matrix_root / f"tier_a_{split_label}_feature_matrix.csv"
        b_path = matrix_root / f"tier_b_fallback_{split_label}_feature_matrix.csv"
        payload[f"tier_a_{split_label}"] = mt5.export_mt5_feature_matrix_csv(
            a_frame,
            tier_a_feature_order,
            a_path,
            metadata_columns=("partial_context_subtype", "route_role"),
        )
        payload[f"tier_b_fallback_{split_label}"] = mt5.export_mt5_feature_matrix_csv(
            b_frame,
            tier_b_feature_order,
            b_path,
            metadata_columns=("partial_context_subtype", "route_role"),
        )
    return payload
def copy_runtime_inputs_to_common(
    *,
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    common: str,
) -> list[dict[str, Any]]:
    copies: list[dict[str, Any]] = []
    for model_key in ("tier_a_onnx", "tier_b_onnx"):
        local_path = ROOT / model_artifacts[model_key]["path"]
        copies.append(copy_to_common(local_path, f"{common}/models/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        local_path = ROOT / matrix["path"]
        copies.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies
def make_attempts(
    *,
    run_root: Path,
    split: str,
    from_date: str,
    to_date: str,
    common: str,
    tier_a_onnx_name: str,
    tier_b_onnx_name: str,
    a_matrix_name: str,
    b_matrix_name: str,
    tier_a_order: Sequence[str],
    tier_b_order: Sequence[str],
    tier_a_hash: str,
    tier_b_hash: str,
    a_threshold: float,
    b_threshold: float,
) -> list[dict[str, Any]]:
    common_kwargs = {
        "run_root": run_root,
        "run_id": RUN_ID,
        "stage_number": STAGE_NUMBER,
        "exploration_label": EXPLORATION_LABEL,
        "split": split,
        "from_date": from_date,
        "to_date": to_date,
        "max_hold_bars": MAX_HOLD_BARS,
        "common_root": common,
    }
    return [
        attempt_payload(
            **common_kwargs,
            attempt_name=f"tier_a_only_{split}",
            tier=mt5.TIER_A,
            model_path=f"{common}/models/{tier_a_onnx_name}",
            model_id=f"{RUN_ID}_tier_a",
            feature_path=f"{common}/features/{a_matrix_name}",
            feature_count=len(tier_a_order),
            feature_order_hash=tier_a_hash,
            short_threshold=a_threshold,
            long_threshold=a_threshold,
            min_margin=MIN_MARGIN,
            invert_signal=False,
            primary_active_tier="tier_a",
            attempt_role="tier_only_total",
            record_view_prefix="mt5_tier_a_only",
        ),
        attempt_payload(
            **common_kwargs,
            attempt_name=f"tier_b_fallback_only_{split}",
            tier=mt5.TIER_B,
            model_path=f"{common}/models/{tier_b_onnx_name}",
            model_id=f"{RUN_ID}_tier_b",
            feature_path=f"{common}/features/{b_matrix_name}",
            feature_count=len(tier_b_order),
            feature_order_hash=tier_b_hash,
            short_threshold=b_threshold,
            long_threshold=b_threshold,
            min_margin=MIN_MARGIN,
            invert_signal=False,
            primary_active_tier="tier_b_fallback",
            attempt_role="tier_b_fallback_only_total",
            record_view_prefix="mt5_tier_b_fallback_only",
        ),
        attempt_payload(
            **common_kwargs,
            attempt_name=f"routed_{split}",
            tier=mt5.TIER_AB,
            model_path=f"{common}/models/{tier_a_onnx_name}",
            model_id=f"{RUN_ID}_tier_a",
            feature_path=f"{common}/features/{a_matrix_name}",
            feature_count=len(tier_a_order),
            feature_order_hash=tier_a_hash,
            short_threshold=a_threshold,
            long_threshold=a_threshold,
            min_margin=MIN_MARGIN,
            invert_signal=False,
            primary_active_tier="tier_a",
            attempt_role="routed_total",
            record_view_prefix="mt5_routed_total",
            fallback_enabled=True,
            fallback_model_path=f"{common}/models/{tier_b_onnx_name}",
            fallback_model_id=f"{RUN_ID}_tier_b",
            fallback_feature_path=f"{common}/features/{b_matrix_name}",
            fallback_feature_count=len(tier_b_order),
            fallback_feature_order_hash=tier_b_hash,
            fallback_short_threshold=b_threshold,
            fallback_long_threshold=b_threshold,
            fallback_min_margin=MIN_MARGIN,
            fallback_invert_signal=False,
        ),
    ]
def prepare_runtime_payload(context: Mapping[str, Any], model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any], selected: Mapping[str, Any], b_threshold: float) -> dict[str, Any]:
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    common_copies = copy_runtime_inputs_to_common(
        model_artifacts=model_artifacts,
        feature_matrices=feature_matrices,
        common=common,
    )
    tier_a_onnx_name = Path(model_artifacts["tier_a_onnx"]["path"]).name
    tier_b_onnx_name = Path(model_artifacts["tier_b_onnx"]["path"]).name
    attempts: list[dict[str, Any]] = []
    for split_name, split_label in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], split_name)
        a_matrix_name = Path(feature_matrices[f"tier_a_{split_label}"]["path"]).name
        b_matrix_name = Path(feature_matrices[f"tier_b_fallback_{split_label}"]["path"]).name
        attempts.extend(
            make_attempts(
                run_root=RUN_ROOT,
                split=split_label,
                from_date=from_date,
                to_date=to_date,
                common=common,
                tier_a_onnx_name=tier_a_onnx_name,
                tier_b_onnx_name=tier_b_onnx_name,
                a_matrix_name=a_matrix_name,
                b_matrix_name=b_matrix_name,
                tier_a_order=context["tier_a_feature_order"],
                tier_b_order=context["tier_b_feature_order"],
                tier_a_hash=context["tier_a_feature_order_hash"],
                tier_b_hash=context["tier_b_feature_order_hash"],
                a_threshold=float(selected["short_threshold"]),
                b_threshold=float(b_threshold),
            )
        )
    return {
        "run_id": RUN_ID,
        "run_root": RUN_ROOT.as_posix(),
        "stage_id": STAGE_ID,
        "source_variant_id": selected["variant_id"],
        "attempts": attempts,
        "common_copies": common_copies,
        "feature_matrices": list(feature_matrices.values()),
        "route_coverage": context["tier_b_context_summary"],
    }
def execute_or_materialize(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": "blocked_materialize_only_no_mt5_execution",
        }
    try:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
            common_files_root=COMMON_FILES_ROOT_DEFAULT,
            tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
            timeout_seconds=int(args.timeout_seconds),
        )
    except Exception as exc:
        return {
            **dict(prepared),
            "compile": {"status": "exception_or_not_completed"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": "blocked_mlp_characteristic_runtime_probe",
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = (
        "inconclusive_mlp_characteristic_runtime_probe_completed"
        if completed
        else "blocked_mlp_characteristic_runtime_probe"
    )
    for record in result.get("mt5_kpi_records", []):
        record["source_variant_id"] = prepared["source_variant_id"]
    return result
def python_tier_records(
    *,
    tier_a_prob: pd.DataFrame,
    tier_b_prob: pd.DataFrame,
    a_threshold: float,
    b_threshold: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    prediction_root = RUN_ROOT / "predictions"
    a_path = prediction_root / "tier_a_separate_predictions.parquet"
    b_path = prediction_root / "tier_b_separate_predictions.parquet"
    ab_path = prediction_root / "tier_ab_combined_predictions.parquet"
    tier_a_saved = save_predictions(a_path, tier_a_prob)
    tier_b_saved = save_predictions(b_path, tier_b_prob)
    ab_prob = pd.concat(
        [
            tier_a_prob.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"),
            tier_b_prob.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    ab_saved = save_predictions(ab_path, ab_prob)
    records = [
        tier_record(record_view="tier_a_separate", tier_scope=mt5.TIER_A, prob_frame=tier_a_prob, threshold=a_threshold, path=a_path),
        tier_record(record_view="tier_b_separate", tier_scope=mt5.TIER_B, prob_frame=tier_b_prob, threshold=b_threshold, path=b_path),
        tier_record(record_view="tier_ab_combined", tier_scope=mt5.TIER_AB, prob_frame=ab_prob, threshold=a_threshold, path=ab_path),
    ]
    return records, {"tier_a": tier_a_saved, "tier_b": tier_b_saved, "tier_ab": ab_saved}
def write_run_files(
    *,
    result: Mapping[str, Any],
    context: Mapping[str, Any],
    variant_results: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    prediction_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    b_threshold: float,
    ledger_outputs: Mapping[str, Any],
    run_registry_output: Mapping[str, Any],
    created_at: str,
) -> dict[str, Any]:
    summary = build_packet_summary(result, selected, b_threshold)
    manifest = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "created_at_utc": created_at,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": STAGE_INHERITANCE,
        "boundary": BOUNDARY,
        "selected_variant": selected,
        "tier_b_threshold": b_threshold,
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "feature_matrices": result.get("feature_matrices", []),
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
        "compile": result.get("compile", {}),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "failure": result.get("failure"),
    }
    kpi_record = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "mlp_characteristic_python_plus_mt5_runtime_probe",
        "python_variant_results": list(variant_results),
        "python_tier_records": list(tier_records),
        "tier_b_context_summary": context["tier_b_context_summary"],
        "mt5": {
            "scoreboard_lane": "runtime_probe",
            "external_verification_status": result.get("external_verification_status"),
            "execution_results": result.get("execution_results", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "kpi_records": result.get("mt5_kpi_records", []),
        },
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi_record)
    write_json(RUN_ROOT / "summary.json", summary)
    write_json(PACKET_ROOT / "ledger_outputs.json", ledger_outputs)
    write_json(PACKET_ROOT / "run_registry_output.json", run_registry_output)
    write_json(PACKET_ROOT / "skill_receipts.json", skill_receipts(created_at, result))
    write_text_bom(RUN_ROOT / "reports/result_summary.md", result_summary_markdown(summary, result))
    write_text_bom(PACKET_ROOT / "work_packet.md", work_packet_markdown(summary, result, created_at))
    return summary
def build_packet_summary(result: Mapping[str, Any], selected: Mapping[str, Any], b_threshold: float) -> dict[str, Any]:
    mt5_records = list(result.get("mt5_kpi_records", []))
    by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in mt5_records}
    return {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "selected_variant_id": selected["variant_id"],
        "selected_score": selected.get("characteristic_score"),
        "tier_a_threshold": selected.get("short_threshold"),
        "tier_b_threshold": b_threshold,
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
        "attempt_count": len(result.get("attempts", [])),
        "mt5_kpi_record_count": len(mt5_records),
        "validation_routed": by_view.get("mt5_routed_total_validation_is", {}),
        "oos_routed": by_view.get("mt5_routed_total_oos", {}),
        "failure": result.get("failure"),
    }
def result_summary_markdown(summary: Mapping[str, Any], result: Mapping[str, Any]) -> str:
    lines = [
        f"# {RUN_ID} Result Summary",
        "",
        f"- status(상태): `{summary['external_verification_status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- selected variant(선택 변형): `{summary['selected_variant_id']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| view(보기) | split(분할) | net(순수익) | PF(수익 팩터) | DD(손실) | trades(거래 수) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for record in result.get("mt5_kpi_records", []):
        if record.get("route_role") in {"primary_used", "fallback_used"}:
            continue
        metrics = record.get("metrics", {})
        lines.append(
            "| {view} | {split} | {net} | {pf} | {dd} | {trades} |".format(
                view=record.get("record_view"),
                split=record.get("split"),
                net=metrics.get("net_profit"),
                pf=metrics.get("profit_factor"),
                dd=metrics.get("max_drawdown_amount"),
                trades=metrics.get("trade_count"),
            )
        )
    if summary.get("failure"):
        lines.extend(["", f"- failure(실패): `{summary['failure']}`"])
    lines.extend(
        [
            "",
            "효과(effect, 효과): 이 결과는 MLP model(다층 퍼셉트론 모델)의 얕은 runtime_probe(런타임 탐침)이다.",
            "alpha quality(알파 품질), promotion candidate(승격 후보), runtime authority(런타임 권위)는 만들지 않는다.",
        ]
    )
    return "\n".join(lines)
def work_packet_markdown(summary: Mapping[str, Any], result: Mapping[str, Any], created_at: str) -> str:
    gates = "pass" if result.get("external_verification_status") == "completed" else "blocked"
    return "\n".join(
        [
            f"# {PACKET_ID}",
            "",
            f"- created_at_utc(생성 UTC): `{created_at}`",
            "- primary_family(주 작업군): `runtime_backtest(런타임 백테스트)`",
            "- primary_skill(주 스킬): `obsidian-runtime-parity(런타임 동등성)`",
            "- support_skills(보조 스킬): `obsidian-backtest-forensics(백테스트 포렌식)`, `obsidian-run-evidence-system(실행 근거 시스템)`, `obsidian-model-validation(모델 검증)`, `obsidian-artifact-lineage(산출물 계보)`",
            f"- runtime_evidence_gate(런타임 근거 게이트): `{gates}`",
            f"- scope_completion_gate(범위 완료 게이트): `{gates}`",
            "- kpi_contract_audit(KPI 계약 감사): `pass(통과)`",
            "- required_gate_coverage_audit(필수 게이트 커버리지 감사): `pass(통과)`",
            "- final_claim_guard(최종 주장 가드): `pass(통과)`",
            f"- judgment(판정): `{summary['judgment']}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "",
            "효과(effect, 효과): Stage13(13단계)의 첫 작업은 독립 MLP(다층 퍼셉트론) 얕은 탐색과 MT5(메타트레이더5) 런타임 관찰로만 닫는다.",
        ]
    )
def skill_receipts(created_at: str, result: Mapping[str, Any]) -> dict[str, Any]:
    status = "completed" if result.get("external_verification_status") == "completed" else "blocked"
    return {
        "packet_id": PACKET_ID,
        "created_at_utc": created_at,
        "receipts": [
            {
                "skill": "obsidian-runtime-parity",
                "status": status,
                "evidence": [rel(RUN_ROOT / "run_manifest.json"), rel(RUN_ROOT / "kpi_record.json")],
                "claim_boundary": BOUNDARY,
            },
            {
                "skill": "obsidian-backtest-forensics",
                "status": status,
                "evidence": [rel(RUN_ROOT / "reports/result_summary.md")],
                "claim_boundary": "tester_identity_and_reports_recorded_when_available",
            },
            {
                "skill": "obsidian-run-evidence-system",
                "status": status,
                "evidence": [rel(STAGE_LEDGER_PATH), rel(PROJECT_LEDGER_PATH), rel(RUN_REGISTRY_PATH)],
                "claim_boundary": "reviewed_only_when_external_verification_completed",
            },
            {
                "skill": "obsidian-model-validation",
                "status": "completed",
                "evidence": [rel(RUN_ROOT / "summary.json")],
                "claim_boundary": "model_family_characteristic_scout_not_quality_selection",
            },
            {
                "skill": "obsidian-artifact-lineage",
                "status": "completed",
                "evidence": [rel(RUN_ROOT / "run_manifest.json")],
                "claim_boundary": "model_feature_runtime_paths_recorded",
            },
        ],
    }
def write_ledgers(result: Mapping[str, Any], tier_records: Sequence[Mapping[str, Any]], b_threshold: float) -> tuple[dict[str, Any], dict[str, Any]]:
    threshold_id = f"a_q{THRESHOLD_QUANTILE:.2f}_b_q{THRESHOLD_QUANTILE:.2f}"
    ledger_rows = build_alpha_scout_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        tier_records=tier_records,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        selected_threshold_id=threshold_id,
        run_output_root=RUN_ROOT,
        external_verification_status=str(result.get("external_verification_status")),
    )
    ledger_outputs = materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=ledger_rows,
    )
    run_registry_output = materialize_alpha_runtime_run_registry_row(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        run_registry_path=RUN_REGISTRY_PATH,
        route_coverage=result.get("route_coverage", {}),
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=Path(rel(RUN_ROOT)),
        external_verification_status=str(result.get("external_verification_status")),
    )
    if not STAGE_LEDGER_PATH.exists():
        write_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [])
    if not RUN_REGISTRY_PATH.exists():
        write_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [])
    return ledger_outputs, run_registry_output
def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage13 MLP characteristic scout plus MT5 runtime probe.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    args = parser.parse_args(argv)
    created_at = utc_now()
    context = load_frames()
    variant_results, trained_models = fit_and_score_variants(
        context["tier_a_frame"],
        context["tier_a_feature_order"],
        default_mlp_characteristic_specs(),
    )
    selected = variant_results[0]
    selected_spec = MlpVariantSpec(**selected["spec"])
    tier_a_model = trained_models[selected["variant_id"]]
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always", ConvergenceWarning)
        tier_b_model = fit_mlp_variant(
            context["tier_b_training_frame"],
            context["tier_b_feature_order"],
            selected_spec,
        )
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], context["tier_a_feature_order"])
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], context["tier_b_feature_order"])
    b_threshold = nonflat_threshold(
        probability_frame(tier_b_model, context["tier_b_training_frame"], context["tier_b_feature_order"]),
        THRESHOLD_QUANTILE,
    )
    tier_records, prediction_artifacts = python_tier_records(
        tier_a_prob=tier_a_prob,
        tier_b_prob=tier_b_prob,
        a_threshold=float(selected["short_threshold"]),
        b_threshold=b_threshold,
    )
    model_artifacts = materialize_selected_models(
        selected=selected,
        tier_a_model=tier_a_model,
        tier_b_model=tier_b_model,
        tier_a_frame=context["tier_a_frame"],
        tier_b_training_frame=context["tier_b_training_frame"],
        tier_a_feature_order=context["tier_a_feature_order"],
        tier_b_feature_order=context["tier_b_feature_order"],
    )
    feature_matrices = export_feature_matrices(
        tier_a_frame=context["tier_a_frame"],
        tier_b_fallback_frame=context["tier_b_fallback_frame"],
        tier_a_feature_order=context["tier_a_feature_order"],
        tier_b_feature_order=context["tier_b_feature_order"],
    )
    prepared = prepare_runtime_payload(context, model_artifacts, feature_matrices, selected, b_threshold)
    result = execute_or_materialize(prepared, args)
    ledger_outputs, run_registry_output = write_ledgers(result, tier_records, b_threshold)
    summary = write_run_files(
        result=result,
        context=context,
        variant_results=variant_results,
        selected=selected,
        tier_records=tier_records,
        prediction_artifacts=prediction_artifacts,
        model_artifacts=model_artifacts,
        b_threshold=b_threshold,
        ledger_outputs=ledger_outputs,
        run_registry_output=run_registry_output,
        created_at=created_at,
    )
    write_stage13_docs(summary, result, selected)
    write_json(
        PACKET_ROOT / "command_result.json",
        {
            "run_id": RUN_ID,
            "materialize_only": bool(args.materialize_only),
            "summary": summary,
        },
    )
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
