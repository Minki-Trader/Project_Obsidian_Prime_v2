from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "docs/agent_control/row_grain_contract.yaml"
NORMALIZED_PATH = ROOT / "docs/agent_control/packets/kpi_rebuild_mt5_recording_v1/normalized_kpi_records.jsonl"


class RowGrainContractTests(unittest.TestCase):
    def test_checked_in_normalized_records_match_contract_allowed_values(self) -> None:
        contract = yaml.safe_load(CONTRACT_PATH.read_text(encoding="utf-8-sig"))
        allowed = {
            str(field): {str(value) for value in values or []}
            for field, values in contract.get("allowed_values", {}).items()
        }
        self.assertTrue(allowed, "row_grain_contract has no allowed_values")
        self.assertTrue(NORMALIZED_PATH.exists(), "checked-in normalized KPI records are missing")

        failures: list[tuple[int, str, str]] = []
        for line_index, line in enumerate(NORMALIZED_PATH.read_text(encoding="utf-8-sig").splitlines(), start=1):
            if not line.strip():
                continue
            row_grain = json.loads(line).get("row_grain", {})
            for field, field_allowed in allowed.items():
                cell = row_grain.get(field, {})
                value = cell.get("value") if isinstance(cell, dict) else None
                if value is not None and str(value) not in field_allowed:
                    failures.append((line_index, field, str(value)))

        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
