from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from foundation.control_plane import mt5_missing_report_executor as executor


class Mt5MissingReportExecutorTests(unittest.TestCase):
    def test_classifies_materialized_and_structural_only_missing_runs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _seed_source_summary(root)
            _seed_inventory(root)
            materialized = root / "stages/stage/02_runs/materialized/mt5"
            materialized.mkdir(parents=True)
            (materialized / "routed_oos.ini").write_text(
                "[Tester]\nReport=Project_Obsidian_Prime_v2_materialized_routed_oos\n",
                encoding="utf-8",
            )
            (materialized / "routed_oos.set").write_text(
                "InpTelemetryCsvPath=Project_Obsidian_Prime_v2/stage/materialized/telemetry.csv\n"
                "InpSummaryCsvPath=Project_Obsidian_Prime_v2/stage/materialized/summary.csv\n",
                encoding="utf-8",
            )
            (root / "stages/stage/02_runs/structural").mkdir(parents=True)

            rows = executor._missing_inventory_rows(root)
            executable, blocked = executor._classify_missing_rows(root, rows)

            self.assertEqual([row["run_id"] for row in executable], ["materialized"])
            self.assertEqual([row["run_id"] for row in blocked], ["structural"])
            self.assertEqual(blocked[0]["reason"], "mt5_inputs_not_materialized")

    def test_attempt_payload_reads_ini_set_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            mt5_root = root / "stages/stage/02_runs/materialized/mt5"
            mt5_root.mkdir(parents=True)
            (mt5_root / "routed_validation_is.ini").write_text(
                "[Tester]\nReport=Project_Obsidian_Prime_v2_materialized_routed_validation_is\n",
                encoding="utf-8",
            )
            (mt5_root / "routed_validation_is.set").write_text(
                "InpTelemetryCsvPath=Project_Obsidian_Prime_v2/stage/materialized/telemetry.csv\n"
                "InpSummaryCsvPath=Project_Obsidian_Prime_v2/stage/materialized/summary.csv\n",
                encoding="utf-8",
            )

            payload = executor._attempt_payload(
                root,
                {"run_id": "materialized", "stage_id": "stage", "path": "stages/stage/02_runs/materialized"},
                "routed_validation_is",
            )

            self.assertEqual(payload["tier"], "Tier A+B")
            self.assertEqual(payload["split"], "validation_is")
            self.assertEqual(payload["ini"]["tester"]["Report"], "Project_Obsidian_Prime_v2_materialized_routed_validation_is")
            self.assertEqual(payload["common_summary_path"], "Project_Obsidian_Prime_v2/stage/materialized/summary.csv")


def _seed_source_summary(root: Path) -> None:
    path = root / executor.SOURCE_SUMMARY_PATH
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "missing_runs": [
                    {"run_id": "materialized"},
                    {"run_id": "structural"},
                ]
            }
        ),
        encoding="utf-8",
    )


def _seed_inventory(root: Path) -> None:
    path = root / executor.INVENTORY_PATH
    path.parent.mkdir(parents=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["run_id", "stage_id", "path"])
        writer.writeheader()
        writer.writerow({"run_id": "materialized", "stage_id": "stage", "path": "stages/stage/02_runs/materialized"})
        writer.writerow({"run_id": "structural", "stage_id": "stage", "path": "stages/stage/02_runs/structural"})


if __name__ == "__main__":
    unittest.main()
