from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult


@dataclass(frozen=True)
class ScopeCountCheck:
    check_id: str
    expected_count: int
    actual_count: int
    evidence_label: str
    description: str = ""
    required: bool = True
    user_scope_reduction_quote: str = ""

    @property
    def passed(self) -> bool:
        return self.actual_count >= self.expected_count

    @property
    def reduced_with_user_quote(self) -> bool:
        return (not self.passed) and bool(self.user_scope_reduction_quote.strip())

    def to_counts(self) -> dict[str, Any]:
        return {
            "expected": self.expected_count,
            "actual": self.actual_count,
            "evidence_label": self.evidence_label,
            "required": self.required,
            "has_user_scope_reduction_quote": bool(self.user_scope_reduction_quote.strip()),
        }


def evaluate_scope_completion(checks: Iterable[ScopeCountCheck]) -> AuditResult:
    checks_tuple = tuple(checks)
    findings: list[AuditFinding] = []
    counts: dict[str, Any] = {check.check_id: check.to_counts() for check in checks_tuple}
    reduced = False

    for check in checks_tuple:
        if check.passed or not check.required:
            continue
        if check.reduced_with_user_quote:
            reduced = True
            findings.append(
                AuditFinding(
                    check_id=check.check_id,
                    severity="warning",
                    message="Scope was reduced with an explicit user quote; full-scope completion is still forbidden.",
                    details=check.to_counts(),
                )
            )
            continue
        findings.append(
            AuditFinding(
                check_id=check.check_id,
                message=(
                    f"Requested {check.expected_count} {check.evidence_label}, "
                    f"but only {check.actual_count} exist."
                ),
                details=check.to_counts(),
            )
        )

    blocking = any(finding.is_blocking for finding in findings)
    if blocking:
        status = "partial" if any(check.actual_count > 0 for check in checks_tuple) else "blocked"
        forbidden_claims = tuple(sorted(COMPLETION_CLAIMS))
        allowed_claims = ("partial", "incomplete", "blocked")
    elif reduced:
        status = "reduced_scope"
        forbidden_claims = ("full_verification_complete", "mt5_verification_complete")
        allowed_claims = ("completed_reduced_scope", "partial")
    else:
        status = "complete"
        forbidden_claims = ()
        allowed_claims = ("completed", "verified")

    return AuditResult(
        audit_name="scope_completion_gate",
        status=status,
        findings=tuple(findings),
        counts=counts,
        allowed_claims=allowed_claims,
        forbidden_claims=forbidden_claims,
    )


def scope_counts_from_mapping(scope: Mapping[str, Mapping[str, Any]]) -> list[ScopeCountCheck]:
    return [
        ScopeCountCheck(
            check_id=check_id,
            expected_count=int(payload.get("expected_count", 0)),
            actual_count=int(payload.get("actual_count", 0)),
            evidence_label=str(payload.get("evidence_label", check_id)),
            description=str(payload.get("description", "")),
            required=bool(payload.get("required", True)),
            user_scope_reduction_quote=str(payload.get("user_scope_reduction_quote", "")),
        )
        for check_id, payload in scope.items()
    ]
