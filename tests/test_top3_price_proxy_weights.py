from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "features" / "top3_price_proxy_weights.py"


def load_weights_module():
    module_name = "top3_price_proxy_weights"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class Top3PriceProxyWeightsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_weights_module()

    def _source(self, symbol: str, timestamps: list[str], closes: list[float]) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "timestamp": pd.to_datetime(timestamps, utc=True),
                self.module.CLOSE_COLUMNS[symbol]: closes,
            }
        )

    def test_compute_monthly_weights_covers_months_and_bootstraps_first_month(self) -> None:
        common = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(
                    [
                        "2022-08-01T16:40:00Z",
                        "2022-08-31T22:55:00Z",
                        "2022-09-30T22:55:00Z",
                    ],
                    utc=True,
                ),
                "msft_xnas_close": [100.0, 200.0, 300.0],
                "nvda_xnas_close": [50.0, 100.0, 300.0],
                "aapl_xnas_close": [50.0, 100.0, 400.0],
            }
        )
        spec = self.module.PriceProxyWeightSpec(start_month="2022-08", end_month="2022-10")

        weights = self.module.compute_monthly_price_proxy_weights(common, spec)

        self.assertEqual(weights["month"].tolist(), ["2022-08", "2022-09", "2022-10"])
        self.assertTrue(bool(weights.loc[0, "bootstrap_month"]))
        self.assertFalse(bool(weights.loc[1, "bootstrap_month"]))
        self.assertAlmostEqual(float(weights.loc[0, "weight_sum"]), 1.0, places=12)
        self.assertAlmostEqual(float(weights.loc[1, "msft_xnas_weight"]), 0.5, places=12)
        self.assertAlmostEqual(float(weights.loc[2, "aapl_xnas_weight"]), 0.4, places=12)

    def test_build_common_close_frame_fails_without_common_timestamp(self) -> None:
        frames = {
            "MSFT": self._source("MSFT", ["2022-08-01T16:40:00Z"], [100.0]),
            "NVDA": self._source("NVDA", ["2022-08-01T16:45:00Z"], [50.0]),
            "AAPL": self._source("AAPL", ["2022-08-01T16:50:00Z"], [50.0]),
        }

        with self.assertRaisesRegex(RuntimeError, "No common MT5 timestamp"):
            self.module.build_common_close_frame(frames)


if __name__ == "__main__":
    unittest.main()

