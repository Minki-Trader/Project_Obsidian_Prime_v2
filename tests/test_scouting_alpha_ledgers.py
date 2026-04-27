from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from foundation.scouting import alpha_ledgers


class AlphaLedgerTests(unittest.TestCase):
    def test_routed_component_rows_do_not_claim_profit(self) -> None:
        records = [
            {
                "record_view": "mt5_routed_tier_a_used_validation_is",
                "tier_scope": alpha_ledgers.TIER_A,
                "status": "completed",
                "route_role": "primary_used",
                "metrics": {
                    "route_bar_count": 10,
                    "route_share": 0.8,
                    "signal_count": 4,
                    "long_count": 3,
                    "short_count": 1,
                    "fill_count": 4,
                    "reject_count": 0,
                    "skip_count": 0,
                    "profit_attribution": "not_separable_from_single_routed_account_path",
                },
                "report": {},
            },
            {
                "record_view": "mt5_routed_total_validation_is",
                "tier_scope": alpha_ledgers.TIER_AB,
                "status": "completed",
                "route_role": "routed_total",
                "metrics": {
                    "net_profit": 12.5,
                    "profit_factor": 1.25,
                    "expectancy": 0.5,
                    "trade_count": 25,
                    "win_rate_percent": 56.0,
                    "tier_a_used_count": 10,
                    "tier_b_fallback_used_count": 2,
                    "no_tier_labelable_rows": 1,
                    "max_drawdown_amount": 3.0,
                    "recovery_factor": 4.0,
                    "fill_count": 5,
                    "reject_count": 0,
                    "skip_count": 0,
                },
                "report": {},
            },
        ]

        rows = alpha_ledgers.build_mt5_alpha_ledger_rows(
            run_id="unit_run",
            stage_id="unit_stage",
            mt5_kpi_records=records,
            run_output_root=Path("stages/unit_stage/02_runs/unit_run"),
            external_verification_status="completed",
        )

        component = rows[0]
        total = rows[1]
        self.assertEqual(component["kpi_scope"], "routed_signal_execution_usage")
        self.assertNotIn("net_profit", component["primary_kpi"])
        self.assertIn("profit_attribution=not_separable_from_single_routed_account_path", component["guardrail_kpi"])
        self.assertEqual(total["kpi_scope"], "trading_risk_execution")
        self.assertIn("net_profit=12.5", total["primary_kpi"])
        self.assertIn("max_dd=3", total["guardrail_kpi"])

    def test_materialize_alpha_ledgers_upserts_stage_and_project_registers(self) -> None:
        row = {
            "ledger_row_id": "unit_run__mt5_routed_total_validation_is",
            "stage_id": "unit_stage",
            "run_id": "unit_run",
            "subrun_id": "mt5_routed_total_validation_is",
            "parent_run_id": "unit_run",
            "record_view": "mt5_routed_total_validation_is",
            "tier_scope": alpha_ledgers.TIER_AB,
            "kpi_scope": "trading_risk_execution",
            "scoreboard_lane": "runtime_probe",
            "status": "completed",
            "judgment": "inconclusive_routed_total_runtime_probe",
            "path": "stages/unit_stage/02_runs/unit_run/kpi_record.json",
            "primary_kpi": "net_profit=12.5",
            "guardrail_kpi": "max_dd=3",
            "external_verification_status": "completed",
            "notes": "unit",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            payload = alpha_ledgers.materialize_alpha_ledgers(
                stage_run_ledger_path=root / "stage_run_ledger.csv",
                project_alpha_ledger_path=root / "alpha_run_ledger.csv",
                rows=[row],
            )

            self.assertEqual(payload["stage_run_ledger"]["upserted_rows"], 1)
            self.assertEqual(payload["project_alpha_run_ledger"]["upserted_rows"], 1)
            self.assertIn("unit_run__mt5_routed_total_validation_is", (root / "stage_run_ledger.csv").read_text())
            self.assertIn("unit_run__mt5_routed_total_validation_is", (root / "alpha_run_ledger.csv").read_text())


if __name__ == "__main__":
    unittest.main()

