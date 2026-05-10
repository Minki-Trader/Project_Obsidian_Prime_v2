from __future__ import annotations

import pandas as pd

from stage_pipelines.stage54 import cost_aware_side_permission as stage54


def test_cost_defensive_filter_blocks_late_long_violation_and_weak_shorts() -> None:
    frame = pd.DataFrame(
        {
            stage54.SOURCE_SIGNAL_COLUMN: [1, 1, -1, -1, -1],
            "session_slice": ["early", "late", "mid", "late", "late"],
            "volatility_regime": ["vol_low", "vol_low", "vol_mid", "vol_low", "vol_low"],
            "adx_bucket": ["adx_20_25", "adx_gt25", "adx_20_25", "adx_lt20", "adx_gt25"],
            "di_spread_bucket": ["di_long_mild", "di_long_strong", "di_short_mild", "di_short_mild", "di_short_strong"],
        }
    )

    output, counts = stage54.apply_signal_filter(frame, "csp04_late_longs_no_volmid_shorts")

    assert output[stage54.SOURCE_SIGNAL_COLUMN].tolist() == [0, 1, 0, 0, -1]
    assert counts["adapter_blocked_long_signals"] == 1
    assert counts["adapter_blocked_short_signals"] == 2


def test_short_only_trend_or_di_blocks_nonqualified_short_context() -> None:
    frame = pd.DataFrame(
        {
            stage54.SOURCE_SIGNAL_COLUMN: [1, -1, -1],
            "session_slice": ["late", "mid", "early"],
            "volatility_regime": ["vol_low", "vol_low", "vol_mid"],
            "adx_bucket": ["adx_20_25", "adx_20_25", "adx_gt25"],
            "di_spread_bucket": ["di_long_mild", "di_short_mild", "di_long_mild"],
        }
    )

    output, counts = stage54.apply_signal_filter(frame, "csp05_short_only_trend_or_di")

    assert output[stage54.SOURCE_SIGNAL_COLUMN].tolist() == [0, 0, -1]
    assert counts["adapter_blocked_long_signals"] == 1
    assert counts["adapter_blocked_short_signals"] == 1
