from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from foundation.control_plane.kpi_interpretation_audit import audit_kpi_interpretation_ledgers


class KpiInterpretationAuditTests(unittest.TestCase):
    def test_missing_required_tier_row_cannot_claim_economic_columns(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            ledger = Path(temp_dir) / "ledger.csv"
            _write_rows(
                ledger,
                [
                    {
                        "ledger_row_id": "unit__tier_b_missing",
                        "run_id": "unit",
                        "record_view": "Tier B separate",
                        "tier_scope": "Tier B missing_required",
                        "kpi_scope": "missing_required",
                        "scoreboard_lane": "runtime_probe",
                        "status": "reviewed",
                        "judgment": "missing_required",
                        "external_verification_status": "out_of_scope_by_claim",
                        "net_profit": "12.5",
                        "profit_factor": "1.2",
                        "trade_count": "40",
                    }
                ],
            )

            result = audit_kpi_interpretation_ledgers([ledger])

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "kpi_interpretation::missing_or_out_of_scope_row_has_economic_metrics",
            {finding.check_id for finding in result.findings},
        )

    def test_actual_routed_total_with_missing_component_language_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            ledger = Path(temp_dir) / "ledger.csv"
            _write_rows(
                ledger,
                [
                    {
                        "ledger_row_id": "unit__routed_total",
                        "run_id": "unit",
                        "record_view": "actual routed total",
                        "tier_scope": "Tier A used; Tier B missing_required; actual routed total",
                        "kpi_scope": "trading_risk_execution",
                        "scoreboard_lane": "runtime_probe",
                        "status": "completed",
                        "judgment": "inconclusive_routed_total_runtime_probe",
                        "external_verification_status": "completed",
                        "net_profit": "12.5",
                        "profit_factor": "1.2",
                        "trade_count": "40",
                    }
                ],
            )

            result = audit_kpi_interpretation_ledgers([ledger])

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])

    def test_tier_a_row_with_composite_missing_note_warns_not_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            ledger = Path(temp_dir) / "ledger.csv"
            _write_rows(
                ledger,
                [
                    {
                        "ledger_row_id": "unit__tier_a_runtime",
                        "run_id": "unit",
                        "record_view": "Tier A MT5 Runtime Probe",
                        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
                        "kpi_scope": "runtime_probe_kpi",
                        "scoreboard_lane": "runtime_probe",
                        "status": "completed",
                        "judgment": "negative",
                        "external_verification_status": "completed",
                        "net_profit": "-12.5",
                        "profit_factor": "0.8",
                        "trade_count": "40",
                    }
                ],
            )

            result = audit_kpi_interpretation_ledgers([ledger])

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])
        self.assertIn(
            "kpi_interpretation::mixed_scope_economic_metrics_need_boundary",
            {finding.check_id for finding in result.findings},
        )

    def test_economic_rows_need_context_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            ledger = Path(temp_dir) / "ledger.csv"
            _write_rows(
                ledger,
                [
                    {
                        "ledger_row_id": "unit__economics",
                        "run_id": "unit",
                        "record_view": "runtime materialization",
                        "tier_scope": "Tier A",
                        "net_profit": "12.5",
                    }
                ],
            )

            result = audit_kpi_interpretation_ledgers([ledger])

        self.assertEqual(result.status, "pass")
        self.assertIn(
            "kpi_interpretation::economic_row_missing_context",
            {finding.check_id for finding in result.findings},
        )


def _write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    columns = [
        "ledger_row_id",
        "run_id",
        "stage_id",
        "record_view",
        "tier_scope",
        "kpi_scope",
        "scoreboard_lane",
        "status",
        "judgment",
        "result_judgment",
        "external_verification_status",
        "net_profit",
        "profit_factor",
        "drawdown",
        "trade_count",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


if __name__ == "__main__":
    unittest.main()
