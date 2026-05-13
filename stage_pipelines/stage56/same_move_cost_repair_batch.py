from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50AA"
PARENT_RUN_ID = "run50AA_stage56_same_move_cost_repair_v1"
PACKET_ID = "stage56_run50AA_same_move_cost_repair_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__SameMoveCostRepair"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50AA_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50AA_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50AA_audit.csv"
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
    block_long_adx_min: float,
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
        side_filter_id="same_move_cost_repair_buy_adx",
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        tier_b_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        block_short_feature_range=True,
        block_short_feature_min=20.0,
        block_short_feature_max=30.0,
        block_long_feature_range=True,
        block_long_feature_min=block_long_adx_min,
        block_long_feature_max=1000.0,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "nfaa_s25l14_c6_l30_a",
        "nfaa_s25l14_c6_l30",
        "cool6_buy_adx30_density_aonly",
        0.250,
        0.140,
        routed_fallback_enabled=False,
        reentry_cooldown_bars=6,
        block_long_adx_min=30.0,
        notes="lower thresholds under cooldown6 and buy ADX below 30 to recover density from run50Z cost-positive branch",
    ),
    _variant(
        "nfaa_s23l13_c6_l30_a",
        "nfaa_s23l13_c6_l30",
        "cool6_buy_adx30_density_aonly",
        0.230,
        0.130,
        routed_fallback_enabled=False,
        reentry_cooldown_bars=6,
        block_long_adx_min=30.0,
        notes="stronger density pressure under cooldown6 and buy ADX below 30",
    ),
    _variant(
        "nfaa_s23l13_c6_l30_b",
        "nfaa_s23l13_c6_l30",
        "cool6_buy_adx30_tier_b_comparison",
        0.230,
        0.130,
        routed_fallback_enabled=True,
        reentry_cooldown_bars=6,
        block_long_adx_min=30.0,
        notes="matched A+B comparison for Tier B disablement under same-move cost repair",
    ),
    _variant(
        "nfaa_s21l12_c6_l30_a",
        "nfaa_s21l12_c6_l30",
        "cool6_buy_adx30_max_density_aonly",
        0.210,
        0.120,
        routed_fallback_enabled=False,
        reentry_cooldown_bars=6,
        block_long_adx_min=30.0,
        notes="maximum density pressure under cooldown6 and buy ADX below 30",
    ),
    _variant(
        "nfaa_s23l13_c5_l30_a",
        "nfaa_s23l13_c5_l30",
        "cool5_buy_adx30_density_aonly",
        0.230,
        0.130,
        routed_fallback_enabled=False,
        reentry_cooldown_bars=5,
        block_long_adx_min=30.0,
        notes="slightly looser cooldown to test density recovery without fully returning same-move split",
    ),
    _variant(
        "nfaa_s23l13_c6_l35_a",
        "nfaa_s23l13_c6_l35",
        "cool6_buy_adx35_density_aonly",
        0.230,
        0.130,
        routed_fallback_enabled=False,
        reentry_cooldown_bars=6,
        block_long_adx_min=35.0,
        notes="allow buy ADX below 35 to recover density while keeping strongest high-ADX block",
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
