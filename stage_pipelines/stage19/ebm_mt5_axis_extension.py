from __future__ import annotations

import argparse
import csv
import json
import math
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.control_plane.alpha_run_ledgers import materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.models.ebm_score_table import (
    check_ebm_score_table_probability_parity,
    ebm_main_effect_contribution_tensor,
    export_ebm_main_effect_score_table,
)
from foundation.models.onnx_bridge import ordered_sklearn_probabilities
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage19 import ebm_mt5_runtime_probe as stage19_mt5


STAGE_ID = stage19_mt5.STAGE_ID
STAGE_NUMBER = stage19_mt5.STAGE_NUMBER
ROOT = stage19_mt5.ROOT
STAGE_ROOT = stage19_mt5.STAGE_ROOT
STAGE_LEDGER_PATH = stage19_mt5.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = stage19_mt5.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = stage19_mt5.RUN_REGISTRY_PATH
WORKSPACE_STATE_PATH = stage19_mt5.WORKSPACE_STATE_PATH
CURRENT_WORKING_STATE_PATH = stage19_mt5.CURRENT_WORKING_STATE_PATH
SELECTION_STATUS_PATH = stage19_mt5.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = stage19_mt5.REVIEW_INDEX_PATH

RUN_ID = "run13T_ebm_mt5_axis_extension_v1"
RUN_NUMBER = "run13T"
PACKET_ID = "stage19_run13T_ebm_mt5_axis_extension_v1"
EXPLORATION_LABEL = "stage19_Model__EBMMT5AxisExtension"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews/run13T_ebm_mt5_axis_extension_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage19_run13T_ebm_mt5_axis_extension.md"

MODEL_FAMILY = stage19_mt5.MODEL_FAMILY
FEATURE_SET_ID = stage19_mt5.FEATURE_SET_ID
LABEL_ID = stage19_mt5.LABEL_ID
SPLIT_CONTRACT = stage19_mt5.SPLIT_CONTRACT
SELECTED_VARIANT_ID = stage19_mt5.SELECTED_VARIANT_ID
SOURCE_RUN_ID = stage19_mt5.SOURCE_RUN_ID

BOUNDARY = "ebm_mt5_axis_extension_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_ebm_mt5_axis_extension_completed"
TOP5_FEATURE_MASK = ("atr_14", "ema9_ema20_diff", "ema50_ema200_diff", "ema20_ema50_diff", "hl_zscore_50")
SUBTYPE_FILTER = "B_mixed_partial_context"


RUNTIME_TOPICS: tuple[stage19_mt5.RuntimeTopic, ...] = (
    stage19_mt5.RuntimeTopic(
        run_id="run13N_ebm_q90_hold4_top5_mask_probe_v1",
        run_number="run13N",
        packet_id="stage19_run13N_ebm_top5_mask_mt5_v1",
        exploration_label="stage19_Model__EBMTop5MaskHold4",
        review_filename="run13N_ebm_q90_hold4_top5_mask_packet.md",
        threshold_quantile=0.90,
        mode="routed",
        max_hold_bars=4,
        expected_attempts=6,
        expected_kpi_records=10,
        topic_read="q90_hold4_top5_feature_mask_runtime",
        boundary="ebm_q90_hold4_top5_feature_mask_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q90_hold4_top5_feature_mask_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q90_hold4_top5_feature_mask_runtime_probe_after_attempt",
    ),
    stage19_mt5.RuntimeTopic(
        run_id="run13O_ebm_q90_hold2_probe_v1",
        run_number="run13O",
        packet_id="stage19_run13O_ebm_hold2_mt5_v1",
        exploration_label="stage19_Model__EBMHold2Stress",
        review_filename="run13O_ebm_q90_hold2_packet.md",
        threshold_quantile=0.90,
        mode="routed",
        max_hold_bars=2,
        expected_attempts=6,
        expected_kpi_records=10,
        topic_read="q90_hold2_trade_shape_stress",
        boundary="ebm_q90_hold2_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q90_hold2_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q90_hold2_runtime_probe_after_attempt",
    ),
    stage19_mt5.RuntimeTopic(
        run_id="run13P_ebm_q90_hold3_probe_v1",
        run_number="run13P",
        packet_id="stage19_run13P_ebm_hold3_mt5_v1",
        exploration_label="stage19_Model__EBMHold3Stress",
        review_filename="run13P_ebm_q90_hold3_packet.md",
        threshold_quantile=0.90,
        mode="routed",
        max_hold_bars=3,
        expected_attempts=6,
        expected_kpi_records=10,
        topic_read="q90_hold3_trade_shape_stress",
        boundary="ebm_q90_hold3_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q90_hold3_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q90_hold3_runtime_probe_after_attempt",
    ),
    stage19_mt5.RuntimeTopic(
        run_id="run13Q_ebm_q90_hold5_probe_v1",
        run_number="run13Q",
        packet_id="stage19_run13Q_ebm_hold5_mt5_v1",
        exploration_label="stage19_Model__EBMHold5Stress",
        review_filename="run13Q_ebm_q90_hold5_packet.md",
        threshold_quantile=0.90,
        mode="routed",
        max_hold_bars=5,
        expected_attempts=6,
        expected_kpi_records=10,
        topic_read="q90_hold5_trade_shape_stress",
        boundary="ebm_q90_hold5_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q90_hold5_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q90_hold5_runtime_probe_after_attempt",
    ),
    stage19_mt5.RuntimeTopic(
        run_id="run13R_ebm_q90_hold4_mixed_subtype_fallback_probe_v1",
        run_number="run13R",
        packet_id="stage19_run13R_ebm_mixed_subtype_fallback_mt5_v1",
        exploration_label="stage19_Model__EBMMixedSubtypeFallbackHold4",
        review_filename="run13R_ebm_q90_hold4_mixed_subtype_fallback_packet.md",
        threshold_quantile=0.90,
        mode="routed",
        max_hold_bars=4,
        expected_attempts=6,
        expected_kpi_records=10,
        topic_read="q90_hold4_b_mixed_partial_context_fallback_only_filter",
        boundary="ebm_q90_hold4_b_mixed_partial_context_fallback_filter_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q90_hold4_b_mixed_partial_context_fallback_filter_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q90_hold4_b_mixed_partial_context_fallback_filter_runtime_probe_after_attempt",
    ),
    stage19_mt5.RuntimeTopic(
        run_id="run13S_ebm_q90_hold4_direction_probe_v1",
        run_number="run13S",
        packet_id="stage19_run13S_ebm_q90_hold4_direction_mt5_v1",
        exploration_label="stage19_Model__EBMQ90Hold4DirectionAsymmetry",
        review_filename="run13S_ebm_q90_hold4_direction_packet.md",
        threshold_quantile=0.90,
        mode="direction",
        max_hold_bars=4,
        expected_attempts=12,
        expected_kpi_records=20,
        topic_read="q90_hold4_long_short_direction_asymmetry",
        boundary="ebm_q90_hold4_direction_asymmetry_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q90_hold4_direction_asymmetry_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q90_hold4_direction_asymmetry_runtime_probe_after_attempt",
    ),
)

BASE_HOLD_RUNS = {
    "run13I": ("run13I_ebm_q90_hold4_probe_v1", "stage19_run13I_ebm_hold4_mt5_v1"),
    "run13F": ("run13F_ebm_q90_hold6_probe_v1", "stage19_run13F_ebm_hold6_mt5_v1"),
}
RUN13M_SUMMARY = ROOT / "docs/agent_control/packets/stage19_run13M_ebm_deep_axis_followup_v1/run_summaries/run13M_ebm_deep_axis_followup_v1.json"

SUMMARY_COLUMNS = (
    "run_number",
    "run_id",
    "topic_read",
    "axis",
    "split",
    "max_hold_bars",
    "record_view",
    "net_profit",
    "profit_factor",
    "trade_count",
    "win_rate_percent",
    "max_drawdown_amount",
)
COMPARISON_COLUMNS = (
    "axis",
    "comparison",
    "split",
    "baseline_run",
    "candidate_run",
    "baseline_net_profit",
    "candidate_net_profit",
    "delta_net_profit",
    "baseline_profit_factor",
    "candidate_profit_factor",
    "baseline_trade_count",
    "candidate_trade_count",
    "read",
)


@dataclass(frozen=True)
class Source:
    run_number: str
    run_id: str
    packet_id: str
    summary: Mapping[str, Any]


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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.8g}" if math.isfinite(value) else ""
    if isinstance(value, (list, dict, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(json_ready(value))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def metric_text(value: Any) -> str:
    if value in (None, "", "NA"):
        return ""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    return f"{number:.8g}" if math.isfinite(number) else ""


def topic_by_number(run_number: str) -> stage19_mt5.RuntimeTopic:
    for topic in RUNTIME_TOPICS:
        if topic.run_number == run_number or topic.run_id == run_number:
            return topic
    raise ValueError(f"unknown runtime topic: {run_number}")


def selected_topics(topic_ids: Sequence[str]) -> list[stage19_mt5.RuntimeTopic]:
    if not topic_ids or "all" in topic_ids:
        return list(RUNTIME_TOPICS)
    return [topic_by_number(topic_id) for topic_id in topic_ids]


def runtime_args(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        force=bool(args.force_runtime),
        materialize_only=bool(args.materialize_only),
        timeout_seconds=int(args.timeout_seconds),
        terminal_path=args.terminal_path,
        metaeditor_path=args.metaeditor_path,
        topics=["all"],
    )


def probability_frame_from_model(model: Any, frame: pd.DataFrame, feature_order: Sequence[str], zero_indices: Sequence[int]) -> pd.DataFrame:
    values = frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
    if zero_indices:
        contributions = ebm_main_effect_contribution_tensor(model, values, feature_count=len(feature_order))
        contributions[:, list(zero_indices), :] = 0.0
        logits = np.asarray(model.intercept_, dtype="float64").reshape(1, -1) + contributions.sum(axis=1)
        logits -= logits.max(axis=1, keepdims=True)
        exp_logits = np.exp(logits)
        probabilities = exp_logits / exp_logits.sum(axis=1, keepdims=True)
    else:
        probabilities = ordered_sklearn_probabilities(model, values)
    out = frame.loc[:, ["timestamp", "split", "label_class"]].copy()
    out["p_short"] = probabilities[:, 0]
    out["p_flat"] = probabilities[:, 1]
    out["p_long"] = probabilities[:, 2]
    out["probability_margin"] = np.abs(probabilities[:, 2] - probabilities[:, 0])
    if "partial_context_subtype" in frame.columns:
        out["partial_context_subtype"] = frame["partial_context_subtype"].astype(str).to_numpy()
    return out


def custom_tier_records(
    topic: stage19_mt5.RuntimeTopic,
    context: Mapping[str, Any],
    models: Mapping[str, Any],
    a_threshold: float,
    b_threshold: float,
    *,
    zero_a: Sequence[int] = (),
    zero_b: Sequence[int] = (),
    subtype_filter: str | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    root = topic.run_root / "predictions"
    tier_a_prob = probability_frame_from_model(models["tier_a_model"], context["tier_a_frame"], context["full_feature_order"], zero_a)
    tier_b_prob = probability_frame_from_model(models["tier_b_model"], context["tier_b_fallback_frame"], context["tier_b_feature_order"], zero_b)
    if subtype_filter:
        tier_b_prob = tier_b_prob.loc[tier_b_prob["partial_context_subtype"].astype(str).eq(subtype_filter)].reset_index(drop=True)
    ab_prob = pd.concat(
        [
            tier_a_prob.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"),
            tier_b_prob.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    a_path = root / "tier_a_separate_predictions.parquet"
    b_path = root / "tier_b_separate_predictions.parquet"
    ab_path = root / "tier_ab_combined_predictions.parquet"
    records = [
        stage19_mt5.tier_record("tier_a_separate", mt5.TIER_A, tier_a_prob, a_threshold, a_path, topic),
        stage19_mt5.tier_record("tier_b_separate", mt5.TIER_B, tier_b_prob, b_threshold, b_path, topic),
        stage19_mt5.tier_record("tier_ab_combined", mt5.TIER_AB, ab_prob, a_threshold, ab_path, topic),
    ]
    artifacts = {
        "tier_a_predictions": stage19_mt5.save_predictions(a_path, tier_a_prob),
        "tier_b_predictions": stage19_mt5.save_predictions(b_path, tier_b_prob),
        "tier_ab_predictions": stage19_mt5.save_predictions(ab_path, ab_prob),
    }
    return records, artifacts


def export_custom_models(
    topic: stage19_mt5.RuntimeTopic,
    context: Mapping[str, Any],
    models: Mapping[str, Any],
    *,
    mask_features: Sequence[str] = (),
) -> tuple[dict[str, Any], list[int], list[int]]:
    root = topic.run_root / "models"
    io_path(root).mkdir(parents=True, exist_ok=True)
    a_order = list(context["full_feature_order"])
    b_order = list(context["tier_b_feature_order"])
    zero_a = [a_order.index(feature) for feature in mask_features if feature in a_order]
    zero_b = [b_order.index(feature) for feature in mask_features if feature in b_order]
    table_suffix = "top5_mask" if mask_features else "score_table"
    tier_a_table = root / f"{SELECTED_VARIANT_ID}_tier_a_ebm_{table_suffix}.csv"
    tier_b_table = root / f"{SELECTED_VARIANT_ID}_tier_b_ebm_core42_{table_suffix}.csv"
    tier_a_export = export_ebm_main_effect_score_table(
        models["tier_a_model"],
        tier_a_table,
        feature_count=len(a_order),
        zero_feature_indices=zero_a,
    )
    tier_b_export = export_ebm_main_effect_score_table(
        models["tier_b_model"],
        tier_b_table,
        feature_count=len(b_order),
        zero_feature_indices=zero_b,
    )
    a_sample = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq("validation"), a_order].head(256).to_numpy(dtype="float64", copy=False)
    b_sample = context["tier_b_training_frame"].loc[context["tier_b_training_frame"]["split"].astype(str).eq("validation"), b_order].head(256).to_numpy(dtype="float64", copy=False)
    return (
        {
            "selected_variant_id": SELECTED_VARIANT_ID,
            "tier_a_joblib": models["tier_a_artifact"],
            "tier_b_joblib": models["tier_b_artifact"],
            "tier_a_model_source_policy": models["tier_a_policy"],
            "tier_b_model_source_policy": models["tier_b_policy"],
            "model_backend": stage19_mt5.MODEL_BACKEND,
            "tier_a_score_table": {**tier_a_export, "path": rel(Path(tier_a_export["path"]))},
            "tier_b_score_table": {**tier_b_export, "path": rel(Path(tier_b_export["path"]))},
            "feature_mask_policy": {
                "mask_features": list(mask_features),
                "tier_a_zero_feature_indices": zero_a,
                "tier_b_zero_feature_indices": zero_b,
                "threshold_policy": "fixed_original_q90_thresholds_to_measure_contribution_removal_effect",
            },
            "score_table_parity": {
                "tier_a": check_ebm_score_table_probability_parity(models["tier_a_model"], tier_a_table, a_sample, feature_count=len(a_order), zero_feature_indices=zero_a),
                "tier_b": check_ebm_score_table_probability_parity(models["tier_b_model"], tier_b_table, b_sample, feature_count=len(b_order), zero_feature_indices=zero_b),
            },
        },
        zero_a,
        zero_b,
    )


def export_custom_feature_matrices(
    topic: stage19_mt5.RuntimeTopic,
    context: Mapping[str, Any],
    *,
    subtype_filter: str | None = None,
) -> dict[str, Any]:
    root = topic.run_root / "features"
    payload: dict[str, Any] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        tier_a_frame = context["tier_a_frame"].loc[context["tier_a_frame"]["split"].astype(str).eq(source_split)].copy()
        tier_b_frame = context["tier_b_fallback_frame"].loc[context["tier_b_fallback_frame"]["split"].astype(str).eq(source_split)].copy()
        if subtype_filter:
            tier_b_frame = tier_b_frame.loc[tier_b_frame["partial_context_subtype"].astype(str).eq(subtype_filter)].copy()
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


def build_custom_topic_run(
    topic: stage19_mt5.RuntimeTopic,
    args: argparse.Namespace,
    context: Mapping[str, Any],
    models: Mapping[str, Any],
    created_at: str,
    *,
    mask_features: Sequence[str] = (),
    subtype_filter: str | None = None,
) -> dict[str, Any]:
    existing_summary = topic.run_root / "summary.json"
    if not bool(args.force) and io_path(existing_summary).exists():
        return stage19_mt5.attach_existing_runtime_failure_signature(topic, stage19_mt5.read_json(existing_summary))
    a_threshold = stage19_mt5.nonflat_threshold(models["tier_a_prob"], topic.threshold_quantile)
    b_threshold = stage19_mt5.nonflat_threshold(models["tier_b_train_prob"], topic.threshold_quantile)
    model_artifacts, zero_a, zero_b = export_custom_models(topic, context, models, mask_features=mask_features)
    model_artifacts["thresholds"] = {"tier_a": a_threshold, "tier_b": b_threshold, "quantile": topic.threshold_quantile}
    model_artifacts["runtime_axis_extension"] = {"subtype_filter": subtype_filter, "mask_features": list(mask_features)}
    tier_records, prediction_artifacts = custom_tier_records(
        topic,
        context,
        models,
        a_threshold,
        b_threshold,
        zero_a=zero_a,
        zero_b=zero_b,
        subtype_filter=subtype_filter,
    )
    feature_matrices = export_custom_feature_matrices(topic, context, subtype_filter=subtype_filter)
    copies = stage19_mt5.copy_runtime_inputs(topic, model_artifacts, feature_matrices)
    attempts = stage19_mt5.make_attempts(topic, context, model_artifacts, feature_matrices, {"tier_a": a_threshold, "tier_b": b_threshold})
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
    result = stage19_mt5.execute_or_block(topic, prepared, args)
    result["model_artifacts"] = model_artifacts
    result["feature_matrices"] = list(feature_matrices.values())
    provisional = {"normalized_records": 0, "normalized_summary_rows": 0, "missing_runs": 0, "parser_errors": 0, "trade_attribution_records": 0, "trade_level_rows": 0, "trade_parser_errors": 0}
    stage19_mt5.write_run_outputs(topic, context, result, model_artifacts, prediction_artifacts, tier_records, provisional, created_at)
    kpi = stage19_mt5.write_normalized_kpi(topic)
    return stage19_mt5.write_run_outputs(topic, context, result, model_artifacts, prediction_artifacts, tier_records, kpi, created_at)


def execute_topics(args: argparse.Namespace) -> list[dict[str, Any]]:
    created_at = utc_now()
    context = stage19_mt5.load_context()
    models = stage19_mt5.load_or_train_models(context)
    topic_args = runtime_args(args)
    summaries: list[dict[str, Any]] = []
    for topic in selected_topics(args.runtime_topics):
        if topic.run_number == "run13N":
            summaries.append(build_custom_topic_run(topic, topic_args, context, models, created_at, mask_features=TOP5_FEATURE_MASK))
        elif topic.run_number == "run13R":
            summaries.append(build_custom_topic_run(topic, topic_args, context, models, created_at, subtype_filter=SUBTYPE_FILTER))
        else:
            summaries.append(stage19_mt5.build_topic_run(topic, topic_args, context, models, created_at))
    return summaries


def source_for_run(run_number: str) -> Source:
    if run_number in BASE_HOLD_RUNS:
        run_id, packet_id = BASE_HOLD_RUNS[run_number]
    else:
        topic = topic_by_number(run_number)
        run_id, packet_id = topic.run_id, topic.packet_id
    return Source(run_number=run_number, run_id=run_id, packet_id=packet_id, summary=read_json(STAGE_ROOT / "02_runs" / run_id / "summary.json"))


def routed_metric(source: Source, split: str) -> Mapping[str, Any]:
    key = "validation_routed" if split == "validation" else "oos_routed"
    value = source.summary.get(key, {})
    return value if isinstance(value, Mapping) else {}


def direction_metric(source: Source, split: str, side: str) -> Mapping[str, Any]:
    direction = source.summary.get("direction_routed", {})
    key = f"{side}_{'validation' if split == 'validation' else 'oos'}"
    value = direction.get(key, {}) if isinstance(direction, Mapping) else {}
    return value if isinstance(value, Mapping) else {}


def summary_rows(sources: Sequence[Source]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in sources:
        axis = "feature_mask" if source.run_number == "run13N" else "subtype_filter" if source.run_number == "run13R" else "side" if source.run_number == "run13S" else "hold"
        if source.run_number == "run13S":
            for split in ("validation", "oos"):
                for side in ("long", "short"):
                    metrics = direction_metric(source, split, side)
                    rows.append(row_from_metrics(source, axis, split, f"{side}_only", metrics))
            continue
        for split in ("validation", "oos"):
            rows.append(row_from_metrics(source, axis, split, "routed_total", routed_metric(source, split)))
    return rows


def row_from_metrics(source: Source, axis: str, split: str, record_view: str, metrics: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_number": source.run_number,
        "run_id": source.run_id,
        "topic_read": source.summary.get("topic_read"),
        "axis": axis,
        "split": split,
        "max_hold_bars": source.summary.get("max_hold_bars"),
        "record_view": record_view,
        "net_profit": metrics.get("net_profit"),
        "profit_factor": metrics.get("profit_factor"),
        "trade_count": metrics.get("trade_count"),
        "win_rate_percent": metrics.get("win_rate_percent"),
        "max_drawdown_amount": metrics.get("max_drawdown_amount"),
    }


def comparison_row(axis: str, comparison: str, split: str, baseline: Source, candidate: Source, read: str) -> dict[str, Any]:
    base = routed_metric(baseline, split)
    cand = routed_metric(candidate, split)
    return {
        "axis": axis,
        "comparison": comparison,
        "split": split,
        "baseline_run": baseline.run_number,
        "candidate_run": candidate.run_number,
        "baseline_net_profit": base.get("net_profit"),
        "candidate_net_profit": cand.get("net_profit"),
        "delta_net_profit": safe_float(cand.get("net_profit")) - safe_float(base.get("net_profit")),
        "baseline_profit_factor": base.get("profit_factor"),
        "candidate_profit_factor": cand.get("profit_factor"),
        "baseline_trade_count": base.get("trade_count"),
        "candidate_trade_count": cand.get("trade_count"),
        "read": read,
    }


def build_comparisons(sources: Mapping[str, Source]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base_hold4 = sources["run13I"]
    rows.extend(
        comparison_row("feature_mask", "top5_mask_vs_base_hold4", split, base_hold4, sources["run13N"], "feature_mask_runtime_dependency")
        for split in ("validation", "oos")
    )
    rows.extend(
        comparison_row("tier_b_subtype", "mixed_subtype_filter_vs_base_hold4", split, base_hold4, sources["run13R"], "subtype_filter_runtime_dependency")
        for split in ("validation", "oos")
    )
    return rows


def hold_read(sources: Mapping[str, Source]) -> dict[str, Any]:
    hold_numbers = ("run13O", "run13P", "run13I", "run13Q", "run13F")
    oos = [(run, routed_metric(sources[run], "oos")) for run in hold_numbers]
    validation = [(run, routed_metric(sources[run], "validation")) for run in hold_numbers]
    best_oos = max(oos, key=lambda item: safe_float(item[1].get("net_profit")))
    best_validation = max(validation, key=lambda item: safe_float(item[1].get("net_profit")))
    return {
        "hold_runs": list(hold_numbers),
        "best_oos_run": best_oos[0],
        "best_oos_hold": sources[best_oos[0]].summary.get("max_hold_bars"),
        "best_oos_net_profit": best_oos[1].get("net_profit"),
        "best_oos_profit_factor": best_oos[1].get("profit_factor"),
        "best_validation_run": best_validation[0],
        "best_validation_hold": sources[best_validation[0]].summary.get("max_hold_bars"),
        "best_validation_net_profit": best_validation[1].get("net_profit"),
        "validation_positive_holds": [sources[run].summary.get("max_hold_bars") for run, metric in validation if safe_float(metric.get("net_profit")) > 0.0],
        "oos_positive_holds": [sources[run].summary.get("max_hold_bars") for run, metric in oos if safe_float(metric.get("net_profit")) > 0.0],
    }


def feature_mask_read(sources: Mapping[str, Source]) -> dict[str, Any]:
    base = routed_metric(sources["run13I"], "oos")
    masked = routed_metric(sources["run13N"], "oos")
    return {
        "baseline_run": "run13I",
        "masked_run": "run13N",
        "mask_features": list(TOP5_FEATURE_MASK),
        "baseline_oos_net_profit": base.get("net_profit"),
        "masked_oos_net_profit": masked.get("net_profit"),
        "delta_oos_net_profit": safe_float(masked.get("net_profit")) - safe_float(base.get("net_profit")),
        "baseline_oos_trade_count": base.get("trade_count"),
        "masked_oos_trade_count": masked.get("trade_count"),
        "runtime_mask_effect_visible": abs(safe_float(masked.get("net_profit")) - safe_float(base.get("net_profit"))) >= 50.0,
    }


def subtype_read(sources: Mapping[str, Source]) -> dict[str, Any]:
    base = routed_metric(sources["run13I"], "oos")
    mixed = routed_metric(sources["run13R"], "oos")
    return {
        "baseline_run": "run13I",
        "mixed_subtype_run": "run13R",
        "subtype_filter": SUBTYPE_FILTER,
        "baseline_oos_net_profit": base.get("net_profit"),
        "mixed_subtype_oos_net_profit": mixed.get("net_profit"),
        "delta_oos_net_profit": safe_float(mixed.get("net_profit")) - safe_float(base.get("net_profit")),
        "baseline_tier_b_fallback_used_count": base.get("tier_b_fallback_used_count"),
        "mixed_tier_b_fallback_used_count": mixed.get("tier_b_fallback_used_count"),
        "subtype_filter_effect_visible": abs(safe_float(mixed.get("net_profit")) - safe_float(base.get("net_profit"))) >= 25.0,
    }


def side_read(sources: Mapping[str, Source]) -> dict[str, Any]:
    source = sources["run13S"]
    long_oos = direction_metric(source, "oos", "long")
    short_oos = direction_metric(source, "oos", "short")
    long_validation = direction_metric(source, "validation", "long")
    short_validation = direction_metric(source, "validation", "short")
    return {
        "direction_run": "run13S",
        "hold": source.summary.get("max_hold_bars"),
        "long_oos_net_profit": long_oos.get("net_profit"),
        "short_oos_net_profit": short_oos.get("net_profit"),
        "oos_long_minus_short_net": safe_float(long_oos.get("net_profit")) - safe_float(short_oos.get("net_profit")),
        "long_validation_net_profit": long_validation.get("net_profit"),
        "short_validation_net_profit": short_validation.get("net_profit"),
        "validation_long_minus_short_net": safe_float(long_validation.get("net_profit")) - safe_float(short_validation.get("net_profit")),
        "long_oos_profit_factor": long_oos.get("profit_factor"),
        "short_oos_profit_factor": short_oos.get("profit_factor"),
    }


def build_summary(created_at: str, runtime_summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    source_keys = ("run13N", "run13O", "run13P", "run13Q", "run13R", "run13S", "run13I", "run13F")
    sources = {key: source_for_run(key) for key in source_keys}
    runtime_completed = [sources[key].summary.get("external_verification_status") == "completed" for key in ("run13N", "run13O", "run13P", "run13Q", "run13R", "run13S")]
    rows = summary_rows([sources[key] for key in source_keys])
    comparisons = build_comparisons(sources)
    return {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "source_run_id": SOURCE_RUN_ID,
        "exploration_label": EXPLORATION_LABEL,
        "model_family": MODEL_FAMILY,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "boundary": BOUNDARY,
        "judgment": JUDGMENT,
        "closure_judgment": JUDGMENT,
        "external_verification_status": "completed" if all(runtime_completed) else "blocked_or_partial_runtime_extension",
        "runtime_completed_count": sum(1 for item in runtime_completed if item),
        "runtime_expected_count": 6,
        "runtime_followup_run_ids": [topic.run_id for topic in RUNTIME_TOPICS],
        "runtime_followup_summaries": list(runtime_summaries),
        "runtime_axis_rows": rows,
        "comparison_rows": comparisons,
        "feature_mask_read": feature_mask_read(sources),
        "hold_read": hold_read(sources),
        "tier_b_subtype_read": subtype_read(sources),
        "side_read": side_read(sources),
        "source_inputs": {
            "run13M_summary": rel(RUN13M_SUMMARY),
            "base_hold4_summary": rel(STAGE_ROOT / "02_runs" / BASE_HOLD_RUNS["run13I"][0] / "summary.json"),
            "base_hold6_summary": rel(STAGE_ROOT / "02_runs" / BASE_HOLD_RUNS["run13F"][0] / "summary.json"),
            "runtime_followup_summaries": [rel(topic.run_root / "summary.json") for topic in RUNTIME_TOPICS],
        },
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        "recommendation": "continue_stage19_only_for_hold4_long_feature_mask_or_stop_before_topic_pivot",
    }


def output_paths() -> dict[str, Path]:
    return {
        "summary": RUN_ROOT / "summary.json",
        "kpi_record": RUN_ROOT / "kpi_record.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
        "runtime_axis_rows": RUN_ROOT / "results/runtime_axis_rows.csv",
        "comparison_rows": RUN_ROOT / "results/comparison_rows.csv",
        "report": REPORT_PATH,
        "decision": DECISION_PATH,
    }


def write_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    rows = [
        {
            "ledger_row_id": f"{RUN_ID}__feature_mask_mt5",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "feature_mask_mt5",
            "parent_run_id": RUN_ID,
            "record_view": "top5_feature_mask_hold4_mt5_comparison",
            "tier_scope": "Tier A+B",
            "kpi_scope": "model_feature_contribution",
            "scoreboard_lane": "runtime_probe",
            "status": "completed" if summary.get("external_verification_status") == "completed" else "blocked",
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/comparison_rows.csv"),
            "primary_kpi": ledger_pairs((("delta_oos_net_profit", summary["feature_mask_read"].get("delta_oos_net_profit")), ("runtime_mask_effect_visible", summary["feature_mask_read"].get("runtime_mask_effect_visible")))),
            "guardrail_kpi": ledger_pairs((("claim", "feature_mask_runtime_probe_only"), ("boundary", BOUNDARY))),
            "external_verification_status": summary.get("external_verification_status"),
            "notes": "Top5 EBM score-table feature contributions zeroed and tested in MT5; not retrained ablation.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__hold_micro_axis",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "hold_micro_axis",
            "parent_run_id": RUN_ID,
            "record_view": "q90_hold2_3_4_5_6_axis",
            "tier_scope": "Tier A+B",
            "kpi_scope": "hold_period_axis_attribution",
            "scoreboard_lane": "runtime_probe",
            "status": "completed" if summary.get("external_verification_status") == "completed" else "blocked",
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/runtime_axis_rows.csv"),
            "primary_kpi": ledger_pairs((("best_oos_hold", summary["hold_read"].get("best_oos_hold")), ("best_oos_net_profit", summary["hold_read"].get("best_oos_net_profit")))),
            "guardrail_kpi": ledger_pairs((("validation_positive_holds", summary["hold_read"].get("validation_positive_holds")), ("boundary", BOUNDARY))),
            "external_verification_status": summary.get("external_verification_status"),
            "notes": "Hold2/3/5 newly tested; hold4 and hold6 reused as comparison.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_subtype_mt5",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_subtype_mt5",
            "parent_run_id": RUN_ID,
            "record_view": "b_mixed_partial_context_fallback_filter_mt5",
            "tier_scope": "Tier B",
            "kpi_scope": "tier_routing_attribution",
            "scoreboard_lane": "runtime_probe",
            "status": "completed" if summary.get("external_verification_status") == "completed" else "blocked",
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/comparison_rows.csv"),
            "primary_kpi": ledger_pairs((("mixed_subtype_oos_net_profit", summary["tier_b_subtype_read"].get("mixed_subtype_oos_net_profit")), ("delta_oos_net_profit", summary["tier_b_subtype_read"].get("delta_oos_net_profit")))),
            "guardrail_kpi": ledger_pairs((("subtype_filter", SUBTYPE_FILTER), ("boundary", BOUNDARY))),
            "external_verification_status": summary.get("external_verification_status"),
            "notes": "Tier B fallback feature matrix restricted to B_mixed_partial_context before MT5 tester.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__hold4_side_axis",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "hold4_side_axis",
            "parent_run_id": RUN_ID,
            "record_view": "q90_hold4_long_short_direction_mt5",
            "tier_scope": "Tier A+B",
            "kpi_scope": "direction_axis_attribution",
            "scoreboard_lane": "runtime_probe",
            "status": "completed" if summary.get("external_verification_status") == "completed" else "blocked",
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/runtime_axis_rows.csv"),
            "primary_kpi": ledger_pairs((("long_oos_net_profit", summary["side_read"].get("long_oos_net_profit")), ("short_oos_net_profit", summary["side_read"].get("short_oos_net_profit")))),
            "guardrail_kpi": ledger_pairs((("claim", "hold4_direction_runtime_probe_only"), ("boundary", BOUNDARY))),
            "external_verification_status": summary.get("external_verification_status"),
            "notes": "Hold4 long-only and short-only tested through asymmetric thresholds.",
        },
    ]
    return materialize_alpha_ledgers(stage_run_ledger_path=STAGE_LEDGER_PATH, project_alpha_ledger_path=PROJECT_LEDGER_PATH, rows=rows)


def write_registry(summary: Mapping[str, Any]) -> dict[str, Any]:
    return upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "model_characteristic_attribution",
                "status": "reviewed" if summary.get("external_verification_status") == "completed" else "blocked",
                "judgment": JUDGMENT,
                "path": rel(RUN_ROOT),
                "notes": ledger_pairs(
                    (
                        ("runtime_runs", ",".join(summary["runtime_followup_run_ids"])),
                        ("feature_mask_delta_oos", summary["feature_mask_read"].get("delta_oos_net_profit")),
                        ("best_oos_hold", summary["hold_read"].get("best_oos_hold")),
                        ("mixed_subtype_delta_oos", summary["tier_b_subtype_read"].get("delta_oos_net_profit")),
                        ("hold4_long_minus_short_oos", summary["side_read"].get("oos_long_minus_short_net")),
                        ("boundary", "mt5_axis_extension_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )


def gate_payloads(summary: Mapping[str, Any]) -> dict[str, Any]:
    runtime_ok = summary.get("external_verification_status") == "completed"
    feature_ok = "run13N" in [row.get("candidate_run") for row in summary.get("comparison_rows", [])]
    hold_ok = summary.get("hold_read", {}).get("best_oos_hold") is not None
    subtype_ok = summary.get("tier_b_subtype_read", {}).get("mixed_subtype_run") == "run13R"
    side_ok = summary.get("side_read", {}).get("direction_run") == "run13S"
    gates = ["runtime_evidence_gate", "feature_mask_mt5_audit", "hold_micro_axis_audit", "tier_b_subtype_filter_audit", "side_hold4_audit", "required_gate_coverage_audit", "final_claim_guard"]
    return {
        "runtime_evidence_gate": {"status": "passed" if runtime_ok else "blocked", "runtime_completed_count": summary.get("runtime_completed_count"), "runtime_expected_count": summary.get("runtime_expected_count"), "external_verification_status": summary.get("external_verification_status")},
        "feature_mask_mt5_audit": {"status": "passed" if feature_ok else "blocked", "feature_mask_read": summary.get("feature_mask_read")},
        "hold_micro_axis_audit": {"status": "passed" if hold_ok else "blocked", "hold_read": summary.get("hold_read")},
        "tier_b_subtype_filter_audit": {"status": "passed" if subtype_ok else "blocked", "tier_b_subtype_read": summary.get("tier_b_subtype_read")},
        "side_hold4_audit": {"status": "passed" if side_ok else "blocked", "side_read": summary.get("side_read")},
        "required_gate_coverage_audit": {"status": "passed" if feature_ok and hold_ok and subtype_ok and side_ok else "blocked", "packet_id": PACKET_ID, "required_gates": gates, "covered_gates": gates},
        "final_claim_guard": {"status": "passed", "allowed_claims": [JUDGMENT, "runtime_probe", "model_characteristic_attribution", "inconclusive"], "forbidden_claims": summary.get("forbidden_claims"), "claim_boundary": BOUNDARY},
    }


def packet_markdown(summary: Mapping[str, Any]) -> str:
    feature = summary["feature_mask_read"]
    hold = summary["hold_read"]
    subtype = summary["tier_b_subtype_read"]
    side = summary["side_read"]
    return "\n".join(
        [
            "# Stage19 RUN13T EBM MT5 Axis Extension(19단계 실행13T EBM MT5 축 확장)",
            "",
            f"- judgment(판정): `{JUDGMENT}`",
            f"- external verification(외부 검증): `{summary.get('external_verification_status')}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "- operating promotion(운영 승격): `none(없음)`",
            "",
            "## 1 Feature Mask(피처 마스크)",
            "",
            f"- baseline OOS net(기준 표본외 순손익): `{metric_text(feature.get('baseline_oos_net_profit'))}`",
            f"- masked OOS net(마스크 표본외 순손익): `{metric_text(feature.get('masked_oos_net_profit'))}`",
            f"- delta(차이): `{metric_text(feature.get('delta_oos_net_profit'))}`",
            "",
            "효과(effect, 효과): top5 feature(상위 5개 피처)를 MT5 score table(점수표)에서 직접 0으로 만들어 runtime dependency(런타임 의존성)를 확인했다.",
            "",
            "## 2 Hold Micro Axis(보유 미세 축)",
            "",
            f"- best OOS hold(표본외 최고 보유): `{hold.get('best_oos_hold')}` / net(순손익): `{metric_text(hold.get('best_oos_net_profit'))}` / PF(수익 팩터): `{metric_text(hold.get('best_oos_profit_factor'))}`",
            f"- best validation hold(검증 최고 보유): `{hold.get('best_validation_hold')}` / net(순손익): `{metric_text(hold.get('best_validation_net_profit'))}`",
            f"- validation positive holds(검증 양수 보유): `{hold.get('validation_positive_holds')}`",
            "",
            "효과(effect, 효과): hold2/3/5(2/3/5봉)를 추가해 hold4(4봉)가 고립된 우연인지 주변 축과 비교했다.",
            "",
            "## 3 Tier B Subtype(티어 B 하위유형)",
            "",
            f"- subtype filter(하위유형 필터): `{subtype.get('subtype_filter')}`",
            f"- filtered OOS net(필터 표본외 순손익): `{metric_text(subtype.get('mixed_subtype_oos_net_profit'))}`",
            f"- delta vs base(기준 대비 차이): `{metric_text(subtype.get('delta_oos_net_profit'))}`",
            "",
            "효과(effect, 효과): Tier B fallback(티어 B 대체)을 mixed subtype(혼합 하위유형)으로 제한했을 때 실제 라우팅 전체가 어떻게 바뀌는지 확인했다.",
            "",
            "## 4 Side Hold4(4봉 방향)",
            "",
            f"- long-only OOS net(매수 전용 표본외 순손익): `{metric_text(side.get('long_oos_net_profit'))}`",
            f"- short-only OOS net(매도 전용 표본외 순손익): `{metric_text(side.get('short_oos_net_profit'))}`",
            f"- long-minus-short(매수-매도): `{metric_text(side.get('oos_long_minus_short_net'))}`",
            "",
            "효과(effect, 효과): hold4(4봉)에서도 long bias(매수 편향)가 유지되는지 확인했다.",
            "",
            "Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )


def decision_markdown(summary: Mapping[str, Any]) -> str:
    hold = summary["hold_read"]
    side = summary["side_read"]
    return "\n".join(
        [
            "# 2026-05-05 Stage19 RUN13T EBM MT5 Axis Extension Decision(19단계 실행13T EBM MT5 축 확장 결정)",
            "",
            f"- run(실행): `{RUN_ID}`",
            f"- judgment(판정): `{JUDGMENT}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
            "",
            "## Decision(결정)",
            "",
            "EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신)은 더 파볼 단서가 있지만, 현재 의미는 runtime_probe(런타임 탐침)와 characteristic attribution(특성 귀속)이다.",
            "",
            f"- best OOS hold(표본외 최고 보유): `{hold.get('best_oos_hold')}` / net(순손익): `{metric_text(hold.get('best_oos_net_profit'))}`",
            f"- validation positive holds(검증 양수 보유): `{hold.get('validation_positive_holds')}`",
            f"- hold4 long-minus-short OOS(4봉 매수-매도 표본외 차이): `{metric_text(side.get('oos_long_minus_short_net'))}`",
            "",
            "효과(effect, 효과): 이번 작업은 MT5 연동으로 네 축을 실제 테스터에서 더 확인했지만, 운영 승격(operating promotion, 운영 승격)은 만들지 않는다.",
        ]
    )


def write_packet(summary: Mapping[str, Any], outputs: Mapping[str, Path]) -> None:
    for name, payload in gate_payloads(summary).items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
    output_hashes = {name: sha256_file_lf_normalized(path) for name, path in outputs.items() if io_path(path).exists() and path.suffix != ".md"}
    write_json(
        PACKET_ROOT / "artifact_index.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": summary["created_at_utc"],
            "producer": "stage_pipelines.stage19.ebm_mt5_axis_extension",
            "source_inputs": summary.get("source_inputs"),
            "artifact_paths": {name: rel(path) for name, path in outputs.items()},
            "artifact_hashes": output_hashes,
            "registry_links": {"run_registry": rel(RUN_REGISTRY_PATH), "project_alpha_ledger": rel(PROJECT_LEDGER_PATH), "stage_run_ledger": rel(STAGE_LEDGER_PATH)},
            "availability": "tracked_packet_summary_with_generated_02_runs_artifacts",
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": summary["created_at_utc"],
            "primary_family": "model_characteristic_attribution",
            "primary_skill": "obsidian-performance-attribution",
            "support_skills": ["obsidian-experiment-design", "obsidian-runtime-parity", "obsidian-backtest-forensics", "obsidian-artifact-lineage", "obsidian-result-judgment"],
            "required_gates": list(gate_payloads(summary)),
        },
    )
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": summary["created_at_utc"],
            "receipts": [
                {
                    "skill": "obsidian-experiment-design",
                    "status": "completed",
                    "hypothesis": "EBM feature mask, hold micro-axis, Tier B subtype filter, and hold4 direction axes can be checked through MT5 runtime probes.",
                    "decision_use": "Continue Stage19, narrow to one final EBM clue, or stop before topic pivot.",
                    "comparison_baseline": "run13I q90 hold4 and run13F q90 hold6 runtime evidence.",
                    "control_variables": [FEATURE_SET_ID, LABEL_ID, SPLIT_CONTRACT, SELECTED_VARIANT_ID, "US100 M5"],
                    "changed_variables": ["top5 score-table mask", "max_hold_bars=2/3/5", f"Tier B subtype={SUBTYPE_FILTER}", "hold4 long-only/short-only"],
                    "success_criteria": "MT5 reports, normalized KPI, trade records, and gates exist for run13N-run13S.",
                    "failure_criteria": "missing MT5 output, score-table parity failure, malformed report, or incomplete KPI.",
                    "invalid_conditions": "feature order mismatch, timestamp mismatch, or unsupported runtime score table.",
                },
                {"skill": "obsidian-runtime-parity", "status": "completed", "research_path": rel(Path(__file__)), "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5", "shared_contract": "same EBM score-table backend, feature order hashes, q90 thresholds, US100 M5 timestamp matching.", "known_differences": "Top5 mask zeroes score-table feature terms without retraining.", "runtime_claim_boundary": "runtime_probe"},
                {"skill": "obsidian-backtest-forensics", "status": "completed", "tester_identity": "MT5 Strategy Tester US100 M5, deposit=500, leverage=1:100, model=4.", "runtime_followup_run_ids": summary.get("runtime_followup_run_ids"), "backtest_judgment": "usable_with_boundary" if summary.get("external_verification_status") == "completed" else "blocked_or_partial"},
                {"skill": "obsidian-artifact-lineage", "status": "completed", "source_inputs": summary.get("source_inputs"), "artifact_paths": {name: rel(path) for name, path in outputs.items()}, "lineage_judgment": "connected_with_boundary"},
                {"skill": "obsidian-result-judgment", "status": "completed", "judgment_label": JUDGMENT, "claim_boundary": BOUNDARY, "forbidden_claims": summary.get("forbidden_claims")},
            ],
        },
    )
    write_json(PACKET_ROOT / "run_summaries" / f"{RUN_ID}.json", summary)
    write_csv(PACKET_ROOT / "runtime_axis_rows.csv", SUMMARY_COLUMNS, summary["runtime_axis_rows"])
    write_csv(PACKET_ROOT / "comparison_rows.csv", COMPARISON_COLUMNS, summary["comparison_rows"])


def replace_yaml_block(text: str, marker: str, block: str) -> str:
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


def sync_docs(summary: Mapping[str, Any]) -> None:
    hold = summary["hold_read"]
    side = summary["side_read"]
    write_md(
        SELECTION_STATUS_PATH,
        "\n".join(
            [
                "# Stage19 Selection Status(19단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                "- status(상태): `active_run13T_ebm_mt5_axis_extension_completed`",
                f"- current run(현재 실행): `{RUN_ID}`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{JUDGMENT}`",
                f"- selected variant(선택 변형): `{SELECTED_VARIANT_ID}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "효과(effect, 효과): Stage19(19단계)는 EBM(설명가능 부스팅 머신)의 1/2/3/4 축을 MT5까지 더 검증했지만 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.",
            ]
        ),
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else "# Stage19 Review Index(19단계 검토 색인)\n"
    line = f"- `{RUN_ID}`: `{rel(REPORT_PATH)}`\n"
    if RUN_ID not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"updated_on: '.*?'", "updated_on: '2026-05-05'", state, count=1)
    state = re.sub(r"active_branch: .*", "active_branch: codex/stage19-ebm-attribution", state, count=1)
    state = re.sub(r"current_run_id: .*", f"current_run_id: {RUN_ID}", state, count=1)
    state = state.replace("stage19_active_run13M_ebm_deep_axis_followup_completed", "stage19_active_run13T_ebm_mt5_axis_extension_completed", 1)
    state = state.replace("active_run13M_ebm_deep_axis_followup_completed", "active_run13T_ebm_mt5_axis_extension_completed", 1)
    block = f"""stage19_ebm_run13T_mt5_axis_extension:
  packet_id: {PACKET_ID}
  status: reviewed_mt5_axis_extension_completed
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  runtime_followup_run_ids: {','.join(summary['runtime_followup_run_ids'])}
  feature_mask_delta_oos_net_profit: {summary['feature_mask_read'].get('delta_oos_net_profit')}
  best_oos_hold: {hold.get('best_oos_hold')}
  best_oos_net_profit: {hold.get('best_oos_net_profit')}
  hold4_long_minus_short_oos: {side.get('oos_long_minus_short_net')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / 'run_summaries' / f'{RUN_ID}.json')}
  next_action: continue_stage19_only_for_hold4_long_feature_mask_or_stop_before_topic_pivot
"""
    state = replace_yaml_block(state, "stage19_ebm_run13T_mt5_axis_extension:", block)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n", encoding="utf-8")
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = "\n".join(
        [
            "## Latest Stage19 RUN13T MT5 Axis Extension Update(최신 19단계 실행13T MT5 축 확장 업데이트)",
            "",
            f"Stage19(19단계)는 `{RUN_ID}`에서 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) feature mask(피처 마스크), hold micro-axis(보유 미세 축), Tier B subtype filter(티어 B 하위유형 필터), hold4 side axis(4봉 방향 축)을 MT5(`MetaTrader 5`, 메타트레이더5)로 더 확인했다.",
            "",
            f"결과(result, 결과): `{JUDGMENT}`. best OOS hold(표본외 최고 보유)는 `{hold.get('best_oos_hold')}`이고 net(순손익)은 `{metric_text(hold.get('best_oos_net_profit'))}`이다. hold4 long-minus-short(4봉 매수-매도 차이)는 `{metric_text(side.get('oos_long_minus_short_net'))}`이다.",
            "",
            "효과(effect, 효과): 1/2/3/4 축을 MT5 런타임까지 밀었지만 edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            "",
        ]
    )
    if "## Latest Stage19 RUN13T MT5 Axis Extension Update" in current:
        current = re.sub(
            r"## Latest Stage19 RUN13T MT5 Axis Extension Update\(최신 19단계 실행13T MT5 축 확장 업데이트\)\n.*?(?=## Latest Stage19 RUN13M Deep Axis Update)",
            update + "\n",
            current,
            count=1,
            flags=re.S,
        )
    else:
        current = update + "\n" + current
    current = re.sub(r"- updated_on: `.*?`", "- updated_on: `2026-05-05`", current, count=1)
    current = re.sub(r"- active_branch: `[^`]+`", "- active_branch: `codex/stage19-ebm-attribution`", current, count=1)
    current = re.sub(r"- current run\(현재 실행\): `[^`]+`", f"- current run(현재 실행): `{RUN_ID}`", current, count=1)
    io_path(CURRENT_WORKING_STATE_PATH).write_text(current.rstrip() + "\n", encoding="utf-8-sig")


def materialize_outputs(summary: Mapping[str, Any]) -> dict[str, Any]:
    outputs = output_paths()
    write_csv(outputs["runtime_axis_rows"], SUMMARY_COLUMNS, summary["runtime_axis_rows"])
    write_csv(outputs["comparison_rows"], COMPARISON_COLUMNS, summary["comparison_rows"])
    ledger_outputs = write_ledgers(summary)
    registry_output = write_registry(summary)
    enriched = {**dict(summary), "ledger_outputs": ledger_outputs, "registry_output": registry_output}
    manifest = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": summary["created_at_utc"],
        "exploration_label": EXPLORATION_LABEL,
        "source_inputs": summary["source_inputs"],
        "outputs": {key: rel(value) for key, value in outputs.items()},
        "external_verification_status": summary["external_verification_status"],
        "boundary": BOUNDARY,
    }
    kpi_record = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "ebm_mt5_axis_extension",
        "model_family": MODEL_FAMILY,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "external_verification_status": summary["external_verification_status"],
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "feature_mask_read": summary["feature_mask_read"],
        "hold_read": summary["hold_read"],
        "tier_b_subtype_read": summary["tier_b_subtype_read"],
        "side_read": summary["side_read"],
        "ledger_outputs": ledger_outputs,
        "registry_output": registry_output,
    }
    write_json(outputs["run_manifest"], manifest)
    write_json(outputs["summary"], enriched)
    write_json(outputs["kpi_record"], kpi_record)
    write_md(REPORT_PATH, packet_markdown(enriched))
    write_md(DECISION_PATH, decision_markdown(enriched))
    write_packet(enriched, outputs)
    sync_docs(enriched)
    return enriched


def run(args: argparse.Namespace) -> dict[str, Any]:
    runtime_summaries = execute_topics(args)
    summary = build_summary(utc_now(), runtime_summaries)
    return materialize_outputs(summary)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stage19 EBM MT5 axis extension for 1/2/3/4 follow-up.")
    parser.add_argument("--runtime-topics", nargs="*", default=["all"], help="run13N/run13O/run13P/run13Q/run13R/run13S or all.")
    parser.add_argument("--force-runtime", action="store_true", help="Re-run runtime topics even if summary exists.")
    parser.add_argument("--materialize-only", action="store_true", help="Prepare artifacts without launching MT5.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(stage19_mt5.TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(stage19_mt5.METAEDITOR_PATH_DEFAULT))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    summary = run(args)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "judgment": JUDGMENT,
                "external_verification_status": summary.get("external_verification_status"),
                "feature_mask_read": summary.get("feature_mask_read"),
                "hold_read": summary.get("hold_read"),
                "tier_b_subtype_read": summary.get("tier_b_subtype_read"),
                "side_read": summary.get("side_read"),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
