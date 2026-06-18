from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from foundation.control_plane.skill_receipt_schema_lint import audit_skill_receipt_schemas


class SkillReceiptSchemaLintTests(unittest.TestCase):
    def test_executed_receipt_without_required_content_blocks(self) -> None:
        result = audit_skill_receipt_schemas(
            [
                {
                    "packet_id": "unit",
                    "skill": "obsidian-answer-clarity",
                    "status": "executed",
                }
            ],
            schema_path=Path("docs/agent_control/skill_receipt_schema.yaml"),
            root=Path(__file__).resolve().parents[1],
        )

        self.assertEqual(result.status, "blocked")
        self.assertTrue(result.completed_forbidden)
        self.assertIn("skill_receipt_schema::obsidian-answer-clarity::missing_fields", {finding.check_id for finding in result.findings})

    def test_complete_receipt_passes(self) -> None:
        result = audit_skill_receipt_schemas(
            [
                {
                    "packet_id": "unit",
                    "skill": "obsidian-answer-clarity",
                    "status": "executed",
                    "plain_conclusion": "pass",
                    "confirmed": ["schema checked"],
                    "not_yet_confirmed": ["none"],
                    "why_it_matters": "Keeps user-facing claim clear.",
                    "next_action": "none",
                    "forbidden_claims_avoided": ["runtime_authority"],
                }
            ],
            schema_path=Path("docs/agent_control/skill_receipt_schema.yaml"),
            root=Path(__file__).resolve().parents[1],
        )

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])

    def test_receipt_path_missing_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "schema.yaml").write_text(
                "schemas:\n  default:\n    required_fields:\n      - packet_id\n      - skill\n      - status\n",
                encoding="utf-8",
            )
            result = audit_skill_receipt_schemas(
                [
                    {
                        "packet_id": "unit",
                        "skill": "unknown-skill",
                        "status": "executed",
                        "path": "missing.yaml",
                    }
                ],
                schema_path=Path("schema.yaml"),
                root=root,
            )

        self.assertEqual(result.status, "blocked")
        self.assertIn("skill_receipt_schema::unknown-skill::path_missing", {finding.check_id for finding in result.findings})

    def test_small_grok_review_accepts_compact_receipt_fields(self) -> None:
        result = audit_skill_receipt_schemas(
            [
                {
                    "packet_id": "unit",
                    "skill": "obsidian-grok-collaboration",
                    "status": "executed",
                    "review_size": "small",
                    "trigger_reason": "user requested Grok",
                    "bounded_evidence": ["one narrow snapshot"],
                    "advice_classification": {"accepted": ["compact"]},
                    "claim_boundary": "no authority claims",
                    "final_codex_direction": "continue locally",
                }
            ],
            schema_path=Path("docs/agent_control/skill_receipt_schema.yaml"),
            root=Path(__file__).resolve().parents[1],
        )

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])

    def test_generic_compact_receipt_requires_gate_na_boundary(self) -> None:
        result = audit_skill_receipt_schemas(
            [
                {
                    "packet_id": "unit",
                    "skill": "obsidian-answer-clarity",
                    "status": "executed",
                    "receipt_mode": "compact",
                    "source_current_truth_docs": ["docs/workspace/workspace_state.yaml"],
                    "evidence_used": ["status only"],
                    "claim_boundary": "no completion claim",
                    "forbidden_claims": ["completed"],
                }
            ],
            schema_path=Path("docs/agent_control/skill_receipt_schema.yaml"),
            root=Path(__file__).resolve().parents[1],
        )

        self.assertEqual(result.status, "blocked")
        self.assertIn("skill_receipt_schema::obsidian-answer-clarity::missing_fields", {finding.check_id for finding in result.findings})

    def test_generic_compact_receipt_passes_with_gate_na_boundary(self) -> None:
        result = audit_skill_receipt_schemas(
            [
                {
                    "packet_id": "unit",
                    "skill": "obsidian-answer-clarity",
                    "status": "executed",
                    "receipt_mode": "compact",
                    "source_current_truth_docs": ["docs/workspace/workspace_state.yaml"],
                    "evidence_used": ["status only"],
                    "claim_boundary": "no completion claim",
                    "gates_not_run_with_reason": [
                        {
                            "gate": "runtime_evidence_gate",
                            "reason_code": "outside_claim_surface",
                            "reason": "No runtime claim is made.",
                            "claim_effect": "runtime claims forbidden",
                        }
                    ],
                    "forbidden_claims": ["completed", "runtime_authority"],
                }
            ],
            schema_path=Path("docs/agent_control/skill_receipt_schema.yaml"),
            root=Path(__file__).resolve().parents[1],
        )

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])

    def test_forbidden_claim_conflict_blocks(self) -> None:
        result = audit_skill_receipt_schemas(
            [
                {
                    "packet_id": "unit",
                    "skill": "unknown-skill",
                    "status": "executed",
                    "forbidden_claims": ["completed"],
                }
            ],
            schema_path=Path("docs/agent_control/skill_receipt_schema.yaml"),
            root=Path(__file__).resolve().parents[1],
            requested_claims=("completed",),
        )

        self.assertEqual(result.status, "blocked")
        self.assertIn("skill_receipt_schema::unknown-skill::claim_conflict", {finding.check_id for finding in result.findings})

    def test_required_task_force_review_not_called_blocks(self) -> None:
        result = audit_skill_receipt_schemas(
            [
                {
                    "packet_id": "unit",
                    "skill": "obsidian-task-force-review",
                    "status": "not_called",
                    "review_requirement": "active_goal_required",
                    "actual_subagent_calls": "not_called",
                }
            ],
            schema_path=Path("docs/agent_control/skill_receipt_schema.yaml"),
            root=Path(__file__).resolve().parents[1],
            requested_claims=("reviewed",),
        )

        self.assertEqual(result.status, "blocked")
        check_ids = {finding.check_id for finding in result.findings}
        self.assertIn("skill_receipt_schema::obsidian-task-force-review::required_review_not_called", check_ids)
        self.assertIn("skill_receipt_schema::obsidian-task-force-review::missing_actual_subagent_calls", check_ids)

    def test_optional_task_force_not_called_cannot_support_review_claim(self) -> None:
        result = audit_skill_receipt_schemas(
            [
                {
                    "packet_id": "unit",
                    "skill": "obsidian-task-force-review",
                    "status": "optional_not_called_no_task_force_claim",
                    "review_requirement": "optional",
                    "actual_subagent_calls": "not_called",
                }
            ],
            schema_path=Path("docs/agent_control/skill_receipt_schema.yaml"),
            root=Path(__file__).resolve().parents[1],
            requested_claims=("task_force_reviewed",),
        )

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "skill_receipt_schema::obsidian-task-force-review::optional_not_called_claim_conflict",
            {finding.check_id for finding in result.findings},
        )

    def test_required_task_force_review_with_actual_calls_passes_schema_lint(self) -> None:
        result = audit_skill_receipt_schemas(
            [
                {
                    "packet_id": "unit",
                    "skill": "obsidian-task-force-review",
                    "status": "executed",
                    "trigger_reason": "policy governance",
                    "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
                    "agents_used": ["agent_01_system_governor", "agent_04_evidence_control_plane"],
                    "actual_subagent_calls": [
                        {
                            "roster_agent_id": "agent_01_system_governor",
                            "spawned_agent_id": "agent-a",
                            "tool_name": "multi_agent_v1.spawn_agent",
                            "result_status": "completed",
                            "opinion_classification": "accepted",
                        },
                        {
                            "roster_agent_id": "agent_04_evidence_control_plane",
                            "spawned_agent_id": "agent-b",
                            "tool_name": "multi_agent_v1.spawn_agent",
                            "result_status": "completed",
                            "opinion_classification": "needs_local_verification",
                        },
                    ],
                    "review_requirement": "codex_task_force_review_packet",
                    "model_policy": "highest_available_xhigh",
                    "bounded_evidence": ["policy diff"],
                    "advice_classification": {"accepted": ["tighten required gate"]},
                    "local_verification": "schema lint",
                    "final_codex_direction": "apply strict block",
                    "forbidden_claim_check": "no authority claims",
                }
            ],
            schema_path=Path("docs/agent_control/skill_receipt_schema.yaml"),
            root=Path(__file__).resolve().parents[1],
        )

        self.assertEqual(result.status, "pass", [finding.to_dict() for finding in result.findings])

    def test_required_task_force_review_call_records_require_spawn_tool_and_opinion(self) -> None:
        result = audit_skill_receipt_schemas(
            [
                {
                    "packet_id": "unit",
                    "skill": "obsidian-task-force-review",
                    "status": "executed",
                    "trigger_reason": "policy governance",
                    "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
                    "agents_used": ["agent_01_system_governor"],
                    "actual_subagent_calls": [
                        {
                            "roster_agent_id": "agent_01_system_governor",
                            "spawned_agent_id": "agent-a",
                            "tool_name": "notes_only",
                            "result_status": "completed",
                            "opinion_classification": "rubber_stamp",
                        }
                    ],
                    "review_requirement": "codex_task_force_review_packet",
                    "model_policy": "highest_available_xhigh",
                    "bounded_evidence": ["policy diff"],
                    "advice_classification": {"accepted": ["tighten required gate"]},
                    "local_verification": "schema lint",
                    "final_codex_direction": "apply strict block",
                    "forbidden_claim_check": "no authority claims",
                }
            ],
            schema_path=Path("docs/agent_control/skill_receipt_schema.yaml"),
            root=Path(__file__).resolve().parents[1],
        )

        self.assertEqual(result.status, "blocked")
        check_ids = {finding.check_id for finding in result.findings}
        self.assertIn("skill_receipt_schema::obsidian-task-force-review::actual_subagent_call_wrong_tool", check_ids)
        self.assertIn("skill_receipt_schema::obsidian-task-force-review::actual_subagent_call_bad_opinion_classification", check_ids)

    def test_required_task_force_review_all_agents_requires_reason(self) -> None:
        calls = [
            {
                "roster_agent_id": f"agent_{index:02d}_role",
                "spawned_agent_id": f"agent-{index}",
                "tool_name": "multi_agent_v1.spawn_agent",
                "result_status": "completed",
                "opinion_classification": "accepted",
            }
            for index in range(1, 9)
        ]
        result = audit_skill_receipt_schemas(
            [
                {
                    "packet_id": "unit",
                    "skill": "obsidian-task-force-review",
                    "status": "executed",
                    "trigger_reason": "policy governance",
                    "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
                    "agents_used": [call["roster_agent_id"] for call in calls],
                    "actual_subagent_calls": calls,
                    "review_requirement": "codex_task_force_review_packet",
                    "model_policy": "highest_available_xhigh",
                    "bounded_evidence": ["policy diff"],
                    "advice_classification": {"accepted": ["tighten required gate"]},
                    "local_verification": "schema lint",
                    "final_codex_direction": "apply strict block",
                    "forbidden_claim_check": "no authority claims",
                }
            ],
            schema_path=Path("docs/agent_control/skill_receipt_schema.yaml"),
            root=Path(__file__).resolve().parents[1],
        )

        self.assertEqual(result.status, "blocked")
        self.assertIn(
            "skill_receipt_schema::obsidian-task-force-review::full_roster_call_missing_reason",
            {finding.check_id for finding in result.findings},
        )


if __name__ == "__main__":
    unittest.main()
