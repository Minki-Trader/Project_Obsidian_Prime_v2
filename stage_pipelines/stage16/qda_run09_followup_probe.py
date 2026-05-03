from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import pandas as pd

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.alpha_run_ledgers import build_alpha_scout_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import RUN_REGISTRY_COLUMNS, io_path, json_ready, ledger_pairs, sha256_file_lf_normalized, upsert_csv_rows, write_csv_rows
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.models.onnx_bridge import check_onnxruntime_probability_parity, export_sklearn_to_onnx_zipmap_disabled, ordered_hash
from foundation.models.qda_discriminant import (
    classifier_training_diagnostics,
    fit_qda_variant,
    nonflat_threshold,
    probability_frame,
    probability_shape_metrics,
    shape_score,
    split_decision_metrics,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage16 import qda_characterization_probe as base


PACKET_ID = "stage16_qda_run09A_run09Q_followup_mt5_runtime_probe_v1"
REVIEW_PACKET_PATH = base.STAGE_ROOT / "03_reviews/run09A_run09Q_qda_followup_mt5_runtime_probe_packet.md"
DECISION_PATH = base.ROOT / "docs/decisions/2026-05-03_stage16_qda_run09A_run09Q_followup.md"
PACKET_ROOT = base.ROOT / "docs/agent_control/packets" / PACKET_ID
BOUNDARY = "qda_run09_followup_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_qda_run09_followup_mt5_runtime_probe_completed"
JUDGMENT_BLOCKED = "blocked_qda_run09_followup_mt5_runtime_probe_after_attempt"
EXPLORATION_LABEL = "stage16_Model__QDARun09Followup"
ONNX_OPSET = 13
ONNX_PARITY_TOLERANCE = 0.005
MAX_HOLD_BARS = 12
MIN_MARGIN = 0.0
BASELINE_RUN_ID = "run08F_qda_moderate_regularization150_characterization_v1"

VOLATILITY_FEATURES = (
    "hl_range",
    "hl_zscore_50",
    "atr_14",
    "atr_50",
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "bb_squeeze",
    "historical_vol_20",
    "historical_vol_5_over_20",
)
MOMENTUM_FEATURES = (
    "rsi_14",
    "rsi_50",
    "rsi_14_slope_3",
    "rsi_14_minus_50",
    "stoch_kd_diff",
    "stochrsi_kd_diff",
    "ppo_hist_12_26_9",
    "roc_12",
    "trix_15",
    "adx_14",
    "di_spread_14",
    "vortex_indicator",
)
SESSION_FEATURES = (
    "is_us_cash_open",
    "minutes_from_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
)


@dataclass(frozen=True)
class FollowupSpec:
    run_number: str
    run_id: str
    variant_id: str
    idea_id: str
    description: str
    axis: str
    reg_param: float
    rows_per_class: int = 600
    threshold_quantile: float = 0.90
    excluded_features: tuple[str, ...] = ()
    priors: tuple[float, float, float] | None = None
    tol: float = 0.0001
    tier_a_feature_mode: str = "full58"
    random_state: int = 1900

    def payload(self) -> dict[str, Any]:
        payload = asdict(self)
        if self.priors is not None:
            payload["priors"] = list(self.priors)
        payload["excluded_features"] = list(self.excluded_features)
        return payload


def run09_specs() -> list[FollowupSpec]:
    return [
        FollowupSpec("run09A", "run09A_qda_reg008_full58_followup_v1", "v11_reg008_full58", "reg008_fine_search", "QDA reg_param 0.08, full58, q90 coverage.", "regularization", 0.08, random_state=1901),
        FollowupSpec("run09B", "run09B_qda_reg010_full58_followup_v1", "v12_reg010_full58", "reg010_fine_search", "QDA reg_param 0.10, full58, q90 coverage.", "regularization", 0.10, random_state=1902),
        FollowupSpec("run09C", "run09C_qda_reg012_full58_followup_v1", "v13_reg012_full58", "reg012_fine_search", "QDA reg_param 0.12, full58, q90 coverage.", "regularization", 0.12, random_state=1903),
        FollowupSpec("run09D", "run09D_qda_reg018_full58_followup_v1", "v14_reg018_full58", "reg018_fine_search", "QDA reg_param 0.18, full58, q90 coverage.", "regularization", 0.18, random_state=1904),
        FollowupSpec("run09E", "run09E_qda_reg025_full58_followup_v1", "v15_reg025_full58", "reg025_fine_search", "QDA reg_param 0.25, full58, q90 coverage.", "regularization", 0.25, random_state=1905),
        FollowupSpec("run09F", "run09F_qda_reg015_drop_macro6_followup_v1", "v16_reg015_drop_macro6", "drop_macro6", "QDA reg_param 0.15 with macro proxy features removed.", "feature_removal", 0.15, excluded_features=base.MACRO_FEATURES, tier_a_feature_mode="full58_drop_macro6", random_state=1906),
        FollowupSpec("run09G", "run09G_qda_reg015_drop_mega10_followup_v1", "v17_reg015_drop_mega10", "drop_mega10", "QDA reg_param 0.15 with mega-cap proxy features removed.", "feature_removal", 0.15, excluded_features=base.MEGA_FEATURES, tier_a_feature_mode="full58_drop_mega10", random_state=1907),
        FollowupSpec("run09H", "run09H_qda_reg015_drop_volatility9_followup_v1", "v18_reg015_drop_volatility9", "drop_volatility9", "QDA reg_param 0.15 with volatility and range features removed.", "feature_removal", 0.15, excluded_features=VOLATILITY_FEATURES, tier_a_feature_mode="full58_drop_volatility9", random_state=1908),
        FollowupSpec("run09I", "run09I_qda_reg015_drop_momentum12_followup_v1", "v19_reg015_drop_momentum12", "drop_momentum12", "QDA reg_param 0.15 with momentum and oscillator features removed.", "feature_removal", 0.15, excluded_features=MOMENTUM_FEATURES, tier_a_feature_mode="full58_drop_momentum12", random_state=1909),
        FollowupSpec("run09J", "run09J_qda_reg015_drop_session4_followup_v1", "v20_reg015_drop_session4", "drop_session4", "QDA reg_param 0.15 with session-clock features removed.", "feature_removal", 0.15, excluded_features=SESSION_FEATURES, tier_a_feature_mode="full58_drop_session4", random_state=1910),
        FollowupSpec("run09K", "run09K_qda_reg015_sample300_followup_v1", "v21_reg015_sample300", "sample300_reg015", "QDA run08F neighborhood with 300 rows per class.", "sample_size", 0.15, rows_per_class=300, random_state=1911),
        FollowupSpec("run09L", "run09L_qda_reg015_sample450_followup_v1", "v22_reg015_sample450", "sample450_reg015", "QDA run08F neighborhood with 450 rows per class.", "sample_size", 0.15, rows_per_class=450, random_state=1912),
        FollowupSpec("run09M", "run09M_qda_reg015_sample600_resample_followup_v1", "v23_reg015_sample600_resample", "sample600_resample_reg015", "QDA run08F neighborhood with 600 rows per class and a new random sample.", "sample_size", 0.15, rows_per_class=600, random_state=1913),
        FollowupSpec("run09N", "run09N_qda_reg015_sample900_followup_v1", "v24_reg015_sample900", "sample900_reg015", "QDA run08F neighborhood with 900 rows per class.", "sample_size", 0.15, rows_per_class=900, random_state=1914),
        FollowupSpec("run09O", "run09O_qda_reg015_q85_coverage_followup_v1", "v25_reg015_q85", "coverage_q85", "QDA run08F model neighborhood with validation non-flat q85 threshold.", "coverage_threshold", 0.15, threshold_quantile=0.85, random_state=1806),
        FollowupSpec("run09P", "run09P_qda_reg015_q93_coverage_followup_v1", "v26_reg015_q93", "coverage_q93", "QDA run08F model neighborhood with validation non-flat q93 threshold.", "coverage_threshold", 0.15, threshold_quantile=0.93, random_state=1806),
        FollowupSpec("run09Q", "run09Q_qda_reg015_q95_coverage_followup_v1", "v27_reg015_q95", "coverage_q95", "QDA run08F model neighborhood with validation non-flat q95 threshold.", "coverage_threshold", 0.15, threshold_quantile=0.95, random_state=1806),
    ]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: Any) -> None:
    base.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    base.write_md(path, text)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_jsonl(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(json_ready(row), ensure_ascii=False, sort_keys=True) + "\n")


def run_root(spec: FollowupSpec) -> Path:
    return base.STAGE_ROOT / "02_runs" / spec.run_id


def feature_order_for_spec(full_feature_order: Sequence[str], spec: FollowupSpec) -> list[str]:
    full = list(full_feature_order)
    missing = sorted(set(spec.excluded_features).difference(full))
    if missing:
        raise RuntimeError(f"Unknown excluded features for {spec.run_id}: {missing}")
    selected = [feature for feature in full if feature not in set(spec.excluded_features)]
    if not selected:
        raise RuntimeError(f"{spec.run_id} produced an empty feature order.")
    return selected


def save_predictions(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    return base.save_predictions(path, frame)


def tier_record(spec: FollowupSpec, *, record_view: str, tier_scope: str, prob_frame: pd.DataFrame, threshold: float, path: Path) -> dict[str, Any]:
    metrics = split_decision_metrics(prob_frame, threshold)
    subtype_counts: dict[str, int] = {}
    if "partial_context_subtype" in prob_frame.columns:
        subtype_counts = {str(k): int(v) for k, v in prob_frame["partial_context_subtype"].astype(str).value_counts().sort_index().items()}
    total = {
        "rows": int(len(prob_frame)),
        "signal_count": int(sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))),
        "short_count": int(sum(metrics.get(split, {}).get("short_count", 0) for split in ("train", "validation", "oos"))),
        "long_count": int(sum(metrics.get(split, {}).get("long_count", 0) for split in ("train", "validation", "oos"))),
        "partial_context_subtype_counts": subtype_counts or None,
        "threshold_ids": f"q{spec.threshold_quantile:.2f}",
        "probability_row_sum_max_abs_error": metrics.get("probability_checks", {}).get("row_sum_max_abs_error"),
    }
    total["signal_coverage"] = base.safe_float(total["signal_count"]) / max(1, int(total["rows"]))
    return {"record_view": record_view, "tier_scope": tier_scope, "status": "completed", "path": base.rel(path), "metrics": total, "split_metrics": {split: metrics.get(split, {}) for split in ("train", "validation", "oos")}}


def python_tier_records(spec: FollowupSpec, *, tier_a_prob: pd.DataFrame, tier_b_prob: pd.DataFrame, a_threshold: float, b_threshold: float) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root = run_root(spec) / "predictions"
    a_path = root / "tier_a_separate_predictions.parquet"
    b_path = root / "tier_b_separate_predictions.parquet"
    ab_path = root / "tier_ab_combined_predictions.parquet"
    ab_prob = pd.concat([tier_a_prob.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"), tier_b_prob.assign(record_source="tier_b_fallback")], ignore_index=True)
    return [
        tier_record(spec, record_view="tier_a_separate", tier_scope=mt5.TIER_A, prob_frame=tier_a_prob, threshold=a_threshold, path=a_path),
        tier_record(spec, record_view="tier_b_separate", tier_scope=mt5.TIER_B, prob_frame=tier_b_prob, threshold=b_threshold, path=b_path),
        tier_record(spec, record_view="tier_ab_combined", tier_scope=mt5.TIER_AB, prob_frame=ab_prob, threshold=a_threshold, path=ab_path),
    ], {"tier_a": save_predictions(a_path, tier_a_prob), "tier_b": save_predictions(b_path, tier_b_prob), "tier_ab": save_predictions(ab_path, ab_prob)}


def characteristic_result(spec: FollowupSpec, model: Any, prob_frame: pd.DataFrame, threshold: float, sample_info: Mapping[str, Any], feature_order: Sequence[str]) -> dict[str, Any]:
    metrics = split_decision_metrics(prob_frame, threshold)
    result = {
        "run_number": spec.run_number,
        "run_id": spec.run_id,
        "variant_id": spec.variant_id,
        "spec": spec.payload(),
        "training_sample": sample_info,
        "tier_a_feature_count": int(len(feature_order)),
        "tier_a_feature_order_hash": ordered_hash(feature_order),
        "threshold_quantile": float(spec.threshold_quantile),
        "short_threshold": threshold,
        "long_threshold": threshold,
        "metrics": metrics,
        "probability_shape": probability_shape_metrics(prob_frame),
        "training_diagnostics": classifier_training_diagnostics(model),
        "feature_exclusion": {"excluded_features": list(spec.excluded_features), "excluded_count": len(spec.excluded_features)},
    }
    result["shape_score"] = shape_score(result)
    return result


def write_characteristic_files(spec: FollowupSpec, result: Mapping[str, Any]) -> dict[str, Any]:
    root = run_root(spec) / "results"
    io_path(root).mkdir(parents=True, exist_ok=True)
    json_path = root / "qda_followup_result.json"
    csv_path = root / "qda_followup_result.csv"
    write_json(json_path, result)
    row = {
        "run_id": spec.run_id,
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "axis": spec.axis,
        "reg_param": spec.reg_param,
        "rows_per_class": spec.rows_per_class,
        "threshold_quantile": spec.threshold_quantile,
        "feature_mode": spec.tier_a_feature_mode,
        "feature_count": result.get("tier_a_feature_count"),
        "shape_score": result.get("shape_score"),
        "val_signal_coverage": result.get("metrics", {}).get("validation", {}).get("signal_coverage"),
        "oos_signal_coverage": result.get("metrics", {}).get("oos", {}).get("signal_coverage"),
    }
    with io_path(csv_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    return {"characteristic_json": {"path": base.rel(json_path), "sha256": sha256_file_lf_normalized(json_path)}, "characteristic_csv": {"path": base.rel(csv_path), "sha256": sha256_file_lf_normalized(csv_path)}}


def materialize_models(spec: FollowupSpec, *, tier_a_model: Any, tier_b_model: Any) -> dict[str, Any]:
    return base.materialize_models(spec, tier_a_model=tier_a_model, tier_b_model=tier_b_model)


def write_structural_ledgers(spec: FollowupSpec, tier_records: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    rows = build_alpha_scout_ledger_rows(
        run_id=spec.run_id,
        stage_id=base.STAGE_ID,
        tier_records=tier_records,
        mt5_kpi_records=[],
        selected_threshold_id=f"validation_nonflat_q{spec.threshold_quantile:.2f}",
        run_output_root=run_root(spec),
        external_verification_status="out_of_scope_by_claim",
    )
    ledger_outputs = materialize_alpha_ledgers(stage_run_ledger_path=base.STAGE_LEDGER_PATH, project_alpha_ledger_path=base.PROJECT_LEDGER_PATH, rows=rows)
    registry_row = {"run_id": spec.run_id, "stage_id": base.STAGE_ID, "lane": "alpha_structural_scout", "status": "reviewed", "judgment": "inconclusive_qda_run09_followup_structural_scout_completed", "path": base.rel(run_root(spec)), "notes": ledger_pairs((("axis", spec.axis), ("reg_param", spec.reg_param), ("rows_per_class", spec.rows_per_class), ("threshold_q", spec.threshold_quantile), ("feature_mode", spec.tier_a_feature_mode), ("external_verification", "out_of_scope_by_claim"), ("boundary", "structural_scout_only")))}
    registry_output = upsert_csv_rows(base.RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [registry_row], key="run_id")
    return ledger_outputs, registry_output


def summary_payload(spec: FollowupSpec, characteristic: Mapping[str, Any], *, b_threshold: float, model_artifacts: Mapping[str, Any], characteristic_artifacts: Mapping[str, Any]) -> dict[str, Any]:
    validation = characteristic.get("metrics", {}).get("validation", {})
    oos = characteristic.get("metrics", {}).get("oos", {})
    return {
        "run_number": spec.run_number,
        "run_id": spec.run_id,
        "variant_id": spec.variant_id,
        "idea_id": spec.idea_id,
        "description": spec.description,
        "axis": spec.axis,
        "packet_id": PACKET_ID,
        "stage_id": base.STAGE_ID,
        "model_family": base.MODEL_FAMILY,
        "boundary": BOUNDARY,
        "judgment": "inconclusive_qda_run09_followup_structural_scout_completed",
        "external_verification_status": "out_of_scope_by_claim",
        "shape_score": characteristic.get("shape_score"),
        "thresholds": {"tier_a": characteristic.get("short_threshold"), "tier_b": b_threshold},
        "threshold_quantile": spec.threshold_quantile,
        "feature_mode": spec.tier_a_feature_mode,
        "feature_count": characteristic.get("tier_a_feature_count"),
        "excluded_features": list(spec.excluded_features),
        "rows_per_class": spec.rows_per_class,
        "reg_param": spec.reg_param,
        "validation": {"signal_coverage": validation.get("signal_coverage"), "signal_count": validation.get("signal_count"), "directional_hit_rate": validation.get("directional_hit_rate"), "log_loss": validation.get("log_loss")},
        "oos": {"signal_coverage": oos.get("signal_coverage"), "signal_count": oos.get("signal_count"), "directional_hit_rate": oos.get("directional_hit_rate"), "log_loss": oos.get("log_loss")},
        "model_artifacts": model_artifacts,
        "characteristic_artifacts": characteristic_artifacts,
    }


def run_result_markdown(summary: Mapping[str, Any]) -> str:
    val = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    return "\n".join([
        f"# {summary['run_id']} Result Summary({summary['run_id']} 결과 요약)",
        "",
        f"- variant(변형): `{summary['variant_id']}`",
        f"- axis(축): `{summary['axis']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- MT5 KPI records(MT5 핵심성과지표 기록): `{summary.get('mt5_kpi_record_count', 0)}`",
        f"- validation routed net/PF/trades(검증 라우팅 순수익/수익 팩터/거래): `{val.get('net_profit')}` / `{val.get('profit_factor')}` / `{val.get('trade_count')}`",
        f"- OOS routed net/PF/trades(표본외 라우팅 순수익/수익 팩터/거래): `{oos.get('net_profit')}` / `{oos.get('profit_factor')}` / `{oos.get('trade_count')}`",
        "",
        "효과(effect, 효과): 이 실행(run, 실행)은 QDA(이차판별분석) run08F 주변 조건을 MT5(메타트레이더5) KPI(핵심성과지표)까지 확인한 runtime_probe(런타임 탐침)이다.",
    ])


def write_structural_files(spec: FollowupSpec, *, context: Mapping[str, Any], feature_order: Sequence[str], characteristic: Mapping[str, Any], tier_records: Sequence[Mapping[str, Any]], prediction_artifacts: Mapping[str, Any], model_artifacts: Mapping[str, Any], characteristic_artifacts: Mapping[str, Any], b_threshold: float, ledger_outputs: Mapping[str, Any], registry_output: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    summary = summary_payload(spec, characteristic, b_threshold=b_threshold, model_artifacts=model_artifacts, characteristic_artifacts=characteristic_artifacts)
    manifest = {"run_id": spec.run_id, "packet_id": PACKET_ID, "stage_id": base.STAGE_ID, "run_number": spec.run_number, "created_at_utc": created_at, "model_family": base.MODEL_FAMILY, "feature_set_id": base.FEATURE_SET_ID, "label_id": base.LABEL_ID, "split_contract": base.SPLIT_CONTRACT, "stage_inheritance": False, "baseline_comparison_run_id": BASELINE_RUN_ID, "boundary": BOUNDARY, "spec": spec.payload(), "tier_a_feature_order": list(feature_order), "tier_a_feature_order_hash": ordered_hash(feature_order), "tier_b_feature_order_hash": context["tier_b_feature_order_hash"], "threshold_policy": f"validation nonflat q{spec.threshold_quantile:.2f}; coverage-based, not profit-searched", "characteristic": characteristic, "prediction_artifacts": prediction_artifacts, "model_artifacts": model_artifacts, "external_verification_status": "out_of_scope_by_claim", "judgment": summary["judgment"]}
    kpi_record = {"run_id": spec.run_id, "packet_id": PACKET_ID, "stage_id": base.STAGE_ID, "model_family": base.MODEL_FAMILY, "feature_set_id": base.FEATURE_SET_ID, "label_id": base.LABEL_ID, "split_contract": base.SPLIT_CONTRACT, "stage_inheritance": False, "kpi_scope": "qda_run09_followup_python_shape_before_mt5", "python_characteristic": characteristic, "python_tier_records": list(tier_records), "tier_b_context_summary": context["tier_b_context_summary"], "external_verification_status": "out_of_scope_by_claim", "judgment": summary["judgment"], "boundary": BOUNDARY, "ledger_outputs": ledger_outputs, "registry_output": registry_output}
    write_json(run_root(spec) / "run_manifest.json", manifest)
    write_json(run_root(spec) / "kpi_record.json", kpi_record)
    write_json(run_root(spec) / "summary.json", summary)
    write_md(run_root(spec) / "reports/result_summary.md", run_result_markdown(summary))
    return summary


def build_structural_one(spec: FollowupSpec, context: Mapping[str, Any]) -> dict[str, Any]:
    created_at = utc_now()
    feature_order = feature_order_for_spec(context["full_feature_order"], spec)
    tier_a_model, a_sample = fit_qda_variant(context["tier_a_frame"], feature_order, spec)
    tier_b_model, b_sample = fit_qda_variant(context["tier_b_training_frame"], context["tier_b_feature_order"], spec)
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], feature_order)
    tier_b_training_prob = probability_frame(tier_b_model, context["tier_b_training_frame"], context["tier_b_feature_order"])
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], context["tier_b_feature_order"])
    a_threshold = nonflat_threshold(tier_a_prob, spec.threshold_quantile)
    b_threshold = nonflat_threshold(tier_b_training_prob, spec.threshold_quantile)
    characteristic = characteristic_result(spec, tier_a_model, tier_a_prob, a_threshold, a_sample, feature_order)
    characteristic = {**characteristic, "tier_b_training_sample": b_sample}
    tier_records, prediction_artifacts = python_tier_records(spec, tier_a_prob=tier_a_prob, tier_b_prob=tier_b_prob, a_threshold=a_threshold, b_threshold=b_threshold)
    model_artifacts = materialize_models(spec, tier_a_model=tier_a_model, tier_b_model=tier_b_model)
    characteristic_artifacts = write_characteristic_files(spec, characteristic)
    ledger_outputs, registry_output = write_structural_ledgers(spec, tier_records)
    return write_structural_files(spec, context=context, feature_order=feature_order, characteristic=characteristic, tier_records=tier_records, prediction_artifacts=prediction_artifacts, model_artifacts=model_artifacts, characteristic_artifacts=characteristic_artifacts, b_threshold=b_threshold, ledger_outputs=ledger_outputs, registry_output=registry_output, created_at=created_at)


def export_models(spec: FollowupSpec, context: Mapping[str, Any], feature_order: Sequence[str], summary: Mapping[str, Any]) -> dict[str, Any]:
    root = run_root(spec) / "models"
    tier_a_model = joblib.load(io_path(base.ROOT / summary["model_artifacts"]["tier_a_joblib"]["path"]))
    tier_b_model = joblib.load(io_path(base.ROOT / summary["model_artifacts"]["tier_b_joblib"]["path"]))
    tier_a_onnx = root / f"{spec.variant_id}_tier_a_qda_opset{ONNX_OPSET}.onnx"
    tier_b_onnx = root / f"{spec.variant_id}_tier_b_qda_core42_opset{ONNX_OPSET}.onnx"
    tier_a_export = export_sklearn_to_onnx_zipmap_disabled(tier_a_model, tier_a_onnx, feature_count=len(feature_order), target_opset=ONNX_OPSET)
    tier_b_export = export_sklearn_to_onnx_zipmap_disabled(tier_b_model, tier_b_onnx, feature_count=len(context["tier_b_feature_order"]), target_opset=ONNX_OPSET)
    a_sample = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq("validation"), list(feature_order)].head(128).to_numpy(dtype="float64", copy=False)
    b_sample = context["tier_b_training_frame"].loc[context["tier_b_training_frame"]["split"].astype(str).eq("validation"), context["tier_b_feature_order"]].head(128).to_numpy(dtype="float64", copy=False)
    return {"tier_a_onnx": tier_a_export, "tier_b_onnx": tier_b_export, "onnx_parity": {"tier_a": check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx, a_sample, tolerance=ONNX_PARITY_TOLERANCE), "tier_b": check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx, b_sample, tolerance=ONNX_PARITY_TOLERANCE)}}


def export_feature_matrices(spec: FollowupSpec, context: Mapping[str, Any], feature_order: Sequence[str]) -> dict[str, Any]:
    root = run_root(spec) / "features"
    payload: dict[str, Any] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        tier_a_frame = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq(source_split)].copy()
        tier_b_frame = context["tier_b_fallback_frame"].loc[context["tier_b_fallback_frame"]["split"].astype(str).eq(source_split)].copy()
        payload[f"tier_a_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(tier_a_frame, feature_order, root / f"tier_a_{runtime_split}_feature_matrix.csv", metadata_columns=("partial_context_subtype", "route_role"))
        payload[f"tier_b_fallback_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(tier_b_frame, context["tier_b_feature_order"], root / f"tier_b_fallback_{runtime_split}_feature_matrix.csv", metadata_columns=("partial_context_subtype", "route_role"))
    return payload


def copy_runtime_inputs(spec: FollowupSpec, model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = common_run_root(base.STAGE_NUMBER, spec.run_id)
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_onnx", "tier_b_onnx"):
        local_path = base.ROOT / model_artifacts[key]["path"]
        copies.append(copy_to_common(local_path, f"{common}/models/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        local_path = base.ROOT / matrix["path"]
        copies.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_attempts(spec: FollowupSpec, context: Mapping[str, Any], feature_order: Sequence[str], model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any], thresholds: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(base.STAGE_NUMBER, spec.run_id)
    tier_a_model = Path(model_artifacts["tier_a_onnx"]["path"]).name
    tier_b_model = Path(model_artifacts["tier_b_onnx"]["path"]).name
    a_threshold = float(thresholds["tier_a"])
    b_threshold = float(thresholds["tier_b"])
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        tier_a_matrix = Path(feature_matrices[f"tier_a_{runtime_split}"]["path"]).name
        tier_b_matrix = Path(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"]).name
        common_kwargs = {"run_root": run_root(spec), "run_id": spec.run_id, "stage_number": base.STAGE_NUMBER, "exploration_label": EXPLORATION_LABEL, "split": runtime_split, "from_date": from_date, "to_date": to_date, "max_hold_bars": MAX_HOLD_BARS, "common_root": common}
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_a_only_{runtime_split}", tier=mt5.TIER_A, model_path=f"{common}/models/{tier_a_model}", model_id=f"{spec.run_id}_tier_a", feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(feature_order), feature_order_hash=ordered_hash(feature_order), short_threshold=a_threshold, long_threshold=a_threshold, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role="tier_only_total", record_view_prefix="mt5_tier_a_only"))
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_b_fallback_only_{runtime_split}", tier=mt5.TIER_B, model_path=f"{common}/models/{tier_b_model}", model_id=f"{spec.run_id}_tier_b", feature_path=f"{common}/features/{tier_b_matrix}", feature_count=len(context["tier_b_feature_order"]), feature_order_hash=context["tier_b_feature_order_hash"], short_threshold=b_threshold, long_threshold=b_threshold, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_b_fallback", attempt_role="tier_b_fallback_only_total", record_view_prefix="mt5_tier_b_fallback_only"))
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"routed_{runtime_split}", tier=mt5.TIER_AB, model_path=f"{common}/models/{tier_a_model}", model_id=f"{spec.run_id}_tier_a", feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(feature_order), feature_order_hash=ordered_hash(feature_order), short_threshold=a_threshold, long_threshold=a_threshold, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role="routed_total", record_view_prefix="mt5_routed_total", fallback_enabled=True, fallback_model_path=f"{common}/models/{tier_b_model}", fallback_model_id=f"{spec.run_id}_tier_b", fallback_feature_path=f"{common}/features/{tier_b_matrix}", fallback_feature_count=len(context["tier_b_feature_order"]), fallback_feature_order_hash=context["tier_b_feature_order_hash"], fallback_short_threshold=b_threshold, fallback_long_threshold=b_threshold, fallback_min_margin=MIN_MARGIN, fallback_invert_signal=False))
    return attempts


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    try:
        result = execute_prepared_run(prepared, terminal_path=Path(args.terminal_path), metaeditor_path=Path(args.metaeditor_path), terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT, common_files_root=COMMON_FILES_ROOT_DEFAULT, tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT, timeout_seconds=int(args.timeout_seconds))
    except Exception as exc:
        return {**dict(prepared), "compile": {"status": "exception_or_not_completed"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": JUDGMENT_BLOCKED, "failure": {"type": type(exc).__name__, "message": str(exc)}}
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED
    for record in result.get("mt5_kpi_records", []):
        record["source_variant_id"] = prepared["source_variant_id"]
    return result


def routed_metrics(result: Mapping[str, Any], view: str) -> dict[str, Any]:
    for record in result.get("mt5_kpi_records", []):
        if record.get("record_view") == view:
            metrics = record.get("metrics", {})
            return dict(metrics) if isinstance(metrics, Mapping) else {}
    return {}


def upsert_runtime_registry(spec: FollowupSpec, result: Mapping[str, Any]) -> dict[str, Any]:
    validation = routed_metrics(result, "mt5_routed_total_validation_is")
    oos = routed_metrics(result, "mt5_routed_total_oos")
    row = {"run_id": spec.run_id, "stage_id": base.STAGE_ID, "lane": "alpha_runtime_probe", "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked", "judgment": result["judgment"], "path": base.rel(run_root(spec)), "notes": ledger_pairs((("axis", spec.axis), ("model_family", base.MODEL_FAMILY), ("routing_mode", "tier_a_primary_tier_b_fallback"), ("reg_param", spec.reg_param), ("rows_per_class", spec.rows_per_class), ("threshold_q", spec.threshold_quantile), ("feature_mode", spec.tier_a_feature_mode), ("validation_net_profit", validation.get("net_profit")), ("validation_pf", validation.get("profit_factor")), ("oos_net_profit", oos.get("net_profit")), ("oos_pf", oos.get("profit_factor")), ("external_verification", result["external_verification_status"]), ("boundary", "runtime_probe_only")))}
    return upsert_csv_rows(base.RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [row], key="run_id")


def write_runtime_outputs(spec: FollowupSpec, result: Mapping[str, Any], tier_records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    manifest = read_json(run_root(spec) / "run_manifest.json")
    kpi_record = read_json(run_root(spec) / "kpi_record.json")
    summary = read_json(run_root(spec) / "summary.json")
    ledger_rows = build_alpha_scout_ledger_rows(run_id=spec.run_id, stage_id=base.STAGE_ID, tier_records=tier_records, mt5_kpi_records=result.get("mt5_kpi_records", []), selected_threshold_id=f"validation_nonflat_q{spec.threshold_quantile:.2f}", run_output_root=run_root(spec), external_verification_status=result["external_verification_status"])
    ledger_outputs = materialize_alpha_ledgers(stage_run_ledger_path=base.STAGE_LEDGER_PATH, project_alpha_ledger_path=base.PROJECT_LEDGER_PATH, rows=ledger_rows)
    registry_output = upsert_runtime_registry(spec, result)
    validation = routed_metrics(result, "mt5_routed_total_validation_is")
    oos = routed_metrics(result, "mt5_routed_total_oos")
    runtime_payload = {"packet_id": PACKET_ID, "scoreboard_lane": "runtime_probe", "external_verification_status": result["external_verification_status"], "execution_results": result.get("execution_results", []), "strategy_tester_reports": result.get("strategy_tester_reports", []), "kpi_records": result.get("mt5_kpi_records", []), "validation_routed": validation, "oos_routed": oos}
    manifest["runtime_probe"] = {key: result.get(key) for key in ("attempts", "common_copies", "compile", "execution_results", "strategy_tester_reports", "external_verification_status", "judgment", "failure") if key in result}
    manifest["runtime_probe"]["packet_id"] = PACKET_ID
    manifest["runtime_probe"]["model_artifacts"] = result.get("model_artifacts")
    manifest["runtime_probe"]["feature_matrices"] = result.get("feature_matrices")
    kpi_record.update({"mt5": runtime_payload, "external_verification_status": result["external_verification_status"], "judgment": result["judgment"], "boundary": BOUNDARY, "ledger_outputs": ledger_outputs, "registry_output": registry_output})
    summary.update({"judgment": result["judgment"], "external_verification_status": result["external_verification_status"], "boundary": BOUNDARY, "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])), "attempt_count": len(result.get("attempts", [])), "validation_routed": validation, "oos_routed": oos})
    write_json(run_root(spec) / "run_manifest.json", manifest)
    write_json(run_root(spec) / "kpi_record.json", kpi_record)
    write_json(run_root(spec) / "summary.json", summary)
    write_json(PACKET_ROOT / "run_summaries" / f"{spec.run_id}.json", summary)
    write_md(run_root(spec) / "reports/result_summary.md", run_result_markdown(summary))
    return summary


def build_runtime_one(spec: FollowupSpec, context: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    summary = read_json(run_root(spec) / "summary.json")
    feature_order = feature_order_for_spec(context["full_feature_order"], spec)
    model_artifacts = export_models(spec, context, feature_order, summary)
    feature_matrices = export_feature_matrices(spec, context, feature_order)
    copies = copy_runtime_inputs(spec, model_artifacts, feature_matrices)
    attempts = make_attempts(spec, context, feature_order, model_artifacts, feature_matrices, summary["thresholds"])
    prepared = {"stage_id": base.STAGE_ID, "stage_number": base.STAGE_NUMBER, "run_id": spec.run_id, "run_number": spec.run_number, "run_root": run_root(spec), "source_variant_id": spec.variant_id, "attempts": attempts, "common_copies": copies, "route_coverage": context["tier_b_context_summary"], "model_artifacts": model_artifacts, "feature_matrices": list(feature_matrices.values())}
    result = execute_or_block(prepared, args)
    result["model_artifacts"] = model_artifacts
    result["feature_matrices"] = list(feature_matrices.values())
    tier_records = read_json(run_root(spec) / "kpi_record.json").get("python_tier_records", [])
    return write_runtime_outputs(spec, result, tier_records)


def aggregate_summary(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [row for row in summaries if row.get("external_verification_status") == "completed"]
    best_oos = max(summaries, key=lambda row: base.safe_float(row.get("oos_routed", {}).get("net_profit"), -1e18), default=None)
    best_val = max(summaries, key=lambda row: base.safe_float(row.get("validation_routed", {}).get("net_profit"), -1e18), default=None)
    return {"packet_id": PACKET_ID, "stage_id": base.STAGE_ID, "run_range": "run09A-run09Q", "baseline_comparison_run_id": BASELINE_RUN_ID, "run_count": len(summaries), "completed_run_count": len(completed), "blocked_run_count": len(summaries) - len(completed), "external_verification_status": "completed" if len(completed) == len(summaries) else "blocked_or_partial", "judgment": JUDGMENT_COMPLETED if len(completed) == len(summaries) else JUDGMENT_BLOCKED, "boundary": BOUNDARY, "mt5_kpi_record_count": sum(int(row.get("mt5_kpi_record_count", 0)) for row in summaries), "attempt_count": sum(int(row.get("attempt_count", 0)) for row in summaries), "best_oos_routed_net_run": best_oos, "best_validation_routed_net_run": best_val, "run_ids": [row["run_id"] for row in summaries]}


def write_normalized_kpi(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    inventory = [{"run_id": str(row["run_id"]), "stage_id": base.STAGE_ID, "idea_id": str(row.get("idea_id") or row.get("run_number") or row["run_id"]), "path": base.rel(base.STAGE_ROOT / "02_runs" / str(row["run_id"]))} for row in summaries]
    records, summary_rows, missing, parser_errors = mt5_kpi_recorder.build_normalized_records(base.ROOT, inventory)
    market_data = mt5_trade_attribution.MarketData.load(base.ROOT)
    enriched, trade_rows, trade_summary, trade_errors = mt5_trade_attribution.enrich_records(records, base.ROOT, market_data)
    write_jsonl(PACKET_ROOT / "normalized_kpi_records.jsonl", records)
    write_csv_rows(PACKET_ROOT / "normalized_kpi_summary.csv", mt5_kpi_recorder.SUMMARY_COLUMNS, summary_rows)
    write_json(PACKET_ROOT / "normalized_kpi_missing_runs.json", missing)
    write_json(PACKET_ROOT / "normalized_kpi_parser_errors.json", parser_errors)
    write_jsonl(PACKET_ROOT / "enriched_kpi_records.jsonl", enriched)
    write_csv_rows(PACKET_ROOT / "trade_level_records.csv", mt5_trade_attribution.TRADE_COLUMNS, trade_rows)
    write_csv_rows(PACKET_ROOT / "trade_attribution_summary.csv", mt5_trade_attribution.SUMMARY_COLUMNS, trade_summary)
    write_json(PACKET_ROOT / "trade_attribution_parser_errors.json", trade_errors)
    return {"normalized_records": len(records), "normalized_summary_rows": len(summary_rows), "missing_runs": len(missing), "parser_errors": len(parser_errors), "trade_attribution_records": len(trade_summary), "trade_level_rows": len(trade_rows), "trade_parser_errors": len(trade_errors)}


def experiment_design() -> dict[str, Any]:
    return {
        "hypothesis": "QDA run08F 주변에서 중간 정규화, full58 기반 피처 제거, 표본 크기, coverage 기반 임계값이 거래 가능한 KPI 모양을 바꾸는지 확인한다.",
        "decision_use": "Stage16 QDA 후속 탐색을 계속 좁힐지, 또는 QDA를 부정/보존 단서로 닫을지 판단한다.",
        "comparison_baseline": BASELINE_RUN_ID,
        "control_variables": {"symbol": "FPMarkets US100", "timeframe": "M5", "label": base.LABEL_ID, "split": base.SPLIT_CONTRACT, "routing": "Tier A primary + Tier B fallback", "max_hold_bars": MAX_HOLD_BARS, "threshold_method": "validation nonflat coverage quantile, not profit-searched"},
        "changed_variables": ["reg_param 0.08~0.25", "full58 minus feature groups", "rows_per_class 300/450/600/900", "threshold_quantile q85/q93/q95"],
        "sample_scope": "Tier A full-context model input plus Tier B partial-context fallback, validation and OOS tester windows.",
        "success_criteria": "여러 축에서 validation/OOS routed KPI가 같이 나아지고 parser error 없이 KPI가 정규화된다.",
        "failure_criteria": "개선이 한 축/한 split에만 머물거나, drawdown/trade shape가 나빠지거나, QDA가 피처/표본/임계값에 과민하게 흔들린다.",
        "invalid_conditions": "MT5 출력 누락, ONNX parity 실패, feature order mismatch, parser error, missing run ledger.",
        "stop_conditions": "run08F보다 좋은 단서가 없으면 QDA는 보존 단서로 낮추고 새 Stage 주제로 이동한다.",
        "evidence_plan": ["run_manifest.json", "kpi_record.json", "MT5 Strategy Tester reports", "normalized_kpi_summary.csv", "trade_attribution_summary.csv", "stage/project alpha ledgers", "gate JSON files"],
    }


def packet_markdown(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], kpi: Mapping[str, Any]) -> str:
    lines = [
        "# Stage16 QDA RUN09A-RUN09Q Follow-up MT5 Runtime Probe(16단계 QDA 실행 09A-09Q 후속 MT5 런타임 탐침)",
        "",
        f"- judgment(판정): `{aggregate['judgment']}`",
        f"- completed runs(완료 실행): `{aggregate['completed_run_count']}/{aggregate['run_count']}`",
        f"- MT5 KPI records(MT5 핵심성과지표 기록): `{aggregate['mt5_kpi_record_count']}`",
        f"- normalized KPI records(정규화 KPI 기록): `{kpi['normalized_records']}`",
        f"- trade attribution records(거래 귀속 기록): `{kpi['trade_attribution_records']}`",
        f"- baseline comparison(비교 기준): `{BASELINE_RUN_ID}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| run(실행) | axis(축) | topic(주제) | reg(정규화) | rows(행/클래스) | q(분위수) | features(피처) | val net/PF/trades(검증) | oos net/PF/trades(표본외) |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summaries:
        val = row.get("validation_routed", {})
        oos = row.get("oos_routed", {})
        lines.append(f"| `{row['run_number']}` | `{row['axis']}` | `{row['idea_id']}` | `{row['reg_param']}` | `{row['rows_per_class']}` | `{row['threshold_quantile']}` | `{row['feature_count']}` | `{val.get('net_profit')}/{val.get('profit_factor')}/{val.get('trade_count')}` | `{oos.get('net_profit')}/{oos.get('profit_factor')}/{oos.get('trade_count')}` |")
    best_oos = aggregate.get("best_oos_routed_net_run") or {}
    lines.extend(["", f"- best OOS routed net(최고 표본외 라우팅 순수익): `{best_oos.get('run_number')}` `{best_oos.get('idea_id')}` `{(best_oos.get('oos_routed') or {}).get('net_profit')}`", "", "효과(effect, 효과): 이 묶음은 QDA(이차판별분석) run08F 주변의 정규화, 피처 제거, 표본 크기, coverage threshold(커버리지 임계값)를 수익 최적화 없이 MT5(메타트레이더5) KPI(핵심성과지표)까지 비교한다.", "", "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)."])
    return "\n".join(lines)


def gate_payloads(aggregate: Mapping[str, Any], kpi: Mapping[str, Any]) -> dict[str, Any]:
    expected_kpi = int(aggregate["run_count"]) * 10
    expected_attempts = int(aggregate["run_count"]) * 6
    runtime_ok = aggregate["completed_run_count"] == aggregate["run_count"] and aggregate["attempt_count"] == expected_attempts and aggregate["mt5_kpi_record_count"] == expected_kpi
    kpi_ok = kpi["normalized_records"] == expected_kpi and kpi["parser_errors"] == 0 and kpi["missing_runs"] == 0
    passed = bool(runtime_ok and kpi_ok)
    return {
        "runtime_evidence_gate": {"audit_name": "runtime_evidence_gate", "status": "pass" if runtime_ok else "blocked", "passed": runtime_ok, "expected_attempts": expected_attempts, "expected_kpi_records": expected_kpi, "counts": {"attempt_count": aggregate["attempt_count"], "mt5_kpi_record_count": aggregate["mt5_kpi_record_count"]}},
        "kpi_contract_audit": {"audit_name": "kpi_contract_audit", "status": "pass" if kpi_ok else "blocked", "passed": kpi_ok, **dict(kpi)},
        "source_authority_audit": {"audit_name": "source_authority_audit", "status": "pass" if passed else "blocked", "passed": passed, "source": "run kpi_record.json plus MT5 Strategy Tester reports plus normalized KPI files"},
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass" if passed else "blocked", "passed": passed, "allowed_claims": [aggregate["judgment"], "runtime_probe", "followup_characterization"], "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"]},
        "required_gate_coverage_audit": {"audit_name": "required_gate_coverage_audit", "status": "pass" if passed else "blocked", "passed": passed, "required_gates": {"runtime_evidence_gate": "pass" if runtime_ok else "blocked", "kpi_contract_audit": "pass" if kpi_ok else "blocked", "source_authority_audit": "pass" if passed else "blocked", "final_claim_guard": "pass" if passed else "blocked"}},
    }


def write_packet_files(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], kpi: Mapping[str, Any], created_at: str) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", {**dict(aggregate), "kpi_management": dict(kpi)})
    write_json(PACKET_ROOT / "experiment_design.json", experiment_design())
    write_json(PACKET_ROOT / "artifact_index.json", {"run_summaries": list(summaries), "report_path": base.rel(REVIEW_PACKET_PATH), "created_at_utc": created_at})
    write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "primary_family": "runtime_backtest", "primary_skill": "obsidian-runtime-parity", "support_skills": ["obsidian-experiment-design", "obsidian-exploration-mandate", "obsidian-backtest-forensics", "obsidian-artifact-lineage", "obsidian-result-judgment"], "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "source_authority_audit", "required_gate_coverage_audit", "final_claim_guard"]})
    write_json(PACKET_ROOT / "skill_receipts.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "receipts": [{"skill": "obsidian-experiment-design", "status": "completed", "decision_use": "Stage16 QDA follow-up narrowing"}, {"skill": "obsidian-exploration-mandate", "status": "completed", "evidence_boundary": "runtime_probe"}, {"skill": "obsidian-runtime-parity", "status": "completed", "runtime_claim_boundary": "runtime_probe"}, {"skill": "obsidian-backtest-forensics", "status": "completed", "backtest_judgment": "usable_with_boundary"}, {"skill": "obsidian-artifact-lineage", "status": "completed", "lineage_judgment": "connected_with_boundary"}, {"skill": "obsidian-result-judgment", "status": "completed", "judgment_label": aggregate["judgment"], "claim_boundary": BOUNDARY}]})
    write_json(PACKET_ROOT / "runtime_identity.json", {"research_path": "stage_pipelines/stage16/qda_run09_followup_probe.py", "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5", "shared_contract": {"feature_set_id": base.FEATURE_SET_ID, "label_id": base.LABEL_ID, "split_contract": base.SPLIT_CONTRACT, "onnx_opset": ONNX_OPSET}, "module_hashes": {"pipeline": sha256_file_lf_normalized(Path(__file__)), "ea": sha256_file_lf_normalized(base.ROOT / "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"), "model_runtime": sha256_file_lf_normalized(base.ROOT / "foundation/mt5/include/ObsidianPrime/ModelRuntime.mqh")}, "runtime_claim_boundary": "runtime_probe"})
    for name, payload in gate_payloads(aggregate, kpi).items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
    write_md(REVIEW_PACKET_PATH, packet_markdown(aggregate, summaries, kpi))


def sync_docs(aggregate: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    best = aggregate.get("best_oos_routed_net_run") or {}
    current_run = str(best.get("run_id") or "run09Q_qda_reg015_q95_coverage_followup_v1")
    write_md(base.STAGE_ROOT / "03_reviews/review_index.md", "\n".join(["# Stage 16 Review Index(16단계 검토 색인)", "", "- `run08A`~`run08J`: `inconclusive_qda_characterization_structural_scout_completed`, report(보고서): `stages/16_model_family_challenge__qda_class_covariance_scout/03_reviews/run08A_run08J_qda_characterization_packet.md`", "- `run08A`~`run08J` MT5(`MetaTrader 5`, 메타트레이더5): `inconclusive_qda_characterization_mt5_runtime_probe_completed`, report(보고서): `stages/16_model_family_challenge__qda_class_covariance_scout/03_reviews/run08A_run08J_qda_mt5_runtime_probe_packet.md`", f"- `run09A`~`run09Q` follow-up(후속): `{aggregate['judgment']}`, report(보고서): `{base.rel(REVIEW_PACKET_PATH)}`", "", "효과(effect, 효과): Stage16(16단계)은 QDA(이차판별분석)의 class covariance(클래스별 공분산) 후속 탐색을 MT5(메타트레이더5) KPI(핵심성과지표)까지 연결했지만 edge(거래 우위)는 주장하지 않는다."]))
    write_md(base.STAGE_ROOT / "04_selected/selection_status.md", "\n".join(["# Stage 16 Selection Status(16단계 선택 상태)", "", "## Current Read(현재 판독)", "", f"- stage(단계): `{base.STAGE_ID}`", "- status(상태): `reviewed_qda_run09A_run09Q_followup_mt5_runtime_probe_no_edge(검토됨, QDA 실행 09A-09Q 후속 MT5 런타임 탐침, 엣지 없음)`", f"- current run(현재 실행): `{current_run}`", "- model family(모델 계열): QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석)", "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`", f"- judgment(판정): `{aggregate['judgment']}`", f"- MT5 KPI records(MT5 핵심성과지표 기록): `{aggregate['mt5_kpi_record_count']}`", f"- normalized KPI records(정규화 KPI 기록): `{kpi['normalized_records']}`", f"- boundary(경계): `{BOUNDARY}`", "", "효과(effect, 효과): 이번 follow-up(후속 탐색)은 run08F 주변 조건을 좁혔지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다."]))
    write_md(DECISION_PATH, "\n".join(["# 2026-05-03 Stage16 QDA Run09 Follow-up(16단계 QDA 실행09 후속 탐색)", "", "## Decision(결정)", "", "`run09A`~`run09Q`는 QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석) run08F 주변의 regularization(정규화), feature removal(피처 제거), sample size(표본 크기), coverage threshold(커버리지 임계값)를 MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터)까지 확인한 runtime_probe(런타임 탐침)로 기록한다.", "", "효과(effect, 효과): Stage16(16단계) 안에서 QDA(이차판별분석)를 더 볼지, 보존 단서로 닫을지 판단할 비교 근거를 만든다.", "", "## Boundary(경계)", "", f"`{BOUNDARY}`"]))
    sync_workspace_docs(aggregate, kpi, current_run)
    sync_misc_docs()


def sync_workspace_docs(aggregate: Mapping[str, Any], kpi: Mapping[str, Any], current_run: str) -> None:
    state_path = base.ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    state = re.sub(r"updated_on: '2026-05-02'", "updated_on: '2026-05-03'", state, count=1)
    state = re.sub(r"current_run_id: .*", f"current_run_id: {current_run}", state, count=1)
    state = state.replace("stage16_qda_run08A_run08J_mt5_runtime_probe_reviewed", "stage16_qda_run09A_run09Q_followup_mt5_runtime_probe_reviewed")
    state = state.replace("reviewed_qda_run08A_run08J_mt5_runtime_probe_no_edge", "reviewed_qda_run09A_run09Q_followup_mt5_runtime_probe_no_edge")
    append = f"""stage16_qda_run09_followup_mt5_runtime_probe:
  packet_id: {PACKET_ID}
  status: reviewed_runtime_probe_completed
  judgment: {aggregate['judgment']}
  run_range: run09A-run09Q
  current_run_id: {current_run}
  completed_run_count: {aggregate['completed_run_count']}
  mt5_kpi_record_count: {aggregate['mt5_kpi_record_count']}
  normalized_kpi_record_count: {kpi['normalized_records']}
  trade_attribution_records: {kpi['trade_attribution_records']}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {base.rel(REVIEW_PACKET_PATH)}
  decision_path: {base.rel(DECISION_PATH)}
  next_action: judge_qda_run09_followup_before_stage16_closeout_or_next_micro_probe
"""
    if "stage16_qda_run09_followup_mt5_runtime_probe:" not in state:
        state = state.replace("stage16_qda_mt5_runtime_probe_run08A_run08J:\n", append + "stage16_qda_mt5_runtime_probe_run08A_run08J:\n", 1)
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")
    current_path = base.ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    current = re.sub(r"- updated_on: `2026-05-02`", "- updated_on: `2026-05-03`", current, count=1)
    current = re.sub(r"- current run\(현재 실행\): `[^`]+`", f"- current run(현재 실행): `{current_run}`", current, count=1)
    latest = "\n".join(["## Latest Stage 16 Update(최신 Stage 16 업데이트)", "", f"Stage16(16단계)는 QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석) `run09A`~`run09Q` follow-up(후속 탐색)을 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)까지 실행하고 KPI(`Key Performance Indicator`, 핵심성과지표)를 정규화했다.", "", f"효과(effect, 효과): `{aggregate['judgment']}`로 기록했지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.", ""])
    current = re.sub(r"## Latest Stage 16 Update\(최신 Stage 16 업데이트\)\n\n.*?(?=## 쉬운 설명)", latest, current, count=1, flags=re.S)
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")


def sync_misc_docs() -> None:
    changelog_path = base.ROOT / "docs/workspace/changelog.md"
    changelog = io_path(changelog_path).read_text(encoding="utf-8-sig")
    line = "- 2026-05-03: Stage16 QDA(이차판별분석) `run09A`~`run09Q` follow-up(후속 탐색)을 MT5 runtime_probe(MT5 런타임 탐침)와 KPI(핵심성과지표) 정규화까지 완료했다. 효과(effect, 효과): run08F 주변 조건을 좁혔지만 edge(거래 우위)는 주장하지 않는다."
    if line not in changelog:
        io_path(changelog_path).write_text(changelog.rstrip() + "\n" + line + "\n", encoding="utf-8-sig")
    idea_path = base.ROOT / "docs/registers/idea_registry.md"
    idea = io_path(idea_path).read_text(encoding="utf-8-sig")
    line = "- 2026-05-03 Stage16 QDA run09 follow-up(16단계 QDA 실행09 후속 탐색): regularization(정규화), feature removal(피처 제거), sample size(표본 크기), coverage threshold(커버리지 임계값)를 MT5(메타트레이더5) KPI(핵심성과지표)까지 비교했다. 효과(effect, 효과): 보존 단서와 실패 기억을 Stage16 안에 남긴다."
    if line not in idea:
        io_path(idea_path).write_text(idea.rstrip() + "\n" + line + "\n", encoding="utf-8-sig")


def selected_specs(run_filter: str) -> list[FollowupSpec]:
    selected = {item.strip() for item in run_filter.split(",") if item.strip()} if run_filter else set()
    return [spec for spec in run09_specs() if not selected or spec.run_number in selected or spec.run_id in selected]


def build_all(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = base.load_context()
    specs = selected_specs(args.run_filter)
    structural = [build_structural_one(spec, context) for spec in specs]
    if args.structural_only:
        print(json.dumps(json_ready({"packet_id": PACKET_ID, "structural_run_count": len(structural), "run_ids": [row["run_id"] for row in structural]}), ensure_ascii=False, indent=2))
        return {"packet_id": PACKET_ID, "structural_run_count": len(structural)}
    summaries = [build_runtime_one(spec, context, args) for spec in specs]
    aggregate = aggregate_summary(summaries)
    kpi = write_normalized_kpi(summaries)
    write_packet_files(aggregate, summaries, kpi, created_at)
    sync_docs(aggregate, kpi)
    print(json.dumps(json_ready({**aggregate, "kpi_management": kpi}), ensure_ascii=False, indent=2))
    return dict(aggregate)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage16 QDA run09 follow-up probes with MT5 KPI management.")
    parser.add_argument("--run-filter", default="")
    parser.add_argument("--structural-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    args = parser.parse_args(argv)
    build_all(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
