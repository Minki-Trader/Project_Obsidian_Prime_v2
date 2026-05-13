from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50W"
PARENT_RUN_ID = "run50W_stage56_nonflat_regime_firewall_v1"
PACKET_ID = "stage56_run50W_nonflat_regime_firewall_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__NonflatRegimeFirewall"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50W_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50W_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50W_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    reentry_cooldown_bars: int,
    *,
    block_short_adx_20_25: bool = True,
    block_long_adx_gt25: bool = False,
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
        side_filter_id="directional_adx_regime_firewall",
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        tier_b_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        block_short_feature_range=block_short_adx_20_25,
        block_short_feature_min=20.0,
        block_short_feature_max=25.0,
        block_long_feature_range=block_long_adx_gt25,
        block_long_feature_min=25.0,
        block_long_feature_max=1000.0,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "nfw_s37l24_c0_sadx",
        "nfw_s37l24",
        "nonflat_regime_firewall_short_adx20_25",
        0.370,
        0.240,
        0,
        notes="run50V threshold with short ADX 20-25 firewall and core/mixed Tier B gate",
    ),
    _variant(
        "nfw_s37l24_c1_sadx",
        "nfw_s37l24",
        "nonflat_regime_firewall_short_adx20_25_cooldown",
        0.370,
        0.240,
        1,
        notes="run50V threshold with short ADX 20-25 firewall plus one-bar reentry firewall",
    ),
    _variant(
        "nfw_s35l22_c2_sadx",
        "nfw_s35l22",
        "nonflat_regime_firewall_short_adx20_25_cooldown_density",
        0.350,
        0.220,
        2,
        notes="lower thresholds to recover density after short ADX 20-25 and two-bar reentry firewalls",
    ),
    _variant(
        "nfw_s33l20_c3_sadx",
        "nfw_s33l20",
        "nonflat_regime_firewall_short_adx20_25_cooldown_density",
        0.330,
        0.200,
        3,
        notes="strong density pressure after short ADX 20-25 and three-bar reentry firewalls",
    ),
    _variant(
        "nfw_s37l24_c0_sadxlgt",
        "nfw_s37l24",
        "nonflat_regime_firewall_short_adx20_25_long_gt25",
        0.370,
        0.240,
        0,
        block_long_adx_gt25=True,
        notes="run50V threshold with short ADX 20-25 and long ADX >25 firewalls",
    ),
    _variant(
        "nfw_s35l22_c1_sadxlgt",
        "nfw_s35l22",
        "nonflat_regime_firewall_short_adx20_25_long_gt25_cooldown",
        0.350,
        0.220,
        1,
        block_long_adx_gt25=True,
        notes="lower thresholds with short ADX 20-25, long ADX >25, and one-bar reentry firewalls",
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
