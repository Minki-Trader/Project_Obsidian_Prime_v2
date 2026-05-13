from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import direction_repair_batch as batch  # noqa: E402


RUN_NUMBER = "run50I"
PARENT_RUN_ID = "run50I_stage56_early_mid_session_direction_v1"
PACKET_ID = "stage56_run50I_early_mid_session_direction_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__EarlyMidSessionDirection"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50I_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50I_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50I_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"


DEFAULT_VARIANTS: tuple[batch.DirectionVariant, ...] = (
    batch.DirectionVariant(
        "em_s390l300h06_aonly",
        "em_s390l300h06",
        "early_mid_session_direction_disablement",
        0.390,
        0.300,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        False,
        session_slice_id="early_mid",
        notes="early+mid session, lower long threshold, A-only matched comparison",
    ),
    batch.DirectionVariant(
        "em_s390l300h06_b045",
        "em_s390l300h06",
        "early_mid_session_direction_comparison",
        0.390,
        0.300,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        True,
        session_slice_id="early_mid",
        notes="early+mid session, lower long threshold, strict Tier B",
    ),
    batch.DirectionVariant(
        "em_s400l290h06_aonly",
        "em_s400l290h06",
        "early_mid_session_direction_disablement",
        0.400,
        0.290,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        False,
        session_slice_id="early_mid",
        notes="early+mid session, stronger short filter, stronger long-density pressure, A-only matched comparison",
    ),
    batch.DirectionVariant(
        "em_s400l290h06_b045",
        "em_s400l290h06",
        "early_mid_session_direction_comparison",
        0.400,
        0.290,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        True,
        session_slice_id="early_mid",
        notes="early+mid session, stronger short filter, stronger long-density pressure, strict Tier B",
    ),
    batch.DirectionVariant(
        "em_s410l285h06_aonly",
        "em_s410l285h06",
        "early_mid_session_direction_disablement",
        0.410,
        0.285,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        False,
        session_slice_id="early_mid",
        notes="early+mid session, quality-heavy short filter, maximum long-density pressure, A-only matched comparison",
    ),
    batch.DirectionVariant(
        "em_s410l285h06_b045",
        "em_s410l285h06",
        "early_mid_session_direction_comparison",
        0.410,
        0.285,
        0.0,
        0.450,
        0.450,
        0.0,
        6,
        True,
        session_slice_id="early_mid",
        notes="early+mid session, quality-heavy short filter, maximum long-density pressure, strict Tier B",
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
