from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from foundation.control_plane.kpi_interpretation_cleanup import (
    KpiCleanupError,
    cleanup_kpi_interpretation_findings,
)


class KpiInterpretationCleanupTests(unittest.TestCase):
    def test_cleanup_clears_only_flagged_economic_values_and_writes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ledger = root / "ledger.csv"
            audit = root / "audit.json"
            manifest = root / "manifest.json"
            _write_rows(
                ledger,
                [
                    {
                        "ledger_row_id": "row_blocked",
                        "run_id": "run01",
                        "record_view": "Tier B separate",
                        "tier_scope": "Tier B missing_required",
                        "kpi_scope": "missing_required",
                        "status": "blocked",
                        "net_profit": "12.5",
                        "profit_factor": "1.2",
                        "trade_count": "40",
                    },
                    {
                        "ledger_row_id": "row_ok",
                        "run_id": "run02",
                        "record_view": "actual routed total",
                        "tier_scope": "actual routed total",
                        "kpi_scope": "runtime_probe",
                        "status": "completed",
                        "net_profit": "99.0",
                        "profit_factor": "1.9",
                        "trade_count": "140",
                    },
                ],
            )
            _write_audit(audit, ledger, line=2)

            result = cleanup_kpi_interpretation_findings(audit, output_manifest=manifest)

            rows = _read_rows(ledger)
            self.assertEqual(rows[0]["net_profit"], "")
            self.assertEqual(rows[0]["profit_factor"], "")
            self.assertEqual(rows[0]["trade_count"], "")
            self.assertEqual(rows[0]["status"], "blocked")
            self.assertEqual(rows[1]["net_profit"], "99.0")
            self.assertEqual(result["cleaned_rows"], 1)
            written_manifest = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(written_manifest["cleared_values"], 3)
            self.assertEqual(
                written_manifest["cleaned_files"][0]["rows"][0]["cleared_values"],
                {"net_profit": "12.5", "profit_factor": "1.2", "trade_count": "40"},
            )

    def test_cleanup_refuses_identity_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ledger = root / "ledger.csv"
            audit = root / "audit.json"
            _write_rows(
                ledger,
                [
                    {
                        "ledger_row_id": "different_row",
                        "run_id": "run01",
                        "record_view": "Tier B separate",
                        "tier_scope": "Tier B missing_required",
                        "kpi_scope": "missing_required",
                        "net_profit": "12.5",
                    }
                ],
            )
            _write_audit(audit, ledger, line=2)

            with self.assertRaises(KpiCleanupError):
                cleanup_kpi_interpretation_findings(audit)

    def test_dry_run_writes_manifest_without_mutating_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ledger = root / "ledger.csv"
            audit = root / "audit.json"
            manifest = root / "manifest.json"
            _write_rows(
                ledger,
                [
                    {
                        "ledger_row_id": "row_blocked",
                        "run_id": "run01",
                        "record_view": "Tier B separate",
                        "tier_scope": "Tier B missing_required",
                        "kpi_scope": "missing_required",
                        "net_profit": "12.5",
                    }
                ],
            )
            before = ledger.read_text(encoding="utf-8")
            _write_audit(audit, ledger, line=2, economic_values={"net_profit": "12.5"})

            cleanup_kpi_interpretation_findings(audit, output_manifest=manifest, dry_run=True)

            self.assertEqual(ledger.read_text(encoding="utf-8"), before)
            self.assertTrue(manifest.exists())


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
        "trade_count",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_audit(
    path: Path,
    ledger: Path,
    *,
    line: int,
    economic_values: dict[str, str] | None = None,
) -> None:
    path.write_text(
        json.dumps(
            {
                "audit_name": "kpi_interpretation_audit",
                "status": "blocked",
                "findings": [
                    {
                        "check_id": "kpi_interpretation::missing_or_out_of_scope_row_has_economic_metrics",
                        "message": "blocked",
                        "severity": "blocking",
                        "details": {
                            "path": ledger.as_posix(),
                            "line": line,
                            "ledger_row_id": "row_blocked",
                            "run_id": "run01",
                            "record_view": "Tier B separate",
                            "tier_scope": "Tier B missing_required",
                            "kpi_scope": "missing_required",
                            "economic_values": economic_values
                            or {"net_profit": "12.5", "profit_factor": "1.2", "trade_count": "40"},
                        },
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
