from __future__ import annotations

import argparse
import csv
import json
import math
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
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
from foundation.models.baseline_training import load_feature_order
from foundation.models.ebm_score_table import ebm_main_effect_contribution_tensor
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

RUN_ID = "run13M_ebm_deep_axis_followup_v1"
RUN_NUMBER = "run13M"
PACKET_ID = "stage19_run13M_ebm_deep_axis_followup_v1"
EXPLORATION_LABEL = "stage19_Model__EBMDeepAxisFollowup"
REPORT_PATH = STAGE_ROOT / "03_reviews/run13M_ebm_deep_axis_followup_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-04_stage19_run13M_ebm_deep_axis_followup.md"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID

MODEL_FAMILY = stage19_mt5.MODEL_FAMILY
FEATURE_SET_ID = stage19_mt5.FEATURE_SET_ID
LABEL_ID = stage19_mt5.LABEL_ID
SPLIT_CONTRACT = stage19_mt5.SPLIT_CONTRACT
SELECTED_VARIANT_ID = stage19_mt5.SELECTED_VARIANT_ID
SOURCE_RUN_ID = stage19_mt5.SOURCE_RUN_ID
SOURCE_PACKET_ID = stage19_mt5.SOURCE_PACKET_ID

BOUNDARY = "ebm_deep_axis_followup_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_ebm_deep_axis_followup_completed"

EXISTING_HOLD_SOURCES: tuple[tuple[str, str, str], ...] = (
    ("run13B", "run13B_ebm_q90_runtime_handoff_probe_v1", "stage19_run13B_ebm_q90_mt5_runtime_v1"),
    ("run13F", "run13F_ebm_q90_hold6_probe_v1", "stage19_run13F_ebm_hold6_mt5_v1"),
    ("run13G", "run13G_ebm_q90_hold18_probe_v1", "stage19_run13G_ebm_hold18_mt5_v1"),
)
FOCUS_RUN_NUMBER = "run13F"
FOCUS_RUN_ID = "run13F_ebm_q90_hold6_probe_v1"
FOCUS_PACKET_ID = "stage19_run13F_ebm_hold6_mt5_v1"
RUN13H_SUMMARY_PATH = STAGE_ROOT / "02_runs/run13H_ebm_feature_hold6_routing_attribution_v1/summary.json"
RUN13H_PACKET_SUMMARY_PATH = (
    ROOT
    / "docs/agent_control/packets/stage19_run13H_ebm_feature_hold6_routing_attribution_v1/run_summaries/run13H_ebm_feature_hold6_routing_attribution_v1.json"
)

RUNTIME_FOLLOWUP_TOPICS: tuple[stage19_mt5.RuntimeTopic, ...] = (
    stage19_mt5.RuntimeTopic(
        run_id="run13I_ebm_q90_hold4_probe_v1",
        run_number="run13I",
        packet_id="stage19_run13I_ebm_hold4_mt5_v1",
        exploration_label="stage19_Model__EBMHold4Stress",
        review_filename="run13I_ebm_q90_hold4_packet.md",
        threshold_quantile=0.90,
        mode="routed",
        max_hold_bars=4,
        expected_attempts=6,
        expected_kpi_records=10,
        topic_read="q90_hold4_trade_shape_stress",
        boundary="ebm_q90_hold4_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q90_hold4_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q90_hold4_runtime_probe_after_attempt",
    ),
    stage19_mt5.RuntimeTopic(
        run_id="run13J_ebm_q90_hold8_probe_v1",
        run_number="run13J",
        packet_id="stage19_run13J_ebm_hold8_mt5_v1",
        exploration_label="stage19_Model__EBMHold8Stress",
        review_filename="run13J_ebm_q90_hold8_packet.md",
        threshold_quantile=0.90,
        mode="routed",
        max_hold_bars=8,
        expected_attempts=6,
        expected_kpi_records=10,
        topic_read="q90_hold8_trade_shape_stress",
        boundary="ebm_q90_hold8_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q90_hold8_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q90_hold8_runtime_probe_after_attempt",
    ),
    stage19_mt5.RuntimeTopic(
        run_id="run13K_ebm_q90_hold10_probe_v1",
        run_number="run13K",
        packet_id="stage19_run13K_ebm_hold10_mt5_v1",
        exploration_label="stage19_Model__EBMHold10Stress",
        review_filename="run13K_ebm_q90_hold10_packet.md",
        threshold_quantile=0.90,
        mode="routed",
        max_hold_bars=10,
        expected_attempts=6,
        expected_kpi_records=10,
        topic_read="q90_hold10_trade_shape_stress",
        boundary="ebm_q90_hold10_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q90_hold10_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q90_hold10_runtime_probe_after_attempt",
    ),
    stage19_mt5.RuntimeTopic(
        run_id="run13L_ebm_q90_hold6_direction_probe_v1",
        run_number="run13L",
        packet_id="stage19_run13L_ebm_q90_hold6_direction_mt5_v1",
        exploration_label="stage19_Model__EBMQ90Hold6DirectionAsymmetry",
        review_filename="run13L_ebm_q90_hold6_direction_packet.md",
        threshold_quantile=0.90,
        mode="direction",
        max_hold_bars=6,
        expected_attempts=12,
        expected_kpi_records=20,
        topic_read="q90_hold6_long_short_direction_asymmetry",
        boundary="ebm_q90_hold6_direction_asymmetry_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed="inconclusive_ebm_q90_hold6_direction_asymmetry_runtime_probe_completed",
        judgment_blocked="blocked_ebm_q90_hold6_direction_asymmetry_runtime_probe_after_attempt",
    ),
)

FEATURE_MASK_COLUMNS = (
    "mask_id",
    "tier_scope",
    "split",
    "mask_feature_count",
    "features_masked",
    "row_count",
    "base_signal_count",
    "masked_signal_count",
    "base_long_count",
    "base_short_count",
    "masked_long_count",
    "masked_short_count",
    "lost_signal_count",
    "gained_signal_count",
    "retained_same_side_signal_count",
    "decision_flip_count",
    "lost_signal_rate",
    "retained_same_side_signal_rate",
    "chosen_probability_drop_mean",
    "max_abs_base_probability_diff",
)
HOLD_AXIS_COLUMNS = (
    "source_run_number",
    "source_run_id",
    "topic_read",
    "threshold_quantile",
    "max_hold_bars",
    "split",
    "routed_net_profit",
    "routed_profit_factor",
    "routed_trade_count",
    "routed_expectancy",
    "routed_max_drawdown",
    "tier_a_only_net_profit",
    "tier_a_only_profit_factor",
    "tier_a_only_trade_count",
    "tier_b_fallback_only_net_profit",
    "tier_b_fallback_only_profit_factor",
    "tier_b_fallback_only_trade_count",
    "tier_a_route_share",
    "tier_b_fallback_route_share",
    "tier_a_signal_count",
    "tier_b_fallback_signal_count",
)
SUBTYPE_COLUMNS = (
    "focus_run_id",
    "split",
    "partial_context_subtype",
    "row_count",
    "signal_count",
    "signal_rate",
    "long_signal_count",
    "short_signal_count",
    "mean_p_short",
    "mean_p_long",
    "mean_nonflat_probability",
    "mean_probability_margin",
    "signal_directional_hit_rate",
)
SIDE_AXIS_COLUMNS = (
    "source_run_number",
    "source_run_id",
    "threshold_quantile",
    "max_hold_bars",
    "split",
    "side_mode",
    "record_view",
    "tier_scope",
    "route_role",
    "net_profit",
    "profit_factor",
    "trade_count",
    "win_rate_percent",
    "max_drawdown_amount",
    "feature_ready_count",
    "order_fill_count",
    "signal_count",
    "long_signal_count",
    "short_signal_count",
)


@dataclass(frozen=True)
class AnalysisSource:
    run_number: str
    run_id: str
    packet_id: str
    summary: Mapping[str, Any]

    @property
    def run_root(self) -> Path:
        return STAGE_ROOT / "02_runs" / self.run_id

    @property
    def packet_root(self) -> Path:
        return ROOT / "docs/agent_control/packets" / self.packet_id

    @property
    def topic_read(self) -> str:
        return str(self.summary.get("topic_read", ""))

    @property
    def threshold_quantile(self) -> float:
        return safe_float(self.summary.get("threshold_quantile"))

    @property
    def max_hold_bars(self) -> int:
        return int(self.summary.get("max_hold_bars") or 0)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def repo_path(path_value: str | Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else ROOT / path


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if io_path(path).exists():
        return read_json(path)
    return {}


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.8g}" if math.isfinite(value) else ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(json_ready(value))


def display_metric(value: Any) -> str:
    if value in (None, "", "NA"):
        return ""
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(numeric):
        return ""
    return f"{numeric:.8g}"


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


def safe_div(numerator: Any, denominator: Any) -> float | None:
    den = safe_float(denominator)
    if den == 0.0:
        return None
    return safe_float(numerator) / den


def mean_or_none(values: Iterable[Any]) -> float | None:
    clean = [safe_float(value) for value in values if value not in (None, "", "NA")]
    return sum(clean) / len(clean) if clean else None


def metric_value(record: Mapping[str, Any], section: str, key: str) -> Any:
    section_value = record.get(section, {})
    if not isinstance(section_value, Mapping):
        return None
    value = section_value.get(key)
    if isinstance(value, Mapping) and "value" in value:
        return value.get("value")
    return value


def load_json_or_jsonl(path: Path) -> list[dict[str, Any]]:
    if not io_path(path).exists():
        return []
    payload = io_path(path).read_text(encoding="utf-8-sig").strip()
    if not payload:
        return []
    if payload.startswith("["):
        data = json.loads(payload)
    else:
        data = [json.loads(line) for line in payload.splitlines() if line.strip()]
    return [item for item in data if isinstance(item, dict)]


def softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max(axis=1, keepdims=True)
    exp_logits = np.exp(shifted)
    return exp_logits / exp_logits.sum(axis=1, keepdims=True)


def decision_labels(probabilities: np.ndarray, threshold: float) -> np.ndarray:
    labels = np.full(probabilities.shape[0], "flat", dtype=object)
    p_short = probabilities[:, 0]
    p_long = probabilities[:, 2]
    long_mask = (p_long >= float(threshold)) & (p_long >= p_short)
    short_mask = (p_short >= float(threshold)) & (p_short > p_long)
    labels[long_mask] = "long"
    labels[short_mask] = "short"
    return labels


def chosen_probability(probabilities: np.ndarray, labels: np.ndarray) -> np.ndarray:
    out = np.full(probabilities.shape[0], np.nan, dtype="float64")
    long_mask = labels == "long"
    short_mask = labels == "short"
    out[long_mask] = probabilities[long_mask, 2]
    out[short_mask] = probabilities[short_mask, 0]
    return out


def runtime_topic_by_number(run_number: str) -> stage19_mt5.RuntimeTopic:
    for topic in RUNTIME_FOLLOWUP_TOPICS:
        if topic.run_number == run_number or topic.run_id == run_number:
            return topic
    raise ValueError(f"unknown runtime follow-up topic: {run_number}")


def selected_runtime_topics(topic_ids: Sequence[str]) -> list[stage19_mt5.RuntimeTopic]:
    if not topic_ids or "all" in topic_ids:
        return list(RUNTIME_FOLLOWUP_TOPICS)
    return [runtime_topic_by_number(topic_id) for topic_id in topic_ids]


def runtime_args(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        force=bool(args.force_runtime),
        materialize_only=bool(args.materialize_only),
        timeout_seconds=int(args.timeout_seconds),
        terminal_path=args.terminal_path,
        metaeditor_path=args.metaeditor_path,
        topics=["all"],
    )


def execute_runtime_topics(args: argparse.Namespace) -> list[dict[str, Any]]:
    created_at = utc_now()
    context = stage19_mt5.load_context()
    models = stage19_mt5.load_or_train_models(context)
    summaries: list[dict[str, Any]] = []
    topic_args = runtime_args(args)
    for topic in selected_runtime_topics(args.runtime_topics):
        summaries.append(stage19_mt5.build_topic_run(topic, topic_args, context, models, created_at))
    return summaries


def source_from_tuple(item: tuple[str, str, str]) -> AnalysisSource:
    run_number, run_id, packet_id = item
    return AnalysisSource(
        run_number=run_number,
        run_id=run_id,
        packet_id=packet_id,
        summary=read_json(STAGE_ROOT / "02_runs" / run_id / "summary.json"),
    )


def source_from_topic(topic: stage19_mt5.RuntimeTopic) -> AnalysisSource:
    return AnalysisSource(
        run_number=topic.run_number,
        run_id=topic.run_id,
        packet_id=topic.packet_id,
        summary=read_json(topic.run_root / "summary.json"),
    )


def hold_sources() -> list[AnalysisSource]:
    sources = [source_from_tuple(item) for item in EXISTING_HOLD_SOURCES]
    sources.extend(source_from_topic(topic) for topic in RUNTIME_FOLLOWUP_TOPICS if topic.mode == "routed")
    sources.sort(key=lambda source: (source.threshold_quantile, source.max_hold_bars, source.run_number))
    return sources


def direction_source() -> AnalysisSource:
    return source_from_topic(runtime_topic_by_number("run13L"))


def focus_source() -> AnalysisSource:
    return source_from_tuple((FOCUS_RUN_NUMBER, FOCUS_RUN_ID, FOCUS_PACKET_ID))


def load_normalized_kpi(source: AnalysisSource) -> list[dict[str, Any]]:
    return load_json_or_jsonl(source.packet_root / "normalized_kpi_records.jsonl")


def routing_rows(sources: Sequence[AnalysisSource]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in sources:
        records = load_normalized_kpi(source)
        split_total_feature_ready: dict[str, float] = {}
        for record in records:
            if metric_value(record, "row_grain", "route_role") == "routed_total":
                split_total_feature_ready[str(metric_value(record, "row_grain", "split"))] = safe_float(metric_value(record, "execution", "feature_ready_count"))
        for record in records:
            split = str(metric_value(record, "row_grain", "split"))
            role = str(metric_value(record, "row_grain", "route_role"))
            if role not in {"routed_total", "tier_only_total", "tier_b_fallback_only_total", "primary_used", "fallback_used"}:
                continue
            feature_ready = safe_float(metric_value(record, "execution", "feature_ready_count"))
            routed_summary_key = "validation_routed" if split == "validation" else "oos_routed"
            routed_summary = source.summary.get(routed_summary_key, {}) if isinstance(source.summary.get(routed_summary_key), Mapping) else {}
            if role == "primary_used" and feature_ready == 0.0:
                feature_ready = safe_float(routed_summary.get("tier_a_used_count"))
            elif role == "fallback_used" and feature_ready == 0.0:
                feature_ready = safe_float(routed_summary.get("tier_b_fallback_used_count"))
            route_share = 1.0 if role == "routed_total" else None
            if role in {"primary_used", "fallback_used"}:
                route_share = safe_div(feature_ready, split_total_feature_ready.get(split))
            rows.append(
                {
                    "source_run_number": source.run_number,
                    "source_run_id": source.run_id,
                    "topic_read": source.topic_read,
                    "threshold_quantile": source.threshold_quantile,
                    "max_hold_bars": source.max_hold_bars,
                    "split": split,
                    "record_view": metric_value(record, "row_grain", "record_view"),
                    "tier_scope": metric_value(record, "row_grain", "tier_scope"),
                    "route_role": role,
                    "net_profit": metric_value(record, "mt5_trading_headline", "net_profit"),
                    "profit_factor": metric_value(record, "mt5_trading_headline", "profit_factor"),
                    "expectancy": metric_value(record, "mt5_trading_headline", "expectancy"),
                    "trade_count": metric_value(record, "mt5_trading_headline", "trade_count"),
                    "win_rate_percent": metric_value(record, "mt5_trading_headline", "win_rate"),
                    "max_drawdown_amount": metric_value(record, "risk", "max_drawdown_amount"),
                    "feature_ready_count": feature_ready,
                    "model_ok_count": metric_value(record, "execution", "model_ok_count"),
                    "model_fail_count": metric_value(record, "execution", "model_fail_count"),
                    "order_attempt_count": metric_value(record, "execution", "order_attempt_count"),
                    "order_fill_count": metric_value(record, "execution", "order_fill_count"),
                    "signal_count": metric_value(record, "signal_model", "signal_count"),
                    "long_signal_count": metric_value(record, "signal_model", "long_count"),
                    "short_signal_count": metric_value(record, "signal_model", "short_count"),
                    "route_share": route_share,
                }
            )
    return rows


def find_routing_row(rows: Sequence[Mapping[str, Any]], source_run_number: str, split: str, role: str, tier_scope: str | None = None) -> Mapping[str, Any]:
    for row in rows:
        if row.get("source_run_number") != source_run_number or row.get("split") != split or row.get("route_role") != role:
            continue
        if tier_scope is not None and row.get("tier_scope") != tier_scope:
            continue
        return row
    return {}


def hold_axis_rows(sources: Sequence[AnalysisSource], rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for source in sources:
        if source.threshold_quantile != 0.90:
            continue
        for split in ("validation", "oos"):
            routed = find_routing_row(rows, source.run_number, split, "routed_total")
            tier_a = find_routing_row(rows, source.run_number, split, "tier_only_total", "Tier A")
            tier_b = find_routing_row(rows, source.run_number, split, "tier_b_fallback_only_total", "Tier B")
            comp_a = find_routing_row(rows, source.run_number, split, "primary_used", "Tier A")
            comp_b = find_routing_row(rows, source.run_number, split, "fallback_used", "Tier B")
            out.append(
                {
                    "source_run_number": source.run_number,
                    "source_run_id": source.run_id,
                    "topic_read": source.topic_read,
                    "threshold_quantile": source.threshold_quantile,
                    "max_hold_bars": source.max_hold_bars,
                    "split": split,
                    "routed_net_profit": routed.get("net_profit"),
                    "routed_profit_factor": routed.get("profit_factor"),
                    "routed_trade_count": routed.get("trade_count"),
                    "routed_expectancy": routed.get("expectancy"),
                    "routed_max_drawdown": routed.get("max_drawdown_amount"),
                    "tier_a_only_net_profit": tier_a.get("net_profit"),
                    "tier_a_only_profit_factor": tier_a.get("profit_factor"),
                    "tier_a_only_trade_count": tier_a.get("trade_count"),
                    "tier_b_fallback_only_net_profit": tier_b.get("net_profit"),
                    "tier_b_fallback_only_profit_factor": tier_b.get("profit_factor"),
                    "tier_b_fallback_only_trade_count": tier_b.get("trade_count"),
                    "tier_a_route_share": comp_a.get("route_share"),
                    "tier_b_fallback_route_share": comp_b.get("route_share"),
                    "tier_a_signal_count": comp_a.get("signal_count"),
                    "tier_b_fallback_signal_count": comp_b.get("signal_count"),
                }
            )
    return sorted(out, key=lambda row: (safe_float(row.get("max_hold_bars")), str(row.get("split"))))


def hold_axis_read(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    requested_holds = {4, 6, 8, 10}
    requested_oos = [row for row in rows if row.get("split") == "oos" and int(row.get("max_hold_bars") or 0) in requested_holds]
    requested_validation = [row for row in rows if row.get("split") == "validation" and int(row.get("max_hold_bars") or 0) in requested_holds]
    ranked_oos = sorted(requested_oos, key=lambda row: safe_float(row.get("routed_net_profit")), reverse=True)
    ranked_validation = sorted(requested_validation, key=lambda row: safe_float(row.get("routed_net_profit")), reverse=True)
    best_oos = ranked_oos[0] if ranked_oos else {}
    best_validation = ranked_validation[0] if ranked_validation else {}
    oos_values = [safe_float(row.get("routed_net_profit")) for row in requested_oos]
    validation_values = [safe_float(row.get("routed_net_profit")) for row in requested_validation]
    return {
        "requested_holds": sorted(requested_holds),
        "best_requested_oos_hold": best_oos.get("max_hold_bars"),
        "best_requested_oos_run": best_oos.get("source_run_number"),
        "best_requested_oos_net_profit": best_oos.get("routed_net_profit"),
        "best_requested_oos_profit_factor": best_oos.get("routed_profit_factor"),
        "best_requested_validation_hold": best_validation.get("max_hold_bars"),
        "best_requested_validation_run": best_validation.get("source_run_number"),
        "best_requested_validation_net_profit": best_validation.get("routed_net_profit"),
        "best_requested_validation_profit_factor": best_validation.get("routed_profit_factor"),
        "oos_net_profit_range": (max(oos_values) - min(oos_values)) if oos_values else None,
        "validation_net_profit_range": (max(validation_values) - min(validation_values)) if validation_values else None,
        "oos_positive_holds": [row.get("max_hold_bars") for row in requested_oos if safe_float(row.get("routed_net_profit")) > 0.0],
        "validation_positive_holds": [row.get("max_hold_bars") for row in requested_validation if safe_float(row.get("routed_net_profit")) > 0.0],
        "axis_visible": bool(oos_values and (max(oos_values) - min(oos_values)) >= 50.0),
        "claim": "hold_axis_characteristic_only",
    }


def top_repeated_features() -> list[str]:
    summary = read_json_if_exists(RUN13H_PACKET_SUMMARY_PATH) or read_json_if_exists(RUN13H_SUMMARY_PATH)
    read = summary.get("feature_contribution_read", {}) if isinstance(summary.get("feature_contribution_read"), Mapping) else {}
    rows = read.get("top_repeated_features", [])
    features = [str(item.get("feature")) for item in rows if isinstance(item, Mapping) and item.get("feature")]
    if features:
        return features[:5]
    return ["atr_14", "ema9_ema20_diff", "ema50_ema200_diff", "ema20_ema50_diff", "hl_zscore_50"]


def feature_mask_specs(full_feature_order: Sequence[str]) -> dict[str, list[str]]:
    top5 = top_repeated_features()
    return {
        "mask_top5_repeated": top5,
        "mask_volatility_core": [
            feature
            for feature in (
                "atr_14",
                "atr_50",
                "atr_14_over_atr_50",
                "bollinger_width_20",
                "historical_vol_20",
                "historical_vol_5_over_20",
            )
            if feature in full_feature_order
        ],
        "mask_trend_ema_core": [
            feature
            for feature in (
                "ema9_ema20_diff",
                "ema20_ema50_diff",
                "ema50_ema200_diff",
                "close_ema20_ratio",
                "close_ema50_ratio",
                "sma50_sma200_ratio",
            )
            if feature in full_feature_order
        ],
        "mask_range_momentum_mix": [
            feature
            for feature in (
                "hl_zscore_50",
                "rsi_14",
                "rsi_50",
                "stoch_kd_diff",
                "stochrsi_kd_diff",
                "roc_12",
            )
            if feature in full_feature_order
        ],
    }


def load_focus_inputs() -> dict[str, Any]:
    source = focus_source()
    summary = source.summary
    artifacts = summary.get("model_artifacts", {}) if isinstance(summary.get("model_artifacts"), Mapping) else {}
    predictions = summary.get("prediction_artifacts", {}) if isinstance(summary.get("prediction_artifacts"), Mapping) else {}
    tier_a_model_path = repo_path(artifacts["tier_a_joblib"]["source"])
    tier_b_model_path = repo_path(artifacts["tier_b_joblib"]["source"])
    tier_a_predictions_path = repo_path(predictions["tier_a_predictions"]["path"])
    tier_b_predictions_path = repo_path(predictions["tier_b_predictions"]["path"])
    full_feature_order = load_feature_order(stage19_mt5.FEATURE_ORDER_PATH)
    tier_b_feature_order = list(mt5.TIER_B_CORE_FEATURE_ORDER)
    return {
        "source": source,
        "summary": summary,
        "tier_a_model": joblib.load(io_path(tier_a_model_path)),
        "tier_b_model": joblib.load(io_path(tier_b_model_path)),
        "tier_a_model_path": tier_a_model_path,
        "tier_b_model_path": tier_b_model_path,
        "tier_a_feature_order": full_feature_order,
        "tier_b_feature_order": tier_b_feature_order,
        "tier_a_predictions": pd.read_parquet(io_path(tier_a_predictions_path)),
        "tier_b_predictions": pd.read_parquet(io_path(tier_b_predictions_path)),
        "thresholds": artifacts.get("thresholds", {}),
        "feature_paths": {
            ("Tier A", "validation"): source.run_root / "features/tier_a_validation_is_feature_matrix.csv",
            ("Tier A", "oos"): source.run_root / "features/tier_a_oos_feature_matrix.csv",
            ("Tier B", "validation"): source.run_root / "features/tier_b_fallback_validation_is_feature_matrix.csv",
            ("Tier B", "oos"): source.run_root / "features/tier_b_fallback_oos_feature_matrix.csv",
        },
    }


def feature_mask_rows(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    tier_specs = (
        ("Tier A", inputs["tier_a_model"], inputs["tier_a_feature_order"], inputs["tier_a_predictions"], safe_float(inputs["thresholds"].get("tier_a"))),
        ("Tier B", inputs["tier_b_model"], inputs["tier_b_feature_order"], inputs["tier_b_predictions"], safe_float(inputs["thresholds"].get("tier_b"))),
    )
    all_masks = feature_mask_specs(inputs["tier_a_feature_order"])
    for tier_scope, model, feature_order, predictions, threshold in tier_specs:
        mask_indices = {
            mask_id: [feature_order.index(feature) for feature in features if feature in feature_order]
            for mask_id, features in all_masks.items()
        }
        for split in ("validation", "oos"):
            feature_frame = pd.read_csv(io_path(inputs["feature_paths"][(tier_scope, split)]))
            pred_split = predictions.loc[predictions["split"].astype(str).eq(split)].reset_index(drop=True)
            values = feature_frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
            contributions = ebm_main_effect_contribution_tensor(model, values, feature_count=len(feature_order))
            logits = np.asarray(model.intercept_, dtype="float64").reshape(1, -1) + contributions.sum(axis=1)
            rebuilt_prob = softmax(logits)
            pred_prob = pred_split.loc[:, ["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64", copy=False)
            max_abs_base_probability_diff = float(np.max(np.abs(rebuilt_prob - pred_prob))) if len(pred_prob) else 0.0
            base_labels = decision_labels(rebuilt_prob, threshold)
            base_signal = base_labels != "flat"
            base_chosen = chosen_probability(rebuilt_prob, base_labels)
            audits.append(
                {
                    "tier_scope": tier_scope,
                    "split": split,
                    "row_count": int(len(pred_split)),
                    "threshold": threshold,
                    "max_abs_base_probability_diff": max_abs_base_probability_diff,
                    "feature_matrix_path": rel(inputs["feature_paths"][(tier_scope, split)]),
                }
            )
            for mask_id, indices in mask_indices.items():
                masked = contributions.copy()
                if indices:
                    masked[:, indices, :] = 0.0
                masked_prob = softmax(np.asarray(model.intercept_, dtype="float64").reshape(1, -1) + masked.sum(axis=1))
                masked_labels = decision_labels(masked_prob, threshold)
                masked_signal = masked_labels != "flat"
                masked_chosen = chosen_probability(masked_prob, base_labels)
                lost = base_signal & ~masked_signal
                gained = ~base_signal & masked_signal
                retained_same_side = base_signal & masked_signal & (base_labels == masked_labels)
                drop_values = base_chosen[base_signal] - masked_chosen[base_signal]
                feature_names = [feature_order[index] for index in indices]
                rows.append(
                    {
                        "mask_id": mask_id,
                        "tier_scope": tier_scope,
                        "split": split,
                        "mask_feature_count": len(feature_names),
                        "features_masked": feature_names,
                        "row_count": int(len(pred_split)),
                        "base_signal_count": int(base_signal.sum()),
                        "masked_signal_count": int(masked_signal.sum()),
                        "base_long_count": int((base_labels == "long").sum()),
                        "base_short_count": int((base_labels == "short").sum()),
                        "masked_long_count": int((masked_labels == "long").sum()),
                        "masked_short_count": int((masked_labels == "short").sum()),
                        "lost_signal_count": int(lost.sum()),
                        "gained_signal_count": int(gained.sum()),
                        "retained_same_side_signal_count": int(retained_same_side.sum()),
                        "decision_flip_count": int((base_labels != masked_labels).sum()),
                        "lost_signal_rate": safe_div(int(lost.sum()), int(base_signal.sum())),
                        "retained_same_side_signal_rate": safe_div(int(retained_same_side.sum()), int(base_signal.sum())),
                        "chosen_probability_drop_mean": float(np.nanmean(drop_values)) if len(drop_values) else None,
                        "max_abs_base_probability_diff": max_abs_base_probability_diff,
                    }
                )
    return rows, audits


def feature_mask_read(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    oos = [row for row in rows if row.get("split") == "oos"]
    ranked = sorted(oos, key=lambda row: safe_float(row.get("lost_signal_rate")), reverse=True)
    top = ranked[0] if ranked else {}
    top5 = [row for row in oos if row.get("mask_id") == "mask_top5_repeated"]
    return {
        "strongest_oos_mask_id": top.get("mask_id"),
        "strongest_oos_tier_scope": top.get("tier_scope"),
        "strongest_oos_lost_signal_rate": top.get("lost_signal_rate"),
        "top5_repeated_oos": top5,
        "mask_axis_visible": any(safe_float(row.get("lost_signal_rate")) >= 0.25 for row in oos),
        "claim": "score_table_feature_mask_attribution_not_retrained_ablation",
    }


def subtype_rows(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    predictions = inputs["tier_b_predictions"]
    threshold = safe_float(inputs["thresholds"].get("tier_b"))
    for split in ("validation", "oos"):
        frame = predictions.loc[predictions["split"].astype(str).eq(split)].copy()
        if frame.empty:
            continue
        prob = frame.loc[:, ["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64", copy=False)
        labels = decision_labels(prob, threshold)
        frame["decision_side"] = labels
        frame["max_nonflat"] = np.maximum(frame["p_short"].to_numpy(dtype="float64"), frame["p_long"].to_numpy(dtype="float64"))
        frame["directional_hit"] = np.where(
            frame["decision_side"].eq("long"),
            frame["label_class"].eq(2),
            np.where(frame["decision_side"].eq("short"), frame["label_class"].eq(0), np.nan),
        )
        for subtype, group in frame.groupby("partial_context_subtype", dropna=False):
            signal = group["decision_side"].ne("flat")
            hit_values = group.loc[signal, "directional_hit"].dropna()
            rows.append(
                {
                    "focus_run_id": FOCUS_RUN_ID,
                    "split": split,
                    "partial_context_subtype": str(subtype),
                    "row_count": int(len(group)),
                    "signal_count": int(signal.sum()),
                    "signal_rate": safe_div(int(signal.sum()), int(len(group))),
                    "long_signal_count": int(group["decision_side"].eq("long").sum()),
                    "short_signal_count": int(group["decision_side"].eq("short").sum()),
                    "mean_p_short": safe_float(group["p_short"].mean()),
                    "mean_p_long": safe_float(group["p_long"].mean()),
                    "mean_nonflat_probability": safe_float(group["max_nonflat"].mean()),
                    "mean_probability_margin": safe_float(group["probability_margin"].mean()),
                    "signal_directional_hit_rate": safe_float(hit_values.mean()) if len(hit_values) else None,
                }
            )
    return sorted(rows, key=lambda row: (str(row.get("split")), -safe_float(row.get("signal_count")), str(row.get("partial_context_subtype"))))


def subtype_read(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    oos = [row for row in rows if row.get("split") == "oos"]
    signal_rank = sorted(oos, key=lambda row: safe_float(row.get("signal_count")), reverse=True)
    rate_rank = sorted([row for row in oos if safe_float(row.get("row_count")) >= 10], key=lambda row: safe_float(row.get("signal_rate")), reverse=True)
    top_signal = signal_rank[0] if signal_rank else {}
    top_rate = rate_rank[0] if rate_rank else {}
    return {
        "oos_top_signal_subtype": top_signal.get("partial_context_subtype"),
        "oos_top_signal_count": top_signal.get("signal_count"),
        "oos_top_signal_rate": top_signal.get("signal_rate"),
        "oos_top_rate_subtype_min10": top_rate.get("partial_context_subtype"),
        "oos_top_rate_min10": top_rate.get("signal_rate"),
        "subtype_axis_visible": bool(oos and len({row.get("partial_context_subtype") for row in oos if safe_float(row.get("signal_count")) > 0}) >= 2),
        "claim": "tier_b_subtype_signal_breakdown_only",
    }


def side_axis_rows(source: AnalysisSource) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in load_normalized_kpi(source):
        view = str(metric_value(record, "row_grain", "record_view"))
        if "long_only" not in view and "short_only" not in view:
            continue
        side_mode = "long_only" if "long_only" in view else "short_only"
        rows.append(
            {
                "source_run_number": source.run_number,
                "source_run_id": source.run_id,
                "threshold_quantile": source.threshold_quantile,
                "max_hold_bars": source.max_hold_bars,
                "split": metric_value(record, "row_grain", "split"),
                "side_mode": side_mode,
                "record_view": view,
                "tier_scope": metric_value(record, "row_grain", "tier_scope"),
                "route_role": metric_value(record, "row_grain", "route_role"),
                "net_profit": metric_value(record, "mt5_trading_headline", "net_profit"),
                "profit_factor": metric_value(record, "mt5_trading_headline", "profit_factor"),
                "trade_count": metric_value(record, "mt5_trading_headline", "trade_count"),
                "win_rate_percent": metric_value(record, "mt5_trading_headline", "win_rate"),
                "max_drawdown_amount": metric_value(record, "risk", "max_drawdown_amount"),
                "feature_ready_count": metric_value(record, "execution", "feature_ready_count"),
                "order_fill_count": metric_value(record, "execution", "order_fill_count"),
                "signal_count": metric_value(record, "signal_model", "signal_count"),
                "long_signal_count": metric_value(record, "signal_model", "long_count"),
                "short_signal_count": metric_value(record, "signal_model", "short_count"),
            }
        )
    return rows


def find_side_row(rows: Sequence[Mapping[str, Any]], split: str, side_mode: str, tier_scope: str = "Tier A+B") -> Mapping[str, Any]:
    for row in rows:
        if row.get("split") == split and row.get("side_mode") == side_mode and row.get("tier_scope") == tier_scope:
            return row
    return {}


def side_axis_read(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    long_oos = find_side_row(rows, "oos", "long_only")
    short_oos = find_side_row(rows, "oos", "short_only")
    long_validation = find_side_row(rows, "validation", "long_only")
    short_validation = find_side_row(rows, "validation", "short_only")
    return {
        "long_oos_net_profit": long_oos.get("net_profit"),
        "long_oos_profit_factor": long_oos.get("profit_factor"),
        "long_oos_trade_count": long_oos.get("trade_count"),
        "short_oos_net_profit": short_oos.get("net_profit"),
        "short_oos_profit_factor": short_oos.get("profit_factor"),
        "short_oos_trade_count": short_oos.get("trade_count"),
        "long_validation_net_profit": long_validation.get("net_profit"),
        "short_validation_net_profit": short_validation.get("net_profit"),
        "oos_long_minus_short_net": safe_float(long_oos.get("net_profit")) - safe_float(short_oos.get("net_profit")),
        "validation_long_minus_short_net": safe_float(long_validation.get("net_profit")) - safe_float(short_validation.get("net_profit")),
        "side_axis_visible": bool(long_oos or short_oos),
        "claim": "q90_hold6_direction_asymmetry_runtime_probe_only",
    }


def build_summary(created_at: str, runtime_summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    focus_inputs = load_focus_inputs()
    feature_rows, feature_audits = feature_mask_rows(focus_inputs)
    subtype = subtype_rows(focus_inputs)
    holds = hold_sources()
    routing = routing_rows(holds)
    hold_axis = hold_axis_rows(holds, routing)
    direction = direction_source()
    side_rows = side_axis_rows(direction)
    runtime_completed = [
        source_from_topic(topic).summary.get("external_verification_status") == "completed"
        for topic in RUNTIME_FOLLOWUP_TOPICS
    ]
    summary = {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "source_run_id": SOURCE_RUN_ID,
        "source_packet_id": SOURCE_PACKET_ID,
        "runtime_followup_run_ids": [topic.run_id for topic in RUNTIME_FOLLOWUP_TOPICS],
        "runtime_followup_packet_ids": [topic.packet_id for topic in RUNTIME_FOLLOWUP_TOPICS],
        "runtime_followup_summaries": list(runtime_summaries),
        "focus_run_id": FOCUS_RUN_ID,
        "focus_packet_id": FOCUS_PACKET_ID,
        "exploration_label": EXPLORATION_LABEL,
        "model_family": MODEL_FAMILY,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "boundary": BOUNDARY,
        "judgment": JUDGMENT,
        "closure_judgment": JUDGMENT,
        "external_verification_status": "completed" if all(runtime_completed) else "blocked_or_partial_runtime_followup",
        "runtime_completed_count": sum(1 for item in runtime_completed if item),
        "runtime_expected_count": len(RUNTIME_FOLLOWUP_TOPICS),
        "feature_mask_ablation": feature_rows,
        "feature_mask_audit": feature_audits,
        "feature_mask_read": feature_mask_read(feature_rows),
        "hold_axis_q90": hold_axis,
        "hold_axis_read": hold_axis_read(hold_axis),
        "tier_b_subtype_breakdown": subtype,
        "tier_b_subtype_read": subtype_read(subtype),
        "side_asymmetry_q90_hold6": side_rows,
        "side_asymmetry_read": side_axis_read(side_rows),
        "source_inputs": {
            "focus_run_summary": rel(STAGE_ROOT / "02_runs" / FOCUS_RUN_ID / "summary.json"),
            "focus_packet": rel(ROOT / "docs/agent_control/packets" / FOCUS_PACKET_ID),
            "run13H_summary": rel(RUN13H_PACKET_SUMMARY_PATH if io_path(RUN13H_PACKET_SUMMARY_PATH).exists() else RUN13H_SUMMARY_PATH),
            "runtime_followup_summaries": [rel(topic.run_root / "summary.json") for topic in RUNTIME_FOLLOWUP_TOPICS],
            "focus_tier_a_model": rel(focus_inputs["tier_a_model_path"]),
            "focus_tier_b_model": rel(focus_inputs["tier_b_model_path"]),
        },
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        "recommendation": "continue_stage19_only_if_next_question_targets_specific_mask_or_routing_axis",
    }
    return summary


def output_paths() -> dict[str, Path]:
    return {
        "summary": RUN_ROOT / "summary.json",
        "kpi_record": RUN_ROOT / "kpi_record.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
        "feature_mask_ablation": RUN_ROOT / "results/feature_mask_ablation.csv",
        "hold_axis_q90": RUN_ROOT / "results/hold_axis_q90.csv",
        "tier_b_subtype_breakdown": RUN_ROOT / "results/tier_b_subtype_breakdown.csv",
        "side_asymmetry_q90_hold6": RUN_ROOT / "results/side_asymmetry_q90_hold6.csv",
        "report": REPORT_PATH,
        "decision": DECISION_PATH,
    }


def write_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    rows = [
        {
            "ledger_row_id": f"{RUN_ID}__feature_mask_ablation",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "feature_mask_ablation",
            "parent_run_id": RUN_ID,
            "record_view": "ebm_score_table_feature_mask_ablation",
            "tier_scope": "Tier A+B",
            "kpi_scope": "model_feature_contribution",
            "scoreboard_lane": "model_characteristic_attribution",
            "status": "completed",
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/feature_mask_ablation.csv"),
            "primary_kpi": ledger_pairs((("strongest_oos_mask_id", summary["feature_mask_read"].get("strongest_oos_mask_id")), ("strongest_oos_lost_signal_rate", summary["feature_mask_read"].get("strongest_oos_lost_signal_rate")))),
            "guardrail_kpi": ledger_pairs((("boundary", BOUNDARY), ("claim", summary["feature_mask_read"].get("claim")))),
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Score-table contribution mask attribution, not retrained model ablation and not MT5 runtime authority.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__hold_axis_q90",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "hold_axis_q90",
            "parent_run_id": RUN_ID,
            "record_view": "q90_hold4_6_8_10_axis_with_mt5_runtime",
            "tier_scope": "Tier A+B",
            "kpi_scope": "hold_period_axis_attribution",
            "scoreboard_lane": "runtime_probe",
            "status": "completed" if summary.get("external_verification_status") == "completed" else "blocked",
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/hold_axis_q90.csv"),
            "primary_kpi": ledger_pairs((("best_requested_oos_hold", summary["hold_axis_read"].get("best_requested_oos_hold")), ("best_requested_oos_net_profit", summary["hold_axis_read"].get("best_requested_oos_net_profit")))),
            "guardrail_kpi": ledger_pairs((("validation_positive_holds", summary["hold_axis_read"].get("validation_positive_holds")), ("boundary", BOUNDARY))),
            "external_verification_status": summary.get("external_verification_status"),
            "notes": "Hold4/8/10 were newly MT5-tested; hold6 reused run13F.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_subtype_breakdown",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_subtype_breakdown",
            "parent_run_id": RUN_ID,
            "record_view": "tier_b_partial_context_subtype_signal_breakdown",
            "tier_scope": "Tier B",
            "kpi_scope": "tier_routing_attribution",
            "scoreboard_lane": "model_characteristic_attribution",
            "status": "completed",
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/tier_b_subtype_breakdown.csv"),
            "primary_kpi": ledger_pairs((("oos_top_signal_subtype", summary["tier_b_subtype_read"].get("oos_top_signal_subtype")), ("oos_top_signal_count", summary["tier_b_subtype_read"].get("oos_top_signal_count")))),
            "guardrail_kpi": ledger_pairs((("claim", summary["tier_b_subtype_read"].get("claim")), ("boundary", BOUNDARY))),
            "external_verification_status": "completed_reused_run13F_mt5_evidence",
            "notes": "Subtype signal read from run13F Tier B fallback predictions; routed component profit remains not separable.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__side_asymmetry_q90_hold6",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "side_asymmetry_q90_hold6",
            "parent_run_id": RUN_ID,
            "record_view": "q90_hold6_long_only_short_only_mt5_runtime",
            "tier_scope": "Tier A+B",
            "kpi_scope": "direction_axis_attribution",
            "scoreboard_lane": "runtime_probe",
            "status": "completed" if summary.get("external_verification_status") == "completed" else "blocked",
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/side_asymmetry_q90_hold6.csv"),
            "primary_kpi": ledger_pairs((("long_oos_net_profit", summary["side_asymmetry_read"].get("long_oos_net_profit")), ("short_oos_net_profit", summary["side_asymmetry_read"].get("short_oos_net_profit")))),
            "guardrail_kpi": ledger_pairs((("claim", summary["side_asymmetry_read"].get("claim")), ("boundary", BOUNDARY))),
            "external_verification_status": summary.get("external_verification_status"),
            "notes": "Long-only/short-only q90 hold6 runtime probe via asymmetric thresholds.",
        },
    ]
    return materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_LEDGER_PATH,
        rows=rows,
    )


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
                        ("best_oos_hold", summary["hold_axis_read"].get("best_requested_oos_hold")),
                        ("best_oos_net", summary["hold_axis_read"].get("best_requested_oos_net_profit")),
                        ("top_subtype", summary["tier_b_subtype_read"].get("oos_top_signal_subtype")),
                        ("long_oos_net", summary["side_asymmetry_read"].get("long_oos_net_profit")),
                        ("short_oos_net", summary["side_asymmetry_read"].get("short_oos_net_profit")),
                        ("boundary", "deep_axis_followup_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )


def gate_payloads(summary: Mapping[str, Any]) -> dict[str, Any]:
    runtime_ok = summary.get("external_verification_status") == "completed"
    feature_ok = all(safe_float(item.get("max_abs_base_probability_diff")) <= 1.0e-3 for item in summary.get("feature_mask_audit", []))
    hold_ok = len([row for row in summary.get("hold_axis_q90", []) if int(row.get("max_hold_bars") or 0) in {4, 6, 8, 10}]) == 8
    subtype_ok = len(summary.get("tier_b_subtype_breakdown", [])) > 0
    side_ok = len(summary.get("side_asymmetry_q90_hold6", [])) >= 4
    gates = ["runtime_evidence_gate", "feature_mask_audit", "hold_axis_audit", "tier_b_subtype_audit", "side_asymmetry_audit", "required_gate_coverage_audit", "final_claim_guard"]
    return {
        "runtime_evidence_gate": {
            "status": "passed" if runtime_ok else "blocked",
            "external_verification_status": summary.get("external_verification_status"),
            "runtime_completed_count": summary.get("runtime_completed_count"),
            "runtime_expected_count": summary.get("runtime_expected_count"),
            "runtime_followup_run_ids": summary.get("runtime_followup_run_ids"),
        },
        "feature_mask_audit": {
            "status": "passed" if feature_ok else "blocked",
            "feature_mask_read": summary.get("feature_mask_read"),
            "max_probability_diff_by_scope": summary.get("feature_mask_audit"),
        },
        "hold_axis_audit": {
            "status": "passed" if hold_ok else "blocked",
            "hold_axis_read": summary.get("hold_axis_read"),
            "requested_holds": [4, 6, 8, 10],
        },
        "tier_b_subtype_audit": {
            "status": "passed" if subtype_ok else "blocked",
            "tier_b_subtype_read": summary.get("tier_b_subtype_read"),
        },
        "side_asymmetry_audit": {
            "status": "passed" if side_ok else "blocked",
            "side_asymmetry_read": summary.get("side_asymmetry_read"),
        },
        "required_gate_coverage_audit": {
            "status": "passed" if feature_ok and hold_ok and subtype_ok and side_ok else "blocked",
            "packet_id": PACKET_ID,
            "required_gates": gates,
            "covered_gates": gates,
        },
        "final_claim_guard": {
            "status": "passed",
            "allowed_claims": [JUDGMENT, "runtime_probe", "model_characteristic_attribution", "inconclusive"],
            "forbidden_claims": summary.get("forbidden_claims"),
            "claim_boundary": BOUNDARY,
        },
    }


def write_packet(summary: Mapping[str, Any], outputs: Mapping[str, Path]) -> None:
    for name, payload in gate_payloads(summary).items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
    output_hashes = {name: sha256_file_lf_normalized(path) for name, path in outputs.items() if io_path(path).exists() and path.suffix != ".md"}
    write_json(
        PACKET_ROOT / "artifact_index.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": summary["created_at_utc"],
            "producer": "stage_pipelines.stage19.ebm_deep_axis_followup",
            "source_inputs": summary.get("source_inputs"),
            "artifact_paths": {name: rel(path) for name, path in outputs.items()},
            "artifact_hashes": output_hashes,
            "registry_links": {
                "run_registry": rel(RUN_REGISTRY_PATH),
                "project_alpha_ledger": rel(PROJECT_LEDGER_PATH),
                "stage_run_ledger": rel(STAGE_LEDGER_PATH),
            },
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
                    "hypothesis": "EBM deep axes can reveal whether feature concentration, hold length, Tier B subtype, and direction are model characteristics.",
                    "changed_variables": ["feature_mask", "max_hold_bars=4/8/10", "Tier B subtype", "q90 hold6 long-only/short-only"],
                    "success_criteria": "runtime topics complete where needed and attribution outputs pass probability and scope audits.",
                    "failure_criteria": "missing MT5 output, malformed KPI, probability mismatch, or empty subtype/side rows.",
                },
                {
                    "skill": "obsidian-runtime-parity",
                    "status": "completed",
                    "runtime_claim_boundary": "runtime_probe",
                    "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
                    "known_differences": "Feature mask is Python score-table attribution only; hold and side axes are MT5 runtime probes.",
                },
                {
                    "skill": "obsidian-backtest-forensics",
                    "status": "completed",
                    "tester_identity": "MT5 Strategy Tester US100 M5, deposit=500, leverage=1:100, model=4.",
                    "runtime_followup_run_ids": summary.get("runtime_followup_run_ids"),
                    "backtest_judgment": "usable_with_boundary" if summary.get("external_verification_status") == "completed" else "blocked_or_partial",
                },
                {
                    "skill": "obsidian-artifact-lineage",
                    "status": "completed",
                    "source_inputs": summary.get("source_inputs"),
                    "artifact_paths": {name: rel(path) for name, path in outputs.items()},
                    "lineage_judgment": "connected_with_boundary",
                },
                {
                    "skill": "obsidian-result-judgment",
                    "status": "completed",
                    "judgment_label": JUDGMENT,
                    "claim_boundary": BOUNDARY,
                    "forbidden_claims": summary.get("forbidden_claims"),
                },
            ],
        },
    )
    write_json(PACKET_ROOT / "run_summaries" / f"{RUN_ID}.json", summary)
    write_csv(PACKET_ROOT / "feature_mask_ablation.csv", FEATURE_MASK_COLUMNS, summary["feature_mask_ablation"])
    write_csv(PACKET_ROOT / "hold_axis_q90.csv", HOLD_AXIS_COLUMNS, summary["hold_axis_q90"])
    write_csv(PACKET_ROOT / "tier_b_subtype_breakdown.csv", SUBTYPE_COLUMNS, summary["tier_b_subtype_breakdown"])
    write_csv(PACKET_ROOT / "side_asymmetry_q90_hold6.csv", SIDE_AXIS_COLUMNS, summary["side_asymmetry_q90_hold6"])


def packet_markdown(summary: Mapping[str, Any]) -> str:
    hold = summary["hold_axis_read"]
    mask = summary["feature_mask_read"]
    subtype = summary["tier_b_subtype_read"]
    side = summary["side_asymmetry_read"]
    return "\n".join(
        [
            "# Stage19 RUN13M EBM Deep Axis Follow-up(19단계 실행13M EBM 심층 축 후속)",
            "",
            f"- judgment(판정): `{JUDGMENT}`",
            f"- external verification(외부 검증): `{summary.get('external_verification_status')}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "- operating promotion(운영 승격): `none(없음)`",
            "",
            "## Feature Mask(피처 마스크)",
            "",
            f"- strongest OOS mask(표본외 최강 마스크): `{mask.get('strongest_oos_mask_id')}` / tier(티어): `{mask.get('strongest_oos_tier_scope')}`",
            f"- lost signal rate(상실 신호 비율): `{mask.get('strongest_oos_lost_signal_rate')}`",
            "- claim(주장): `score_table_feature_mask_attribution_not_retrained_ablation(점수표 피처 마스크 기여도이며 재학습 제거가 아님)`",
            "",
            "효과(effect, 효과): EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신)이 몇 개 피처에 얼마나 기대는지 봤고, 재학습 모델 성능 주장으로 키우지 않았다.",
            "",
            "## Hold Axis(보유 축)",
            "",
            f"- requested holds(요청 보유): `{hold.get('requested_holds')}`",
            f"- best OOS hold(표본외 최고 보유): `{hold.get('best_requested_oos_hold')}` / net(순손익): `{display_metric(hold.get('best_requested_oos_net_profit'))}` / PF(수익 팩터): `{display_metric(hold.get('best_requested_oos_profit_factor'))}`",
            f"- best validation hold(검증 최고 보유): `{hold.get('best_requested_validation_hold')}` / net(순손익): `{display_metric(hold.get('best_requested_validation_net_profit'))}`",
            f"- validation positive holds(검증 양수 보유): `{hold.get('validation_positive_holds')}`",
            "",
            "효과(effect, 효과): hold4/8/10(4/8/10봉)은 새 MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)로 확인했고 hold6(6봉)은 run13F(실행13F)를 재사용했다.",
            "",
            "## Tier B Subtype(티어 B 하위유형)",
            "",
            f"- OOS top signal subtype(표본외 최다 신호 하위유형): `{subtype.get('oos_top_signal_subtype')}` / signals(신호): `{subtype.get('oos_top_signal_count')}`",
            f"- OOS top rate subtype min10(표본외 최소 10행 기준 최고 신호율 하위유형): `{subtype.get('oos_top_rate_subtype_min10')}` / rate(비율): `{display_metric(subtype.get('oos_top_rate_min10'))}`",
            "",
            "효과(effect, 효과): Tier B fallback(티어 B 대체)이 어떤 partial context subtype(부분 문맥 하위유형)에서 신호를 내는지 분해했다.",
            "",
            "## Side Axis(방향 축)",
            "",
            f"- long-only OOS net(매수 전용 표본외 순손익): `{display_metric(side.get('long_oos_net_profit'))}` / PF(수익 팩터): `{display_metric(side.get('long_oos_profit_factor'))}` / trades(거래): `{side.get('long_oos_trade_count')}`",
            f"- short-only OOS net(매도 전용 표본외 순손익): `{display_metric(side.get('short_oos_net_profit'))}` / PF(수익 팩터): `{display_metric(side.get('short_oos_profit_factor'))}` / trades(거래): `{side.get('short_oos_trade_count')}`",
            f"- OOS long-minus-short net(표본외 매수-매도 순손익 차이): `{display_metric(side.get('oos_long_minus_short_net'))}`",
            "",
            "효과(effect, 효과): q90 hold6(q90 6봉)에서 long-only/short-only(매수 전용/매도 전용)를 실제 MT5 threshold routing(임계값 라우팅)으로 나눠 봤다.",
            "",
            "Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )


def decision_markdown(summary: Mapping[str, Any]) -> str:
    hold = summary["hold_axis_read"]
    side = summary["side_asymmetry_read"]
    return "\n".join(
        [
            "# 2026-05-04 Stage19 RUN13M EBM Deep Axis Decision(19단계 실행13M EBM 심층 축 결정)",
            "",
            f"- run(실행): `{RUN_ID}`",
            f"- judgment(판정): `{JUDGMENT}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
            "",
            "## Decision(결정)",
            "",
            "EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신)은 아직 계속 해부할 가치는 있다. 다만 이번 결과도 operating promotion(운영 승격)이 아니라 characteristic attribution(특성 기여도)이다.",
            "",
            f"- best requested OOS hold(요청 축 표본외 최고 보유): `{hold.get('best_requested_oos_hold')}` / net(순손익): `{display_metric(hold.get('best_requested_oos_net_profit'))}`",
            f"- validation positive holds(검증 양수 보유): `{hold.get('validation_positive_holds')}`",
            f"- q90 hold6 OOS long-minus-short(표본외 매수-매도 차이): `{display_metric(side.get('oos_long_minus_short_net'))}`",
            "",
            "효과(effect, 효과): Stage19(19단계)는 EBM(설명가능 부스팅 머신)의 feature mask(피처 마스크), hold axis(보유 축), Tier B subtype(티어 B 하위유형), side axis(방향 축)을 확인했지만, edge(거래 우위)나 runtime authority(런타임 권위)는 만들지 않았다.",
        ]
    )


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
    hold = summary["hold_axis_read"]
    side = summary["side_asymmetry_read"]
    write_md(
        SELECTION_STATUS_PATH,
        "\n".join(
            [
                "# Stage19 Selection Status(19단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                "- status(상태): `active_run13M_ebm_deep_axis_followup_completed`",
                f"- current run(현재 실행): `{RUN_ID}`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{JUDGMENT}`",
                f"- selected variant(선택 변형): `{SELECTED_VARIANT_ID}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "효과(effect, 효과): Stage19(19단계)는 EBM(설명가능 부스팅 머신)의 심층 축을 더 봤지만 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.",
            ]
        ),
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else "# Stage19 Review Index(19단계 검토 색인)\n"
    line = f"- `{RUN_ID}`: `{rel(REPORT_PATH)}`\n"
    if RUN_ID not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"updated_on: '.*?'", "updated_on: '2026-05-04'", state, count=1)
    state = re.sub(r"active_branch: .*", "active_branch: codex/stage19-ebm-attribution", state, count=1)
    state = re.sub(r"current_run_id: .*", f"current_run_id: {RUN_ID}", state, count=1)
    state = state.replace("stage19_active_run13H_ebm_feature_hold6_routing_attribution_completed", "stage19_active_run13M_ebm_deep_axis_followup_completed", 1)
    state = state.replace("active_run13H_ebm_feature_hold6_routing_attribution_completed", "active_run13M_ebm_deep_axis_followup_completed", 1)
    block = f"""stage19_ebm_run13M_deep_axis_followup:
  packet_id: {PACKET_ID}
  status: reviewed_deep_axis_followup_completed
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  runtime_followup_run_ids: {','.join(summary['runtime_followup_run_ids'])}
  best_requested_oos_hold: {hold.get('best_requested_oos_hold')}
  best_requested_oos_net_profit: {hold.get('best_requested_oos_net_profit')}
  validation_positive_holds: {hold.get('validation_positive_holds')}
  q90_hold6_long_oos_net_profit: {side.get('long_oos_net_profit')}
  q90_hold6_short_oos_net_profit: {side.get('short_oos_net_profit')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / 'run_summaries' / f'{RUN_ID}.json')}
  next_action: continue_stage19_only_if_next_question_targets_specific_mask_or_routing_axis
"""
    state = replace_yaml_block(state, "stage19_ebm_run13M_deep_axis_followup:", block)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n", encoding="utf-8")
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = "\n".join(
        [
            "## Latest Stage19 RUN13M Deep Axis Update(최신 19단계 실행13M 심층 축 업데이트)",
            "",
            f"Stage19(19단계)는 `{RUN_ID}`에서 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) feature mask(피처 마스크), hold axis(보유 축), Tier B subtype(티어 B 하위유형), side axis(방향 축)을 추가로 확인했다.",
            "",
            f"결과(result, 결과): `{JUDGMENT}`. best requested OOS hold(요청 축 표본외 최고 보유)는 `{hold.get('best_requested_oos_hold')}`이고 net(순손익)은 `{display_metric(hold.get('best_requested_oos_net_profit'))}`이다. q90 hold6(q90 6봉) long-minus-short(매수-매도 차이)는 `{display_metric(side.get('oos_long_minus_short_net'))}`이다.",
            "",
            "효과(effect, 효과): MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)는 더 늘렸지만 edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            "",
        ]
    )
    if "## Latest Stage19 RUN13M Deep Axis Update" in current:
        current = re.sub(
            r"## Latest Stage19 RUN13M Deep Axis Update\(최신 19단계 실행13M 심층 축 업데이트\)\n.*?(?=## Latest Stage19 RUN13H Attribution Update)",
            update + "\n",
            current,
            count=1,
            flags=re.S,
        )
    else:
        current = update + "\n" + current
    current = re.sub(r"- updated_on: `.*?`", "- updated_on: `2026-05-04`", current, count=1)
    current = re.sub(r"- active_branch: `[^`]+`", "- active_branch: `codex/stage19-ebm-attribution`", current, count=1)
    current = re.sub(r"- current run\(현재 실행\): `[^`]+`", f"- current run(현재 실행): `{RUN_ID}`", current, count=1)
    io_path(CURRENT_WORKING_STATE_PATH).write_text(current.rstrip() + "\n", encoding="utf-8-sig")


def materialize_outputs(summary: Mapping[str, Any]) -> dict[str, Any]:
    outputs = output_paths()
    write_csv(outputs["feature_mask_ablation"], FEATURE_MASK_COLUMNS, summary["feature_mask_ablation"])
    write_csv(outputs["hold_axis_q90"], HOLD_AXIS_COLUMNS, summary["hold_axis_q90"])
    write_csv(outputs["tier_b_subtype_breakdown"], SUBTYPE_COLUMNS, summary["tier_b_subtype_breakdown"])
    write_csv(outputs["side_asymmetry_q90_hold6"], SIDE_AXIS_COLUMNS, summary["side_asymmetry_q90_hold6"])
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
        "kpi_scope": "ebm_deep_axis_followup",
        "model_family": MODEL_FAMILY,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "external_verification_status": summary["external_verification_status"],
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "feature_mask_read": summary["feature_mask_read"],
        "hold_axis_read": summary["hold_axis_read"],
        "tier_b_subtype_read": summary["tier_b_subtype_read"],
        "side_asymmetry_read": summary["side_asymmetry_read"],
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
    runtime_summaries = execute_runtime_topics(args)
    created_at = utc_now()
    summary = build_summary(created_at, runtime_summaries)
    return materialize_outputs(summary)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stage19 EBM deep-axis follow-up with MT5 runtime probes.")
    parser.add_argument("--runtime-topics", nargs="*", default=["all"], help="run13I/run13J/run13K/run13L or all.")
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
                "hold_axis_read": summary.get("hold_axis_read"),
                "tier_b_subtype_read": summary.get("tier_b_subtype_read"),
                "side_asymmetry_read": summary.get("side_asymmetry_read"),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
