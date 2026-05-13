from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import direction_repair_batch as batch  # noqa: E402


RUN_NUMBER = "run50J"
PARENT_RUN_ID = "run50J_stage56_hold_extension_direction_v1"
PACKET_ID = "stage56_run50J_hold_extension_direction_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__HoldExtensionDirection"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50J_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50J_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50J_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"


DEFAULT_VARIANTS: tuple[batch.DirectionVariant, ...] = (
    batch.DirectionVariant(
        "h10_s390l300_aonly",
        "h10_s390l300",
        "hold_extension_direction_disablement",
        0.390,
        0.300,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        False,
        notes="hold extension to test whether density survives without same-move split; A-only matched comparison",
    ),
    batch.DirectionVariant(
        "h10_s390l300_b045",
        "h10_s390l300",
        "hold_extension_direction_comparison",
        0.390,
        0.300,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        True,
        notes="hold extension with strict Tier B comparison",
    ),
    batch.DirectionVariant(
        "h10_s400l295_aonly",
        "h10_s400l295",
        "hold_extension_direction_disablement",
        0.400,
        0.295,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        False,
        notes="stronger short filter plus long-density pressure under longer hold; A-only matched comparison",
    ),
    batch.DirectionVariant(
        "h10_s400l295_b045",
        "h10_s400l295",
        "hold_extension_direction_comparison",
        0.400,
        0.295,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        True,
        notes="stronger short filter plus long-density pressure under longer hold with strict Tier B",
    ),
    batch.DirectionVariant(
        "h10_s410l290_aonly",
        "h10_s410l290",
        "hold_extension_direction_disablement",
        0.410,
        0.290,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        False,
        notes="quality-heavy short filter plus maximum long-density pressure under longer hold; A-only matched comparison",
    ),
    batch.DirectionVariant(
        "h10_s410l290_b045",
        "h10_s410l290",
        "hold_extension_direction_comparison",
        0.410,
        0.290,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        True,
        notes="quality-heavy short filter plus maximum long-density pressure under longer hold with strict Tier B",
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
