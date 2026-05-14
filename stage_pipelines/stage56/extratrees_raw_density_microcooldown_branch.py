from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50BI"
PARENT_RUN_ID = "run50BI_stage56_extratrees_raw_density_microcooldown_v1"
PACKET_ID = "stage56_run50BI_extratrees_raw_density_microcooldown_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ExtraTreesRawDensityMicrocooldown"
RUN_ROOT = batch.STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = batch.REVIEWS_ROOT / "run50BI_extratrees_raw_density_microcooldown.md"
RESULTS_CSV_PATH = batch.REVIEWS_ROOT / "run50BI_summary.csv"
AUDIT_CSV_PATH = batch.REVIEWS_ROOT / "run50BI_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    group: str,
    *,
    leaf: int = 40,
    short_threshold: float,
    long_threshold: float,
    rearm_delta: float,
    max_hold_bars: int,
    cooldown_bars: int,
    routed_fallback_enabled: bool = False,
    notes: str,
) -> batch.ModelAxisVariant:
    threshold_tag = f"s{int(round(short_threshold * 1000)):03d}l{int(round(long_threshold * 1000)):03d}"
    rearm_tag = f"r{int(round(rearm_delta * 1000)):03d}"
    return batch.ModelAxisVariant(
        variant_id=variant_id,
        base_id=f"et{leaf}h{max_hold_bars}c{cooldown_bars}_{threshold_tag}_{rearm_tag}",
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
        reentry_cooldown_bars=cooldown_bars,
        entry_transition_only=True,
        entry_transition_rearm_min_confidence_delta=rearm_delta,
        side_filter_id=f"et{leaf}_s25_raw_density_microcooldown_guard",
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
        "et40h3c0_s240l150_r001_a",
        "raw_density_short_hold_control_aonly",
        short_threshold=0.240,
        long_threshold=0.150,
        rearm_delta=0.001,
        max_hold_bars=3,
        cooldown_bars=0,
        notes="run50BH leaf40 clue with lower thresholds and hold3 to test whether raw density can rise enough before cooldown pressure",
    ),
    _variant(
        "et40h3c3_s240l150_r001_a",
        "raw_density_microcooldown_aonly",
        short_threshold=0.240,
        long_threshold=0.150,
        rearm_delta=0.001,
        max_hold_bars=3,
        cooldown_bars=3,
        notes="hold3 plus cooldown3 tests whether expanded raw density can survive a small real re-entry guard",
    ),
    _variant(
        "et40h4c3_s240l150_r001_a",
        "raw_density_microcooldown_aonly",
        short_threshold=0.240,
        long_threshold=0.150,
        rearm_delta=0.001,
        max_hold_bars=4,
        cooldown_bars=3,
        notes="hold4 cooldown3 balances run50BH hold6 quality with a real-density survival guard",
    ),
    _variant(
        "et40h4c3_s235l145_r001_a",
        "raw_density_threshold_expansion_aonly",
        short_threshold=0.235,
        long_threshold=0.145,
        rearm_delta=0.001,
        max_hold_bars=4,
        cooldown_bars=3,
        notes="slightly wider threshold expansion tests whether OOS density can pass after micro-cooldown without collapsing PF",
    ),
    _variant(
        "et40h4c3_s230l140_r001_a",
        "raw_density_threshold_expansion_aonly",
        short_threshold=0.230,
        long_threshold=0.140,
        rearm_delta=0.001,
        max_hold_bars=4,
        cooldown_bars=3,
        notes="widest leaf40 threshold expansion in this batch; stop condition is PF/net damage or same-move still dominating",
    ),
    _variant(
        "et40h4c3_s240l150_r005_a",
        "raw_density_rearm_quality_aonly",
        short_threshold=0.240,
        long_threshold=0.150,
        rearm_delta=0.005,
        max_hold_bars=4,
        cooldown_bars=3,
        notes="same threshold as the main micro-cooldown branch with stronger rearm quality guard",
    ),
    _variant(
        "et40h4c6_s240l150_r001_a",
        "raw_density_cooldown_stress_aonly",
        short_threshold=0.240,
        long_threshold=0.150,
        rearm_delta=0.001,
        max_hold_bars=4,
        cooldown_bars=6,
        notes="cooldown6 stress checks whether density expansion is real enough to survive stricter same-move pressure",
    ),
    _variant(
        "et40h4c3_s240l150_r001_b",
        "raw_density_microcooldown_tier_b_check",
        short_threshold=0.240,
        long_threshold=0.150,
        rearm_delta=0.001,
        max_hold_bars=4,
        cooldown_bars=3,
        routed_fallback_enabled=True,
        notes="matched Tier B fallback check for the hold4 cooldown3 raw-density branch",
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
