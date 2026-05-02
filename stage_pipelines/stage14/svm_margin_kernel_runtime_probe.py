from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
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
    ledger_pairs,
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
from foundation.models.onnx_bridge import (
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
)
from foundation.models.svm_margin_kernel import (
    SvmVariantSpec,
    classifier_training_diagnostics,
    default_svm_margin_kernel_specs,
    fit_svm_variant,
    nonflat_threshold,
    probability_frame,
    probability_shape_metrics,
    split_decision_metrics,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage14.svm_margin_kernel_closeout import (
    closeout_report_markdown,
    final_claim_guard,
    kpi_contract_audit,
    required_gate_coverage,
    result_summary_markdown,
    routing_receipt,
    run_packet_markdown,
    runtime_evidence_gate,
    scope_completion_gate,
    skill_receipts,
    sync_stage_docs,
)


STAGE_NUMBER = 14
STAGE_ID = "14_model_family_challenge__margin_kernel_training_effect"
RUN_NUMBER = "run05A"
RUN_ID = "run05A_svm_margin_kernel_characteristic_runtime_probe_v1"
PACKET_ID = "stage14_run05A_svm_margin_kernel_closeout_packet_v1"
EXPLORATION_LABEL = "stage14_Model__SVMMarginKernelCloseoutProbe"
MODEL_FAMILY = "sklearn_svm_margin_kernel_family"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
STAGE_INHERITANCE = "independent_no_stage10_11_12_13_run_baseline_seed_or_reference"
BOUNDARY = "svm_margin_kernel_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "closed_inconclusive_svm_margin_kernel_runtime_probe_evidence"
JUDGMENT_BLOCKED = "blocked_svm_margin_kernel_runtime_probe_after_attempt"
THRESHOLD_QUANTILE = 0.90
MIN_MARGIN = 0.0
MAX_HOLD_BARS = 12
ROWS_PER_CLASS = 600

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets/stage14_svm_margin_kernel_closeout_v1"
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REPORT_PATH = STAGE_ROOT / "03_reviews/run05A_svm_margin_kernel_runtime_probe_packet.md"
CLOSEOUT_PATH = STAGE_ROOT / "03_reviews/stage14_closeout_packet.md"
STAGE15_ID = "15_model_family_challenge__untried_learning_methods_scout"
STAGE15_ROOT = ROOT / "stages" / STAGE15_ID


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


def load_frames() -> dict[str, Any]:
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


def shape_score(result: Mapping[str, Any]) -> float:
    metrics = result.get("metrics", {})
    shape = result.get("probability_shape", {})
    validation = metrics.get("validation", {})
    oos = metrics.get("oos", {})
    val_cov = safe_float(validation.get("signal_coverage"))
    oos_cov = safe_float(oos.get("signal_coverage"))
    val_entropy = safe_float(shape.get("validation", {}).get("mean_entropy"))
    oos_entropy = safe_float(shape.get("oos", {}).get("mean_entropy"))
    val_margin = safe_float(shape.get("validation", {}).get("probability_margin_mean"))
    oos_margin = safe_float(shape.get("oos", {}).get("probability_margin_mean"))
    density = 1.0 - min(abs(val_cov - 0.10) / 0.10, 1.0)
    density_stability = 1.0 - min(abs(val_cov - oos_cov) / 0.18, 1.0)
    entropy_stability = 1.0 - min(abs(val_entropy - oos_entropy) / 0.18, 1.0)
    margin_presence = min((val_margin + oos_margin) / 0.16, 1.0)
    margin_stability = 1.0 - min(abs(val_margin - oos_margin) / 0.08, 1.0)
    return float(
        0.25 * density
        + 0.25 * density_stability
        + 0.20 * entropy_stability
        + 0.20 * margin_presence
        + 0.10 * margin_stability
    )


def fit_and_score_variants(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    specs: Sequence[SvmVariantSpec],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    results: list[dict[str, Any]] = []
    models: dict[str, Any] = {}
    for spec in specs:
        model, sample_info = fit_svm_variant(
            frame,
            feature_order,
            spec,
            rows_per_class=ROWS_PER_CLASS,
        )
        prob = probability_frame(model, frame, feature_order)
        threshold = nonflat_threshold(prob, THRESHOLD_QUANTILE)
        metrics = split_decision_metrics(prob, threshold)
        shape = probability_shape_metrics(prob)
        result = {
            "variant_id": spec.variant_id,
            "spec": spec.payload(),
            "training_sample": sample_info,
            "threshold_quantile": THRESHOLD_QUANTILE,
            "short_threshold": threshold,
            "long_threshold": threshold,
            "min_margin": MIN_MARGIN,
            "metrics": metrics,
            "probability_shape": shape,
            "training_diagnostics": classifier_training_diagnostics(model),
        }
        result["shape_score"] = shape_score(result)
        results.append(result)
        models[spec.variant_id] = model
    results.sort(key=lambda row: safe_float(row.get("shape_score")), reverse=True)
    return results, models


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
        "signal_count": int(
            sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))
        ),
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
    return [
        tier_record(record_view="tier_a_separate", tier_scope=mt5.TIER_A, prob_frame=tier_a_prob, threshold=a_threshold, path=a_path),
        tier_record(record_view="tier_b_separate", tier_scope=mt5.TIER_B, prob_frame=tier_b_prob, threshold=b_threshold, path=b_path),
        tier_record(record_view="tier_ab_combined", tier_scope=mt5.TIER_AB, prob_frame=ab_prob, threshold=a_threshold, path=ab_path),
    ], {"tier_a": tier_a_saved, "tier_b": tier_b_saved, "tier_ab": ab_saved}


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
    model_root = RUN_ROOT / "models"
    io_path(model_root).mkdir(parents=True, exist_ok=True)
    variant_id = str(selected["variant_id"])
    tier_a_joblib = model_root / f"{variant_id}_tier_a_svm_58.joblib"
    tier_b_joblib = model_root / f"{variant_id}_tier_b_svm_core42.joblib"
    tier_a_onnx = model_root / f"{variant_id}_tier_a_svm_58.onnx"
    tier_b_onnx = model_root / f"{variant_id}_tier_b_svm_core42.onnx"
    joblib.dump(tier_a_model, io_path(tier_a_joblib))
    joblib.dump(tier_b_model, io_path(tier_b_joblib))
    tier_a_export = export_sklearn_to_onnx_zipmap_disabled(tier_a_model, tier_a_onnx, feature_count=len(tier_a_feature_order))
    tier_b_export = export_sklearn_to_onnx_zipmap_disabled(tier_b_model, tier_b_onnx, feature_count=len(tier_b_feature_order))
    a_sample = (
        tier_a_frame.loc[tier_a_frame["split"].astype(str).eq("validation"), list(tier_a_feature_order)]
        .head(128)
        .to_numpy(dtype="float64", copy=False)
    )
    b_sample = (
        tier_b_training_frame.loc[tier_b_training_frame["split"].astype(str).eq("validation"), list(tier_b_feature_order)]
        .head(128)
        .to_numpy(dtype="float64", copy=False)
    )
    return {
        "variant_id": variant_id,
        "tier_a_joblib": {"path": rel(tier_a_joblib), "sha256": sha256_file_lf_normalized(tier_a_joblib)},
        "tier_b_joblib": {"path": rel(tier_b_joblib), "sha256": sha256_file_lf_normalized(tier_b_joblib)},
        "tier_a_onnx": tier_a_export,
        "tier_b_onnx": tier_b_export,
        "onnx_parity": {
            "tier_a": check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx, a_sample),
            "tier_b": check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx, b_sample),
        },
    }


def export_feature_matrices(context: Mapping[str, Any]) -> dict[str, Any]:
    feature_root = RUN_ROOT / "features"
    io_path(feature_root).mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        tier_a_frame = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq(source_split)].copy()
        tier_b_frame = context["tier_b_fallback_frame"].loc[
            context["tier_b_fallback_frame"]["split"].astype(str).eq(source_split)
        ].copy()
        tier_a_path = feature_root / f"tier_a_{runtime_split}_feature_matrix.csv"
        tier_b_path = feature_root / f"tier_b_fallback_{runtime_split}_feature_matrix.csv"
        payload[f"tier_a_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_a_frame,
            context["tier_a_feature_order"],
            tier_a_path,
            metadata_columns=("partial_context_subtype", "route_role"),
        )
        payload[f"tier_b_fallback_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_b_frame,
            context["tier_b_feature_order"],
            tier_b_path,
            metadata_columns=("partial_context_subtype", "route_role"),
        )
    return payload


def copy_runtime_inputs(model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_onnx", "tier_b_onnx"):
        local_path = ROOT / model_artifacts[key]["path"]
        copies.append(copy_to_common(local_path, f"{common}/models/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        local_path = ROOT / matrix["path"]
        copies.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_attempts(
    *,
    context: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    a_threshold: float,
    b_threshold: float,
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    tier_a_model = Path(model_artifacts["tier_a_onnx"]["path"]).name
    tier_b_model = Path(model_artifacts["tier_b_onnx"]["path"]).name
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        tier_a_matrix = Path(feature_matrices[f"tier_a_{runtime_split}"]["path"]).name
        tier_b_matrix = Path(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"]).name
        common_kwargs = {
            "run_root": RUN_ROOT,
            "run_id": RUN_ID,
            "stage_number": STAGE_NUMBER,
            "exploration_label": EXPLORATION_LABEL,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": MAX_HOLD_BARS,
            "common_root": common,
        }
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_a_only_{runtime_split}",
                tier=mt5.TIER_A,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{RUN_ID}_tier_a",
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=len(context["tier_a_feature_order"]),
                feature_order_hash=context["tier_a_feature_order_hash"],
                short_threshold=a_threshold,
                long_threshold=a_threshold,
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix="mt5_tier_a_only",
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_b_fallback_only_{runtime_split}",
                tier=mt5.TIER_B,
                model_path=f"{common}/models/{tier_b_model}",
                model_id=f"{RUN_ID}_tier_b",
                feature_path=f"{common}/features/{tier_b_matrix}",
                feature_count=len(context["tier_b_feature_order"]),
                feature_order_hash=context["tier_b_feature_order_hash"],
                short_threshold=b_threshold,
                long_threshold=b_threshold,
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_b_fallback",
                attempt_role="tier_b_fallback_only_total",
                record_view_prefix="mt5_tier_b_fallback_only",
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"routed_{runtime_split}",
                tier=mt5.TIER_AB,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{RUN_ID}_tier_a",
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=len(context["tier_a_feature_order"]),
                feature_order_hash=context["tier_a_feature_order_hash"],
                short_threshold=a_threshold,
                long_threshold=a_threshold,
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="routed_total",
                record_view_prefix="mt5_routed_total",
                fallback_enabled=True,
                fallback_model_path=f"{common}/models/{tier_b_model}",
                fallback_model_id=f"{RUN_ID}_tier_b",
                fallback_feature_path=f"{common}/features/{tier_b_matrix}",
                fallback_feature_count=len(context["tier_b_feature_order"]),
                fallback_feature_order_hash=context["tier_b_feature_order_hash"],
                fallback_short_threshold=b_threshold,
                fallback_long_threshold=b_threshold,
                fallback_min_margin=MIN_MARGIN,
                fallback_invert_signal=False,
            )
        )
    return attempts


def prepare_runtime_payload(
    context: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    feature_matrices: Mapping[str, Any],
    selected: Mapping[str, Any],
    b_threshold: float,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_root": RUN_ROOT.as_posix(),
        "stage_id": STAGE_ID,
        "source_variant_id": selected["variant_id"],
        "attempts": make_attempts(
            context=context,
            model_artifacts=model_artifacts,
            feature_matrices=feature_matrices,
            a_threshold=float(selected["short_threshold"]),
            b_threshold=b_threshold,
        ),
        "common_copies": copy_runtime_inputs(model_artifacts, feature_matrices),
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
            "judgment": JUDGMENT_BLOCKED,
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED
    for record in result.get("mt5_kpi_records", []):
        record["source_variant_id"] = prepared["source_variant_id"]
    return result


def write_variant_results(variant_results: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result_root = RUN_ROOT / "results"
    io_path(result_root).mkdir(parents=True, exist_ok=True)
    json_path = result_root / "variant_results.json"
    csv_path = result_root / "variant_results.csv"
    write_json(json_path, list(variant_results))
    flat_rows: list[dict[str, Any]] = []
    for row in variant_results:
        metrics = row.get("metrics", {})
        shape = row.get("probability_shape", {})
        flat_rows.append(
            {
                "variant_id": row.get("variant_id"),
                "kernel": row.get("spec", {}).get("kernel"),
                "c_value": row.get("spec", {}).get("c_value"),
                "shape_score": row.get("shape_score"),
                "threshold": row.get("short_threshold"),
                "val_signal_coverage": metrics.get("validation", {}).get("signal_coverage"),
                "oos_signal_coverage": metrics.get("oos", {}).get("signal_coverage"),
                "val_entropy": shape.get("validation", {}).get("mean_entropy"),
                "oos_entropy": shape.get("oos", {}).get("mean_entropy"),
                "val_probability_margin": shape.get("validation", {}).get("probability_margin_mean"),
                "oos_probability_margin": shape.get("oos", {}).get("probability_margin_mean"),
            }
        )
    with io_path(csv_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(flat_rows[0]))
        writer.writeheader()
        writer.writerows(flat_rows)
    return {
        "variant_results_json": {"path": rel(json_path), "sha256": sha256_file_lf_normalized(json_path)},
        "variant_results_csv": {"path": rel(csv_path), "sha256": sha256_file_lf_normalized(csv_path), "rows": len(flat_rows)},
    }


def write_ledgers(result: Mapping[str, Any], tier_records: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    threshold_id = f"fixed_shape_q{THRESHOLD_QUANTILE:.2f}"
    rows = build_alpha_scout_ledger_rows(
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
        rows=rows,
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
    return ledger_outputs, run_registry_output


def build_summary(
    *,
    result: Mapping[str, Any],
    selected: Mapping[str, Any],
    b_threshold: float,
    model_artifacts: Mapping[str, Any],
    variant_artifacts: Mapping[str, Any],
) -> dict[str, Any]:
    mt5_records = list(result.get("mt5_kpi_records", []))
    by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in mt5_records}
    return {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "selected_variant_id": selected["variant_id"],
        "selected_shape_score": selected.get("shape_score"),
        "tier_a_threshold": selected.get("short_threshold"),
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
        "variant_artifacts": variant_artifacts,
        "failure": result.get("failure"),
    }


def write_run_files(
    *,
    result: Mapping[str, Any],
    context: Mapping[str, Any],
    variant_results: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    prediction_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    variant_artifacts: Mapping[str, Any],
    b_threshold: float,
    ledger_outputs: Mapping[str, Any],
    run_registry_output: Mapping[str, Any],
    created_at: str,
) -> dict[str, Any]:
    summary = build_summary(
        result=result,
        selected=selected,
        b_threshold=b_threshold,
        model_artifacts=model_artifacts,
        variant_artifacts=variant_artifacts,
    )
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
        "training_sample_policy": summary["training_sample_policy"],
        "threshold_policy": summary["threshold_policy"],
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
        "kpi_scope": "svm_margin_kernel_python_shape_plus_mt5_runtime_probe",
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
    write_json(PACKET_ROOT / "skill_receipts.json", skill_receipts(created_at, result, summary))
    write_json(PACKET_ROOT / "routing_receipt.json", routing_receipt(created_at))
    write_json(PACKET_ROOT / "scope_completion_gate.json", scope_completion_gate(result, summary))
    write_json(PACKET_ROOT / "runtime_evidence_gate.json", runtime_evidence_gate(result, summary))
    write_json(PACKET_ROOT / "kpi_contract_audit.json", kpi_contract_audit(result, tier_records))
    write_json(PACKET_ROOT / "required_gate_coverage_audit.json", required_gate_coverage(result))
    write_json(PACKET_ROOT / "final_claim_guard.json", final_claim_guard(result))
    write_md(RUN_ROOT / "reports/result_summary.md", result_summary_markdown(summary, result, variant_results))
    write_md(REPORT_PATH, run_packet_markdown(summary, result, variant_results))
    write_md(PACKET_ROOT / "closeout_report.md", closeout_report_markdown(summary, result))
    return summary


def build_all(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = load_frames()
    specs = default_svm_margin_kernel_specs()
    variant_results, trained_models = fit_and_score_variants(context["tier_a_frame"], context["tier_a_feature_order"], specs)
    selected = variant_results[0]
    selected_spec = SvmVariantSpec(**selected["spec"])
    tier_a_model = trained_models[selected["variant_id"]]
    tier_b_model, tier_b_sample = fit_svm_variant(
        context["tier_b_training_frame"],
        context["tier_b_feature_order"],
        selected_spec,
        rows_per_class=ROWS_PER_CLASS,
    )
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], context["tier_a_feature_order"])
    tier_b_training_prob = probability_frame(tier_b_model, context["tier_b_training_frame"], context["tier_b_feature_order"])
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], context["tier_b_feature_order"])
    b_threshold = nonflat_threshold(tier_b_training_prob, THRESHOLD_QUANTILE)
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
    feature_matrices = export_feature_matrices(context)
    prepared = prepare_runtime_payload(context, model_artifacts, feature_matrices, selected, b_threshold)
    result = execute_or_materialize(prepared, args)
    result["route_coverage"] = context["tier_b_context_summary"]
    variant_artifacts = write_variant_results(variant_results)
    ledger_outputs, run_registry_output = write_ledgers(result, tier_records)
    selected = {**selected, "tier_b_training_sample": tier_b_sample}
    summary = write_run_files(
        result=result,
        context=context,
        variant_results=variant_results,
        selected=selected,
        tier_records=tier_records,
        prediction_artifacts=prediction_artifacts,
        model_artifacts=model_artifacts,
        variant_artifacts=variant_artifacts,
        b_threshold=b_threshold,
        ledger_outputs=ledger_outputs,
        run_registry_output=run_registry_output,
        created_at=created_at,
    )
    sync_stage_docs(summary, result)
    write_json(PACKET_ROOT / "command_result.json", {"run_id": RUN_ID, "materialize_only": bool(args.materialize_only), "summary": summary})
    return summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage14 SVM margin/kernel shape scout and MT5 runtime probe.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    args = parser.parse_args(argv)
    summary = build_all(args)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
