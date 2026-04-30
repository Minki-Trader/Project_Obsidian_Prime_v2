from __future__ import annotations

import tempfile
import unittest
import subprocess
import sys
from pathlib import Path

from foundation.control_plane.final_claim_guard import guard_final_claims
from foundation.control_plane.kpi_contract_audit import KpiContract, audit_kpi_contract, required_files_for_structural_scout
from foundation.control_plane.ledger import ALPHA_LEDGER_COLUMNS, write_csv_rows
from foundation.control_plane.preflight_clarifier import analyze_prompt_for_clarification, format_clarification_for_user
from foundation.control_plane.scope_completion_gate import ScopeCountCheck, evaluate_scope_completion
from foundation.control_plane.skill_receipt_lint import SkillReceipt, lint_skill_receipts
from foundation.control_plane.work_packet_gate import evaluate_work_packet_closeout


class AgentControlGateTests(unittest.TestCase):
    def test_stage12_scope_shrink_pattern_blocks_full_completion(self) -> None:
        scope = evaluate_scope_completion(
            [
                ScopeCountCheck(
                    check_id="python_structural_results",
                    expected_count=20,
                    actual_count=20,
                    evidence_label="Python structural results",
                ),
                ScopeCountCheck(
                    check_id="mt5_validation_reports",
                    expected_count=20,
                    actual_count=1,
                    evidence_label="MT5 validation reports",
                ),
                ScopeCountCheck(
                    check_id="mt5_oos_reports",
                    expected_count=20,
                    actual_count=1,
                    evidence_label="MT5 OOS reports",
                ),
            ]
        )

        self.assertEqual(scope.status, "partial")
        self.assertTrue(scope.completed_forbidden)

        final_guard = guard_final_claims(
            requested_claims=("completed", "mt5_verification_complete"),
            audit_results=(scope,),
        )

        self.assertEqual(final_guard.status, "blocked")
        self.assertIn("completed", final_guard.forbidden_claims)
        self.assertIn("mt5_verification_complete", final_guard.forbidden_claims)

    def test_user_scope_reduction_quote_allows_reduced_scope_claim_only(self) -> None:
        scope = evaluate_scope_completion(
            [
                ScopeCountCheck(
                    check_id="mt5_validation_reports",
                    expected_count=20,
                    actual_count=1,
                    evidence_label="MT5 validation reports",
                    user_scope_reduction_quote="Only verify the top variant in MT5.",
                )
            ]
        )

        self.assertEqual(scope.status, "reduced_scope")

        reduced_claim = guard_final_claims(requested_claims=("completed_reduced_scope",), audit_results=(scope,))
        self.assertEqual(reduced_claim.status, "pass")

        full_claim = guard_final_claims(requested_claims=("full_verification_complete",), audit_results=(scope,))
        self.assertEqual(full_claim.status, "blocked")

    def test_skill_receipt_lint_blocks_missing_triggered_skill(self) -> None:
        result = lint_skill_receipts(
            required_skills=("obsidian-runtime-parity", "obsidian-run-evidence-system"),
            receipts=[
                SkillReceipt(
                    skill="obsidian-run-evidence-system",
                    triggered=True,
                    status="executed",
                    receipt_path="docs/agent_control/packets/unit/receipts/run_evidence.yaml",
                )
            ],
        )

        self.assertEqual(result.status, "blocked")
        self.assertTrue(result.completed_forbidden)
        self.assertIn("skill::obsidian-runtime-parity", {finding.check_id for finding in result.findings})

    def test_skill_receipt_lint_rejects_freeform_not_used_reason(self) -> None:
        result = lint_skill_receipts(
            required_skills=("obsidian-runtime-parity",),
            receipts=[
                SkillReceipt(
                    skill="obsidian-runtime-parity",
                    triggered=True,
                    status="not_used",
                    not_used_reason="handled implicitly",
                )
            ],
        )

        self.assertEqual(result.status, "blocked")
        self.assertIn("skill::obsidian-runtime-parity::not_used_reason", {finding.check_id for finding in result.findings})

    def test_kpi_contract_audit_blocks_missing_files_and_ledger_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_root = root / "stages" / "unit_stage" / "02_runs" / "unit_run"
            (run_root / "reports").mkdir(parents=True)
            (run_root / "run_manifest.json").write_text("{}", encoding="utf-8")
            (run_root / "summary.json").write_text("{}", encoding="utf-8")
            (run_root / "reports" / "result_summary.md").write_text("summary", encoding="utf-8")
            stage_ledger = root / "stage_run_ledger.csv"
            project_ledger = root / "alpha_run_ledger.csv"
            row = {
                "ledger_row_id": "unit_run__python",
                "stage_id": "unit_stage",
                "run_id": "unit_run",
                "subrun_id": "python",
                "parent_run_id": "unit_run",
                "record_view": "python",
                "tier_scope": "Tier A",
                "kpi_scope": "structural_scout",
                "scoreboard_lane": "structural_scout",
                "status": "completed",
                "judgment": "inconclusive",
                "path": "stages/unit_stage/02_runs/unit_run/summary.json",
                "primary_kpi": "signals=20",
                "guardrail_kpi": "",
                "external_verification_status": "not_applicable",
                "notes": "unit",
            }
            write_csv_rows(stage_ledger, ALPHA_LEDGER_COLUMNS, [row])
            write_csv_rows(project_ledger, ALPHA_LEDGER_COLUMNS, [row])

            result = audit_kpi_contract(
                KpiContract(
                    run_id="unit_run",
                    stage_id="unit_stage",
                    run_root=run_root,
                    required_files=required_files_for_structural_scout(),
                    stage_ledger_path=stage_ledger,
                    project_ledger_path=project_ledger,
                    expected_stage_ledger_rows=3,
                    expected_project_ledger_rows=3,
                )
            )

        self.assertEqual(result.status, "blocked")
        self.assertTrue(result.completed_forbidden)
        self.assertIn("kpi_required_files", {finding.check_id for finding in result.findings})
        self.assertIn("stage_ledger_rows", {finding.check_id for finding in result.findings})
        self.assertIn("project_ledger_rows", {finding.check_id for finding in result.findings})

    def test_work_packet_gate_combines_scope_skill_and_claim_guards(self) -> None:
        report = evaluate_work_packet_closeout(
            packet_id="st12_scope_shrink_regression",
            requested_claims=("completed",),
            scope_checks=[
                ScopeCountCheck(
                    check_id="mt5_validation_reports",
                    expected_count=20,
                    actual_count=1,
                    evidence_label="MT5 validation reports",
                )
            ],
            required_skills=("obsidian-runtime-parity",),
            skill_receipts=[],
        )

        self.assertEqual(report.status, "blocked")
        self.assertTrue(report.completed_forbidden)
        self.assertEqual(report.final_claim_guard.status, "blocked")

    def test_closeout_gate_cli_blocks_scope_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            csv_path = root / "variant_results.csv"
            csv_path.write_text("variant_id\nv01\nv02\n", encoding="utf-8")
            output_path = root / "gate.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "foundation.control_plane.closeout_gate",
                    "--packet-id",
                    "unit_packet",
                    "--requested-claim",
                    "completed",
                    "--scope-csv-rows",
                    "python_results",
                    "2",
                    str(csv_path),
                    "Python results",
                    "--scope-file-count",
                    "mt5_reports",
                    "2",
                    str(root / "reports" / "*.htm"),
                    "MT5 reports",
                    "--output-json",
                    str(output_path),
                ],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 2)
            payload = output_path.read_text(encoding="utf-8")
            self.assertIn('"status": "blocked"', payload)
            self.assertIn("mt5_reports", payload)

    def test_closeout_gate_cli_blocks_schema_and_receipt_content_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            work_packet = root / "work_packet.yaml"
            skill_receipts = root / "skill_receipts.json"
            schema = root / "skill_receipt_schema.yaml"
            output_path = root / "gate.json"
            work_packet.write_text(
                "\n".join(
                    [
                        "version: work_packet_schema_v2",
                        "packet_id: unit_packet",
                        "created_at_utc: '2026-04-29T00:00:00Z'",
                        "user_request: {requested_action: state_sync}",
                        "current_truth: {}",
                        "work_classification: {primary_family: state_sync}",
                        "risk_vector_scan: {risks: {state_sync_risk: high}}",
                        "interpreted_scope:",
                        "  work_families: [state_sync]",
                        "  target_surfaces: [docs_current_truth]",
                        "  scope_units: [document]",
                        "  execution_layers: [read_only]",
                        "  mutation_policy: {allowed: false}",
                        "  evidence_layers: [current_truth_reference]",
                        "  reduction_policy: {reduction_allowed: false}",
                        "  claim_boundary: {allowed_claims: [state_sync_findings_reported]}",
                        "acceptance_criteria: []",
                        "work_plan: {phases: []}",
                        "skill_routing:",
                        "  primary_family: state_sync",
                        "  primary_skill: obsidian-stage-transition",
                        "  support_skills: [obsidian-reentry-read, obsidian-artifact-lineage, obsidian-claim-discipline]",
                        "  skills_considered: [obsidian-stage-transition, obsidian-reentry-read]",
                        "  skills_selected: [obsidian-stage-transition, obsidian-reentry-read, obsidian-artifact-lineage, obsidian-claim-discipline]",
                        "  skills_not_used: []",
                        "  required_skill_receipts: [obsidian-stage-transition, obsidian-reentry-read, obsidian-artifact-lineage, obsidian-claim-discipline]",
                        "  required_gates: [work_packet_schema_lint, required_gate_coverage_audit, final_claim_guard]",
                        "evidence_contract: {raw_evidence: [], machine_readable: [], human_readable: []}",
                        "gates: {}",
                        "final_claim_policy: {}",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            skill_receipts.write_text(
                '{"receipts": [{"packet_id": "unit_packet", "skill": "obsidian-answer-clarity", "status": "executed"}]}',
                encoding="utf-8",
            )
            schema.write_text(
                "\n".join(
                    [
                        "schemas:",
                        "  obsidian-answer-clarity:",
                        "    required_fields:",
                        "      - packet_id",
                        "      - skill",
                        "      - status",
                        "      - plain_conclusion",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "foundation.control_plane.closeout_gate",
                    "--packet-id",
                    "unit_packet",
                    "--requested-claim",
                    "completed",
                    "--work-packet",
                    str(work_packet),
                    "--validate-work-packet-schema",
                    "--skill-receipt-json",
                    str(skill_receipts),
                    "--skill-receipt-schema",
                    str(schema),
                    "--output-json",
                    str(output_path),
                ],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)
            payload = output_path.read_text(encoding="utf-8")
            self.assertIn("work_packet_schema::v2::missing_top_level::decision_lock", payload)
            self.assertIn("skill_receipt_schema::obsidian-answer-clarity::missing_fields", payload)

    def test_closeout_gate_includes_required_gate_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            work_packet = root / "work_packet.yaml"
            output_path = root / "gate.json"
            work_packet.write_text(
                "\n".join(
                    [
                        "version: work_packet_schema_v2",
                        "packet_id: unit_packet",
                        "created_at_utc: '2026-04-29T00:00:00Z'",
                        "user_request: {requested_action: state_sync}",
                        "current_truth: {}",
                        "work_classification: {primary_family: state_sync}",
                        "risk_vector_scan:",
                        "  risks: {state_sync_risk: low}",
                        "  required_gates: [work_packet_schema_lint, required_gate_coverage_audit, final_claim_guard]",
                        "decision_lock: {mode: assume_safe_default, assumptions: {report_only: true}}",
                        "interpreted_scope:",
                        "  work_families: [state_sync]",
                        "  target_surfaces: [docs_current_truth]",
                        "  scope_units: [document]",
                        "  execution_layers: [read_only]",
                        "  mutation_policy: {allowed: false}",
                        "  evidence_layers: [current_truth_reference]",
                        "  reduction_policy: {reduction_allowed: false}",
                        "  claim_boundary: {allowed_claims: [state_sync_findings_reported]}",
                        "acceptance_criteria: []",
                        "work_plan: {phases: []}",
                        "skill_routing:",
                        "  primary_family: state_sync",
                        "  primary_skill: obsidian-stage-transition",
                        "  support_skills: [obsidian-reentry-read, obsidian-artifact-lineage, obsidian-claim-discipline]",
                        "  skills_considered: [obsidian-stage-transition, obsidian-reentry-read]",
                        "  skills_selected: [obsidian-stage-transition, obsidian-reentry-read, obsidian-artifact-lineage, obsidian-claim-discipline]",
                        "  skills_not_used: []",
                        "  required_skill_receipts: [obsidian-stage-transition, obsidian-reentry-read, obsidian-artifact-lineage, obsidian-claim-discipline]",
                        "  required_gates: [work_packet_schema_lint, required_gate_coverage_audit, final_claim_guard]",
                        "evidence_contract: {raw_evidence: [], machine_readable: [], human_readable: []}",
                        "gates:",
                        "  required: [work_packet_schema_lint, required_gate_coverage_audit, final_claim_guard]",
                        "  actual_status_source: gate.json",
                        "final_claim_policy: {}",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "foundation.control_plane.closeout_gate",
                    "--packet-id",
                    "unit_packet",
                    "--requested-claim",
                    "completed",
                    "--work-packet",
                    str(work_packet),
                    "--validate-work-packet-schema",
                    "--required-gate-coverage",
                    "--output-json",
                    str(output_path),
                ],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            payload = output_path.read_text(encoding="utf-8")
            self.assertIn('"audit_name": "required_gate_coverage_audit"', payload)
            self.assertIn('"status": "pass"', payload)

    def test_closeout_gate_accepts_extra_audit_json_for_required_gate_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            work_packet = root / "work_packet.yaml"
            extra_audit = root / "agent_control_contracts.json"
            output_path = root / "gate.json"
            work_packet.write_text(
                "\n".join(
                    [
                        "risk_vector_scan:",
                        "  required_gates: [agent_control_contracts, required_gate_coverage_audit, final_claim_guard]",
                        "gates: {}",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            extra_audit.write_text(
                '{"audit_name":"agent_control_contracts","status":"pass","findings":[],"allowed_claims":["contracts_ready"],"forbidden_claims":[]}',
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "foundation.control_plane.closeout_gate",
                    "--packet-id",
                    "unit_packet",
                    "--requested-claim",
                    "completed",
                    "--work-packet",
                    str(work_packet),
                    "--extra-audit-json",
                    str(extra_audit),
                    "--required-gate-coverage",
                    "--output-json",
                    str(output_path),
                ],
                cwd=Path(__file__).resolve().parents[1],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            payload = output_path.read_text(encoding="utf-8")
            self.assertIn('"audit_name": "agent_control_contracts"', payload)
            self.assertIn('"audit_name": "required_gate_coverage_audit"', payload)

    def test_preflight_clarifier_blocks_ambiguous_batch_verification_prompt(self) -> None:
        result = analyze_prompt_for_clarification("20개 정도 가설 세워서 검증까지 돌려봐")

        self.assertTrue(result.needs_clarification)
        self.assertTrue(result.blocked_until_answer)
        self.assertEqual(result.inferred_counts["requested_variants"], 20)
        self.assertIn("approximate_batch_count", result.risk_flags)
        self.assertIn("ambiguous_verification_layer", result.risk_flags)
        option_ids = {
            option.option_id
            for question in result.questions
            for option in question.options
        }
        self.assertIn("python_mt5_all", option_ids)
        self.assertIn("python_structural_only", option_ids)
        self.assertIn("python_all_mt5_top_k", option_ids)

    def test_preflight_clarifier_does_not_block_explicit_python_only_prompt(self) -> None:
        result = analyze_prompt_for_clarification("20개 Python structural scout만 돌려봐. MT5는 하지마")

        self.assertFalse(result.needs_clarification)
        self.assertFalse(result.blocked_until_answer)
        self.assertEqual(result.questions, ())

    def test_preflight_clarifier_blocks_unattended_batch_prompt(self) -> None:
        result = analyze_prompt_for_clarification("자는 동안 20개 가설 돌려봐")

        self.assertTrue(result.needs_clarification)
        self.assertIn("unattended_batch_work", result.risk_flags)
        self.assertIn("execution_layer_ambiguous", result.risk_flags)

    def test_preflight_clarifier_formats_user_facing_choices(self) -> None:
        result = analyze_prompt_for_clarification("20개 정도 가설 세워서 검증까지 돌려봐")
        message = format_clarification_for_user(result)

        self.assertIn("실행 전에 확인이 필요합니다.", message)
        self.assertIn("Python(파이썬)+MT5(메타트레이더5) 전체 검증", message)
        self.assertIn("효과(effect, 효과)", message)
        self.assertIn("completed_reduced_scope(축소 범위 완료)", message)


if __name__ == "__main__":
    unittest.main()
