from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from foundation.control_plane.ops_instruction_audit import audit_ops_instructions


ROOT = Path(__file__).resolve().parents[1]


class OpsInstructionAuditTests(unittest.TestCase):
    def test_repo_ops_instructions_are_stable(self) -> None:
        result = audit_ops_instructions(ROOT)

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])
        self.assertIn("ops_instructions_stable", result.allowed_claims)

    def test_frontier_topic_rotation_guard_is_wired(self) -> None:
        registry = yaml.safe_load((ROOT / "docs/agent_control/work_family_registry.yaml").read_text(encoding="utf-8-sig"))
        overlay = registry["trigger_overlays"]["frontier_topic_rotation_check"]

        self.assertEqual(overlay["status"], "active")
        self.assertTrue(overlay["active_by_default"])
        self.assertEqual(overlay["trigger_skill"], "obsidian-stage-transition")
        self.assertEqual(overlay["appends_required_gate"], "frontier_topic_rotation_check")

        expected_surfaces = [
            ROOT / "AGENTS.md",
            ROOT / "docs/policies/frontier_governance.md",
            ROOT / "docs/policies/agent_trigger_policy.md",
            ROOT / ".agents/skills/obsidian-stage-transition/SKILL.md",
        ]
        for path in expected_surfaces:
            self.assertIn("frontier_topic_rotation_check", path.read_text(encoding="utf-8-sig"))

        stage_transition = (ROOT / ".agents/skills/obsidian-stage-transition/SKILL.md").read_text(encoding="utf-8-sig")
        self.assertNotIn("five-stage Grok retrospective(5단계 Grok 중간 검토) is recorded", stage_transition)

    def test_goal_verification_profile_contract_is_wired(self) -> None:
        registry = yaml.safe_load((ROOT / "docs/agent_control/work_family_registry.yaml").read_text(encoding="utf-8-sig"))
        schema = yaml.safe_load((ROOT / "docs/agent_control/work_packet.schema.yaml").read_text(encoding="utf-8-sig"))

        self.assertIn("verification_profile_rule", registry["routing_contract"])
        self.assertIn("governance_evidence_balance_rule", registry["routing_contract"])
        self.assertIn("active_verification_over_procedure_rule", registry["routing_contract"])
        self.assertIn("runtime_probe_reluctance_rule", registry["routing_contract"])
        self.assertIn("verification_profiles", registry)
        self.assertIn("runtime_probe", registry["verification_profiles"]["profiles"])
        self.assertIn("authority_candidate", registry["verification_profiles"]["profiles"])
        self.assertIn("runtime_probe_reluctance_rule", registry["verification_profiles"])
        self.assertIn("verification_profile", schema["v2_1_required_top_level"])
        self.assertIn("verification_profile_ids_allowed", schema)

        expected_surfaces = [
            ROOT / "AGENTS.md",
            ROOT / "docs/policies/agent_trigger_policy.md",
            ROOT / "docs/agent_control/work_family_registry.yaml",
            ROOT / "docs/agent_control/work_packet.schema.yaml",
        ]
        for path in expected_surfaces:
            text = path.read_text(encoding="utf-8-sig")
            self.assertIn("verification_profile", text)
            self.assertIn("claim_surface", text)
            self.assertIn("trigger_source", text)
            self.assertIn("active verification", text)
            self.assertIn("runtime_probe", text)

    def test_frontier_extra_progressive_mix_depth_contract_is_wired(self) -> None:
        registry = yaml.safe_load((ROOT / "docs/agent_control/work_family_registry.yaml").read_text(encoding="utf-8-sig"))
        overlay = registry["trigger_overlays"]["frontier_extra_stage_due_check"]
        contract = overlay["progressive_mix_depth_contract"]

        self.assertEqual(overlay["status"], "active")
        self.assertTrue(overlay["active_by_default"])
        self.assertIn("frontier_extra_progressive_mix_depth_rule", registry["routing_contract"])
        self.assertEqual(contract["total_mt5_attempt_cap_default"], 24)
        self.assertEqual(contract["total_mt5_attempt_cap_with_invalid_or_block_recovery"], 30)
        self.assertIn("frontier_extra_mix_depth_lint", overlay["closeout_required_audits"])
        self.assertEqual([item["depth_id"] for item in contract["depth_sequence"]], ["2mix(2개 혼합)", "3mix(3개 혼합)", "4mix(4개 혼합)"])
        self.assertEqual(contract["selection_lane_limits"]["top_forward_pf_max_share"], 0.25)

        required_card_fields = set(contract["required_ingredient_card_fields"])
        for field in {
            "ingredient_card_id",
            "source_frontier_id",
            "source_run_id",
            "axis_tags",
            "artifact_path_hash",
            "salvage_value",
            "negative_memory",
            "do_not_repeat",
            "tier_scope",
            "claim_boundary",
            "selection_eligibility",
            "selection_lane_candidates",
        }:
            self.assertIn(field, required_card_fields)

        required_mix_fields = set(contract["required_mix_queue_receipt_fields"])
        for field in {
            "mix_id",
            "depth_id",
            "source_card_ids",
            "axis_tags",
            "selection_lanes",
            "novelty_delta",
            "near_duplicate_cluster_id",
            "sample_method",
            "selected_for_runtime",
            "selection_reason",
            "risk_notes",
            "claim_boundary",
        }:
            self.assertIn(field, required_mix_fields)

        required_depth_fields = set(contract["required_depth_receipt_fields"])
        for field in {
            "selection_lane_counts",
            "top_forward_pf_share",
            "runtime_substrate_count",
            "single_substrate_warning",
            "full_mix_materialized",
            "claim_effect",
            "claim_boundary",
        }:
            self.assertIn(field, required_depth_fields)

        required_attempt_fields = set(contract["required_attempt_receipt_fields"])
        for field in {
            "dataset_id",
            "feature_set_id",
            "label_id",
            "split_id",
            "split_contract",
            "source_identities",
            "parser_contract_version",
            "runtime_contract_version",
            "runtime_substrate_id",
            "compile_status",
            "tester_status",
            "runtime_status",
            "report_status",
            "onnx_hash",
            "ea_source_hash",
            "ea_binary_hash",
            "set_ini_hash",
            "feature_order_hash",
            "tester_identity",
            "report_hash",
            "trade_list_hash",
            "telemetry_hash",
            "claim_effect",
        }:
            self.assertIn(field, required_attempt_fields)

        runtime_contract = registry["runtime_evidence_contract"]
        self.assertIn("compile_not_runtime_rule", runtime_contract)
        for field in {"dataset_id", "onnx_hash", "ea_binary_hash", "tester_identity", "trade_list_hash", "telemetry_hash"}:
            self.assertIn(field, runtime_contract["standard_required_fields"])

        for path in [
            ROOT / "AGENTS.md",
            ROOT / "docs/policies/frontier_governance.md",
            ROOT / "docs/policies/agent_trigger_policy.md",
        ]:
            text = path.read_text(encoding="utf-8-sig")
            self.assertIn("progressive mix depth", text.lower())
            self.assertIn("top_forward_pf", text)
            self.assertIn("single_substrate_warning", text)
            self.assertIn("compile-only", text)
            self.assertIn("ingredient", text.lower())
            self.assertIn("mix queue", text.lower())

    def test_missing_primary_skill_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = _copy_ops_fixture(Path(temp_dir))
            path = root / "docs/agent_control/work_family_registry.yaml"
            payload = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
            payload["families"]["code_refactor"].pop("primary_skill")
            path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")

            result = audit_ops_instructions(root)

        self.assertEqual(result.status, "blocked")
        self.assertIn("ops_instruction::code_refactor::missing::primary_skill", {finding.check_id for finding in result.findings})

    def test_support_skill_without_receipt_schema_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = _copy_ops_fixture(Path(temp_dir))
            path = root / "docs/agent_control/skill_receipt_schema.yaml"
            payload = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
            payload["schemas"].pop("obsidian-code-quality")
            path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")

            result = audit_ops_instructions(root)

        self.assertEqual(result.status, "blocked")
        self.assertIn("ops_instruction::code_edit::obsidian-code-quality::missing_receipt_schema", {finding.check_id for finding in result.findings})

    def test_trigger_overlay_without_receipt_schema_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = _copy_ops_fixture(Path(temp_dir))
            path = root / "docs/agent_control/skill_receipt_schema.yaml"
            payload = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
            payload["schemas"].pop("obsidian-grok-collaboration")
            path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")

            result = audit_ops_instructions(root)

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "ops_instruction::trigger_overlay::grok_external_review::obsidian-grok-collaboration::missing_receipt_schema",
            {finding.check_id for finding in result.findings},
        )


def _copy_ops_fixture(root: Path) -> Path:
    shutil.copytree(
        ROOT / "docs/agent_control",
        root / "docs/agent_control",
        ignore=_ignore_generated_packet_artifacts,
    )
    shutil.copytree(ROOT / "docs/policies", root / "docs/policies")
    shutil.copytree(ROOT / ".agents", root / ".agents")
    shutil.copy2(ROOT / "AGENTS.md", root / "AGENTS.md")
    return root


def _ignore_generated_packet_artifacts(directory: str, names: list[str]) -> set[str]:
    if Path(directory).name == "agent_control":
        return {"grok_reviews", "packets"} & set(names)
    return set()


if __name__ == "__main__":
    unittest.main()
