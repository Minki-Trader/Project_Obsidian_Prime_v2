from __future__ import annotations

import unittest

import pandas as pd

from stage_pipelines.stage34.markov_long_permission_segment_stress_probe import (
    classify_rule,
    evaluate_rule_splits,
    summarize_rules,
)


class Stage34MarkovSegmentStressProbeTests(unittest.TestCase):
    def test_exclude_short_hold_improves_splits_but_is_not_entry_time_rule(self) -> None:
        rows = []
        for split in ("validation", "oos"):
            for index in range(40):
                rows.append(
                    {
                        "matched_split": split,
                        "hold_bucket": "hold_gt_96" if index < 30 else "hold_0_12",
                        "session_slice": "late",
                        "volatility_regime": "vol_low",
                        "adx_bucket": "adx_gt25",
                        "month": "2025-01",
                        "net_profit": 3.0 if index < 30 else -5.0,
                        "hold_bars": 120 if index < 30 else 6,
                        "mae": 1.0,
                        "mfe": 4.0,
                        "realized_over_mfe": 0.5,
                    }
                )
        frame = pd.DataFrame(rows)

        split_rows = evaluate_rule_splits(frame)
        summary_rows = summarize_rules(split_rows)
        short_hold = next(row for row in summary_rows if row["rule_id"] == "exclude_short_hold_0_12")

        self.assertEqual(short_hold["classification"], "mechanism_survivor_not_entry_time_rule")
        self.assertGreater(short_hold["validation_net_delta_vs_base"], 0)
        self.assertGreater(short_hold["oos_net_delta_vs_base"], 0)

    def test_classify_direct_filter_marks_split_conflict(self) -> None:
        meta = {"rule_id": "exclude_mid_session", "entry_time_available": True}
        validation = {"net_delta_vs_base": -80, "pf_delta_vs_base": -0.2, "removed_net_profit": 90, "kept_profit_factor": 1.2, "sample_status": "ok"}
        oos = {"net_delta_vs_base": 40, "pf_delta_vs_base": 0.5, "removed_net_profit": -40, "kept_profit_factor": 1.8, "sample_status": "ok"}

        self.assertEqual(classify_rule(meta, validation, oos), "split_inconsistent_removed_positive_validation_negative_oos")


if __name__ == "__main__":
    unittest.main()
