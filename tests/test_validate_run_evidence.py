from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from foundation.control_plane.ledger import ALPHA_LEDGER_COLUMNS, write_csv_rows
from foundation.control_plane.validate_run_evidence import audit_run_evidence


class ValidateRunEvidenceTests(unittest.TestCase):
    def test_passes_registered_reason_row_grain_and_ledger_counterpart(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_contracts(root)
            normalized = root / "records.jsonl"
            normalized.write_text(json.dumps(_record()) + "\n", encoding="utf-8")
            ledger = root / "ledger.csv"
            write_csv_rows(ledger, ALPHA_LEDGER_COLUMNS, [_ledger_row()])

            result = audit_run_evidence(
                root=root,
                normalized_jsonl_paths=[normalized],
                stage_ledger_paths=[ledger],
            )

        self.assertEqual(result.status, "pass", result.to_dict())

    def test_blocks_unregistered_reason_null_without_reason_and_missing_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_contracts(root)
            bad = _record()
            bad["mt5_trading_headline"]["net_profit"] = {
                "value": None,
                "n/a_reason": "freeform_reason",
                "authority": "unit",
            }
            bad["risk"]["max_drawdown_amount"] = {"value": None, "n/a_reason": None, "authority": "unit"}
            normalized = root / "records.jsonl"
            normalized.write_text(json.dumps(bad) + "\n", encoding="utf-8")

            result = audit_run_evidence(root=root, normalized_jsonl_paths=[normalized], stage_ledger_paths=[root / "ledger.csv"])

        self.assertEqual(result.status, "blocked")
        check_ids = {finding.check_id for finding in result.findings}
        self.assertIn("n_a_reason::unregistered", check_ids)
        self.assertIn("n_a_reason::missing_for_null", check_ids)
        self.assertIn("ledger::missing_counterpart", check_ids)

    def test_blocks_partial_mt5_parse_for_trading_total(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_contracts(root)
            record = _record()
            record["source_evidence"] = {
                "mt5_report_parse_status": "partial",
                "mt5_report_missing_required_metrics": ["max_drawdown_amount"],
                "mt5_report_path": "report.htm",
            }
            normalized = root / "records.jsonl"
            normalized.write_text(json.dumps(record) + "\n", encoding="utf-8")

            result = audit_run_evidence(
                root=root,
                normalized_jsonl_paths=[normalized],
                require_completed_mt5_report_parse=True,
            )

        self.assertEqual(result.status, "blocked")
        self.assertIn("mt5_report_parse::partial_required_metrics", {finding.check_id for finding in result.findings})

    def test_completed_mt5_parse_passes_strict_parse_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_contracts(root)
            record = _record()
            record["source_evidence"] = {
                "mt5_report_parse_status": "completed",
                "mt5_report_missing_required_metrics": [],
                "mt5_report_path": "report.htm",
            }
            normalized = root / "records.jsonl"
            normalized.write_text(json.dumps(record) + "\n", encoding="utf-8")

            result = audit_run_evidence(
                root=root,
                normalized_jsonl_paths=[normalized],
                require_completed_mt5_report_parse=True,
            )

        self.assertEqual(result.status, "pass", result.to_dict())

    def test_blocks_when_project_ledger_counterpart_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_contracts(root)
            normalized = root / "records.jsonl"
            normalized.write_text(json.dumps(_record()) + "\n", encoding="utf-8")
            stage = root / "stage.csv"
            project = root / "project.csv"
            write_csv_rows(stage, ALPHA_LEDGER_COLUMNS, [_ledger_row()])
            write_csv_rows(project, ALPHA_LEDGER_COLUMNS, [])

            result = audit_run_evidence(
                root=root,
                normalized_jsonl_paths=[normalized],
                stage_ledger_paths=[stage],
                project_ledger_path=project,
                require_stage_and_project_ledger_counterparts=True,
            )

        self.assertEqual(result.status, "blocked")
        self.assertIn("ledger::missing_project_counterpart", {finding.check_id for finding in result.findings})

    def test_blocks_when_stage_ledger_counterpart_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_contracts(root)
            normalized = root / "records.jsonl"
            normalized.write_text(json.dumps(_record()) + "\n", encoding="utf-8")
            stage = root / "stage.csv"
            project = root / "project.csv"
            write_csv_rows(stage, ALPHA_LEDGER_COLUMNS, [])
            write_csv_rows(project, ALPHA_LEDGER_COLUMNS, [_ledger_row()])

            result = audit_run_evidence(
                root=root,
                normalized_jsonl_paths=[normalized],
                stage_ledger_paths=[stage],
                project_ledger_path=project,
                require_stage_and_project_ledger_counterparts=True,
            )

        self.assertEqual(result.status, "blocked")
        self.assertIn("ledger::missing_stage_counterpart", {finding.check_id for finding in result.findings})

    def test_derive_run_roots_from_records_blocks_missing_required_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_contracts(root)
            run_root = root / "stages/unit/02_runs/unit_run"
            run_root.mkdir(parents=True)
            (run_root / "kpi_record.json").write_text("{}", encoding="utf-8")
            record = _record()
            record["source_evidence"] = {"kpi_record_path": "stages/unit/02_runs/unit_run/kpi_record.json"}
            normalized = root / "records.jsonl"
            normalized.write_text(json.dumps(record) + "\n", encoding="utf-8")

            result = audit_run_evidence(
                root=root,
                normalized_jsonl_paths=[normalized],
                derive_run_roots_from_records=True,
            )

        self.assertEqual(result.status, "blocked")
        self.assertIn("run_root::missing_required_file", {finding.check_id for finding in result.findings})

    def test_required_skill_receipt_missing_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_contracts(root)
            packet = root / "work_packet.yaml"
            packet.write_text(
                "skill_routing:\n  required_skill_receipts:\n    - docs/receipts/runtime.yaml\n",
                encoding="utf-8",
            )

            result = audit_run_evidence(root=root, work_packet_paths=[packet], require_skill_receipts=True)

        self.assertEqual(result.status, "blocked")
        self.assertIn("skill_receipt::missing_required_receipt", {finding.check_id for finding in result.findings})

    def test_mt5_identity_missing_report_hash_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_contracts(root)
            run_root = root / "stages/unit/02_runs/unit_run"
            run_root.mkdir(parents=True)
            (run_root / "kpi_record.json").write_text("{}", encoding="utf-8")
            (run_root / "run_manifest.json").write_text("{}", encoding="utf-8")
            record = _record()
            record["source_evidence"] = {
                "kpi_record_path": "stages/unit/02_runs/unit_run/kpi_record.json",
                "mt5_report_sha256": None,
            }
            normalized = root / "records.jsonl"
            normalized.write_text(json.dumps(record) + "\n", encoding="utf-8")

            result = audit_run_evidence(root=root, normalized_jsonl_paths=[normalized], require_mt5_identity=True)

        self.assertEqual(result.status, "blocked")
        self.assertIn("mt5_identity::missing_report_hash", {finding.check_id for finding in result.findings})


def _seed_contracts(root: Path) -> None:
    registry = root / "docs/agent_control/n_a_reason_registry.yaml"
    registry.parent.mkdir(parents=True)
    registry.write_text(
        "\n".join(
            [
                "version: unit",
                "allowed_reasons:",
                "  metric_not_emitted_by_mt5: {category: source, use_when: unit}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    row_grain = root / "docs/agent_control/row_grain_contract.yaml"
    row_grain.write_text(
        "\n".join(
            [
                "version: unit",
                "allowed_values:",
                "  split: [validation]",
                "  tier_scope: [Tier A+B]",
                "  record_view: [mt5_routed_total_validation_is]",
                "  route_role: [routed_total]",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _record() -> dict:
    return {
        "row_grain": {
            "run_id": {"value": "unit_run", "n/a_reason": None, "authority": "unit"},
            "variant_id": {"value": "unit_variant", "n/a_reason": None, "authority": "unit"},
            "split": {"value": "validation", "n/a_reason": None, "authority": "unit"},
            "tier_scope": {"value": "Tier A+B", "n/a_reason": None, "authority": "unit"},
            "record_view": {"value": "mt5_routed_total_validation_is", "n/a_reason": None, "authority": "unit"},
            "route_role": {"value": "routed_total", "n/a_reason": None, "authority": "unit"},
        },
        "run_identity": {"stage_id": {"value": "unit_stage", "n/a_reason": None, "authority": "unit"}},
        "mt5_trading_headline": {
            "net_profit": {"value": 1.0, "n/a_reason": None, "authority": "unit"},
        },
        "risk": {
            "max_drawdown_amount": {"value": 2.0, "n/a_reason": None, "authority": "unit"},
        },
    }


def _ledger_row() -> dict:
    return {
        "ledger_row_id": "unit_run__mt5_routed_total_validation_is",
        "stage_id": "unit_stage",
        "run_id": "unit_run",
        "subrun_id": "mt5_routed_total_validation_is",
        "parent_run_id": "unit_run",
        "record_view": "mt5_routed_total_validation_is",
        "tier_scope": "Tier A+B",
        "kpi_scope": "runtime_probe",
        "scoreboard_lane": "runtime_probe",
        "status": "completed",
        "judgment": "inconclusive",
        "path": "unit.htm",
        "primary_kpi": "net_profit=1",
        "guardrail_kpi": "",
        "external_verification_status": "completed",
        "notes": "unit",
    }


if __name__ == "__main__":
    unittest.main()
