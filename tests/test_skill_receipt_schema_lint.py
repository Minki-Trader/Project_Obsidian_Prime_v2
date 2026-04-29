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
                        "receipt_path": "missing.yaml",
                    }
                ],
                schema_path=Path("schema.yaml"),
                root=root,
            )

        self.assertEqual(result.status, "blocked")
        self.assertIn("skill_receipt_schema::unknown-skill::path_missing", {finding.check_id for finding in result.findings})

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


if __name__ == "__main__":
    unittest.main()
