from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50BM"
PARENT_RUN_ID = "run50BM_stage56_leaf_same_direction_density_pivot_v1"
PACKET_ID = "stage56_run50BM_leaf_same_direction_density_pivot_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__LeafSameDirectionDensityPivot"
RUN_ROOT = batch.STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = batch.REVIEWS_ROOT / "run50BM_leaf_sd_pivot.md"
RESULTS_CSV_PATH = batch.REVIEWS_ROOT / "run50BM_summary.csv"
AUDIT_CSV_PATH = batch.REVIEWS_ROOT / "run50BM_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    group: str,
    *,
    leaf: int,
    short_threshold: float,
    long_threshold: float,
    rearm_delta: float,
    max_hold_bars: int,
    same_direction_cooldown_bars: int,
    notes: str,
) -> batch.ModelAxisVariant:
    threshold_tag = f"s{int(round(short_threshold * 1000)):03d}l{int(round(long_threshold * 1000)):03d}"
    rearm_tag = f"r{int(round(rearm_delta * 1000)):03d}"
    return batch.ModelAxisVariant(
        variant_id=variant_id,
        base_id=f"et{leaf}h{max_hold_bars}sd{same_direction_cooldown_bars}_{threshold_tag}_{rearm_tag}",
        group=group,
        model_spec_id=f"extratrees_leaf{leaf}_n420_{threshold_tag}",
        c_value=0.50,
        class_weight="balanced",
        flat_sample_weight=None,
        nonflat_sample_weight=None,
        train_start_utc=None,
        tier_a_short_threshold=short_threshold,
        tier_a_long_threshold=long_threshold,
        tier_a_min_margin=0.0,
        tier_b_short_threshold=0.450,
        tier_b_long_threshold=0.450,
        tier_b_min_margin=0.0,
        max_hold_bars=max_hold_bars,
        routed_fallback_enabled=False,
        reentry_cooldown_bars=0,
        same_direction_reentry_cooldown_bars=same_direction_cooldown_bars,
        entry_transition_only=True,
        entry_transition_rearm_min_confidence_delta=rearm_delta,
        side_filter_id=f"et{leaf}_leaf_sd_density_guard",
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        tier_b_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        block_short_feature_range=True,
        block_short_feature_min=20.0,
        block_short_feature_max=25.0,
        block_long_feature_range=False,
        block_long_feature_min=0.0,
        block_long_feature_max=0.0,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
        estimator_family="extratrees",
        n_estimators=420,
        min_samples_leaf=leaf,
        max_features="sqrt",
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "et20h6sd2_s240l150_r015_a",
        "leaf20_same_direction_density_recovery_aonly",
        leaf=20,
        short_threshold=0.240,
        long_threshold=0.150,
        rearm_delta=0.015,
        max_hold_bars=6,
        same_direction_cooldown_bars=2,
        notes="run50AT leaf20 source with lower thresholds plus same-direction-only cooldown2; tests density recovery without generic cooldown damage",
    ),
    _variant(
        "et20h6sd2_s220l130_r015_a",
        "leaf20_threshold_expansion_aonly",
        leaf=20,
        short_threshold=0.220,
        long_threshold=0.130,
        rearm_delta=0.015,
        max_hold_bars=6,
        same_direction_cooldown_bars=2,
        notes="leaf20 lower threshold expansion checks whether OOS trades/day can clear five after same-direction cooldown2",
    ),
    _variant(
        "et20h4sd2_s220l130_r015_a",
        "leaf20_hold4_threshold_expansion_aonly",
        leaf=20,
        short_threshold=0.220,
        long_threshold=0.130,
        rearm_delta=0.015,
        max_hold_bars=4,
        same_direction_cooldown_bars=2,
        notes="hold4 variant tests whether shorter lifecycle keeps OOS density above five while preserving leaf20 validation quality",
    ),
    _variant(
        "et30h6sd2_s230l140_r015_a",
        "leaf30_middle_granularity_aonly",
        leaf=30,
        short_threshold=0.230,
        long_threshold=0.140,
        rearm_delta=0.015,
        max_hold_bars=6,
        same_direction_cooldown_bars=2,
        notes="leaf30 middle granularity with same-direction cooldown2; control against leaf20 noise and leaf40 density collapse",
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
