from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50BH"
PARENT_RUN_ID = "run50BH_stage56_extratrees_light_rearm_density_recovery_v1"
PACKET_ID = "stage56_run50BH_extratrees_light_rearm_density_recovery_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ExtraTreesLightRearmDensityRecovery"
RUN_ROOT = batch.STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = batch.REVIEWS_ROOT / "run50BH_extratrees_light_rearm_density_recovery.md"
RESULTS_CSV_PATH = batch.REVIEWS_ROOT / "run50BH_summary.csv"
AUDIT_CSV_PATH = batch.REVIEWS_ROOT / "run50BH_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    group: str,
    *,
    leaf: int,
    rearm_delta: float,
    max_hold_bars: int = 6,
    tier_a_short_threshold: float = 0.260,
    tier_a_long_threshold: float = 0.170,
    routed_fallback_enabled: bool = False,
    notes: str,
) -> batch.ModelAxisVariant:
    threshold_tag = f"s{int(round(tier_a_short_threshold * 1000)):03d}l{int(round(tier_a_long_threshold * 1000)):03d}"
    rearm_tag = f"r{int(round(rearm_delta * 1000)):03d}"
    return batch.ModelAxisVariant(
        variant_id=variant_id,
        base_id=f"et{leaf}h{max_hold_bars}_{threshold_tag}_{rearm_tag}",
        group=group,
        model_spec_id=f"extratrees_leaf{leaf}_n360_{threshold_tag}",
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
        max_hold_bars=max_hold_bars,
        routed_fallback_enabled=routed_fallback_enabled,
        reentry_cooldown_bars=0,
        entry_transition_only=True,
        entry_transition_rearm_min_confidence_delta=rearm_delta,
        side_filter_id=f"et{leaf}_s25_light_rearm_guard",
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
        n_estimators=360,
        min_samples_leaf=leaf,
        max_features="sqrt",
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "et40h6_r001_a",
        "light_rearm_density_recovery_aonly",
        leaf=40,
        rearm_delta=0.001,
        notes="run50AS leaf40 quality branch with minimal confidence rearm to test density recovery before raw same-move splitting returns",
    ),
    _variant(
        "et40h6_r005_a",
        "light_rearm_density_recovery_aonly",
        leaf=40,
        rearm_delta=0.005,
        notes="run50AS leaf40 quality branch with 0.005 confidence rearm; midpoint between strict transition and run50AS 0.015 rearm",
    ),
    _variant(
        "et40h6_r010_a",
        "light_rearm_density_recovery_aonly",
        leaf=40,
        rearm_delta=0.010,
        notes="run50AS leaf40 quality branch with 0.010 confidence rearm; checks whether OOS density rises without losing cost-stressed expectancy",
    ),
    _variant(
        "et30h6_r001_a",
        "leaf30_light_rearm_density_aonly",
        leaf=30,
        rearm_delta=0.001,
        notes="run50AT leaf30 quality clue with minimal confidence rearm to pressure density while preserving positive OOS cost stress",
    ),
    _variant(
        "et30h6_r005_a",
        "leaf30_light_rearm_density_aonly",
        leaf=30,
        rearm_delta=0.005,
        notes="run50AT leaf30 quality clue with 0.005 confidence rearm for density recovery",
    ),
    _variant(
        "et30h6_r005_b",
        "leaf30_light_rearm_tier_b_damage_check",
        leaf=30,
        rearm_delta=0.005,
        routed_fallback_enabled=True,
        notes="matched Tier B fallback check for the leaf30 0.005 rearm branch; prior Tier B damage remains suspect",
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
