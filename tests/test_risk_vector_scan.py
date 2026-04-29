from __future__ import annotations

import unittest

from foundation.control_plane.prompt_intake_classifier import classify_prompt
from foundation.control_plane.risk_vector_scan import scan_risk_vector


class RiskVectorScanTests(unittest.TestCase):
    def test_state_sync_work_requires_state_sync_audit(self) -> None:
        classification = classify_prompt("상태 싱크 맞춰줘")
        result = scan_risk_vector(classification)

        self.assertEqual(result.risks["state_sync_risk"], "high")
        self.assertIn("state_sync_audit", result.required_gates)
        self.assertIn("current_truth_synced", result.forbidden_claims)

    def test_current_truth_conflict_is_hard_stop(self) -> None:
        classification = classify_prompt("상태 확인해줘")
        result = scan_risk_vector(classification, current_truth_conflict=True)

        self.assertIn("state_sync_risk", result.hard_stop_risks)
        self.assertIn("canonical_current_truth", result.required_decision_locks)

    def test_kpi_work_requires_source_authority_checks(self) -> None:
        classification = classify_prompt("KPI 포맷 통일해줘")
        result = scan_risk_vector(classification)

        self.assertEqual(result.risks["kpi_source_risk"], "high")
        self.assertIn("kpi_contract_audit", result.required_gates)
        self.assertIn("source_authority_audit", result.required_gates)

    def test_code_refactor_requires_code_surface_audit(self) -> None:
        classification = classify_prompt("코드 분산 정리해줘")
        result = scan_risk_vector(classification)

        self.assertEqual(result.risks["code_surface_risk"], "high")
        self.assertIn("code_surface_audit", result.required_gates)
        self.assertIn("obsidian-code-surface-guard", result.required_skills)

    def test_runtime_work_requires_runtime_parity_skills(self) -> None:
        classification = classify_prompt("MT5까지 돌려줘")
        result = scan_risk_vector(classification)

        self.assertEqual(result.risks["runtime_parity_risk"], "high")
        self.assertIn("obsidian-runtime-parity", result.required_skills)
        self.assertIn("mt5_verification_complete", result.forbidden_claims)


if __name__ == "__main__":
    unittest.main()
