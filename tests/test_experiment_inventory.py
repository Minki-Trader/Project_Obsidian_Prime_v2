from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

import yaml

from foundation.control_plane.experiment_inventory import (
    INVENTORY_COLUMNS,
    build_experiment_inventory,
    classify_rework_scope,
    write_inventory_packet,
)


ROOT = Path(__file__).resolve().parents[1]


class ExperimentInventoryTests(unittest.TestCase):
    def test_inventory_represents_every_run_registry_row(self) -> None:
        with (ROOT / "docs/registers/run_registry.csv").open(encoding="utf-8-sig", newline="") as handle:
            registry_rows = list(csv.DictReader(handle))

        result = build_experiment_inventory(ROOT, created_at_utc="2026-04-29T00:00:00Z")

        self.assertEqual(len(result.records), len(registry_rows))
        self.assertEqual(result.summary["counts"]["inventory_rows"], len(registry_rows))
        self.assertEqual(result.summary["counts"]["missing_run_paths"], 0)

    def test_rework_classification_separates_foundation_invalid_and_default_targets(self) -> None:
        result = build_experiment_inventory(ROOT, created_at_utc="2026-04-29T00:00:00Z")
        by_run = {record["run_id"]: record for record in result.records}

        self.assertEqual(by_run["20260424_raw_m5_inventory"]["rework_scope"], "foundation_reference_only")
        self.assertFalse(by_run["20260424_raw_m5_inventory"]["default_rework_target"])

        self.assertEqual(by_run["run03A_extratrees_fwd18_inverse_context_scout_v1"]["rework_scope"], "invalid_reference_only")
        self.assertFalse(by_run["run03A_extratrees_fwd18_inverse_context_scout_v1"]["default_rework_target"])

        self.assertEqual(by_run["run01A_logreg_threshold_mt5_scout_v1"]["rework_scope"], "kpi_rebuild_candidate")
        self.assertTrue(by_run["run01A_logreg_threshold_mt5_scout_v1"]["default_rework_target"])

    def test_summary_counts_match_rework_scopes(self) -> None:
        result = build_experiment_inventory(ROOT, created_at_utc="2026-04-29T00:00:00Z")
        scopes = {}
        for record in result.records:
            scopes[record["rework_scope"]] = scopes.get(record["rework_scope"], 0) + 1

        self.assertEqual(result.summary["by_rework_scope"], dict(sorted(scopes.items())))
        self.assertEqual(
            result.summary["counts"]["default_rework_targets"],
            sum(1 for record in result.records if record["default_rework_target"]),
        )
        self.assertEqual(result.summary["counts"]["stage10_to_active_rows"], 71)

    def test_long_path_safe_inventory_keeps_run01y_available(self) -> None:
        result = build_experiment_inventory(ROOT, created_at_utc="2026-04-29T00:00:00Z")
        by_run = {record["run_id"]: record for record in result.records}
        run01y = by_run["run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1"]

        self.assertTrue(run01y["path_exists"])
        self.assertGreaterEqual(run01y["path_length"], 240)
        self.assertTrue(run01y["long_path_risk"])

    def test_write_inventory_packet_materializes_required_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "packet"
            result = write_inventory_packet(
                ROOT,
                output_dir=output_dir,
                created_at_utc="2026-04-29T00:00:00Z",
            )

            inventory_path = output_dir / "experiment_inventory.csv"
            summary_path = output_dir / "inventory_summary.json"
            work_packet_path = output_dir / "work_packet.yaml"
            run_plan_path = output_dir / "run_plan.yaml"

            self.assertTrue(inventory_path.exists())
            self.assertTrue(summary_path.exists())
            self.assertTrue(work_packet_path.exists())
            self.assertTrue(run_plan_path.exists())
            self.assertTrue((output_dir / "skill_receipts/session_intake.yaml").exists())
            self.assertTrue((output_dir / "skill_receipts/artifact_lineage.yaml").exists())
            self.assertTrue((output_dir / "skill_receipts/experiment_design.yaml").exists())

            with inventory_path.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(tuple(rows[0].keys()), INVENTORY_COLUMNS)
            self.assertEqual(len(rows), result.summary["counts"]["inventory_rows"])

            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertTrue(summary["no_experiment_execution"])
            self.assertTrue(summary["no_ledger_overwrite"])

            packet = yaml.safe_load(work_packet_path.read_text(encoding="utf-8"))
            plan = yaml.safe_load(run_plan_path.read_text(encoding="utf-8"))
            self.assertEqual(packet["preflight"]["selected_option_id"], "inventory_only_no_rerun")
            self.assertTrue(plan["execution_scope"]["no_experiment_execution"])
            self.assertIn("claim_kpi_rebuild_completed", plan["forbidden_actions"])

    def test_classify_rework_scope_does_not_expand_non_run_sequence_rows(self) -> None:
        scope, target, reason = classify_rework_scope(
            {
                "run_id": "20260425_stage07_baseline_training_smoke_v1",
                "stage_id": "07_model_training_baseline__contract_preprocessing_smoke",
                "status": "reviewed",
                "judgment": "positive_baseline_training_smoke_passed",
            }
        )

        self.assertEqual(scope, "foundation_reference_only")
        self.assertFalse(target)
        self.assertEqual(reason, "pre_alpha_or_non_run_sequence_reference")


if __name__ == "__main__":
    unittest.main()
