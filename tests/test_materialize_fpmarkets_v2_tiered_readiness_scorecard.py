from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    REPO_ROOT / "foundation" / "pipelines" / "materialize_fpmarkets_v2_tiered_readiness_scorecard.py"
)
DATASET_MODULE_PATH = REPO_ROOT / "foundation" / "pipelines" / "materialize_fpmarkets_v2_dataset.py"
RAW_ROOT = REPO_ROOT / "data" / "raw" / "mt5_bars" / "m5"

_CACHE: dict[str, object] = {}


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_scorecard_module():
    return load_module("materialize_fpmarkets_v2_tiered_readiness_scorecard", MODULE_PATH)


def load_dataset_module():
    return load_module("materialize_fpmarkets_v2_dataset_for_scorecard_tests", DATASET_MODULE_PATH)


def get_cached_scorecard():
    if "scorecard" not in _CACHE:
        dataset_module = load_dataset_module()
        scorecard_module = load_scorecard_module()
        frame, _ = dataset_module.build_feature_frame(RAW_ROOT)
        row_labels = scorecard_module.build_scorecard_frame(frame)
        summary = scorecard_module.build_summary_payload(
            row_labels,
            row_labels_path="stages/06_tiered_readiness_exploration/02_runs/tiered_readiness_scorecard_0001/"
            "readiness_row_labels_fpmarkets_v2_tiered_readiness_0001.parquet",
        )
        _CACHE["dataset_module"] = dataset_module
        _CACHE["scorecard_module"] = scorecard_module
        _CACHE["frame"] = frame
        _CACHE["row_labels"] = row_labels
        _CACHE["summary"] = summary
    return _CACHE


class ReadinessRuleUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_scorecard_module()

    def test_canonical_tier_rule_matches_fixed_boundary(self) -> None:
        cases = (
            (
                "group1_failure",
                dict(
                    g1_contract_base_complete=False,
                    g2_session_semantics_complete=True,
                    g3_macro_proxy_complete=True,
                    g4_leader_equity_complete=True,
                    g5_breadth_extension_complete=True,
                ),
                "tier_c",
            ),
            (
                "all_external_groups_complete",
                dict(
                    g1_contract_base_complete=True,
                    g2_session_semantics_complete=True,
                    g3_macro_proxy_complete=True,
                    g4_leader_equity_complete=True,
                    g5_breadth_extension_complete=True,
                ),
                "tier_a",
            ),
            (
                "exactly_one_external_group_complete",
                dict(
                    g1_contract_base_complete=True,
                    g2_session_semantics_complete=True,
                    g3_macro_proxy_complete=True,
                    g4_leader_equity_complete=False,
                    g5_breadth_extension_complete=False,
                ),
                "tier_b",
            ),
            (
                "no_external_groups_complete",
                dict(
                    g1_contract_base_complete=True,
                    g2_session_semantics_complete=True,
                    g3_macro_proxy_complete=False,
                    g4_leader_equity_complete=False,
                    g5_breadth_extension_complete=False,
                ),
                "tier_c",
            ),
        )

        for name, kwargs, expected in cases:
            with self.subTest(case=name):
                self.assertEqual(self.module.classify_tier_flags(**kwargs), expected)

    def test_reporting_lane_is_null_for_tier_c(self) -> None:
        self.assertIsNone(self.module.reporting_lane_for_tier("tier_c"))

    def test_pipe_serialization_is_sorted_and_stable(self) -> None:
        rendered = self.module.serialize_pipe_tokens(
            ["META.xnas", "VIX", "AAPL.xnas", "VIX"],
            self.module.SYMBOL_TOKEN_ORDER,
        )
        self.assertEqual(rendered, "VIX|AAPL.xnas|META.xnas")


class ScorecardIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cache = get_cached_scorecard()
        cls.module = cache["scorecard_module"]
        cls.row_labels = cache["row_labels"]
        cls.summary = cache["summary"]

    def test_real_data_counts_match_expected_shared_and_practical_windows(self) -> None:
        shared_counts = self.summary["shared_window"]["tier_counts"]
        practical_counts = self.summary["practical_window"]["tier_counts"]

        self.assertEqual(
            shared_counts,
            {
                "tier_a": 56988,
                "tier_b": 88303,
                "tier_c": 116053,
            },
        )
        self.assertEqual(
            practical_counts,
            {
                "tier_a": 55457,
                "tier_b": 86192,
                "tier_c": 113352,
            },
        )

    def test_output_writes_expected_columns_and_review_phrases(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            output_root = temp_root / "scorecard"
            report_path = temp_root / "report.md"
            outputs = self.module.write_outputs(
                output_root=output_root,
                report_path=report_path,
                row_labels=self.row_labels,
                reviewed_on="2026-04-21",
            )

            parquet_frame = pd.read_parquet(outputs["row_labels_path"])
            self.assertEqual(list(parquet_frame.columns), self.module.ROW_LABEL_COLUMNS)

            summary_payload = json.loads(Path(outputs["summary_path"]).read_text(encoding="utf-8"))
            self.assertIn("shared_window", summary_payload)
            self.assertIn("practical_window", summary_payload)

            report_text = Path(outputs["report_path"]).read_text(encoding="utf-8")
            self.assertIn("strict `Tier A` (엄격 `Tier A`) remains the only current runtime rule", report_text)
            self.assertIn("`Tier B` (부분 준비도 `Tier B`) is exploration-only", report_text)
            self.assertIn("no operating promotion (운영 승격) is claimed", report_text)

