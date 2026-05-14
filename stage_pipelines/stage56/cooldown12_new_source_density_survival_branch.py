from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50AV"
PARENT_RUN_ID = "run50AV_stage56_cooldown12_new_source_density_survival_v1"
PACKET_ID = "stage56_run50AV_cooldown12_new_source_density_survival_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__Cooldown12NewSourceDensitySurvival"
RUN_ROOT = batch.STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = batch.REVIEWS_ROOT / "run50AV_reopen_batch.md"
RESULTS_CSV_PATH = batch.REVIEWS_ROOT / "run50AV_summary.csv"
AUDIT_CSV_PATH = batch.REVIEWS_ROOT / "run50AV_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    group: str,
    *,
    tier_a_short_threshold: float,
    tier_a_long_threshold: float,
    max_hold_bars: int = 4,
    routed_fallback_enabled: bool = False,
    estimator_family: str = "extratrees",
    min_samples_leaf: int = 40,
    n_estimators: int = 420,
    short_block_max: float = 25.0,
    notes: str,
) -> batch.ModelAxisVariant:
    threshold_tag = f"s{int(round(tier_a_short_threshold * 1000)):03d}l{int(round(tier_a_long_threshold * 1000)):03d}"
    model_tag = (
        f"extratrees_leaf{int(min_samples_leaf):02d}_n{int(n_estimators)}_{threshold_tag}"
        if estimator_family == "extratrees"
        else f"logreg_nonflat200_c050_{threshold_tag}"
    )
    return batch.ModelAxisVariant(
        variant_id=variant_id,
        base_id=f"{estimator_family}_c12_h{int(max_hold_bars)}_{threshold_tag}",
        group=group,
        model_spec_id=model_tag,
        c_value=0.50,
        class_weight="balanced" if estimator_family == "extratrees" else None,
        flat_sample_weight=None if estimator_family == "extratrees" else 0.60,
        nonflat_sample_weight=None if estimator_family == "extratrees" else 2.00,
        train_start_utc=None,
        tier_a_short_threshold=tier_a_short_threshold,
        tier_a_long_threshold=tier_a_long_threshold,
        tier_a_min_margin=0.0,
        tier_b_short_threshold=0.450,
        tier_b_long_threshold=0.450,
        tier_b_min_margin=0.0,
        max_hold_bars=max_hold_bars,
        routed_fallback_enabled=routed_fallback_enabled,
        reentry_cooldown_bars=12,
        entry_transition_only=False,
        entry_transition_rearm_min_confidence_delta=0.0,
        side_filter_id="cooldown12_new_source_adx_short_firewall",
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        tier_b_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        block_short_feature_range=True,
        block_short_feature_min=20.0,
        block_short_feature_max=short_block_max,
        block_long_feature_range=False,
        block_long_feature_min=0.0,
        block_long_feature_max=0.0,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
        estimator_family=estimator_family,
        n_estimators=n_estimators,
        min_samples_leaf=min_samples_leaf,
        max_features="sqrt",
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "et40c12_h4_s220l140_a",
        "extratrees_leaf40_actual_cooldown12_aonly",
        tier_a_short_threshold=0.220,
        tier_a_long_threshold=0.140,
        notes="ExtraTrees leaf40 with actual 12-bar cooldown; tests whether smoother source density survives same-move audit.",
    ),
    _variant(
        "et40c12_h4_s200l120_a",
        "extratrees_leaf40_actual_cooldown12_aggressive_aonly",
        tier_a_short_threshold=0.200,
        tier_a_long_threshold=0.120,
        notes="Aggressive threshold pressure under actual cooldown12; probes whether density can approach 5/day without split re-entry.",
    ),
    _variant(
        "et30c12_h4_s220l140_a",
        "extratrees_leaf30_actual_cooldown12_aonly",
        tier_a_short_threshold=0.220,
        tier_a_long_threshold=0.140,
        min_samples_leaf=30,
        notes="Leaf30 middle granularity with actual cooldown12; checks whether leaf40 was too smooth for real OOS density.",
    ),
    _variant(
        "et20c12_h4_s240l150_a",
        "extratrees_leaf20_actual_cooldown12_quality_aonly",
        tier_a_short_threshold=0.240,
        tier_a_long_threshold=0.150,
        min_samples_leaf=20,
        notes="Leaf20 quality threshold under actual cooldown12; tests finer source while resisting validation cost drag.",
    ),
    _variant(
        "nf200c12_h4_s240l150_a",
        "logreg_nonflat200_actual_cooldown12_control_aonly",
        tier_a_short_threshold=0.240,
        tier_a_long_threshold=0.150,
        estimator_family="logreg",
        notes="Logistic nonflat200 control with actual cooldown12; separates lifecycle effect from ExtraTrees source effect.",
    ),
    _variant(
        "et40c12_h4_s220l140_b",
        "extratrees_leaf40_actual_cooldown12_tier_b_comparison",
        tier_a_short_threshold=0.220,
        tier_a_long_threshold=0.140,
        routed_fallback_enabled=True,
        notes="Matched A+B comparison for et40 cooldown12 source; checks whether Tier B creates hidden OOS damage.",
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
