from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from foundation.control_plane.state_sync_audit import audit_state_sync


class StateSyncAuditTests(unittest.TestCase):
    def test_detects_run_conflict_and_stale_boundary_then_passes_after_sync(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root, selection_run="run03E_old_mt5_v1", stale_boundary=True)

            blocked = audit_state_sync(root)

            self.assertEqual(blocked.status, "blocked")
            self.assertTrue(blocked.completed_forbidden)
            self.assertIn("current_run_conflict", {finding.check_id for finding in blocked.findings})
            self.assertIn("stage_brief_boundary_stale", {finding.check_id for finding in blocked.findings})
            self.assertIn("current_truth_synced", blocked.forbidden_claims)

            self._write_fixture(root, selection_run="run03F_et_v11_tier_balance_mt5_v1", stale_boundary=False)
            passed = audit_state_sync(root)

            self.assertEqual(passed.status, "pass")
            self.assertFalse(passed.completed_forbidden)
            self.assertEqual(passed.findings, ())
            self.assertIn("current_truth_synced", passed.allowed_claims)

    def test_detects_active_branch_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_fixture(root, selection_run="run03F_et_v11_tier_balance_mt5_v1", stale_boundary=False)

            blocked = audit_state_sync(root, current_branch="feature/unit")

            self.assertEqual(blocked.status, "blocked")
            self.assertIn("active_branch_mismatch", {finding.check_id for finding in blocked.findings})

            passed = audit_state_sync(root, current_branch="main")

            self.assertEqual(passed.status, "pass", [finding.to_dict() for finding in passed.findings])

    def _write_fixture(self, root: Path, *, selection_run: str, stale_boundary: bool) -> None:
        stage_id = "12_stage_unit"
        (root / "docs/workspace").mkdir(parents=True, exist_ok=True)
        (root / "docs/context").mkdir(parents=True, exist_ok=True)
        (root / "docs/registers").mkdir(parents=True, exist_ok=True)
        stage_root = root / "stages" / stage_id
        (stage_root / "04_selected").mkdir(parents=True, exist_ok=True)
        (stage_root / "00_spec").mkdir(parents=True, exist_ok=True)
        (stage_root / "03_reviews").mkdir(parents=True, exist_ok=True)

        current_run = "run03F_et_v11_tier_balance_mt5_v1"
        (root / "docs/workspace/workspace_state.yaml").write_text(
            "\n".join(
                [
                    f'active_stage: "{stage_id}"',
                    'active_branch: "main"',
                    "stage12:",
                    f'  stage_id: "{stage_id}"',
                    f'  current_run_id: "{current_run}"',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (root / "docs/context/current_working_state.md").write_text(
            f"- current run(현재 실행): `{current_run}`\n",
            encoding="utf-8",
        )
        (stage_root / "04_selected/selection_status.md").write_text(
            f"- current run(현재 실행): `{selection_run}`\n",
            encoding="utf-8",
        )
        boundary = (
            "Python structural scout(파이썬 구조 탐침)만 주장한다."
            if stale_boundary
            else "Python structural scout(파이썬 구조 탐침)와 MT5 runtime_probe(MT5 런타임 탐침) 근거를 함께 기록한다."
        )
        (stage_root / "00_spec/stage_brief.md").write_text(
            f"## 경계(Boundary, 경계)\n\n{boundary}\n",
            encoding="utf-8",
        )
        (root / "docs/registers/run_registry.csv").write_text(
            f"stage_id,run_id\n{stage_id},{current_run}\n",
            encoding="utf-8",
        )
        (stage_root / "03_reviews/stage_run_ledger.csv").write_text(
            f"stage_id,run_id\n{stage_id},{current_run}\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
