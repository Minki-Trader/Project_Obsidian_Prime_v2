from __future__ import annotations

import unittest

from foundation.control_plane.final_claim_guard import guard_final_claims
from foundation.control_plane.required_gate_coverage_audit import audit_required_gate_coverage


class RequiredGateCoverageAuditTests(unittest.TestCase):
    def test_required_gate_coverage_audit_blocks_missing_gate(self) -> None:
        result = audit_required_gate_coverage(
            {"risk_vector_scan": {"required_gates": ["code_surface_audit"]}},
            {"audits": [{"audit_name": "state_sync_audit"}], "final_claim_guard": {"audit_name": "final_claim_guard"}},
        )

        self.assertEqual(result.status, "blocked")
        self.assertTrue(result.completed_forbidden)
        self.assertIn("required_gate_coverage::missing_required_gates", {finding.check_id for finding in result.findings})

    def test_required_gate_coverage_allows_not_applicable_with_reason(self) -> None:
        result = audit_required_gate_coverage(
            {
                "risk_vector_scan": {"required_gates": ["kpi_contract_audit"]},
                "gates": {"not_applicable_with_reason": {"kpi_contract_audit": "not KPI work"}},
            },
            {"audits": [], "final_claim_guard": {"audit_name": "final_claim_guard"}},
        )

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])
        self.assertFalse(result.completed_forbidden)

    def test_required_gate_coverage_blocks_declared_not_implemented_for_completed(self) -> None:
        coverage = audit_required_gate_coverage(
            {
                "risk_vector_scan": {"required_gates": ["semantic_code_surface_audit"]},
                "gates": {"declared_not_implemented": {"semantic_code_surface_audit": "not implemented yet"}},
            },
            {"audits": [], "final_claim_guard": {"audit_name": "final_claim_guard"}},
        )
        final_guard = guard_final_claims(requested_claims=("completed",), audit_results=(coverage,))

        self.assertEqual(coverage.status, "blocked")
        self.assertTrue(coverage.completed_forbidden)
        self.assertEqual(final_guard.status, "blocked")


if __name__ == "__main__":
    unittest.main()
