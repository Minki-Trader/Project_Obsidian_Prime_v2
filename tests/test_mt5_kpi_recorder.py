from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from foundation.control_plane.mt5_kpi_recorder import write_mt5_kpi_recording_packet


ROOT = Path(__file__).resolve().parents[1]


class Mt5KpiRecorderTests(unittest.TestCase):
    def test_records_normalized_kpi_from_mt5_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_template(root)
            run_root = root / "stages/unit_stage/02_runs/unit_run"
            report_path = run_root / "mt5/reports/unit_report.htm"
            report_path.parent.mkdir(parents=True)
            report_path.write_text(_report_html(gross_loss="-10.00", profit_factor="2.25"), encoding="utf-16")
            kpi_payload = {
                "run_id": "unit_run",
                "stage_id": "unit_stage",
                "python_metrics": {
                    "validation": {
                        "signal_count": 4,
                        "short_count": 1,
                        "long_count": 3,
                        "signal_coverage": 0.4,
                        "directional_hit_rate": 0.75,
                    }
                },
                "mt5_records": [
                    {
                        "record_view": "mt5_routed_total_validation_is",
                        "tier_scope": "Tier A+B",
                        "split": "validation_is",
                        "route_role": "routed_total",
                        "metrics": {
                            "order_attempt_count": 5,
                            "fill_count": 4,
                            "fill_rate": 0.8,
                            "reject_count": 1,
                            "skip_count": 7,
                            "feature_ready_count": 10,
                            "model_fail_count": 2,
                        },
                        "report": {"html_report": {"path": report_path.as_posix()}},
                    }
                ],
            }
            (run_root / "kpi_record.json").write_text(json.dumps(kpi_payload), encoding="utf-8")
            _seed_inventory(root, "unit_run", "unit_stage", "stages/unit_stage/02_runs/unit_run")

            packet = write_mt5_kpi_recording_packet(root, created_at_utc="2026-04-29T00:00:00Z")

            self.assertEqual(packet["summary"]["normalized_records_written"], 1)
            record_path = root / "docs/agent_control/packets/kpi_rebuild_mt5_recording_v1/normalized_kpi_records.jsonl"
            record = json.loads(record_path.read_text(encoding="utf-8").splitlines()[0])

            self.assertEqual(record["row_grain"]["split"]["value"], "validation")
            self.assertEqual(record["mt5_trading_headline"]["net_profit"]["value"], 12.5)
            self.assertEqual(record["mt5_trading_headline"]["profit_factor"]["authority"], "mt5_strategy_tester_report")
            self.assertEqual(record["risk"]["max_drawdown_amount"]["value"], 6.25)
            self.assertEqual(record["execution"]["order_attempt_count"]["value"], 5)
            self.assertEqual(record["signal_model"]["directional_hit_rate"]["value"], 0.75)
            self.assertEqual(record["source_evidence"]["mt5_report_parse_status"], "completed")
            self.assertEqual(record["source_evidence"]["mt5_report_missing_required_metrics"], [])
            self.assertEqual(record["source_evidence"]["mt5_report_source_encoding"], "utf-16")
            self.assertEqual(record["source_evidence"]["report_identity_source"], "kpi_record_mt5_records")

    def test_profit_factor_denominator_zero_gets_n_a_reason(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_template(root)
            run_root = root / "stages/unit_stage/02_runs/unit_run"
            report_path = run_root / "mt5/reports/unit_report.htm"
            report_path.parent.mkdir(parents=True)
            report_path.write_text(_report_html(gross_loss="0.00", profit_factor="0.00"), encoding="utf-16")
            (run_root / "kpi_record.json").write_text(
                json.dumps(
                    {
                        "run_id": "unit_run",
                        "stage_id": "unit_stage",
                        "mt5_records": [
                            {
                                "record_view": "mt5_tier_a_only_oos",
                                "tier_scope": "Tier A",
                                "split": "oos",
                                "route_role": "tier_only_total",
                                "metrics": {},
                                "report": {"html_report": {"path": report_path.as_posix()}},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            _seed_inventory(root, "unit_run", "unit_stage", "stages/unit_stage/02_runs/unit_run")

            write_mt5_kpi_recording_packet(root, created_at_utc="2026-04-29T00:00:00Z")

            record_path = root / "docs/agent_control/packets/kpi_rebuild_mt5_recording_v1/normalized_kpi_records.jsonl"
            record = json.loads(record_path.read_text(encoding="utf-8").splitlines()[0])
            profit_factor = record["mt5_trading_headline"]["profit_factor"]

            self.assertIsNone(profit_factor["value"])
            self.assertEqual(profit_factor["n/a_reason"], "gross_loss_is_zero")
            self.assertEqual(profit_factor["raw_mt5_display"], 0.0)

    def test_reads_legacy_nested_mt5_kpi_records_and_preserves_component_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_template(root)
            run_root = root / "stages/unit_stage/02_runs/unit_run"
            report_path = run_root / "mt5/reports/unit_report.htm"
            report_path.parent.mkdir(parents=True)
            report_path.write_text(_report_html(gross_loss="-10.00", profit_factor="2.25"), encoding="utf-16")
            (run_root / "kpi_record.json").write_text(
                json.dumps(
                    {
                        "run_id": "unit_run",
                        "stage_id": "unit_stage",
                        "mt5": {
                            "kpi_records": [
                                {
                                    "record_view": "mt5_routed_tier_a_used_validation_is",
                                    "tier_scope": "Tier A",
                                    "split": "validation_is",
                                    "route_role": "primary_used",
                                    "metrics": {
                                        "aggregation": "actual_routed_component",
                                        "profit_attribution": "not_separable_from_single_routed_account_path",
                                        "net_profit": None,
                                        "trade_count": None,
                                        "order_attempt_count": 3,
                                        "fill_count": 2,
                                    },
                                    "report": {
                                        "aggregation": "actual_routed_component",
                                        "source_report": {"html_report": {"path": report_path.as_posix()}},
                                    },
                                }
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            _seed_inventory(root, "unit_run", "unit_stage", "stages/unit_stage/02_runs/unit_run")

            write_mt5_kpi_recording_packet(root, created_at_utc="2026-04-29T00:00:00Z")

            record_path = root / "docs/agent_control/packets/kpi_rebuild_mt5_recording_v1/normalized_kpi_records.jsonl"
            record = json.loads(record_path.read_text(encoding="utf-8").splitlines()[0])

            self.assertIsNone(record["mt5_trading_headline"]["net_profit"]["value"])
            self.assertEqual(
                record["mt5_trading_headline"]["net_profit"]["n/a_reason"],
                "profit_attribution_not_separable_from_single_routed_account_path",
            )
            self.assertEqual(record["execution"]["order_attempt_count"]["value"], 3)

    def test_execution_aliases_accept_stage10_runtime_summary_names(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_template(root)
            run_root = root / "stages/unit_stage/02_runs/unit_run"
            report_path = run_root / "mt5/reports/unit_report.htm"
            report_path.parent.mkdir(parents=True)
            report_path.write_text(_report_html(gross_loss="-10.00", profit_factor="2.25"), encoding="utf-16")
            (run_root / "kpi_record.json").write_text(
                json.dumps(
                    {
                        "run_id": "unit_run",
                        "stage_id": "unit_stage",
                        "mt5_records": [
                            {
                                "record_view": "mt5_routed_total_validation_is",
                                "tier_scope": "Tier A+B",
                                "split": "validation_is",
                                "route_role": "routed_total",
                                "metrics": {
                                    "order_attempt_count": 5,
                                    "order_fill_count": 4,
                                    "feature_skip_count": 7,
                                },
                                "report": {"html_report": {"path": report_path.as_posix()}},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            _seed_inventory(root, "unit_run", "unit_stage", "stages/unit_stage/02_runs/unit_run")

            write_mt5_kpi_recording_packet(root, created_at_utc="2026-04-29T00:00:00Z")

            record_path = root / "docs/agent_control/packets/kpi_rebuild_mt5_recording_v1/normalized_kpi_records.jsonl"
            record = json.loads(record_path.read_text(encoding="utf-8").splitlines()[0])

            self.assertEqual(record["execution"]["order_fill_count"]["value"], 4)
            self.assertEqual(record["execution"]["skip_count"]["value"], 7)

    def test_scans_reports_folder_when_kpi_records_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_template(root)
            run_root = root / "stages/unit_stage/02_runs/unit_run"
            report_path = run_root / "mt5/reports/Project_Obsidian_Prime_v2_unit_run_routed_oos.htm"
            report_path.parent.mkdir(parents=True)
            report_path.write_text(_report_html(gross_loss="-10.00", profit_factor="2.25"), encoding="utf-16")
            (run_root / "kpi_record.json").write_text(json.dumps({"run_id": "unit_run"}), encoding="utf-8")
            _seed_inventory(root, "unit_run", "unit_stage", "stages/unit_stage/02_runs/unit_run")

            packet = write_mt5_kpi_recording_packet(root, created_at_utc="2026-04-29T00:00:00Z")

            self.assertEqual(packet["summary"]["normalized_records_written"], 1)
            record_path = root / "docs/agent_control/packets/kpi_rebuild_mt5_recording_v1/normalized_kpi_records.jsonl"
            record = json.loads(record_path.read_text(encoding="utf-8").splitlines()[0])

            self.assertEqual(record["row_grain"]["record_view"]["value"], "mt5_routed_total_oos")
            self.assertEqual(record["row_grain"]["tier_scope"]["value"], "Tier A+B")
            self.assertEqual(record["mt5_trading_headline"]["net_profit"]["value"], 12.5)
            self.assertEqual(record["source_evidence"]["report_identity_source"], "filename_scan_fallback")

    def test_target_confirmation_filters_excluded_run_and_count(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_template(root)
            _seed_inventory_many(
                root,
                [
                    ("run_a", "unit_stage", "stages/unit_stage/02_runs/run_a", "1"),
                    ("run_b", "unit_stage", "stages/unit_stage/02_runs/run_b", "1"),
                    ("run_excluded", "unit_stage", "stages/unit_stage/02_runs/run_excluded", "0"),
                ],
            )
            _seed_target_confirmation(root, expected=2, excluded=["run_excluded"])

            packet = write_mt5_kpi_recording_packet(root, created_at_utc="2026-04-29T00:00:00Z")

            self.assertEqual(packet["summary"]["target_runs_total"], 2)
            self.assertEqual(packet["summary"]["target_confirmation_status"], "confirmed")

    def test_target_confirmation_blocks_when_excluded_default_target_is_selected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_template(root)
            _seed_inventory_many(
                root,
                [
                    ("run_a", "unit_stage", "stages/unit_stage/02_runs/run_a", "1"),
                    ("run_b", "unit_stage", "stages/unit_stage/02_runs/run_b", "1"),
                    ("run_excluded", "unit_stage", "stages/unit_stage/02_runs/run_excluded", "1"),
                ],
            )
            _seed_target_confirmation(root, expected=2, excluded=["run_excluded"])

            packet = write_mt5_kpi_recording_packet(root, created_at_utc="2026-04-29T00:00:00Z")

            self.assertEqual(packet["summary"]["status"], "blocked_target_confirmation")
            self.assertIn(
                "target_confirmation_excluded_run_selected",
                {finding["check_id"] for finding in packet["summary"]["target_confirmation_findings"]},
            )

    def test_target_confirmation_blocks_count_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_template(root)
            _seed_inventory_many(
                root,
                [
                    ("run_a", "unit_stage", "stages/unit_stage/02_runs/run_a", "1"),
                    ("run_b", "unit_stage", "stages/unit_stage/02_runs/run_b", "1"),
                ],
            )
            _seed_target_confirmation(root, expected=3, excluded=[])

            packet = write_mt5_kpi_recording_packet(root, created_at_utc="2026-04-29T00:00:00Z")

            self.assertEqual(packet["summary"]["status"], "blocked_target_confirmation")
            self.assertIn(
                "target_confirmation_mismatch",
                {finding["check_id"] for finding in packet["summary"]["target_confirmation_findings"]},
            )

    def test_target_confirmation_missing_falls_back_to_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_template(root)
            _seed_inventory_many(
                root,
                [("run_a", "unit_stage", "stages/unit_stage/02_runs/run_a", "1")],
            )

            packet = write_mt5_kpi_recording_packet(root, created_at_utc="2026-04-29T00:00:00Z")

            self.assertEqual(packet["summary"]["target_runs_total"], 1)
            self.assertEqual(packet["summary"]["target_confirmation_status"], "missing_fallback_inventory_only")

    def test_kpi_record_report_identity_wins_over_filename(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_template(root)
            run_root = root / "stages/unit_stage/02_runs/unit_run"
            report_path = run_root / "mt5/reports/unknown_name.htm"
            report_path.parent.mkdir(parents=True)
            report_path.write_text(_report_html(gross_loss="-10.00", profit_factor="2.25"), encoding="utf-16")
            (run_root / "kpi_record.json").write_text(
                json.dumps(
                    {
                        "run_id": "unit_run",
                        "stage_id": "unit_stage",
                        "mt5_records": [
                            {
                                "record_view": "mt5_tier_a_only_oos",
                                "tier_scope": "Tier A",
                                "split": "oos",
                                "route_role": "tier_only_total",
                                "metrics": {},
                                "report": {"html_report": {"path": report_path.as_posix()}},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            _seed_inventory(root, "unit_run", "unit_stage", "stages/unit_stage/02_runs/unit_run")

            write_mt5_kpi_recording_packet(root, created_at_utc="2026-04-29T00:00:00Z")

            record_path = root / "docs/agent_control/packets/kpi_rebuild_mt5_recording_v1/normalized_kpi_records.jsonl"
            record = json.loads(record_path.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(record["row_grain"]["record_view"]["value"], "mt5_tier_a_only_oos")
            self.assertEqual(record["source_evidence"]["report_identity_source"], "kpi_record_mt5_records")

    def test_unknown_report_filename_is_parser_error_not_normalized_row(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_template(root)
            run_root = root / "stages/unit_stage/02_runs/unit_run"
            report_path = run_root / "mt5/reports/unknown_name.htm"
            report_path.parent.mkdir(parents=True)
            report_path.write_text(_report_html(gross_loss="-10.00", profit_factor="2.25"), encoding="utf-16")
            (run_root / "kpi_record.json").write_text(json.dumps({"run_id": "unit_run"}), encoding="utf-8")
            _seed_inventory(root, "unit_run", "unit_stage", "stages/unit_stage/02_runs/unit_run")

            packet = write_mt5_kpi_recording_packet(root, created_at_utc="2026-04-29T00:00:00Z")

            self.assertEqual(packet["summary"]["normalized_records_written"], 0)
            self.assertIn(
                "mt5_report_identity_unresolved",
                {error["error"] for error in packet["summary"]["parser_errors"]},
            )


def _seed_template(root: Path) -> None:
    destination = root / "docs/templates/kpi_record_normalized.template.json"
    destination.parent.mkdir(parents=True)
    destination.write_text((ROOT / "docs/templates/kpi_record_normalized.template.json").read_text(encoding="utf-8"), encoding="utf-8")


def _seed_inventory(root: Path, run_id: str, stage_id: str, path: str) -> None:
    _seed_inventory_many(root, [(run_id, stage_id, path, "1")])


def _seed_inventory_many(root: Path, rows: list[tuple[str, str, str, str]]) -> None:
    inventory_path = root / "docs/agent_control/packets/kpi_rebuild_inventory_v1/experiment_inventory.csv"
    inventory_path.parent.mkdir(parents=True)
    with inventory_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["run_id", "stage_id", "path", "default_rework_target", "judgment"])
        writer.writeheader()
        for run_id, stage_id, path, default_target in rows:
            writer.writerow(
                {
                    "run_id": run_id,
                    "stage_id": stage_id,
                    "path": path,
                    "default_rework_target": default_target,
                    "judgment": "unit_judgment",
                }
            )


def _seed_target_confirmation(root: Path, *, expected: int, excluded: list[str]) -> None:
    path = root / "docs/agent_control/packets/kpi_rebuild_inventory_v1/target_confirmation.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    excluded_lines = ["  excluded_run_ids: []"] if not excluded else ["  excluded_run_ids:", *[f"    - {run_id}" for run_id in excluded]]
    path.write_text(
        "\n".join(
            [
                "confirmation_id: unit",
                "interpretation:",
                f"  kpi_rebuild_default_target_rows: {expected}",
                *excluded_lines,
                "next_packet_scope:",
                "  do_not_rerun_invalid_reference: true",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _report_html(*, gross_loss: str, profit_factor: str) -> str:
    return f"""
    <html><body><table>
    <tr><td>Total Net Profit:</td><td>12.50</td><td>Balance Drawdown Maximal:</td><td>5.00 (1.00%)</td><td>Equity Drawdown Maximal:</td><td>6.25 (1.25%)</td></tr>
    <tr><td>Gross Profit:</td><td>22.50</td><td>Gross Loss:</td><td>{gross_loss}</td></tr>
    <tr><td>Profit Factor:</td><td>{profit_factor}</td><td>Expected Payoff:</td><td>1.25</td></tr>
    <tr><td>Recovery Factor:</td><td>2.00</td><td>Sharpe Ratio:</td><td>1.50</td></tr>
    <tr><td>Total Trades:</td><td>10</td><td>Short Trades (won %):</td><td>4 (50.00%)</td><td>Long Trades (won %):</td><td>6 (66.67%)</td></tr>
    <tr><td>Total Deals:</td><td>20</td><td>Profit Trades (% of total):</td><td>6 (60.00%)</td><td>Loss Trades (% of total):</td><td>4 (40.00%)</td></tr>
    </table></body></html>
    """


if __name__ == "__main__":
    unittest.main()
