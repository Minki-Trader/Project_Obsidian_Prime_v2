from __future__ import annotations

import unittest

from foundation.control_plane.decision_lock import build_decision_lock
from foundation.control_plane.prompt_intake_classifier import classify_prompt
from foundation.control_plane.risk_vector_scan import scan_risk_vector


class DecisionLockTests(unittest.TestCase):
    def test_report_only_prompt_uses_safe_default(self) -> None:
        classification = classify_prompt("설명만 해줘")
        risk_scan = scan_risk_vector(classification)
        result = build_decision_lock(classification, risk_scan)

        self.assertEqual(result.mode, "assume_safe_default")
        self.assertTrue(result.assumptions["report_only"])
        self.assertFalse(result.assumptions["file_edit_allowed"])
        self.assertFalse(result.assumptions["execution_allowed"])

    def test_state_sync_conflict_requires_user_decision(self) -> None:
        classification = classify_prompt("상태 싱크 맞춰줘")
        risk_scan = scan_risk_vector(classification, current_truth_conflict=True)
        result = build_decision_lock(classification, risk_scan)

        self.assertEqual(result.mode, "ask_user")
        self.assertIn("canonical_current_truth", result.required_user_decisions)

    def test_cleanup_requires_destructive_permission(self) -> None:
        classification = classify_prompt("기존 작업물 아카이브로 이동해줘")
        risk_scan = scan_risk_vector(classification)
        result = build_decision_lock(classification, risk_scan)

        self.assertEqual(result.mode, "ask_user")
        self.assertIn("destructive_change_permission", result.required_user_decisions)


if __name__ == "__main__":
    unittest.main()
