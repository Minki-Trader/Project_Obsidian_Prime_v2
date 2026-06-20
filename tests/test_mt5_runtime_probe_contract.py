from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from foundation.control_plane.mt5_runtime_probe_contract import (
    STANDARD_RUNTIME_PROBE_PROFILE,
    audit_mt5_runtime_probe_contract,
    standard_split_specs,
)
from foundation.mt5.terminal_runner import run_mt5_tester


def _attempt(
    name: str,
    split: str,
    from_date: str,
    to_date: str,
    *,
    profile: str = STANDARD_RUNTIME_PROBE_PROFILE,
    surface_scope: str = "full_period_deterministic",
    source_artifact_role: str = "full_runtime_surface",
    completion_claim_allowed: bool = True,
    standard_period_covered: bool = True,
):
    return {
        "attempt_name": name,
        "tier": "Tier A+B",
        "split": split,
        "probe_profile": profile,
        "runtime_surface_contract": {
            "surface_scope": surface_scope,
            "source_artifact_role": source_artifact_role,
            "completion_claim_allowed": completion_claim_allowed,
            "standard_period_covered": standard_period_covered,
        },
        "ini": {
            "tester": {
                "Symbol": "US100",
                "Period": "M5",
                "Model": 4,
                "Deposit": 500,
                "Leverage": "1:100",
                "UseLocal": 1,
                "UseRemote": 0,
                "UseCloud": 0,
                "ReplaceReport": 1,
                "ShutdownTerminal": 1,
                "FromDate": from_date,
                "ToDate": to_date,
                "Report": f"Project_Obsidian_Prime_v2_unit_{name}",
            }
        },
    }


def _completed_report(attempt):
    tester = attempt["ini"]["tester"]
    return {
        "attempt_name": attempt["attempt_name"],
        "split": attempt["split"],
        "report_name": tester["Report"],
        "status": "completed",
    }


def _execution_result(attempt, *, portable: bool = True):
    command = ["terminal64.exe"]
    if portable:
        command.append("/portable")
    command.append(f"/config:{attempt['attempt_name']}.ini")
    return {
        "attempt_name": attempt["attempt_name"],
        "tier": attempt["tier"],
        "split": attempt["split"],
        "status": "completed",
        "command": command,
        "mt5_runtime_probe_contract": {
            "portable_arg_present": portable,
        },
    }


class Mt5RuntimeProbeContractTests(unittest.TestCase):
    def test_standard_contract_uses_validation_and_oos_pair(self) -> None:
        self.assertEqual(
            standard_split_specs(),
            {
                "validation_is": ("validation", "2025.01.02", "2025.10.01"),
                "oos": ("oos", "2025.10.01", "2026.04.13"),
            },
        )

    def test_runtime_probe_completed_passes_only_with_both_standard_splits_and_reports(self) -> None:
        validation = _attempt("routed_validation_is", "validation_is", "2025.01.02", "2025.10.01")
        oos = _attempt("routed_oos", "oos", "2025.10.01", "2026.04.13")

        result = audit_mt5_runtime_probe_contract(
            {
                "attempts": [validation, oos],
                "execution_results": [_execution_result(validation), _execution_result(oos)],
                "strategy_tester_reports": [_completed_report(validation), _completed_report(oos)],
            },
            requested_claims=("runtime_probe_completed",),
        )

        self.assertEqual(result.status, "pass", result.to_dict())
        self.assertEqual(result.audit_name, "mt5_runtime_probe_contract_audit")
        self.assertIn("runtime_probe_completed", result.allowed_claims)
        self.assertFalse(result.completed_forbidden)

    def test_runtime_probe_completed_blocks_missing_oos(self) -> None:
        validation = _attempt("routed_validation_is", "validation_is", "2025.01.02", "2025.10.01")

        result = audit_mt5_runtime_probe_contract(
            {
                "attempts": [validation],
                "execution_results": [_execution_result(validation)],
                "strategy_tester_reports": [_completed_report(validation)],
            },
            requested_claims=("runtime_probe_completed",),
        )

        self.assertEqual(result.status, "blocked")
        self.assertTrue(result.completed_forbidden)
        self.assertTrue(any(finding.check_id.endswith("missing_required_split") for finding in result.findings))

    def test_runtime_probe_completed_blocks_noncanonical_period(self) -> None:
        validation = _attempt("routed_validation_is", "validation_is", "2025.01.03", "2025.02.07")
        oos = _attempt("routed_oos", "oos", "2025.10.01", "2026.04.13")

        result = audit_mt5_runtime_probe_contract(
            {
                "attempts": [validation, oos],
                "execution_results": [_execution_result(validation), _execution_result(oos)],
                "strategy_tester_reports": [_completed_report(validation), _completed_report(oos)],
            },
            requested_claims=("runtime_probe_completed",),
        )

        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(finding.check_id.endswith("attempt_contract_mismatch") for finding in result.findings))

    def test_exception_profile_cannot_support_completed_claim(self) -> None:
        smoke = _attempt(
            "debug_slice",
            "validation_is",
            "2025.01.03",
            "2025.02.07",
            profile="specific_period_probe",
        )

        result = audit_mt5_runtime_probe_contract(
            {
                "attempts": [smoke],
                "execution_results": [_execution_result(smoke)],
                "strategy_tester_reports": [_completed_report(smoke)],
            },
            requested_claims=("runtime_probe_completed",),
        )

        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(finding.check_id.endswith("exception_profile_for_completion_claim") for finding in result.findings))

    def test_runtime_probe_completed_blocks_nonportable_execution(self) -> None:
        validation = _attempt("routed_validation_is", "validation_is", "2025.01.02", "2025.10.01")
        oos = _attempt("routed_oos", "oos", "2025.10.01", "2026.04.13")

        result = audit_mt5_runtime_probe_contract(
            {
                "attempts": [validation, oos],
                "execution_results": [_execution_result(validation, portable=False), _execution_result(oos)],
                "strategy_tester_reports": [_completed_report(validation), _completed_report(oos)],
            },
            requested_claims=("runtime_probe_completed",),
        )

        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(finding.check_id.endswith("nonportable_execution") for finding in result.findings))

    def test_runtime_probe_completed_blocks_sample_surface_even_with_reports(self) -> None:
        validation = _attempt(
            "routed_validation_is",
            "validation_is",
            "2025.01.02",
            "2025.10.01",
            surface_scope="sparse_diagnostic_sample",
            source_artifact_role="proxy_score_sample",
            completion_claim_allowed=False,
            standard_period_covered=False,
        )
        oos = _attempt(
            "routed_oos",
            "oos",
            "2025.10.01",
            "2026.04.13",
            surface_scope="sparse_diagnostic_sample",
            source_artifact_role="proxy_score_sample",
            completion_claim_allowed=False,
            standard_period_covered=False,
        )

        result = audit_mt5_runtime_probe_contract(
            {
                "attempts": [validation, oos],
                "execution_results": [_execution_result(validation), _execution_result(oos)],
                "strategy_tester_reports": [_completed_report(validation), _completed_report(oos)],
            },
            requested_claims=("runtime_probe_completed",),
        )

        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(finding.check_id.endswith("sample_source_forbids_completion") for finding in result.findings))
        self.assertTrue(any(finding.check_id.endswith("surface_contract_forbids_completion") for finding in result.findings))

    def test_runtime_probe_observation_blocks_standard_attempt_with_partial_surface(self) -> None:
        oos = _attempt(
            "routed_oos",
            "oos",
            "2025.10.01",
            "2026.04.13",
            surface_scope="partial_period_deterministic_surface",
            source_artifact_role="deterministic_surface_with_missing_tail",
            completion_claim_allowed=False,
            standard_period_covered=False,
        )

        result = audit_mt5_runtime_probe_contract(
            {
                "attempts": [oos],
                "execution_results": [_execution_result(oos)],
                "strategy_tester_reports": [_completed_report(oos)],
            },
            requested_claims=("runtime_probe_observation",),
        )

        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(finding.check_id.endswith("surface_contract_forbids_standard_attempt") for finding in result.findings))

    def test_runtime_probe_completed_blocks_missing_surface_contract(self) -> None:
        validation = _attempt("routed_validation_is", "validation_is", "2025.01.02", "2025.10.01")
        oos = _attempt("routed_oos", "oos", "2025.10.01", "2026.04.13")
        validation.pop("runtime_surface_contract")
        oos.pop("runtime_surface_contract")

        result = audit_mt5_runtime_probe_contract(
            {
                "attempts": [validation, oos],
                "execution_results": [_execution_result(validation), _execution_result(oos)],
                "strategy_tester_reports": [_completed_report(validation), _completed_report(oos)],
            },
            requested_claims=("runtime_probe_completed",),
        )

        self.assertEqual(result.status, "blocked")
        self.assertTrue(any(finding.check_id.endswith("missing_runtime_surface_contract") for finding in result.findings))

    def test_nested_execution_payload_is_accepted(self) -> None:
        validation = _attempt("routed_validation_is", "validation_is", "2025.01.02", "2025.10.01")
        oos = _attempt("routed_oos", "oos", "2025.10.01", "2026.04.13")

        result = audit_mt5_runtime_probe_contract(
            {
                "attempts": [validation, oos],
                "execution": {
                    "execution_results": [_execution_result(validation), _execution_result(oos)],
                    "strategy_tester_reports": [_completed_report(validation), _completed_report(oos)],
                },
            },
            requested_claims=("runtime_probe_completed",),
        )

        self.assertEqual(result.status, "pass", result.to_dict())

    def test_packet_wrapper_mt5_result_payload_is_accepted(self) -> None:
        validation = _attempt("routed_validation_is", "validation_is", "2025.01.02", "2025.10.01")
        oos = _attempt("routed_oos", "oos", "2025.10.01", "2026.04.13")

        result = audit_mt5_runtime_probe_contract(
            {
                "packet_id": "unit_packet_wrapper",
                "mt5_result": {
                    "attempts": [validation, oos],
                    "execution_results": [_execution_result(validation), _execution_result(oos)],
                    "strategy_tester_reports": [_completed_report(validation), _completed_report(oos)],
                },
            },
            requested_claims=("runtime_probe_completed",),
        )

        self.assertEqual(result.status, "pass", result.to_dict())

    def test_packet_wrapper_prefers_mt5_result_over_prepared_attempts(self) -> None:
        validation = _attempt("routed_validation_is", "validation_is", "2025.01.02", "2025.10.01")

        result = audit_mt5_runtime_probe_contract(
            {
                "packet_id": "unit_packet_wrapper",
                "prepared": {"attempts": [validation]},
                "mt5_result": {
                    "attempts": [validation],
                    "execution_results": [_execution_result(validation)],
                    "strategy_tester_reports": [_completed_report(validation)],
                },
            },
            requested_claims=("runtime_probe_observation",),
        )

        self.assertEqual(result.status, "pass", result.to_dict())
        self.assertEqual(result.to_dict()["counts"]["attempts"], 1)

    def test_mt5_runner_adds_portable_arg_before_config(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ini_path = root / "tester.ini"
            ini_path.write_text("[Tester]\n", encoding="utf-8")
            missing_terminal = root / "terminal64.exe"

            result = run_mt5_tester(missing_terminal, ini_path)

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["blocker"], "terminal_missing")
        self.assertIn("/portable", result["command"])
        self.assertTrue(result["mt5_runtime_probe_contract"]["portable_arg_present"])


if __name__ == "__main__":
    unittest.main()
