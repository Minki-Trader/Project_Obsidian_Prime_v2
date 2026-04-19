from __future__ import annotations

import importlib.util
import json
import tempfile
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

    def test_render_report_uses_stage05_specific_wording_and_bucket_counts(self) -> None:
        comparison = {
            "aggregate_results": {
                "exact_parity": False,
                "tolerance_parity": True,
                "max_abs_diff": 0.0,
                "zero_shift_share_mean": 1.0,
            },
            "matching": {
                "missing_fixture_ids": [],
                "unexpected_record_count": 0,
            },
            "identity": {
                "expected": {
                    "dataset_id": "dataset_fpmarkets_v2_us100_m5_20220801_20260413_freeze01",
                    "fixture_set_id": "fixture_fpmarkets_v2_runtime_broader_0001",
                    "bundle_id": "bundle_fpmarkets_v2_runtime_broader_0001",
                    "report_id": "report_fpmarkets_v2_runtime_broader_parity_0001",
                    "runtime_id": "runtime_fpmarkets_v2_mt5_snapshot_broader_0001",
                },
                "machine_readable_identity_trace": {
                    "request_consistent": True,
                    "mt5_fields_present": True,
                    "mt5_values_match": True,
                    "traceable": True,
                },
            },
            "fixtures": {
                "fix_regular_cash_session_0001": {
                    "status": "matched",
                    "actual_row_ready": True,
                    "skip_reason": "",
                    "feature_comparison": {"top_abs_diffs": []},
                },
                "fix_negative_cash_open_missing_equities_0001": {
                    "status": "matched",
                    "actual_row_ready": False,
                    "skip_reason": "EXTERNAL_TIMESTAMP_MISMATCH_AAPL.xnas",
                    "feature_comparison": {"top_abs_diffs": []},
                },
            },
            "warnings": [],
        }
        python_snapshot = {
            "parser_version": "fpmarkets_v2_stage01_materializer_v1",
            "feature_contract_version": "docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-16",
            "feature_order_hash": "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2",
            "fixtures": {
                "fix_regular_cash_session_0001": {
                    "fixture_id": "fix_regular_cash_session_0001",
                    "timestamp_utc": "2022-09-02T17:00:00Z",
                    "timestamp_america_new_york": "2022-09-02T13:00:00-04:00",
                    "valid_row": True,
                    "selection_stratum": "regular_cash_session",
                    "selection_bucket": "regular_cash_session",
                },
                "fix_negative_cash_open_missing_equities_0001": {
                    "fixture_id": "fix_negative_cash_open_missing_equities_0001",
                    "timestamp_utc": "2023-01-03T14:35:00Z",
                    "timestamp_america_new_york": "2023-01-03T09:35:00-05:00",
                    "valid_row": False,
                    "selection_stratum": "cash_open_missing_equities",
                    "selection_bucket": "negative_cash_open_missing_equities",
                },
            },
        }
        mt5_request = {
            "runtime_contract_version": "docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-16",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            fixture_bindings_path = temp_root / "fixture_bindings.json"
            python_snapshot_path = temp_root / "python_snapshot.json"
            mt5_request_path = temp_root / "mt5_request.json"
            mt5_snapshot_path = temp_root / "mt5_snapshot.jsonl"

            fixture_bindings_path.write_text("{}", encoding="utf-8")
            python_snapshot_path.write_text(json.dumps(python_snapshot), encoding="utf-8")
            mt5_request_path.write_text(json.dumps(mt5_request), encoding="utf-8")
            mt5_snapshot_path.write_text('{"fixture_id":"fix_regular_cash_session_0001"}\n', encoding="utf-8")

            rendered = self.module.render_report(
                comparison=comparison,
                python_snapshot=python_snapshot,
                mt5_request=mt5_request,
                stage_name="05_exploration_kernel_freeze",
                fixture_bindings_path=fixture_bindings_path,
                python_snapshot_path=python_snapshot_path,
                mt5_request_path=mt5_request_path,
                mt5_snapshot_path=mt5_snapshot_path,
                reviewed_on="2026-04-19",
            )

        self.assertIn("- stage: `05_exploration_kernel_freeze`", rendered)
        self.assertIn(
            "- fixture_strata: `cash_open_missing_equities=1|regular_cash_session=1`",
            rendered,
        )
        self.assertIn(
            "- fixture_buckets: `negative_cash_open_missing_equities=1|regular_cash_session=1`",
            rendered,
        )
        self.assertIn("matched_non_ready=1/1", rendered)
        self.assertIn("keep Stage 05 open", rendered)
        self.assertIn("no separate broader-sample parity closure read", rendered)
        self.assertNotIn("fix_negative_required_missing_0001", rendered)
        self.assertNotIn("Stage 03", rendered)
