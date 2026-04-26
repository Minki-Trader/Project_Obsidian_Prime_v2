from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


REPO_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_MODULE_PATH = REPO_ROOT / "foundation" / "pipelines" / "run_stage10_logreg_mt5_scout.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module spec from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Stage10LogregMt5ScoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module("run_stage10_logreg_mt5_scout", PIPELINE_MODULE_PATH)

    def test_threshold_rule_uses_threshold_and_margin(self) -> None:
        rule = self.module.ThresholdRule(
            threshold_id="unit",
            short_threshold=0.50,
            long_threshold=0.50,
            min_margin=0.05,
        )
        probabilities = np.array(
            [
                [0.70, 0.20, 0.10],
                [0.10, 0.20, 0.70],
                [0.49, 0.02, 0.49],
                [0.52, 0.02, 0.49],
                [0.10, 0.60, 0.30],
            ],
            dtype="float64",
        )

        decisions = self.module.apply_threshold_rule(probabilities, rule)

        self.assertEqual(
            decisions["decision_label"].tolist(),
            ["short", "long", "no_trade", "no_trade", "no_trade"],
        )
        self.assertEqual(decisions.loc[0, "decision_label_class"], 0)
        self.assertEqual(decisions.loc[1, "decision_label_class"], 2)

    def test_paired_tier_records_include_separate_and_combined_views(self) -> None:
        predictions = pd.DataFrame(
            {
                "tier_label": ["Tier A", "Tier A", "Tier B", "Tier B"],
                "decision_label": ["short", "no_trade", "long", "no_trade"],
                "p_short": [0.6, 0.3, 0.2, 0.3],
                "p_flat": [0.2, 0.4, 0.2, 0.4],
                "p_long": [0.2, 0.3, 0.6, 0.3],
            }
        )

        views = self.module.build_tier_prediction_views(predictions)
        records = self.module.build_paired_tier_records(
            views,
            run_id="run01A_unit",
            stage_id=self.module.STAGE_ID,
            base_path=Path("stage10/unit"),
        )

        self.assertEqual(set(views), {"tier_a_separate", "tier_b_separate", "tier_ab_combined"})
        self.assertEqual(len(views["tier_a_separate"]), 2)
        self.assertEqual(len(views["tier_b_separate"]), 2)
        self.assertEqual(len(views["tier_ab_combined"]), 4)
        self.assertEqual([record["record_view"] for record in records], list(views.keys()))
        self.assertEqual([record["status"] for record in records], ["completed_payload"] * 3)
        self.assertEqual(records[2]["tier_scope"], "Tier A+B")
        self.assertEqual(records[2]["metrics"]["signal_count"], 2)

    def test_onnx_parity_on_tiny_synthetic_model(self) -> None:
        X = np.array(
            [
                [-2.0, -1.0],
                [-1.5, -0.4],
                [-0.2, 0.0],
                [0.0, 0.2],
                [1.2, 0.9],
                [1.8, 1.5],
                [-2.2, -0.8],
                [0.2, -0.1],
                [2.0, 1.2],
            ],
            dtype="float32",
        )
        y = np.array([0, 0, 1, 1, 2, 2, 0, 1, 2], dtype="int64")
        model = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(max_iter=500, random_state=3),
                ),
            ]
        ).fit(X, y)

        with tempfile.TemporaryDirectory() as temp_dir:
            onnx_path = Path(temp_dir) / "tiny_logreg.onnx"
            export = self.module.export_sklearn_to_onnx_zipmap_disabled(
                model,
                onnx_path,
                feature_count=X.shape[1],
            )
            parity = self.module.check_onnxruntime_probability_parity(
                model,
                onnx_path,
                X,
                tolerance=1e-5,
            )
            self.assertTrue(onnx_path.exists())

        self.assertTrue(export["zipmap_disabled"])
        self.assertTrue(parity["passed"], parity)
        self.assertLessEqual(parity["max_abs_diff"], 1e-5)

    def test_mt5_report_parser_extracts_required_kpis(self) -> None:
        html = """
        <html><body><table>
        <tr><td>Total Net Profit:</td><td>12.50</td><td>Balance Drawdown Maximal:</td><td>5.00 (1.00%)</td><td>Equity Drawdown Maximal:</td><td>6.25 (1.25%)</td></tr>
        <tr><td>Gross Profit:</td><td>22.50</td><td>Gross Loss:</td><td>-10.00</td></tr>
        <tr><td>Profit Factor:</td><td>2.25</td><td>Expected Payoff:</td><td>1.25</td></tr>
        <tr><td>Recovery Factor:</td><td>2.00</td></tr>
        <tr><td>Total Trades:</td><td>10</td><td>Short Trades (won %):</td><td>4 (50.00%)</td><td>Long Trades (won %):</td><td>6 (66.67%)</td></tr>
        <tr><td>Total Deals:</td><td>20</td><td>Profit Trades (% of total):</td><td>6 (60.00%)</td><td>Loss Trades (% of total):</td><td>4 (40.00%)</td></tr>
        </table></body></html>
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.htm"
            report_path.write_text(html, encoding="utf-16")
            metrics = self.module.extract_mt5_strategy_report_metrics(report_path)

        self.assertEqual(metrics["status"], "completed")
        self.assertEqual(metrics["net_profit"], 12.5)
        self.assertEqual(metrics["profit_factor"], 2.25)
        self.assertEqual(metrics["expectancy"], 1.25)
        self.assertEqual(metrics["trade_count"], 10)
        self.assertEqual(metrics["win_rate_percent"], 60.0)
        self.assertEqual(metrics["max_drawdown_amount"], 6.25)
        self.assertEqual(metrics["recovery_factor"], 2.0)

    def test_materialize_routed_mt5_attempt_sets_primary_and_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            attempt = self.module.materialize_mt5_routed_attempt_files(
                run_output_root=root,
                split_name="validation_is",
                primary_onnx_path=root / "tier_a.onnx",
                primary_feature_matrix_path=root / "tier_a_features.csv",
                primary_feature_count=58,
                primary_feature_order_hash="hash_a",
                fallback_onnx_path=root / "tier_b.onnx",
                fallback_feature_matrix_path=root / "tier_b_features.csv",
                fallback_feature_count=56,
                fallback_feature_order_hash="hash_b",
                rule=self.module.ThresholdRule(
                    threshold_id="unit",
                    short_threshold=0.6,
                    long_threshold=0.4,
                    min_margin=0.0,
                ),
                from_date="2025.01.01",
                to_date="2025.10.01",
            )
            set_text = Path(attempt["set"]["path"]).read_text(encoding="utf-8")

        self.assertEqual(attempt["routing_mode"], "tier_a_primary_tier_b_fallback")
        self.assertIn("InpFeatureCount=58", set_text)
        self.assertIn("InpFallbackEnabled=true", set_text)
        self.assertIn("InpFallbackFeatureCount=56", set_text)
        self.assertIn("InpFallbackFeatureOrderHash=hash_b", set_text)

    def test_routed_mt5_kpi_records_are_not_synthetic_sum(self) -> None:
        result = {
            "status": "completed",
            "tier": self.module.TIER_AB,
            "split": "validation_is",
            "routing_mode": "tier_a_primary_tier_b_fallback",
            "runtime_outputs": {
                "last_summary": {
                    "order_attempt_count": 5,
                    "order_fill_count": 4,
                    "feature_skip_count": 7,
                    "feature_ready_count": 12,
                    "model_ok_count": 12,
                    "model_fail_count": 0,
                    "tier_a_used_count": 10,
                    "tier_b_fallback_used_count": 2,
                    "no_tier_count": 7,
                    "tier_a_long_count": 3,
                    "tier_a_short_count": 2,
                    "tier_a_flat_count": 5,
                    "tier_a_order_attempt_count": 4,
                    "tier_a_order_fill_count": 3,
                    "tier_b_fallback_long_count": 1,
                    "tier_b_fallback_short_count": 0,
                    "tier_b_fallback_flat_count": 1,
                    "tier_b_fallback_order_attempt_count": 1,
                    "tier_b_fallback_order_fill_count": 1,
                }
            },
            "strategy_tester_report": {
                "metrics": {
                    "status": "completed",
                    "net_profit": 12.0,
                    "profit_factor": 1.2,
                    "expectancy": 0.5,
                    "trade_count": 24,
                    "win_rate_percent": 55.0,
                    "max_drawdown_amount": 8.0,
                    "max_drawdown_percent": 1.6,
                    "recovery_factor": 1.5,
                }
            },
        }

        records = self.module.build_mt5_kpi_records([result])

        self.assertEqual(
            [record["record_view"] for record in records],
            [
                "mt5_routed_tier_a_used_validation_is",
                "mt5_routed_tier_b_fallback_used_validation_is",
                "mt5_routed_total_validation_is",
            ],
        )
        self.assertEqual(records[0]["metrics"]["route_bar_count"], 10)
        self.assertEqual(records[1]["metrics"]["route_bar_count"], 2)
        self.assertEqual(records[1]["metrics"]["profit_attribution"], "not_separable_from_single_routed_account_path")
        self.assertEqual(records[2]["metrics"]["aggregation"], "actual_routed_tester_run")
        self.assertNotEqual(records[2]["metrics"].get("aggregation"), "synthetic_sum_of_separate_tier_tester_runs")

    def test_tier_b_partial_context_subtypes_are_explicit(self) -> None:
        module = self.module
        rows = []
        group_names = list(module.TIER_B_CONTEXT_GROUPS)
        cases = [
            ((), "B_full_context_outside_tier_a_scope", "none", "macro|constituent|basket"),
            (("macro",), "B_macro_missing", "macro", "constituent|basket"),
            (("constituent",), "B_constituent_missing", "constituent", "macro|basket"),
            (("basket",), "B_basket_missing", "basket", "macro|constituent"),
            (tuple(group_names), "B_core_only", "macro|constituent|basket", "core_only"),
            (("macro", "basket"), "B_mixed_partial_context", "macro|basket", "constituent"),
        ]
        for missing_groups, _expected_subtype, _missing_mask, _available_mask in cases:
            row = {name: 1.0 for names in module.TIER_B_CONTEXT_GROUPS.values() for name in names}
            for group in missing_groups:
                for feature_name in module.TIER_B_CONTEXT_GROUPS[group]:
                    row[feature_name] = np.nan
            rows.append(row)

        classified = module.classify_tier_b_partial_context(pd.DataFrame(rows))

        self.assertEqual(classified["partial_context_subtype"].tolist(), [case[1] for case in cases])
        self.assertEqual(classified["missing_feature_group_mask"].tolist(), [case[2] for case in cases])
        self.assertEqual(classified["available_feature_group_mask"].tolist(), [case[3] for case in cases])

    def test_mt5_kpi_records_are_enriched_with_route_coverage(self) -> None:
        records = [
            {
                "record_view": "mt5_routed_tier_b_fallback_used_validation_is",
                "tier_scope": self.module.TIER_B,
                "split": "validation_is",
                "route_role": "fallback_used",
                "metrics": {},
            },
            {
                "record_view": "mt5_routed_total_oos",
                "tier_scope": self.module.TIER_AB,
                "split": "oos",
                "route_role": "routed_total",
                "metrics": {},
            },
        ]
        route_coverage = {
            "by_split": {
                "validation": {"tier_a_primary_rows": 3, "tier_b_fallback_rows": 2, "routed_labelable_rows": 5},
                "oos": {"tier_a_primary_rows": 7, "tier_b_fallback_rows": 1, "routed_labelable_rows": 8},
            },
            "tier_b_fallback_by_split_subtype": {
                "validation": {"B_macro_missing": 2},
                "oos": {"B_core_only": 1},
            },
            "no_tier_by_split": {"validation": 1, "oos": 4},
        }

        enriched = self.module.enrich_mt5_kpi_records_with_route_coverage(records, route_coverage)

        self.assertEqual(enriched[0]["metrics"]["tier_b_fallback_labelable_rows"], 2)
        self.assertEqual(enriched[0]["metrics"]["partial_context_subtype_counts"], {"B_macro_missing": 2})
        self.assertEqual(enriched[0]["metrics"]["no_tier_labelable_rows"], 1)
        self.assertEqual(enriched[1]["metrics"]["tier_a_primary_labelable_rows"], 7)
        self.assertEqual(enriched[1]["metrics"]["partial_context_subtype_counts"], {"B_core_only": 1})

    def test_path_exists_uses_long_path_adapter(self) -> None:
        temp_dir = tempfile.mkdtemp()
        root = Path(temp_dir)
        try:
            long_dir = root
            for index in range(6):
                long_dir = long_dir / f"segment_{index:02d}_{'x' * 32}"
            long_path = long_dir / "stage10_long_path_probe.txt"

            self.module._io_path(long_path.parent).mkdir(parents=True, exist_ok=True)
            self.module._io_path(long_path).write_text("ok", encoding="utf-8")

            self.assertTrue(self.module._path_exists(long_path))
        finally:
            shutil.rmtree(self.module._io_path(root), ignore_errors=True)

    def test_lf_normalized_hash_is_stable_across_crlf(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            lf_path = root / "ledger_lf.csv"
            crlf_path = root / "ledger_crlf.csv"
            lf_path.write_bytes(b"a,b\n1,2\n")
            crlf_path.write_bytes(b"a,b\r\n1,2\r\n")

            self.assertEqual(
                self.module.sha256_file_lf_normalized(lf_path),
                self.module.sha256_file_lf_normalized(crlf_path),
            )


if __name__ == "__main__":
    unittest.main()
