from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import independent_event_source_route_branch as source  # noqa: E402


RUN_NUMBER = "run50BJ"
PARENT_RUN_ID = "run50BJ_stage56_independent_event_source_cooldown_sweep_v1"
PACKET_ID = "stage56_run50BJ_independent_event_source_cooldown_sweep_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__IndependentEventSourceCooldownSweep"
RUN_ROOT = source.STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = source.REVIEWS_ROOT / "run50BJ_independent_event_source_cooldown_sweep.md"
RESULTS_CSV_PATH = source.REVIEWS_ROOT / "run50BJ_summary.csv"
AUDIT_CSV_PATH = source.REVIEWS_ROOT / "run50BJ_audit.csv"
SOURCE_SUMMARY_CSV_PATH = source.REVIEWS_ROOT / "run50BJ_source_summary.csv"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_independent_event_source_cooldown_sweep"


DEFAULT_VARIANTS: tuple[source.SourceVariant, ...] = (
    source.SourceVariant(
        variant_id="s45c04_h4c0",
        source_stage_number=45,
        source_candidate_id="c04_histvol_ratio_expansion",
        group="stage45_volatility_expansion_raw_density",
        max_hold_bars=4,
        reentry_cooldown_bars=0,
        routed_fallback_enabled=True,
        notes="Run50AW c6 source had validation density but OOS density shortage; c0 tests raw independent-event density before cooldown pressure.",
    ),
    source.SourceVariant(
        variant_id="s45c04_h4c2",
        source_stage_number=45,
        source_candidate_id="c04_histvol_ratio_expansion",
        group="stage45_volatility_expansion_microcooldown",
        max_hold_bars=4,
        reentry_cooldown_bars=2,
        routed_fallback_enabled=True,
        notes="Cooldown2 interpolation for the Stage45 volatility expansion source.",
    ),
    source.SourceVariant(
        variant_id="s45c04_h4c4",
        source_stage_number=45,
        source_candidate_id="c04_histvol_ratio_expansion",
        group="stage45_volatility_expansion_cooldown_stress",
        max_hold_bars=4,
        reentry_cooldown_bars=4,
        routed_fallback_enabled=True,
        notes="Cooldown4 stress for the Stage45 volatility expansion source; checks whether real density survives without c6 collapse.",
    ),
    source.SourceVariant(
        variant_id="s47c03_h4c0",
        source_stage_number=47,
        source_candidate_id="c03_majority_agreement",
        group="stage47_meta_majority_raw_density",
        max_hold_bars=4,
        reentry_cooldown_bars=0,
        routed_fallback_enabled=True,
        notes="Stage47 majority agreement raw-density check; tests whether consensus source is less same-move dominated than ExtraTrees thresholds.",
    ),
    source.SourceVariant(
        variant_id="s47c03_h4c2",
        source_stage_number=47,
        source_candidate_id="c03_majority_agreement",
        group="stage47_meta_majority_microcooldown",
        max_hold_bars=4,
        reentry_cooldown_bars=2,
        routed_fallback_enabled=True,
        notes="Cooldown2 check for Stage47 majority agreement source.",
    ),
    source.SourceVariant(
        variant_id="s43c02_h4c0",
        source_stage_number=43,
        source_candidate_id="c02_top8_stability_ranked_elasticnet",
        group="stage43_low_complexity_raw_density",
        max_hold_bars=4,
        reentry_cooldown_bars=0,
        routed_fallback_enabled=True,
        notes="Stage43 low-complexity raw-density check; tests whether a simpler source gives cleaner route coverage.",
    ),
)


def main(argv: list[str] | None = None) -> int:
    source.RUN_NUMBER = RUN_NUMBER
    source.PARENT_RUN_ID = PARENT_RUN_ID
    source.PACKET_ID = PACKET_ID
    source.EXPLORATION_LABEL = EXPLORATION_LABEL
    source.RUN_ROOT = RUN_ROOT
    source.REPORT_PATH = REPORT_PATH
    source.RESULTS_CSV_PATH = RESULTS_CSV_PATH
    source.AUDIT_CSV_PATH = AUDIT_CSV_PATH
    source.SOURCE_SUMMARY_CSV_PATH = SOURCE_SUMMARY_CSV_PATH
    source.PACKET_ROOT = PACKET_ROOT
    source.AGGREGATE_SUMMARY_PATH = AGGREGATE_SUMMARY_PATH
    source.COMMON_ROOT = COMMON_ROOT
    source.DEFAULT_VARIANTS = DEFAULT_VARIANTS
    return source.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
