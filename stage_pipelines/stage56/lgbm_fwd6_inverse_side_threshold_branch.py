from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import lgbm_fwd6_density_branch as base


def configure_run50ao() -> None:
    base.RUN_NUMBER = "run50AO"
    base.PARENT_RUN_ID = "run50AO_stage56_lgbm_fwd6_inverse_side_threshold_repair_v1"
    base.PACKET_ID = "stage56_run50AO_lgbm_fwd6_inverse_side_threshold_repair_v1"
    base.EXPLORATION_LABEL = "stage56_BaseEngine__LGBMFwd6InverseSideThresholdRepair"
    base.RUN_ROOT = base.STAGE_ROOT / "02_runs" / base.RUN_NUMBER
    base.REPORT_PATH = base.REVIEWS_ROOT / "run50AO_reopen_batch.md"
    base.RESULTS_CSV_PATH = base.REVIEWS_ROOT / "run50AO_summary.csv"
    base.AUDIT_CSV_PATH = base.REVIEWS_ROOT / "run50AO_audit.csv"
    base.AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / base.PACKET_ID / "aggregate_summary.json"
    base.TRAINING_DATASET_ID = "training_fpmarkets_v2_us100_m5_label_v1_fwd6_split_v1_proxyw58_stage56_run50AO"
    base.MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd6_split_v1_proxyw58_feature_set_v2_stage56_run50AO"
    base.INPUT_ROOT = base.RUN_ROOT / "_inputs"
    base.TRAINING_OUTPUT_ROOT = base.INPUT_ROOT / "label_v1_fwd6_split_v1_proxyw58"
    base.MODEL_INPUT_OUTPUT_ROOT = base.INPUT_ROOT / "label_v1_fwd6_split_v1_feature_set_v2_mt5_price_proxy_58"
    base.DEFAULT_VARIANTS = (
        base.LgbmFwd6Variant(
            "inv6_s048l045_h3_b060",
            "inverse_short_firewall_hold3",
            0.480,
            0.450,
            0.600,
            0.600,
            3,
            710,
            invert_signal=True,
            fallback_invert_signal=True,
            notes="run50AN attribution repair: keep hold3 density while raising inverse short threshold to the hold4 quality frontier",
        ),
        base.LgbmFwd6Variant(
            "inv6_s050l045_h3_b060",
            "inverse_stronger_short_firewall_hold3",
            0.500,
            0.450,
            0.600,
            0.600,
            3,
            711,
            invert_signal=True,
            fallback_invert_signal=True,
            notes="test whether stricter short threshold removes OOS sell damage without losing long-side density",
        ),
        base.LgbmFwd6Variant(
            "inv6_s052l045_h3_b060",
            "inverse_max_short_firewall_hold3",
            0.520,
            0.450,
            0.600,
            0.600,
            3,
            712,
            invert_signal=True,
            fallback_invert_signal=True,
            notes="upper short-threshold stress to see whether sell side should be sparse or effectively disabled",
        ),
        base.LgbmFwd6Variant(
            "inv6_s048l043_h3_b060",
            "inverse_long_density_restore_hold3",
            0.480,
            0.430,
            0.600,
            0.600,
            3,
            713,
            invert_signal=True,
            fallback_invert_signal=True,
            notes="restore long-side density after short firewall; checks whether positive OOS buy contribution survives lower long threshold",
        ),
        base.LgbmFwd6Variant(
            "inv6_s050l043_h3_b060",
            "inverse_firewall_long_density_hold3",
            0.500,
            0.430,
            0.600,
            0.600,
            3,
            714,
            invert_signal=True,
            fallback_invert_signal=True,
            notes="paired short-firewall plus long-density restoration candidate for OOS density and PF survival",
        ),
    )


def main(argv: list[str] | None = None) -> int:
    configure_run50ao()
    return base.main(sys.argv[1:] if argv is None else argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
