from __future__ import annotations

import csv
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "collectors" / "raw_m5_inventory.py"


def load_inventory_module():
    module_name = "raw_m5_inventory"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class RawM5InventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_inventory_module()

    def write_symbol(self, root: Path, symbol: str, broker: str, *, row_count: int = 3) -> None:
        symbol_dir = root / symbol
        symbol_dir.mkdir(parents=True)
        csv_path = symbol_dir / f"bars_{broker.lower().replace('.', '_')}_m5_mt5api_raw.csv"
        rows = []
        start = 1659315600
        for index in range(row_count):
            open_unix = start + index * 300
            rows.append(
                {
                    "time_open_unix": open_unix,
                    "time_close_unix": open_unix + 300,
                    "contract_symbol": symbol,
                    "broker_symbol": broker,
                    "timeframe": "M5",
                    "price_basis": "Bid",
                    "open": "1.0",
                    "high": "1.1",
                    "low": "0.9",
                    "close": "1.0",
                    "tick_volume": "10",
                    "spread_points": "1",
                    "real_volume": "0",
                    "time_basis": "MT5_PY_API_UNIX_SECONDS",
                    "timezone_status": "UNRESOLVED_REQUIRES_MANUAL_BINDING",
                }
            )
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=self.module.REQUIRED_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

        manifest = {
            "row_count": row_count,
            "resolved_first_open_unix": rows[0]["time_open_unix"],
            "resolved_last_open_unix": rows[-1]["time_open_unix"],
            "contract_symbol": symbol,
            "broker_symbol": broker,
            "timeframe": "M5",
        }
        manifest_path = symbol_dir / f"bars_{broker.lower().replace('.', '_')}_m5_mt5api_raw.manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    def test_build_inventory_marks_complete_symbols_usable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_root = Path(temp_dir) / "raw"
            self.write_symbol(raw_root, "US100", "US100")
            inventory = self.module.build_inventory(
                raw_root,
                expected_symbols=(self.module.SymbolExpectation("US100", "US100"),),
                repo_root=Path(temp_dir),
            )

            self.assertEqual(inventory["summary"]["status"], "complete")
            self.assertEqual(inventory["summary"]["usable_symbol_count"], 1)
            self.assertEqual(inventory["symbols"][0]["status"], "usable_raw_inventory")
            self.assertEqual(inventory["symbols"][0]["row_count"], 3)

    def test_build_inventory_reports_manifest_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_root = Path(temp_dir) / "raw"
            self.write_symbol(raw_root, "US100", "US100")
            manifest_path = next((raw_root / "US100").glob("*.manifest.json"))
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["row_count"] = 99
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            inventory = self.module.build_inventory(
                raw_root,
                expected_symbols=(self.module.SymbolExpectation("US100", "US100"),),
                repo_root=Path(temp_dir),
            )

            self.assertEqual(inventory["summary"]["status"], "attention_needed")
            self.assertEqual(inventory["symbols"][0]["manifest_status"], "mismatch")
            self.assertEqual(inventory["symbols"][0]["status"], "manifest_mismatch")


if __name__ == "__main__":
    unittest.main()
