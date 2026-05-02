from __future__ import annotations

import argparse
import csv
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import pandas as pd

from foundation.control_plane.alpha_run_ledgers import (
    build_alpha_scout_ledger_rows,
    materialize_alpha_ledgers,
    materialize_alpha_runtime_run_registry_row,
)
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    io_path,
    json_ready,
    sha256_file_lf_normalized,
    write_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    FEATURE_ORDER_PATH,
    MODEL_INPUT_PATH,
    RAW_ROOT,
    ROOT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    TRAINING_SUMMARY_PATH,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.models.baseline_training import load_feature_order, validate_model_input_frame
from foundation.models.lda_discriminant import (
    LdaRunSpec,
    classifier_training_diagnostics,
    default_stage15_lda_specs,
    fit_lda_variant,
    nonflat_threshold,
    probability_frame,
    probability_shape_metrics,
    shape_score,
    split_decision_metrics,
)
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
)
from foundation.mt5 import runtime_support as mt5


STAGE_NUMBER = 15
STAGE_ID = "15_model_family_challenge__untried_learning_methods_scout"
PACKET_ID = "stage15_lda_run06A_run06J_runtime_probe_v1"
EXPLORATION_LABEL = "stage15_Model__LDADiscriminantLearning"
MODEL_FAMILY = "sklearn_lda_discriminant_family"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
STAGE_INHERITANCE = "independent_no_stage10_11_12_13_14_baseline_seed_or_reference"
BOUNDARY = "lda_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_lda_discriminant_runtime_probe_completed"
JUDGMENT_BLOCKED = "blocked_lda_discriminant_runtime_probe_after_attempt"
THRESHOLD_QUANTILE = 0.90
ONNX_PARITY_TOLERANCE = 0.005
MIN_MARGIN = 0.0
MAX_HOLD_BARS = 12
ROWS_PER_CLASS = 600

STAGE_ROOT = ROOT / "stages" / STAGE_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets/stage15_lda_run06A_run06J_runtime_probe_v1"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REVIEW_PACKET_PATH = STAGE_ROOT / "03_reviews/run06A_run06J_lda_runtime_probe_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage15_lda_run06A_run06J_runtime_probe.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def load_context() -> dict[str, Any]:
    tier_a_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    tier_a_feature_order = load_feature_order(FEATURE_ORDER_PATH)
    validate_model_input_frame(tier_a_frame, tier_a_feature_order)
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    tier_b_context = mt5.build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=tier_a_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=float(training_summary["threshold_log_return"]),
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
        "training_summary": training_summary,
    }


def run_root(spec: LdaRunSpec) -> Path:
    return STAGE_ROOT / "02_runs" / spec.run_id


def save_predictions(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def tier_record(*, record_view: str, tier_scope: str, prob_frame: pd.DataFrame, threshold: float, path: Path) -> dict[str, Any]:
    metrics = split_decision_metrics(prob_frame, threshold)
    subtype_counts: dict[str, int] = {}
    if "partial_context_subtype" in prob_frame.columns:
        subtype_counts = {
            str(key): int(value)
            for key, value in prob_frame["partial_context_subtype"].astype(str).value_counts().sort_index().items()
        }
    total = {
        "rows": int(len(prob_frame)),
        "signal_count": int(sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))),
        "short_count": int(sum(metrics.get(split, {}).get("short_count", 0) for split in ("train", "validation", "oos"))),
        "long_count": int(sum(metrics.get(split, {}).get("long_count", 0) for split in ("train", "validation", "oos"))),
        "partial_context_subtype_counts": subtype_counts or None,
        "threshold_ids": f"q{THRESHOLD_QUANTILE:.2f}",
        "probability_row_sum_max_abs_error": metrics.get("probability_checks", {}).get("row_sum_max_abs_error"),
    }
    total["signal_coverage"] = safe_float(total["signal_count"]) / max(1, int(total["rows"]))
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": total,
        "split_metrics": {split: metrics.get(split, {}) for split in ("train", "validation", "oos")},
    }


def python_tier_records(
    spec: LdaRunSpec,
    *,
    tier_a_prob: pd.DataFrame,
    tier_b_prob: pd.DataFrame,
    a_threshold: float,
    b_threshold: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root = run_root(spec) / "predictions"
    a_path = root / "tier_a_separate_predictions.parquet"
    b_path = root / "tier_b_separate_predictions.parquet"
    ab_path = root / "tier_ab_combined_predictions.parquet"
    ab_prob = pd.concat(
        [
            tier_a_prob.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"),
            tier_b_prob.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    return [
        tier_record(record_view="tier_a_separate", tier_scope=mt5.TIER_A, prob_frame=tier_a_prob, threshold=a_threshold, path=a_path),
        tier_record(record_view="tier_b_separate", tier_scope=mt5.TIER_B, prob_frame=tier_b_prob, threshold=b_threshold, path=b_path),
        tier_record(record_view="tier_ab_combined", tier_scope=mt5.TIER_AB, prob_frame=ab_prob, threshold=a_threshold, path=ab_path),
    ], {"tier_a": save_predictions(a_path, tier_a_prob), "tier_b": save_predictions(b_path, tier_b_prob), "tier_ab": save_predictions(ab_path, ab_prob)}


def materialize_models(
    spec: LdaRunSpec,
    *,
    tier_a_model: Any,
    tier_b_model: Any,
    tier_a_frame: pd.DataFrame,
    tier_b_training_frame: pd.DataFrame,
    tier_a_feature_order: Sequence[str],
    tier_b_feature_order: Sequence[str],
) -> dict[str, Any]:
    root = run_root(spec) / "models"
    io_path(root).mkdir(parents=True, exist_ok=True)
    tier_a_joblib = root / f"{spec.variant_id}_tier_a_lda_58.joblib"
    tier_b_joblib = root / f"{spec.variant_id}_tier_b_lda_core42.joblib"
    tier_a_onnx = root / f"{spec.variant_id}_tier_a_lda_58.onnx"
    tier_b_onnx = root / f"{spec.variant_id}_tier_b_lda_core42.onnx"
    joblib.dump(tier_a_model, io_path(tier_a_joblib))
    joblib.dump(tier_b_model, io_path(tier_b_joblib))
    tier_a_export = export_sklearn_to_onnx_zipmap_disabled(tier_a_model, tier_a_onnx, feature_count=len(tier_a_feature_order))
    tier_b_export = export_sklearn_to_onnx_zipmap_disabled(tier_b_model, tier_b_onnx, feature_count=len(tier_b_feature_order))
    a_sample = tier_a_frame.loc[tier_a_frame["split"].astype(str).eq("validation"), list(tier_a_feature_order)].head(128).to_numpy(dtype="float64", copy=False)
    b_sample = tier_b_training_frame.loc[tier_b_training_frame["split"].astype(str).eq("validation"), list(tier_b_feature_order)].head(128).to_numpy(dtype="float64", copy=False)
    return {
        "variant_id": spec.variant_id,
        "tier_a_joblib": {"path": rel(tier_a_joblib), "sha256": sha256_file_lf_normalized(tier_a_joblib)},
        "tier_b_joblib": {"path": rel(tier_b_joblib), "sha256": sha256_file_lf_normalized(tier_b_joblib)},
        "tier_a_onnx": tier_a_export,
        "tier_b_onnx": tier_b_export,
        "onnx_parity": {
            "tier_a": check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx, a_sample, tolerance=ONNX_PARITY_TOLERANCE),
            "tier_b": check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx, b_sample, tolerance=ONNX_PARITY_TOLERANCE),
        },
    }


def export_feature_matrices(spec: LdaRunSpec, context: Mapping[str, Any]) -> dict[str, Any]:
    root = run_root(spec) / "features"
    io_path(root).mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        tier_a_frame = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq(source_split)].copy()
        tier_b_frame = context["tier_b_fallback_frame"].loc[context["tier_b_fallback_frame"]["split"].astype(str).eq(source_split)].copy()
        payload[f"tier_a_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_a_frame,
            context["tier_a_feature_order"],
            root / f"tier_a_{runtime_split}_feature_matrix.csv",
            metadata_columns=("partial_context_subtype", "route_role"),
        )
        payload[f"tier_b_fallback_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_b_frame,
            context["tier_b_feature_order"],
            root / f"tier_b_fallback_{runtime_split}_feature_matrix.csv",
            metadata_columns=("partial_context_subtype", "route_role"),
        )
    return payload


def copy_runtime_inputs(spec: LdaRunSpec, model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, spec.run_id)
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_onnx", "tier_b_onnx"):
        local_path = ROOT / model_artifacts[key]["path"]
        copies.append(copy_to_common(local_path, f"{common}/models/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        local_path = ROOT / matrix["path"]
        copies.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_attempts(
    spec: LdaRunSpec,
    *,
    context: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    a_threshold: float,
    b_threshold: float,
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(STAGE_NUMBER, spec.run_id)
    tier_a_model = Path(model_artifacts["tier_a_onnx"]["path"]).name
    tier_b_model = Path(model_artifacts["tier_b_onnx"]["path"]).name
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        tier_a_matrix = Path(feature_matrices[f"tier_a_{runtime_split}"]["path"]).name
        tier_b_matrix = Path(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"]).name
        common_kwargs = {
            "run_root": run_root(spec),
            "run_id": spec.run_id,
            "stage_number": STAGE_NUMBER,
            "exploration_label": EXPLORATION_LABEL,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": MAX_HOLD_BARS,
            "common_root": common,
        }
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_a_only_{runtime_split}", tier=mt5.TIER_A, model_path=f"{common}/models/{tier_a_model}", model_id=f"{spec.run_id}_tier_a", feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(context["tier_a_feature_order"]), feature_order_hash=context["tier_a_feature_order_hash"], short_threshold=a_threshold, long_threshold=a_threshold, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role="tier_only_total", record_view_prefix="mt5_tier_a_only"))
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_b_fallback_only_{runtime_split}", tier=mt5.TIER_B, model_path=f"{common}/models/{tier_b_model}", model_id=f"{spec.run_id}_tier_b", feature_path=f"{common}/features/{tier_b_matrix}", feature_count=len(context["tier_b_feature_order"]), feature_order_hash=context["tier_b_feature_order_hash"], short_threshold=b_threshold, long_threshold=b_threshold, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_b_fallback", attempt_role="tier_b_fallback_only_total", record_view_prefix="mt5_tier_b_fallback_only"))
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"routed_{runtime_split}", tier=mt5.TIER_AB, model_path=f"{common}/models/{tier_a_model}", model_id=f"{spec.run_id}_tier_a", feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(context["tier_a_feature_order"]), feature_order_hash=context["tier_a_feature_order_hash"], short_threshold=a_threshold, long_threshold=a_threshold, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role="routed_total", record_view_prefix="mt5_routed_total", fallback_enabled=True, fallback_model_path=f"{common}/models/{tier_b_model}", fallback_model_id=f"{spec.run_id}_tier_b", fallback_feature_path=f"{common}/features/{tier_b_matrix}", fallback_feature_count=len(context["tier_b_feature_order"]), fallback_feature_order_hash=context["tier_b_feature_order_hash"], fallback_short_threshold=b_threshold, fallback_long_threshold=b_threshold, fallback_min_margin=MIN_MARGIN, fallback_invert_signal=False))
    return attempts


def execute_or_materialize(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {**dict(prepared), "compile": {"status": "not_attempted_materialize_only"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": "blocked_materialize_only_no_mt5_execution"}
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
        return {**dict(prepared), "compile": {"status": "exception_or_not_completed"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": JUDGMENT_BLOCKED, "failure": {"type": type(exc).__name__, "message": str(exc)}}
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED
    for record in result.get("mt5_kpi_records", []):
        record["source_variant_id"] = prepared["source_variant_id"]
    return result


def variant_result(spec: LdaRunSpec, model: Any, prob_frame: pd.DataFrame, threshold: float, sample_info: Mapping[str, Any]) -> dict[str, Any]:
    result = {
        "run_number": spec.run_number,
        "run_id": spec.run_id,
        "variant_id": spec.variant_id,
        "spec": spec.payload(),
        "training_sample": sample_info,
        "threshold_quantile": THRESHOLD_QUANTILE,
        "short_threshold": threshold,
        "long_threshold": threshold,
        "min_margin": MIN_MARGIN,
        "metrics": split_decision_metrics(prob_frame, threshold),
        "probability_shape": probability_shape_metrics(prob_frame),
        "training_diagnostics": classifier_training_diagnostics(model),
    }
    result["shape_score"] = shape_score(result)
    return result


def write_characteristic_files(spec: LdaRunSpec, result: Mapping[str, Any]) -> dict[str, Any]:
    root = run_root(spec) / "results"
    io_path(root).mkdir(parents=True, exist_ok=True)
    json_path = root / "lda_characteristic_result.json"
    csv_path = root / "lda_characteristic_result.csv"
    write_json(json_path, result)
    row = {
        "run_id": spec.run_id,
        "variant_id": result.get("variant_id"),
        "solver": result.get("spec", {}).get("solver"),
        "shrinkage": result.get("spec", {}).get("shrinkage"),
        "shape_score": result.get("shape_score"),
        "threshold": result.get("short_threshold"),
        "val_signal_coverage": result.get("metrics", {}).get("validation", {}).get("signal_coverage"),
        "oos_signal_coverage": result.get("metrics", {}).get("oos", {}).get("signal_coverage"),
        "val_entropy": result.get("probability_shape", {}).get("validation", {}).get("mean_entropy"),
        "oos_entropy": result.get("probability_shape", {}).get("oos", {}).get("mean_entropy"),
    }
    with io_path(csv_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    return {"characteristic_json": {"path": rel(json_path), "sha256": sha256_file_lf_normalized(json_path)}, "characteristic_csv": {"path": rel(csv_path), "sha256": sha256_file_lf_normalized(csv_path)}}


def write_ledgers(spec: LdaRunSpec, result: Mapping[str, Any], tier_records: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    rows = build_alpha_scout_ledger_rows(
        run_id=spec.run_id,
        stage_id=STAGE_ID,
        tier_records=tier_records,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        selected_threshold_id=f"fixed_shape_q{THRESHOLD_QUANTILE:.2f}",
        run_output_root=run_root(spec),
        external_verification_status=str(result.get("external_verification_status")),
    )
    ledger_outputs = materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=rows,
    )
    registry_output = materialize_alpha_runtime_run_registry_row(
        run_id=spec.run_id,
        stage_id=STAGE_ID,
        run_registry_path=RUN_REGISTRY_PATH,
        route_coverage=result.get("route_coverage", {}),
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=Path(rel(run_root(spec))),
        external_verification_status=str(result.get("external_verification_status")),
    )
    return ledger_outputs, registry_output


def build_summary(spec: LdaRunSpec, characteristic: Mapping[str, Any], result: Mapping[str, Any], b_threshold: float, model_artifacts: Mapping[str, Any], characteristic_artifacts: Mapping[str, Any]) -> dict[str, Any]:
    mt5_records = list(result.get("mt5_kpi_records", []))
    by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in mt5_records}
    return {
        "packet_id": PACKET_ID,
        "run_number": spec.run_number,
        "run_id": spec.run_id,
        "stage_id": STAGE_ID,
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "description": spec.description,
        "shape_score": characteristic.get("shape_score"),
        "tier_a_threshold": characteristic.get("short_threshold"),
        "tier_b_threshold": b_threshold,
        "threshold_policy": f"fixed validation nonflat q{THRESHOLD_QUANTILE:.2f}; not profit search",
        "training_sample_policy": f"deterministic stratified cap {ROWS_PER_CLASS} rows per class",
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
        "attempt_count": len(result.get("attempts", [])),
        "mt5_kpi_record_count": len(mt5_records),
        "validation_routed": by_view.get("mt5_routed_total_validation_is", {}),
        "oos_routed": by_view.get("mt5_routed_total_oos", {}),
        "model_artifacts": model_artifacts,
        "characteristic_artifacts": characteristic_artifacts,
        "failure": result.get("failure"),
    }


def write_run_files(spec: LdaRunSpec, *, result: Mapping[str, Any], context: Mapping[str, Any], characteristic: Mapping[str, Any], tier_records: Sequence[Mapping[str, Any]], prediction_artifacts: Mapping[str, Any], model_artifacts: Mapping[str, Any], characteristic_artifacts: Mapping[str, Any], b_threshold: float, ledger_outputs: Mapping[str, Any], registry_output: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    summary = build_summary(spec, characteristic, result, b_threshold, model_artifacts, characteristic_artifacts)
    manifest = {
        "run_id": spec.run_id,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_number": spec.run_number,
        "created_at_utc": created_at,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "stage_inheritance": STAGE_INHERITANCE,
        "boundary": BOUNDARY,
        "spec": spec.payload(),
        "characteristic": characteristic,
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
        "run_id": spec.run_id,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "lda_discriminant_python_shape_plus_mt5_runtime_probe",
        "python_characteristic": characteristic,
        "python_tier_records": list(tier_records),
        "tier_b_context_summary": context["tier_b_context_summary"],
        "mt5": {"scoreboard_lane": "runtime_probe", "external_verification_status": result.get("external_verification_status"), "execution_results": result.get("execution_results", []), "strategy_tester_reports": result.get("strategy_tester_reports", []), "kpi_records": result.get("mt5_kpi_records", [])},
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    }
    write_json(run_root(spec) / "run_manifest.json", manifest)
    write_json(run_root(spec) / "kpi_record.json", kpi_record)
    write_json(run_root(spec) / "summary.json", summary)
    write_json(PACKET_ROOT / "run_summaries" / f"{spec.run_id}.json", summary)
    write_json(PACKET_ROOT / "run_registry_outputs" / f"{spec.run_id}.json", registry_output)
    write_json(PACKET_ROOT / "ledger_outputs" / f"{spec.run_id}.json", ledger_outputs)
    write_md(run_root(spec) / "reports/result_summary.md", run_result_markdown(summary))
    return summary


def prepare_runtime_payload(spec: LdaRunSpec, context: Mapping[str, Any], model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any], a_threshold: float, b_threshold: float) -> dict[str, Any]:
    return {
        "run_id": spec.run_id,
        "run_root": run_root(spec).as_posix(),
        "stage_id": STAGE_ID,
        "source_variant_id": spec.variant_id,
        "attempts": make_attempts(spec, context=context, model_artifacts=model_artifacts, feature_matrices=feature_matrices, a_threshold=a_threshold, b_threshold=b_threshold),
        "common_copies": copy_runtime_inputs(spec, model_artifacts, feature_matrices),
        "feature_matrices": list(feature_matrices.values()),
        "route_coverage": context["tier_b_context_summary"],
    }


def build_one(spec: LdaRunSpec, context: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    tier_a_model, a_sample = fit_lda_variant(context["tier_a_frame"], context["tier_a_feature_order"], spec, rows_per_class=ROWS_PER_CLASS)
    tier_b_model, b_sample = fit_lda_variant(context["tier_b_training_frame"], context["tier_b_feature_order"], spec, rows_per_class=ROWS_PER_CLASS)
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], context["tier_a_feature_order"])
    tier_b_training_prob = probability_frame(tier_b_model, context["tier_b_training_frame"], context["tier_b_feature_order"])
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], context["tier_b_feature_order"])
    a_threshold = nonflat_threshold(tier_a_prob, THRESHOLD_QUANTILE)
    b_threshold = nonflat_threshold(tier_b_training_prob, THRESHOLD_QUANTILE)
    characteristic = variant_result(spec, tier_a_model, tier_a_prob, a_threshold, a_sample)
    characteristic = {**characteristic, "tier_b_training_sample": b_sample}
    tier_records, prediction_artifacts = python_tier_records(spec, tier_a_prob=tier_a_prob, tier_b_prob=tier_b_prob, a_threshold=a_threshold, b_threshold=b_threshold)
    model_artifacts = materialize_models(spec, tier_a_model=tier_a_model, tier_b_model=tier_b_model, tier_a_frame=context["tier_a_frame"], tier_b_training_frame=context["tier_b_training_frame"], tier_a_feature_order=context["tier_a_feature_order"], tier_b_feature_order=context["tier_b_feature_order"])
    feature_matrices = export_feature_matrices(spec, context)
    prepared = prepare_runtime_payload(spec, context, model_artifacts, feature_matrices, a_threshold, b_threshold)
    result = execute_or_materialize(prepared, args)
    result["route_coverage"] = context["tier_b_context_summary"]
    characteristic_artifacts = write_characteristic_files(spec, characteristic)
    ledger_outputs, registry_output = write_ledgers(spec, result, tier_records)
    return write_run_files(spec, result=result, context=context, characteristic=characteristic, tier_records=tier_records, prediction_artifacts=prediction_artifacts, model_artifacts=model_artifacts, characteristic_artifacts=characteristic_artifacts, b_threshold=b_threshold, ledger_outputs=ledger_outputs, registry_output=registry_output, created_at=created_at)


def run_result_markdown(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            f"# {summary['run_id']} Result Summary({summary['run_id']} 결과 요약)",
            "",
            f"- variant(변형): `{summary['variant_id']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            f"- external verification(외부 검증): `{summary['external_verification_status']}`",
            f"- shape score(모양 점수): `{summary['shape_score']}`",
            f"- validation routed net/trades(검증 라우팅 순수익/거래수): `{summary['validation_routed'].get('net_profit')}` / `{summary['validation_routed'].get('trade_count')}`",
            f"- OOS routed net/trades(표본외 라우팅 순수익/거래수): `{summary['oos_routed'].get('net_profit')}` / `{summary['oos_routed'].get('trade_count')}`",
            "",
            f"효과(effect, 효과): `{summary['run_number']}`는 LDA(선형 판별 분석)의 `{summary['idea_id']}` 특징을 MT5(메타트레이더5) runtime_probe(런타임 탐침) 경계로 읽었다.",
        ]
    )


def aggregate_summary(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [row for row in summaries if row.get("external_verification_status") == "completed"]
    all_completed = len(completed) == len(summaries)
    return {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_count": len(summaries),
        "completed_run_count": len(completed),
        "blocked_run_count": len(summaries) - len(completed),
        "external_verification_status": "completed" if all_completed else "blocked_or_partial",
        "judgment": "inconclusive_lda_run06A_run06J_runtime_probe_completed" if all_completed else "blocked_or_partial_lda_run06A_run06J_runtime_probe",
        "boundary": BOUNDARY,
        "run_ids": [row["run_id"] for row in summaries],
        "best_shape_score_run": max(summaries, key=lambda row: safe_float(row.get("shape_score"))) if summaries else None,
        "best_validation_routed_net_run": max(summaries, key=lambda row: safe_float(row.get("validation_routed", {}).get("net_profit"), -1e18)) if summaries else None,
        "best_oos_routed_net_run": max(summaries, key=lambda row: safe_float(row.get("oos_routed", {}).get("net_profit"), -1e18)) if summaries else None,
        "mt5_kpi_record_count": int(sum(int(row.get("mt5_kpi_record_count", 0)) for row in summaries)),
        "attempt_count": int(sum(int(row.get("attempt_count", 0)) for row in summaries)),
    }


def packet_markdown(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage15 LDA RUN06A-RUN06J Runtime Probe(15단계 LDA 실행 06A-06J 런타임 탐침)",
        "",
        f"- judgment(판정): `{aggregate['judgment']}`",
        f"- completed runs(완료 실행): `{aggregate['completed_run_count']}/{aggregate['run_count']}`",
        f"- MT5 KPI records(MT5 KPI 기록): `{aggregate['mt5_kpi_record_count']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| run(실행) | feature(특징) | status(상태) | shape(모양) | val net/trades(검증) | oos net/trades(표본외) |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in summaries:
        lines.append(
            "| `{}` | `{}` | `{}` | `{:.6f}` | `{}/{}` | `{}/{}` |".format(
                row["run_number"],
                row["idea_id"],
                row["external_verification_status"],
                safe_float(row.get("shape_score")),
                row.get("validation_routed", {}).get("net_profit"),
                row.get("validation_routed", {}).get("trade_count"),
                row.get("oos_routed", {}).get("net_profit"),
                row.get("oos_routed", {}).get("trade_count"),
            )
        )
    lines.extend(
        [
            "",
            "효과(effect, 효과): 이 표는 LDA(선형 판별 분석)의 solver(풀이 방식), shrinkage(공분산 축소), prior(사전확률), rank tolerance(랭크 허용치) 축을 수익 선택 없이 나란히 본 것이다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): alpha quality(알파 품질), edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )
    return "\n".join(lines)


def gate_payloads(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    all_completed = aggregate.get("completed_run_count") == aggregate.get("run_count") == 10
    required_views = {"mt5_tier_a_only_validation_is", "mt5_tier_a_only_oos", "mt5_tier_b_fallback_only_validation_is", "mt5_tier_b_fallback_only_oos", "mt5_routed_total_validation_is", "mt5_routed_total_oos"}
    return {
        "scope_completion_gate": {"audit_name": "scope_completion_gate", "status": "pass" if all_completed else "blocked", "passed": all_completed, "counts": {"run_count": aggregate.get("run_count"), "completed_run_count": aggregate.get("completed_run_count")}},
        "runtime_evidence_gate": {"audit_name": "runtime_evidence_gate", "status": "pass" if all_completed else "blocked", "passed": all_completed, "counts": {"attempt_count": aggregate.get("attempt_count"), "mt5_kpi_record_count": aggregate.get("mt5_kpi_record_count")}},
        "kpi_contract_audit": {"audit_name": "kpi_contract_audit", "status": "pass" if all_completed else "blocked", "passed": all_completed, "required_views": sorted(required_views), "run_count": len(summaries)},
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass" if all_completed else "blocked", "passed": all_completed, "allowed_claims": [aggregate.get("judgment")], "forbidden_claims": ["alpha_quality", "edge", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"]},
        "required_gate_coverage_audit": {"audit_name": "required_gate_coverage_audit", "status": "pass" if all_completed else "blocked", "passed": all_completed, "required_gates": {"scope_completion_gate": "pass" if all_completed else "blocked", "runtime_evidence_gate": "pass" if all_completed else "blocked", "kpi_contract_audit": "pass" if all_completed else "blocked", "final_claim_guard": "pass" if all_completed else "blocked"}},
    }


def sync_stage_docs(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]]) -> None:
    write_md(REVIEW_PACKET_PATH, packet_markdown(aggregate, summaries))
    write_md(
        STAGE_ROOT / "03_reviews/review_index.md",
        "\n".join(
            [
                "# Stage 15 Review Index(15단계 검토 색인)",
                "",
                f"- `run06A`~`run06J`: `{aggregate['judgment']}`, report(보고서) `{rel(REVIEW_PACKET_PATH)}`",
                "",
                "효과(effect, 효과): Stage15(15단계)는 LDA(선형 판별 분석) 10개 특징 실행을 MT5(메타트레이더5) runtime_probe(런타임 탐침)로 기록했다.",
            ]
        ),
    )
    write_md(
        STAGE_ROOT / "04_selected/selection_status.md",
        "\n".join(
            [
                "# Stage 15 Selection Status(15단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                "- status(상태): `open_with_run06A_run06J_lda_runtime_probe_reviewed(열림, LDA 실행 06A-06J 검토됨)`",
                "- current run(현재 실행): `run06J_lda_eigen_balanced_shrinkage050_runtime_probe_v1`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{aggregate['judgment']}`",
                "",
                "효과(effect, 효과): LDA(선형 판별 분석) 특징은 보존하지만 Stage15(15단계)는 아직 다음 학습법 탐색을 계속할 수 있다.",
            ]
        ),
    )
    write_md(
        DECISION_PATH,
        "\n".join(
            [
                "# 2026-05-02 Stage15 LDA RUN06A-RUN06J Runtime Probe(15단계 LDA 실행 06A-06J 런타임 탐침)",
                "",
                "## Decision(결정)",
                "",
                f"Stage15(15단계)의 첫 model learning method(모델 학습법)를 LDA(선형 판별 분석)로 열고 `run06A`부터 `run06J`까지 기록했다.",
                "",
                "효과(effect, 효과): 분포/공분산 기반 학습의 여러 특징을 같은 데이터 계약과 MT5(메타트레이더5) runtime_probe(런타임 탐침) 경계에서 비교할 수 있다.",
                "",
                "## Boundary(경계)",
                "",
                f"`{BOUNDARY}`",
            ]
        ),
    )
    sync_workspace_docs(aggregate)


def sync_workspace_docs(aggregate: Mapping[str, Any]) -> None:
    state_path = ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    block = f"""stage15_lda_run06A_run06J_runtime_probe:
  packet_id: {PACKET_ID}
  status: reviewed_runtime_probe_completed
  judgment: {aggregate['judgment']}
  model_family: {MODEL_FAMILY}
  run_range: run06A-run06J
  completed_run_count: {aggregate['completed_run_count']}
  mt5_kpi_record_count: {aggregate['mt5_kpi_record_count']}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REVIEW_PACKET_PATH)}
  decision_path: {rel(DECISION_PATH)}
"""
    state = state.replace("current_run_id: ''\n", "current_run_id: run06J_lda_eigen_balanced_shrinkage050_runtime_probe_v1\n", 1)
    state = state.replace("stage15_opened_no_run_yet", "stage15_lda_run06A_run06J_reviewed_runtime_probe")
    state = state.replace("Stage 15 as open_no_run_yet", "Stage 15 as open_with_run06A_run06J_lda_runtime_probe_reviewed")
    state = state.replace("model_family: not_yet_selected_untried_learning_methods", f"model_family: {MODEL_FAMILY}", 1)
    state = state.replace("current_run_id: ''\n  current_status: no_run_yet", "current_run_id: run06J_lda_eigen_balanced_shrinkage050_runtime_probe_v1\n  current_status: run06A_run06J_runtime_probe_reviewed", 1)
    state = state.replace("next_action: design_first_untried_learning_method_scout", "next_action: continue_stage15_with_next_untried_learning_method_or_close_lda_topic", 1)
    if "stage15_lda_run06A_run06J_runtime_probe:" in state:
        state = re.sub(r"stage15_lda_run06A_run06J_runtime_probe:\n(?:  .*\n)+", block, state, count=1)
    else:
        state = state.replace("stage01_raw_m5_inventory:\n", block + "stage01_raw_m5_inventory:\n", 1)
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")
    current_path = ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    latest = "\n".join(
        [
            "## Latest Stage 15 Update(최신 Stage 15 업데이트)",
            "",
            f"Stage15(15단계)는 LDA(`Linear Discriminant Analysis`, 선형 판별 분석)로 `run06A`~`run06J`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)까지 실행했다.",
            "",
            f"효과(effect, 효과): `{aggregate['judgment']}`로 기록했지만 alpha quality(알파 품질), edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.",
            "",
        ]
    )
    current = re.sub(r"## Latest Stage 15 Update\(최신 Stage 15 업데이트\)\n\n.*?(?=## 쉬운 설명)", latest, current, count=1, flags=re.S)
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")


def write_packet_files(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], created_at: str) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", aggregate)
    write_json(PACKET_ROOT / "artifact_index.json", {"run_summaries": list(summaries), "report_path": rel(REVIEW_PACKET_PATH), "created_at_utc": created_at})
    write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "primary_family": "runtime_backtest", "primary_skill": "obsidian-runtime-parity", "support_skills": ["obsidian-backtest-forensics", "obsidian-run-evidence-system", "obsidian-model-validation", "obsidian-code-surface-guard"], "required_gates": ["scope_completion_gate", "runtime_evidence_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"]})
    write_json(PACKET_ROOT / "skill_receipts.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "receipts": [{"skill": "obsidian-experiment-design", "status": "completed", "hypothesis": "LDA covariance and prior variants expose different probability shape and signal density.", "decision_use": "Stage15 LDA clue preservation only"}, {"skill": "obsidian-runtime-parity", "status": "completed", "runtime_claim_boundary": "runtime_probe"}, {"skill": "obsidian-run-evidence-system", "status": "completed", "measurement_scope": "10 Python shape reads plus 10 MT5 routed probes"}, {"skill": "obsidian-model-validation", "status": "completed", "threshold_policy": "fixed validation nonflat q90 per run, not profit search"}]})
    for name, payload in gate_payloads(aggregate, summaries).items():
        write_json(PACKET_ROOT / f"{name}.json", payload)


def build_all(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = load_context()
    selected_ids = {item.strip() for item in args.run_filter.split(",") if item.strip()} if args.run_filter else set()
    specs = [spec for spec in default_stage15_lda_specs() if not selected_ids or spec.run_number in selected_ids or spec.run_id in selected_ids]
    summaries = [build_one(spec, context, args) for spec in specs]
    aggregate = aggregate_summary(summaries)
    write_packet_files(aggregate, summaries, created_at)
    sync_stage_docs(aggregate, summaries)
    return aggregate


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage15 LDA RUN06A-RUN06J runtime probes.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--run-filter", default="")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    args = parser.parse_args(argv)
    summary = build_all(args)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
