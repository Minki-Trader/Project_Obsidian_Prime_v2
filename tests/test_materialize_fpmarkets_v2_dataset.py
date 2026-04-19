from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "pipelines" / "materialize_fpmarkets_v2_dataset.py"
RAW_ROOT = REPO_ROOT / "data" / "raw" / "mt5_bars" / "m5"


def load_dataset_module():
    module_name = "materialize_fpmarkets_v2_dataset"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class MaterializeDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_dataset_module()
        cls.frame, _ = cls.module.build_feature_frame(RAW_ROOT)
        cls.bindings = {
            binding.contract_symbol: binding for binding in cls.module.SYMBOL_BINDINGS
        }

    def row_at(self, timestamp_utc: str) -> pd.Series:
        target = pd.Timestamp(timestamp_utc)
        row = self.frame.loc[self.frame["timestamp"] == target]
        if row.empty:
            raise RuntimeError(f"Timestamp not found in feature frame: {timestamp_utc}")
        return row.iloc[0]

    def direct_proxy_value(self, symbol: str, timestamp_utc: str, field: str) -> float:
        source = self.module.load_raw_symbol(RAW_ROOT, self.bindings[symbol])
        prepared = source[["timestamp", "close"]].copy()
        prepared["change_1"] = prepared["close"] / prepared["close"].shift(1) - 1.0
        prepared["zscore_20"] = self.module.rolling_zscore(prepared["close"], 20)
        row = prepared.loc[prepared["timestamp"] == pd.Timestamp(timestamp_utc)]
        if row.empty:
            raise RuntimeError(f"Timestamp not found in raw source {symbol}: {timestamp_utc}")
        return float(row.iloc[0][field])

    def test_proxy_features_are_computed_on_raw_symbol_series_before_merge(self) -> None:
        row = self.row_at("2025-09-30T20:05:00Z")

        self.assertTrue(bool(row["valid_row"]))
        self.assertFalse(bool(row["invalid__external_alignment_missing"]))

        self.assertAlmostEqual(
            float(row["vix_change_1"]),
            self.direct_proxy_value("VIX", "2025-09-30T20:05:00Z", "change_1"),
            places=12,
        )
        self.assertAlmostEqual(
            float(row["vix_zscore_20"]),
            self.direct_proxy_value("VIX", "2025-09-30T20:05:00Z", "zscore_20"),
            places=12,
        )
        self.assertAlmostEqual(
            float(row["us10yr_change_1"]),
            self.direct_proxy_value("US10YR", "2025-09-30T20:05:00Z", "change_1"),
            places=12,
        )
        self.assertAlmostEqual(
            float(row["us10yr_zscore_20"]),
            self.direct_proxy_value("US10YR", "2025-09-30T20:05:00Z", "zscore_20"),
            places=12,
        )

    def test_supertrend_seed_rule_defaults_to_downtrend_until_updated_band_exists(self) -> None:
        high = pd.Series([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], dtype="float64")
        low = pd.Series([9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], dtype="float64")
        close = pd.Series([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], dtype="float64")

        state = self.module.compute_supertrend_state(high, low, close, 10, 3.0)

        self.assertTrue(pd.isna(state.iloc[8]))
        self.assertEqual(float(state.iloc[9]), -1.0)
        self.assertEqual(float(state.iloc[10]), -1.0)
