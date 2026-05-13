from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50AT"
PARENT_RUN_ID = "run50AT_stage56_extratrees_leaf_granularity_transition_density_source_v1"
PACKET_ID = "stage56_run50AT_extratrees_leaf_granularity_transition_density_source_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ExtraTreesLeafGranularityTransitionDensitySource"
RUN_ROOT = batch.STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = batch.REVIEWS_ROOT / "run50AT_reopen_batch.md"
RESULTS_CSV_PATH = batch.REVIEWS_ROOT / "run50AT_summary.csv"
AUDIT_CSV_PATH = batch.REVIEWS_ROOT / "run50AT_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    group: str,
    *,
    min_samples_leaf: int,
    rearm_delta: float,
    tier_a_short_threshold: float = 0.260,
    tier_a_long_threshold: float = 0.170,
    routed_fallback_enabled: bool = False,
    n_estimators: int = 420,
    notes: str,
) -> batch.ModelAxisVariant:
    leaf_tag = f"leaf{int(min_samples_leaf):02d}"
    threshold_tag = f"s{int(round(tier_a_short_threshold * 1000)):03d}l{int(round(tier_a_long_threshold * 1000)):03d}"
    rearm_tag = f"r{int(round(rearm_delta * 1000)):03d}"
    return batch.ModelAxisVariant(
        variant_id=variant_id,
        base_id=f"et{int(min_samples_leaf):02d}h6_{threshold_tag}_{rearm_tag}",
        group=group,
        model_spec_id=f"extratrees_{leaf_tag}_n{int(n_estimators)}_{threshold_tag}",
        c_value=0.50,
        class_weight="balanced",
        flat_sample_weight=None,
        nonflat_sample_weight=None,
        train_start_utc=None,
        tier_a_short_threshold=tier_a_short_threshold,
        tier_a_long_threshold=tier_a_long_threshold,
        tier_a_min_margin=0.0,
        tier_b_short_threshold=0.450,
        tier_b_long_threshold=0.450,
        tier_b_min_margin=0.0,
        max_hold_bars=6,
        routed_fallback_enabled=routed_fallback_enabled,
        reentry_cooldown_bars=0,
        entry_transition_only=True,
        entry_transition_rearm_min_confidence_delta=rearm_delta,
        side_filter_id="et_leaf_entry_rearm_guard",
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
        n_estimators=n_estimators,
        min_samples_leaf=min_samples_leaf,
        max_features="sqrt",
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "et20h6_r015_a",
        "leaf20_transition_density_source_aonly",
        min_samples_leaf=20,
        rearm_delta=0.015,
        notes="leaf20 ExtraTrees with run50AS closest-density rearm; tests whether finer tree granularity creates real transition-gated density",
    ),
    _variant(
        "et20h6_r015_b",
        "leaf20_transition_density_source_tier_b_comparison",
        min_samples_leaf=20,
        rearm_delta=0.015,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for leaf20 0.015 rearm; Tier B must not hide OOS damage",
    ),
    _variant(
        "et20h6_r030_a",
        "leaf20_quality_guard_aonly",
        min_samples_leaf=20,
        rearm_delta=0.030,
        notes="leaf20 ExtraTrees with run50AS quality rearm; tests whether finer probability shape keeps PF while adding OOS density",
    ),
    _variant(
        "et20h6_r030_b",
        "leaf20_quality_guard_tier_b_comparison",
        min_samples_leaf=20,
        rearm_delta=0.030,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for leaf20 0.030 rearm; checks Tier B under the quality branch",
    ),
    _variant(
        "et20h6_r030_s24l15_a",
        "leaf20_threshold_recovery_aonly",
        min_samples_leaf=20,
        rearm_delta=0.030,
        tier_a_short_threshold=0.240,
        tier_a_long_threshold=0.150,
        notes="leaf20 0.030 rearm with lower thresholds; tests whether threshold relaxation stops saturating after granularity change",
    ),
    _variant(
        "et30h6_r015_a",
        "leaf30_transition_density_source_aonly",
        min_samples_leaf=30,
        rearm_delta=0.015,
        notes="leaf30 middle granularity with closest-density rearm; checks whether leaf20 is too noisy",
    ),
    _variant(
        "et30h6_r030_a",
        "leaf30_quality_guard_aonly",
        min_samples_leaf=30,
        rearm_delta=0.030,
        notes="leaf30 middle granularity with quality rearm; compares against leaf20 and run50AS leaf40",
    ),
    _variant(
        "et60h6_r015_a",
        "leaf60_smooth_transition_source_aonly",
        min_samples_leaf=60,
        rearm_delta=0.015,
        n_estimators=360,
        notes="leaf60 smoother ExtraTrees branch; tests whether run50AS density loss came from over-fragmented leaf40 decisions",
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
