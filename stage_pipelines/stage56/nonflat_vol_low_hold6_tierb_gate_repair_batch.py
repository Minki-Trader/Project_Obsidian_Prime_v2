from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50V"
PARENT_RUN_ID = "run50V_stage56_nonflat_vol_low_hold6_tierb_gate_repair_v1"
PACKET_ID = "stage56_run50V_nonflat_vol_low_hold6_tierb_gate_repair_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__NonflatVolLowHold6TierBGateRepair"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50V_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50V_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50V_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

HISTORICAL_VOL_20_FEATURE_INDEX = 32
VOL_LOW_MAX = 0.19637160003185267
SIDE_FILTER_KWARGS = {
    "side_filter_id": "block_both_vol_low",
    "side_filter_enabled": True,
    "tier_a_side_filter_feature_index": HISTORICAL_VOL_20_FEATURE_INDEX,
    "tier_b_side_filter_feature_index": HISTORICAL_VOL_20_FEATURE_INDEX,
    "block_short_feature_range": True,
    "block_short_feature_min": 0.0,
    "block_short_feature_max": VOL_LOW_MAX,
    "block_long_feature_range": True,
    "block_long_feature_min": 0.0,
    "block_long_feature_max": VOL_LOW_MAX,
}


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    tier_b_allowed_subtypes: tuple[str, ...],
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
        reentry_cooldown_bars=0,
        tier_b_allowed_subtypes=tier_b_allowed_subtypes,
        notes=notes,
        **SIDE_FILTER_KWARGS,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "nfv_h6_s37l24_bcm",
        "nfv_h6_s37l24",
        "nonflat_vol_low_hold6_tier_b_core_mixed_gate",
        0.370,
        0.240,
        ("B_core_only", "B_mixed_partial_context"),
        "shortened-id repair of run50U gated Tier B core-or-mixed fallback",
    ),
    _variant(
        "nfv_h6_s39l23_bcm",
        "nfv_h6_s39l23",
        "nonflat_vol_low_hold6_tier_b_core_mixed_gate",
        0.390,
        0.230,
        ("B_core_only", "B_mixed_partial_context"),
        "shortened-id stronger short filter with gated Tier B core-or-mixed fallback",
    ),
    _variant(
        "nfv_h6_s39l23_bmx",
        "nfv_h6_s39l23",
        "nonflat_vol_low_hold6_tier_b_mixed_gate",
        0.390,
        0.230,
        ("B_mixed_partial_context",),
        "shortened-id stronger short filter with mixed-only Tier B fallback",
    ),
    _variant(
        "nfv_h6_s39l23_bma",
        "nfv_h6_s39l23",
        "nonflat_vol_low_hold6_tier_b_macro_gate",
        0.390,
        0.230,
        ("B_macro_missing",),
        "shortened-id stronger short filter with macro-missing Tier B fallback",
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
