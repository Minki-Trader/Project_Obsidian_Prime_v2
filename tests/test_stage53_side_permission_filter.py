from __future__ import annotations

import pandas as pd

from stage_pipelines.stage53 import side_permission_filter as stage53


def test_short_only_filter_blocks_longs_and_keeps_shorts() -> None:
    frame = pd.DataFrame(
        {
            stage53.SOURCE_SIGNAL_COLUMN: [1, -1, 0],
            "session_slice": ["early", "late", "mid"],
            "volatility_regime": ["vol_low", "vol_mid", "vol_low"],
            "adx_bucket": ["adx_gt25", "adx_lt20", "adx_20_25"],
            "di_spread_bucket": ["di_long_strong", "di_short_strong", "di_short_mild"],
        }
    )

    output, counts = stage53.apply_signal_filter(frame, "spf01_short_only")

    assert output[stage53.SOURCE_SIGNAL_COLUMN].tolist() == [0, -1, 0]
    assert counts["adapter_blocked_long_signals"] == 1
    assert counts["adapter_blocked_short_signals"] == 0


def test_validation_weak_filter_blocks_named_strata() -> None:
    frame = pd.DataFrame(
        {
            stage53.SOURCE_SIGNAL_COLUMN: [1, 1, -1, -1, -1],
            "session_slice": ["mid", "late", "early", "late", "late"],
            "volatility_regime": ["vol_low", "vol_low", "vol_mid", "vol_low", "vol_low"],
            "adx_bucket": ["adx_gt25", "adx_20_25", "adx_gt25", "adx_lt20", "adx_gt25"],
            "di_spread_bucket": ["di_long_mild", "di_short_mild", "di_short_strong", "di_long_mild", "di_short_strong"],
        }
    )

    output, counts = stage53.apply_signal_filter(frame, "spf02_validation_weak_strata_block")

    assert output[stage53.SOURCE_SIGNAL_COLUMN].tolist() == [0, 0, 0, 0, -1]
    assert counts["adapter_blocked_long_signals"] == 2
    assert counts["adapter_blocked_short_signals"] == 2


def test_candidate_set_values_disables_atr_sltp_runtime_inputs() -> None:
    values = stage53.candidate_set_values({"adapter_id": "spf01_short_only"}, magic=53)

    assert values["InpMagic"] == 53
    assert values["InpAtrSltpEnabled"] is False
    assert values["InpAtrStopMultiplier"] == 0.0
    assert values["InpAtrTakeProfitMultiplier"] == 0.0
