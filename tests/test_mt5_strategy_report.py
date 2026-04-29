from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "mt5_reports"


class Mt5StrategyReportTests(unittest.TestCase):
    def test_korean_report_aliases_include_drawdown_and_trade_counts(self) -> None:
        html = """
        <html><body><table>
        <tr><td>총 순수익:</td><td>12.50</td><td>잔고 하락폭 최대:</td><td>5.00 (1.00%)</td><td>평가금 하락폭 최대:</td><td>6.25 (1.25%)</td></tr>
        <tr><td>총 수익:</td><td>22.50</td><td>총 손실:</td><td>-10.00</td></tr>
        <tr><td>수익 팩터:</td><td>2.25</td><td>기대 수익:</td><td>1.25</td></tr>
        <tr><td>회복 계수:</td><td>2.00</td></tr>
        <tr><td>총 거래:</td><td>10</td><td>매도 거래 (승률 %):</td><td>4 (50.00%)</td><td>매수 거래 (승률 %):</td><td>6 (66.67%)</td></tr>
        <tr><td>총 딜:</td><td>20</td><td>수익 거래 (% 총계 중):</td><td>6 (60.00%)</td><td>손실 거래 (% 총계 중):</td><td>4 (40.00%)</td></tr>
        </table></body></html>
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "korean_report.htm"
            path.write_text(html, encoding="utf-8-sig")
            metrics = extract_mt5_strategy_report_metrics(path)

        self.assertEqual(metrics["status"], "completed", metrics)
        self.assertEqual(metrics["trade_count"], 10)
        self.assertEqual(metrics["short_trade_count"], 4)
        self.assertEqual(metrics["long_trade_count"], 6)
        self.assertEqual(metrics["max_drawdown_amount"], 6.25)
        self.assertEqual(metrics["recovery_factor"], 2.0)

    def test_sourced_run03e_report_excerpt_parses_core_metrics(self) -> None:
        metrics = extract_mt5_strategy_report_metrics(FIXTURE_ROOT / "run03e_validation_sourced_excerpt.htm")

        self.assertEqual(metrics["status"], "completed", metrics)
        self.assertEqual(metrics["source_encoding"], "utf-8-sig")
        self.assertEqual(metrics["net_profit"], -205.14)
        self.assertEqual(metrics["trade_count"], 301)
        self.assertEqual(metrics["profit_factor"], 0.88)
        self.assertEqual(metrics["max_drawdown_amount"], 335.29)
        self.assertEqual(metrics["recovery_factor"], -0.61)
        self.assertEqual(metrics["missing_required_metrics"], [])

    def test_trade_count_parse_failure_stays_none_not_zero(self) -> None:
        html = """
        <html><body><table>
        <tr><td>Total Net Profit:</td><td>12.50</td><td>Balance Drawdown Maximal:</td><td>5.00 (1.00%)</td><td>Equity Drawdown Maximal:</td><td>6.25 (1.25%)</td></tr>
        <tr><td>Gross Profit:</td><td>22.50</td><td>Gross Loss:</td><td>-10.00</td></tr>
        <tr><td>Profit Factor:</td><td>2.25</td><td>Expected Payoff:</td><td>1.25</td></tr>
        <tr><td>Recovery Factor:</td><td>2.00</td></tr>
        <tr><td>Total Trades:</td><td>not available</td><td>Short Trades (won %):</td><td>4 (50.00%)</td><td>Long Trades (won %):</td><td>6 (66.67%)</td></tr>
        <tr><td>Total Deals:</td><td>20</td><td>Profit Trades (% of total):</td><td>6 (60.00%)</td><td>Loss Trades (% of total):</td><td>4 (40.00%)</td></tr>
        </table></body></html>
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "bad_count.htm"
            path.write_text(html, encoding="utf-16")
            metrics = extract_mt5_strategy_report_metrics(path)

        self.assertIsNone(metrics["trade_count"])
        self.assertEqual(metrics["status"], "partial")
        self.assertIn("trade_count", metrics["missing_required_metrics"])


if __name__ == "__main__":
    unittest.main()
