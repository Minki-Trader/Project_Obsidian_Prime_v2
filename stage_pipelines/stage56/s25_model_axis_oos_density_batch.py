from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage56 import model_axis_batch as batch  # noqa: E402


RUN_NUMBER = "run50AH"
PARENT_RUN_ID = "run50AH_stage56_s25_model_axis_oos_density_v1"
PACKET_ID = "stage56_run50AH_s25_model_axis_oos_density_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__S25ModelAxisOosDensity"
STAGE_ROOT = batch.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = batch.REVIEWS_ROOT
REPORT_PATH = REVIEWS_ROOT / "run50AH_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50AH_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50AH_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"

ADX_14_FEATURE_INDEX = 34


def _variant(
    variant_id: str,
    base_id: str,
    group: str,
    *,
    model_spec_id: str,
    c_value: float,
    flat_sample_weight: float | None,
    nonflat_sample_weight: float | None,
    class_weight: str | None = None,
    train_start_utc: str | None = None,
    routed_fallback_enabled: bool,
    notes: str,
) -> batch.ModelAxisVariant:
    return batch.ModelAxisVariant(
        variant_id,
        base_id,
        group,
        model_spec_id,
        c_value,
        class_weight,
        flat_sample_weight,
        nonflat_sample_weight,
        train_start_utc,
        0.260,
        0.170,
        0.0,
        0.450,
        0.450,
        0.0,
        8,
        routed_fallback_enabled,
        reentry_cooldown_bars=8,
        side_filter_id="s25_model_axis_c08",
        side_filter_enabled=True,
        tier_a_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        tier_b_side_filter_feature_index=ADX_14_FEATURE_INDEX,
        block_short_feature_range=True,
        block_short_feature_min=20.0,
        block_short_feature_max=25.0,
        block_long_feature_range=False,
        block_long_feature_min=0.0,
        block_long_feature_max=0.0,
        tier_b_allowed_subtypes=("B_core_only", "B_mixed_partial_context"),
        notes=notes,
    )


DEFAULT_VARIANTS: tuple[batch.ModelAxisVariant, ...] = (
    _variant(
        "c025s25a",
        "c025s25",
        "s25_model_axis_c025_aonly",
        model_spec_id="logreg_nonflat_weight_c025_flat070_nonflat150",
        c_value=0.25,
        flat_sample_weight=0.70,
        nonflat_sample_weight=1.50,
        routed_fallback_enabled=False,
        notes="A-only C=0.25 model-axis perturbation after run50AG threshold saturation",
    ),
    _variant(
        "c025s25b",
        "c025s25",
        "s25_model_axis_c025_tier_b_comparison",
        model_spec_id="logreg_nonflat_weight_c025_flat070_nonflat150",
        c_value=0.25,
        flat_sample_weight=0.70,
        nonflat_sample_weight=1.50,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for C=0.25 s25 model-axis perturbation",
    ),
    _variant(
        "c100s25a",
        "c100s25",
        "s25_model_axis_c100_aonly",
        model_spec_id="logreg_nonflat_weight_c100_flat070_nonflat150",
        c_value=1.00,
        flat_sample_weight=0.70,
        nonflat_sample_weight=1.50,
        routed_fallback_enabled=False,
        notes="A-only C=1.00 model-axis perturbation to change probability ranking without lowering thresholds",
    ),
    _variant(
        "c100s25b",
        "c100s25",
        "s25_model_axis_c100_tier_b_comparison",
        model_spec_id="logreg_nonflat_weight_c100_flat070_nonflat150",
        c_value=1.00,
        flat_sample_weight=0.70,
        nonflat_sample_weight=1.50,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for C=1.00 s25 model-axis perturbation",
    ),
    _variant(
        "nf200s25a",
        "nf200s25",
        "s25_model_axis_nonflat200_aonly",
        model_spec_id="logreg_nonflat_weight_c050_flat060_nonflat200",
        c_value=0.50,
        flat_sample_weight=0.60,
        nonflat_sample_weight=2.00,
        routed_fallback_enabled=False,
        notes="A-only stronger non-flat weighting to open OOS density without same threshold relaxation",
    ),
    _variant(
        "nf200s25b",
        "nf200s25",
        "s25_model_axis_nonflat200_tier_b_comparison",
        model_spec_id="logreg_nonflat_weight_c050_flat060_nonflat200",
        c_value=0.50,
        flat_sample_weight=0.60,
        nonflat_sample_weight=2.00,
        routed_fallback_enabled=True,
        notes="matched A+B comparison for stronger non-flat weighting",
    ),
    _variant(
        "r23s25a",
        "r23s25",
        "s25_model_axis_recent2023_aonly",
        model_spec_id="logreg_recent2023_balanced_c050_s25",
        c_value=0.50,
        flat_sample_weight=None,
        nonflat_sample_weight=None,
        class_weight="balanced",
        train_start_utc="2023-01-01T00:00:00Z",
        routed_fallback_enabled=False,
        notes="A-only recent-2023 balanced model-axis perturbation after run50AG OOS density stall",
    ),
    _variant(
        "r23s25b",
        "r23s25",
        "s25_model_axis_recent2023_tier_b_comparison",
        model_spec_id="logreg_recent2023_balanced_c050_s25",
        c_value=0.50,
        flat_sample_weight=None,
        nonflat_sample_weight=None,
        class_weight="balanced",
        train_start_utc="2023-01-01T00:00:00Z",
        routed_fallback_enabled=True,
        notes="matched A+B comparison for recent-2023 balanced s25 model-axis perturbation",
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
