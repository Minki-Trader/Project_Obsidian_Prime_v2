from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50AB"
PARENT_RUN_ID = "run50AB_stage56_cooldown12_density_repair_v1"
PACKET_ID = "stage56_run50AB_cooldown12_density_repair_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__Cooldown12DensityRepair"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50AB_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50AB_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50AB_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    max_hold_bars: int,
    *,
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
        max_hold_bars,
        routed_fallback_enabled,
        reentry_cooldown_bars=12,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "nfab_c12_h10_s300l210_a",
        "nfab_c12_h10_s300l210",
        "cooldown12_hold10_density_aonly",
        0.300,
        0.210,
        10,
        routed_fallback_enabled=False,
        notes="lower thresholds under actual 12-bar cooldown and hold10 to test whether real density recovers without same-move splitting",
    ),
    _variant(
        "nfab_c12_h10_s300l210_b",
        "nfab_c12_h10_s300l210",
        "cooldown12_hold10_density_tier_b_comparison",
        0.300,
        0.210,
        10,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for Tier B disablement under cooldown12 hold10 density repair",
    ),
    _variant(
        "nfab_c12_h08_s300l210_a",
        "nfab_c12_h08_s300l210",
        "cooldown12_hold8_density_aonly",
        0.300,
        0.210,
        8,
        routed_fallback_enabled=False,
        notes="hold8 with actual 12-bar cooldown to recover density while keeping the cooldown audit strict",
    ),
    _variant(
        "nfab_c12_h08_s300l210_b",
        "nfab_c12_h08_s300l210",
        "cooldown12_hold8_density_tier_b_comparison",
        0.300,
        0.210,
        8,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for Tier B disablement under cooldown12 hold8 density repair",
    ),
    _variant(
        "nfab_c12_h06_s300l210_a",
        "nfab_c12_h06_s300l210",
        "cooldown12_hold6_density_aonly",
        0.300,
        0.210,
        6,
        routed_fallback_enabled=False,
        notes="hold6 with actual 12-bar cooldown to test the highest density recovery that still faces the same-move audit",
    ),
    _variant(
        "nfab_c12_h06_s300l210_b",
        "nfab_c12_h06_s300l210",
        "cooldown12_hold6_density_tier_b_comparison",
        0.300,
        0.210,
        6,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for Tier B disablement under cooldown12 hold6 density repair",
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
