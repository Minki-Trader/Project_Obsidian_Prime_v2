from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "foundation" / "parity" / "render_fpmarkets_v2_runtime_parity_report.py"


def load_render_module():
    spec = importlib.util.spec_from_file_location("render_fpmarkets_v2_runtime_parity_report", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ClassifyScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_render_module()

    def build_comparison(self, *, exact_parity: bool, tolerance_parity: bool, traceable: bool) -> dict:
        return {
            "aggregate_results": {
                "exact_parity": exact_parity,
                "tolerance_parity": tolerance_parity,
            },
            "matching": {
                "missing_fixture_ids": [],
                "unexpected_record_count": 0,
            },
            "identity": {
                "machine_readable_identity_trace": {
                    "traceable": traceable,
                }
            },
        }

    def test_classify_scope_prefers_exact_match_before_tolerance_closure(self) -> None:
        cases = (
            (
                "exact_match_with_traceable_identity",
                self.build_comparison(exact_parity=True, tolerance_parity=True, traceable=True),
                "first_evaluated_pack_exact_match",
            ),
            (
                "tolerance_closure_with_traceable_identity",
                self.build_comparison(exact_parity=False, tolerance_parity=True, traceable=True),
                "first_evaluated_pack_tolerance_closed_identity_trace_materialized_exact_open",
            ),
        )

        for name, comparison, expected in cases:
            with self.subTest(case=name):
                self.assertEqual(self.module.classify_scope(comparison), expected)
