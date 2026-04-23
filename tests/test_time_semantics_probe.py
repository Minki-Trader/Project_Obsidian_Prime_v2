from __future__ import annotations

import csv
import importlib.util
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "collectors" / "time_semantics_probe.py"


def load_probe_module():
    module_name = "time_semantics_probe"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class TimeSemanticsProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_probe_module()

    def write_equity_csv(self, raw_root: Path, symbol: str, opens: list[str]) -> None:
        symbol_dir = raw_root / symbol
        symbol_dir.mkdir(parents=True)
        csv_path = symbol_dir / f"bars_{symbol.lower()}_m5_mt5api_raw.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            fieldnames = ("time_open_unix",)
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for value in opens:
                dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
                writer.writerow({"time_open_unix": int(dt.timestamp())})

    def test_build_probe_flags_broker_clock_like_offsets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_root = Path(temp_dir) / "raw"
            self.write_equity_csv(
                raw_root,
                "AAPL",
                [
                    "2025-01-02T16:30:00Z",
                    "2025-01-02T16:35:00Z",
                    "2025-07-01T16:30:00Z",
                    "2025-07-01T16:35:00Z",
                ],
            )

            probe = self.module.build_probe(
                raw_root,
                symbols=(self.module.EquitySessionSymbol("AAPL", "AAPL.xnas"),),
                repo_root=Path(temp_dir),
            )

            self.assertEqual(probe["summary"]["candidate_interpretation"], "broker_server_wall_clock_candidate")
            self.assertEqual(probe["summary"]["direct_utc_match_ratio"], 0.0)
            self.assertEqual(probe["summary"]["first_open_offset_distribution"], {"+2h": 1, "+3h": 1})

    def test_build_probe_reports_missing_csv_as_mixed_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            raw_root = Path(temp_dir) / "raw"
            probe = self.module.build_probe(
                raw_root,
                symbols=(self.module.EquitySessionSymbol("AAPL", "AAPL.xnas"),),
                repo_root=Path(temp_dir),
            )

            self.assertEqual(probe["summary"]["candidate_interpretation"], "mixed_or_incomplete_candidate")
            self.assertIn("AAPL: expected one CSV, found 0", probe["summary"]["notes"])


if __name__ == "__main__":
    unittest.main()
