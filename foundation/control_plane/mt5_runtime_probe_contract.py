from __future__ import annotations

import argparse
import json
from collections.abc import Sequence as SequenceABC
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.audit_result import AuditFinding, AuditResult
from foundation.control_plane.ledger import io_path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONTRACT_PATH = ROOT / "foundation" / "config" / "mt5_runtime_probe_contract.yaml"
STANDARD_RUNTIME_PROBE_PROFILE = "standard_runtime_probe"
RUNTIME_COMPLETION_CLAIMS = frozenset(
    {
        "runtime_probe_completed",
        "mt5_verification_complete",
        "runtime_verified",
        "runtime_authority",
        "operating_promotion",
        "live_readiness",
        "goal_achieve",
    }
)


def load_contract(path: Path | str | None = None) -> dict[str, Any]:
    contract_path = Path(path) if path is not None else DEFAULT_CONTRACT_PATH
    payload = yaml.safe_load(io_path(contract_path).read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"MT5 runtime probe contract must be a mapping: {contract_path}")
    return payload


def canonical_periods(contract: Mapping[str, Any] | None = None) -> dict[str, dict[str, str]]:
    payload = contract or load_contract()
    raw = payload.get("canonical_periods", {})
    if not isinstance(raw, Mapping):
        raise ValueError("canonical_periods must be a mapping")
    periods: dict[str, dict[str, str]] = {}
    for split, spec in raw.items():
        if not isinstance(spec, Mapping):
            raise ValueError(f"canonical_periods.{split} must be a mapping")
        periods[str(split)] = {
            "source_split": str(spec["source_split"]),
            "from_date": str(spec["from_date"]),
            "to_date": str(spec["to_date"]),
        }
    return periods


def standard_split_specs(contract: Mapping[str, Any] | None = None) -> dict[str, tuple[str, str, str]]:
    return {
        split: (spec["source_split"], spec["from_date"], spec["to_date"])
        for split, spec in canonical_periods(contract).items()
    }


def standard_period(split: str, contract: Mapping[str, Any] | None = None) -> tuple[str, str]:
    spec = canonical_periods(contract)[split]
    return spec["from_date"], spec["to_date"]


def required_splits(contract: Mapping[str, Any] | None = None) -> tuple[str, ...]:
    payload = contract or load_contract()
    completion = payload.get("completion", {})
    values = completion.get("required_splits", ("validation_is", "oos")) if isinstance(completion, Mapping) else ()
    return tuple(str(value) for value in values)


def exception_profiles(contract: Mapping[str, Any] | None = None) -> frozenset[str]:
    payload = contract or load_contract()
    raw = payload.get("exception_profiles", {})
    return frozenset(str(key) for key in raw.keys()) if isinstance(raw, Mapping) else frozenset()


def required_terminal_args(contract: Mapping[str, Any] | None = None) -> tuple[str, ...]:
    payload = contract or load_contract()
    execution = payload.get("execution", {})
    args = execution.get("required_terminal_args", ("/portable",)) if isinstance(execution, Mapping) else ("/portable",)
    return tuple(str(arg) for arg in args)


def ensure_required_terminal_args(
    terminal_extra_args: Sequence[str] | None,
    contract: Mapping[str, Any] | None = None,
) -> tuple[str, ...]:
    existing = tuple(str(arg) for arg in (terminal_extra_args or ()))
    existing_lower = {arg.lower() for arg in existing}
    missing = tuple(arg for arg in required_terminal_args(contract) if arg.lower() not in existing_lower)
    return (*missing, *existing)


def tester_defaults(contract: Mapping[str, Any] | None = None) -> dict[str, str]:
    payload = contract or load_contract()
    execution = payload.get("execution", {})
    tester = execution.get("tester", {}) if isinstance(execution, Mapping) else {}
    if not isinstance(tester, Mapping):
        return {}
    return {str(key): _canonical_value(value) for key, value in tester.items()}


def _canonical_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return f"{float(value):.12g}"
    return str(value)


def profile_for_attempt(attempt: Mapping[str, Any]) -> str:
    if attempt.get("probe_profile"):
        return str(attempt["probe_profile"])
    metadata = attempt.get("mt5_runtime_probe_contract")
    if isinstance(metadata, Mapping) and metadata.get("profile"):
        return str(metadata["profile"])
    return STANDARD_RUNTIME_PROBE_PROFILE


def _attempt_tester(attempt: Mapping[str, Any]) -> Mapping[str, Any]:
    ini = attempt.get("ini", {})
    if isinstance(ini, Mapping):
        tester = ini.get("tester", {})
        if isinstance(tester, Mapping):
            return tester
    return {}


def validate_attempt_contract(
    *,
    split: str,
    from_date: str,
    to_date: str,
    tester: Mapping[str, Any] | None = None,
    probe_profile: str = STANDARD_RUNTIME_PROBE_PROFILE,
    contract: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    payload = contract or load_contract()
    periods = canonical_periods(payload)
    profile = str(probe_profile or STANDARD_RUNTIME_PROBE_PROFILE)
    result: dict[str, Any] = {
        "version": str(payload.get("version", "mt5_runtime_probe_contract_v1")),
        "profile": profile,
        "split": split,
        "from_date": from_date,
        "to_date": to_date,
        "runtime_probe_completed_claim_allowed": False,
        "status": "blocked",
    }
    if profile in exception_profiles(payload):
        result.update(
            {
                "status": "reduced_scope",
                "claim_effect": "exception_profile_forbids_runtime_probe_completed",
            }
        )
        return result
    if profile != STANDARD_RUNTIME_PROBE_PROFILE:
        result["claim_effect"] = "unknown_profile_forbids_runtime_probe_completed"
        return result
    expected = periods.get(split)
    if expected is None:
        result["claim_effect"] = "unknown_split_for_standard_runtime_probe"
        return result
    result["expected_from_date"] = expected["from_date"]
    result["expected_to_date"] = expected["to_date"]
    if from_date != expected["from_date"] or to_date != expected["to_date"]:
        result["claim_effect"] = "noncanonical_period_forbids_runtime_probe_completed"
        return result
    mismatches = {}
    for key, expected_value in tester_defaults(payload).items():
        if tester is None or key not in tester:
            mismatches[key] = {"expected": expected_value, "actual": None}
            continue
        actual = _canonical_value(tester[key])
        if actual != expected_value:
            mismatches[key] = {"expected": expected_value, "actual": actual}
    if mismatches:
        result["claim_effect"] = "tester_setting_mismatch_forbids_runtime_probe_completed"
        result["tester_mismatches"] = mismatches
        return result
    result.update(
        {
            "status": "pass",
            "runtime_probe_completed_claim_allowed": True,
            "claim_effect": "standard_runtime_probe_contract_satisfied",
        }
    )
    return result


def metadata_for_attempt(
    *,
    split: str,
    from_date: str,
    to_date: str,
    tester: Mapping[str, Any] | None = None,
    probe_profile: str = STANDARD_RUNTIME_PROBE_PROFILE,
    contract: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return validate_attempt_contract(
        split=split,
        from_date=from_date,
        to_date=to_date,
        tester=tester,
        probe_profile=probe_profile,
        contract=contract,
    )


def assert_standard_attempt_period(
    *,
    split: str,
    from_date: str,
    to_date: str,
    contract: Mapping[str, Any] | None = None,
) -> None:
    expected_from, expected_to = standard_period(split, contract)
    if from_date != expected_from or to_date != expected_to:
        raise ValueError(
            f"Noncanonical MT5 runtime probe period for {split}: "
            f"{from_date}..{to_date}; expected {expected_from}..{expected_to}"
        )


def _payload_sequence(payload: Mapping[str, Any], *keys: str) -> list[Mapping[str, Any]]:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, Mapping)]
    return []


def _report_names_by_status(reports: Sequence[Mapping[str, Any]]) -> tuple[set[str], dict[str, set[str]]]:
    completed: set[str] = set()
    by_split: dict[str, set[str]] = {}
    for report in reports:
        name = str(report.get("report_name", "")).strip()
        split = str(report.get("split", "")).strip()
        if str(report.get("status", "")).strip() == "completed":
            if name:
                completed.add(name)
            if split:
                by_split.setdefault(split, set()).add(name or f"split:{split}")
    return completed, by_split


def _execution_rows(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    rows = _payload_sequence(payload, "execution_results")
    if rows:
        return rows
    execution = payload.get("execution")
    if isinstance(execution, Mapping):
        rows = _payload_sequence(execution, "execution_results")
        if rows:
            return rows
    nested = _payload_sequence(payload, "results", "runs")
    return [row for item in nested for row in _payload_sequence(item, "execution_results")]


def _nested_runtime_payloads(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    mt5_result = payload.get("mt5_result")
    if isinstance(mt5_result, Mapping):
        return [mt5_result]
    prepared = payload.get("prepared")
    if isinstance(prepared, Mapping):
        return [prepared]
    return []


def _portable_present(row: Mapping[str, Any]) -> bool:
    metadata = row.get("mt5_runtime_probe_contract")
    if isinstance(metadata, Mapping) and metadata.get("portable_arg_present") is True:
        return True
    command = row.get("command", ())
    if not isinstance(command, SequenceABC) or isinstance(command, (str, bytes)):
        return False
    return any(str(arg).lower() == "/portable" for arg in command)


def _matching_execution_rows(
    attempt: Mapping[str, Any],
    execution_rows: Sequence[Mapping[str, Any]],
) -> list[Mapping[str, Any]]:
    attempt_name = str(attempt.get("attempt_name", "")).strip()
    if attempt_name:
        matches = [row for row in execution_rows if str(row.get("attempt_name", "")).strip() == attempt_name]
        if matches:
            return matches
    tier = str(attempt.get("tier", "")).strip()
    split = str(attempt.get("split", "")).strip()
    return [
        row
        for row in execution_rows
        if str(row.get("tier", "")).strip() == tier and str(row.get("split", "")).strip() == split
    ]


def _completion_config(contract: Mapping[str, Any]) -> Mapping[str, Any]:
    completion = contract.get("completion", {})
    return completion if isinstance(completion, Mapping) else {}


def _completion_requires_surface_contract(contract: Mapping[str, Any]) -> bool:
    value = _completion_config(contract).get("runtime_probe_completed_requires_surface_contract", False)
    return bool(value)


def _allowed_surface_scopes(contract: Mapping[str, Any]) -> set[str]:
    raw = _completion_config(contract).get("allowed_surface_scopes_for_completion", ())
    if not isinstance(raw, SequenceABC) or isinstance(raw, (str, bytes)):
        return set()
    return {str(value).strip() for value in raw}


def _forbidden_source_artifact_roles(contract: Mapping[str, Any]) -> set[str]:
    raw = _completion_config(contract).get("forbidden_source_artifact_roles_for_completion", ())
    if not isinstance(raw, SequenceABC) or isinstance(raw, (str, bytes)):
        return set()
    return {str(value).strip() for value in raw}


def _runtime_surface_contract_for_attempt(
    payload: Mapping[str, Any],
    attempt: Mapping[str, Any],
) -> Mapping[str, Any] | None:
    attempt_contract = attempt.get("runtime_surface_contract")
    if isinstance(attempt_contract, Mapping):
        return attempt_contract

    split = str(attempt.get("split", "")).strip()
    for container in (payload.get("runtime_surface_contract"), payload.get("surface")):
        if not isinstance(container, Mapping):
            continue
        contract = container.get("runtime_surface_contract") if "runtime_surface_contract" in container else container
        if not isinstance(contract, Mapping):
            continue
        by_split = contract.get("by_split")
        if isinstance(by_split, Mapping) and split in by_split and isinstance(by_split[split], Mapping):
            merged = dict(contract)
            merged.update(dict(by_split[split]))
            return merged
        return contract
    return None


def _surface_contract_blocking_details(
    payload: Mapping[str, Any],
    attempt: Mapping[str, Any],
    contract_payload: Mapping[str, Any],
) -> dict[str, Any] | None:
    surface_contract = _runtime_surface_contract_for_attempt(payload, attempt)
    if surface_contract is None:
        return None
    completion_allowed = _bool_contract_value(surface_contract.get("completion_claim_allowed"))
    standard_period_covered = _bool_contract_value(surface_contract.get("standard_period_covered"))
    surface_scope = str(surface_contract.get("surface_scope", "")).strip()
    source_role = str(surface_contract.get("source_artifact_role", "")).strip()
    allowed_scopes = _allowed_surface_scopes(contract_payload)
    forbidden_roles = _forbidden_source_artifact_roles(contract_payload)
    reasons: list[str] = []
    if completion_allowed is False:
        reasons.append("completion_claim_not_allowed")
    if standard_period_covered is False:
        reasons.append("standard_period_not_covered")
    if allowed_scopes and surface_scope and surface_scope not in allowed_scopes:
        reasons.append("surface_scope_not_standard_completion_eligible")
    if source_role in forbidden_roles:
        reasons.append("forbidden_source_artifact_role")
    if not reasons:
        return None
    return {
        "attempt_name": attempt.get("attempt_name"),
        "split": attempt.get("split"),
        "completion_claim_allowed": completion_allowed,
        "standard_period_covered": standard_period_covered,
        "surface_scope": surface_scope,
        "source_artifact_role": source_role,
        "allowed_surface_scopes": sorted(allowed_scopes),
        "forbidden_source_artifact_roles": sorted(forbidden_roles),
        "reasons": reasons,
    }


def _bool_contract_value(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    text = str(value).strip().lower()
    if text in {"true", "yes", "1", "allowed", "pass"}:
        return True
    if text in {"false", "no", "0", "blocked", "forbidden"}:
        return False
    return None


def audit_mt5_runtime_probe_contract(
    payload: Mapping[str, Any],
    *,
    requested_claims: Sequence[str] = (),
    contract: Mapping[str, Any] | None = None,
) -> AuditResult:
    contract_payload = contract or load_contract()
    claims = tuple(str(claim) for claim in requested_claims)
    completion_claim_requested = bool(RUNTIME_COMPLETION_CLAIMS.intersection(claims))
    attempts = _payload_sequence(payload, "attempts", "mt5_attempts")
    if not attempts:
        nested = _payload_sequence(payload, "results", "runs")
        attempts = [attempt for item in nested for attempt in _payload_sequence(item, "attempts", "mt5_attempts")]
    if not attempts:
        attempts = [
            attempt
            for item in _nested_runtime_payloads(payload)
            for attempt in _payload_sequence(item, "attempts", "mt5_attempts")
        ]
    execution_rows = _execution_rows(payload)
    if not execution_rows:
        execution_rows = [row for item in _nested_runtime_payloads(payload) for row in _execution_rows(item)]
    reports = _payload_sequence(payload, "strategy_tester_reports", "report_records", "reports")
    if not reports:
        execution = payload.get("execution")
        if isinstance(execution, Mapping):
            reports = _payload_sequence(execution, "strategy_tester_reports", "report_records", "reports")
    if not reports:
        reports = [
            report
            for item in _nested_runtime_payloads(payload)
            for report in _payload_sequence(item, "strategy_tester_reports", "report_records", "reports")
        ]
    if not reports:
        reports = [
            dict(row["strategy_tester_report"])
            for row in execution_rows
            if isinstance(row.get("strategy_tester_report"), Mapping)
        ]
    findings: list[AuditFinding] = []
    standard_attempts: list[Mapping[str, Any]] = []
    exception_attempt_count = 0
    seen_splits: set[str] = set()
    for attempt in attempts:
        split = str(attempt.get("split", "")).strip()
        tester = _attempt_tester(attempt)
        from_date = str(tester.get("FromDate", "")).strip()
        to_date = str(tester.get("ToDate", "")).strip()
        profile = profile_for_attempt(attempt)
        metadata = validate_attempt_contract(
            split=split,
            from_date=from_date,
            to_date=to_date,
            tester=tester,
            probe_profile=profile,
            contract=contract_payload,
        )
        if profile == STANDARD_RUNTIME_PROBE_PROFILE:
            standard_attempts.append(attempt)
            seen_splits.add(split)
            if metadata["status"] != "pass":
                findings.append(
                    AuditFinding(
                        check_id="mt5_runtime_probe_contract::attempt_contract_mismatch",
                        message="Standard MT5 runtime probe attempt does not match the canonical contract.",
                        details={
                            "attempt_name": attempt.get("attempt_name"),
                            "split": split,
                            "from_date": from_date,
                            "to_date": to_date,
                            "contract": metadata,
                        },
                    )
                )
            blocking_surface_details = _surface_contract_blocking_details(payload, attempt, contract_payload)
            if blocking_surface_details is not None:
                findings.append(
                    AuditFinding(
                        check_id="mt5_runtime_probe_contract::surface_contract_forbids_standard_attempt",
                        message=(
                            "A standard MT5 runtime probe attempt cannot be created from a partial, sample, "
                            "or non-completion-eligible runtime surface."
                        ),
                        details=blocking_surface_details,
                    )
                )
        else:
            exception_attempt_count += 1
            if completion_claim_requested:
                findings.append(
                    AuditFinding(
                        check_id="mt5_runtime_probe_contract::exception_profile_for_completion_claim",
                        message="Exception-profile MT5 probe cannot support runtime_probe_completed.",
                        details={
                            "attempt_name": attempt.get("attempt_name"),
                            "split": split,
                            "profile": profile,
                            "claim_effect": metadata.get("claim_effect"),
                        },
                    )
                )
    if completion_claim_requested:
        missing_splits = [split for split in required_splits(contract_payload) if split not in seen_splits]
        if missing_splits:
            findings.append(
                AuditFinding(
                    check_id="mt5_runtime_probe_contract::missing_required_split",
                    message="runtime_probe_completed requires both canonical validation_is and oos attempts.",
                    details={"missing_splits": missing_splits, "seen_splits": sorted(seen_splits)},
                )
            )
        completed_report_names, completed_reports_by_split = _report_names_by_status(reports)
        for attempt in standard_attempts:
            matching_rows = _matching_execution_rows(attempt, execution_rows)
            if not matching_rows:
                findings.append(
                    AuditFinding(
                        check_id="mt5_runtime_probe_contract::missing_execution_result",
                        message="Standard MT5 runtime probe attempt is missing an execution result with terminal command evidence.",
                        details={"attempt_name": attempt.get("attempt_name"), "split": attempt.get("split"), "tier": attempt.get("tier")},
                    )
                )
            elif not any(_portable_present(row) for row in matching_rows):
                findings.append(
                    AuditFinding(
                        check_id="mt5_runtime_probe_contract::nonportable_execution",
                        message="Standard MT5 runtime probe execution did not show required /portable mode.",
                        details={"attempt_name": attempt.get("attempt_name"), "split": attempt.get("split"), "tier": attempt.get("tier")},
                    )
                )
            report_name = str(_attempt_tester(attempt).get("Report", "")).strip()
            if not report_name or report_name not in completed_report_names:
                findings.append(
                    AuditFinding(
                        check_id="mt5_runtime_probe_contract::missing_completed_report",
                        message="Standard MT5 runtime probe attempt is missing a completed Strategy Tester report.",
                        details={
                            "attempt_name": attempt.get("attempt_name"),
                            "split": attempt.get("split"),
                            "report_name": report_name,
                        },
                    )
                )
            if _completion_requires_surface_contract(contract_payload):
                surface_contract = _runtime_surface_contract_for_attempt(payload, attempt)
                if surface_contract is None:
                    findings.append(
                        AuditFinding(
                            check_id="mt5_runtime_probe_contract::missing_runtime_surface_contract",
                            message="runtime_probe_completed requires an explicit runtime surface contract, not an implicit sample or preview surface.",
                            details={
                                "attempt_name": attempt.get("attempt_name"),
                                "split": attempt.get("split"),
                            },
                        )
                    )
                else:
                    completion_allowed = _bool_contract_value(surface_contract.get("completion_claim_allowed"))
                    standard_period_covered = _bool_contract_value(surface_contract.get("standard_period_covered"))
                    surface_scope = str(surface_contract.get("surface_scope", "")).strip()
                    source_role = str(surface_contract.get("source_artifact_role", "")).strip()
                    allowed_scopes = _allowed_surface_scopes(contract_payload)
                    forbidden_roles = _forbidden_source_artifact_roles(contract_payload)
                    if completion_allowed is False or standard_period_covered is False:
                        findings.append(
                            AuditFinding(
                                check_id="mt5_runtime_probe_contract::surface_contract_forbids_completion",
                                message="runtime_probe_completed is blocked by the runtime surface contract.",
                                details={
                                    "attempt_name": attempt.get("attempt_name"),
                                    "split": attempt.get("split"),
                                    "completion_claim_allowed": completion_allowed,
                                    "standard_period_covered": standard_period_covered,
                                    "surface_scope": surface_scope,
                                    "source_artifact_role": source_role,
                                },
                            )
                        )
                    if allowed_scopes and surface_scope not in allowed_scopes:
                        findings.append(
                            AuditFinding(
                                check_id="mt5_runtime_probe_contract::surface_scope_not_completion_eligible",
                                message="runtime_probe_completed requires a full-period runtime surface scope.",
                                details={
                                    "attempt_name": attempt.get("attempt_name"),
                                    "split": attempt.get("split"),
                                    "surface_scope": surface_scope,
                                    "allowed_surface_scopes": sorted(allowed_scopes),
                                },
                            )
                        )
                    if source_role in forbidden_roles:
                        findings.append(
                            AuditFinding(
                                check_id="mt5_runtime_probe_contract::sample_source_forbids_completion",
                                message="runtime_probe_completed cannot be supported by a sample or preview source artifact.",
                                details={
                                    "attempt_name": attempt.get("attempt_name"),
                                    "split": attempt.get("split"),
                                    "source_artifact_role": source_role,
                                    "forbidden_source_artifact_roles": sorted(forbidden_roles),
                                },
                            )
                        )
        for split in required_splits(contract_payload):
            if split not in completed_reports_by_split:
                findings.append(
                    AuditFinding(
                        check_id="mt5_runtime_probe_contract::missing_split_report",
                        message="runtime_probe_completed requires at least one completed Strategy Tester report for each required split.",
                        details={"split": split},
                    )
                )
    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    allowed_claims = ["runtime_probe_observation"]
    if status == "pass" and completion_claim_requested:
        allowed_claims.append("runtime_probe_completed")
    return AuditResult(
        audit_name="mt5_runtime_probe_contract_audit",
        status=status,
        findings=tuple(findings),
        counts={
            "attempts": len(attempts),
            "standard_attempts": len(standard_attempts),
            "exception_attempts": exception_attempt_count,
            "execution_results": len(execution_rows),
            "reports": len(reports),
            "required_splits": required_splits(contract_payload),
            "standard_periods": standard_split_specs(contract_payload),
            "requested_claims": claims,
        },
        allowed_claims=tuple(allowed_claims) if status == "pass" else ("blocked",),
        forbidden_claims=()
        if status == "pass"
        else ("runtime_probe_completed", "mt5_verification_complete", "runtime_verified"),
    )


def audit_mt5_runtime_probe_contract_path(
    path: Path,
    *,
    requested_claims: Sequence[str] = (),
    contract_path: Path | None = None,
) -> AuditResult:
    raw_payload = json.loads(io_path(path).read_text(encoding="utf-8-sig"))
    if isinstance(raw_payload, list):
        payload: Mapping[str, Any] = {"results": raw_payload}
    elif isinstance(raw_payload, Mapping):
        payload = raw_payload
    else:
        raise ValueError(f"MT5 runtime probe audit input must be a mapping: {path}")
    return audit_mt5_runtime_probe_contract(
        payload,
        requested_claims=requested_claims,
        contract=load_contract(contract_path),
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit MT5 runtime probe period, execution, and report contract.")
    parser.add_argument("payload_json")
    parser.add_argument("--requested-claim", action="append", default=[])
    parser.add_argument("--contract", default=None)
    parser.add_argument("--output-json", default=None)
    parser.add_argument("--allow-blocked-exit-zero", action="store_true")
    args = parser.parse_args(argv)
    result = audit_mt5_runtime_probe_contract_path(
        Path(args.payload_json),
        requested_claims=tuple(args.requested_claim),
        contract_path=Path(args.contract) if args.contract else None,
    )
    payload = result.to_dict()
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output_json:
        io_path(Path(args.output_json).parent).mkdir(parents=True, exist_ok=True)
        io_path(Path(args.output_json)).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if args.allow_blocked_exit_zero or not result.completed_forbidden else 2


if __name__ == "__main__":
    raise SystemExit(main())
