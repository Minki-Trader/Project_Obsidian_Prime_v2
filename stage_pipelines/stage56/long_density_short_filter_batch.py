from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import direction_repair_batch as batch  # noqa: E402


RUN_NUMBER = "run50H"
PARENT_RUN_ID = "run50H_stage56_long_density_short_filter_v1"
PACKET_ID = "stage56_run50H_long_density_short_filter_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__LongDensityShortFilter"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50H_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50H_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50H_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"


DEFAULT_VARIANTS: tuple[batch.DirectionVariant, ...] = (
    batch.DirectionVariant(
        "s390l320h06_aonly",
        "s390l320h06",
        "long_density_short_filter_disablement",
        0.390,
        0.320,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        False,
        notes="d390h10-quality short filter with lower long threshold; A-only matched comparison",
    ),
    batch.DirectionVariant(
        "s390l320h06_b045",
        "s390l320h06",
        "long_density_short_filter_comparison",
        0.390,
        0.320,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        True,
        notes="d390h10-quality short filter with lower long threshold plus strict Tier B",
    ),
    batch.DirectionVariant(
        "s400l320h06_aonly",
        "s400l320h06",
        "long_density_short_filter_disablement",
        0.400,
        0.320,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        False,
        notes="stronger short filter with lower long threshold; A-only matched comparison",
    ),
    batch.DirectionVariant(
        "s400l320h06_b045",
        "s400l320h06",
        "long_density_short_filter_comparison",
        0.400,
        0.320,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        True,
        notes="stronger short filter with lower long threshold plus strict Tier B",
    ),
    batch.DirectionVariant(
        "s410l315h06_aonly",
        "s410l315h06",
        "long_density_short_filter_disablement",
        0.410,
        0.315,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        False,
        notes="quality-heavy short filter with stronger long-density pressure; A-only matched comparison",
    ),
    batch.DirectionVariant(
        "s410l315h06_b045",
        "s410l315h06",
        "long_density_short_filter_comparison",
        0.410,
        0.315,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        True,
        notes="quality-heavy short filter with stronger long-density pressure plus strict Tier B",
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
