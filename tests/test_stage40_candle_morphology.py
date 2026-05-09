from __future__ import annotations

from pathlib import Path

import pandas as pd

from foundation.features.candle_morphology import (
    SIGNAL_FEATURE_ORDER,
    apply_candidate_to_table,
    build_broad_candidate_grid,
    build_thresholds,
    materialize_candle_morphology,
    summarize_candidate_frames,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage40.candle_morphology_signal_quality_scout import export_signal_score_table


def _raw_bars() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "time_close_unix": 1_700_000_000,
                "contract_symbol": "US100",
                "broker_symbol": "US100",
                "timeframe": "M5",
                "open": 10.0,
                "high": 11.0,
                "low": 9.0,
                "close": 10.5,
            },
            {
                "time_close_unix": 1_700_000_300,
                "contract_symbol": "US100",
                "broker_symbol": "US100",
                "timeframe": "M5",
                "open": 10.4,
                "high": 10.8,
                "low": 9.8,
                "close": 10.2,
            },
            {
                "time_close_unix": 1_700_000_600,
                "contract_symbol": "US100",
                "broker_symbol": "US100",
                "timeframe": "M5",
                "open": 10.5,
                "high": 11.5,
                "low": 9.0,
                "close": 9.5,
            },
        ]
    )


def test_closed_bar_morphology_formulas_and_alignment() -> None:
    frame = materialize_candle_morphology(_raw_bars())

    assert frame.loc[0, "timestamp"] == pd.to_datetime(1_700_000_000, unit="s", utc=True)
    assert frame.loc[0, "candle_body_size"] == 0.5
    assert frame.loc[0, "candle_full_range"] == 2.0
    assert frame.loc[0, "candle_upper_wick"] == 0.5
    assert frame.loc[0, "candle_lower_wick"] == 1.0
    assert frame.loc[0, "candle_body_range_ratio"] == 0.25
    assert frame.loc[1, "candle_inside_bar_flag"] == 1
    assert frame.loc[2, "candle_outside_bar_flag"] == 1
    assert frame.loc[2, "candle_adverse_outside_long"] == 1
    assert frame.loc[2, "candle_adverse_outside_short"] == 0


def test_candidate_grid_has_required_broad_morphology_families() -> None:
    ids = [spec.candidate_id for spec in build_broad_candidate_grid()]

    assert len(ids) == 17
    assert ids[0] == "c01_reference_no_candle_morphology"
    assert "c03_adverse_outside_bar_filter" in ids
    assert "c08_wide_range_doji_negative_control" in ids
    assert "c17_morphology_contrast_extreme_sweep" in ids


def test_adverse_outside_filter_blocks_long_entry() -> None:
    morphology = materialize_candle_morphology(_raw_bars())
    common = morphology.copy()
    common["stage40_row_id"] = range(len(common))
    common["timestamp_utc"] = common["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    common["split"] = "train"
    common.loc[2, "split"] = "validation"
    common["validation_oos_split_label"] = common["split"].replace({"validation": "validation_is"})
    common["label_class"] = 2
    common["tier_label"] = mt5.TIER_A
    common["routing_source"] = "tier_a_primary"
    common["partial_context_subtype"] = "Tier_A_full_context"
    common["tier_a_available"] = True
    common["tier_b_fallback_available"] = False
    common["return_zscore_20"] = 1.0
    common["adx_14"] = 30.0
    thresholds = build_thresholds(common)
    specs = {spec.candidate_id: spec for spec in build_broad_candidate_grid()}

    reference = apply_candidate_to_table(common, specs["c01_reference_no_candle_morphology"], thresholds)
    filtered = apply_candidate_to_table(common, specs["c03_adverse_outside_bar_filter"], thresholds)

    assert int(reference.loc[2, SIGNAL_FEATURE_ORDER[0]]) == 1
    assert int(filtered.loc[2, SIGNAL_FEATURE_ORDER[0]]) == 0


def test_summary_tracks_activation_thinning_and_tier_b_share() -> None:
    morphology = materialize_candle_morphology(_raw_bars())
    common = pd.concat([morphology, morphology], ignore_index=True)
    common["stage40_row_id"] = range(len(common))
    common["timestamp_utc"] = common["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    common["split"] = ["train", "validation", "oos", "train", "validation", "oos"]
    common["validation_oos_split_label"] = common["split"].replace({"validation": "validation_is"})
    common["label_class"] = 2
    common["tier_label"] = [mt5.TIER_A, mt5.TIER_A, mt5.TIER_A, mt5.TIER_B, mt5.TIER_B, mt5.TIER_B]
    common["routing_source"] = ["tier_a_primary"] * 3 + ["tier_b_fallback"] * 3
    common["partial_context_subtype"] = common["tier_label"]
    common["tier_a_available"] = common["tier_label"].eq(mt5.TIER_A)
    common["tier_b_fallback_available"] = common["tier_label"].eq(mt5.TIER_B)
    common["return_zscore_20"] = 1.0
    common["adx_14"] = 30.0
    thresholds = build_thresholds(common)
    specs = {spec.candidate_id: spec for spec in build_broad_candidate_grid()}
    frames = {
        key: apply_candidate_to_table(common, specs[key], thresholds)
        for key in ("c01_reference_no_candle_morphology", "c08_wide_range_doji_negative_control")
    }

    rows = summarize_candidate_frames(frames)
    doji_rows = [row for row in rows if row["candidate_id"] == "c08_wide_range_doji_negative_control"]

    assert doji_rows
    assert all("morphology_activation_rate" in row for row in doji_rows)
    assert any(row["candidate_rejection_reason"].startswith("thin_trade_stream") for row in doji_rows)


def test_signal_score_table_exports_manifest_fields(tmp_path: Path) -> None:
    payload = export_signal_score_table(tmp_path / "signal_table.csv")

    assert payload["feature_order"] == list(SIGNAL_FEATURE_ORDER)
    assert payload["feature_order_hash"]
    assert Path(payload["path"]).exists()
