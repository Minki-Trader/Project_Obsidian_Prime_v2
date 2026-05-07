from __future__ import annotations

import unittest

import pandas as pd

from stage_pipelines.stage34.markov_long_permission_attribution import assign_bands, matched_tier_trades, profit_metrics


class Stage34MarkovLongPermissionAttributionTests(unittest.TestCase):
    def test_profit_metrics_calculates_profit_factor(self) -> None:
        frame = pd.DataFrame({"net_profit": [10.0, -4.0, 2.0], "hold_bars": [1, 2, 3], "mae": [0.5, 1.0, 1.5], "mfe": [2.0, 1.0, 3.0], "realized_over_mfe": [0.5, -4.0, 0.67]})

        metrics = profit_metrics(frame)

        self.assertEqual(metrics["trade_count"], 3)
        self.assertEqual(metrics["net_profit"], 8.0)
        self.assertEqual(metrics["profit_factor"], 3.0)

    def test_assign_bands_labels_state_confidence_and_hold(self) -> None:
        frame = pd.DataFrame(
            {
                "mk_state_score": [1.0, 0.25, -0.1],
                "mk_state_confidence": [0.99, 0.92, 0.5],
                "mk_state_entropy_inv": [0.9, 0.6, 0.1],
                "p_long": [0.98, 0.96, 0.2],
                "hold_bars": [6, 40, 120],
                "open_time_dt": pd.to_datetime(["2025-01-01", "2025-02-01", "2025-03-01"]),
            }
        )

        out = assign_bands(frame)

        self.assertEqual(out.loc[0, "state_score_band"], "state_score_high_positive")
        self.assertEqual(out.loc[1, "state_score_band"], "state_score_weak_positive")
        self.assertEqual(out.loc[2, "hold_bucket"], "hold_gt_96")

    def test_matched_tier_trades_joins_on_open_time(self) -> None:
        trades = pd.DataFrame(
            {
                "record_view": ["mt5_tier_a_only_validation_is"],
                "open_time": ["2025-01-02 10:00:00"],
                "open_time_dt": pd.to_datetime(["2025-01-02 10:00:00"]),
                "close_time": ["2025-01-02 10:10:00"],
                "direction": ["buy"],
                "net_profit": [1.0],
                "hold_bars": [2.0],
                "mae": [0.1],
                "mfe": [1.5],
                "realized_over_mfe": [0.66],
                "session_slice": ["mid"],
                "volatility_regime": ["vol_mid"],
                "trend_regime": ["downtrend"],
                "adx_bucket": ["adx_gt25"],
                "trade_index": [1],
            }
        )
        feature = pd.DataFrame(
            {
                "open_time_dt": pd.to_datetime(["2025-01-02 10:00:00"]),
                "mk_state_score": [1.0],
                "mk_state_confidence": [0.99],
                "mk_state_entropy_inv": [0.9],
                "mk_return_abs": [0.2],
                "markov_state": [0],
                "p_short": [0.01],
                "p_flat": [0.04],
                "p_long": [0.95],
                "threshold": [0.9],
                "decision": ["long"],
                "state_score_band": ["state_score_high_positive"],
                "confidence_band": ["confidence_ge_0.97"],
                "entropy_inv_band": ["entropy_inv_ge_0.80"],
                "p_long_band": ["p_long_0.90_0.95"],
            }
        )
        empty = feature.iloc[0:0].copy()
        features = {("Tier A", "validation"): feature, ("Tier A", "oos"): empty, ("Tier B", "validation"): empty, ("Tier B", "oos"): empty}

        matched = matched_tier_trades(trades, features)

        self.assertEqual(len(matched), 1)
        self.assertEqual(matched.loc[0, "feature_match_status"], "matched")
        self.assertEqual(matched.loc[0, "matched_tier_scope"], "Tier A")


if __name__ == "__main__":
    unittest.main()
