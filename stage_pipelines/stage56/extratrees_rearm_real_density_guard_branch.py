from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50AS"
PARENT_RUN_ID = "run50AS_stage56_extratrees_rearm_real_density_guard_v1"
PACKET_ID = "stage56_run50AS_extratrees_rearm_real_density_guard_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ExtraTreesRearmRealDensityGuard"
RUN_ROOT = batch.STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = batch.REVIEWS_ROOT / "run50AS_reopen_batch.md"
RESULTS_CSV_PATH = batch.REVIEWS_ROOT / "run50AS_summary.csv"
AUDIT_CSV_PATH = batch.REVIEWS_ROOT / "run50AS_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    group: str,
    *,
    max_hold_bars: int = 6,
    rearm_delta: float = 0.0,
    tier_a_short_threshold: float = 0.260,
    tier_a_long_threshold: float = 0.170,
    routed_fallback_enabled: bool = False,
    notes: str,
) -> batch.ModelAxisVariant:
    rearm_tag = f"r{int(round(rearm_delta * 1000)):03d}"
    threshold_tag = f"s{int(round(tier_a_short_threshold * 1000)):03d}l{int(round(tier_a_long_threshold * 1000)):03d}"
    return batch.ModelAxisVariant(
        variant_id=variant_id,
        base_id=f"et40h{max_hold_bars}_{threshold_tag}_{rearm_tag}",
        group=group,
        model_spec_id=f"extratrees_leaf40_n360_{threshold_tag}",
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
        side_filter_id="et40_s25_entry_rearm_guard",
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
        min_samples_leaf=40,
        max_features="sqrt",
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "et40h6_tr_a",
        "strict_transition_gate_aonly",
        rearm_delta=0.0,
        notes="run50AR et40s25_c0_h6_a with strict same-signal transition block; tests real density without confidence rearm",
    ),
    _variant(
        "et40h6_r015_a",
        "confidence_rearm_guard_aonly",
        rearm_delta=0.015,
        notes="run50AR et40s25_c0_h6_a with 0.015 confidence pulse rearm; tests whether density can survive without pure split re-entry",
    ),
    _variant(
        "et40h6_r030_a",
        "confidence_rearm_guard_aonly",
        rearm_delta=0.030,
        notes="run50AR et40s25_c0_h6_a with 0.030 confidence pulse rearm; balanced guard against same-move split trading",
    ),
    _variant(
        "et40h6_r050_a",
        "confidence_rearm_guard_aonly",
        rearm_delta=0.050,
        notes="run50AR et40s25_c0_h6_a with stricter 0.050 confidence pulse rearm; quality-pressure branch",
    ),
    _variant(
        "et40h6_r030_s24l15_a",
        "transition_guard_density_recovery_aonly",
        rearm_delta=0.030,
        tier_a_short_threshold=0.240,
        tier_a_long_threshold=0.150,
        notes="0.030 rearm with slightly lower thresholds to recover transition-gated density without returning to same-signal splitting",
    ),
    _variant(
        "et40h8_r030_a",
        "hold8_transition_guard_aonly",
        max_hold_bars=8,
        rearm_delta=0.030,
        notes="hold8 control with 0.030 confidence rearm to test whether longer lifecycle reduces split re-entry pressure",
    ),
    _variant(
        "et40h6_r030_b",
        "tier_b_damage_control_comparison",
        rearm_delta=0.030,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for the 0.030 rearm branch; Tier B remains suspect and must not create hidden OOS damage",
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
