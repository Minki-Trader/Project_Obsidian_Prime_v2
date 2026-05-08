from __future__ import annotations

import unittest

import pandas as pd

from stage_pipelines.stage34.markov_long_permission_entry_time_hold_proxy_probe import (
    classify_rule,
    evaluate_rule_splits,
    summarize_rules,
)


class Stage34MarkovEntryTimeHoldProxyProbeTests(unittest.TestCase):
    def test_keep_late_or_vol_mid_can_be_entry_proxy_candidate(self) -> None:
        rows = []
        for split in ("validation", "oos"):
            for index in range(60):
                keep = index < 42
                kept_profit = -1.0 if keep and index % 7 == 0 else 4.0
                rows.append(
                    {
                        "matched_split": split,
                        "session_slice": "late" if keep else "mid",
                        "volatility_regime": "vol_mid" if keep else "vol_high",
                        "trend_regime": "downtrend",
                        "adx_bucket": "adx_gt25",
                        "confidence_band": "confidence_ge_0.97",
                        "p_long_band": "p_long_0.90_0.95",
                        "state_score_band": "state_score_high_positive",
                        "entropy_inv_band": "entropy_inv_ge_0.80",
                        "hour_bucket": "hour_16_19",
                        "hold_bucket": "hold_gt_96" if keep else "hold_0_12",
                        "net_profit": kept_profit if keep else -3.0,
                        "hold_bars": 120 if keep else 6,
                        "mae": 1.0,
                        "mfe": 4.0,
                        "realized_over_mfe": 0.5,
                    }
                )
        frame = pd.DataFrame(rows)
        frame["short_hold_any"] = frame["hold_bucket"].eq("hold_0_12")
        frame["short_hold_loss"] = frame["short_hold_any"] & frame["net_profit"].lt(0)
        frame["long_hold_any"] = frame["hold_bucket"].eq("hold_gt_96")
        frame["long_hold_win"] = frame["long_hold_any"] & frame["net_profit"].gt(0)

        split_rows = evaluate_rule_splits(frame)
        summary_rows = summarize_rules(split_rows)
        primary = next(row for row in summary_rows if row["rule_id"] == "keep_late_or_vol_mid")

        self.assertIn(primary["classification"], {"entry_proxy_candidate", "entry_proxy_candidate_thin_sample"})
        self.assertLess(primary["oos_short_hold_loss_delta"], 0)
        self.assertGreater(primary["oos_pf_delta_vs_base"], 0)

    def test_classify_sample_thin_blocks_direct_candidate(self) -> None:
        rule = {"rule_id": "keep_late_session_only"}
        validation = {"sample_status": "sample_thin", "pf_delta_vs_base": 1.0, "net_delta_vs_base": 10, "short_hold_loss_delta_vs_base": -0.1}
        oos = {"sample_status": "ok", "pf_delta_vs_base": 1.0, "net_delta_vs_base": 10, "short_hold_loss_delta_vs_base": -0.1}

        self.assertEqual(classify_rule(rule, validation, oos), "sample_thin_diagnostic_only")


if __name__ == "__main__":
    unittest.main()
