from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50Z"
PARENT_RUN_ID = "run50Z_stage56_partial_buy_adx_reintro_v1"
PACKET_ID = "stage56_run50Z_partial_buy_adx_reintro_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__PartialBuyAdxReintro"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50Z_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50Z_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50Z_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    *,
    routed_fallback_enabled: bool,
    reentry_cooldown_bars: int,
    block_long_adx_min: float | None,
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
        side_filter_id="partial_buy_adx_reintro",
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        tier_b_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        block_short_feature_range=True,
        block_short_feature_min=20.0,
        block_short_feature_max=30.0,
        block_long_feature_range=block_long_adx_min is not None,
        block_long_feature_min=0.0 if block_long_adx_min is None else block_long_adx_min,
        block_long_feature_max=0.0 if block_long_adx_min is None else 1000.0,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "nfz_s31l18_c3_s2030_a",
        "nfz_s31l18_c3_s2030",
        "short2030_aonly_density_repair",
        0.310,
        0.180,
        routed_fallback_enabled=False,
        reentry_cooldown_bars=3,
        block_long_adx_min=None,
        notes="A-only density repair after run50Y; keep short ADX 20-30 block and reintroduce all buy ADX",
    ),
    _variant(
        "nfz_s31l18_c3_s2030_b",
        "nfz_s31l18_c3_s2030",
        "short2030_tier_b_comparison",
        0.310,
        0.180,
        routed_fallback_enabled=True,
        reentry_cooldown_bars=3,
        block_long_adx_min=None,
        notes="matched A+B routed comparison for Tier B disablement evidence",
    ),
    _variant(
        "nfz_s30l17_c3_l25_a",
        "nfz_s30l17_c3_l25",
        "partial_buy_adx25_block_aonly",
        0.300,
        0.170,
        routed_fallback_enabled=False,
        reentry_cooldown_bars=3,
        block_long_adx_min=25.0,
        notes="partial buy ADX reintroduction: allow buy ADX below 25 only",
    ),
    _variant(
        "nfz_s29l16_c3_l30_a",
        "nfz_s29l16_c3_l30",
        "partial_buy_adx30_block_aonly",
        0.290,
        0.160,
        routed_fallback_enabled=False,
        reentry_cooldown_bars=3,
        block_long_adx_min=30.0,
        notes="partial buy ADX reintroduction: allow buy ADX below 30",
    ),
    _variant(
        "nfz_s28l15_c3_l35_a",
        "nfz_s28l15_c3_l35",
        "partial_buy_adx35_block_aonly",
        0.280,
        0.150,
        routed_fallback_enabled=False,
        reentry_cooldown_bars=3,
        block_long_adx_min=35.0,
        notes="partial buy ADX reintroduction: allow buy ADX below 35",
    ),
    _variant(
        "nfz_s27l15_c6_l30_a",
        "nfz_s27l15_c6_l30",
        "partial_buy_adx30_cooldown_aonly",
        0.270,
        0.150,
        routed_fallback_enabled=False,
        reentry_cooldown_bars=6,
        block_long_adx_min=30.0,
        notes="density pressure with buy ADX below 30 and stronger cooldown audit",
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
