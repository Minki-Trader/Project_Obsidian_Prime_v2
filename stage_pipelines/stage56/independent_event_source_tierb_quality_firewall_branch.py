from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.mt5_trade_attribution import MarketData  # noqa: E402
from stage_pipelines.stage56 import independent_event_source_route_branch as source  # noqa: E402


RUN_NUMBER = "run50BK"
PARENT_RUN_ID = "run50BK_stage56_s43c02_tierb_quality_firewall_v1"
PACKET_ID = "stage56_run50BK_s43c02_tierb_quality_firewall_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__S43TierBQualityFirewall"
RUN_ROOT = source.STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = source.REVIEWS_ROOT / "run50BK_s43c02_tierb_quality_firewall.md"
RESULTS_CSV_PATH = source.REVIEWS_ROOT / "run50BK_summary.csv"
AUDIT_CSV_PATH = source.REVIEWS_ROOT / "run50BK_audit.csv"
SOURCE_SUMMARY_CSV_PATH = source.REVIEWS_ROOT / "run50BK_source_summary.csv"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_s43c02_tierb_quality_firewall"

S43_C02 = "c02_top8_stability_ranked_elasticnet"
VOL_LOW_EDGE = MarketData.load(REPO_ROOT).volatility_edges[0]


DEFAULT_VARIANTS: tuple[source.SourceVariant, ...] = (
    source.SourceVariant(
        variant_id="s43c02_h4c0_no_b",
        source_stage_number=43,
        source_candidate_id=S43_C02,
        group="stage43_tier_b_disabled_raw_density",
        max_hold_bars=4,
        reentry_cooldown_bars=0,
        routed_fallback_enabled=False,
        notes="Run50BJ s43c02 raw-density route with Tier B disabled after Tier B OOS damage.",
    ),
    source.SourceVariant(
        variant_id="s43c02_h4c2_no_b",
        source_stage_number=43,
        source_candidate_id=S43_C02,
        group="stage43_tier_b_disabled_microcooldown",
        max_hold_bars=4,
        reentry_cooldown_bars=2,
        routed_fallback_enabled=False,
        notes="Cooldown2 interpolation with Tier B disabled; tests same-move reduction without fallback damage.",
    ),
    source.SourceVariant(
        variant_id="s43c02_h4c4_no_b",
        source_stage_number=43,
        source_candidate_id=S43_C02,
        group="stage43_tier_b_disabled_cooldown_stress",
        max_hold_bars=4,
        reentry_cooldown_bars=4,
        routed_fallback_enabled=False,
        notes="Cooldown4 stress with Tier B disabled; tests whether real density survives stronger spacing.",
    ),
    source.SourceVariant(
        variant_id="s43c02_h4c0_no_b_blvl",
        source_stage_number=43,
        source_candidate_id=S43_C02,
        group="stage43_buy_lowvol_late_firewall",
        max_hold_bars=4,
        reentry_cooldown_bars=0,
        routed_fallback_enabled=False,
        notes="Blocks long signals during low historical_vol_20 late session, the largest run50BJ OOS damage bucket; Tier B disabled.",
    ),
    source.SourceVariant(
        variant_id="s43c02_h4c2_no_b_blvl",
        source_stage_number=43,
        source_candidate_id=S43_C02,
        group="stage43_buy_lowvol_late_firewall_microcooldown",
        max_hold_bars=4,
        reentry_cooldown_bars=2,
        routed_fallback_enabled=False,
        notes="Combines buy-low-vol-late firewall with cooldown2 and Tier B disabled.",
    ),
    source.SourceVariant(
        variant_id="s43c02_h4c0_with_b_blvl",
        source_stage_number=43,
        source_candidate_id=S43_C02,
        group="stage43_buy_lowvol_late_firewall_tier_b_audit",
        max_hold_bars=4,
        reentry_cooldown_bars=0,
        routed_fallback_enabled=True,
        notes="Matched filtered route with Tier B enabled to audit whether fallback still creates hidden OOS damage.",
    ),
)

QUALITY_FILTERS = {
    "s43c02_h4c0_no_b_blvl": "block_buy_lowvol_late",
    "s43c02_h4c2_no_b_blvl": "block_buy_lowvol_late",
    "s43c02_h4c0_with_b_blvl": "block_buy_lowvol_late",
}


def _numeric(frame: pd.DataFrame, column: str, fallback: float = 0.0) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(fallback, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan).astype("float64")


def _apply_quality_filter(
    variant: source.SourceVariant,
    frame: pd.DataFrame,
    common: pd.DataFrame,
    topic_signal_column: str,
) -> pd.DataFrame:
    filter_id = QUALITY_FILTERS.get(variant.variant_id, "none")
    out = frame.copy()
    signal = pd.to_numeric(out[topic_signal_column], errors="coerce").fillna(0).astype("int8")
    blocked = pd.Series(False, index=out.index)
    if filter_id == "block_buy_lowvol_late":
        minutes = _numeric(common, "minutes_from_cash_open")
        historical_vol_20 = _numeric(common, "historical_vol_20")
        blocked = signal.eq(1) & historical_vol_20.le(float(VOL_LOW_EDGE)) & minutes.gt(220.0) & minutes.le(330.0)
        signal = signal.mask(blocked, 0)
    out[topic_signal_column] = signal.astype("int8")
    out["entry_decision"] = np.where(signal > 0, "long", np.where(signal < 0, "short", "flat"))
    out["quality_filter_id"] = filter_id
    out["quality_filter_blocked_signal"] = blocked.astype("int8")
    return out


def build_variant_frames(
    variants: Sequence[source.SourceVariant],
    common: pd.DataFrame,
) -> tuple[dict[str, pd.DataFrame], list[dict[str, Any]], dict[int, dict[str, Any]]]:
    context_by_stage: dict[int, dict[str, Any]] = {}
    frames: dict[str, pd.DataFrame] = {}
    python_summary_rows: list[dict[str, Any]] = []
    for variant in variants:
        topic = source.topic_for_variant(variant)
        context = context_by_stage.setdefault(topic.stage_number, source.build_stage_model_context(common, topic))
        spec = source.spec_for_variant(variant)
        frame = source.apply_candidate_to_table(common, topic, spec, context)
        frame = _apply_quality_filter(variant, frame, common, topic.signal_column)
        frame["variant_id"] = variant.variant_id
        frame["source_stage_number"] = variant.source_stage_number
        frame["source_candidate_id"] = variant.source_candidate_id
        frames[variant.variant_id] = frame
        summary = source.summarize_candidate_frames(topic, {variant.source_candidate_id: frame}, [spec])
        for row in summary:
            python_summary_rows.append(
                {
                    **dict(row),
                    "variant_id": variant.variant_id,
                    "source_stage_number": variant.source_stage_number,
                    "source_candidate_id": variant.source_candidate_id,
                    "max_hold_bars": variant.max_hold_bars,
                    "reentry_cooldown_bars": variant.reentry_cooldown_bars,
                    "routed_fallback_enabled": variant.routed_fallback_enabled,
                    "quality_filter_id": QUALITY_FILTERS.get(variant.variant_id, "none"),
                    "quality_filter_blocked_signals": int(frame["quality_filter_blocked_signal"].sum()),
                    "group": variant.group,
                }
            )
    context_manifest = {stage: source.model_context_manifest(context) for stage, context in context_by_stage.items()}
    return frames, python_summary_rows, context_manifest


def main(argv: list[str] | None = None) -> int:
    source.RUN_NUMBER = RUN_NUMBER
    source.PARENT_RUN_ID = PARENT_RUN_ID
    source.PACKET_ID = PACKET_ID
    source.EXPLORATION_LABEL = EXPLORATION_LABEL
    source.RUN_ROOT = RUN_ROOT
    source.REPORT_PATH = REPORT_PATH
    source.RESULTS_CSV_PATH = RESULTS_CSV_PATH
    source.AUDIT_CSV_PATH = AUDIT_CSV_PATH
    source.SOURCE_SUMMARY_CSV_PATH = SOURCE_SUMMARY_CSV_PATH
    source.PACKET_ROOT = PACKET_ROOT
    source.AGGREGATE_SUMMARY_PATH = AGGREGATE_SUMMARY_PATH
    source.COMMON_ROOT = COMMON_ROOT
    source.DEFAULT_VARIANTS = DEFAULT_VARIANTS
    source.build_variant_frames = build_variant_frames
    return source.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
