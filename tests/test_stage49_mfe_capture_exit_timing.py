from __future__ import annotations

import pandas as pd

from stage_pipelines.stage49.mfe_capture_exit_timing import (
    build_decision_rows,
    compute_trade_path,
    summarize_loss_rescue,
    summarize_thresholds,
)


def test_compute_trade_path_detects_target_touch_for_buy() -> None:
    bars = pd.DataFrame(
        {
            "time_open": pd.to_datetime(["2025-01-01 10:00:00", "2025-01-01 10:05:00"]),
            "high": [101.0, 103.0],
            "low": [99.5, 100.0],
        }
    )
    trade = {
        "split": "validation_is",
        "trade_index": 1,
        "direction": "buy",
        "open_time": pd.Timestamp("2025-01-01 10:00:00"),
        "close_time": pd.Timestamp("2025-01-01 10:10:00"),
        "volume": 1.0,
        "open_price": 100.0,
        "hold_bars": 2,
        "net_profit": -1.0,
        "mfe": 3.0,
        "mae": 0.5,
    }

    path = compute_trade_path(trade, bars, targets=[2.0])

    assert path.max_favorable_seen == 3.0
    assert path.target_hit_bars[2.0] == 2
    assert path.first_adverse_bar == 1


def test_threshold_summary_separates_take_profit_from_loss_rescue() -> None:
    bars = pd.DataFrame(
        {
            "time_open": pd.to_datetime(["2025-01-01 10:00:00", "2025-01-01 10:05:00"]),
            "high": [103.0, 104.0],
            "low": [99.0, 98.0],
        }
    )
    trades = [
        {"split": "validation_is", "trade_index": 1, "direction": "buy", "open_time": pd.Timestamp("2025-01-01 10:00:00"), "close_time": pd.Timestamp("2025-01-01 10:10:00"), "volume": 1.0, "open_price": 100.0, "hold_bars": 2, "net_profit": 5.0, "mfe": 4.0, "mae": 2.0},
        {"split": "validation_is", "trade_index": 2, "direction": "buy", "open_time": pd.Timestamp("2025-01-01 10:00:00"), "close_time": pd.Timestamp("2025-01-01 10:10:00"), "volume": 1.0, "open_price": 100.0, "hold_bars": 2, "net_profit": -3.0, "mfe": 4.0, "mae": 2.0},
    ]
    paths = [compute_trade_path(trade, bars, targets=[2.0]) for trade in trades]

    threshold = summarize_thresholds(paths, targets=[2.0])[0]
    rescue = summarize_loss_rescue(paths, targets=[2.0])[0]

    assert threshold["take_profit_net_profit"] == 4.0
    assert threshold["winner_cut_count"] == 1
    assert rescue["diagnostic_rescue_net_profit"] == 2.0
    assert rescue["status"] == "diagnostic_only_not_executable_without_selection_rule"


def test_decision_marks_no_common_fixed_target_when_oos_negative() -> None:
    threshold_rows = [
        {"split": "validation_is", "target_net": 2.0, "take_profit_delta": 5.0},
        {"split": "oos", "target_net": 2.0, "take_profit_delta": -1.0},
    ]
    rescue_rows = [
        {"split": "validation_is", "target_net": 2.0, "diagnostic_rescue_delta": 10.0},
    ]

    row = build_decision_rows(threshold_rows, rescue_rows)[0]

    assert row["best_common_target"] == 2.0
    assert "no_common_fixed_take_profit_target_improves_both_splits" in row["decision_reasons"]
