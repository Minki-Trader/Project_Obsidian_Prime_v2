from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from foundation.control_plane.code_surface_audit import audit_code_surface
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics


ROOT = Path(__file__).resolve().parents[1]


class CodeSurfaceAuditTests(unittest.TestCase):
    def test_current_repo_code_surface_audit_passes_with_registered_debt(self) -> None:
        result = audit_code_surface(ROOT)

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])
        self.assertFalse(result.completed_forbidden)
        self.assertGreater(result.counts["scanned_files"], 0)
        self.assertIn(
            "compatibility_shim::foundation/mt5/runtime_support.py",
            {finding.check_id for finding in result.findings if finding.severity == "warning"},
        )

    def test_direct_control_plane_stage_pipeline_import_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            bad_file = root / "foundation/control_plane/bad.py"
            bad_file.parent.mkdir(parents=True)
            bad_file.write_text("from foundation.pipelines import run_stage10_logreg_mt5_scout as scout\n", encoding="utf-8")

            result = audit_code_surface(root)

        self.assertEqual(result.status, "blocked")
        self.assertTrue(result.completed_forbidden)
        self.assertIn("cross_owner_import::foundation/control_plane/bad.py", {finding.check_id for finding in result.findings})

    def test_mt5_strategy_report_parser_lives_under_mt5_owner(self) -> None:
        html = """
        <html><body><table>
        <tr><td>Total Net Profit:</td><td>12.50</td><td>Equity Drawdown Maximal:</td><td>6.25 (1.25%)</td></tr>
        <tr><td>Gross Profit:</td><td>22.50</td><td>Gross Loss:</td><td>-10.00</td></tr>
        <tr><td>Profit Factor:</td><td>2.25</td><td>Expected Payoff:</td><td>1.25</td></tr>
        <tr><td>Recovery Factor:</td><td>2.00</td></tr>
        <tr><td>Total Trades:</td><td>10</td><td>Short Trades (won %):</td><td>4 (50.00%)</td><td>Long Trades (won %):</td><td>6 (66.67%)</td></tr>
        <tr><td>Total Deals:</td><td>20</td><td>Profit Trades (% of total):</td><td>6 (60.00%)</td><td>Loss Trades (% of total):</td><td>4 (40.00%)</td></tr>
        </table></body></html>
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.htm"
            report_path.write_text(html, encoding="utf-16")
            metrics = extract_mt5_strategy_report_metrics(report_path)

        self.assertEqual(metrics["status"], "completed")
        self.assertEqual(metrics["net_profit"], 12.5)
        self.assertEqual(metrics["trade_count"], 10)
        self.assertEqual(metrics["win_rate_percent"], 60.0)


if __name__ == "__main__":
    unittest.main()
