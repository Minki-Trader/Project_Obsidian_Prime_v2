from __future__ import annotations

from stage_pipelines.stage52 import atr_sltp_adapter as stage52


def test_candidate_set_values_maps_adapter_to_runtime_inputs() -> None:
    values = stage52.candidate_set_values({"enabled": True, "sl": 1.5, "tp": 2.0}, magic=100)

    assert values["InpMagic"] == 100
    assert values["InpAtrSltpEnabled"] is True
    assert values["InpAtrPeriod"] == stage52.ATR_PERIOD
    assert values["InpAtrStopMultiplier"] == 1.5
    assert values["InpAtrTakeProfitMultiplier"] == 2.0
    assert values["InpAtrMinStopPoints"] > 0
    assert values["InpAtrMaxTakeProfitPoints"] >= values["InpAtrMinTakeProfitPoints"]


def test_trade_count_gate_passes_period_adjusted_thresholds() -> None:
    partitions = [
        {
            "adapter_id": "atr",
            "route_view": "tier_a_atr_sltp_separate",
            "partition": "validation",
            "closed_trades": 60,
            "trades_per_month": 9.5,
        },
        {
            "adapter_id": "atr",
            "route_view": "tier_a_atr_sltp_separate",
            "partition": "oos",
            "closed_trades": 55,
            "trades_per_month": 8.1,
        },
    ]
    concentration = {"single_trade_share": 0.10, "day_share": 0.20, "week_share": 0.30, "month_share": 0.40}
    summary_rows = [
        {"adapter_id": "atr", "route_view": "tier_a_atr_sltp_separate", "window_id": f"w0{index}", "trade_count": 12}
        for index in range(1, 5)
    ]

    result = stage52.trade_count_gate("atr", "tier_a_atr_sltp_separate", partitions, concentration, summary_rows)

    assert result["status"] == "passed"
    assert result["combined_closed_trades"] == 115


def test_trade_count_gate_fails_thin_or_concentrated_candidate() -> None:
    partitions = [
        {
            "adapter_id": "atr",
            "route_view": "tier_a_atr_sltp_separate",
            "partition": "validation",
            "closed_trades": 20,
            "trades_per_month": 2.0,
        },
        {
            "adapter_id": "atr",
            "route_view": "tier_a_atr_sltp_separate",
            "partition": "oos",
            "closed_trades": 30,
            "trades_per_month": 2.9,
        },
    ]
    concentration = {"single_trade_share": 0.30, "day_share": 0.40, "week_share": 0.60, "month_share": 0.70}
    summary_rows = [
        {"adapter_id": "atr", "route_view": "tier_a_atr_sltp_separate", "window_id": "w01", "trade_count": 5}
    ]

    result = stage52.trade_count_gate("atr", "tier_a_atr_sltp_separate", partitions, concentration, summary_rows)

    assert result["status"] == "failed"
    assert "validation_closed_trades_lt_40" in result["failed_reasons"]
    assert "single_trade_share_gt_25pct" in result["failed_reasons"]


def test_concentration_counts_buy_sell_as_long_short() -> None:
    rows = [
        {"adapter_id": "atr", "route_mode": "route", "direction": "buy", "net_profit": 4.0, "close_time": "2025-04-01 10:00:00"},
        {"adapter_id": "atr", "route_mode": "route", "direction": "sell", "net_profit": -1.0, "close_time": "2025-04-02 10:00:00"},
    ]

    result = stage52.concentration_for("atr", "route", rows)

    assert result["long_trades"] == 1
    assert result["short_trades"] == 1
