from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch


RUN_NUMBER = "run50AQ"
PARENT_RUN_ID = "run50AQ_stage56_extratrees_model_axis_density_v1"
PACKET_ID = "stage56_run50AQ_extratrees_model_axis_density_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ExtraTreesModelAxisDensity"
RUN_ROOT = batch.STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = batch.REVIEWS_ROOT / "run50AQ_reopen_batch.md"
RESULTS_CSV_PATH = batch.REVIEWS_ROOT / "run50AQ_summary.csv"
AUDIT_CSV_PATH = batch.REVIEWS_ROOT / "run50AQ_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    *,
    min_samples_leaf: int,
    n_estimators: int = 360,
    max_features: str | float | None = "sqrt",
    max_depth: int | None = None,
    tier_a_short_threshold: float = 0.260,
    tier_a_long_threshold: float = 0.170,
    routed_fallback_enabled: bool,
    notes: str,
) -> batch.ModelAxisVariant:
    return batch.ModelAxisVariant(
        variant_id,
        base_id,
        group,
        f"extratrees_leaf{min_samples_leaf}_n{n_estimators}_s{int(tier_a_short_threshold * 1000)}l{int(tier_a_long_threshold * 1000)}",
        0.50,
        "balanced",
        None,
        None,
        None,
        tier_a_short_threshold,
        tier_a_long_threshold,
        0.0,
        0.450,
        0.450,
        0.0,
        8,
        routed_fallback_enabled,
        reentry_cooldown_bars=8,
        side_filter_id="s25_extratrees_adx_short_block",
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        tier_b_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        block_short_feature_range=True,
        block_short_feature_min=20.0,
        block_short_feature_max=25.0,
        block_long_feature_range=False,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
        estimator_family="extratrees",
        n_estimators=n_estimators,
        min_samples_leaf=min_samples_leaf,
        max_features=max_features,
        max_depth=max_depth,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "et20s25a",
        "et20s25",
        "extratrees_leaf20_s25_aonly",
        min_samples_leaf=20,
        routed_fallback_enabled=False,
        notes="ExtraTrees leaf20 on s25 route without Tier B; tests model-family density against nf200s25a style reference",
    ),
    _variant(
        "et20s25b",
        "et20s25",
        "extratrees_leaf20_s25_tier_b",
        min_samples_leaf=20,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for ExtraTrees leaf20 s25 route and hidden Tier B damage",
    ),
    _variant(
        "et40s25a",
        "et40s25",
        "extratrees_leaf40_s25_aonly",
        min_samples_leaf=40,
        routed_fallback_enabled=False,
        notes="smoother ExtraTrees leaf40 A-only variant to reduce same-move split trading and cost drag",
    ),
    _variant(
        "et40s25b",
        "et40s25",
        "extratrees_leaf40_s25_tier_b",
        min_samples_leaf=40,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for smoother ExtraTrees leaf40 route",
    ),
    _variant(
        "et20s30a",
        "et20s30",
        "extratrees_leaf20_stricter_aonly",
        min_samples_leaf=20,
        tier_a_short_threshold=0.300,
        tier_a_long_threshold=0.220,
        routed_fallback_enabled=False,
        notes="stricter ExtraTrees threshold stress if s25 route over-trades or cost-stress fails",
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
