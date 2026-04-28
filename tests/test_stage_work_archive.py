from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from foundation.control_plane.stage_work_archive import build_stage_work_archive


class StageWorkArchiveTests(unittest.TestCase):
    def test_archive_creates_zip_and_manifest_without_moving_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            stage_dir = root / "stages/10_alpha_scout__default_split_model_threshold_scan"
            source_file = stage_dir / "02_runs/run01A/summary.json"
            source_file.parent.mkdir(parents=True)
            source_file.write_text('{"ok": true}\n', encoding="utf-8")

            result = build_stage_work_archive(
                root,
                archive_id="unit_archive",
                stage_ids=("10_alpha_scout__default_split_model_threshold_scan",),
                manifest_path=root / "docs/agent_control/packets/unit/archive_manifest.json",
                created_at_utc="2026-04-29T00:00:00Z",
            )

            self.assertTrue(result.zip_path.exists())
            self.assertTrue(result.manifest_path.exists())
            self.assertTrue(source_file.exists())

            manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["file_count"], 1)
            self.assertEqual(manifest["archive_strategy"], "zip_plus_manifest; original_paths_preserved")

            with zipfile.ZipFile(result.zip_path) as archive:
                names = archive.namelist()
            self.assertEqual(names, ["stages/10_alpha_scout__default_split_model_threshold_scan/02_runs/run01A/summary.json"])

    def test_archive_rejects_paths_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "stages/unit").mkdir(parents=True)

            with self.assertRaises(ValueError):
                build_stage_work_archive(
                    root,
                    archive_id="unit_archive",
                    stage_ids=("unit",),
                    zip_path=Path(temp_dir).parent / "outside.zip",
                    created_at_utc="2026-04-29T00:00:00Z",
                )


if __name__ == "__main__":
    unittest.main()
