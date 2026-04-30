from __future__ import annotations

import unittest

from foundation.control_plane.work_packet_schema_lint import audit_work_packet_schema


class WorkPacketSchemaLintTests(unittest.TestCase):
    def test_v1_packet_remains_compatible(self) -> None:
        result = audit_work_packet_schema(_v1_packet())

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])

    def test_v2_missing_required_section_blocks_completion(self) -> None:
        packet = _v2_packet()
        packet.pop("decision_lock")

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertTrue(result.completed_forbidden)
        self.assertIn("work_packet_schema::v2::missing_top_level::decision_lock", {finding.check_id for finding in result.findings})

    def test_non_run_work_cannot_use_old_run_only_scope(self) -> None:
        packet = _v1_packet()
        packet["user_request"]["requested_action"] = "state_sync"

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn("work_packet_schema::non_run_uses_run_only_scope", {finding.check_id for finding in result.findings})

    def test_v2_non_run_packet_passes_with_general_scope(self) -> None:
        result = audit_work_packet_schema(_v2_packet())

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])


def _v1_packet() -> dict[str, object]:
    return {
        "packet_id": "unit_v1",
        "created_at_utc": "2026-04-29T00:00:00Z",
        "user_request": {"user_quote": "", "requested_action": "experiment_execution"},
        "current_truth": {},
        "preflight": {},
        "interpreted_scope": {
            "variants_requested": {"value": 1},
            "verification_layers": ["python_structural"],
            "mt5_required": False,
            "top_k_reduction_allowed": False,
        },
        "acceptance_criteria": [],
        "row_grain": {},
        "kpi_contract": {},
        "artifact_contract": {},
        "skill_routing": {
            "primary_family": "state_sync",
            "primary_skill": "obsidian-stage-transition",
            "support_skills": ["obsidian-reentry-read", "obsidian-artifact-lineage", "obsidian-claim-discipline"],
            "skills_considered": ["obsidian-stage-transition", "obsidian-reentry-read"],
            "skills_selected": ["obsidian-stage-transition", "obsidian-reentry-read", "obsidian-artifact-lineage", "obsidian-claim-discipline"],
            "skills_not_used": [],
            "required_skill_receipts": ["obsidian-stage-transition", "obsidian-reentry-read", "obsidian-artifact-lineage", "obsidian-claim-discipline"],
            "required_gates": ["state_sync_audit", "final_claim_guard"],
        },
        "gates": {},
        "final_claim_policy": {},
    }


def _v2_packet() -> dict[str, object]:
    return {
        "version": "work_packet_schema_v2",
        "packet_id": "unit_v2",
        "created_at_utc": "2026-04-29T00:00:00Z",
        "user_request": {"user_quote": "", "requested_action": "state_sync"},
        "current_truth": {},
        "work_classification": {"primary_family": "state_sync"},
        "risk_vector_scan": {"risks": {"state_sync_risk": "high"}},
        "decision_lock": {"mode": "assume_safe_default", "assumptions": {"report_only": True}},
        "interpreted_scope": {
            "work_families": ["state_sync"],
            "target_surfaces": ["docs_current_truth"],
            "scope_units": ["document"],
            "execution_layers": ["read_only"],
            "mutation_policy": {"allowed": False},
            "evidence_layers": ["current_truth_reference"],
            "reduction_policy": {"reduction_allowed": False},
            "claim_boundary": {"allowed_claims": ["state_sync_findings_reported"]},
        },
        "acceptance_criteria": [],
        "work_plan": {"phases": []},
        "skill_routing": {
            "primary_family": "state_sync",
            "primary_skill": "obsidian-stage-transition",
            "support_skills": ["obsidian-reentry-read", "obsidian-artifact-lineage", "obsidian-claim-discipline"],
            "skills_considered": ["obsidian-stage-transition", "obsidian-reentry-read"],
            "skills_selected": ["obsidian-stage-transition", "obsidian-reentry-read", "obsidian-artifact-lineage", "obsidian-claim-discipline"],
            "skills_not_used": [],
            "required_skill_receipts": ["obsidian-stage-transition", "obsidian-reentry-read", "obsidian-artifact-lineage", "obsidian-claim-discipline"],
            "required_gates": ["state_sync_audit", "final_claim_guard"],
        },
        "evidence_contract": {"raw_evidence": [], "machine_readable": [], "human_readable": []},
        "gates": {},
        "final_claim_policy": {},
    }


if __name__ == "__main__":
    unittest.main()
