from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50L"
PARENT_RUN_ID = "run50L_stage56_lifecycle_cooldown_model_axis_v1"
PACKET_ID = "stage56_run50L_lifecycle_cooldown_model_axis_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__LifecycleCooldownModelAxis"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50L_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50L_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50L_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    batch.ModelAxisVariant(
        "nf150_c6_h10_s370l270_aonly",
        "nf150_c6_h10_s370l270",
        "lifecycle_cooldown_model_axis_aonly",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.370,
        0.270,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        False,
        reentry_cooldown_bars=6,
        notes="six-bar actual reentry cooldown with lower thresholds to test whether real density survives without same-move splitting",
    ),
    batch.ModelAxisVariant(
        "nf150_c6_h10_s370l270_b045",
        "nf150_c6_h10_s370l270",
        "lifecycle_cooldown_model_axis_tier_b_comparison",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.370,
        0.270,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        True,
        reentry_cooldown_bars=6,
        notes="matched six-bar cooldown A+B comparison for Tier B disablement evidence",
    ),
    batch.ModelAxisVariant(
        "nf150_c12_h10_s330l240_aonly",
        "nf150_c12_h10_s330l240",
        "lifecycle_cooldown_model_axis_aonly",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.330,
        0.240,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        False,
        reentry_cooldown_bars=12,
        notes="twelve-bar actual reentry cooldown with stronger density pressure",
    ),
    batch.ModelAxisVariant(
        "nf150_c12_h10_s330l240_b045",
        "nf150_c12_h10_s330l240",
        "lifecycle_cooldown_model_axis_tier_b_comparison",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.330,
        0.240,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        True,
        reentry_cooldown_bars=12,
        notes="matched twelve-bar cooldown A+B comparison for Tier B disablement evidence",
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
