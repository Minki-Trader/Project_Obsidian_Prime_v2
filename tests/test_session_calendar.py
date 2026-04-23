from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "features" / "session_calendar.py"


def load_session_calendar_module():
    module_name = "session_calendar"
    spec = importlib.util.spec_from_file_location(module_name, MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class SessionCalendarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_session_calendar_module()

    def test_broker_clock_key_converts_to_cash_open_event_utc_across_dst(self) -> None:
        raw_keys = pd.Series(
            pd.to_datetime(
                [
                    "2022-08-01T16:35:00Z",
                    "2023-01-03T16:35:00Z",
                ],
                utc=True,
            )
        )

        converted = self.module.broker_clock_key_to_event_utc(raw_keys)

        self.assertEqual(converted.iloc[0], pd.Timestamp("2022-08-01T13:35:00Z"))
        self.assertEqual(converted.iloc[1], pd.Timestamp("2023-01-03T14:35:00Z"))

    def test_us_cash_session_features_use_event_time_not_raw_utc(self) -> None:
        frame = pd.DataFrame(
            {
                "timestamp": pd.to_datetime(
                    [
                        "2023-01-03T23:00:00Z",
                        "2023-01-04T16:35:00Z",
                        "2023-01-04T23:00:00Z",
                    ],
                    utc=True,
                ),
                "open": [99.0, 110.0, 120.0],
                "close": [100.0, 111.0, 121.0],
            }
        )
        frame = self.module.attach_event_time_columns(frame)

        features = self.module.compute_us_cash_session_features(frame)

        self.assertEqual(features["timestamp_ny"].iloc[1], pd.Timestamp("2023-01-04T09:35:00-0500"))
        self.assertEqual(float(features["minutes_from_cash_open"].iloc[1]), 5.0)
        self.assertEqual(float(features["is_us_cash_open"].iloc[1]), 1.0)
        self.assertAlmostEqual(float(features["overnight_return"].iloc[1]), 0.10, places=12)


if __name__ == "__main__":
    unittest.main()
