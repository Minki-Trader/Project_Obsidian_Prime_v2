from __future__ import annotations

import unittest

from foundation.control_plane.preflight_clarifier import analyze_experiment_runtime_clarification
from foundation.control_plane.prompt_intake_classifier import classify_prompt


class PromptIntakeClassifierTests(unittest.TestCase):
    def test_report_only_prompt_stays_information_only(self) -> None:
        result = classify_prompt("설명만 해줘")

        self.assertEqual(result.primary_family, "information_only")
        self.assertFalse(result.mutation_intent)
        self.assertFalse(result.execution_intent)

    def test_state_sync_prompt_routes_to_state_sync(self) -> None:
        result = classify_prompt("상태 싱크 맞춰줘")

        self.assertEqual(result.primary_family, "state_sync")
        self.assertIn("docs_current_truth", result.touched_surfaces)

    def test_code_structure_prompt_routes_to_code_refactor(self) -> None:
        result = classify_prompt("코드 분산 정리해줘")

        self.assertEqual(result.primary_family, "code_refactor")
        self.assertIn("foundation_code", result.touched_surfaces)
        self.assertIn("pipelines", result.touched_surfaces)

    def test_runtime_prompt_routes_to_runtime_backtest(self) -> None:
        result = classify_prompt("MT5까지 돌려줘")

        self.assertEqual(result.primary_family, "runtime_backtest")
        self.assertIn("mt5_runtime", result.touched_surfaces)
        self.assertTrue(result.execution_intent)

    def test_kpi_prompt_routes_to_kpi_evidence(self) -> None:
        result = classify_prompt("KPI 포맷 통일해줘")

        self.assertEqual(result.primary_family, "kpi_evidence")
        self.assertIn("kpi_ledgers", result.touched_surfaces)
        self.assertTrue(result.mutation_intent)

    def test_stage12_batch_prompt_still_uses_experiment_runtime_clarifier(self) -> None:
        result = analyze_experiment_runtime_clarification("20개 정도 가설 세워서 검증까지 돌려봐")

        self.assertTrue(result.needs_clarification)
        self.assertTrue(result.blocked_until_answer)
        self.assertEqual(result.inferred_counts["requested_variants"], 20)
        option_ids = {option.option_id for question in result.questions for option in question.options}
        self.assertIn("python_mt5_all", option_ids)
        self.assertIn("python_structural_only", option_ids)
        self.assertIn("python_all_mt5_top_k", option_ids)


if __name__ == "__main__":
    unittest.main()
