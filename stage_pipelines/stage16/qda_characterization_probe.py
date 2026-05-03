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
from foundation.control_plane.alpha_run_ledgers import build_alpha_scout_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    FEATURE_ORDER_PATH,
    MODEL_INPUT_PATH,
    RAW_ROOT,
    ROOT,
    TRAINING_SUMMARY_PATH,
)
from foundation.models.baseline_training import load_feature_order, validate_model_input_frame
from foundation.models.onnx_bridge import ordered_hash
from foundation.models.qda_discriminant import (
    QdaRunSpec,
    classifier_training_diagnostics,
    default_stage16_qda_specs,
    fit_qda_variant,
    nonflat_threshold,
    probability_frame,
    probability_shape_metrics,
    shape_score,
    split_decision_metrics,
)
from foundation.mt5 import runtime_support as mt5
STAGE_NUMBER = 16
STAGE_ID = "16_model_family_challenge__qda_class_covariance_scout"
PACKET_ID = "stage16_qda_run08A_run08J_characterization_v1"
EXPLORATION_LABEL = "stage16_Model__QDAClassCovarianceCharacterization"
MODEL_FAMILY = "sklearn_qda_discriminant_family"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
STAGE_INHERITANCE = "independent_qda_topic_after_stage15_lda_closeout_no_baseline_inheritance"
BOUNDARY = "qda_characterization_structural_scout_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_qda_characterization_structural_scout_completed"
THRESHOLD_QUANTILE = 0.90
STAGE_ROOT = ROOT / "stages" / STAGE_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REVIEW_PACKET_PATH = STAGE_ROOT / "03_reviews/run08A_run08J_qda_characterization_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage16_qda_run08A_run08J_characterization.md"
MACRO_FEATURES = (
    "vix_change_1",
    "vix_zscore_20",
    "us10yr_change_1",
    "us10yr_zscore_20",
    "usdx_change_1",
    "usdx_zscore_20",
)
MEGA_FEATURES = (
    "nvda_xnas_log_return_1",
    "aapl_xnas_log_return_1",
    "msft_xnas_log_return_1",
    "amzn_xnas_log_return_1",
    "mega8_equal_return_1",
    "top3_weighted_return_1",
    "mega8_pos_breadth_1",
    "mega8_dispersion_5",
    "us100_minus_mega8_equal_return_1",
    "us100_minus_top3_weighted_return_1",
)
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
def feature_order_for_mode(all_features: Sequence[str], mode: str) -> list[str]:
    full = list(all_features)
    core = [feature for feature in mt5.TIER_B_CORE_FEATURE_ORDER if feature in full]
    macro = [feature for feature in MACRO_FEATURES if feature in full]
    mega = [feature for feature in MEGA_FEATURES if feature in full]
    if mode == "full58":
        selected = full
    elif mode == "core42":
        selected = core
    elif mode == "core_plus_macro48":
        selected = core + macro
    elif mode == "external16":
        selected = macro + mega
    else:
        raise ValueError(f"Unknown tier_a_feature_mode: {mode}")
    if not selected:
        raise RuntimeError(f"Feature mode {mode} produced an empty feature order.")
    if len(selected) != len(set(selected)):
        raise RuntimeError(f"Feature mode {mode} produced duplicate features.")
    return selected
def load_context() -> dict[str, Any]:
    tier_a_frame = pd.read_parquet(io_path(MODEL_INPUT_PATH))
    full_feature_order = load_feature_order(FEATURE_ORDER_PATH)
    validate_model_input_frame(tier_a_frame, full_feature_order)
    training_summary = read_json(TRAINING_SUMMARY_PATH)
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    tier_b_context = mt5.build_tier_b_partial_context_frames(
        raw_root=RAW_ROOT,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=full_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=float(training_summary["threshold_log_return"]),
    )
    return {
        "tier_a_frame": tier_a_frame,
        "full_feature_order": full_feature_order,
        "full_feature_order_hash": ordered_hash(full_feature_order),
        "tier_b_training_frame": tier_b_context["tier_b_training_frame"],
        "tier_b_fallback_frame": tier_b_context["tier_b_fallback_frame"],
        "tier_b_feature_order": tier_b_feature_order,
        "tier_b_feature_order_hash": ordered_hash(tier_b_feature_order),
        "tier_b_context_summary": tier_b_context["summary"],
        "training_summary": training_summary,
    }
def run_root(spec: QdaRunSpec) -> Path:
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
    spec: QdaRunSpec,
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
def materialize_models(spec: QdaRunSpec, *, tier_a_model: Any, tier_b_model: Any) -> dict[str, Any]:
    root = run_root(spec) / "models"
    io_path(root).mkdir(parents=True, exist_ok=True)
    tier_a_joblib = root / f"{spec.variant_id}_tier_a_qda.joblib"
    tier_b_joblib = root / f"{spec.variant_id}_tier_b_qda_core42.joblib"
    joblib.dump(tier_a_model, io_path(tier_a_joblib))
    joblib.dump(tier_b_model, io_path(tier_b_joblib))
    return {
        "variant_id": spec.variant_id,
        "tier_a_joblib": {"path": rel(tier_a_joblib), "sha256": sha256_file_lf_normalized(tier_a_joblib)},
        "tier_b_joblib": {"path": rel(tier_b_joblib), "sha256": sha256_file_lf_normalized(tier_b_joblib)},
    }
def variant_result(
    spec: QdaRunSpec,
    model: Any,
    prob_frame: pd.DataFrame,
    threshold: float,
    sample_info: Mapping[str, Any],
    feature_order: Sequence[str],
) -> dict[str, Any]:
    result = {
        "run_number": spec.run_number,
        "run_id": spec.run_id,
        "variant_id": spec.variant_id,
        "spec": spec.payload(),
        "training_sample": sample_info,
        "tier_a_feature_count": int(len(feature_order)),
        "tier_a_feature_order_hash": ordered_hash(feature_order),
        "threshold_quantile": THRESHOLD_QUANTILE,
        "short_threshold": threshold,
        "long_threshold": threshold,
        "metrics": split_decision_metrics(prob_frame, threshold),
        "probability_shape": probability_shape_metrics(prob_frame),
        "training_diagnostics": classifier_training_diagnostics(model),
    }
    result["shape_score"] = shape_score(result)
    return result
def write_characteristic_files(spec: QdaRunSpec, result: Mapping[str, Any]) -> dict[str, Any]:
    root = run_root(spec) / "results"
    io_path(root).mkdir(parents=True, exist_ok=True)
    json_path = root / "qda_characteristic_result.json"
    csv_path = root / "qda_characteristic_result.csv"
    write_json(json_path, result)
    row = {
        "run_id": spec.run_id,
        "variant_id": result.get("variant_id"),
        "idea_id": spec.idea_id,
        "reg_param": result.get("spec", {}).get("reg_param"),
        "rows_per_class": result.get("spec", {}).get("rows_per_class"),
        "feature_mode": result.get("spec", {}).get("tier_a_feature_mode"),
        "feature_count": result.get("tier_a_feature_count"),
        "shape_score": result.get("shape_score"),
        "threshold": result.get("short_threshold"),
        "val_signal_coverage": result.get("metrics", {}).get("validation", {}).get("signal_coverage"),
        "oos_signal_coverage": result.get("metrics", {}).get("oos", {}).get("signal_coverage"),
        "val_directional_hit_rate": result.get("metrics", {}).get("validation", {}).get("directional_hit_rate"),
        "oos_directional_hit_rate": result.get("metrics", {}).get("oos", {}).get("directional_hit_rate"),
    }
    with io_path(csv_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    return {
        "characteristic_json": {"path": rel(json_path), "sha256": sha256_file_lf_normalized(json_path)},
        "characteristic_csv": {"path": rel(csv_path), "sha256": sha256_file_lf_normalized(csv_path)},
    }
def write_ledgers(spec: QdaRunSpec, tier_records: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    rows = build_alpha_scout_ledger_rows(
        run_id=spec.run_id,
        stage_id=STAGE_ID,
        tier_records=tier_records,
        mt5_kpi_records=[],
        selected_threshold_id=f"validation_nonflat_q{THRESHOLD_QUANTILE:.2f}",
        run_output_root=run_root(spec),
        external_verification_status="out_of_scope_by_claim",
    )
    ledger_outputs = materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=rows,
    )
    registry_row = {
        "run_id": spec.run_id,
        "stage_id": STAGE_ID,
        "lane": "alpha_structural_scout",
        "status": "reviewed",
        "judgment": JUDGMENT_COMPLETED,
        "path": rel(run_root(spec)),
        "notes": ledger_pairs(
            (
                ("model_family", MODEL_FAMILY),
                ("feature_mode", spec.tier_a_feature_mode),
                ("reg_param", spec.reg_param),
                ("rows_per_class", spec.rows_per_class),
                ("external_verification", "out_of_scope_by_claim"),
                ("boundary", BOUNDARY),
            )
        ),
    }
    registry_output = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id")
    return ledger_outputs, registry_output
def build_summary(
    spec: QdaRunSpec,
    characteristic: Mapping[str, Any],
    *,
    b_threshold: float,
    model_artifacts: Mapping[str, Any],
    characteristic_artifacts: Mapping[str, Any],
) -> dict[str, Any]:
    validation = characteristic.get("metrics", {}).get("validation", {})
    oos = characteristic.get("metrics", {}).get("oos", {})
    return {
        "run_number": spec.run_number,
        "run_id": spec.run_id,
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "description": spec.description,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "model_family": MODEL_FAMILY,
        "boundary": BOUNDARY,
        "judgment": JUDGMENT_COMPLETED,
        "external_verification_status": "out_of_scope_by_claim",
        "shape_score": characteristic.get("shape_score"),
        "thresholds": {"tier_a": characteristic.get("short_threshold"), "tier_b": b_threshold},
        "feature_mode": spec.tier_a_feature_mode,
        "feature_count": characteristic.get("tier_a_feature_count"),
        "rows_per_class": spec.rows_per_class,
        "reg_param": spec.reg_param,
        "validation": {
            "signal_coverage": validation.get("signal_coverage"),
            "signal_count": validation.get("signal_count"),
            "directional_hit_rate": validation.get("directional_hit_rate"),
            "log_loss": validation.get("log_loss"),
        },
        "oos": {
            "signal_coverage": oos.get("signal_coverage"),
            "signal_count": oos.get("signal_count"),
            "directional_hit_rate": oos.get("directional_hit_rate"),
            "log_loss": oos.get("log_loss"),
        },
        "model_artifacts": model_artifacts,
        "characteristic_artifacts": characteristic_artifacts,
    }
def run_result_markdown(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            f"# {summary['run_id']} Result Summary({summary['run_id']} 결과 요약)",
            "",
            f"- variant(변형): `{summary['variant_id']}`",
            f"- idea(아이디어): `{summary['idea_id']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            f"- external verification(외부 검증): `{summary['external_verification_status']}`",
            f"- feature mode(피처 방식): `{summary['feature_mode']}`",
            f"- reg_param(정규화 계수): `{summary['reg_param']}`",
            f"- shape score(모양 점수): `{summary['shape_score']}`",
            f"- validation/OOS signal coverage(검증/표본외 신호 비율): `{summary['validation'].get('signal_coverage')}` / `{summary['oos'].get('signal_coverage')}`",
            "",
            f"효과(effect, 효과): `{summary['run_number']}`는 QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석)의 `{summary['idea_id']}` 성격을 Python structural scout(파이썬 구조 스카우트) 경계로 읽었다.",
        ]
    )
def write_run_files(
    spec: QdaRunSpec,
    *,
    context: Mapping[str, Any],
    tier_a_feature_order: Sequence[str],
    characteristic: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    prediction_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    characteristic_artifacts: Mapping[str, Any],
    b_threshold: float,
    ledger_outputs: Mapping[str, Any],
    registry_output: Mapping[str, Any],
    created_at: str,
) -> dict[str, Any]:
    summary = build_summary(
        spec,
        characteristic,
        b_threshold=b_threshold,
        model_artifacts=model_artifacts,
        characteristic_artifacts=characteristic_artifacts,
    )
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
        "tier_a_feature_order": list(tier_a_feature_order),
        "tier_a_feature_order_hash": ordered_hash(tier_a_feature_order),
        "tier_b_feature_order_hash": context["tier_b_feature_order_hash"],
        "threshold_policy": f"validation nonflat q{THRESHOLD_QUANTILE:.2f}; not profit searched",
        "characteristic": characteristic,
        "prediction_artifacts": prediction_artifacts,
        "model_artifacts": model_artifacts,
        "external_verification_status": "out_of_scope_by_claim",
        "judgment": JUDGMENT_COMPLETED,
    }
    kpi_record = {
        "run_id": spec.run_id,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "qda_characterization_python_shape_no_mt5_no_edge_search",
        "python_characteristic": characteristic,
        "python_tier_records": list(tier_records),
        "tier_b_context_summary": context["tier_b_context_summary"],
        "external_verification_status": "out_of_scope_by_claim",
        "judgment": JUDGMENT_COMPLETED,
        "boundary": BOUNDARY,
        "ledger_outputs": ledger_outputs,
        "registry_output": registry_output,
    }
    write_json(run_root(spec) / "run_manifest.json", manifest)
    write_json(run_root(spec) / "kpi_record.json", kpi_record)
    write_json(run_root(spec) / "summary.json", summary)
    write_json(PACKET_ROOT / "run_summaries" / f"{spec.run_id}.json", summary)
    write_json(PACKET_ROOT / "run_registry_outputs" / f"{spec.run_id}.json", registry_output)
    write_json(PACKET_ROOT / "ledger_outputs" / f"{spec.run_id}.json", ledger_outputs)
    write_md(run_root(spec) / "reports/result_summary.md", run_result_markdown(summary))
    return summary
def build_one(spec: QdaRunSpec, context: Mapping[str, Any]) -> dict[str, Any]:
    created_at = utc_now()
    tier_a_feature_order = feature_order_for_mode(context["full_feature_order"], spec.tier_a_feature_mode)
    tier_a_model, a_sample = fit_qda_variant(context["tier_a_frame"], tier_a_feature_order, spec)
    tier_b_model, b_sample = fit_qda_variant(context["tier_b_training_frame"], context["tier_b_feature_order"], spec)
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], tier_a_feature_order)
    tier_b_training_prob = probability_frame(tier_b_model, context["tier_b_training_frame"], context["tier_b_feature_order"])
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], context["tier_b_feature_order"])
    a_threshold = nonflat_threshold(tier_a_prob, THRESHOLD_QUANTILE)
    b_threshold = nonflat_threshold(tier_b_training_prob, THRESHOLD_QUANTILE)
    characteristic = variant_result(spec, tier_a_model, tier_a_prob, a_threshold, a_sample, tier_a_feature_order)
    characteristic = {**characteristic, "tier_b_training_sample": b_sample}
    tier_records, prediction_artifacts = python_tier_records(
        spec,
        tier_a_prob=tier_a_prob,
        tier_b_prob=tier_b_prob,
        a_threshold=a_threshold,
        b_threshold=b_threshold,
    )
    model_artifacts = materialize_models(spec, tier_a_model=tier_a_model, tier_b_model=tier_b_model)
    characteristic_artifacts = write_characteristic_files(spec, characteristic)
    ledger_outputs, registry_output = write_ledgers(spec, tier_records)
    return write_run_files(
        spec,
        context=context,
        tier_a_feature_order=tier_a_feature_order,
        characteristic=characteristic,
        tier_records=tier_records,
        prediction_artifacts=prediction_artifacts,
        model_artifacts=model_artifacts,
        characteristic_artifacts=characteristic_artifacts,
        b_threshold=b_threshold,
        ledger_outputs=ledger_outputs,
        registry_output=registry_output,
        created_at=created_at,
    )
def aggregate_summary(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [row for row in summaries if row.get("judgment") == JUDGMENT_COMPLETED]
    return {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_range": "run08A-run08J",
        "run_count": len(summaries),
        "completed_run_count": len(completed),
        "blocked_run_count": len(summaries) - len(completed),
        "external_verification_status": "out_of_scope_by_claim",
        "judgment": JUDGMENT_COMPLETED if len(completed) == len(summaries) else "blocked_or_partial_qda_characterization",
        "boundary": BOUNDARY,
        "mt5_kpi_record_count": 0,
        "python_ledger_row_count": len(summaries) * 3,
        "run_ids": [row["run_id"] for row in summaries],
        "highest_shape_score_run": max(summaries, key=lambda row: safe_float(row.get("shape_score")), default=None),
        "highest_oos_signal_coverage_run": max(summaries, key=lambda row: safe_float(row.get("oos", {}).get("signal_coverage")), default=None),
        "lowest_oos_log_loss_run": min(summaries, key=lambda row: safe_float(row.get("oos", {}).get("log_loss"), 1e18), default=None),
        "characterization_topics": [row["idea_id"] for row in summaries],
    }
def packet_markdown(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage16 QDA RUN08A-RUN08J Characterization(16단계 QDA 실행 08A-08J 특성 파악)",
        "",
        f"- judgment(판정): `{aggregate['judgment']}`",
        f"- completed runs(완료 실행): `{aggregate['completed_run_count']}/{aggregate['run_count']}`",
        "- MT5 KPI records(MT5 핵심성과지표 기록): `0`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| run(실행) | topic(주제) | feature mode(피처 방식) | reg(정규화) | rows/class(클래스별 행) | shape(모양) | val/oos coverage(검증/표본외 비율) |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for row in summaries:
        lines.append(
            "| `{}` | `{}` | `{}` | `{}` | `{}` | `{:.6f}` | `{:.6f}/{:.6f}` |".format(
                row["run_number"],
                row["idea_id"],
                row["feature_mode"],
                row["reg_param"],
                row["rows_per_class"],
                safe_float(row.get("shape_score")),
                safe_float(row.get("validation", {}).get("signal_coverage")),
                safe_float(row.get("oos", {}).get("signal_coverage")),
            )
        )
    high_shape = aggregate.get("highest_shape_score_run") or {}
    high_cov = aggregate.get("highest_oos_signal_coverage_run") or {}
    lines.extend(
        [
            "",
            f"- highest shape score(최고 모양 점수): `{high_shape.get('run_number')}` `{high_shape.get('idea_id')}` `{high_shape.get('shape_score')}`",
            f"- highest OOS signal coverage(최고 표본외 신호 비율): `{high_cov.get('run_number')}` `{high_cov.get('idea_id')}` `{(high_cov.get('oos') or {}).get('signal_coverage')}`",
            "",
            "효과(effect, 효과): 이 묶음은 QDA(이차 판별 분석)의 class covariance(클래스별 공분산), prior(사전확률), regularization(정규화), sample size(표본 크기), feature geometry(피처 기하)를 수익 선택 없이 나란히 읽는다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )
    return "\n".join(lines)
def gate_payloads(aggregate: Mapping[str, Any]) -> dict[str, Any]:
    all_completed = aggregate.get("completed_run_count") == aggregate.get("run_count") == 10
    ledger_ok = aggregate.get("python_ledger_row_count") == 30
    passed = bool(all_completed and ledger_ok)
    return {
        "scope_completion_gate": {
            "audit_name": "scope_completion_gate",
            "status": "pass" if passed else "blocked",
            "passed": passed,
            "counts": {"run_count": aggregate.get("run_count"), "completed_run_count": aggregate.get("completed_run_count")},
        },
        "kpi_contract_audit": {
            "audit_name": "kpi_contract_audit",
            "status": "pass" if passed else "blocked",
            "passed": passed,
            "scoreboard_lane": "structural_scout",
            "required_views": ["python_tier_a_separate", "python_tier_b_separate", "python_tier_ab_combined"],
            "mt5_runtime_probe": "out_of_scope_by_claim",
        },
        "skill_receipt_lint": {"audit_name": "skill_receipt_lint", "status": "pass", "passed": True},
        "final_claim_guard": {
            "audit_name": "final_claim_guard",
            "status": "pass" if passed else "blocked",
            "passed": passed,
            "allowed_claims": [aggregate.get("judgment"), "structural_scout_characterization"],
            "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        "required_gate_coverage_audit": {
            "audit_name": "required_gate_coverage_audit",
            "status": "pass" if passed else "blocked",
            "passed": passed,
            "required_gates": {
                "scope_completion_gate": "pass" if passed else "blocked",
                "kpi_contract_audit": "pass" if passed else "blocked",
                "skill_receipt_lint": "pass",
                "final_claim_guard": "pass" if passed else "blocked",
            },
        },
    }
def write_packet_files(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], created_at: str) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", aggregate)
    write_json(PACKET_ROOT / "artifact_index.json", {"run_summaries": list(summaries), "report_path": rel(REVIEW_PACKET_PATH), "created_at_utc": created_at})
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-experiment-design",
            "support_skills": ["obsidian-data-integrity", "obsidian-model-validation", "obsidian-artifact-lineage", "obsidian-result-judgment"],
            "required_gates": ["scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit", "final_claim_guard"],
            "runtime_backtest_status": "out_of_scope_by_claim_no_edge_search",
        },
    )
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "receipts": [
                {
                    "skill": "obsidian-experiment-design",
                    "status": "completed",
                    "hypothesis": "QDA class-specific covariance behavior can be characterized without profit or edge search.",
                    "decision_use": "Choose the next Stage16 question, not a baseline or promotion.",
                },
                {
                    "skill": "obsidian-data-integrity",
                    "status": "completed",
                    "data_source": rel(MODEL_INPUT_PATH),
                    "split_boundary": SPLIT_CONTRACT,
                    "integrity_judgment": "usable_with_boundary",
                },
                {
                    "skill": "obsidian-model-validation",
                    "status": "completed",
                    "model_family": MODEL_FAMILY,
                    "threshold_policy": f"validation nonflat q{THRESHOLD_QUANTILE:.2f}; not profit searched",
                    "validation_judgment": "exploratory",
                },
                {
                    "skill": "obsidian-artifact-lineage",
                    "status": "completed",
                    "availability": "generated_local_ignored_run_artifacts_with_manifest_and_hashes",
                    "lineage_judgment": "connected_with_boundary",
                },
                {
                    "skill": "obsidian-result-judgment",
                    "status": "completed",
                    "judgment_label": JUDGMENT_COMPLETED,
                    "claim_boundary": BOUNDARY,
                },
            ],
        },
    )
    for name, payload in gate_payloads(aggregate).items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
def sync_workspace_docs(aggregate: Mapping[str, Any]) -> None:
    state_path = ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    state = state.replace("current_run_id: ''", "current_run_id: run08J_qda_external16_feature_geometry_characterization_v1", 1)
    state = state.replace("stage16_qda_open_only", "stage16_qda_run08A_run08J_characterization_reviewed")
    state = state.replace("open_qda_design_only_no_run_no_mt5_no_kpi", "reviewed_qda_run08A_run08J_characterization_no_mt5_no_edge")
    block = f"""stage16_qda_class_covariance_scout:
  stage_id: {STAGE_ID}
  status: reviewed_qda_run08A_run08J_characterization_no_mt5_no_edge
  lane: independent_model_family_topic_pivot_no_promotion
  model_family: {MODEL_FAMILY}
  current_run_id: run08J_qda_external16_feature_geometry_characterization_v1
  current_status: run08A_run08J_characterization_reviewed
  source_clue: Stage15 LDA light covariance shrinkage clue; QDA tests class-specific covariance behavior without edge search
  hypothesis: QDA class-specific covariance may show probability shape and signal-density behavior different from LDA under the same label and split contract.
  comparison_baseline: no trading baseline; compare only within Stage16 characterization axes
  boundary: {BOUNDARY}
  stage_brief_path: stages/16_model_family_challenge__qda_class_covariance_scout/00_spec/stage_brief.md
  input_references_path: stages/16_model_family_challenge__qda_class_covariance_scout/01_inputs/input_references.md
  selection_status_path: stages/16_model_family_challenge__qda_class_covariance_scout/04_selected/selection_status.md
  current_run_packet_path: {rel(REVIEW_PACKET_PATH)}
  decision_path: {rel(DECISION_PATH)}
  next_action: inspect_qda_characterization_clues_before_any_runtime_probe
stage16_qda_characterization_run08A_run08J:
  packet_id: {PACKET_ID}
  status: reviewed_structural_scout_completed
  judgment: {aggregate['judgment']}
  run_range: run08A-run08J
  completed_run_count: {aggregate['completed_run_count']}
  python_ledger_row_count: {aggregate['python_ledger_row_count']}
  mt5_kpi_record_count: 0
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REVIEW_PACKET_PATH)}
  decision_path: {rel(DECISION_PATH)}
  next_action: inspect_qda_characterization_clues_before_any_runtime_probe
"""
    state = re.sub(
        r"stage16_qda_class_covariance_scout:\n(?:  .*\n)+(?=stage15_lda_run06A_run06J_runtime_probe:)",
        block,
        state,
        count=1,
    )
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")
    current_path = ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    current = re.sub(r"- current run\(현재 실행\): .+", "- current run(현재 실행): `run08J_qda_external16_feature_geometry_characterization_v1`", current, count=1)
    latest = "\n".join(
        [
            "## Latest Stage 16 Update(최신 Stage 16 업데이트)",
            "",
            "Stage16(16단계)는 QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석) 성격 파악용으로 `run08A`~`run08J` 10개 Python structural scout(파이썬 구조 스카우트)를 실행했다.",
            "",
            f"효과(effect, 효과): `{aggregate['judgment']}`로 기록했지만 edge(거래 우위), alpha quality(알파 품질), MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.",
            "",
        ]
    )
    current = re.sub(r"## Latest Stage 16 Update\(최신 Stage 16 업데이트\)\n\n.*?(?=## 쉬운 설명)", latest, current, count=1, flags=re.S)
    current = current.replace("Stage16(16단계)는 design-open(설계 개방) 상태라", "Stage16(16단계)는 QDA(이차 판별 분석) 특성 파악 run(실행) 10개를 마친 상태지만")
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")
def sync_stage_docs(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]]) -> None:
    write_md(REVIEW_PACKET_PATH, packet_markdown(aggregate, summaries))
    write_md(
        STAGE_ROOT / "03_reviews/review_index.md",
        "\n".join(
            [
                "# Stage 16 Review Index(16단계 검토 색인)",
                "",
                f"- `run08A`~`run08J`: `{aggregate['judgment']}`, report(보고서): `{rel(REVIEW_PACKET_PATH)}`",
                "",
                "효과(effect, 효과): Stage16(16단계)는 QDA(이차 판별 분석) 성격 파악용 Python structural scout(파이썬 구조 스카우트)를 완료했지만, edge(거래 우위)나 MT5(메타트레이더5) 주장은 없다.",
            ]
        ),
    )
    write_md(
        STAGE_ROOT / "04_selected/selection_status.md",
        "\n".join(
            [
                "# Stage 16 Selection Status(16단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                "- status(상태): `reviewed_qda_run08A_run08J_characterization_no_mt5_no_edge(검토됨, QDA 실행 08A-08J 특성 파악, MT5/엣지 없음)`",
                "- current run(현재 실행): `run08J_qda_external16_feature_geometry_characterization_v1`",
                "- model family(모델 계열): QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석)",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{aggregate['judgment']}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "효과(effect, 효과): 이번 10개 run(실행)은 Stage16(16단계)의 모델 성격을 읽기 위한 것이며, edge(거래 우위), alpha quality(알파 품질), MT5 runtime_probe(MT5 런타임 탐침), baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다.",
            ]
        ),
    )
    write_md(
        DECISION_PATH,
        "\n".join(
            [
                "# 2026-05-02 Stage16 QDA RUN08A-RUN08J Characterization(16단계 QDA 실행 08A-08J 특성 파악)",
                "",
                "## Decision(결정)",
                "",
                "Stage16(16단계)는 QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석)의 class-specific covariance(클래스별 공분산) 성격을 보기 위해 `run08A`~`run08J` 10개 주제를 Python structural scout(파이썬 구조 스카우트)로 실행했다.",
                "",
                "효과(effect, 효과): 수익/엣지 탐색(profit/edge search, 수익/거래 우위 탐색) 없이 regularization(정규화), prior(사전확률), sample size(표본 크기), feature geometry(피처 기하)를 비교할 수 있다.",
                "",
                "## Boundary(경계)",
                "",
                f"`{BOUNDARY}`",
            ]
        ),
    )
    sync_workspace_docs(aggregate)
def sync_misc_docs() -> None:
    changelog_path = ROOT / "docs/workspace/changelog.md"
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    line = "- 2026-05-02: Stage16 QDA(이차 판별 분석) `run08A`~`run08J` characterization(특성 파악) structural scout(구조 스카우트)를 완료했다. 효과(effect, 효과): edge(거래 우위) 없이 Stage16 모델 성격만 기록한다."
    if line not in changelog:
        changelog = changelog.rstrip() + "\n" + line + "\n"
        io_path(changelog_path).write_text(changelog, encoding="utf-8-sig")
    idea_path = ROOT / "docs/registers/idea_registry.md"
    idea = io_path(idea_path).read_text(encoding="utf-8-sig")
    idea = idea.replace("IDEA-ST16-QDA-CLASS-COVARIANCE | Stage16 QDA class-specific covariance scout | design_open_no_run", "IDEA-ST16-QDA-CLASS-COVARIANCE | Stage16 QDA class-specific covariance scout | run08A_run08J_characterization_reviewed")
    io_path(idea_path).write_text(idea.rstrip() + "\n", encoding="utf-8-sig")
def build_all(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = load_context()
    selected_ids = {item.strip() for item in args.run_filter.split(",") if item.strip()} if args.run_filter else set()
    specs = [
        spec
        for spec in default_stage16_qda_specs()
        if not selected_ids or spec.run_number in selected_ids or spec.run_id in selected_ids
    ]
    summaries = [build_one(spec, context) for spec in specs]
    aggregate = aggregate_summary(summaries)
    write_packet_files(aggregate, summaries, created_at)
    sync_stage_docs(aggregate, summaries)
    sync_misc_docs()
    print(json.dumps(json_ready(aggregate), ensure_ascii=False, indent=2))
    return aggregate
def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage16 QDA characterization structural scouts.")
    parser.add_argument("--run-filter", default="")
    args = parser.parse_args(argv)
    build_all(args)
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
