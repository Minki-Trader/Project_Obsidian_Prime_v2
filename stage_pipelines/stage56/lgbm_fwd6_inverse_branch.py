from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import lgbm_fwd6_density_branch as base


def configure_run50an() -> None:
    base.RUN_NUMBER = "run50AN"
    base.PARENT_RUN_ID = "run50AN_stage56_lgbm_fwd6_inverse_signal_probe_v1"
    base.PACKET_ID = "stage56_run50AN_lgbm_fwd6_inverse_signal_probe_v1"
    base.EXPLORATION_LABEL = "stage56_BaseEngine__LGBMFwd6InverseSignalProbe"
    base.RUN_ROOT = base.STAGE_ROOT / "02_runs" / base.RUN_NUMBER
    base.REPORT_PATH = base.REVIEWS_ROOT / "run50AN_reopen_batch.md"
    base.RESULTS_CSV_PATH = base.REVIEWS_ROOT / "run50AN_summary.csv"
    base.AUDIT_CSV_PATH = base.REVIEWS_ROOT / "run50AN_audit.csv"
    base.AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / base.PACKET_ID / "aggregate_summary.json"
    base.TRAINING_DATASET_ID = "training_fpmarkets_v2_us100_m5_label_v1_fwd6_split_v1_proxyw58_stage56_run50AN"
    base.MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd6_split_v1_proxyw58_feature_set_v2_stage56_run50AN"
    base.INPUT_ROOT = base.RUN_ROOT / "_inputs"
    base.TRAINING_OUTPUT_ROOT = base.INPUT_ROOT / "label_v1_fwd6_split_v1_proxyw58"
    base.MODEL_INPUT_OUTPUT_ROOT = base.INPUT_ROOT / "label_v1_fwd6_split_v1_feature_set_v2_mt5_price_proxy_58"
    base.DEFAULT_VARIANTS = (
        base.LgbmFwd6Variant(
            "inv6_s040l040_h3_b060",
            "inverse_high_density_symmetric",
            0.400,
            0.400,
            0.600,
            0.600,
            3,
            706,
            invert_signal=True,
            fallback_invert_signal=True,
            notes=(
                "invert fwd6 LGBM raw direction after run50AM systematic negative MT5 result; "
                "lower threshold and hold3 test whether inverse edge can recover real density"
            ),
        ),
        base.LgbmFwd6Variant(
            "inv6_s042l040_h3_b060",
            "inverse_short_firewall_density",
            0.420,
            0.400,
            0.600,
            0.600,
            3,
            707,
            invert_signal=True,
            fallback_invert_signal=True,
            notes="inverse fwd6 LGBM with a mild raw-short confidence firewall and hold3 density pressure",
        ),
        base.LgbmFwd6Variant(
            "inv6_s045l045_h3_b060",
            "inverse_mid_density_symmetric",
            0.450,
            0.450,
            0.600,
            0.600,
            3,
            708,
            invert_signal=True,
            fallback_invert_signal=True,
            notes="inverse fwd6 LGBM with run50AM dense threshold but shorter hold3 lifecycle",
        ),
        base.LgbmFwd6Variant(
            "inv6_s048l045_h4_b060",
            "inverse_run50am_direct_comparison",
            0.480,
            0.450,
            0.600,
            0.600,
            4,
            709,
            invert_signal=True,
            fallback_invert_signal=True,
            notes="direct inversion of run50AM asym hold4 variant to measure whether raw negativity is exploitable",
        ),
    )


def main(argv: list[str] | None = None) -> int:
    configure_run50an()
    return base.main(sys.argv[1:] if argv is None else argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
