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


def _copy_ops_fixture(root: Path) -> Path:
    shutil.copytree(ROOT / "docs/agent_control", root / "docs/agent_control")
    shutil.copytree(ROOT / "docs/policies", root / "docs/policies")
    shutil.copytree(ROOT / ".agents", root / ".agents")
    shutil.copy2(ROOT / "AGENTS.md", root / "AGENTS.md")
    return root


if __name__ == "__main__":
    unittest.main()
