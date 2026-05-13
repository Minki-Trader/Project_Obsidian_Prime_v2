from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import cooldown_repair_batch as batch  # noqa: E402


RUN_NUMBER = "run50O"
PARENT_RUN_ID = "run50O_stage56_hold6_side_adx_density_v1"
PACKET_ID = "stage56_run50O_hold6_side_adx_density_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__Hold6SideAdxDensity"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50O_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50O_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50O_audit.csv"
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


DEFAULT_VARIANTS: tuple[batch.CooldownVariant, ...] = (
    batch.CooldownVariant(
        "d340h06_sadx_c0_aonly",
        "hold6_side_adx_density_aonly",
        0.340,
        0.340,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        0,
        routed_fallback_enabled=False,
        notes="hold6 density frontier with short ADX 20-25 block and Tier B disabled for matched comparison",
        **SIDE_FILTER_KWARGS,
    ),
    batch.CooldownVariant(
        "d340h06_sadx_c0_b045",
        "hold6_side_adx_density_tier_b_comparison",
        0.340,
        0.340,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        0,
        routed_fallback_enabled=True,
        notes="hold6 density frontier with short ADX 20-25 block and B045 fallback",
        **SIDE_FILTER_KWARGS,
    ),
    batch.CooldownVariant(
        "d320h06_sadx_c0_aonly",
        "hold6_side_adx_density_aonly",
        0.320,
        0.320,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        0,
        routed_fallback_enabled=False,
        notes="extra hold6 density pressure after short ADX block with Tier B disabled",
        **SIDE_FILTER_KWARGS,
    ),
    batch.CooldownVariant(
        "d320h06_sadx_c0_b045",
        "hold6_side_adx_density_tier_b_comparison",
        0.320,
        0.320,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        0,
        routed_fallback_enabled=True,
        notes="extra hold6 density pressure after short ADX block with B045 fallback",
        **SIDE_FILTER_KWARGS,
    ),
    batch.CooldownVariant(
        "d315h06_sadx_c1_aonly",
        "hold6_side_adx_cooldown_aonly",
        0.315,
        0.315,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        1,
        routed_fallback_enabled=False,
        notes="one-bar cooldown survival test with short ADX block and Tier B disabled",
        **SIDE_FILTER_KWARGS,
    ),
    batch.CooldownVariant(
        "d315h06_sadx_c1_b045",
        "hold6_side_adx_cooldown_tier_b_comparison",
        0.315,
        0.315,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        1,
        routed_fallback_enabled=True,
        notes="one-bar cooldown survival test with short ADX block and B045 fallback",
        **SIDE_FILTER_KWARGS,
    ),
)


def main(argv: list[str] | None = None) -> int:
    for module in (batch, batch.deep, batch.reopen):
        module.RUN_NUMBER = RUN_NUMBER
        module.PARENT_RUN_ID = PARENT_RUN_ID
        module.PACKET_ID = PACKET_ID
        module.EXPLORATION_LABEL = EXPLORATION_LABEL
        module.RUN_ROOT = RUN_ROOT
        module.REPORT_PATH = REPORT_PATH
        module.RESULTS_CSV_PATH = RESULTS_CSV_PATH
        module.AUDIT_CSV_PATH = AUDIT_CSV_PATH
        module.AGGREGATE_SUMMARY_PATH = AGGREGATE_SUMMARY_PATH
        module.STAGE_RUN_LEDGER_PATH = batch.STAGE_RUN_LEDGER_PATH
        module.PROJECT_ALPHA_LEDGER_PATH = batch.PROJECT_ALPHA_LEDGER_PATH
        module.RUN_REGISTRY_PATH = batch.RUN_REGISTRY_PATH
    batch.DEFAULT_VARIANTS = DEFAULT_VARIANTS
    return batch.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
