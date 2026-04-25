from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "pipelines" / "materialize_fpmarkets_v2_dataset.py"
RAW_ROOT = REPO_ROOT / "data" / "raw" / "mt5_bars" / "m5"
RUN_SLOW_INTEGRATION_TESTS = os.environ.get("OBSIDIAN_RUN_SLOW_TESTS") == "1"
SLOW_INTEGRATION_SKIP_REASON = "set OBSIDIAN_RUN_SLOW_TESTS=1 to run raw-data integration tests"


def load_dataset_module():
    module_name = "materialize_fpmarkets_v2_dataset"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless(RUN_SLOW_INTEGRATION_TESTS, SLOW_INTEGRATION_SKIP_REASON)
class MaterializeDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_dataset_module()
        cls.frame, cls.counts = cls.module.build_feature_frame(RAW_ROOT)
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

    def direct_stock_value(self, symbol: str, timestamp_utc: str, *, field: str) -> float:
        source = self.module.load_raw_symbol(RAW_ROOT, self.bindings[symbol]).copy()
        source["simple_return_1"] = source["close"] / source["close"].shift(1) - 1.0
        source["simple_return_5"] = source["close"] / source["close"].shift(5) - 1.0
        source["log_return_1"] = np.log(source["close"] / source["close"].shift(1))
        row = source.loc[source["timestamp"] == pd.Timestamp(timestamp_utc)]
        if row.empty:
            raise RuntimeError(f"Timestamp not found in raw source {symbol}: {timestamp_utc}")
        return float(row.iloc[0][field])

    def previous_available_timestamp(self, symbol: str, timestamp_utc: str) -> pd.Timestamp:
        source = self.module.load_raw_symbol(RAW_ROOT, self.bindings[symbol]).copy()
        target_index = source.index[source["timestamp"] == pd.Timestamp(timestamp_utc)]
        if len(target_index) != 1:
            raise RuntimeError(f"Timestamp not found in raw source {symbol}: {timestamp_utc}")
        index = int(target_index[0])
        return pd.Timestamp(source.iloc[index - 1]["timestamp"])

    def write_weights_csv(
        self,
        path: Path,
        *,
        default_weight: float = 1.0 / 3.0,
        overrides: dict[str, dict[str, float]] | None = None,
    ) -> None:
        month_index = pd.period_range("2022-08", "2026-04", freq="M").astype(str)
        rows = []
        overrides = overrides or {}
        for month in month_index:
            row = {
                "month": month,
                "msft_xnas_weight": default_weight,
                "nvda_xnas_weight": default_weight,
                "aapl_xnas_weight": default_weight,
            }
            row.update(overrides.get(month, {}))
            rows.append(row)
        pd.DataFrame(rows).to_csv(path, index=False)

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

    def test_materializer_metadata_rejects_direct_utc_raw_time_assumption(self) -> None:
        self.assertEqual(
            self.module.RAW_TIME_AXIS_POLICY,
            "raw_broker_clock_bar_close_key_not_direct_utc",
        )
        self.assertEqual(
            self.counts["session_time_policy_status"],
            "closed_by_broker_session_calendar_mapper_v1",
        )

    def test_session_features_use_broker_clock_mapper(self) -> None:
        row = self.row_at("2022-09-01T16:40:00Z")

        self.assertEqual(pd.Timestamp(row["timestamp_event_utc"]), pd.Timestamp("2022-09-01T13:40:00Z"))
        self.assertEqual(pd.Timestamp(row["timestamp_ny"]), pd.Timestamp("2022-09-01T09:40:00-0400"))
        self.assertEqual(float(row["minutes_from_cash_open"]), 10.0)
        self.assertEqual(float(row["is_us_cash_open"]), 1.0)

    def test_supertrend_seed_rule_defaults_to_downtrend_until_updated_band_exists(self) -> None:
        high = pd.Series([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], dtype="float64")
        low = pd.Series([9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], dtype="float64")
        close = pd.Series([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], dtype="float64")

        state = self.module.compute_supertrend_state(high, low, close, 10, 3.0)

        self.assertTrue(pd.isna(state.iloc[8]))
        self.assertEqual(float(state.iloc[9]), -1.0)
        self.assertEqual(float(state.iloc[10]), -1.0)

    def test_gap_stock_returns_follow_previous_available_bar_before_merge(self) -> None:
        row = self.row_at("2022-09-01T16:40:00Z")
        weights = self.module.load_weights().set_index("month").loc["2022-09"]

        self.assertTrue(bool(row["valid_row"]))
        self.assertEqual(
            self.previous_available_timestamp("NVDA", "2022-09-01T16:40:00Z"),
            pd.Timestamp("2022-08-31T22:55:00Z"),
        )

        expected_nvda = self.direct_stock_value("NVDA", "2022-09-01T16:40:00Z", field="log_return_1")
        expected_aapl = self.direct_stock_value("AAPL", "2022-09-01T16:40:00Z", field="simple_return_1")
        expected_msft = self.direct_stock_value("MSFT", "2022-09-01T16:40:00Z", field="simple_return_1")

        basket_symbols = ("AAPL", "AMZN", "AMD", "GOOGL.xnas", "META", "MSFT", "NVDA", "TSLA")
        basket_returns = [
            self.direct_stock_value(symbol, "2022-09-01T16:40:00Z", field="simple_return_1")
            for symbol in basket_symbols
        ]
        expected_mega8 = float(sum(basket_returns) / len(basket_returns))
        expected_top3 = (
            float(weights["msft_xnas_weight"]) * expected_msft
            + float(weights["nvda_xnas_weight"]) * (np.exp(expected_nvda) - 1.0)
            + float(weights["aapl_xnas_weight"]) * expected_aapl
        )
        expected_us100_simple = float(row["close_prev_close_ratio"]) - 1.0

        self.assertAlmostEqual(float(row["nvda_xnas_log_return_1"]), expected_nvda, places=12)
        self.assertAlmostEqual(float(row["mega8_equal_return_1"]), expected_mega8, places=12)
        self.assertAlmostEqual(float(row["top3_weighted_return_1"]), expected_top3, places=12)
        self.assertAlmostEqual(
            float(row["us100_minus_mega8_equal_return_1"]),
            expected_us100_simple - expected_mega8,
            places=12,
        )
        self.assertAlmostEqual(
            float(row["us100_minus_top3_weighted_return_1"]),
            expected_us100_simple - expected_top3,
            places=12,
        )

    def test_build_feature_frame_accepts_custom_weight_source(self) -> None:
        baseline_row = self.row_at("2022-09-01T16:40:00Z")
        with tempfile.TemporaryDirectory() as temp_dir:
            weights_path = Path(temp_dir) / "real_weights.csv"
            self.write_weights_csv(
                weights_path,
                overrides={
                    "2022-09": {
                        "msft_xnas_weight": 0.6,
                        "nvda_xnas_weight": 0.2,
                        "aapl_xnas_weight": 0.2,
                    }
                },
            )

            custom_frame, custom_counts = self.module.build_feature_frame(
                RAW_ROOT,
                weights_path=weights_path,
                weights_version_label="test_real_weights_v1",
            )
            custom_row = custom_frame.loc[
                custom_frame["timestamp"] == pd.Timestamp("2022-09-01T16:40:00Z")
            ].iloc[0]

            self.assertEqual(custom_counts["weights_version"], "test_real_weights_v1")
            self.assertEqual(self.module.build_feature_frame(RAW_ROOT)[1]["weights_version"], self.module.WEIGHTS_VERSION)
            self.assertNotAlmostEqual(
                float(custom_row["top3_weighted_return_1"]),
                float(baseline_row["top3_weighted_return_1"]),
                places=12,
            )
            self.assertNotAlmostEqual(
                float(custom_row["us100_minus_top3_weighted_return_1"]),
                float(baseline_row["us100_minus_top3_weighted_return_1"]),
                places=12,
            )
