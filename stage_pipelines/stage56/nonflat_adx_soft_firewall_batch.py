from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50X"
PARENT_RUN_ID = "run50X_stage56_nonflat_adx_soft_firewall_v1"
PACKET_ID = "stage56_run50X_nonflat_adx_soft_firewall_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__NonflatAdxSoftFirewall"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50X_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50X_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50X_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    reentry_cooldown_bars: int,
    short_block_min: float,
    short_block_max: float,
    *,
    block_long: bool = False,
    long_block_min: float = 40.0,
    long_block_max: float = 1000.0,
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
        6,
        True,
        reentry_cooldown_bars=reentry_cooldown_bars,
        side_filter_id="directional_adx_soft_firewall",
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        tier_b_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        block_short_feature_range=True,
        block_short_feature_min=short_block_min,
        block_short_feature_max=short_block_max,
        block_long_feature_range=block_long,
        block_long_feature_min=long_block_min,
        block_long_feature_max=long_block_max,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "nfx_s35l22_c2_s2030",
        "nfx_s35l22",
        "nonflat_adx_soft_firewall_short20_30",
        0.350,
        0.220,
        2,
        20.0,
        30.0,
        notes="run50W seed with wider short ADX 20-30 firewall",
    ),
    _variant(
        "nfx_s33l20_c3_s2030",
        "nfx_s33l20",
        "nonflat_adx_soft_firewall_short20_30_density",
        0.330,
        0.200,
        3,
        20.0,
        30.0,
        notes="lower thresholds to recover density after wider short ADX 20-30 firewall",
    ),
    _variant(
        "nfx_s35l22_c2_s2030l40",
        "nfx_s35l22",
        "nonflat_adx_soft_firewall_short20_30_long40",
        0.350,
        0.220,
        2,
        20.0,
        30.0,
        block_long=True,
        long_block_min=40.0,
        notes="wider short ADX firewall plus soft long ADX 40+ OOS damage firewall",
    ),
    _variant(
        "nfx_s33l20_c3_s2030l40",
        "nfx_s33l20",
        "nonflat_adx_soft_firewall_short20_30_long40_density",
        0.330,
        0.200,
        3,
        20.0,
        30.0,
        block_long=True,
        long_block_min=40.0,
        notes="density pressure with wider short ADX firewall plus soft long ADX 40+ firewall",
    ),
    _variant(
        "nfx_s35l22_c2_s2030l30p",
        "nfx_s35l22",
        "nonflat_adx_soft_firewall_short20_30_long30plus",
        0.350,
        0.220,
        2,
        20.0,
        30.0,
        block_long=True,
        long_block_min=30.0,
        notes="stress test broader long ADX 30+ firewall after OOS buy downtrend damage",
    ),
    _variant(
        "nfx_s33l20_c3_s2030l30p",
        "nfx_s33l20",
        "nonflat_adx_soft_firewall_short20_30_long30plus_density",
        0.330,
        0.200,
        3,
        20.0,
        30.0,
        block_long=True,
        long_block_min=30.0,
        notes="density pressure with broader long ADX 30+ firewall",
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
