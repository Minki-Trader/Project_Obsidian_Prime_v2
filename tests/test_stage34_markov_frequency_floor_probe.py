from __future__ import annotations

import unittest

import pandas as pd

from stage_pipelines.stage34.markov_long_permission_frequency_floor_probe import (
    classify_rule,
    frequency_floor_status,
    monthly_frequency_metrics,
)


class Stage34MarkovFrequencyFloorProbeTests(unittest.TestCase):
    def test_frequency_floor_fails_low_oos_count(self) -> None:
        frame = pd.DataFrame(
            {
                "month": ["2025-10"] * 5 + ["2025-11"] * 3 + ["2025-12"] * 5 + ["2026-01"] * 5 + ["2026-02"] * 2 + ["2026-03"] * 4 + ["2026-04"] * 2,
                "net_profit": [1.0] * 26,
            }
        )

        metrics = monthly_frequency_metrics(frame, "oos")

        self.assertEqual(metrics["kept_trade_count"], 26)
        self.assertEqual(frequency_floor_status(metrics, "oos"), "fail")

    def test_classify_downgrades_thin_primary_candidate(self) -> None:
        rule = {"rule_id": "keep_late_or_vol_mid"}
        validation = {
            "frequency_floor_status": "fail",
            "pf_delta_vs_base": 0.4,
            "net_delta_vs_base": 10,
        }
        oos = {
            "frequency_floor_status": "fail",
            "pf_delta_vs_base": 0.9,
            "net_delta_vs_base": 90,
        }

        self.assertEqual(classify_rule(rule, validation, oos), "frequency_floor_fail_thin_sample")

    def test_classify_broader_candidate_when_frequency_and_pf_pass(self) -> None:
        rule = {"rule_id": "exclude_vol_high_or_adx_20_25"}
        validation = {
            "frequency_floor_status": "pass",
            "pf_delta_vs_base": 0.31,
            "net_delta_vs_base": 3.3,
        }
        oos = {
            "frequency_floor_status": "pass",
            "pf_delta_vs_base": 0.32,
            "net_delta_vs_base": 15.77,
        }

        self.assertEqual(classify_rule(rule, validation, oos), "frequency_ok_candidate")


if __name__ == "__main__":
    unittest.main()
