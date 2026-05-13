from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50Y"
PARENT_RUN_ID = "run50Y_stage56_buy_side_firewall_tierb_v1"
PACKET_ID = "stage56_run50Y_buy_side_firewall_tierb_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__BuySideFirewallTierB"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50Y_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50Y_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50Y_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

HISTORICAL_VOL_20_FEATURE_INDEX = 32
ADX_14_FEATURE_INDEX = 34
VOL_LOW_MAX = 0.19637160003185267


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    *,
    feature_index: int,
    side_filter_id: str,
    routed_fallback_enabled: bool,
    block_short: bool,
    short_min: float,
    short_max: float,
    block_long: bool,
    long_min: float,
    long_max: float,
    reentry_cooldown_bars: int = 3,
    notes: str,
) -> batch.ModelAxisVariant:
    return batch.ModelAxisVariant(
        variant_id,
        base_id,
        group,
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        short_threshold,
        long_threshold,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        routed_fallback_enabled,
        reentry_cooldown_bars=reentry_cooldown_bars,
        side_filter_id=side_filter_id,
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=feature_index,
        tier_b_side_filter_feature_index=feature_index,
        block_short_feature_range=block_short,
        block_short_feature_min=short_min,
        block_short_feature_max=short_max,
        block_long_feature_range=block_long,
        block_long_feature_min=long_min,
        block_long_feature_max=long_max,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
    )


def _adx_variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    *,
    routed_fallback_enabled: bool,
    reentry_cooldown_bars: int = 3,
    notes: str,
) -> batch.ModelAxisVariant:
    return _variant(
        variant_id,
        base_id,
        group,
        short_threshold,
        long_threshold,
        feature_index=ADX_14_FEATURE_INDEX,
        side_filter_id="buy_adx20plus_short2030_firewall",
        routed_fallback_enabled=routed_fallback_enabled,
        block_short=True,
        short_min=20.0,
        short_max=30.0,
        block_long=True,
        long_min=20.0,
        long_max=1000.0,
        reentry_cooldown_bars=reentry_cooldown_bars,
        notes=notes,
    )


def _vol_variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    *,
    routed_fallback_enabled: bool,
    reentry_cooldown_bars: int = 3,
    notes: str,
) -> batch.ModelAxisVariant:
    return _variant(
        variant_id,
        base_id,
        group,
        short_threshold,
        long_threshold,
        feature_index=HISTORICAL_VOL_20_FEATURE_INDEX,
        side_filter_id="buy_vol_low_firewall",
        routed_fallback_enabled=routed_fallback_enabled,
        block_short=False,
        short_min=0.0,
        short_max=0.0,
        block_long=True,
        long_min=0.0,
        long_max=VOL_LOW_MAX,
        reentry_cooldown_bars=reentry_cooldown_bars,
        notes=notes,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _adx_variant(
        "nfy_s33l20_c3_adx_a",
        "nfy_s33l20_c3_adx",
        "buy_adx20plus_short2030_aonly",
        0.330,
        0.200,
        routed_fallback_enabled=False,
        notes="run50X closest seed; Tier B disabled; block short ADX 20-30 and buy ADX 20+",
    ),
    _adx_variant(
        "nfy_s31l18_c3_adx_b",
        "nfy_s31l18_c3_adx",
        "buy_adx20plus_short2030_density_tier_b",
        0.310,
        0.180,
        routed_fallback_enabled=True,
        notes="density pressure after buy ADX 20+ firewall with core/mixed Tier B",
    ),
    _adx_variant(
        "nfy_s29l16_c6_adx_b",
        "nfy_s29l16_c6_adx",
        "buy_adx20plus_short2030_cooldown_density_tier_b",
        0.290,
        0.160,
        routed_fallback_enabled=True,
        reentry_cooldown_bars=6,
        notes="stronger cooldown stress after buy ADX 20+ firewall",
    ),
    _vol_variant(
        "nfy_s33l20_c3_lvol_a",
        "nfy_s33l20_c3_lvol",
        "buy_vol_low_aonly",
        0.330,
        0.200,
        routed_fallback_enabled=False,
        notes="run50X closest seed; Tier B disabled; block only buy vol_low and preserve sell vol_low",
    ),
    _vol_variant(
        "nfy_s33l20_c3_lvol_b",
        "nfy_s33l20_c3_lvol",
        "buy_vol_low_tier_b_comparison",
        0.330,
        0.200,
        routed_fallback_enabled=True,
        notes="matched A+B routed comparison for buy vol_low firewall",
    ),
    _vol_variant(
        "nfy_s31l18_c6_lvol_b",
        "nfy_s31l18_c6_lvol",
        "buy_vol_low_cooldown_density_tier_b",
        0.310,
        0.180,
        routed_fallback_enabled=True,
        reentry_cooldown_bars=6,
        notes="density pressure with buy vol_low firewall and stronger cooldown audit",
    ),
)


def main(argv: list[str] | None = None) -> int:
    batch.RUN_NUMBER = RUN_NUMBER
    batch.PARENT_RUN_ID = PARENT_RUN_ID
    batch.PACKET_ID = PACKET_ID
    batch.EXPLORATION_LABEL = EXPLORATION_LABEL
    batch.RUN_ROOT = RUN_ROOT
    batch.REPORT_PATH = REPORT_PATH
    batch.RESULTS_CSV_PATH = RESULTS_CSV_PATH
    batch.AUDIT_CSV_PATH = AUDIT_CSV_PATH
    batch.AGGREGATE_SUMMARY_PATH = AGGREGATE_SUMMARY_PATH
    batch.DEFAULT_VARIANTS = DEFAULT_VARIANTS
    return batch.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
