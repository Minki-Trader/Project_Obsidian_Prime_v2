from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50M"
PARENT_RUN_ID = "run50M_stage56_cooldown_threshold_interpolation_v1"
PACKET_ID = "stage56_run50M_cooldown_threshold_interpolation_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__CooldownThresholdInterpolation"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50M_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50M_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50M_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    batch.ModelAxisVariant(
        "nf150_c6_h10_s350l250_aonly",
        "nf150_c6_h10_s350l250",
        "cooldown_threshold_interpolation_aonly",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.350,
        0.250,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        False,
        reentry_cooldown_bars=6,
        notes="six-bar cooldown with lower thresholds to test whether OOS density can recover without further quality collapse",
    ),
    batch.ModelAxisVariant(
        "nf150_c6_h10_s350l250_b045",
        "nf150_c6_h10_s350l250",
        "cooldown_threshold_interpolation_tier_b_comparison",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.350,
        0.250,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        True,
        reentry_cooldown_bars=6,
        notes="matched six-bar cooldown A+B comparison for Tier B contribution and disablement read",
    ),
    batch.ModelAxisVariant(
        "nf150_c8_h10_s340l240_aonly",
        "nf150_c8_h10_s340l240",
        "cooldown_threshold_interpolation_aonly",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.340,
        0.240,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        False,
        reentry_cooldown_bars=8,
        notes="eight-bar cooldown interpolation to test whether same-move pressure can fall while retaining enough density",
    ),
    batch.ModelAxisVariant(
        "nf150_c8_h10_s340l240_b045",
        "nf150_c8_h10_s340l240",
        "cooldown_threshold_interpolation_tier_b_comparison",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.340,
        0.240,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        True,
        reentry_cooldown_bars=8,
        notes="matched eight-bar cooldown A+B comparison for Tier B contribution and disablement read",
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
