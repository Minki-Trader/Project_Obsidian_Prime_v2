from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50AE"
PARENT_RUN_ID = "run50AE_stage56_vl_cooldown_density_v1"
PACKET_ID = "stage56_run50AE_vl_cooldown_density_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__BuyVolLowCooldownDensity"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50AE_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50AE_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50AE_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

HISTORICAL_VOL_20_FEATURE_INDEX = 32
VOL_LOW_MAX = 0.19637160003185267


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    *,
    reentry_cooldown_bars: int,
    routed_fallback_enabled: bool,
    session_slice_id: str | None = None,
    max_hold_bars: int = 8,
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
        0.260,
        0.170,
        0.0,
        0.450,
        0.450,
        0.0,
        max_hold_bars,
        routed_fallback_enabled,
        reentry_cooldown_bars=reentry_cooldown_bars,
        side_filter_id=f"vl_c{reentry_cooldown_bars:02d}",
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=HISTORICAL_VOL_20_FEATURE_INDEX,
        tier_b_side_filter_feature_index=HISTORICAL_VOL_20_FEATURE_INDEX,
        block_short_feature_range=False,
        block_short_feature_min=0.0,
        block_short_feature_max=0.0,
        block_long_feature_range=True,
        block_long_feature_min=0.0,
        block_long_feature_max=VOL_LOW_MAX,
        session_slice_id=session_slice_id,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "c06a",
        "c06",
        "buy_vol_low_cooldown6_aonly",
        reentry_cooldown_bars=6,
        routed_fallback_enabled=False,
        notes="recover density after run50AD while preserving buy vol_low exclusion; A-only comparison",
    ),
    _variant(
        "c06b",
        "c06",
        "buy_vol_low_cooldown6_tier_b_comparison",
        reentry_cooldown_bars=6,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for cooldown6 density recovery after buy vol_low exclusion",
    ),
    _variant(
        "c08a",
        "c08",
        "buy_vol_low_cooldown8_aonly",
        reentry_cooldown_bars=8,
        routed_fallback_enabled=False,
        notes="cooldown8 interpolation between run50AD cooldown12 and denser cooldown branches",
    ),
    _variant(
        "c08b",
        "c08",
        "buy_vol_low_cooldown8_tier_b_comparison",
        reentry_cooldown_bars=8,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for cooldown8 interpolation",
    ),
    _variant(
        "c10a",
        "c10",
        "buy_vol_low_cooldown10_aonly",
        reentry_cooldown_bars=10,
        routed_fallback_enabled=False,
        notes="cooldown10 interpolation to test density survival with less same-move reopening",
    ),
    _variant(
        "c10b",
        "c10",
        "buy_vol_low_cooldown10_tier_b_comparison",
        reentry_cooldown_bars=10,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for cooldown10 interpolation",
    ),
    _variant(
        "em6a",
        "em6",
        "buy_vol_low_early_mid_cooldown6_aonly",
        reentry_cooldown_bars=6,
        routed_fallback_enabled=False,
        session_slice_id="early_mid",
        notes="early_mid session slice after run50AD attribution; A-only density-quality check",
    ),
    _variant(
        "em6b",
        "em6",
        "buy_vol_low_early_mid_cooldown6_tier_b_comparison",
        reentry_cooldown_bars=6,
        routed_fallback_enabled=True,
        session_slice_id="early_mid",
        notes="matched A+B comparison for early_mid cooldown6 branch",
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
