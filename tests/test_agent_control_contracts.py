from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from foundation.control_plane.agent_control_contracts import (
    EXPECTED_KPI_LAYERS,
    EXPECTED_ROW_GRAIN_KEYS,
    audit_agent_control_contracts,
)


ROOT = Path(__file__).resolve().parents[1]


class AgentControlContractTests(unittest.TestCase):
    def test_agent_control_contracts_are_present_and_consistent(self) -> None:
        result = audit_agent_control_contracts(ROOT)

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])
        self.assertFalse(result.completed_forbidden)

    def test_kpi_authority_keeps_mt5_headline_as_authority(self) -> None:
        payload = yaml.safe_load((ROOT / "docs/agent_control/kpi_source_authority.yaml").read_text(encoding="utf-8"))

        self.assertEqual(payload["layers"]["mt5_trading_headline"]["authority"], "mt5_strategy_tester_report")
        self.assertEqual(payload["layers"]["mt5_trading_headline"]["python_role"], "cross_check_only")
        self.assertEqual(payload["special_policies"]["profit_factor"]["if_gross_loss_zero"]["n_a_reason"], "gross_loss_is_zero")

    def test_row_grain_contract_contains_fixed_normalized_key(self) -> None:
        payload = yaml.safe_load((ROOT / "docs/agent_control/row_grain_contract.yaml").read_text(encoding="utf-8"))

        self.assertEqual(tuple(payload["normalized_row_key"]), EXPECTED_ROW_GRAIN_KEYS)

    def test_normalized_kpi_template_contains_seven_layers(self) -> None:
        import json

        payload = json.loads((ROOT / "docs/templates/kpi_record_normalized.template.json").read_text(encoding="utf-8"))

        for layer in EXPECTED_KPI_LAYERS:
            self.assertIn(layer, payload)
        self.assertEqual(payload["mt5_trading_headline"]["net_profit"]["authority"], "mt5_strategy_tester_report")
        self.assertIn("n/a_reason", payload["row_grain"]["variant_id"])

    def test_missing_surface_registry_entry_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _copy_agent_control_fixture(Path(tmp))
            path = root / "docs/agent_control/surface_registry.yaml"
            payload = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
            payload["surfaces"].pop("pipelines")
            path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

            result = audit_agent_control_contracts(root)

        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(finding.check_id == "surface_registry::missing_surfaces" for finding in result.findings))

    def test_missing_risk_flag_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _copy_agent_control_fixture(Path(tmp))
            path = root / "docs/agent_control/risk_flag_registry.yaml"
            payload = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
            payload["risks"].pop("code_surface_risk")
            path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

            result = audit_agent_control_contracts(root)

        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(finding.check_id == "risk_flag_registry::missing_risks" for finding in result.findings))

    def test_missing_skill_receipt_schema_default_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = _copy_agent_control_fixture(Path(tmp))
            path = root / "docs/agent_control/skill_receipt_schema.yaml"
            payload = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
            payload["schemas"].pop("default")
            path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

            result = audit_agent_control_contracts(root)

        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(finding.check_id == "skill_receipt_schema::missing_default" for finding in result.findings))


def _copy_agent_control_fixture(root: Path) -> Path:
    shutil.copytree(ROOT / "docs/agent_control", root / "docs/agent_control")
    shutil.copytree(ROOT / "docs/templates", root / "docs/templates")
    return root


if __name__ == "__main__":
    unittest.main()
