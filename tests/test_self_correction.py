from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from foundation.control_plane.self_correction import audit_self_correction_plan


class SelfCorrectionTests(unittest.TestCase):
    def test_passed_audits_need_no_repair(self) -> None:
        result = audit_self_correction_plan(
            [
                {
                    "audit_name": "ops_instruction_audit",
                    "status": "pass",
                    "findings": [],
                    "allowed_claims": ["ops_instructions_stable"],
                    "forbidden_claims": [],
                }
            ],
            policy={"safe_autofix_allowlist": ["attach_existing_audit_json_to_closeout"]},
        )

        self.assertEqual(result.status, "pass")
        self.assertEqual(result.counts["repair_item_count"], 0)
        self.assertIn("self_correction_not_needed", result.allowed_claims)

    def test_plan_only_classifies_missing_closeout_gate_execution(self) -> None:
        result = audit_self_correction_plan(
            [
                {
                    "audit_name": "required_gate_coverage_audit",
                    "status": "blocked",
                    "findings": [
                        {
                            "check_id": "required_gate_coverage::missing_required_gates",
                            "message": "Required gates were declared but not executed.",
                            "severity": "blocking",
                            "details": {"missing_required_gates": ["state_sync_audit"]},
                        }
                    ],
                }
            ],
            policy={"safe_autofix_allowlist": ["attach_existing_audit_json_to_closeout"]},
        )

        self.assertEqual(result.status, "blocked")
        item = result.counts["repair_items"][0]
        self.assertEqual(item["failure_kind"], "missing_closeout_gate_execution")
        self.assertEqual(item["recommended_action"], "attach_existing_audit_json_to_closeout")
        self.assertTrue(item["safe_autofix_eligible"])
        self.assertEqual(item["target_gates"], ["state_sync_audit"])

    def test_cli_flattens_closeout_gate_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            closeout = root / "closeout_gate.json"
            output = root / "self_correction_plan.json"
            closeout.write_text(
                json.dumps(
                    {
                        "packet_id": "unit",
                        "status": "blocked",
                        "audits": [
                            {
                                "audit_name": "code_surface_audit",
                                "status": "blocked",
                                "findings": [
                                    {
                                        "check_id": "code_surface::large_file",
                                        "message": "File exceeds attention budget.",
                                        "severity": "blocking",
                                        "details": {"path": "foundation/example.py"},
                                    }
                                ],
                            }
                        ],
                        "final_claim_guard": {
                            "audit_name": "final_claim_guard",
                            "status": "blocked",
                            "findings": [],
                        },
                    }
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "foundation.control_plane.self_correction",
                    "--audit-json",
                    str(closeout),
                    "--output-json",
                    str(output),
                    "--allow-blocked-exit-zero",
                ],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "blocked")
            self.assertEqual(payload["counts"]["repair_items"][0]["failure_kind"], "code_surface_violation")


if __name__ == "__main__":
    unittest.main()
