from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from foundation.control_plane.mt5_trade_attribution import (
    MarketData,
    compute_trade_attribution,
    enrich_records,
)
from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report


class Mt5TradeAttributionTests(unittest.TestCase):
    def test_parses_deals_and_pairs_closed_trades(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.htm"
            report_path.write_text(_deal_report_html(), encoding="utf-16")

            report = parse_mt5_trade_report(report_path)
            trades = pair_deals_into_trades(report["deals"])

            self.assertEqual(len(report["deals"]), 2)
            self.assertEqual(len(trades), 1)
            self.assertEqual(trades[0].direction, "buy")
            self.assertEqual(trades[0].net_profit, 0.5)
            self.assertEqual(report["summary"]["average_position_holding_bars"], 2.0)

    def test_computes_hold_mfe_mae_and_regime_slices(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.htm"
            report_path.write_text(_deal_report_html(), encoding="utf-16")
            trades = pair_deals_into_trades(parse_mt5_trade_report(report_path)["deals"])
            market_data = MarketData.from_frames(_bars_frame(), _features_frame())

            stats = compute_trade_attribution(trades, market_data)
            diagnostics = stats["trade_diagnostics"]
            regime = stats["regime_slice_attribution"]

            self.assertEqual(stats["trade_count"], 1)
            self.assertEqual(diagnostics["avg_hold_bars"], 2.0)
            self.assertEqual(diagnostics["mfe_mean"], 0.8)
            self.assertEqual(diagnostics["mae_mean"], 0.2)
            self.assertEqual(regime["session_slice"]["mid"]["trade_count"], 1)
            self.assertEqual(regime["trend_regime"]["uptrend"]["trade_count"], 1)
            self.assertEqual(regime["adx_bucket"]["adx_gt25"]["trade_count"], 1)

    def test_enriches_normalized_record_without_overwriting_headline(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            report_path = root / "report.htm"
            report_path.write_text(_deal_report_html(), encoding="utf-16")
            records = [_normalized_record(report_path.name)]
            market_data = MarketData.from_frames(_bars_frame(), _features_frame())

            enriched, trade_rows, summary_rows, parser_errors = enrich_records(records, root, market_data)

            self.assertEqual(parser_errors, [])
            self.assertEqual(len(trade_rows), 1)
            self.assertEqual(len(summary_rows), 1)
            record = enriched[0]
            self.assertEqual(record["mt5_trading_headline"]["net_profit"]["value"], 0.5)
            self.assertEqual(record["trade_diagnostics"]["avg_hold_bars"]["value"], 2.0)
            self.assertEqual(record["trade_diagnostics"]["mfe_mean"]["value"], 0.8)
            self.assertEqual(record["regime_slice_attribution"]["month_pnl"]["value"], {"2025-01": 0.5})


def _deal_report_html() -> str:
    return """
    <html><body><table>
    <tr><td>Average position holding time:</td><td>00:10:00</td></tr>
    <tr><th>Deals</th></tr>
    <tr><td>Time</td><td>Deal</td><td>Symbol</td><td>Type</td><td>Direction</td><td>Volume</td><td>Price</td><td>Order</td><td>Commission</td><td>Swap</td><td>Profit</td><td>Balance</td><td>Comment</td></tr>
    <tr><td>2025.01.02 10:00:00</td><td>1</td><td>US100</td><td>buy</td><td>in</td><td>0.1</td><td>100.00</td><td>1</td><td>0.00</td><td>0.00</td><td>0.00</td><td>500.00</td><td>unit</td></tr>
    <tr><td>2025.01.02 10:10:00</td><td>2</td><td>US100</td><td>sell</td><td>out</td><td>0.1</td><td>105.00</td><td>2</td><td>0.00</td><td>0.00</td><td>0.50</td><td>500.50</td><td>unit</td></tr>
    </table></body></html>
    """


def _bars_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "time_open": pd.to_datetime(["2025-01-02 10:00:00", "2025-01-02 10:05:00"]),
            "time_close": pd.to_datetime(["2025-01-02 10:05:00", "2025-01-02 10:10:00"]),
            "open": [100.0, 104.0],
            "high": [108.0, 106.0],
            "low": [98.0, 103.0],
            "close": [104.0, 105.0],
            "spread_points": [10.0, 12.0],
        }
    )


def _features_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "timestamp": pd.to_datetime(["2025-01-02 10:00:00"], utc=True),
            "minutes_from_cash_open": [120.0],
            "historical_vol_20": [0.5],
            "adx_14": [30.0],
            "di_spread_14": [5.0],
            "supertrend_10_3": [1.0],
        }
    )


def _normalized_record(report_path: str) -> dict:
    cell = lambda value: {"value": value, "n/a_reason": None, "authority": "unit"}
    empty = {"value": None, "n/a_reason": "unit_missing", "authority": "unit"}
    return {
        "row_grain": {
            "run_id": cell("unit_run"),
            "record_view": cell("mt5_tier_a_only_oos"),
            "split": cell("oos"),
            "tier_scope": cell("Tier A"),
            "route_role": cell("tier_only_total"),
        },
        "mt5_trading_headline": {"net_profit": cell(0.5)},
        "trade_diagnostics": {
            "long_net_profit": dict(empty),
            "short_net_profit": dict(empty),
            "long_expectancy": dict(empty),
            "short_expectancy": dict(empty),
            "avg_hold_bars": dict(empty),
            "hold_distribution": dict(empty),
            "mfe_mean": dict(empty),
            "mae_mean": dict(empty),
            "realized_over_mfe": dict(empty),
            "loss_trade_mfe": dict(empty),
            "win_trade_mae": dict(empty),
        },
        "risk": {"worst_day": dict(empty), "worst_week": dict(empty), "consecutive_losses": dict(empty)},
        "regime_slice_attribution": {
            "session_slice": dict(empty),
            "volatility_regime": dict(empty),
            "trend_regime": dict(empty),
            "adx_bucket": dict(empty),
            "spread_regime": dict(empty),
            "month_pnl": dict(empty),
            "quarter_pnl": dict(empty),
            "subperiod_consistency": dict(empty),
            "validation_oos_gap": dict(empty),
        },
        "source_evidence": {"mt5_report_path": report_path},
    }


if __name__ == "__main__":
    unittest.main()
