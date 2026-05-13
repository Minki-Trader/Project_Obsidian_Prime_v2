from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50AL"
PARENT_RUN_ID = "run50AL_stage56_entry_confidence_rearm_v1"
PACKET_ID = "stage56_run50AL_entry_confidence_rearm_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__EntryConfidenceRearm"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50AL_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50AL_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50AL_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    short_threshold: float,
    long_threshold: float,
    rearm_delta: float,
    *,
    block_long: bool = False,
    long_block_min: float = 40.0,
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
        entry_transition_only=True,
        entry_transition_rearm_min_confidence_delta=rearm_delta,
        side_filter_id="entry_rearm_directional_adx_soft_firewall",
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        tier_b_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        block_short_feature_range=True,
        block_short_feature_min=20.0,
        block_short_feature_max=30.0,
        block_long_feature_range=block_long,
        block_long_feature_min=long_block_min,
        block_long_feature_max=1000.0,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "nfal_s33l20_r020",
        "nfx_s33l20_c3_s2030",
        "entry_rearm_delta020_anchor",
        0.330,
        0.200,
        0.020,
        notes="run50X anchor with transition gate rearmed by 0.020 confidence rise",
    ),
    _variant(
        "nfal_s33l20_r040",
        "nfx_s33l20_c3_s2030",
        "entry_rearm_delta040_anchor",
        0.330,
        0.200,
        0.040,
        notes="run50X anchor with stricter 0.040 confidence pulse rearm",
    ),
    _variant(
        "nfal_s33l20_r060",
        "nfx_s33l20_c3_s2030",
        "entry_rearm_delta060_anchor",
        0.330,
        0.200,
        0.060,
        notes="run50X anchor with sparse 0.060 confidence pulse rearm",
    ),
    _variant(
        "nfal_s33l20_r040l40",
        "nfx_s33l20_c3_s2030l40",
        "entry_rearm_delta040_long_firewall",
        0.330,
        0.200,
        0.040,
        block_long=True,
        long_block_min=40.0,
        notes="confidence rearm plus long ADX 40+ OOS damage firewall",
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
