from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50AF"
PARENT_RUN_ID = "run50AF_stage56_short_adx_repair_after_c08b_v1"
PACKET_ID = "stage56_run50AF_short_adx_repair_after_c08b_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ShortAdxRepairAfterC08B"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50AF_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50AF_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50AF_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    *,
    short_threshold: float,
    long_threshold: float,
    block_short_adx_min: float,
    block_short_adx_max: float,
    reentry_cooldown_bars: int,
    routed_fallback_enabled: bool,
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
        8,
        routed_fallback_enabled,
        reentry_cooldown_bars=reentry_cooldown_bars,
        side_filter_id=f"sadx{int(block_short_adx_min):02d}{int(block_short_adx_max):02d}_c{reentry_cooldown_bars:02d}",
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        tier_b_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        block_short_feature_range=True,
        block_short_feature_min=block_short_adx_min,
        block_short_feature_max=block_short_adx_max,
        block_long_feature_range=False,
        block_long_feature_min=0.0,
        block_long_feature_max=0.0,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "s25c8a",
        "s25c8",
        "short_adx20_25_cooldown8_aonly",
        short_threshold=0.260,
        long_threshold=0.170,
        block_short_adx_min=20.0,
        block_short_adx_max=25.0,
        reentry_cooldown_bars=8,
        routed_fallback_enabled=False,
        notes=(
            "A-only repair probe after run50AE c08b attribution: remove validation sell ADX 20-25 damage "
            "while preserving hold8/cooldown8; single-axis ADX filter does not include buy vol_low firewall"
        ),
    ),
    _variant(
        "s25c8b",
        "s25c8",
        "short_adx20_25_cooldown8_tier_b_comparison",
        short_threshold=0.260,
        long_threshold=0.170,
        block_short_adx_min=20.0,
        block_short_adx_max=25.0,
        reentry_cooldown_bars=8,
        routed_fallback_enabled=True,
        notes="matched A+B routed comparison for short ADX20-25 cooldown8 repair",
    ),
    _variant(
        "s25c6a",
        "s25c6",
        "short_adx20_25_cooldown6_aonly",
        short_threshold=0.260,
        long_threshold=0.170,
        block_short_adx_min=20.0,
        block_short_adx_max=25.0,
        reentry_cooldown_bars=6,
        routed_fallback_enabled=False,
        notes="density pressure with cooldown6 after removing validation sell ADX 20-25 damage; A-only comparison",
    ),
    _variant(
        "s25c6b",
        "s25c6",
        "short_adx20_25_cooldown6_tier_b_comparison",
        short_threshold=0.260,
        long_threshold=0.170,
        block_short_adx_min=20.0,
        block_short_adx_max=25.0,
        reentry_cooldown_bars=6,
        routed_fallback_enabled=True,
        notes="matched A+B routed comparison for cooldown6 density pressure after short ADX20-25 block",
    ),
    _variant(
        "s30c8a",
        "s30c8",
        "short_adx20_30_cooldown8_aonly",
        short_threshold=0.260,
        long_threshold=0.170,
        block_short_adx_min=20.0,
        block_short_adx_max=30.0,
        reentry_cooldown_bars=8,
        routed_fallback_enabled=False,
        notes="wider short ADX20-30 firewall to test whether validation damage extends above 25; A-only comparison",
    ),
    _variant(
        "s30c8b",
        "s30c8",
        "short_adx20_30_cooldown8_tier_b_comparison",
        short_threshold=0.260,
        long_threshold=0.170,
        block_short_adx_min=20.0,
        block_short_adx_max=30.0,
        reentry_cooldown_bars=8,
        routed_fallback_enabled=True,
        notes="matched A+B routed comparison for wider short ADX20-30 firewall",
    ),
    _variant(
        "l16c8a",
        "l16c8",
        "short_adx20_25_lower_long_cooldown8_aonly",
        short_threshold=0.260,
        long_threshold=0.160,
        block_short_adx_min=20.0,
        block_short_adx_max=25.0,
        reentry_cooldown_bars=8,
        routed_fallback_enabled=False,
        notes="recover long-side density after short ADX20-25 repair by lowering long threshold from 0.170 to 0.160",
    ),
    _variant(
        "l16c8b",
        "l16c8",
        "short_adx20_25_lower_long_cooldown8_tier_b_comparison",
        short_threshold=0.260,
        long_threshold=0.160,
        block_short_adx_min=20.0,
        block_short_adx_max=25.0,
        reentry_cooldown_bars=8,
        routed_fallback_enabled=True,
        notes="matched A+B routed comparison for lower-long threshold short ADX20-25 repair",
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
