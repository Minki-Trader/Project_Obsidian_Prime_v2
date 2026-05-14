from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50BL"
PARENT_RUN_ID = "run50BL_stage56_same_direction_cooldown_real_density_repair_v1"
PACKET_ID = "stage56_run50BL_same_direction_cooldown_real_density_repair_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__SameDirectionCooldownRealDensityRepair"
RUN_ROOT = batch.STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = batch.REVIEWS_ROOT / "run50BL_sd_cooldown_repair.md"
RESULTS_CSV_PATH = batch.REVIEWS_ROOT / "run50BL_summary.csv"
AUDIT_CSV_PATH = batch.REVIEWS_ROOT / "run50BL_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    group: str,
    *,
    leaf: int = 40,
    short_threshold: float,
    long_threshold: float,
    rearm_delta: float = 0.001,
    max_hold_bars: int,
    same_direction_cooldown_bars: int,
    routed_fallback_enabled: bool = False,
    notes: str,
) -> batch.ModelAxisVariant:
    threshold_tag = f"s{int(round(short_threshold * 1000)):03d}l{int(round(long_threshold * 1000)):03d}"
    rearm_tag = f"r{int(round(rearm_delta * 1000)):03d}"
    return batch.ModelAxisVariant(
        variant_id=variant_id,
        base_id=f"et{leaf}h{max_hold_bars}sd{same_direction_cooldown_bars}_{threshold_tag}_{rearm_tag}",
        group=group,
        model_spec_id=f"extratrees_leaf{leaf}_n360_{threshold_tag}",
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
        routed_fallback_enabled=routed_fallback_enabled,
        reentry_cooldown_bars=0,
        same_direction_reentry_cooldown_bars=same_direction_cooldown_bars,
        entry_transition_only=True,
        entry_transition_rearm_min_confidence_delta=rearm_delta,
        side_filter_id=f"et{leaf}_s25_same_direction_cooldown_guard",
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
        "et40h3sd2_s240l150_r001_a",
        "same_direction_cooldown_short_hold_aonly",
        short_threshold=0.240,
        long_threshold=0.150,
        max_hold_bars=3,
        same_direction_cooldown_bars=2,
        notes="run50BI raw-density control with same-direction-only cooldown2; tests whether opposite reversals preserve OOS density",
    ),
    _variant(
        "et40h3sd3_s240l150_r001_a",
        "same_direction_cooldown_short_hold_aonly",
        short_threshold=0.240,
        long_threshold=0.150,
        max_hold_bars=3,
        same_direction_cooldown_bars=3,
        notes="matched hold3 same-direction-only cooldown3 against generic cooldown3 that fell under OOS density",
    ),
    _variant(
        "et40h3sd4_s240l150_r001_a",
        "same_direction_cooldown_short_hold_aonly",
        short_threshold=0.240,
        long_threshold=0.150,
        max_hold_bars=3,
        same_direction_cooldown_bars=4,
        notes="stricter same-direction-only cooldown4 pressure on the raw-density branch",
    ),
    _variant(
        "et40h3sd3_s250l160_r001_a",
        "same_direction_cooldown_threshold_pressure_aonly",
        short_threshold=0.250,
        long_threshold=0.160,
        max_hold_bars=3,
        same_direction_cooldown_bars=3,
        notes="slightly tighter thresholds test whether validation PF recovers while OOS density stays above five trades per day",
    ),
    _variant(
        "et40h4sd3_s250l160_r001_a",
        "same_direction_cooldown_hold_balance_aonly",
        short_threshold=0.250,
        long_threshold=0.160,
        max_hold_bars=4,
        same_direction_cooldown_bars=3,
        notes="hold4 control for same-direction-only cooldown3; balances run50BH quality and run50BI density",
    ),
    _variant(
        "et40h6sd3_s260l170_r001_a",
        "same_direction_cooldown_anchor_stress_aonly",
        short_threshold=0.260,
        long_threshold=0.170,
        max_hold_bars=6,
        same_direction_cooldown_bars=3,
        notes="run50BH anchor thresholds with same-direction-only cooldown3; checks whether anchor quality survives real-density guard pressure",
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
