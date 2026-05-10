from __future__ import annotations

from stage_pipelines.stage49.deep_followup_suite import best_variant, di_spread_bucket


def test_best_variant_uses_min_delta_then_combined_delta() -> None:
    rows = [
        {"variant_id": "adx_1_2", "split": "validation_is", "net_profit_delta_vs_original": 10.0},
        {"variant_id": "adx_1_2", "split": "oos", "net_profit_delta_vs_original": 5.0},
        {"variant_id": "adx_2_3", "split": "validation_is", "net_profit_delta_vs_original": 8.0},
        {"variant_id": "adx_2_3", "split": "oos", "net_profit_delta_vs_original": 8.0},
    ]

    assert best_variant(rows) == "adx_2_3"


def test_di_spread_bucket_handles_directional_ranges() -> None:
    assert di_spread_bucket(None) == "feature_missing"
    assert di_spread_bucket(-12.0) == "di_short_strong"
    assert di_spread_bucket(-2.0) == "di_short_mild"
    assert di_spread_bucket(4.0) == "di_long_mild"
    assert di_spread_bucket(14.0) == "di_long_strong"
