from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.mt5.runtime_support import TIER_A
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

    def test_attempt_payload_respects_explicit_ebm_table_backend_for_masked_csv_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_root = Path(temp_dir) / "run"
            payload = attempt_payload(
                run_root=run_root,
                run_id="unit_run",
                stage_number=19,
                exploration_label="unit",
                attempt_name="tier_a_only_oos",
                tier=TIER_A,
                split="oos",
                model_path="Project_Obsidian_Prime_v2/stage19/unit/models/model_top5_mask.csv",
                model_id="unit_model",
                model_backend="ebm_table",
                feature_path="Project_Obsidian_Prime_v2/stage19/unit/features/tier_a.csv",
                feature_count=3,
                feature_order_hash="abc",
                short_threshold=0.5,
                long_threshold=0.5,
                min_margin=0.0,
                invert_signal=False,
                from_date="2025.01.01",
                to_date="2025.01.02",
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix="unit",
                max_hold_bars=4,
                common_root="Project_Obsidian_Prime_v2/stage19/unit",
            )

            set_text = Path(payload["set"]["path"]).read_text(encoding="utf-8")

        self.assertIn("InpModelBackend=ebm_table", set_text)
        self.assertIn("InpFallbackModelBackend=ebm_table", set_text)


if __name__ == "__main__":
    unittest.main()
