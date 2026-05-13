from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch


RUN_NUMBER = "run50AR"
PARENT_RUN_ID = "run50AR_stage56_extratrees_validation_density_repair_v1"
PACKET_ID = "stage56_run50AR_extratrees_validation_density_repair_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ExtraTreesValidationDensityRepair"
RUN_ROOT = batch.STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = batch.REVIEWS_ROOT / "run50AR_reopen_batch.md"
RESULTS_CSV_PATH = batch.REVIEWS_ROOT / "run50AR_summary.csv"
AUDIT_CSV_PATH = batch.REVIEWS_ROOT / "run50AR_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    group: str,
    *,
    max_hold_bars: int,
    reentry_cooldown_bars: int,
    tier_a_short_threshold: float = 0.260,
    tier_a_long_threshold: float = 0.170,
    routed_fallback_enabled: bool = False,
    block_short_min: float = 20.0,
    block_short_max: float = 25.0,
    block_long: bool = False,
    block_long_min: float = 0.0,
    block_long_max: float = 0.0,
    notes: str,
) -> batch.ModelAxisVariant:
    side_filter_id = (
        f"adx_s{int(block_short_min):02d}_{int(block_short_max):02d}"
        + (f"_l{int(block_long_min):02d}_{int(block_long_max):02d}" if block_long else "")
    )
    return batch.ModelAxisVariant(
        variant_id=variant_id,
        base_id=variant_id,
        group=group,
        model_spec_id=f"extratrees_leaf40_n360_s{int(tier_a_short_threshold * 1000)}l{int(tier_a_long_threshold * 1000)}",
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
        reentry_cooldown_bars=reentry_cooldown_bars,
        side_filter_id=side_filter_id,
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        tier_b_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        block_short_feature_range=True,
        block_short_feature_min=block_short_min,
        block_short_feature_max=block_short_max,
        block_long_feature_range=block_long,
        block_long_feature_min=block_long_min,
        block_long_feature_max=block_long_max,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
        estimator_family="extratrees",
        n_estimators=360,
        min_samples_leaf=40,
        max_features="sqrt",
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "et40s25_c0_h8_a",
        "cooldown_density_repair_aonly",
        max_hold_bars=8,
        reentry_cooldown_bars=0,
        notes="run50AQ et40s25a with cooldown removed to test whether OOS density can recover without losing PF/cost/same-move discipline",
    ),
    _variant(
        "et40s25_c4_h8_a",
        "cooldown_density_repair_aonly",
        max_hold_bars=8,
        reentry_cooldown_bars=4,
        notes="run50AQ et40s25a with half cooldown to test density recovery against same-move split trading",
    ),
    _variant(
        "et40s25_c0_h6_a",
        "hold_compression_density_repair_aonly",
        max_hold_bars=6,
        reentry_cooldown_bars=0,
        notes="hold6 plus no cooldown to stress density; should fail if density comes mainly from split re-entry",
    ),
    _variant(
        "et40s25_c4_h6_a",
        "hold_compression_density_repair_aonly",
        max_hold_bars=6,
        reentry_cooldown_bars=4,
        notes="hold6 plus cooldown4 to compare density and same-move survival against cooldown0",
    ),
    _variant(
        "et40adxweak_c0_h8_a",
        "weak_trend_firewall_quality_repair_aonly",
        max_hold_bars=8,
        reentry_cooldown_bars=0,
        block_short_min=0.0,
        block_short_max=25.0,
        block_long=True,
        block_long_min=0.0,
        block_long_max=20.0,
        notes="block short ADX<=25 and long ADX<20 after run50AQ validation weak-trend damage; cooldown0 tests if density can recover",
    ),
    _variant(
        "et40adxweak_c0_h6_a",
        "weak_trend_firewall_quality_repair_aonly",
        max_hold_bars=6,
        reentry_cooldown_bars=0,
        block_short_min=0.0,
        block_short_max=25.0,
        block_long=True,
        block_long_min=0.0,
        block_long_max=20.0,
        notes="same weak-trend firewall under hold6; tests whether shorter lifecycle can offset filtered-route density loss",
    ),
    _variant(
        "et40s25_c0_h8_b",
        "tier_b_damage_control_comparison",
        max_hold_bars=8,
        reentry_cooldown_bars=0,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for the no-cooldown density repair path; Tier B must not create hidden OOS damage",
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
