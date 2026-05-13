from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import lgbm_fwd6_density_branch as base


def configure_run50ap() -> None:
    base.RUN_NUMBER = "run50AP"
    base.PARENT_RUN_ID = "run50AP_stage56_lgbm_fwd3_new_source_real_density_v1"
    base.PACKET_ID = "stage56_run50AP_lgbm_fwd3_new_source_real_density_v1"
    base.EXPLORATION_LABEL = "stage56_BaseEngine__LGBMFwd3NewSourceRealDensity"
    base.RUN_ROOT = base.STAGE_ROOT / "02_runs" / base.RUN_NUMBER
    base.REPORT_PATH = base.REVIEWS_ROOT / "run50AP_reopen_batch.md"
    base.RESULTS_CSV_PATH = base.REVIEWS_ROOT / "run50AP_summary.csv"
    base.AUDIT_CSV_PATH = base.REVIEWS_ROOT / "run50AP_audit.csv"
    base.AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / base.PACKET_ID / "aggregate_summary.json"
    base.LABEL_ID = "label_v1_fwd3_m5_logret_train_q33_3class"
    base.LABEL_HORIZON_BARS = 3
    base.MODEL_SOURCE_TAG = "lgbm_fwd3"
    base.INPUT_MANIFEST_NAME = "fwd3_input_manifest.json"
    base.TRAINING_DATASET_ID = "training_fpmarkets_v2_us100_m5_label_v1_fwd3_split_v1_proxyw58_stage56_run50AP"
    base.MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd3_split_v1_proxyw58_feature_set_v2_stage56_run50AP"
    base.INPUT_ROOT = base.RUN_ROOT / "_inputs"
    base.TRAINING_OUTPUT_ROOT = base.INPUT_ROOT / "label_v1_fwd3_split_v1_proxyw58"
    base.MODEL_INPUT_OUTPUT_ROOT = base.INPUT_ROOT / "label_v1_fwd3_split_v1_feature_set_v2_mt5_price_proxy_58"
    base.DEFAULT_VARIANTS = (
        base.LgbmFwd6Variant(
            "raw3_s045l045_h3_b060",
            "fwd3_raw_direction_control",
            0.450,
            0.450,
            0.600,
            0.600,
            3,
            720,
            notes="raw fwd3 LGBM control to test whether shorter horizon keeps model direction or still needs inversion",
        ),
        base.LgbmFwd6Variant(
            "inv3_s045l045_h3_b060",
            "fwd3_inverse_symmetric",
            0.450,
            0.450,
            0.600,
            0.600,
            3,
            721,
            invert_signal=True,
            fallback_invert_signal=True,
            notes="inverse fwd3 symmetric threshold; checks whether shorter horizon creates real density without relaxing thresholds",
        ),
        base.LgbmFwd6Variant(
            "inv3_s050l043_h3_b060",
            "fwd3_inverse_side_threshold",
            0.500,
            0.430,
            0.600,
            0.600,
            3,
            722,
            invert_signal=True,
            fallback_invert_signal=True,
            notes="carry run50AO side-threshold idea onto a shorter label horizon to test real OOS density survival",
        ),
        base.LgbmFwd6Variant(
            "inv3_s048l040_h2_b060",
            "fwd3_inverse_long_density_hold2",
            0.480,
            0.400,
            0.600,
            0.600,
            2,
            723,
            invert_signal=True,
            fallback_invert_signal=True,
            notes="shorter hold2 with long-side density pressure; tests whether same-move split ratio falls when lifecycle is tighter",
        ),
        base.LgbmFwd6Variant(
            "inv3_s050l040_h2_b060",
            "fwd3_inverse_firewall_long_density_hold2",
            0.500,
            0.400,
            0.600,
            0.600,
            2,
            724,
            invert_signal=True,
            fallback_invert_signal=True,
            notes="short firewall plus long-density hold2 stress for OOS density and cost-stressed expectancy",
        ),
    )


def main(argv: list[str] | None = None) -> int:
    configure_run50ap()
    return base.main(sys.argv[1:] if argv is None else argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
