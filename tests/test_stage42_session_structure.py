from __future__ import annotations

from pathlib import Path

import pandas as pd

from foundation.features.session_structure import (
    SIGNAL_FEATURE_ORDER,
    apply_candidate_to_table,
    build_reference_thresholds,
    build_session_reliability_model,
    build_stage42_broad_candidate_grid,
    materialize_session_structure,
    per_session_attribution,
    session_concentration_rejection,
    session_distribution,
)
from stage_pipelines.stage42.session_structure_signal_reliability_probe import (
    RUN_ID,
    STAGE_NUMBER,
    make_attempts,
)


def _base_frame() -> pd.DataFrame:
    timestamps = pd.date_range("2025-01-02T16:35:00Z", periods=90, freq="5min")
    minutes = [(idx * 5) % 390 for idx in range(90)]
    frame = pd.DataFrame(
        {
            "timestamp": timestamps,
            "split": ["train"] * 50 + ["validation"] * 20 + ["oos"] * 20,
            "minutes_from_cash_open": minutes,
            "return_zscore_20": [1.2, -1.3, 0.1, 0.9, -0.8] * 18,
            "adx_14": [28.0, 30.0, 10.0, 26.0, 27.0] * 18,
            "historical_vol_20": [0.001, 0.002, 0.0015] * 30,
            "stage42_spread_points": [150, 160, 180] * 30,
            "label_class": [2, 0, 1, 2, 0] * 18,
            "tier_label": ["Tier A"] * 45 + ["Tier B"] * 45,
            "routing_source": ["tier_a_primary"] * 45 + ["tier_b_fallback"] * 45,
            "partial_context_subtype": ["Tier_A_full_context"] * 45 + ["missing_secondary_context"] * 45,
        }
    )
    frame["timestamp_utc"] = frame["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return frame


def test_session_feature_materialization_uses_closed_bar_bucket_rules() -> None:
    frame = materialize_session_structure(_base_frame())

    assert frame.loc[0, "stage42_session_bucket_label"] == "overnight_or_unmapped"
    assert frame.loc[1, "stage42_session_bucket_label"] == "cash_open_0_30"
    assert frame.loc[12, "stage42_session_bucket_label"] == "early_cash_30_60"
    assert frame.loc[72, "stage42_session_bucket_label"] == "cash_close_330_390"
    assert frame.loc[1, "stage42_first_30_minutes_flag"] == 1
    assert frame.loc[72, "stage42_last_60_minutes_flag"] == 1


def test_timezone_columns_keep_broker_key_and_add_utc_event_time() -> None:
    frame = materialize_session_structure(_base_frame().head(3))

    assert "stage42_broker_server_timestamp" in frame.columns
    assert "stage42_timestamp_utc" in frame.columns
    assert frame["stage42_timestamp_timezone_rule"].iloc[0] == "broker_clock_key_to_event_utc"
    assert str(frame["stage42_broker_clock_timezone"].iloc[0]) == "Europe/Athens"


def test_candidate_grid_has_required_session_families() -> None:
    specs = build_stage42_broad_candidate_grid()
    ids = [spec.candidate_id for spec in specs]

    assert len(ids) == 17
    assert ids[0] == "c01_reference_no_session_structure"
    assert "c09_session_specific_thresholds" in ids
    assert "c16_direction_specific_session_model" in ids
    assert "c17_session_extreme_stress" in ids


def test_reliability_candidate_changes_signal_by_session_bucket() -> None:
    common = materialize_session_structure(_base_frame())
    thresholds = build_reference_thresholds(common)
    model = build_session_reliability_model(common, thresholds)
    spec = next(item for item in build_stage42_broad_candidate_grid() if item.candidate_id == "c13_session_reliability_score")

    scored = apply_candidate_to_table(common, spec, thresholds, model)

    assert "stage42_session_reliability_signal" in scored.columns
    assert set(scored["stage42_session_reliability_signal"].unique()).issubset({-1, 0, 1})
    assert "weakest_bucket" in model


def test_session_distribution_and_attribution_are_split_aware() -> None:
    common = materialize_session_structure(_base_frame())
    thresholds = build_reference_thresholds(common)
    model = build_session_reliability_model(common, thresholds)
    spec = build_stage42_broad_candidate_grid()[0]
    scored = apply_candidate_to_table(common, spec, thresholds, model)
    distribution = session_distribution(scored)
    attribution = per_session_attribution(scored, spec.candidate_id)

    assert "train" in distribution
    assert any(row["split"] == "validation_is" for row in attribution)
    assert all(row["candidate_id"] == spec.candidate_id for row in attribution)


def test_session_concentration_rejection_flags_thin_or_single_bucket() -> None:
    assert session_concentration_rejection({"actual_routed_total_count": 5, "session_concentration_share": 0.20}) == "session_bucket_trade_count_too_thin"
    assert session_concentration_rejection({"actual_routed_total_count": 50, "session_concentration_share": 0.90}) == "one_session_concentration_too_high"
    assert session_concentration_rejection({"actual_routed_total_count": 50, "session_concentration_share": 0.40}) is None


def test_attempt_manifest_uses_stage42_signal_score_table(tmp_path: Path) -> None:
    spec = build_stage42_broad_candidate_grid()[0]
    frame = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2025-01-02T16:35:00Z", "2025-01-02T16:40:00Z"], utc=True),
            "split": ["validation", "oos"],
            "tier_label": ["Tier A", "Tier A"],
        }
    )
    feature_exports = {}
    for runtime_split in ("validation_is", "oos"):
        feature_exports[f"{spec.candidate_id}_tier_a_{runtime_split}"] = {"path": f"{spec.candidate_id}_a_{runtime_split}.csv"}
        feature_exports[f"{spec.candidate_id}_tier_b_fallback_{runtime_split}"] = {"path": f"{spec.candidate_id}_b_{runtime_split}.csv"}
    attempts = make_attempts([spec], feature_exports, {"path": "stage42_signal_table.csv"}, frame)

    assert attempts[0]["max_hold_bars"] == 12
    assert attempts[0]["set"]["path"].endswith(".set")
    assert RUN_ID in attempts[0]["set"]["path"]
    assert STAGE_NUMBER == 42
    assert SIGNAL_FEATURE_ORDER == ("stage42_session_reliability_signal",)
