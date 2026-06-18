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
        self.assertIn("archive_only_work_packet_schema_valid", result.allowed_claims)

    def test_new_packet_must_use_v2_1(self) -> None:
        packet = _v2_packet()
        packet["packet_lifecycle"] = "new_packet"

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "work_packet_schema::version::new_packet_requires_v2_1",
            {finding.check_id for finding in result.findings},
        )

    def test_v2_1_packet_requires_verification_profile(self) -> None:
        packet = _v2_1_packet()
        packet.pop("verification_profile")

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn("work_packet_schema::v2_1::missing_top_level::verification_profile", {finding.check_id for finding in result.findings})

    def test_v2_1_unknown_verification_profile_blocks(self) -> None:
        packet = _v2_1_packet()
        packet["verification_profile"]["profile_id"] = "full_verification_by_default"

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn("work_packet_schema::verification_profile::unknown_profile_id", {finding.check_id for finding in result.findings})

    def test_v2_1_gate_na_reason_must_be_structured(self) -> None:
        packet = _v2_1_packet()
        packet["verification_profile"]["gates_not_run_with_reason"] = ["runtime_evidence_gate"]

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn("work_packet_schema::verification_profile::gate_na_reason_not_mapping", {finding.check_id for finding in result.findings})

    def test_v2_1_mt5_execution_requires_runtime_profile(self) -> None:
        packet = _v2_1_packet()
        packet["verification_profile"]["profile_id"] = "design_only"
        packet["interpreted_scope"]["execution_layers"] = ["mt5_execution"]

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn("work_packet_schema::verification_profile::mt5_execution_requires_runtime_profile", {finding.check_id for finding in result.findings})

    def test_v2_1_authority_claim_requires_authority_profile_and_gates(self) -> None:
        packet = _v2_1_packet()
        packet["verification_profile"]["profile_id"] = "runtime_probe"
        packet["verification_profile"]["protected_claims"] = ["runtime_authority"]

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        finding_ids = {finding.check_id for finding in result.findings}
        self.assertIn("work_packet_schema::verification_profile::authority_claim_requires_authority_profile", finding_ids)

    def test_v2_1_authority_profile_passes_with_matching_gates(self) -> None:
        packet = _v2_1_packet()
        packet["verification_profile"]["profile_id"] = "authority_candidate"
        packet["verification_profile"]["protected_claims"] = ["runtime_authority"]
        packet["verification_profile"]["required_evidence"] = [
            "narrow_sufficient_runtime_probe",
            "MT5 Strategy Tester output",
            "deal rows",
            "report hash",
            *_runtime_identity_evidence(),
        ]
        packet["skill_routing"]["required_gates"] = [
            "runtime_evidence_gate",
            "kpi_contract_audit",
            "required_gate_coverage_audit",
            "final_claim_guard",
        ]

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])

    def test_v2_1_runtime_adjacent_claim_requires_runtime_profile(self) -> None:
        packet = _v2_1_packet()
        packet["verification_profile"]["profile_id"] = "static_contract"
        packet["verification_profile"]["protected_claims"] = ["materialization_ready"]

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn("work_packet_schema::verification_profile::runtime_adjacent_claim_requires_runtime_profile", {finding.check_id for finding in result.findings})

    def test_v2_1_runtime_profile_requires_probe_evidence(self) -> None:
        packet = _v2_1_packet()
        packet["verification_profile"]["profile_id"] = "runtime_probe"
        packet["verification_profile"]["protected_claims"] = ["runtime_economics_pass"]
        packet["verification_profile"]["required_evidence"] = ["owner response and local review notes"]
        packet["verification_profile"]["gates_not_run_with_reason"] = []
        packet["skill_routing"]["required_gates"] = [
            "runtime_evidence_gate",
            "kpi_contract_audit",
            "required_gate_coverage_audit",
            "final_claim_guard",
        ]

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn("work_packet_schema::verification_profile::runtime_claim_missing_probe_evidence", {finding.check_id for finding in result.findings})

    def test_v2_1_runtime_profile_requires_identity_proof_fields(self) -> None:
        packet = _v2_1_packet()
        packet["verification_profile"]["profile_id"] = "runtime_probe"
        packet["verification_profile"]["protected_claims"] = ["runtime_verified"]
        packet["verification_profile"]["required_evidence"] = ["MT5 Strategy Tester output", "deal rows", "report hash"]
        packet["verification_profile"]["gates_not_run_with_reason"] = []
        packet["skill_routing"]["required_gates"] = [
            "runtime_evidence_gate",
            "kpi_contract_audit",
            "required_gate_coverage_audit",
            "final_claim_guard",
        ]

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "work_packet_schema::verification_profile::runtime_claim_missing_identity_proof_fields",
            {finding.check_id for finding in result.findings},
        )

    def test_v2_1_compile_only_cannot_satisfy_runtime_profile(self) -> None:
        packet = _v2_1_packet()
        packet["verification_profile"]["profile_id"] = "runtime_probe"
        packet["verification_profile"]["protected_claims"] = ["runtime_verified"]
        packet["verification_profile"]["required_evidence"] = [
            "runtime_probe",
            "compile_status",
            *_runtime_identity_evidence(),
        ]
        packet["verification_profile"]["gates_not_run_with_reason"] = []
        packet["skill_routing"]["required_gates"] = [
            "runtime_evidence_gate",
            "kpi_contract_audit",
            "required_gate_coverage_audit",
            "final_claim_guard",
        ]

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "work_packet_schema::verification_profile::compile_only_not_runtime_evidence",
            {finding.check_id for finding in result.findings},
        )

    def test_v2_1_profile_extra_required_gates_are_enforced(self) -> None:
        packet = _v2_1_packet()
        packet["verification_profile"]["profile_id"] = "runtime_probe"
        packet["verification_profile"]["protected_claims"] = ["runtime_verified"]
        packet["verification_profile"]["required_evidence"] = ["MT5 Strategy Tester output"]
        packet["verification_profile"]["gates_not_run_with_reason"] = []
        packet["skill_routing"]["required_gates"] = [
            "runtime_evidence_gate",
            "final_claim_guard",
        ]

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn("work_packet_schema::verification_profile::missing_profile_required_gates", {finding.check_id for finding in result.findings})

    def test_v2_1_runtime_probe_cannot_be_cost_deferred_for_runtime_claim(self) -> None:
        packet = _v2_1_packet()
        packet["verification_profile"]["profile_id"] = "runtime_probe"
        packet["verification_profile"]["protected_claims"] = ["runtime_verified"]
        packet["verification_profile"]["required_evidence"] = ["MT5 Strategy Tester output"]
        packet["verification_profile"]["gates_not_run_with_reason"] = [
            {
                "gate": "runtime_evidence_gate",
                "reason_code": "too_expensive",
                "reason": "Runtime probe is expensive.",
                "claim_effect": "runtime claim still protected",
            }
        ]
        packet["skill_routing"]["required_gates"] = [
            "runtime_evidence_gate",
            "kpi_contract_audit",
            "required_gate_coverage_audit",
            "final_claim_guard",
        ]

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn("work_packet_schema::verification_profile::runtime_probe_cost_deferral_forbidden", {finding.check_id for finding in result.findings})

    def test_v2_1_runtime_probe_passes_with_narrow_evidence(self) -> None:
        packet = _v2_1_packet()
        packet["verification_profile"]["profile_id"] = "runtime_probe"
        packet["verification_profile"]["protected_claims"] = ["runtime_verified"]
        packet["verification_profile"]["required_evidence"] = [
            "narrow_sufficient_runtime_probe",
            "MT5 Strategy Tester output",
            "deal rows",
            "report hash",
            *_runtime_identity_evidence(),
        ]
        packet["verification_profile"]["gates_not_run_with_reason"] = []
        packet["skill_routing"]["required_gates"] = [
            "runtime_evidence_gate",
            "kpi_contract_audit",
            "required_gate_coverage_audit",
            "final_claim_guard",
        ]

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])

    def test_v2_1_broad_onnx_goal_requires_frontier_extra_due_check(self) -> None:
        packet = _v2_1_packet()
        packet["user_request"]["user_quote"] = "/goal onnx 개쩌는거 만들어줘"
        packet["user_request"]["requested_action"] = "broad ONNX frontier continuation"

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "work_packet_schema::frontier_extra::broad_onnx_missing_due_check",
            {finding.check_id for finding in result.findings},
        )

    def test_v2_1_broad_onnx_goal_passes_with_frontier_extra_due_check(self) -> None:
        packet = _v2_1_packet()
        packet["user_request"]["user_quote"] = "/goal onnx 개쩌는거 만들어줘"
        packet["user_request"]["requested_action"] = "broad ONNX frontier continuation"
        packet["skill_routing"]["required_gates"].append("frontier_extra_due_check")
        packet["skill_routing"]["required_gates"].append("frontier_five_stage_direction_synthesis")

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])

    def test_v2_1_frontier_open_requires_five_stage_direction_synthesis(self) -> None:
        packet = _v2_1_packet()
        packet["user_request"]["requested_action"] = "canonical frontier open"
        packet["skill_routing"]["required_gates"].append("frontier_topic_rotation_check")

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "work_packet_schema::frontier_direction::missing_five_stage_synthesis",
            {finding.check_id for finding in result.findings},
        )

    def test_v2_1_frontier_extra_closeout_requires_mix_and_runtime_gates(self) -> None:
        packet = _v2_1_packet()
        packet["user_request"]["user_quote"] = "stage_frontier_extra_E02 closeout"
        packet["user_request"]["requested_action"] = "Frontier Extra stage closeout"
        packet["verification_profile"]["profile_id"] = "stage_closeout"
        packet["verification_profile"]["protected_claims"] = ["stage_closeout"]
        packet["verification_profile"]["claim_surface"]["allowed_claims"] = ["stage_closeout"]
        packet["verification_profile"]["required_evidence"] = ["stage closeout receipt"]
        packet["skill_routing"]["required_gates"] = [
            "frontier_extra_due_check",
            "required_gate_coverage_audit",
            "final_claim_guard",
        ]
        packet["final_claim_policy"] = {
            "allowed_claims": ["stage_closeout"],
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
        }

        result = audit_work_packet_schema(packet)

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "work_packet_schema::frontier_extra::closeout_missing_required_gates",
            {finding.check_id for finding in result.findings},
        )


def _v1_packet() -> dict[str, object]:
    return {
        "packet_lifecycle": "archive_only",
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
        "packet_lifecycle": "archive_only",
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


def _v2_1_packet() -> dict[str, object]:
    packet = _v2_packet()
    packet["version"] = "work_packet_schema_v2_1"
    packet["packet_lifecycle"] = "new_packet"
    packet["verification_profile"] = {
        "profile_id": "static_contract",
        "claim_surface": {
            "allowed_claims": ["static_contract_checked"],
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "claim_boundary": "policy_schema_check_only",
        },
        "trigger_sources": ["explicit_user_scope"],
        "protected_claims": ["static_contract_checked"],
        "required_evidence": ["work_packet_schema_lint"],
        "gates_not_run_with_reason": [
            {
                "gate": "runtime_evidence_gate",
                "reason_code": "outside_claim_surface",
                "reason": "No runtime claim is made.",
                "claim_effect": "runtime claims forbidden",
            }
        ],
        "stop_conditions": ["policy/control-plane lint completed"],
    }
    packet["skill_routing"]["required_gates"] = ["work_packet_schema_lint", "final_claim_guard"]
    packet["final_claim_policy"] = {
        "allowed_claims": ["static_contract_checked"],
        "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
    }
    return packet


def _runtime_identity_evidence() -> list[str]:
    return [
        "dataset_id",
        "feature_set_id",
        "label_id",
        "split_id",
        "onnx_hash",
        "ea_source_hash",
        "ea_binary_hash",
        "set_ini_hash",
        "feature_order_hash",
        "tester_identity",
        "report_hash",
        "trade_list_hash",
        "telemetry_hash",
    ]


if __name__ == "__main__":
    unittest.main()
