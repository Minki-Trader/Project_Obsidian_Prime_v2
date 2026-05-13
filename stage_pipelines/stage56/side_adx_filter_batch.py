from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50N"
PARENT_RUN_ID = "run50N_stage56_side_adx_filter_v1"
PACKET_ID = "stage56_run50N_side_adx_filter_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__SideAdxFilter"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50N_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50N_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50N_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34
SIDE_FILTER_KWARGS = {
    "side_filter_id": "skip_short_adx_20_25",
    "side_filter_enabled": True,
    "tier_a_side_filter_feature_index": ADX_14_FEATURE_INDEX,
    "tier_b_side_filter_feature_index": ADX_14_FEATURE_INDEX,
    "block_short_feature_range": True,
    "block_short_feature_min": 20.0,
    "block_short_feature_max": 25.0,
}


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    batch.ModelAxisVariant(
        "c6s350l250_a_sadx",
        "c6s350l250_sadx",
        "side_adx_filter_aonly",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.350,
        0.250,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        False,
        reentry_cooldown_bars=6,
        notes="six-bar cooldown with short-side ADX 20-25 block; matched A-only read for Tier B comparison",
        **SIDE_FILTER_KWARGS,
    ),
    batch.ModelAxisVariant(
        "c6s350l250_b_sadx",
        "c6s350l250_sadx",
        "side_adx_filter_tier_b_comparison",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.350,
        0.250,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        True,
        reentry_cooldown_bars=6,
        notes="six-bar cooldown with short-side ADX 20-25 block; A+B routed read for Tier B contribution",
        **SIDE_FILTER_KWARGS,
    ),
    batch.ModelAxisVariant(
        "c6s330l235_a_sadx",
        "c6s330l235_sadx",
        "side_adx_filter_aonly",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.330,
        0.235,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        False,
        reentry_cooldown_bars=6,
        notes="lower threshold density recovery after ADX short block; matched A-only read",
        **SIDE_FILTER_KWARGS,
    ),
    batch.ModelAxisVariant(
        "c6s330l235_b_sadx",
        "c6s330l235_sadx",
        "side_adx_filter_tier_b_comparison",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.330,
        0.235,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        True,
        reentry_cooldown_bars=6,
        notes="lower threshold density recovery after ADX short block; A+B routed read",
        **SIDE_FILTER_KWARGS,
    ),
    batch.ModelAxisVariant(
        "c6s315l225_a_sadx",
        "c6s315l225_sadx",
        "side_adx_filter_aonly",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.315,
        0.225,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        False,
        reentry_cooldown_bars=6,
        notes="stronger density recovery pressure after ADX short block; matched A-only read",
        **SIDE_FILTER_KWARGS,
    ),
    batch.ModelAxisVariant(
        "c6s315l225_b_sadx",
        "c6s315l225_sadx",
        "side_adx_filter_tier_b_comparison",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.315,
        0.225,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        True,
        reentry_cooldown_bars=6,
        notes="stronger density recovery pressure after ADX short block; A+B routed read",
        **SIDE_FILTER_KWARGS,
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
