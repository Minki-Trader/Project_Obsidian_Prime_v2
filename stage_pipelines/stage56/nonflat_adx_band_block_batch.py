from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50R"
PARENT_RUN_ID = "run50R_stage56_nonflat_adx_band_block_v1"
PACKET_ID = "stage56_run50R_nonflat_adx_band_block_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__NonflatAdxBandBlock"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50R_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50R_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50R_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34
SIDE_FILTER_KWARGS = {
    "side_filter_id": "block_both_adx_20_25",
    "side_filter_enabled": True,
    "tier_a_side_filter_feature_index": ADX_14_FEATURE_INDEX,
    "tier_b_side_filter_feature_index": ADX_14_FEATURE_INDEX,
    "block_short_feature_range": True,
    "block_short_feature_min": 20.0,
    "block_short_feature_max": 25.0,
    "block_long_feature_range": True,
    "block_long_feature_min": 20.0,
    "block_long_feature_max": 25.0,
}


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    *,
    routed_fallback_enabled: bool,
    reentry_cooldown_bars: int,
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
        10,
        routed_fallback_enabled,
        reentry_cooldown_bars=reentry_cooldown_bars,
        notes=notes,
        **SIDE_FILTER_KWARGS,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "nf_adxblk_c1_s390l280_a",
        "nf_adxblk_c1_s390l280",
        "nonflat_adx_band_block_aonly",
        0.390,
        0.280,
        routed_fallback_enabled=False,
        reentry_cooldown_bars=1,
        notes="run50Q best threshold with one-bar cooldown and both-side ADX 20-25 block; Tier B disabled",
    ),
    _variant(
        "nf_adxblk_c1_s390l280_b",
        "nf_adxblk_c1_s390l280",
        "nonflat_adx_band_block_tier_b_comparison",
        0.390,
        0.280,
        routed_fallback_enabled=True,
        reentry_cooldown_bars=1,
        notes="run50Q best threshold with one-bar cooldown and both-side ADX 20-25 block; B045 fallback",
    ),
    _variant(
        "nf_adxblk_c1_s380l270_a",
        "nf_adxblk_c1_s380l270",
        "nonflat_adx_band_block_aonly",
        0.380,
        0.270,
        routed_fallback_enabled=False,
        reentry_cooldown_bars=1,
        notes="lower threshold to recover density after both-side ADX 20-25 block; Tier B disabled",
    ),
    _variant(
        "nf_adxblk_c1_s380l270_b",
        "nf_adxblk_c1_s380l270",
        "nonflat_adx_band_block_tier_b_comparison",
        0.380,
        0.270,
        routed_fallback_enabled=True,
        reentry_cooldown_bars=1,
        notes="lower threshold to recover density after both-side ADX 20-25 block; B045 fallback",
    ),
    _variant(
        "nf_adxblk_c0_s390l280_b",
        "nf_adxblk_c0_s390l280",
        "nonflat_adx_band_block_no_cooldown_density",
        0.390,
        0.280,
        routed_fallback_enabled=True,
        reentry_cooldown_bars=0,
        notes="no-cooldown density recovery after both-side ADX 20-25 block; B045 fallback",
    ),
    _variant(
        "nf_adxblk_c0_s380l270_b",
        "nf_adxblk_c0_s380l270",
        "nonflat_adx_band_block_no_cooldown_density",
        0.380,
        0.270,
        routed_fallback_enabled=True,
        reentry_cooldown_bars=0,
        notes="lower no-cooldown density recovery after both-side ADX 20-25 block; B045 fallback",
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
