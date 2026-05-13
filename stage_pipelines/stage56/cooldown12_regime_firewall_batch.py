from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50AC"
PARENT_RUN_ID = "run50AC_stage56_cooldown12_regime_firewall_v1"
PACKET_ID = "stage56_run50AC_cooldown12_regime_firewall_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__Cooldown12RegimeFirewall"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50AC_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50AC_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50AC_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

HISTORICAL_VOL_20_FEATURE_INDEX = 32
ADX_14_FEATURE_INDEX = 34
SUPERTREND_10_3_FEATURE_INDEX = 36
VOL_LOW_MAX = 0.19637160003185267


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    *,
    feature_index: int,
    side_filter_id: str,
    block_long_min: float,
    block_long_max: float,
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
        reentry_cooldown_bars=12,
        side_filter_id=side_filter_id,
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=feature_index,
        tier_b_side_filter_feature_index=feature_index,
        block_short_feature_range=False,
        block_short_feature_min=0.0,
        block_short_feature_max=0.0,
        block_long_feature_range=True,
        block_long_feature_min=block_long_min,
        block_long_feature_max=block_long_max,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
    )


def _vol_low_variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    *,
    routed_fallback_enabled: bool,
    notes: str,
) -> batch.ModelAxisVariant:
    return _variant(
        variant_id,
        base_id,
        group,
        short_threshold,
        long_threshold,
        feature_index=HISTORICAL_VOL_20_FEATURE_INDEX,
        side_filter_id="cooldown12_buy_vol_low_firewall",
        block_long_min=0.0,
        block_long_max=VOL_LOW_MAX,
        routed_fallback_enabled=routed_fallback_enabled,
        notes=notes,
    )


def _adx2025_variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    *,
    routed_fallback_enabled: bool,
    notes: str,
) -> batch.ModelAxisVariant:
    return _variant(
        variant_id,
        base_id,
        group,
        short_threshold,
        long_threshold,
        feature_index=ADX_14_FEATURE_INDEX,
        side_filter_id="cooldown12_buy_adx20_25_firewall",
        block_long_min=20.0,
        block_long_max=25.0,
        routed_fallback_enabled=routed_fallback_enabled,
        notes=notes,
    )


def _downtrend_variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    *,
    routed_fallback_enabled: bool,
    notes: str,
) -> batch.ModelAxisVariant:
    return _variant(
        variant_id,
        base_id,
        group,
        short_threshold,
        long_threshold,
        feature_index=SUPERTREND_10_3_FEATURE_INDEX,
        side_filter_id="cooldown12_buy_downtrend_firewall",
        block_long_min=-1.5,
        block_long_max=-0.5,
        routed_fallback_enabled=routed_fallback_enabled,
        notes=notes,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _vol_low_variant(
        "nfac_c12_h08_s260l170_lvol_a",
        "nfac_c12_h08_s260l170_lvol",
        "cooldown12_buy_vol_low_firewall_aonly",
        0.260,
        0.170,
        routed_fallback_enabled=False,
        notes="run50AB attribution repair: block buy vol_low damage under actual 12-bar cooldown and hold8",
    ),
    _vol_low_variant(
        "nfac_c12_h08_s260l170_lvol_b",
        "nfac_c12_h08_s260l170_lvol",
        "cooldown12_buy_vol_low_firewall_tier_b_comparison",
        0.260,
        0.170,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for buy vol_low firewall under actual 12-bar cooldown and hold8",
    ),
    _vol_low_variant(
        "nfac_c12_h08_s240l150_lvol_a",
        "nfac_c12_h08_s240l150_lvol",
        "cooldown12_buy_vol_low_density_aonly",
        0.240,
        0.150,
        routed_fallback_enabled=False,
        notes="density pressure after buy vol_low firewall while preserving actual 12-bar cooldown",
    ),
    _vol_low_variant(
        "nfac_c12_h08_s240l150_lvol_b",
        "nfac_c12_h08_s240l150_lvol",
        "cooldown12_buy_vol_low_density_tier_b_comparison",
        0.240,
        0.150,
        routed_fallback_enabled=True,
        notes="matched A+B density comparison after buy vol_low firewall",
    ),
    _adx2025_variant(
        "nfac_c12_h08_s260l170_ladx2025_a",
        "nfac_c12_h08_s260l170_ladx2025",
        "cooldown12_buy_adx20_25_firewall_aonly",
        0.260,
        0.170,
        routed_fallback_enabled=False,
        notes="run50AB attribution repair: block only buy ADX 20-25 damage and preserve high-ADX buy opportunities",
    ),
    _adx2025_variant(
        "nfac_c12_h08_s260l170_ladx2025_b",
        "nfac_c12_h08_s260l170_ladx2025",
        "cooldown12_buy_adx20_25_firewall_tier_b_comparison",
        0.260,
        0.170,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for buy ADX 20-25 firewall",
    ),
    _downtrend_variant(
        "nfac_c12_h08_s260l170_ldown_a",
        "nfac_c12_h08_s260l170_ldown",
        "cooldown12_buy_downtrend_firewall_aonly",
        0.260,
        0.170,
        routed_fallback_enabled=False,
        notes="stress test OOS buy downtrend damage under actual 12-bar cooldown; validation risk is expected",
    ),
    _downtrend_variant(
        "nfac_c12_h08_s260l170_ldown_b",
        "nfac_c12_h08_s260l170_ldown",
        "cooldown12_buy_downtrend_firewall_tier_b_comparison",
        0.260,
        0.170,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for buy downtrend firewall",
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
