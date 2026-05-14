from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50AZ"
PARENT_RUN_ID = "run50AZ_stage56_cooldown12_broad_model_source_v1"
PACKET_ID = "stage56_run50AZ_cooldown12_broad_model_source_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__Cooldown12BroadModelSource"
RUN_ROOT = batch.STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = batch.REVIEWS_ROOT / "run50AZ_reopen_batch.md"
RESULTS_CSV_PATH = batch.REVIEWS_ROOT / "run50AZ_summary.csv"
AUDIT_CSV_PATH = batch.REVIEWS_ROOT / "run50AZ_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"


def _variant(
    variant_id: str,
    group: str,
    *,
    estimator_family: str,
    short_threshold: float,
    long_threshold: float,
    routed_fallback_enabled: bool,
    class_weight: str | None = None,
    flat_sample_weight: float | None = None,
    nonflat_sample_weight: float | None = None,
    train_start_utc: str | None = None,
    min_samples_leaf: int = 10,
    n_estimators: int = 520,
    side_filter_enabled: bool = False,
    notes: str,
) -> batch.ModelAxisVariant:
    threshold_tag = f"s{int(round(short_threshold * 1000)):03d}l{int(round(long_threshold * 1000)):03d}"
    model_tag = (
        f"extratrees_leaf{min_samples_leaf:02d}_n{n_estimators}_{threshold_tag}"
        if estimator_family == "extratrees"
        else f"logreg_broad_{threshold_tag}_{variant_id}"
    )
    return batch.ModelAxisVariant(
        variant_id=variant_id,
        base_id=f"{estimator_family}_c12_h4_{threshold_tag}",
        group=group,
        model_spec_id=model_tag,
        c_value=0.75,
        class_weight=class_weight,
        flat_sample_weight=flat_sample_weight,
        nonflat_sample_weight=nonflat_sample_weight,
        train_start_utc=train_start_utc,
        tier_a_short_threshold=short_threshold,
        tier_a_long_threshold=long_threshold,
        tier_a_min_margin=0.0,
        tier_b_short_threshold=0.450,
        tier_b_long_threshold=0.450,
        tier_b_min_margin=0.0,
        max_hold_bars=4,
        routed_fallback_enabled=routed_fallback_enabled,
        reentry_cooldown_bars=12,
        entry_transition_only=False,
        entry_transition_rearm_min_confidence_delta=0.0,
        side_filter_id="cooldown12_broad_source_none" if not side_filter_enabled else "cooldown12_broad_source_short_adx2025_block",
        side_filter_enabled=side_filter_enabled,
        tier_a_side_filter_feature_index=34,
        tier_b_side_filter_feature_index=34,
        block_short_feature_range=side_filter_enabled,
        block_short_feature_min=20.0,
        block_short_feature_max=25.0,
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
        "et10c12_h4_s160l090_a",
        "extratrees_leaf10_cooldown12_no_side_aonly",
        estimator_family="extratrees",
        short_threshold=0.160,
        long_threshold=0.090,
        routed_fallback_enabled=False,
        class_weight="balanced",
        notes="A-only broad ExtraTrees leaf10 source with actual cooldown12 and no side firewall; tests true post-cooldown density ceiling.",
    ),
    _variant(
        "et10c12_h4_s160l090_b",
        "extratrees_leaf10_cooldown12_tier_b_damage_audit",
        estimator_family="extratrees",
        short_threshold=0.160,
        long_threshold=0.090,
        routed_fallback_enabled=True,
        class_weight="balanced",
        notes="Matched A+B routed run for broad ExtraTrees leaf10 source; exposes hidden Tier B damage under cooldown12.",
    ),
    _variant(
        "nf250c12_h4_s160l090_a",
        "logreg_nonflat250_cooldown12_no_side_aonly",
        estimator_family="logreg",
        short_threshold=0.160,
        long_threshold=0.090,
        routed_fallback_enabled=False,
        flat_sample_weight=0.50,
        nonflat_sample_weight=2.50,
        notes="A-only logistic nonflat250 broad source with actual cooldown12; tests whether linear source can supply cleaner real density.",
    ),
    _variant(
        "r24balc12_h4_s140l080_a",
        "recent2024_balanced_cooldown12_no_side_aonly",
        estimator_family="logreg",
        short_threshold=0.140,
        long_threshold=0.080,
        routed_fallback_enabled=False,
        class_weight="balanced",
        train_start_utc="2024-01-01T00:00:00Z",
        notes="A-only recent-2024 balanced logistic source with actual cooldown12; tests drift-specific real density.",
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
