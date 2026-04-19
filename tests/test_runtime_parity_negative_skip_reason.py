from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
COMPARE_MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "compare_fpmarkets_v2_runtime_parity.py"
RENDER_MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "render_fpmarkets_v2_runtime_parity_report.py"


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NegativeSkipReasonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.compare = load_module(COMPARE_MODULE_PATH, "compare_fpmarkets_v2_runtime_parity")
        cls.render = load_module(RENDER_MODULE_PATH, "render_fpmarkets_v2_runtime_parity_report")

    def test_external_alignment_negative_rows_only_accept_external_skip_reason(self) -> None:
        expected_fixture = {
            "valid_row": False,
            "invalid_reason_flags": {
                "external_alignment_missing": True,
            },
        }

        self.assertTrue(
            self.compare.negative_fixture_skip_match(
                expected_fixture,
                {"skip_reason": "EXTERNAL_TIMESTAMP_MISMATCH_VIX"},
            )
        )
        self.assertFalse(
            self.compare.negative_fixture_skip_match(
                expected_fixture,
                {"skip_reason": "SESSION_CASH_OPEN_NOT_FOUND"},
            )
        )

    def test_negative_fixture_summary_excludes_mismatched_skip_reason_rows(self) -> None:
        python_snapshot = {
            "fixtures": {
                "fix_negative_cash_open_missing_equities_0001": {
                    "valid_row": False,
                },
                "fix_negative_off_hours_pre_open_0001": {
                    "valid_row": False,
                },
                "fix_negative_off_hours_pre_open_0002": {
                    "valid_row": False,
                },
            }
        }
        comparison = {
            "fixtures": {
                "fix_negative_cash_open_missing_equities_0001": {
                    "status": "matched",
                    "actual_row_ready": False,
                    "skip_reason": "EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas",
                    "negative_skip_reason_match": True,
                },
                "fix_negative_off_hours_pre_open_0001": {
                    "status": "matched",
                    "actual_row_ready": False,
                    "skip_reason": "SESSION_CASH_OPEN_NOT_FOUND",
                    "negative_skip_reason_match": False,
                },
                "fix_negative_off_hours_pre_open_0002": {
                    "status": "matched",
                    "actual_row_ready": False,
                    "skip_reason": "SESSION_CASH_OPEN_NOT_FOUND",
                    "negative_skip_reason_match": False,
                },
            }
        }

        summary = self.render.negative_fixture_summary(python_snapshot, comparison)

        self.assertIn("matched_non_ready=1/3", summary)
        self.assertIn("skip_reasons=EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas=1", summary)
        self.assertIn(
            "mismatched_skip_reason=fix_negative_off_hours_pre_open_0001,fix_negative_off_hours_pre_open_0002",
            summary,
        )
