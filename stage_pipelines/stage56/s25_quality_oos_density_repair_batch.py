from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50AG"
PARENT_RUN_ID = "run50AG_stage56_s25_quality_oos_density_repair_v1"
PACKET_ID = "stage56_run50AG_s25_quality_oos_density_repair_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__S25QualityOosDensityRepair"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50AG_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50AG_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50AG_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    *,
    short_threshold: float,
    long_threshold: float,
    reentry_cooldown_bars: int,
    routed_fallback_enabled: bool,
    notes: str,
) -> batch.ModelAxisVariant:
    return batch.ModelAxisVariant(
        variant_id,
        base_id,
        group,
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        short_threshold,
        long_threshold,
        0.0,
        0.450,
        0.450,
        0.0,
        8,
        routed_fallback_enabled,
        reentry_cooldown_bars=reentry_cooldown_bars,
        side_filter_id=f"sadx2025_c{reentry_cooldown_bars:02d}",
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
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "s24l15a",
        "s24l15",
        "s25_quality_threshold_relax_cooldown8_aonly",
        short_threshold=0.240,
        long_threshold=0.150,
        reentry_cooldown_bars=8,
        routed_fallback_enabled=False,
        notes="A-only OOS density repair from run50AF s25c8a by relaxing short to 0.240 and long to 0.150",
    ),
    _variant(
        "s24l15b",
        "s24l15",
        "s25_quality_threshold_relax_cooldown8_tier_b_comparison",
        short_threshold=0.240,
        long_threshold=0.150,
        reentry_cooldown_bars=8,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for s24/l15 cooldown8 density repair",
    ),
    _variant(
        "s22l14a",
        "s22l14",
        "s25_quality_threshold_relax_cooldown8_aonly",
        short_threshold=0.220,
        long_threshold=0.140,
        reentry_cooldown_bars=8,
        routed_fallback_enabled=False,
        notes="stronger OOS density pressure while retaining short ADX20-25 block; A-only comparison",
    ),
    _variant(
        "s22l14b",
        "s22l14",
        "s25_quality_threshold_relax_cooldown8_tier_b_comparison",
        short_threshold=0.220,
        long_threshold=0.140,
        reentry_cooldown_bars=8,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for stronger threshold relaxation",
    ),
    _variant(
        "s20l13a",
        "s20l13",
        "s25_quality_threshold_relax_cooldown8_aonly",
        short_threshold=0.200,
        long_threshold=0.130,
        reentry_cooldown_bars=8,
        routed_fallback_enabled=False,
        notes="aggressive density pressure from s25c8a quality branch; A-only comparison",
    ),
    _variant(
        "s20l13b",
        "s20l13",
        "s25_quality_threshold_relax_cooldown8_tier_b_comparison",
        short_threshold=0.200,
        long_threshold=0.130,
        reentry_cooldown_bars=8,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for aggressive density pressure",
    ),
    _variant(
        "s24l15c6a",
        "s24l15c6",
        "s25_quality_threshold_relax_cooldown6_aonly",
        short_threshold=0.240,
        long_threshold=0.150,
        reentry_cooldown_bars=6,
        routed_fallback_enabled=False,
        notes="cooldown6 density pressure from the milder s24/l15 relaxation; A-only comparison",
    ),
    _variant(
        "s24l15c6b",
        "s24l15c6",
        "s25_quality_threshold_relax_cooldown6_tier_b_comparison",
        short_threshold=0.240,
        long_threshold=0.150,
        reentry_cooldown_bars=6,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for cooldown6 s24/l15 density pressure",
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
