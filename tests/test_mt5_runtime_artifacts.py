from __future__ import annotations

import unittest

from foundation.mt5.runtime_artifacts import attach_mt5_report_metrics


class Mt5RuntimeArtifactTests(unittest.TestCase):
    def test_attach_metrics_prefers_attempt_name_over_tier_split(self) -> None:
        execution_results = [
            {"status": "completed", "tier": "Tier A full-context", "split": "oos", "attempt_name": "long_only_oos"},
            {"status": "completed", "tier": "Tier A full-context", "split": "oos", "attempt_name": "short_only_oos"},
        ]
        report_records = [
            {"attempt_name": "long_only_oos", "tier": "Tier A full-context", "split": "oos", "report_name": "long"},
            {"attempt_name": "short_only_oos", "tier": "Tier A full-context", "split": "oos", "report_name": "short"},
        ]

        attach_mt5_report_metrics(execution_results, report_records)

        self.assertEqual(execution_results[0]["strategy_tester_report"]["report_name"], "long")
        self.assertEqual(execution_results[1]["strategy_tester_report"]["report_name"], "short")


if __name__ == "__main__":
    unittest.main()
