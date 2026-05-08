from __future__ import annotations

import unittest

import pandas as pd

from stage_pipelines.stage34.markov_long_permission_broader_entry_proxy_probe import (
    filter_candidate_feature_frame,
    monthly_candidate_read,
    monthly_leave_one_out_rows,
    monthly_summary_rows,
)


class Stage34MarkovBroaderEntryProxyProbeTests(unittest.TestCase):
    def test_monthly_candidate_warns_when_leave_one_oos_margin_is_thin(self) -> None:
        rows = []
        for month, profits in {
            "2025-10": [75.0, -1.0],
            "2025-11": [8.0, -2.0],
            "2025-12": [7.0, -3.0],
        }.items():
            for profit in profits:
                rows.append(
                    {
                        "matched_split": "oos",
                        "month": month,
                        "net_profit": profit,
                        "session_slice": "late",
                        "volatility_regime": "vol_mid",
                        "trend_regime": "downtrend",
                        "adx_bucket": "adx_gt25",
                    }
                )
        for month in ("2025-01", "2025-02", "2025-03"):
            rows.append(
                {
                    "matched_split": "validation",
                    "month": month,
                    "net_profit": 20.0,
                    "session_slice": "late",
                    "volatility_regime": "vol_mid",
                    "trend_regime": "downtrend",
                    "adx_bucket": "adx_gt25",
                }
            )
        frame = pd.DataFrame(rows)

        leave_rows = monthly_leave_one_out_rows(frame)
        summaries = monthly_summary_rows(leave_rows)
        read = monthly_candidate_read(summaries)

        self.assertEqual(read["status"], "monthly_survivor_with_dependency")
        self.assertIn("top_positive_month_dependency", read["oos"]["monthly_survival_flags"])

    def test_feature_filter_removes_vol_high_or_adx_20_25_and_keeps_missing_context(self) -> None:
        source = pd.DataFrame(
            {
                "bar_time_server": ["2025.01.01 00:00:00", "2025.01.01 00:05:00", "2025.01.01 00:10:00", "2025.01.01 00:15:00"],
                "timestamp_utc": ["2025-01-01T00:00:00Z", "2025-01-01T00:05:00Z", "2025-01-01T00:10:00Z", "2025-01-01T00:15:00Z"],
                "split": ["validation"] * 4,
                "mk_state_score": [0.1, 0.2, 0.3, 0.4],
            }
        )
        context = pd.DataFrame(
            {
                "bar_time_server": ["2025.01.01 00:00:00", "2025.01.01 00:05:00", "2025.01.01 00:10:00"],
                "volatility_regime": ["vol_mid", "vol_high", "vol_mid"],
                "adx_bucket": ["adx_gt25", "adx_gt25", "adx_20_25"],
                "stage34_rule_allowed": [True, False, False],
            }
        )

        filtered, summary = filter_candidate_feature_frame(source, context)

        self.assertEqual(filtered["bar_time_server"].tolist(), ["2025.01.01 00:00:00", "2025.01.01 00:15:00"])
        self.assertEqual(summary["filtered_rows"], 2)
        self.assertEqual(summary["missing_context_rows_kept"], 1)


if __name__ == "__main__":
    unittest.main()
