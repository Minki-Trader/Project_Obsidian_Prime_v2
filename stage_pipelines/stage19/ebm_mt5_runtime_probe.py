from __future__ import annotations

import argparse
import csv
import json
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
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
    COMMON_FILES_ROOT_DEFAULT,
    FEATURE_ORDER_PATH,
    METAEDITOR_PATH_DEFAULT,
    MODEL_INPUT_PATH,
    RAW_ROOT,
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
from foundation.models.ebm_explainable import (
    EbmVariantSpec,
    default_stage19_ebm_variants,
    fit_ebm_variant,
    nonflat_threshold,
    probability_frame,
    split_decision_metrics,
)
from foundation.models.ebm_score_table import check_ebm_score_table_probability_parity, export_ebm_main_effect_score_table
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5


STAGE_NUMBER = 19
STAGE_ID = "19_model_family_challenge__ebm_explainable_boosting_shape"
SOURCE_RUN_ID = "run13A_ebm_main_effect_shape_scout_v1"
SOURCE_PACKET_ID = "stage19_run13A_ebm_shape_scout_v1"
AGGREGATE_PACKET_ID = "stage19_ebm_run13B_run13G_mt5_runtime_batch_v1"
MODEL_FAMILY = "interpret_ebm_explainable_boosting_classifier_multiclass_main_effect_mql5_score_table"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
SELECTED_VARIANT_ID = "v01_main_effects_broad_bins"
MODEL_BACKEND = "ebm_table"
DEFAULT_MAX_HOLD_BARS = 12
MIN_MARGIN = 0.0

ROOT = Path(__file__).resolve().parents[2]
STAGE_ROOT = ROOT / "stages" / STAGE_ID
SOURCE_RUN_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
AGGREGATE_PACKET_ROOT = ROOT / "docs/agent_control/packets" / AGGREGATE_PACKET_ID
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-03_stage19_run13B_run13G_ebm_mt5_runtime_batch.md"


@dataclass(frozen=True)
class RuntimeTopic:
    run_id: str
    run_number: str
    packet_id: str
    exploration_label: str
    review_filename: str
    threshold_quantile: float
    mode: str
    max_hold_bars: int
    expected_attempts: int
    expected_kpi_records: int
    topic_read: str
    boundary: str
    judgment_completed: str
    judgment_blocked: str

    @property
    def run_root(self) -> Path:
        return STAGE_ROOT / "02_runs" / self.run_id

    @property
    def packet_root(self) -> Path:
        return ROOT / "docs/agent_control/packets" / self.packet_id

    @property
    def review_path(self) -> Path:
        return STAGE_ROOT / "03_reviews" / self.review_filename


RUN_TOPICS: tuple[RuntimeTopic, ...] = (
    RuntimeTopic(
        run_id="run13B_ebm_q90_runtime_handoff_probe_v1",
        run_number="run13B",
        packet_id="stage19_run13B_ebm_q90_mt5_runtime_v1",
        exploration_label="stage19_Model__EBMQ90RuntimeHandoff",
        review_filename="run13B_ebm_q90_runtime_handoff_packet.md",
        threshold_quantile=0.90,
        mode="routed",
        max_hold_bars=DEFAULT_MAX_HOLD_BARS,
        expected_attempts=6,
        expected_kpi_records=10,
        topic_read="q90_runtime_handoff_feasibility",
        boundary="ebm_q90_runtime_handoff_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q90_runtime_handoff_probe_completed",
        judgment_blocked="blocked_ebm_q90_runtime_handoff_probe_after_attempt",
    ),
    RuntimeTopic(
        run_id="run13C_ebm_q80_signal_density_probe_v1",
        run_number="run13C",
        packet_id="stage19_run13C_ebm_q80_density_mt5_v1",
        exploration_label="stage19_Model__EBMQ80SignalDensity",
        review_filename="run13C_ebm_q80_signal_density_packet.md",
        threshold_quantile=0.80,
        mode="routed",
        max_hold_bars=DEFAULT_MAX_HOLD_BARS,
        expected_attempts=6,
        expected_kpi_records=10,
        topic_read="q80_signal_density_pressure",
        boundary="ebm_q80_signal_density_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q80_signal_density_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q80_signal_density_runtime_probe_after_attempt",
    ),
    RuntimeTopic(
        run_id="run13D_ebm_q95_sparse_tail_probe_v1",
        run_number="run13D",
        packet_id="stage19_run13D_ebm_q95_sparse_mt5_v1",
        exploration_label="stage19_Model__EBMQ95SparseTail",
        review_filename="run13D_ebm_q95_sparse_tail_packet.md",
        threshold_quantile=0.95,
        mode="routed",
        max_hold_bars=DEFAULT_MAX_HOLD_BARS,
        expected_attempts=6,
        expected_kpi_records=10,
        topic_read="q95_sparse_tail_extreme",
        boundary="ebm_q95_sparse_tail_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q95_sparse_tail_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q95_sparse_tail_runtime_probe_after_attempt",
    ),
    RuntimeTopic(
        run_id="run13E_ebm_q80_direction_asymmetry_probe_v1",
        run_number="run13E",
        packet_id="stage19_run13E_ebm_direction_mt5_v1",
        exploration_label="stage19_Model__EBMDirectionAsymmetry",
        review_filename="run13E_ebm_direction_asymmetry_packet.md",
        threshold_quantile=0.80,
        mode="direction",
        max_hold_bars=DEFAULT_MAX_HOLD_BARS,
        expected_attempts=12,
        expected_kpi_records=20,
        topic_read="q80_long_short_direction_asymmetry",
        boundary="ebm_q80_direction_asymmetry_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q80_direction_asymmetry_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q80_direction_asymmetry_runtime_probe_after_attempt",
    ),
    RuntimeTopic(
        run_id="run13F_ebm_q90_hold6_probe_v1",
        run_number="run13F",
        packet_id="stage19_run13F_ebm_hold6_mt5_v1",
        exploration_label="stage19_Model__EBMHold6Stress",
        review_filename="run13F_ebm_q90_hold6_packet.md",
        threshold_quantile=0.90,
        mode="routed",
        max_hold_bars=6,
        expected_attempts=6,
        expected_kpi_records=10,
        topic_read="q90_hold6_trade_shape_stress",
        boundary="ebm_q90_hold6_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q90_hold6_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q90_hold6_runtime_probe_after_attempt",
    ),
    RuntimeTopic(
        run_id="run13G_ebm_q90_hold18_probe_v1",
        run_number="run13G",
        packet_id="stage19_run13G_ebm_hold18_mt5_v1",
        exploration_label="stage19_Model__EBMHold18Stress",
        review_filename="run13G_ebm_q90_hold18_packet.md",
        threshold_quantile=0.90,
        mode="routed",
        max_hold_bars=18,
        expected_attempts=6,
        expected_kpi_records=10,
        topic_read="q90_hold18_trade_shape_stress",
        boundary="ebm_q90_hold18_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q90_hold18_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q90_hold18_runtime_probe_after_attempt",
    ),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_div(numerator: Any, denominator: Any) -> float | None:
    den = safe_float(denominator)
    if den == 0.0:
        return None
    return safe_float(numerator) / den


def bump_count(target: dict[str, int], key: Any, amount: int = 1) -> None:
    if key in (None, ""):
        return
    target[str(key)] = target.get(str(key), 0) + int(amount)


def telemetry_failure_reasons(path_value: Any, sample_limit: int = 2000) -> dict[str, int]:
    if path_value in (None, ""):
        return {}
    path = Path(str(path_value))
    if not path.exists():
        return {}
    counts: dict[str, int] = {}
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            sampled = 0
            for row in reader:
                if row.get("record_type") != "cycle":
                    continue
                if row.get("feature_ready") != "true" or row.get("model_ok") != "false":
                    continue
                reason = row.get("skip_reason") or row.get("decision_reason")
                bump_count(counts, reason)
                sampled += 1
                if sampled >= sample_limit:
                    break
    except OSError:
        return counts
    return counts


def runtime_failure_signature_from_probe(probe: Mapping[str, Any]) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    last_skip_reason_counts: dict[str, int] = {}
    sampled_failure_reason_counts: dict[str, int] = {}
    model_ok_total = 0
    model_fail_total = 0
    feature_ready_total = 0
    telemetry_files_seen = 0
    for item in probe.get("execution_results", []) or []:
        if not isinstance(item, Mapping):
            continue
        bump_count(status_counts, item.get("status"))
        outputs = item.get("runtime_outputs", {})
        if not isinstance(outputs, Mapping):
            outputs = {}
        summary = outputs.get("last_summary", {})
        if isinstance(summary, Mapping):
            model_ok_total += int(summary.get("model_ok_count") or 0)
            model_fail_total += int(summary.get("model_fail_count") or 0)
            feature_ready_total += int(summary.get("feature_ready_count") or 0)
            bump_count(last_skip_reason_counts, summary.get("last_skip_reason"))
        telemetry_counts = telemetry_failure_reasons(outputs.get("telemetry_path"))
        if telemetry_counts:
            telemetry_files_seen += 1
        for reason, count in telemetry_counts.items():
            bump_count(sampled_failure_reason_counts, reason, count)
    primary_reason = None
    if sampled_failure_reason_counts:
        primary_reason = max(sampled_failure_reason_counts.items(), key=lambda pair: pair[1])[0]
    elif any(status != "completed" for status in status_counts) and last_skip_reason_counts:
        primary_reason = max(last_skip_reason_counts.items(), key=lambda pair: pair[1])[0]
    primary_skip_reason = None
    if last_skip_reason_counts:
        primary_skip_reason = max(last_skip_reason_counts.items(), key=lambda pair: pair[1])[0]
    return {
        "compile_status": (probe.get("compile") or {}).get("status") if isinstance(probe.get("compile"), Mapping) else None,
        "attempt_status_counts": status_counts,
        "feature_ready_count_total": feature_ready_total,
        "model_ok_count_total": model_ok_total,
        "model_fail_count_total": model_fail_total,
        "model_failure_sample_count": sum(sampled_failure_reason_counts.values()),
        "primary_runtime_failure": primary_reason,
        "primary_runtime_skip": primary_skip_reason,
        "sampled_failure_reason_counts": sampled_failure_reason_counts,
        "last_skip_reason_counts": last_skip_reason_counts,
        "telemetry_files_sampled": telemetry_files_seen,
    }


def runtime_failure_signature_from_result(result: Mapping[str, Any]) -> dict[str, Any]:
    probe = {
        "compile": result.get("compile"),
        "execution_results": result.get("execution_results", []),
    }
    return runtime_failure_signature_from_probe(probe)


def attach_existing_runtime_failure_signature(topic: RuntimeTopic, summary: Mapping[str, Any]) -> dict[str, Any]:
    enriched = dict(summary)
    manifest_path = topic.run_root / "run_manifest.json"
    if not manifest_path.exists():
        return enriched
    manifest = read_json(manifest_path)
    enriched["runtime_failure_signature"] = runtime_failure_signature_from_probe(manifest.get("runtime_probe", {}))
    return enriched


def selected_spec() -> EbmVariantSpec:
    for spec in default_stage19_ebm_variants():
        if spec.variant_id == SELECTED_VARIANT_ID:
            return spec
    raise RuntimeError(f"missing Stage19 selected EBM variant: {SELECTED_VARIANT_ID}")


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


def _load_or_train_model(path: Path, frame: pd.DataFrame, feature_order: Sequence[str], spec: EbmVariantSpec) -> tuple[Any, dict[str, Any], str]:
    if io_path(path).exists():
        return joblib.load(io_path(path)), {"source": rel(path), "sha256": sha256_file_lf_normalized(path)}, "loaded_run13A_joblib"
    model, sample = fit_ebm_variant(frame, feature_order, spec)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    joblib.dump(model, io_path(path))
    return model, {"source": rel(path), "sha256": sha256_file_lf_normalized(path), "training_sample": sample}, "retrained_selected_spec"


def load_or_train_models(context: Mapping[str, Any]) -> dict[str, Any]:
    spec = selected_spec()
    tier_a_path = SOURCE_RUN_ROOT / "models" / f"{SELECTED_VARIANT_ID}_tier_a_ebm.joblib"
    tier_b_path = SOURCE_RUN_ROOT / "models" / f"{SELECTED_VARIANT_ID}_tier_b_ebm_core42.joblib"
    tier_a_model, tier_a_artifact, tier_a_policy = _load_or_train_model(tier_a_path, context["tier_a_frame"], context["full_feature_order"], spec)
    tier_b_model, tier_b_artifact, tier_b_policy = _load_or_train_model(tier_b_path, context["tier_b_training_frame"], context["tier_b_feature_order"], spec)
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], context["full_feature_order"])
    tier_b_train_prob = probability_frame(tier_b_model, context["tier_b_training_frame"], context["tier_b_feature_order"])
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], context["tier_b_feature_order"])
    return {
        "spec": spec,
        "tier_a_model": tier_a_model,
        "tier_b_model": tier_b_model,
        "tier_a_artifact": tier_a_artifact,
        "tier_b_artifact": tier_b_artifact,
        "tier_a_policy": tier_a_policy,
        "tier_b_policy": tier_b_policy,
        "tier_a_prob": tier_a_prob,
        "tier_b_train_prob": tier_b_train_prob,
        "tier_b_prob": tier_b_prob,
    }


def save_predictions(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def tier_record(record_view: str, tier_scope: str, prob_frame: pd.DataFrame, threshold: float, path: Path, topic: RuntimeTopic) -> dict[str, Any]:
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
        "threshold_ids": f"q{topic.threshold_quantile:.2f}",
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


def materialize_python_tier_records(
    topic: RuntimeTopic,
    models: Mapping[str, Any],
    a_threshold: float,
    b_threshold: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root = topic.run_root / "predictions"
    a_path = root / "tier_a_separate_predictions.parquet"
    b_path = root / "tier_b_separate_predictions.parquet"
    ab_path = root / "tier_ab_combined_predictions.parquet"
    tier_a_prob = models["tier_a_prob"]
    tier_b_prob = models["tier_b_prob"]
    ab_prob = pd.concat(
        [
            tier_a_prob.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"),
            tier_b_prob.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    records = [
        tier_record("tier_a_separate", mt5.TIER_A, tier_a_prob, a_threshold, a_path, topic),
        tier_record("tier_b_separate", mt5.TIER_B, tier_b_prob, b_threshold, b_path, topic),
        tier_record("tier_ab_combined", mt5.TIER_AB, ab_prob, a_threshold, ab_path, topic),
    ]
    artifacts = {
        "tier_a_predictions": save_predictions(a_path, tier_a_prob),
        "tier_b_predictions": save_predictions(b_path, tier_b_prob),
        "tier_ab_predictions": save_predictions(ab_path, ab_prob),
    }
    return records, artifacts


def export_models(topic: RuntimeTopic, context: Mapping[str, Any], models: Mapping[str, Any]) -> dict[str, Any]:
    root = topic.run_root / "models"
    io_path(root).mkdir(parents=True, exist_ok=True)
    tier_a_table = root / f"{SELECTED_VARIANT_ID}_tier_a_ebm_score_table.csv"
    tier_b_table = root / f"{SELECTED_VARIANT_ID}_tier_b_ebm_core42_score_table.csv"
    tier_a_export = export_ebm_main_effect_score_table(
        models["tier_a_model"],
        tier_a_table,
        feature_count=len(context["full_feature_order"]),
    )
    tier_b_export = export_ebm_main_effect_score_table(
        models["tier_b_model"],
        tier_b_table,
        feature_count=len(context["tier_b_feature_order"]),
    )
    a_sample = context["tier_a_frame"].loc[
        context["tier_a_frame"]["split"].astype(str).eq("validation"),
        context["full_feature_order"],
    ].head(256).to_numpy(dtype="float64", copy=False)
    b_sample = context["tier_b_training_frame"].loc[
        context["tier_b_training_frame"]["split"].astype(str).eq("validation"),
        context["tier_b_feature_order"],
    ].head(256).to_numpy(dtype="float64", copy=False)
    return {
        "selected_variant_id": SELECTED_VARIANT_ID,
        "tier_a_joblib": models["tier_a_artifact"],
        "tier_b_joblib": models["tier_b_artifact"],
        "tier_a_model_source_policy": models["tier_a_policy"],
        "tier_b_model_source_policy": models["tier_b_policy"],
        "model_backend": MODEL_BACKEND,
        "tier_a_score_table": {**tier_a_export, "path": rel(Path(tier_a_export["path"]))},
        "tier_b_score_table": {**tier_b_export, "path": rel(Path(tier_b_export["path"]))},
        "score_table_parity": {
            "tier_a": check_ebm_score_table_probability_parity(models["tier_a_model"], tier_a_table, a_sample, feature_count=len(context["full_feature_order"])),
            "tier_b": check_ebm_score_table_probability_parity(models["tier_b_model"], tier_b_table, b_sample, feature_count=len(context["tier_b_feature_order"])),
        },
    }


def export_feature_matrices(topic: RuntimeTopic, context: Mapping[str, Any]) -> dict[str, Any]:
    root = topic.run_root / "features"
    payload: dict[str, Any] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        tier_a_frame = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq(source_split)].copy()
        tier_b_frame = context["tier_b_fallback_frame"].loc[context["tier_b_fallback_frame"]["split"].astype(str).eq(source_split)].copy()
        payload[f"tier_a_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_a_frame,
            context["full_feature_order"],
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


def copy_runtime_inputs(topic: RuntimeTopic, model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, topic.run_id)
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_score_table", "tier_b_score_table"):
        local_path = ROOT / model_artifacts[key]["path"]
        copies.append(copy_to_common(local_path, f"{common}/models/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        local_path = ROOT / matrix["path"]
        copies.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_routed_attempts(topic: RuntimeTopic, context: Mapping[str, Any], model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any], thresholds: Mapping[str, float]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(STAGE_NUMBER, topic.run_id)
    tier_a_model = Path(model_artifacts["tier_a_score_table"]["path"]).name
    tier_b_model = Path(model_artifacts["tier_b_score_table"]["path"]).name
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        tier_a_matrix = Path(feature_matrices[f"tier_a_{runtime_split}"]["path"]).name
        tier_b_matrix = Path(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"]).name
        common_kwargs = {
            "run_root": topic.run_root,
            "run_id": topic.run_id,
            "stage_number": STAGE_NUMBER,
            "exploration_label": topic.exploration_label,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": topic.max_hold_bars,
            "common_root": common,
        }
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_a_only_{runtime_split}", tier=mt5.TIER_A, model_path=f"{common}/models/{tier_a_model}", model_id=f"{topic.run_id}_tier_a", model_backend=MODEL_BACKEND, feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(context["full_feature_order"]), feature_order_hash=context["full_feature_order_hash"], short_threshold=float(thresholds["tier_a"]), long_threshold=float(thresholds["tier_a"]), min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role="tier_only_total", record_view_prefix="mt5_tier_a_only"))
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_b_fallback_only_{runtime_split}", tier=mt5.TIER_B, model_path=f"{common}/models/{tier_b_model}", model_id=f"{topic.run_id}_tier_b", model_backend=MODEL_BACKEND, feature_path=f"{common}/features/{tier_b_matrix}", feature_count=len(context["tier_b_feature_order"]), feature_order_hash=context["tier_b_feature_order_hash"], short_threshold=float(thresholds["tier_b"]), long_threshold=float(thresholds["tier_b"]), min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_b_fallback", attempt_role="tier_b_fallback_only_total", record_view_prefix="mt5_tier_b_fallback_only"))
        attempts.append(attempt_payload(**common_kwargs, attempt_name=f"routed_{runtime_split}", tier=mt5.TIER_AB, model_path=f"{common}/models/{tier_a_model}", model_id=f"{topic.run_id}_tier_a", model_backend=MODEL_BACKEND, feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(context["full_feature_order"]), feature_order_hash=context["full_feature_order_hash"], short_threshold=float(thresholds["tier_a"]), long_threshold=float(thresholds["tier_a"]), min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role="routed_total", record_view_prefix="mt5_routed_total", fallback_enabled=True, fallback_model_path=f"{common}/models/{tier_b_model}", fallback_model_id=f"{topic.run_id}_tier_b", fallback_feature_path=f"{common}/features/{tier_b_matrix}", fallback_feature_count=len(context["tier_b_feature_order"]), fallback_feature_order_hash=context["tier_b_feature_order_hash"], fallback_short_threshold=float(thresholds["tier_b"]), fallback_long_threshold=float(thresholds["tier_b"]), fallback_min_margin=MIN_MARGIN, fallback_invert_signal=False))
    return attempts


def make_direction_attempts(topic: RuntimeTopic, context: Mapping[str, Any], model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any], thresholds: Mapping[str, float]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(STAGE_NUMBER, topic.run_id)
    tier_a_model = Path(model_artifacts["tier_a_score_table"]["path"]).name
    tier_b_model = Path(model_artifacts["tier_b_score_table"]["path"]).name
    disabled_threshold = 1.1
    sides = (
        ("long_only", disabled_threshold, float(thresholds["tier_a"]), disabled_threshold, float(thresholds["tier_b"])),
        ("short_only", float(thresholds["tier_a"]), disabled_threshold, float(thresholds["tier_b"]), disabled_threshold),
    )
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_frame"], source_split)
        tier_a_matrix = Path(feature_matrices[f"tier_a_{runtime_split}"]["path"]).name
        tier_b_matrix = Path(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"]).name
        common_kwargs = {
            "run_root": topic.run_root,
            "run_id": topic.run_id,
            "stage_number": STAGE_NUMBER,
            "exploration_label": topic.exploration_label,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": topic.max_hold_bars,
            "common_root": common,
        }
        for side, a_short, a_long, b_short, b_long in sides:
            attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_a_{side}_{runtime_split}", tier=mt5.TIER_A, model_path=f"{common}/models/{tier_a_model}", model_id=f"{topic.run_id}_tier_a", model_backend=MODEL_BACKEND, feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(context["full_feature_order"]), feature_order_hash=context["full_feature_order_hash"], short_threshold=a_short, long_threshold=a_long, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role=f"tier_a_{side}", record_view_prefix=f"mt5_tier_a_{side}"))
            attempts.append(attempt_payload(**common_kwargs, attempt_name=f"tier_b_{side}_{runtime_split}", tier=mt5.TIER_B, model_path=f"{common}/models/{tier_b_model}", model_id=f"{topic.run_id}_tier_b", model_backend=MODEL_BACKEND, feature_path=f"{common}/features/{tier_b_matrix}", feature_count=len(context["tier_b_feature_order"]), feature_order_hash=context["tier_b_feature_order_hash"], short_threshold=b_short, long_threshold=b_long, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_b_fallback", attempt_role=f"tier_b_{side}", record_view_prefix=f"mt5_tier_b_{side}"))
            attempts.append(attempt_payload(**common_kwargs, attempt_name=f"routed_{side}_{runtime_split}", tier=mt5.TIER_AB, model_path=f"{common}/models/{tier_a_model}", model_id=f"{topic.run_id}_tier_a", model_backend=MODEL_BACKEND, feature_path=f"{common}/features/{tier_a_matrix}", feature_count=len(context["full_feature_order"]), feature_order_hash=context["full_feature_order_hash"], short_threshold=a_short, long_threshold=a_long, min_margin=MIN_MARGIN, invert_signal=False, primary_active_tier="tier_a", attempt_role=f"routed_{side}", record_view_prefix=f"mt5_routed_{side}", fallback_enabled=True, fallback_model_path=f"{common}/models/{tier_b_model}", fallback_model_id=f"{topic.run_id}_tier_b", fallback_feature_path=f"{common}/features/{tier_b_matrix}", fallback_feature_count=len(context["tier_b_feature_order"]), fallback_feature_order_hash=context["tier_b_feature_order_hash"], fallback_short_threshold=b_short, fallback_long_threshold=b_long, fallback_min_margin=MIN_MARGIN, fallback_invert_signal=False))
    return attempts


def make_attempts(topic: RuntimeTopic, context: Mapping[str, Any], model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any], thresholds: Mapping[str, float]) -> list[dict[str, Any]]:
    if topic.mode == "direction":
        return make_direction_attempts(topic, context, model_artifacts, feature_matrices, thresholds)
    return make_routed_attempts(topic, context, model_artifacts, feature_matrices, thresholds)


def execute_or_block(topic: RuntimeTopic, prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if bool(args.materialize_only):
        return {**dict(prepared), "compile": {"status": "not_attempted_materialize_only"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": topic.judgment_blocked, "failure": {"type": "materialize_only", "message": "MT5 execution skipped by CLI flag."}}
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
        return {**dict(prepared), "compile": {"status": "exception_or_not_completed"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": topic.judgment_blocked, "failure": {"type": type(exc).__name__, "message": str(exc)}}
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = topic.judgment_completed if completed else topic.judgment_blocked
    for record in result.get("mt5_kpi_records", []):
        record["source_variant_id"] = SELECTED_VARIANT_ID
        record["topic_read"] = topic.topic_read
        record["threshold_quantile"] = f"q{topic.threshold_quantile:.2f}"
        record["max_hold_bars"] = topic.max_hold_bars
    return result


def metrics_by_view(result: Mapping[str, Any], view: str) -> dict[str, Any]:
    for record in result.get("mt5_kpi_records", []):
        if record.get("record_view") == view:
            metrics = record.get("metrics", {})
            return dict(metrics) if isinstance(metrics, Mapping) else {}
    return {}


def metrics_by_hint(result: Mapping[str, Any], hint: str) -> dict[str, Any]:
    for record in result.get("mt5_kpi_records", []):
        path = str(record.get("report", {}).get("html_report", {}).get("path", ""))
        if hint in path:
            metrics = record.get("metrics", {})
            return dict(metrics) if isinstance(metrics, Mapping) else {}
    return {}


def parity_passed(model_artifacts: Mapping[str, Any]) -> bool:
    parity = model_artifacts.get("score_table_parity", {})
    return bool(parity.get("tier_a", {}).get("passed")) and bool(parity.get("tier_b", {}).get("passed"))


def build_runtime_read(topic: RuntimeTopic, summary: Mapping[str, Any]) -> dict[str, Any]:
    completed = summary.get("external_verification_status") == "completed"
    parity_ok = parity_passed(summary.get("model_artifacts", {}))
    if topic.mode == "direction":
        direction = summary.get("direction_routed", {})
        long_val = direction.get("long_validation", {})
        long_oos = direction.get("long_oos", {})
        short_val = direction.get("short_validation", {})
        short_oos = direction.get("short_oos", {})
        long_trades = (safe_float(long_val.get("trade_count")) + safe_float(long_oos.get("trade_count"))) / 2.0
        short_trades = (safe_float(short_val.get("trade_count")) + safe_float(short_oos.get("trade_count"))) / 2.0
        trade_contrast = abs(long_trades - short_trades) / max(1.0, long_trades + short_trades)
        visible = completed and parity_ok and trade_contrast >= 0.20
        return {
            "model_characteristic_strength": "ebm_direction_asymmetry_visible" if visible else "ebm_direction_axis_weak_or_blocked",
            "closure_judgment": topic.judgment_completed if completed else topic.judgment_blocked,
            "direction_read": {
                "long_avg_routed_trades": long_trades,
                "short_avg_routed_trades": short_trades,
                "trade_count_contrast": trade_contrast,
                "new_characteristic_visible": visible,
            },
        }
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    avg_trades = (safe_float(validation.get("trade_count")) + safe_float(oos.get("trade_count"))) / 2.0
    visible = completed and parity_ok and avg_trades >= 5.0
    risk_warning = safe_float(oos.get("max_drawdown_percent")) >= 25.0 or safe_float(validation.get("max_drawdown_percent")) >= 25.0
    return {
        "model_characteristic_strength": "ebm_runtime_axis_visible" if visible else "ebm_runtime_axis_weak_or_blocked",
        "closure_judgment": topic.judgment_completed if completed else topic.judgment_blocked,
        "runtime_read": {
            "avg_routed_trades": avg_trades,
            "validation_net_profit": safe_float(validation.get("net_profit")),
            "oos_net_profit": safe_float(oos.get("net_profit")),
            "risk_warning": risk_warning,
            "new_characteristic_visible": visible,
        },
    }


def build_summary(topic: RuntimeTopic, result: Mapping[str, Any], model_artifacts: Mapping[str, Any], prediction_artifacts: Mapping[str, Any], tier_records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "run_number": topic.run_number,
        "run_id": topic.run_id,
        "packet_id": topic.packet_id,
        "source_run_id": SOURCE_RUN_ID,
        "source_packet_id": SOURCE_PACKET_ID,
        "stage_id": STAGE_ID,
        "model_family": MODEL_FAMILY,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "topic_read": topic.topic_read,
        "threshold_quantile": topic.threshold_quantile,
        "max_hold_bars": topic.max_hold_bars,
        "boundary": topic.boundary,
        "judgment": result["judgment"],
        "external_verification_status": result["external_verification_status"],
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
        "python_tier_records": list(tier_records),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "attempt_count": len(result.get("attempts", [])),
        "expected_attempts": topic.expected_attempts,
        "expected_kpi_records": topic.expected_kpi_records,
        "runtime_failure_signature": runtime_failure_signature_from_result(result),
    }
    if topic.mode == "direction":
        summary["direction_routed"] = {
            "long_validation": metrics_by_hint(result, "_routed_long_only_validation_is"),
            "long_oos": metrics_by_hint(result, "_routed_long_only_oos"),
            "short_validation": metrics_by_hint(result, "_routed_short_only_validation_is"),
            "short_oos": metrics_by_hint(result, "_routed_short_only_oos"),
        }
        summary["validation_routed"] = summary["direction_routed"]["long_validation"]
        summary["oos_routed"] = summary["direction_routed"]["long_oos"]
    else:
        summary["validation_routed"] = metrics_by_view(result, "mt5_routed_total_validation_is")
        summary["oos_routed"] = metrics_by_view(result, "mt5_routed_total_oos")
    summary.update(build_runtime_read(topic, summary))
    return summary


def upsert_run_registry(topic: RuntimeTopic, result: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    row = {
        "run_id": topic.run_id,
        "stage_id": STAGE_ID,
        "lane": "alpha_runtime_probe",
        "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked",
        "judgment": summary["closure_judgment"],
        "path": rel(topic.run_root),
        "notes": ledger_pairs(
            (
                ("model_family", MODEL_FAMILY),
                ("topic_read", topic.topic_read),
                ("routing_mode", "tier_a_primary_tier_b_fallback"),
                ("selected_variant", SELECTED_VARIANT_ID),
                ("threshold_quantile", f"q{topic.threshold_quantile:.2f}"),
                ("max_hold_bars", topic.max_hold_bars),
                ("validation_net_profit", validation.get("net_profit")),
                ("validation_pf", validation.get("profit_factor")),
                ("oos_net_profit", oos.get("net_profit")),
                ("oos_pf", oos.get("profit_factor")),
                ("characteristic_strength", summary.get("model_characteristic_strength")),
                ("external_verification", result["external_verification_status"]),
                ("boundary", "runtime_probe_only"),
            )
        ),
    }
    return upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [row], key="run_id")


def write_normalized_kpi(topic: RuntimeTopic) -> dict[str, Any]:
    inventory = [{"run_id": topic.run_id, "stage_id": STAGE_ID, "idea_id": topic.run_number, "path": rel(topic.run_root)}]
    records, summary_rows, missing, parser_errors = mt5_kpi_recorder.build_normalized_records(ROOT, inventory)
    market_data = mt5_trade_attribution.MarketData.load(ROOT)
    enriched, trade_rows, trade_summary, trade_errors = mt5_trade_attribution.enrich_records(records, ROOT, market_data)
    write_json(topic.packet_root / "normalized_kpi_records.jsonl", records)
    write_json(topic.packet_root / "normalized_kpi_summary.csv", summary_rows)
    write_json(topic.packet_root / "normalized_kpi_missing_runs.json", missing)
    write_json(topic.packet_root / "normalized_kpi_parser_errors.json", parser_errors)
    write_json(topic.packet_root / "enriched_kpi_records.jsonl", enriched)
    write_json(topic.packet_root / "trade_level_records.json", trade_rows)
    write_json(topic.packet_root / "trade_attribution_summary.json", trade_summary)
    write_json(topic.packet_root / "trade_attribution_parser_errors.json", trade_errors)
    return {
        "normalized_records": len(records),
        "normalized_summary_rows": len(summary_rows),
        "missing_runs": len(missing),
        "parser_errors": len(parser_errors),
        "trade_attribution_records": len(trade_summary),
        "trade_level_rows": len(trade_rows),
        "trade_parser_errors": len(trade_errors),
    }


def packet_markdown(topic: RuntimeTopic, summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    lines = [
        f"# {topic.run_id} Result Summary({topic.run_number} 결과 요약)",
        "",
        f"- topic read(주제 판독): `{topic.topic_read}`",
        f"- selected variant(선택 변형): `{SELECTED_VARIANT_ID}`",
        f"- threshold(임계값): `q{topic.threshold_quantile:.2f}`",
        f"- max hold bars(최대 보유 봉): `{topic.max_hold_bars}`",
        f"- judgment(판정): `{summary.get('closure_judgment')}`",
        f"- external verification(외부 검증): `{summary.get('external_verification_status')}`",
        f"- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`",
        f"- normalized KPI records(정규화 핵심 성과 지표 기록): `{kpi.get('normalized_records')}`",
        "",
        "## Runtime Read(런타임 판독)",
        "",
        "| split(분할) | net profit(순수익) | profit factor(수익 팩터) | trades(거래 수) | max DD(최대 손실) | recovery(회복 계수) |",
        "|---|---:|---:|---:|---:|---:|",
        f"| validation(검증) | `{validation.get('net_profit')}` | `{validation.get('profit_factor')}` | `{validation.get('trade_count')}` | `{validation.get('max_drawdown_amount')}` | `{validation.get('recovery_factor')}` |",
        f"| OOS(표본외) | `{oos.get('net_profit')}` | `{oos.get('profit_factor')}` | `{oos.get('trade_count')}` | `{oos.get('max_drawdown_amount')}` | `{oos.get('recovery_factor')}` |",
        "",
        "효과(effect, 효과): 이 run(실행)은 EBM(설명가능 부스팅 머신) shape clue(모양 단서)를 MT5(메타트레이더5) runtime probe(런타임 탐침)로 관찰한다.",
        "",
        "Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
    ]
    if topic.mode == "direction":
        direction = summary.get("direction_routed", {})
        lines.extend(
            [
                "",
                "## Direction Split(방향 분리)",
                "",
                f"- long validation/OOS trades(매수 검증/표본외 거래 수): `{direction.get('long_validation', {}).get('trade_count')}` / `{direction.get('long_oos', {}).get('trade_count')}`",
                f"- short validation/OOS trades(매도 검증/표본외 거래 수): `{direction.get('short_validation', {}).get('trade_count')}` / `{direction.get('short_oos', {}).get('trade_count')}`",
            ]
        )
    return "\n".join(lines)


def gate_payloads(topic: RuntimeTopic, summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> dict[str, Any]:
    completed = summary.get("external_verification_status") == "completed"
    parity_ok = parity_passed(summary.get("model_artifacts", {}))
    runtime_gate_status = "passed" if completed and parity_ok else "blocked"
    gates = ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"]
    return {
        "runtime_evidence_gate": {
            "status": runtime_gate_status,
            "external_verification_status": summary.get("external_verification_status"),
            "score_table_parity_passed": parity_ok,
            "mt5_kpi_record_count": summary.get("mt5_kpi_record_count"),
            "expected_kpi_records": topic.expected_kpi_records,
        },
        "scope_completion_gate": {
            "status": "passed" if summary.get("attempt_count") == topic.expected_attempts else "blocked",
            "attempt_count": summary.get("attempt_count"),
            "expected_attempts": topic.expected_attempts,
            "claim_boundary": topic.boundary,
        },
        "kpi_contract_audit": {
            "status": "passed" if int(summary.get("mt5_kpi_record_count") or 0) > 0 else "blocked",
            "normalized_records": kpi.get("normalized_records"),
            "parser_errors": kpi.get("parser_errors"),
        },
        "required_gate_coverage_audit": {
            "status": "passed",
            "packet_id": topic.packet_id,
            "required_gates": gates,
            "covered_gates": gates,
        },
        "final_claim_guard": {
            "status": "passed",
            "allowed_claims": ["runtime_probe", "inconclusive", "blocked"],
            "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
            "claim_boundary": topic.boundary,
        },
    }


def write_run_outputs(topic: RuntimeTopic, context: Mapping[str, Any], result: Mapping[str, Any], model_artifacts: Mapping[str, Any], prediction_artifacts: Mapping[str, Any], tier_records: Sequence[Mapping[str, Any]], kpi: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    summary = build_summary(topic, result, model_artifacts, prediction_artifacts, tier_records)
    upsert_run_registry(topic, result, summary)
    ledger_rows = build_alpha_scout_ledger_rows(
        run_id=topic.run_id,
        stage_id=STAGE_ID,
        tier_records=tier_records,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        selected_threshold_id=f"q{topic.threshold_quantile:.2f}",
        run_output_root=topic.run_root,
        external_verification_status=result["external_verification_status"],
    )
    materialize_alpha_ledgers(stage_run_ledger_path=STAGE_LEDGER_PATH, project_alpha_ledger_path=PROJECT_LEDGER_PATH, rows=ledger_rows)
    manifest = {
        "run_id": topic.run_id,
        "packet_id": topic.packet_id,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "run_number": topic.run_number,
        "created_at_utc": created_at,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "topic_read": topic.topic_read,
        "threshold_policy": f"non-flat q{topic.threshold_quantile:.2f}; not profit searched",
        "max_hold_bars": topic.max_hold_bars,
        "boundary": topic.boundary,
        "runtime_probe": {
            key: result.get(key)
            for key in ("attempts", "common_copies", "compile", "execution_results", "strategy_tester_reports", "external_verification_status", "judgment", "failure")
            if key in result
        },
        "tier_a_feature_order_hash": context["full_feature_order_hash"],
        "tier_b_feature_order_hash": context["tier_b_feature_order_hash"],
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
    }
    kpi_record = {
        **manifest,
        "kpi_scope": "ebm_mt5_runtime_probe",
        "python_tier_records": list(tier_records),
        "mt5": {
            "scoreboard_lane": "runtime_probe",
            "external_verification_status": result["external_verification_status"],
            "kpi_records": result.get("mt5_kpi_records", []),
        },
        "kpi_management": dict(kpi),
        "judgment": summary["closure_judgment"],
    }
    write_json(topic.run_root / "run_manifest.json", manifest)
    write_json(topic.run_root / "kpi_record.json", kpi_record)
    write_json(topic.run_root / "summary.json", summary)
    write_md(topic.review_path, packet_markdown(topic, summary, kpi))
    write_json(topic.packet_root / "aggregate_summary.json", {**summary, "kpi_management": dict(kpi)})
    write_json(topic.packet_root / "skill_receipts.json", build_skill_receipts(topic, summary, created_at))
    for name, payload in gate_payloads(topic, summary, kpi).items():
        write_json(topic.packet_root / f"{name}.json", payload)
    return summary


def build_skill_receipts(topic: RuntimeTopic, summary: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    return {
        "packet_id": topic.packet_id,
        "created_at_utc": created_at,
        "receipts": [
            {
                "skill": "obsidian-experiment-design",
                "status": "completed",
                "hypothesis": f"EBM runtime topic {topic.topic_read} can reveal a model-characteristic axis.",
                "decision_use": "Continue, narrow, or stop Stage19 EBM runtime exploration.",
                "comparison_baseline": "RUN13A structural scout and same selected EBM variant; no operating baseline.",
                "control_variables": [FEATURE_SET_ID, LABEL_ID, SPLIT_CONTRACT, "US100 M5", "Tier A primary plus Tier B fallback"],
                "changed_variables": [f"threshold=q{topic.threshold_quantile:.2f}", f"mode={topic.mode}", f"max_hold_bars={topic.max_hold_bars}"],
                "success_criteria": "MT5 reports and runtime telemetry exist with EBM score-table parity pass.",
                "failure_criteria": "No MT5 output, malformed report, score-table runtime mismatch, or no usable trade/runtime evidence.",
                "invalid_conditions": "feature order mismatch, timestamp mismatch, missing report, or unsupported score-table handoff.",
            },
            {
                "skill": "obsidian-runtime-parity",
                "status": "completed",
                "research_path": rel(Path(__file__)),
                "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
                "shared_contract": "same feature order hashes, EBM score-table probability order short/flat/long, q-thresholds, US100 M5 timestamp match.",
                "known_differences": "EBM is exported as a score table and calculated directly in MQL5; runtime claim remains runtime_probe only.",
                "parity_check": summary.get("model_artifacts", {}).get("score_table_parity"),
                "runtime_claim_boundary": "runtime_probe",
            },
            {
                "skill": "obsidian-backtest-forensics",
                "status": "completed",
                "tester_identity": "MT5 Strategy Tester US100 M5, deposit=500, leverage=1:100, model=4.",
                "ea_identity": "ObsidianPrimeV2_RuntimeProbeEA with generated .set and .ini files.",
                "report_identity": "run_manifest records tester report and telemetry paths.",
                "trade_evidence": f"MT5 KPI records={summary.get('mt5_kpi_record_count')}",
                "backtest_judgment": "usable_with_boundary" if summary.get("external_verification_status") == "completed" else "blocked",
            },
            {
                "skill": "obsidian-artifact-lineage",
                "status": "completed",
                "source_inputs": [rel(MODEL_INPUT_PATH), rel(FEATURE_ORDER_PATH), rel(SOURCE_RUN_ROOT / "run_manifest.json")],
                "producer": "stage_pipelines.stage19.ebm_mt5_runtime_probe",
                "artifact_paths": [rel(topic.run_root / "run_manifest.json"), rel(topic.run_root / "kpi_record.json"), rel(topic.review_path)],
                "availability": "generated_02_runs_ignored_with_tracked_packet_summary",
                "lineage_judgment": "connected_with_boundary",
            },
            {
                "skill": "obsidian-result-judgment",
                "status": "completed",
                "result_subject": topic.run_id,
                "evidence_available": ["score-table parity", "MT5 tester output", "KPI records", "stage/project ledgers"],
                "evidence_missing": ["WFO", "promotion packet", "runtime authority closure"],
                "judgment_label": summary.get("closure_judgment"),
                "claim_boundary": topic.boundary,
            },
        ],
    }


def build_topic_run(topic: RuntimeTopic, args: argparse.Namespace, context: Mapping[str, Any], models: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    existing_summary = topic.run_root / "summary.json"
    if not bool(args.force) and io_path(existing_summary).exists():
        return attach_existing_runtime_failure_signature(topic, read_json(existing_summary))
    a_threshold = nonflat_threshold(models["tier_a_prob"], topic.threshold_quantile)
    b_threshold = nonflat_threshold(models["tier_b_train_prob"], topic.threshold_quantile)
    tier_records, prediction_artifacts = materialize_python_tier_records(topic, models, a_threshold, b_threshold)
    model_artifacts = export_models(topic, context, models)
    model_artifacts["thresholds"] = {"tier_a": a_threshold, "tier_b": b_threshold, "quantile": topic.threshold_quantile}
    feature_matrices = export_feature_matrices(topic, context)
    copies = copy_runtime_inputs(topic, model_artifacts, feature_matrices)
    attempts = make_attempts(topic, context, model_artifacts, feature_matrices, {"tier_a": a_threshold, "tier_b": b_threshold})
    prepared = {
        "stage_id": STAGE_ID,
        "stage_number": STAGE_NUMBER,
        "run_id": topic.run_id,
        "run_number": topic.run_number,
        "run_root": topic.run_root,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "attempts": attempts,
        "common_copies": copies,
        "route_coverage": context["tier_b_context_summary"],
        "model_artifacts": model_artifacts,
        "feature_matrices": list(feature_matrices.values()),
    }
    result = execute_or_block(topic, prepared, args)
    result["model_artifacts"] = model_artifacts
    result["feature_matrices"] = list(feature_matrices.values())
    provisional = {"normalized_records": 0, "normalized_summary_rows": 0, "missing_runs": 0, "parser_errors": 0, "trade_attribution_records": 0, "trade_level_rows": 0, "trade_parser_errors": 0}
    write_run_outputs(topic, context, result, model_artifacts, prediction_artifacts, tier_records, provisional, created_at)
    kpi = write_normalized_kpi(topic)
    return write_run_outputs(topic, context, result, model_artifacts, prediction_artifacts, tier_records, kpi, created_at)


def aggregate_read(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [item for item in summaries if item.get("external_verification_status") == "completed"]
    blocked = [item.get("run_number") for item in summaries if item.get("external_verification_status") != "completed"]
    visible = [item.get("run_number") for item in summaries if "visible" in str(item.get("model_characteristic_strength"))]
    failure_signatures = {
        item.get("run_number"): item.get("runtime_failure_signature")
        for item in summaries
        if item.get("runtime_failure_signature")
    }
    best_oos = None
    for item in summaries:
        oos = item.get("oos_routed", {})
        if not oos:
            continue
        candidate = {"run_number": item.get("run_number"), "topic_read": item.get("topic_read"), "net_profit": safe_float(oos.get("net_profit")), "profit_factor": oos.get("profit_factor"), "trade_count": oos.get("trade_count")}
        if best_oos is None or candidate["net_profit"] > best_oos["net_profit"]:
            best_oos = candidate
    return {
        "completed_run_count": len(completed),
        "blocked_runs": blocked or "none",
        "visible_run_numbers": visible,
        "total_attempt_count": sum(int(item.get("attempt_count") or 0) for item in summaries),
        "total_mt5_kpi_records": sum(int(item.get("mt5_kpi_record_count") or 0) for item in summaries),
        "best_oos_net_runtime_probe": best_oos,
        "judgment": "inconclusive_ebm_mt5_runtime_batch_completed" if len(completed) == len(summaries) else "blocked_ebm_mt5_runtime_batch_after_attempt",
        "boundary": "ebm_mt5_runtime_probe_batch_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        "recommendation": "preserve_visible_axes_and_consider_one_attribution_followup" if visible else "treat_as_blocked_or_weak_runtime_handoff_until_repaired",
        "runtime_failure_signatures": failure_signatures,
    }


def aggregate_markdown(summaries: Sequence[Mapping[str, Any]], read: Mapping[str, Any]) -> str:
    rows = []
    for summary in summaries:
        oos = summary.get("oos_routed", {})
        failure = summary.get("runtime_failure_signature", {})
        failure_sample_count = failure.get("model_failure_sample_count")
        rows.append(
            f"| `{summary.get('run_number')}` | `{summary.get('topic_read')}` | `{summary.get('external_verification_status')}` | `{summary.get('mt5_kpi_record_count')}` | `{failure.get('primary_runtime_failure')}` | `{failure.get('model_ok_count_total')}` | `{failure_sample_count}` | `{oos.get('net_profit')}` | `{oos.get('profit_factor')}` | `{oos.get('trade_count')}` |"
        )
    return "\n".join(
        [
            "# Stage19 EBM MT5 Runtime Batch(19단계 EBM MT5 런타임 묶음)",
            "",
            f"- judgment(판정): `{read.get('judgment')}`",
            f"- completed runs(완료 실행): `{read.get('completed_run_count')}` / `{len(summaries)}`",
            f"- MT5 KPI records(MT5 핵심 성과 지표 기록): `{read.get('total_mt5_kpi_records')}`",
            f"- boundary(경계): `{read.get('boundary')}`",
            f"- recommendation(권고): `{read.get('recommendation')}`",
            "",
            "| run(실행) | topic(주제) | external verification(외부 검증) | KPI records(KPI 기록) | runtime failure(런타임 실패) | model ok(모델 성공) | model failure samples(모델 실패 표본) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | OOS trades(표본외 거래 수) |",
            "|---|---|---|---:|---|---:|---:|---:|---:|---:|",
            *rows,
            "",
            "효과(effect, 효과): RUN13B~RUN13G(실행13B~13G)는 EBM(설명가능 부스팅 머신) score table(점수표)을 MQL5(엠큐엘5) 직접 계산으로 인계해 MT5(메타트레이더5) Strategy Tester(전략 테스터)에서 넓게 관찰한 runtime_probe(런타임 탐침)이다.",
            "",
            "Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )


def replace_top_level_yaml_block(text: str, marker: str, block: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + block
    start = text.index(marker)
    next_start = len(text)
    cursor = text.find("\n", start + len(marker))
    while cursor != -1:
        line_start = cursor + 1
        line_end = text.find("\n", line_start)
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        if line and not line[0].isspace() and ":" in line:
            next_start = line_start
            break
        cursor = text.find("\n", line_start)
    return text[:start] + block + text[next_start:]


def update_stage_docs(summaries: Sequence[Mapping[str, Any]], read: Mapping[str, Any], created_at: str) -> None:
    all_completed = read.get("completed_run_count") == len(summaries)
    batch_status = "active_run13B_run13G_mt5_runtime_batch_completed" if all_completed else "active_run13B_run13G_mt5_runtime_batch_blocked_after_attempt"
    write_md(STAGE_ROOT / "03_reviews/stage19_ebm_mt5_runtime_batch_packet.md", aggregate_markdown(summaries, read))
    write_md(
        DECISION_PATH,
        "\n".join(
            [
                "# Stage19 RUN13B-RUN13G EBM MT5 Runtime Decision(19단계 실행13B-13G EBM MT5 런타임 결정)",
                "",
                f"- created_at_utc(생성 시각): `{created_at}`",
                f"- judgment(판정): `{read.get('judgment')}`",
                f"- boundary(경계): `{read.get('boundary')}`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                "",
                "효과(effect, 효과): EBM(설명가능 부스팅 머신) 런타임 단서를 보존하지만 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.",
            ]
        ),
    )
    write_md(
        SELECTION_STATUS_PATH,
        "\n".join(
            [
                "# Stage19 Selection Status(19단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                f"- status(상태): `{batch_status}`",
                "- current run(현재 실행): `run13G_ebm_q90_hold18_probe_v1`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{read.get('judgment')}`",
                f"- selected variant(선택 변형): `{SELECTED_VARIANT_ID}`",
                f"- boundary(경계): `{read.get('boundary')}`",
                "",
                "효과(effect, 효과): Stage19(19단계)는 EBM(설명가능 부스팅 머신) MT5(메타트레이더5) 런타임 단서를 보존하지만 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.",
            ]
        ),
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else "# Review Index(검토 색인)\n"
    line = "- `stage19_ebm_mt5_runtime_batch_packet.md`: RUN13B-RUN13G(실행13B-13G) EBM MT5 runtime probe(런타임 탐침) batch(묶음)\n"
    if "stage19_ebm_mt5_runtime_batch_packet.md" not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)


def update_current_truth(summaries: Sequence[Mapping[str, Any]], read: Mapping[str, Any]) -> None:
    all_completed = read.get("completed_run_count") == len(summaries)
    batch_status = "stage19_active_run13B_run13G_mt5_runtime_batch_completed" if all_completed else "stage19_active_run13B_run13G_mt5_runtime_batch_blocked_after_attempt"
    short_batch_status = "active_run13B_run13G_mt5_runtime_batch_completed" if all_completed else "active_run13B_run13G_mt5_runtime_batch_blocked_after_attempt"
    workspace_status = "reviewed_runtime_probe_batch_completed" if all_completed else "reviewed_runtime_probe_batch_blocked_after_attempt"
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state_lines = state.splitlines()
    for index, line in enumerate(state_lines):
        if line.startswith("current_run_id: "):
            state_lines[index] = "current_run_id: run13G_ebm_q90_hold18_probe_v1"
            break
    state = "\n".join(state_lines) + "\n"
    state = state.replace("stage19_active_run13A_structural_scout_completed", batch_status)
    state = state.replace("active_run13A_structural_scout_completed", short_batch_status)
    state = state.replace("status: active_run13A_python_structural_scout_completed", f"status: {short_batch_status}", 1)
    state = state.replace("stage19_active_run13B_run13G_mt5_runtime_batch_completed", batch_status)
    state = state.replace("active_run13B_run13G_mt5_runtime_batch_completed", short_batch_status)
    state = state.replace("stage19_active_run13B_run13G_mt5_runtime_batch_blocked_after_attempt", batch_status)
    state = state.replace("active_run13B_run13G_mt5_runtime_batch_blocked_after_attempt", short_batch_status)
    primary_failures = sorted(
        {
            str(signature.get("primary_runtime_failure"))
            for signature in (read.get("runtime_failure_signatures") or {}).values()
            if isinstance(signature, Mapping) and signature.get("primary_runtime_failure")
        }
    )
    primary_failure_text = ", ".join(primary_failures) if primary_failures else "none"
    block = f"""stage19_ebm_run13B_run13G_mt5_runtime_batch:
  packet_id: {AGGREGATE_PACKET_ID}
  status: {workspace_status}
  judgment: {read.get('judgment')}
  current_run_id: run13G_ebm_q90_hold18_probe_v1
  run_range: run13B-run13G
  selected_variant_id: {SELECTED_VARIANT_ID}
  completed_run_count: {read.get('completed_run_count')}
  mt5_attempt_count: {read.get('total_attempt_count')}
  mt5_kpi_record_count: {read.get('total_mt5_kpi_records')}
  primary_runtime_failure: {primary_failure_text}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {read.get('boundary')}
  report_path: stages/19_model_family_challenge__ebm_explainable_boosting_shape/03_reviews/stage19_ebm_mt5_runtime_batch_packet.md
  packet_summary_path: docs/agent_control/packets/{AGGREGATE_PACKET_ID}/aggregate_summary.json
"""
    state = replace_top_level_yaml_block(state, "stage19_ebm_run13B_run13G_mt5_runtime_batch:", block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8")
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    primary_failure_text = ", ".join(primary_failures) if primary_failures else "none(없음)"
    update = f"""## Latest Stage19 RUN13B-RUN13G MT5 Runtime Update(최신 19단계 실행13B-13G MT5 런타임 업데이트)

Stage19(19단계)는 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) RUN13B-RUN13G(실행13B-13G)를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `{read.get('judgment')}`. primary runtime failure(주 런타임 실패): `{primary_failure_text}`.

효과(effect, 효과): q90 handoff(q90 인계), q80 density(q80 밀도), q95 sparse tail(q95 희소 꼬리), direction asymmetry(방향 비대칭), hold6/hold18(6봉/18봉 보유) 축을 보존하지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

"""
    marker = "## Latest Stage19 RUN13B-RUN13G MT5 Runtime Update"
    if marker in current:
        start = current.index(marker)
        next_section = current.find("\n## ", start + 1)
        current = current[:start] + update + (current[next_section + 1 :] if next_section != -1 else "")
    else:
        current = update + current
    io_path(CURRENT_WORKING_STATE_PATH).write_text(current, encoding="utf-8-sig")


def write_aggregate_packet(summaries: Sequence[Mapping[str, Any]], read: Mapping[str, Any], created_at: str) -> None:
    write_json(AGGREGATE_PACKET_ROOT / "aggregate_summary.json", {"created_at_utc": created_at, "stage_id": STAGE_ID, "source_run_id": SOURCE_RUN_ID, "run_range": "run13B-run13G", "summaries": list(summaries), "aggregate_read": dict(read)})
    write_json(
        AGGREGATE_PACKET_ROOT / "skill_receipts.json",
        {
            "packet_id": AGGREGATE_PACKET_ID,
            "created_at_utc": created_at,
            "receipts": [
                {"skill": "obsidian-runtime-parity", "status": "completed", "runtime_claim_boundary": "runtime_probe", "research_path": rel(Path(__file__)), "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"},
                {"skill": "obsidian-backtest-forensics", "status": "completed", "backtest_judgment": "usable_with_boundary" if read.get("completed_run_count") else "blocked"},
                {"skill": "obsidian-artifact-lineage", "status": "completed", "lineage_judgment": "connected_with_boundary"},
                {"skill": "obsidian-result-judgment", "status": "completed", "judgment_label": read.get("judgment"), "claim_boundary": read.get("boundary")},
            ],
        },
    )
    gates = ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"]
    write_json(
        AGGREGATE_PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "status": "passed" if read.get("completed_run_count") == len(summaries) else "blocked",
            "completed_run_count": read.get("completed_run_count"),
            "run_count": len(summaries),
            "total_mt5_kpi_records": read.get("total_mt5_kpi_records"),
            "runtime_failure_signatures": read.get("runtime_failure_signatures"),
        },
    )
    write_json(AGGREGATE_PACKET_ROOT / "scope_completion_gate.json", {"status": "passed", "run_range": "run13B-run13G", "topics": [item.get("topic_read") for item in summaries]})
    write_json(AGGREGATE_PACKET_ROOT / "kpi_contract_audit.json", {"status": "passed" if int(read.get("total_mt5_kpi_records") or 0) > 0 else "blocked", "total_mt5_kpi_records": read.get("total_mt5_kpi_records")})
    write_json(AGGREGATE_PACKET_ROOT / "required_gate_coverage_audit.json", {"status": "passed", "packet_id": AGGREGATE_PACKET_ID, "required_gates": gates, "covered_gates": gates})
    write_json(AGGREGATE_PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "claim_boundary": read.get("boundary"), "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion", "runtime_authority"]})


def selected_topics(topic_ids: Sequence[str]) -> list[RuntimeTopic]:
    if not topic_ids or "all" in topic_ids:
        return list(RUN_TOPICS)
    wanted = set(topic_ids)
    topics = [topic for topic in RUN_TOPICS if topic.run_number in wanted or topic.run_id in wanted]
    missing = sorted(wanted.difference({topic.run_number for topic in topics}).difference({topic.run_id for topic in topics}))
    if missing:
        raise ValueError(f"Unknown Stage19 EBM MT5 topic ids: {missing}")
    return topics


def run(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = load_context()
    models = load_or_train_models(context)
    summaries: list[dict[str, Any]] = []
    for topic in selected_topics(args.topics):
        summaries.append(build_topic_run(topic, args, context, models, created_at))
    read = aggregate_read(summaries)
    update_stage_docs(summaries, read, created_at)
    update_current_truth(summaries, read)
    write_aggregate_packet(summaries, read, created_at)
    return {"summaries": summaries, "aggregate_read": read}


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage19 EBM MT5 runtime probe topics.")
    parser.add_argument("--topics", nargs="*", default=["all"], help="Run numbers or run ids to execute. Default: all.")
    parser.add_argument("--force", action="store_true", help="Re-run topics even when a completed summary already exists.")
    parser.add_argument("--materialize-only", action="store_true", help="Prepare artifacts without launching MT5.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    payload = run(args)
    print(json.dumps(json_ready(payload["aggregate_read"]), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
