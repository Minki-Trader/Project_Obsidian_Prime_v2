from __future__ import annotations

import pandas as pd

from stage_pipelines.stage51 import q2_loss_firewall as stage51


def test_apply_firewall_blocks_late_or_di_short_after_base_adx() -> None:
    frame = pd.DataFrame(
        {
            stage51.SOURCE_SIGNAL_COLUMN: [-1, -1, -1, 1],
            "entry_decision": ["short", "short", "short", "long"],
            "adx_14": [22.0, 30.0, 30.0, 30.0],
            "session_slice": ["early", "late", "mid", "late"],
            "di_spread_bucket": ["di_short_strong", "di_long_mild", "di_short_mild", "di_short_mild"],
            "volatility_regime": ["vol_low", "vol_low", "vol_mid", "vol_mid"],
        }
    )

    output, counts = stage51.apply_firewall(frame, "fw03_block_late_or_di_short_mild", apply_base_adx=True)

    assert counts["base_removed"] == 1
    assert counts["firewall_removed"] == 2
    assert output[stage51.SOURCE_SIGNAL_COLUMN].tolist() == [0, 0, 0, 1]


def test_summarize_robustness_prefers_three_positive_windows() -> None:
    rows = [
        {"variant_id": "fw01", "route_view": "tier_a_firewall_separate", "window_id": "w01_2025q2", "net_profit": -1.0, "profit_factor": 0.9, "trade_count": 5},
        {"variant_id": "fw01", "route_view": "tier_a_firewall_separate", "window_id": "w02_2025q3", "net_profit": 20.0, "profit_factor": 1.2, "trade_count": 7},
        {"variant_id": "fw01", "route_view": "tier_a_firewall_separate", "window_id": "w03_2025q4", "net_profit": 30.0, "profit_factor": 1.3, "trade_count": 6},
        {"variant_id": "fw01", "route_view": "tier_a_firewall_separate", "window_id": "w04_2026q1", "net_profit": 40.0, "profit_factor": 1.4, "trade_count": 8},
    ]

    summary = stage51.summarize_robustness("run", rows)

    assert summary[0]["positive_windows"] == 3
    assert summary[0]["total_net_profit"] == 89.0
    assert summary[0]["q2_net_profit"] == -1.0
    assert summary[0]["robustness_status"] == "passed"


def test_cost_summary_marks_half_cost_passed() -> None:
    trades = [
        {"variant_id": "fw", "window_id": "w01_2025q2", "net_profit": 5.0},
        {"variant_id": "fw", "window_id": "w02_2025q3", "net_profit": 10.0},
        {"variant_id": "fw", "window_id": "w03_2025q4", "net_profit": 10.0},
        {"variant_id": "fw", "window_id": "w04_2026q1", "net_profit": 10.0},
    ]

    rows = stage51.build_cost_rows("run45C", "source", "label", "tier_a_firewall_separate", trades)
    summary = stage51.summarize_cost_rows(rows)
    half = next(row for row in summary if row["variant_id"] == "fw" and row["extra_cost_per_trade"] == 0.5)

    assert half["positive_windows"] == 4
    assert half["cost_status"] == "passed"

