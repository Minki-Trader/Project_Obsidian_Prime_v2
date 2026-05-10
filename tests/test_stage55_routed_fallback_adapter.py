from __future__ import annotations

import pandas as pd

from stage_pipelines.stage55 import routed_fallback_adapter as stage55


def test_stage55_reuses_decision_time_side_filter_primitives() -> None:
    frame = pd.DataFrame(
        {
            stage55.SOURCE_SIGNAL_COLUMN: [1, -1, -1, -1],
            "session_slice": ["early", "mid", "late", "late"],
            "volatility_regime": ["vol_low", "vol_low", "vol_low", "vol_mid"],
            "adx_bucket": ["adx_gt25", "adx_20_25", "adx_gt25", "adx_lt20"],
            "di_spread_bucket": ["di_long_mild", "di_short_mild", "di_short_strong", "di_short_mild"],
        }
    )

    output, counts = stage55.apply_signal_filter(frame, "csp03_midlate_longs_strong_shorts")

    assert output[stage55.SOURCE_SIGNAL_COLUMN].tolist() == [0, 0, -1, -1]
    assert counts["adapter_blocked_long_signals"] == 1
    assert counts["adapter_blocked_short_signals"] == 1


def test_stage55_routing_candidate_grid_is_deterministic() -> None:
    candidate = stage55.routing_candidate_by_id("rfp02_csp03_primary_csp05_fallback")

    assert candidate["primary_adapter_id"] == "csp03_midlate_longs_strong_shorts"
    assert candidate["fallback_adapter_id"] == "csp05_short_only_trend_or_di"
    assert [row["adapter_id"] for row in stage55.ROUTING_CANDIDATES] == [
        "rfp00_csp03_primary_control_fallback",
        "rfp01_csp03_primary_csp03_fallback",
        "rfp02_csp03_primary_csp05_fallback",
        "rfp03_csp02_primary_csp03_fallback",
    ]
