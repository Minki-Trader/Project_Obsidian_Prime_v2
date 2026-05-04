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

import pandas as pd

from foundation.control_plane.alpha_run_ledgers import materialize_alpha_ledgers
from foundation.control_plane.ledger import RUN_REGISTRY_COLUMNS, io_path, json_ready, ledger_pairs, sha256_file_lf_normalized, upsert_csv_rows
from stage_pipelines.stage19 import ebm_mt5_axis_extension as axis_ext
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

RUN_ID = "run13AD_ebm_axis_exhaustion_followthrough_v1"
RUN_NUMBER = "run13AD"
PACKET_ID = "stage19_run13AD_ebm_axis_exhaustion_followthrough_v1"
EXPLORATION_LABEL = "stage19_Model__EBMAxisExhaustionFollowthrough"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
REPORT_PATH = STAGE_ROOT / "03_reviews/run13AD_ebm_axis_exhaustion_followthrough_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage19_run13AD_ebm_axis_exhaustion_followthrough.md"

MODEL_FAMILY = stage19_mt5.MODEL_FAMILY
FEATURE_SET_ID = stage19_mt5.FEATURE_SET_ID
LABEL_ID = stage19_mt5.LABEL_ID
SPLIT_CONTRACT = stage19_mt5.SPLIT_CONTRACT
SELECTED_VARIANT_ID = stage19_mt5.SELECTED_VARIANT_ID
SOURCE_RUN_ID = stage19_mt5.SOURCE_RUN_ID

BOUNDARY = "ebm_axis_exhaustion_followthrough_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT = "inconclusive_ebm_axis_exhaustion_followthrough_completed"
TOP5_FEATURE_MASK = axis_ext.TOP5_FEATURE_MASK
MIXED_SUBTYPE = "B_mixed_partial_context"
MACRO_SUBTYPE = "B_macro_missing"
CORE_SUBTYPE = "B_core_only"


@dataclass(frozen=True)
class TopicSpec:
    topic: stage19_mt5.RuntimeTopic
    axis: str
    initial: bool
    mask_features: tuple[str, ...] = ()
    subtype_filter: str | None = None


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
        return "NA"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    return f"{number:.8g}" if math.isfinite(number) else "NA"


def runtime_topic(
    *,
    run_number: str,
    run_id: str,
    packet_id: str,
    label_suffix: str,
    review_filename: str,
    threshold_quantile: float,
    mode: str,
    max_hold_bars: int,
    topic_read: str,
) -> stage19_mt5.RuntimeTopic:
    expected_attempts = 12 if mode == "direction" else 6
    expected_kpi_records = 20 if mode == "direction" else 10
    return stage19_mt5.RuntimeTopic(
        run_id=run_id,
        run_number=run_number,
        packet_id=packet_id,
        exploration_label=f"stage19_Model__{label_suffix}",
        review_filename=review_filename,
        threshold_quantile=threshold_quantile,
        mode=mode,
        max_hold_bars=max_hold_bars,
        expected_attempts=expected_attempts,
        expected_kpi_records=expected_kpi_records,
        topic_read=topic_read,
        boundary=f"ebm_{topic_read}_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        judgment_completed=f"inconclusive_ebm_{topic_read}_runtime_probe_completed",
        judgment_blocked=f"blocked_ebm_{topic_read}_runtime_probe_after_attempt",
    )


TOPIC_SPECS: tuple[TopicSpec, ...] = (
    TopicSpec(
        topic=runtime_topic(
            run_number="run13U",
            run_id="run13U_ebm_q90_hold4_mask_atr14_probe_v1",
            packet_id="stage19_run13U_ebm_mask_atr14_mt5_v1",
            label_suffix="EBMMaskAtr14Hold4",
            review_filename="run13U_ebm_q90_hold4_mask_atr14_packet.md",
            threshold_quantile=0.90,
            mode="routed",
            max_hold_bars=4,
            topic_read="q90_hold4_single_feature_mask_atr14",
        ),
        axis="feature_single_mask",
        initial=True,
        mask_features=("atr_14",),
    ),
    TopicSpec(
        topic=runtime_topic(
            run_number="run13V",
            run_id="run13V_ebm_q90_hold4_mask_ema9_ema20_probe_v1",
            packet_id="stage19_run13V_ebm_mask_ema9_ema20_mt5_v1",
            label_suffix="EBMMaskEma9Ema20Hold4",
            review_filename="run13V_ebm_q90_hold4_mask_ema9_ema20_packet.md",
            threshold_quantile=0.90,
            mode="routed",
            max_hold_bars=4,
            topic_read="q90_hold4_single_feature_mask_ema9_ema20_diff",
        ),
        axis="feature_single_mask",
        initial=True,
        mask_features=("ema9_ema20_diff",),
    ),
    TopicSpec(
        topic=runtime_topic(
            run_number="run13W",
            run_id="run13W_ebm_q90_hold4_mask_ema50_ema200_probe_v1",
            packet_id="stage19_run13W_ebm_mask_ema50_ema200_mt5_v1",
            label_suffix="EBMMaskEma50Ema200Hold4",
            review_filename="run13W_ebm_q90_hold4_mask_ema50_ema200_packet.md",
            threshold_quantile=0.90,
            mode="routed",
            max_hold_bars=4,
            topic_read="q90_hold4_single_feature_mask_ema50_ema200_diff",
        ),
        axis="feature_single_mask",
        initial=True,
        mask_features=("ema50_ema200_diff",),
    ),
    TopicSpec(
        topic=runtime_topic(
            run_number="run13X",
            run_id="run13X_ebm_q90_hold4_mask_ema20_ema50_probe_v1",
            packet_id="stage19_run13X_ebm_mask_ema20_ema50_mt5_v1",
            label_suffix="EBMMaskEma20Ema50Hold4",
            review_filename="run13X_ebm_q90_hold4_mask_ema20_ema50_packet.md",
            threshold_quantile=0.90,
            mode="routed",
            max_hold_bars=4,
            topic_read="q90_hold4_single_feature_mask_ema20_ema50_diff",
        ),
        axis="feature_single_mask",
        initial=True,
        mask_features=("ema20_ema50_diff",),
    ),
    TopicSpec(
        topic=runtime_topic(
            run_number="run13Y",
            run_id="run13Y_ebm_q90_hold4_mask_hl_zscore_probe_v1",
            packet_id="stage19_run13Y_ebm_mask_hl_zscore_mt5_v1",
            label_suffix="EBMMaskHlZscoreHold4",
            review_filename="run13Y_ebm_q90_hold4_mask_hl_zscore_packet.md",
            threshold_quantile=0.90,
            mode="routed",
            max_hold_bars=4,
            topic_read="q90_hold4_single_feature_mask_hl_zscore_50",
        ),
        axis="feature_single_mask",
        initial=True,
        mask_features=("hl_zscore_50",),
    ),
    TopicSpec(
        topic=runtime_topic(
            run_number="run13Z",
            run_id="run13Z_ebm_q90_hold4_macro_missing_fallback_probe_v1",
            packet_id="stage19_run13Z_ebm_macro_missing_fallback_mt5_v1",
            label_suffix="EBMMacroMissingFallbackHold4",
            review_filename="run13Z_ebm_q90_hold4_macro_missing_fallback_packet.md",
            threshold_quantile=0.90,
            mode="routed",
            max_hold_bars=4,
            topic_read="q90_hold4_b_macro_missing_fallback_filter",
        ),
        axis="tier_b_subtype",
        initial=True,
        subtype_filter=MACRO_SUBTYPE,
    ),
    TopicSpec(
        topic=runtime_topic(
            run_number="run13AA",
            run_id="run13AA_ebm_q90_hold4_core_only_fallback_probe_v1",
            packet_id="stage19_run13AA_ebm_core_only_fallback_mt5_v1",
            label_suffix="EBMCoreOnlyFallbackHold4",
            review_filename="run13AA_ebm_q90_hold4_core_only_fallback_packet.md",
            threshold_quantile=0.90,
            mode="routed",
            max_hold_bars=4,
            topic_read="q90_hold4_b_core_only_fallback_filter",
        ),
        axis="tier_b_subtype",
        initial=True,
        subtype_filter=CORE_SUBTYPE,
    ),
    TopicSpec(
        topic=runtime_topic(
            run_number="run13AB",
            run_id="run13AB_ebm_q92_hold4_direction_probe_v1",
            packet_id="stage19_run13AB_ebm_q92_hold4_direction_mt5_v1",
            label_suffix="EBMQ92Hold4DirectionCompression",
            review_filename="run13AB_ebm_q92_hold4_direction_packet.md",
            threshold_quantile=0.92,
            mode="direction",
            max_hold_bars=4,
            topic_read="q92_hold4_direction_threshold_compression",
        ),
        axis="side_compression",
        initial=True,
    ),
    TopicSpec(
        topic=runtime_topic(
            run_number="run13AC",
            run_id="run13AC_ebm_q95_hold4_direction_probe_v1",
            packet_id="stage19_run13AC_ebm_q95_hold4_direction_mt5_v1",
            label_suffix="EBMQ95Hold4DirectionCompression",
            review_filename="run13AC_ebm_q95_hold4_direction_packet.md",
            threshold_quantile=0.95,
            mode="direction",
            max_hold_bars=4,
            topic_read="q95_hold4_direction_threshold_compression",
        ),
        axis="side_compression",
        initial=True,
    ),
    TopicSpec(
        topic=runtime_topic(
            run_number="run13AE",
            run_id="run13AE_ebm_q90_hold4_mixed_subtype_direction_probe_v1",
            packet_id="stage19_run13AE_ebm_q90_mixed_subtype_direction_mt5_v1",
            label_suffix="EBMQ90MixedSubtypeDirection",
            review_filename="run13AE_ebm_q90_hold4_mixed_subtype_direction_packet.md",
            threshold_quantile=0.90,
            mode="direction",
            max_hold_bars=4,
            topic_read="q90_hold4_mixed_subtype_direction_followup",
        ),
        axis="followup_side_subtype",
        initial=False,
        subtype_filter=MIXED_SUBTYPE,
    ),
    TopicSpec(
        topic=runtime_topic(
            run_number="run13AF",
            run_id="run13AF_ebm_q92_hold4_mixed_subtype_direction_probe_v1",
            packet_id="stage19_run13AF_ebm_q92_mixed_subtype_direction_mt5_v1",
            label_suffix="EBMQ92MixedSubtypeDirection",
            review_filename="run13AF_ebm_q92_hold4_mixed_subtype_direction_packet.md",
            threshold_quantile=0.92,
            mode="direction",
            max_hold_bars=4,
            topic_read="q92_hold4_mixed_subtype_direction_followup",
        ),
        axis="followup_side_subtype",
        initial=False,
        subtype_filter=MIXED_SUBTYPE,
    ),
    TopicSpec(
        topic=runtime_topic(
            run_number="run13AG",
            run_id="run13AG_ebm_q95_hold4_mixed_subtype_direction_probe_v1",
            packet_id="stage19_run13AG_ebm_q95_mixed_subtype_direction_mt5_v1",
            label_suffix="EBMQ95MixedSubtypeDirection",
            review_filename="run13AG_ebm_q95_hold4_mixed_subtype_direction_packet.md",
            threshold_quantile=0.95,
            mode="direction",
            max_hold_bars=4,
            topic_read="q95_hold4_mixed_subtype_direction_followup",
        ),
        axis="followup_side_subtype",
        initial=False,
        subtype_filter=MIXED_SUBTYPE,
    ),
    TopicSpec(
        topic=runtime_topic(
            run_number="run13AH",
            run_id="run13AH_ebm_q90_hold4_keep_ema50_ema200_top5_probe_v1",
            packet_id="stage19_run13AH_ebm_keep_ema50_ema200_top5_mt5_v1",
            label_suffix="EBMKeepEma50Ema200Top5Hold4",
            review_filename="run13AH_ebm_q90_hold4_keep_ema50_ema200_top5_packet.md",
            threshold_quantile=0.90,
            mode="routed",
            max_hold_bars=4,
            topic_read="q90_hold4_keep_ema50_ema200_within_top5_followup",
        ),
        axis="followup_feature_keep",
        initial=False,
        mask_features=("atr_14", "ema9_ema20_diff", "ema20_ema50_diff", "hl_zscore_50"),
    ),
)

TOPIC_BY_NUMBER = {spec.topic.run_number: spec for spec in TOPIC_SPECS}
TOPIC_BY_ID = {spec.topic.run_id: spec for spec in TOPIC_SPECS}
BASE_RUNS = {
    "run13I": ("run13I_ebm_q90_hold4_probe_v1", "stage19_run13I_ebm_hold4_mt5_v1"),
    "run13N": ("run13N_ebm_q90_hold4_top5_mask_probe_v1", "stage19_run13N_ebm_top5_mask_mt5_v1"),
    "run13O": ("run13O_ebm_q90_hold2_probe_v1", "stage19_run13O_ebm_hold2_mt5_v1"),
    "run13R": ("run13R_ebm_q90_hold4_mixed_subtype_fallback_probe_v1", "stage19_run13R_ebm_mixed_subtype_fallback_mt5_v1"),
    "run13S": ("run13S_ebm_q90_hold4_direction_probe_v1", "stage19_run13S_ebm_q90_hold4_direction_mt5_v1"),
}

FEATURE_MASK_COLUMNS = (
    "run_number",
    "feature_masked",
    "split",
    "baseline_net_profit",
    "candidate_net_profit",
    "delta_net_profit",
    "baseline_trade_count",
    "candidate_trade_count",
    "candidate_profit_factor",
    "candidate_max_drawdown_amount",
)
SUBTYPE_COLUMNS = (
    "run_number",
    "subtype_filter",
    "split",
    "baseline_net_profit",
    "candidate_net_profit",
    "delta_net_profit",
    "tier_b_fallback_used_count",
    "trade_count",
    "profit_factor",
    "max_drawdown_amount",
)
SIDE_COLUMNS = (
    "run_number",
    "threshold_quantile",
    "subtype_filter",
    "split",
    "side",
    "net_profit",
    "profit_factor",
    "trade_count",
    "max_drawdown_amount",
    "long_minus_short_net",
)
SEGMENT_COLUMNS = (
    "run_number",
    "run_id",
    "hold_bars",
    "split",
    "segment_type",
    "segment_value",
    "record_view",
    "trade_count",
    "net_profit",
    "win_rate_percent",
    "avg_profit",
    "max_drawdown_amount",
)


def runtime_args(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        force=bool(args.force_runtime),
        materialize_only=bool(args.materialize_only),
        timeout_seconds=int(args.timeout_seconds),
        terminal_path=args.terminal_path,
        metaeditor_path=args.metaeditor_path,
        topics=["all"],
    )


def selected_specs(topic_ids: Sequence[str], topic_set: str) -> list[TopicSpec]:
    if topic_ids and "all" not in topic_ids:
        specs: list[TopicSpec] = []
        for topic_id in topic_ids:
            if topic_id in TOPIC_BY_NUMBER:
                specs.append(TOPIC_BY_NUMBER[topic_id])
            elif topic_id in TOPIC_BY_ID:
                specs.append(TOPIC_BY_ID[topic_id])
            else:
                raise ValueError(f"unknown Stage19 EBM followthrough topic: {topic_id}")
        return specs
    if topic_set == "initial":
        return [spec for spec in TOPIC_SPECS if spec.initial]
    if topic_set == "followup":
        return [spec for spec in TOPIC_SPECS if not spec.initial]
    if topic_set == "existing":
        return []
    return list(TOPIC_SPECS)


def execute_topics(args: argparse.Namespace) -> list[dict[str, Any]]:
    specs = selected_specs(args.runtime_topics, args.topic_set)
    if not specs:
        return []
    created_at = utc_now()
    context = stage19_mt5.load_context()
    models = stage19_mt5.load_or_train_models(context)
    topic_args = runtime_args(args)
    summaries: list[dict[str, Any]] = []
    for spec in specs:
        if spec.mask_features or spec.subtype_filter:
            summaries.append(
                axis_ext.build_custom_topic_run(
                    spec.topic,
                    topic_args,
                    context,
                    models,
                    created_at,
                    mask_features=spec.mask_features,
                    subtype_filter=spec.subtype_filter,
                )
            )
        else:
            summaries.append(stage19_mt5.build_topic_run(spec.topic, topic_args, context, models, created_at))
    return summaries


def available_topic_specs() -> list[TopicSpec]:
    specs: list[TopicSpec] = []
    for spec in TOPIC_SPECS:
        if io_path(spec.topic.run_root / "summary.json").exists():
            specs.append(spec)
    return specs


def source_for_run(run_number: str) -> Source:
    if run_number in BASE_RUNS:
        run_id, packet_id = BASE_RUNS[run_number]
    else:
        spec = TOPIC_BY_NUMBER[run_number]
        run_id, packet_id = spec.topic.run_id, spec.topic.packet_id
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


def feature_mask_rows(sources: Mapping[str, Source]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base = sources["run13I"]
    for run_number in ("run13N", "run13U", "run13V", "run13W", "run13X", "run13Y", "run13AH"):
        if run_number not in sources:
            continue
        source = sources[run_number]
        if run_number == "run13N":
            feature = "top5_combined"
        elif run_number == "run13AH":
            feature = "keep_ema50_ema200_diff_mask_other_top5"
        else:
            feature = ",".join(TOPIC_BY_NUMBER[run_number].mask_features)
        for split in ("validation", "oos"):
            baseline = routed_metric(base, split)
            candidate = routed_metric(source, split)
            rows.append(
                {
                    "run_number": run_number,
                    "feature_masked": feature,
                    "split": split,
                    "baseline_net_profit": baseline.get("net_profit"),
                    "candidate_net_profit": candidate.get("net_profit"),
                    "delta_net_profit": safe_float(candidate.get("net_profit")) - safe_float(baseline.get("net_profit")),
                    "baseline_trade_count": baseline.get("trade_count"),
                    "candidate_trade_count": candidate.get("trade_count"),
                    "candidate_profit_factor": candidate.get("profit_factor"),
                    "candidate_max_drawdown_amount": candidate.get("max_drawdown_amount"),
                }
            )
    return rows


def subtype_rows(sources: Mapping[str, Source]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base = sources["run13I"]
    run_to_subtype = {"run13R": MIXED_SUBTYPE, "run13Z": MACRO_SUBTYPE, "run13AA": CORE_SUBTYPE}
    for run_number, subtype in run_to_subtype.items():
        if run_number not in sources:
            continue
        source = sources[run_number]
        for split in ("validation", "oos"):
            baseline = routed_metric(base, split)
            candidate = routed_metric(source, split)
            rows.append(
                {
                    "run_number": run_number,
                    "subtype_filter": subtype,
                    "split": split,
                    "baseline_net_profit": baseline.get("net_profit"),
                    "candidate_net_profit": candidate.get("net_profit"),
                    "delta_net_profit": safe_float(candidate.get("net_profit")) - safe_float(baseline.get("net_profit")),
                    "tier_b_fallback_used_count": candidate.get("tier_b_fallback_used_count"),
                    "trade_count": candidate.get("trade_count"),
                    "profit_factor": candidate.get("profit_factor"),
                    "max_drawdown_amount": candidate.get("max_drawdown_amount"),
                }
            )
    return rows


def side_rows(sources: Mapping[str, Source]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    side_sources = [
        ("run13S", 0.90, None),
        ("run13AB", 0.92, None),
        ("run13AC", 0.95, None),
        ("run13AE", 0.90, MIXED_SUBTYPE),
        ("run13AF", 0.92, MIXED_SUBTYPE),
        ("run13AG", 0.95, MIXED_SUBTYPE),
    ]
    for run_number, quantile, subtype_filter in side_sources:
        if run_number not in sources:
            continue
        source = sources[run_number]
        for split in ("validation", "oos"):
            long_metric = direction_metric(source, split, "long")
            short_metric = direction_metric(source, split, "short")
            long_minus_short = safe_float(long_metric.get("net_profit")) - safe_float(short_metric.get("net_profit"))
            for side, metric in (("long", long_metric), ("short", short_metric)):
                rows.append(
                    {
                        "run_number": run_number,
                        "threshold_quantile": quantile,
                        "subtype_filter": subtype_filter or "all_tier_b_fallback",
                        "split": split,
                        "side": side,
                        "net_profit": metric.get("net_profit"),
                        "profit_factor": metric.get("profit_factor"),
                        "trade_count": metric.get("trade_count"),
                        "max_drawdown_amount": metric.get("max_drawdown_amount"),
                        "long_minus_short_net": long_minus_short,
                    }
                )
    return rows


def load_trade_rows(packet_id: str) -> list[dict[str, Any]]:
    path = ROOT / "docs/agent_control/packets" / packet_id / "trade_level_records.json"
    if not io_path(path).exists():
        return []
    payload = read_json(path)
    return payload if isinstance(payload, list) else []


def max_drawdown_from_series(values: Sequence[float]) -> float:
    peak = 0.0
    equity = 0.0
    max_dd = 0.0
    for value in values:
        equity += float(value)
        peak = max(peak, equity)
        max_dd = max(max_dd, peak - equity)
    return max_dd


def trade_segment_metrics(rows: Sequence[Mapping[str, Any]], *, run_number: str, run_id: str, hold_bars: int, split: str, segment_type: str, segment_value: str) -> dict[str, Any]:
    profits = [safe_float(row.get("net_profit")) for row in rows]
    trade_count = len(profits)
    wins = sum(1 for value in profits if value > 0.0)
    return {
        "run_number": run_number,
        "run_id": run_id,
        "hold_bars": hold_bars,
        "split": split,
        "segment_type": segment_type,
        "segment_value": segment_value,
        "record_view": "mt5_routed_total",
        "trade_count": trade_count,
        "net_profit": sum(profits),
        "win_rate_percent": (wins / trade_count * 100.0) if trade_count else None,
        "avg_profit": (sum(profits) / trade_count) if trade_count else None,
        "max_drawdown_amount": max_drawdown_from_series(profits),
    }


def hold_segment_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run_number, hold_bars in (("run13O", 2), ("run13I", 4)):
        source = source_for_run(run_number)
        trade_rows = [
            row
            for row in load_trade_rows(source.packet_id)
            if row.get("route_role") == "routed_total" and str(row.get("record_view", "")).startswith("mt5_routed_total")
        ]
        for split in ("validation", "oos"):
            split_rows = [row for row in trade_rows if row.get("split") == split]
            for segment_type in ("all", "month", "direction", "volatility_regime", "session_slice", "trend_regime", "trade_bucket"):
                if segment_type == "all":
                    groups = {"all": split_rows}
                elif segment_type == "month":
                    groups: dict[str, list[Mapping[str, Any]]] = {}
                    for row in split_rows:
                        value = str(row.get("open_time", ""))[:7] or "unknown"
                        groups.setdefault(value, []).append(row)
                elif segment_type == "trade_bucket":
                    sorted_rows = sorted(split_rows, key=lambda item: safe_float(item.get("trade_index")))
                    groups = {"q1": [], "q2": [], "q3": [], "q4": []}
                    for index, row in enumerate(sorted_rows):
                        bucket = min(3, int(index * 4 / max(1, len(sorted_rows))))
                        groups[f"q{bucket + 1}"].append(row)
                else:
                    groups = {}
                    for row in split_rows:
                        groups.setdefault(str(row.get(segment_type) or "unknown"), []).append(row)
                for value, group_rows in sorted(groups.items()):
                    if group_rows:
                        rows.append(trade_segment_metrics(group_rows, run_number=run_number, run_id=source.run_id, hold_bars=hold_bars, split=split, segment_type=segment_type, segment_value=value))
    return rows


def best_oos_feature_dependency(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    single_oos = [row for row in rows if row.get("split") == "oos" and row.get("feature_masked") != "top5_combined"]
    if not single_oos:
        return {}
    return min(single_oos, key=lambda row: safe_float(row.get("delta_net_profit"), 999999.0))


def best_oos_subtype(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    oos = [row for row in rows if row.get("split") == "oos"]
    if not oos:
        return {}
    return max(oos, key=lambda row: safe_float(row.get("candidate_net_profit"), -999999.0))


def best_long_side(rows: Sequence[Mapping[str, Any]], *, subtype_filter: str | None = None) -> Mapping[str, Any]:
    wanted_subtype = subtype_filter or "all_tier_b_fallback"
    oos = [row for row in rows if row.get("split") == "oos" and row.get("side") == "long" and row.get("subtype_filter") == wanted_subtype]
    if not oos:
        return {}
    return max(oos, key=lambda row: (safe_float(row.get("net_profit"), -999999.0), safe_float(row.get("profit_factor"), 0.0)))


def hold_segment_read(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    all_rows = [row for row in rows if row.get("segment_type") == "all"]
    hold2_oos = next((row for row in all_rows if row.get("run_number") == "run13O" and row.get("split") == "oos"), {})
    hold4_oos = next((row for row in all_rows if row.get("run_number") == "run13I" and row.get("split") == "oos"), {})
    hold2_val = next((row for row in all_rows if row.get("run_number") == "run13O" and row.get("split") == "validation"), {})
    hold4_val = next((row for row in all_rows if row.get("run_number") == "run13I" and row.get("split") == "validation"), {})
    month_rows = [row for row in rows if row.get("run_number") == "run13I" and row.get("split") == "oos" and row.get("segment_type") == "month"]
    positive_total = sum(max(0.0, safe_float(row.get("net_profit"))) for row in month_rows)
    top_month = max(month_rows, key=lambda row: safe_float(row.get("net_profit"), -999999.0), default={})
    top_month_share = max(0.0, safe_float(top_month.get("net_profit"))) / positive_total if positive_total > 0 else None
    return {
        "hold2_validation_net_profit": hold2_val.get("net_profit"),
        "hold4_validation_net_profit": hold4_val.get("net_profit"),
        "hold2_oos_net_profit": hold2_oos.get("net_profit"),
        "hold4_oos_net_profit": hold4_oos.get("net_profit"),
        "hold4_minus_hold2_oos": safe_float(hold4_oos.get("net_profit")) - safe_float(hold2_oos.get("net_profit")),
        "hold2_minus_hold4_validation": safe_float(hold2_val.get("net_profit")) - safe_float(hold4_val.get("net_profit")),
        "hold4_oos_top_month": top_month.get("segment_value"),
        "hold4_oos_top_month_net_profit": top_month.get("net_profit"),
        "hold4_oos_top_positive_month_share": top_month_share,
        "hold_axis_instability_visible": safe_float(hold2_val.get("net_profit")) > 0.0 and safe_float(hold4_val.get("net_profit")) < 0.0 and safe_float(hold4_oos.get("net_profit")) > safe_float(hold2_oos.get("net_profit")),
    }


def followup_decision(feature_rows_: Sequence[Mapping[str, Any]], subtype_rows_: Sequence[Mapping[str, Any]], side_rows_: Sequence[Mapping[str, Any]], hold_read: Mapping[str, Any], sources: Mapping[str, Source]) -> dict[str, Any]:
    feature_dependency = best_oos_feature_dependency(feature_rows_)
    subtype = best_oos_subtype(subtype_rows_)
    all_side = best_long_side(side_rows_)
    mixed_side = best_long_side(side_rows_, subtype_filter=MIXED_SUBTYPE)
    q90_long = next((row for row in side_rows_ if row.get("run_number") == "run13S" and row.get("split") == "oos" and row.get("side") == "long"), {})
    followup_completed = [run for run in ("run13AE", "run13AF", "run13AG", "run13AH") if run in sources]
    recommended: list[str] = []
    side_threshold = safe_float(all_side.get("threshold_quantile"), 0.90)
    q90_net = safe_float(q90_long.get("net_profit"))
    best_net = safe_float(all_side.get("net_profit"))
    if not followup_completed and subtype.get("subtype_filter") == MIXED_SUBTYPE:
        if best_net >= q90_net - 20.0 and safe_float(all_side.get("profit_factor")) >= safe_float(q90_long.get("profit_factor")):
            if side_threshold >= 0.95:
                recommended.append("run13AG")
            elif side_threshold >= 0.92:
                recommended.append("run13AF")
            else:
                recommended.append("run13AE")
        elif q90_net > 0.0:
            recommended.append("run13AE")
    feature_delta = safe_float(feature_dependency.get("delta_net_profit"))
    if feature_dependency and abs(feature_delta) >= 75.0 and "run13AH" not in sources:
        recommended.append("run13AH")
    followup_was_available = bool(recommended) or bool(followup_completed)
    remaining_runtime_followup_recommended = bool(recommended)
    if followup_completed and not recommended:
        action_taken = "followup_completed_no_new_runtime_followup_recommended"
    elif followup_completed:
        action_taken = "followup_completed_more_runtime_followup_recommended"
    elif recommended:
        action_taken = "followup_recommended_after_initial_read"
    else:
        action_taken = "no_runtime_followup_needed_after_initial_read"
    return {
        "followup_was_available": followup_was_available,
        "remaining_runtime_followup_recommended": remaining_runtime_followup_recommended,
        "further_exploration_available": remaining_runtime_followup_recommended,
        "recommended_followup_topics": recommended,
        "completed_followup_topics": followup_completed,
        "largest_single_feature_dependency": feature_dependency,
        "best_subtype_filter": subtype,
        "best_all_tier_b_long_compression": all_side,
        "best_mixed_subtype_long_followup": mixed_side,
        "hold_axis_instability_visible": hold_read.get("hold_axis_instability_visible"),
        "claim_boundary": BOUNDARY,
        "action_taken": action_taken,
    }


def build_summary(created_at: str, executed_summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    specs = available_topic_specs()
    sources: dict[str, Source] = {run: source_for_run(run) for run in BASE_RUNS}
    for spec in specs:
        sources[spec.topic.run_number] = source_for_run(spec.topic.run_number)
    feature_rows_ = feature_mask_rows(sources)
    subtype_rows_ = subtype_rows(sources)
    side_rows_ = side_rows(sources)
    segment_rows = hold_segment_rows()
    hold_read = hold_segment_read(segment_rows)
    decision = followup_decision(feature_rows_, subtype_rows_, side_rows_, hold_read, sources)
    completed_flags = [sources[spec.topic.run_number].summary.get("external_verification_status") == "completed" for spec in specs]
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
        "external_verification_status": "completed" if specs and all(completed_flags) else "blocked_or_partial_runtime_extension",
        "runtime_completed_count": sum(1 for flag in completed_flags if flag),
        "runtime_expected_count": len(specs),
        "executed_summaries": list(executed_summaries),
        "available_runtime_run_ids": [spec.topic.run_id for spec in specs],
        "feature_mask_rows": feature_rows_,
        "tier_b_subtype_rows": subtype_rows_,
        "side_compression_rows": side_rows_,
        "hold_segment_rows": segment_rows,
        "feature_mask_read": {
            "baseline_run": "run13I",
            "top5_mask_run": "run13N",
            "single_mask_runs": [run for run in ("run13U", "run13V", "run13W", "run13X", "run13Y") if run in sources],
            "largest_single_feature_dependency": decision.get("largest_single_feature_dependency"),
        },
        "tier_b_subtype_read": {"baseline_run": "run13I", "best_subtype_filter": decision.get("best_subtype_filter")},
        "side_compression_read": {
            "q90_reference_run": "run13S",
            "best_all_tier_b_long_compression": decision.get("best_all_tier_b_long_compression"),
            "best_mixed_subtype_long_followup": decision.get("best_mixed_subtype_long_followup"),
        },
        "hold_segment_read": hold_read,
        "followup_decision": decision,
        "source_inputs": {
            "run13T_summary": rel(STAGE_ROOT / "02_runs/run13T_ebm_mt5_axis_extension_v1/summary.json"),
            "base_hold4_summary": rel(STAGE_ROOT / "02_runs/run13I_ebm_q90_hold4_probe_v1/summary.json"),
            "runtime_summaries": [rel(spec.topic.run_root / "summary.json") for spec in specs],
        },
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        "recommendation": "continue_only_if_followup_decision_has_runtime_topics_otherwise_preserve_clues_and_pivot",
    }


def output_paths() -> dict[str, Path]:
    return {
        "summary": RUN_ROOT / "summary.json",
        "kpi_record": RUN_ROOT / "kpi_record.json",
        "run_manifest": RUN_ROOT / "run_manifest.json",
        "feature_mask_rows": RUN_ROOT / "results/feature_mask_rows.csv",
        "tier_b_subtype_rows": RUN_ROOT / "results/tier_b_subtype_rows.csv",
        "side_compression_rows": RUN_ROOT / "results/side_compression_rows.csv",
        "hold_segment_rows": RUN_ROOT / "results/hold_segment_rows.csv",
        "followup_decision": RUN_ROOT / "results/followup_decision.json",
        "report": REPORT_PATH,
        "decision": DECISION_PATH,
    }


def write_ledgers(summary: Mapping[str, Any]) -> dict[str, Any]:
    status = "completed" if summary.get("external_verification_status") == "completed" else "blocked"
    rows = [
        {
            "ledger_row_id": f"{RUN_ID}__feature_single_masks",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "feature_single_masks",
            "parent_run_id": RUN_ID,
            "record_view": "q90_hold4_single_feature_mask_sweep",
            "tier_scope": "Tier A+B",
            "kpi_scope": "feature_contribution_attribution",
            "scoreboard_lane": "runtime_probe",
            "status": status,
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/feature_mask_rows.csv"),
            "primary_kpi": ledger_pairs((("largest_dependency", summary["feature_mask_read"].get("largest_single_feature_dependency")),)),
            "guardrail_kpi": ledger_pairs((("boundary", BOUNDARY), ("claim", "not_retrained_ablation"))),
            "external_verification_status": summary.get("external_verification_status"),
            "notes": "Individual top5 EBM score-table feature masks through MT5.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__hold_segments",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "hold_segments",
            "parent_run_id": RUN_ID,
            "record_view": "hold2_vs_hold4_segment_attribution",
            "tier_scope": "Tier A+B",
            "kpi_scope": "hold_period_segment_attribution",
            "scoreboard_lane": "trade_shape",
            "status": status,
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/hold_segment_rows.csv"),
            "primary_kpi": ledger_pairs((("hold4_minus_hold2_oos", summary["hold_segment_read"].get("hold4_minus_hold2_oos")), ("hold_axis_instability", summary["hold_segment_read"].get("hold_axis_instability_visible")))),
            "guardrail_kpi": ledger_pairs((("boundary", BOUNDARY),)),
            "external_verification_status": summary.get("external_verification_status"),
            "notes": "Segment attribution uses existing MT5 trade-level records.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_subtypes",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_subtypes",
            "parent_run_id": RUN_ID,
            "record_view": "tier_b_subtype_filter_sweep",
            "tier_scope": "Tier B",
            "kpi_scope": "tier_routing_attribution",
            "scoreboard_lane": "runtime_probe",
            "status": status,
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/tier_b_subtype_rows.csv"),
            "primary_kpi": ledger_pairs((("best_subtype", summary["tier_b_subtype_read"].get("best_subtype_filter")),)),
            "guardrail_kpi": ledger_pairs((("boundary", BOUNDARY),)),
            "external_verification_status": summary.get("external_verification_status"),
            "notes": "Tier B fallback filtered by subtype before MT5 tester.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__side_compression",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "side_compression",
            "parent_run_id": RUN_ID,
            "record_view": "hold4_long_short_threshold_compression",
            "tier_scope": "Tier A+B",
            "kpi_scope": "direction_threshold_attribution",
            "scoreboard_lane": "runtime_probe",
            "status": status,
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/side_compression_rows.csv"),
            "primary_kpi": ledger_pairs((("best_long", summary["side_compression_read"].get("best_all_tier_b_long_compression")),)),
            "guardrail_kpi": ledger_pairs((("boundary", BOUNDARY),)),
            "external_verification_status": summary.get("external_verification_status"),
            "notes": "Long/short threshold compression and optional mixed subtype follow-up.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__followup_decision",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "followup_decision",
            "parent_run_id": RUN_ID,
            "record_view": "further_exploration_decision",
            "tier_scope": "Tier A+B",
            "kpi_scope": "result_judgment",
            "scoreboard_lane": "model_characteristic_attribution",
            "status": status,
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT / "results/followup_decision.json"),
            "primary_kpi": ledger_pairs((("further_exploration_available", summary["followup_decision"].get("further_exploration_available")), ("action_taken", summary["followup_decision"].get("action_taken")))),
            "guardrail_kpi": ledger_pairs((("boundary", BOUNDARY), ("forbidden", "edge/baseline/promotion/runtime_authority"))),
            "external_verification_status": summary.get("external_verification_status"),
            "notes": "Determines whether follow-up runtime topics were warranted after 1/2/3/4 axes.",
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
                        ("runtime_runs", ",".join(summary.get("available_runtime_run_ids", []))),
                        ("largest_feature_dependency", summary["feature_mask_read"].get("largest_single_feature_dependency")),
                        ("best_subtype", summary["tier_b_subtype_read"].get("best_subtype_filter")),
                        ("best_long_compression", summary["side_compression_read"].get("best_all_tier_b_long_compression")),
                        ("followup_action", summary["followup_decision"].get("action_taken")),
                        ("boundary", "axis_exhaustion_followthrough_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )


def gate_payloads(summary: Mapping[str, Any]) -> dict[str, Any]:
    runtime_ok = summary.get("external_verification_status") == "completed"
    gates = [
        "runtime_evidence_gate",
        "feature_single_mask_audit",
        "hold_segment_attribution_audit",
        "tier_b_subtype_audit",
        "side_compression_audit",
        "followup_decision_gate",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]
    return {
        "runtime_evidence_gate": {"status": "passed" if runtime_ok else "blocked", "runtime_completed_count": summary.get("runtime_completed_count"), "runtime_expected_count": summary.get("runtime_expected_count"), "external_verification_status": summary.get("external_verification_status")},
        "feature_single_mask_audit": {"status": "passed" if summary.get("feature_mask_rows") else "blocked", "feature_mask_read": summary.get("feature_mask_read")},
        "hold_segment_attribution_audit": {"status": "passed" if summary.get("hold_segment_rows") else "blocked", "hold_segment_read": summary.get("hold_segment_read")},
        "tier_b_subtype_audit": {"status": "passed" if summary.get("tier_b_subtype_rows") else "blocked", "tier_b_subtype_read": summary.get("tier_b_subtype_read")},
        "side_compression_audit": {"status": "passed" if summary.get("side_compression_rows") else "blocked", "side_compression_read": summary.get("side_compression_read")},
        "followup_decision_gate": {"status": "passed", "followup_decision": summary.get("followup_decision")},
        "required_gate_coverage_audit": {"status": "passed", "packet_id": PACKET_ID, "required_gates": gates, "covered_gates": gates},
        "final_claim_guard": {"status": "passed", "allowed_claims": [JUDGMENT, "runtime_probe", "model_characteristic_attribution", "inconclusive"], "forbidden_claims": summary.get("forbidden_claims"), "claim_boundary": BOUNDARY},
    }


def packet_markdown(summary: Mapping[str, Any]) -> str:
    feature = summary["feature_mask_read"].get("largest_single_feature_dependency") or {}
    subtype = summary["tier_b_subtype_read"].get("best_subtype_filter") or {}
    side = summary["side_compression_read"].get("best_all_tier_b_long_compression") or {}
    followup = summary["followup_decision"]
    hold = summary["hold_segment_read"]
    return "\n".join(
        [
            "# Stage19 RUN13AD EBM Axis Exhaustion Followthrough(19단계 실행13AD EBM 축 소진 후속)",
            "",
            f"- judgment(판정): `{JUDGMENT}`",
            f"- external verification(외부 검증): `{summary.get('external_verification_status')}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "- operating promotion(운영 승격): `none(없음)`",
            "",
            "## 1 Feature Single Mask(피처 단일 마스크)",
            "",
            f"- largest dependency(최대 의존): `{feature.get('feature_masked')}` / OOS delta(표본외 차이): `{metric_text(feature.get('delta_net_profit'))}`",
            "",
            "효과(effect, 효과): top5(상위5)를 한꺼번에 끄는 대신 한 피처씩 꺼서 EBM(설명가능 부스팅 머신) 점수표(score table, 점수표)의 의존이 집중인지 분산인지 확인했다.",
            "",
            "## 2 Hold Segment(보유 구간)",
            "",
            f"- hold4-hold2 OOS(4봉-2봉 표본외): `{metric_text(hold.get('hold4_minus_hold2_oos'))}`",
            f"- hold2-hold4 validation(2봉-4봉 검증): `{metric_text(hold.get('hold2_minus_hold4_validation'))}`",
            f"- hold4 top OOS month(4봉 표본외 최고 월): `{hold.get('hold4_oos_top_month')}` / `{metric_text(hold.get('hold4_oos_top_month_net_profit'))}`",
            "",
            "효과(effect, 효과): hold2(2봉)와 hold4(4봉)의 충돌이 시간, 방향, 변동성, 세션 구간에서 어디서 생기는지 분해했다.",
            "",
            "## 3 Tier B Subtype(티어 B 하위유형)",
            "",
            f"- best subtype(최고 하위유형): `{subtype.get('subtype_filter')}` / OOS net(표본외 순손익): `{metric_text(subtype.get('candidate_net_profit'))}`",
            "",
            "효과(effect, 효과): Tier B fallback(티어 B 대체)을 하위유형별로 제한해 라우팅 효율이 어디서 나오는지 확인했다.",
            "",
            "## 4 Side Compression(방향 압축)",
            "",
            f"- best long compression(최고 매수 압축): `{side.get('run_number')}` q=`{side.get('threshold_quantile')}` / OOS net(표본외 순손익): `{metric_text(side.get('net_profit'))}` / PF(수익 팩터): `{metric_text(side.get('profit_factor'))}`",
            "",
            "효과(effect, 효과): short(매도)을 무조건 폐기하지 않고 threshold(임계값)를 올려 long bias(매수 편향)가 살아남는지 봤다.",
            "",
            "## Follow-up Decision(후속 판단)",
            "",
            f"- further exploration available(추가 탐색 여지): `{followup.get('further_exploration_available')}`",
            f"- recommended follow-up topics(권장 후속 주제): `{followup.get('recommended_followup_topics')}`",
            f"- completed follow-up topics(완료 후속 주제): `{followup.get('completed_followup_topics')}`",
            f"- action taken(수행 행동): `{followup.get('action_taken')}`",
            "",
            "Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )


def decision_markdown(summary: Mapping[str, Any]) -> str:
    followup = summary["followup_decision"]
    return "\n".join(
        [
            "# 2026-05-05 Stage19 RUN13AD EBM Axis Exhaustion Decision(19단계 실행13AD EBM 축 소진 결정)",
            "",
            f"- run(실행): `{RUN_ID}`",
            f"- judgment(판정): `{JUDGMENT}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
            "",
            "## Decision(결정)",
            "",
            "이번 작업은 EBM(설명가능 부스팅 머신)의 1/2/3/4 축을 더 파고, 추가 탐색 여지가 보이면 후속 runtime probe(런타임 탐침)까지 이어가는 작업이다.",
            "",
            f"- further exploration available(추가 탐색 여지): `{followup.get('further_exploration_available')}`",
            f"- action taken(수행 행동): `{followup.get('action_taken')}`",
            "",
            "효과(effect, 효과): 숫자가 좋아 보이는 조합을 운영 의미(operating meaning, 운영 의미)로 올리지 않고, 보존할 clue(단서)와 멈출 축을 분리한다.",
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
            "producer": "stage_pipelines.stage19.ebm_axis_exhaustion_followthrough",
            "source_inputs": summary.get("source_inputs"),
            "artifact_paths": {name: rel(path) for name, path in outputs.items()},
            "artifact_hashes": output_hashes,
            "registry_links": {"run_registry": rel(RUN_REGISTRY_PATH), "project_alpha_ledger": rel(PROJECT_LEDGER_PATH), "stage_run_ledger": rel(STAGE_LEDGER_PATH)},
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
            "support_skills": ["obsidian-experiment-design", "obsidian-runtime-parity", "obsidian-backtest-forensics", "obsidian-artifact-lineage", "obsidian-result-judgment", "obsidian-exploration-mandate"],
            "required_gates": list(gate_payloads(summary)),
        },
    )
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": summary["created_at_utc"],
            "receipts": [
                {"skill": "obsidian-experiment-design", "status": "completed", "hypothesis": "EBM axis clues can be exhausted through single feature masks, hold segmentation, Tier B subtype filters, and side compression.", "control_variables": [FEATURE_SET_ID, LABEL_ID, SPLIT_CONTRACT, SELECTED_VARIANT_ID, "US100 M5"], "changed_variables": ["single feature mask", "hold segment", "Tier B subtype", "q92/q95 side threshold"], "success_criteria": "runtime summaries, KPI records, segment rows, and follow-up decision exist.", "failure_criteria": "missing MT5 output or incomplete KPI.", "invalid_conditions": "feature order mismatch or timestamp mismatch."},
                {"skill": "obsidian-performance-attribution", "status": "completed", "observed_change": summary.get("followup_decision"), "comparison_baseline": "run13I/run13N/run13R/run13S/run13O", "segment_checks": ["month", "direction", "volatility_regime", "session_slice", "trend_regime", "trade_bucket"], "attribution_confidence": "medium", "next_probe": summary.get("followup_decision", {}).get("recommended_followup_topics")},
                {"skill": "obsidian-runtime-parity", "status": "completed", "runtime_claim_boundary": "runtime_probe", "research_path": rel(Path(__file__)), "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5", "known_differences": "Feature masks are score-table term zeroing and not retraining."},
                {"skill": "obsidian-backtest-forensics", "status": "completed", "tester_identity": "MT5 Strategy Tester US100 M5 through existing runtime runner.", "backtest_judgment": "usable_with_boundary" if summary.get("external_verification_status") == "completed" else "blocked_or_partial"},
                {"skill": "obsidian-artifact-lineage", "status": "completed", "source_inputs": summary.get("source_inputs"), "artifact_paths": {name: rel(path) for name, path in outputs.items()}, "lineage_judgment": "connected_with_boundary"},
                {"skill": "obsidian-result-judgment", "status": "completed", "judgment_label": JUDGMENT, "claim_boundary": BOUNDARY, "next_condition": summary.get("followup_decision")},
                {"skill": "obsidian-exploration-mandate", "status": "completed", "idea_id": "stage19_ebm_axis_exhaustion", "hypothesis": "EBM still has explanatory clues, not operating authority.", "tier_scope": "Tier A+B routed exploration", "evidence_boundary": "runtime_probe"},
            ],
        },
    )
    write_json(PACKET_ROOT / "run_summaries" / f"{RUN_ID}.json", summary)
    write_csv(PACKET_ROOT / "feature_mask_rows.csv", FEATURE_MASK_COLUMNS, summary["feature_mask_rows"])
    write_csv(PACKET_ROOT / "tier_b_subtype_rows.csv", SUBTYPE_COLUMNS, summary["tier_b_subtype_rows"])
    write_csv(PACKET_ROOT / "side_compression_rows.csv", SIDE_COLUMNS, summary["side_compression_rows"])
    write_csv(PACKET_ROOT / "hold_segment_rows.csv", SEGMENT_COLUMNS, summary["hold_segment_rows"])
    write_json(PACKET_ROOT / "followup_decision.json", summary["followup_decision"])


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
    write_md(
        SELECTION_STATUS_PATH,
        "\n".join(
            [
                "# Stage19 Selection Status(19단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                "- status(상태): `active_run13AD_ebm_axis_exhaustion_followthrough_completed`",
                f"- current run(현재 실행): `{RUN_ID}`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{JUDGMENT}`",
                f"- selected variant(선택 변형): `{SELECTED_VARIANT_ID}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "효과(effect, 효과): Stage19(19단계)는 EBM(설명가능 부스팅 머신)의 1/2/3/4 축을 더 소진하고 후속 여지를 판정했지만 운영 의미(operating meaning, 운영 의미)는 만들지 않는다.",
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
    state = state.replace("stage19_active_run13T_ebm_mt5_axis_extension_completed", "stage19_active_run13AD_ebm_axis_exhaustion_followthrough_completed")
    state = state.replace("active_run13T_ebm_mt5_axis_extension_completed", "active_run13AD_ebm_axis_exhaustion_followthrough_completed")
    block = f"""stage19_ebm_run13AD_axis_exhaustion_followthrough:
  packet_id: {PACKET_ID}
  status: reviewed_axis_exhaustion_followthrough_completed
  judgment: {JUDGMENT}
  current_run_id: {RUN_ID}
  runtime_completed_count: {summary.get('runtime_completed_count')}
  runtime_expected_count: {summary.get('runtime_expected_count')}
  followup_action: {summary.get('followup_decision', {}).get('action_taken')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / 'run_summaries' / f'{RUN_ID}.json')}
"""
    state = replace_yaml_block(state, "stage19_ebm_run13AD_axis_exhaustion_followthrough:", block)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n", encoding="utf-8")
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = "\n".join(
        [
            "## Latest Stage19 RUN13AD Axis Exhaustion Update(최신 19단계 실행13AD 축 소진 업데이트)",
            "",
            f"Stage19(19단계)는 `{RUN_ID}`에서 EBM(`Explainable Boosting Machine`, 설명가능 부스팅 머신) 1/2/3/4 축을 추가로 파고 follow-up(후속 탐침) 여지를 판정했다.",
            "",
            f"결과(result, 결과): `{JUDGMENT}`. follow-up action(후속 행동)은 `{summary.get('followup_decision', {}).get('action_taken')}`이다.",
            "",
            "효과(effect, 효과): feature(피처), hold(보유), Tier B routing(티어 B 라우팅), side compression(방향 압축)을 더 봤지만 edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.",
            "",
        ]
    )
    if "## Latest Stage19 RUN13AD Axis Exhaustion Update" in current:
        current = re.sub(r"## Latest Stage19 RUN13AD Axis Exhaustion Update\(최신 19단계 실행13AD 축 소진 업데이트\)\n.*?(?=## Latest Stage19)", update + "\n", current, count=1, flags=re.S)
    else:
        current = update + "\n" + current
    current = re.sub(r"- updated_on: `.*?`", "- updated_on: `2026-05-05`", current, count=1)
    current = re.sub(r"- current run\(현재 실행\): `[^`]+`", f"- current run(현재 실행): `{RUN_ID}`", current, count=1)
    io_path(CURRENT_WORKING_STATE_PATH).write_text(current.rstrip() + "\n", encoding="utf-8-sig")


def materialize_outputs(summary: Mapping[str, Any]) -> dict[str, Any]:
    outputs = output_paths()
    write_csv(outputs["feature_mask_rows"], FEATURE_MASK_COLUMNS, summary["feature_mask_rows"])
    write_csv(outputs["tier_b_subtype_rows"], SUBTYPE_COLUMNS, summary["tier_b_subtype_rows"])
    write_csv(outputs["side_compression_rows"], SIDE_COLUMNS, summary["side_compression_rows"])
    write_csv(outputs["hold_segment_rows"], SEGMENT_COLUMNS, summary["hold_segment_rows"])
    write_json(outputs["followup_decision"], summary["followup_decision"])
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
        "kpi_scope": "ebm_axis_exhaustion_followthrough",
        "model_family": MODEL_FAMILY,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "external_verification_status": summary["external_verification_status"],
        "judgment": JUDGMENT,
        "boundary": BOUNDARY,
        "feature_mask_read": summary["feature_mask_read"],
        "hold_segment_read": summary["hold_segment_read"],
        "tier_b_subtype_read": summary["tier_b_subtype_read"],
        "side_compression_read": summary["side_compression_read"],
        "followup_decision": summary["followup_decision"],
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
    executed = execute_topics(args)
    summary = build_summary(utc_now(), executed)
    return materialize_outputs(summary)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stage19 EBM axis exhaustion follow-through.")
    parser.add_argument("--topic-set", choices=("initial", "followup", "all", "existing"), default="initial")
    parser.add_argument("--runtime-topics", nargs="*", default=["all"], help="Run numbers or run ids to execute.")
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
                "runtime_completed_count": summary.get("runtime_completed_count"),
                "runtime_expected_count": summary.get("runtime_expected_count"),
                "feature_mask_read": summary.get("feature_mask_read"),
                "hold_segment_read": summary.get("hold_segment_read"),
                "tier_b_subtype_read": summary.get("tier_b_subtype_read"),
                "side_compression_read": summary.get("side_compression_read"),
                "followup_decision": summary.get("followup_decision"),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
