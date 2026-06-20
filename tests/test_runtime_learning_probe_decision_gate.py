from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from foundation.control_plane.runtime_learning_probe_decision_gate import audit_runtime_learning_probe_decision


def _decision(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "pre_gate_signal_count": 3,
        "strong_candidate_count": 0,
        "runtime_learning_probe_candidate_count": 1,
        "runtime_surface_status": "probe_candidate_available",
        "mt5_action": "run_probe",
        "not_run_reason_code": "",
        "repair_attempt_required": False,
        "repair_attempts": [],
        "forbidden_skip_basis_seen": [],
        "claim_effect": "runtime_learning_probe_decision_only_no_runtime_authority",
    }
    payload.update(overrides)
    return payload


class RuntimeLearningProbeDecisionGateTests(unittest.TestCase):
    def test_candidate_gate_failure_cannot_skip_runtime_learning_probe(self) -> None:
        result = audit_runtime_learning_probe_decision(
            _decision(
                runtime_learning_probe_candidate_count=1,
                mt5_action="not_run_blocked",
                not_run_reason_code="candidate_gate_failed",
                forbidden_skip_basis_seen=["candidate_gate_failed"],
            )
        )

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "runtime_learning_probe_decision_gate::forbidden_skip_reason",
            {finding.check_id for finding in result.findings},
        )
        self.assertIn(
            "runtime_learning_probe_decision_gate::learning_candidate_requires_mt5_action",
            {finding.check_id for finding in result.findings},
        )

    def test_no_actionable_surface_requires_repair_attempt_before_no_run(self) -> None:
        result = audit_runtime_learning_probe_decision(
            _decision(
                runtime_learning_probe_candidate_count=0,
                runtime_surface_status="no_actionable_runtime_surface",
                mt5_action="not_run_after_repair_impossible",
                not_run_reason_code="no_runtime_substrate_after_repair",
                repair_attempt_required=True,
                repair_attempts=[],
            )
        )

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "runtime_learning_probe_decision_gate::repair_required_without_attempt",
            {finding.check_id for finding in result.findings},
        )

    def test_runtime_learning_candidate_passes_when_probe_action_is_selected(self) -> None:
        result = audit_runtime_learning_probe_decision(_decision())

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])
        self.assertIn("runtime_learning_probe_decision_recorded", result.allowed_claims)

    def test_no_run_can_pass_after_repair_with_allowed_block_reason(self) -> None:
        result = audit_runtime_learning_probe_decision(
            _decision(
                pre_gate_signal_count=1,
                runtime_learning_probe_candidate_count=0,
                runtime_surface_status="repair_required",
                mt5_action="not_run_after_repair_impossible",
                not_run_reason_code="no_runtime_substrate_after_repair",
                repair_attempt_required=True,
                repair_attempts=[
                    {
                        "attempt_id": "repair01",
                        "action": "inspect_f97_runtime_substrate",
                        "result": "no_onnx_ea_set_or_feature_runtime_bundle",
                    }
                ],
            )
        )

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])

    def test_cli_writes_extra_audit_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            decision_path = root / "decision.json"
            output_path = root / "audit.json"
            decision_path.write_text(json.dumps(_decision()), encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "foundation.control_plane.runtime_learning_probe_decision_gate",
                    str(decision_path),
                    "--output-json",
                    str(output_path),
                ],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["audit_name"], "runtime_learning_probe_decision_gate")
            self.assertEqual(payload["status"], "pass")

    def test_closeout_gate_blocks_completed_when_runtime_learning_decision_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            work_packet = root / "work_packet.yaml"
            decision_path = root / "decision.json"
            output_path = root / "closeout_gate.json"
            work_packet.write_text(
                "\n".join(
                    [
                        "risk_vector_scan:",
                        "  required_gates: [runtime_learning_probe_decision_gate, required_gate_coverage_audit, final_claim_guard]",
                        "gates: {}",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            decision_path.write_text(
                json.dumps(
                    _decision(
                        mt5_action="not_run_blocked",
                        not_run_reason_code="proxy_bad",
                        forbidden_skip_basis_seen=["proxy_bad"],
                    )
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "foundation.control_plane.closeout_gate",
                    "--packet-id",
                    "unit_packet",
                    "--requested-claim",
                    "completed",
                    "--work-packet",
                    str(work_packet),
                    "--runtime-learning-probe-decision",
                    str(decision_path),
                    "--required-gate-coverage",
                    "--output-json",
                    str(output_path),
                ],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertTrue(payload["completed_forbidden"])
            self.assertIn(
                "runtime_learning_probe_decision_gate",
                {audit["audit_name"] for audit in payload["audits"]},
            )


if __name__ == "__main__":
    unittest.main()
