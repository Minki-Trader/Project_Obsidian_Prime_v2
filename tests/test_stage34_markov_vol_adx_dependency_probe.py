from __future__ import annotations

import unittest

import pandas as pd

from stage_pipelines.stage34.markov_long_permission_vol_adx_dependency_probe import (
    component_allowed_mask,
    component_rule_mask,
    hold_duration_read,
    hold_duration_rows,
    removal_reason,
    rule_from_record_view,
)


class Stage34MarkovVolAdxDependencyProbeTests(unittest.TestCase):
    def test_component_allowed_masks_split_vol_adx_and_overlap(self) -> None:
        frame = pd.DataFrame(
            {
                "volatility_regime": ["vol_mid", "vol_high", "vol_mid", "vol_high"],
                "adx_bucket": ["adx_gt25", "adx_gt25", "adx_20_25", "adx_20_25"],
            }
        )

        self.assertEqual(component_allowed_mask("exclude_vol_high", frame).tolist(), [True, False, True, False])
        self.assertEqual(component_allowed_mask("exclude_adx_20_25", frame).tolist(), [True, True, False, False])
        self.assertEqual(component_allowed_mask("exclude_vol_high_and_adx_20_25", frame).tolist(), [True, True, True, False])
        self.assertEqual(component_allowed_mask("exclude_vol_high_or_adx_20_25", frame).tolist(), [True, False, False, False])
        self.assertEqual(removal_reason(frame).tolist(), ["kept_context", "vol_high_only", "adx_20_25_only", "both_vol_high_and_adx_20_25"])

    def test_component_rule_mask_overlap_only_on_trade_rows(self) -> None:
        frame = pd.DataFrame(
            {
                "volatility_regime": ["vol_high", "vol_high", "vol_mid"],
                "adx_bucket": ["adx_20_25", "adx_gt25", "adx_20_25"],
            }
        )

        self.assertEqual(component_rule_mask("exclude_vol_high_and_adx_20_25", frame).tolist(), [False, True, True])

    def test_hold_duration_diagnostics_flags_long_runtime_holds(self) -> None:
        rows = pd.DataFrame(
            {
                "split": ["oos", "oos", "oos"],
                "hold_bars": [8, 120, 360],
                "net_profit": [1.0, 5.0, -2.0],
                "mae": [1.0, 1.0, 1.0],
                "mfe": [1.0, 1.0, 1.0],
                "realized_over_mfe": [1.0, 1.0, -2.0],
            }
        )

        diagnostics = hold_duration_rows(rows)
        read = hold_duration_read(diagnostics)

        self.assertEqual(diagnostics[0]["gt_96_count"], 2)
        self.assertIn("feature_ready", read["mechanism_read"])

    def test_record_view_parser_prefers_overlap_rule_before_prefix_rule(self) -> None:
        view = "mt5_tier_a_component_exclude_vol_high_and_adx_20_25_oos"

        self.assertEqual(rule_from_record_view(view), "exclude_vol_high_and_adx_20_25")


if __name__ == "__main__":
    unittest.main()
