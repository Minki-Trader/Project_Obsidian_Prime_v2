from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


COMPLETION_CLAIMS = frozenset(
    {
        "complete",
        "completed",
        "reviewed",
        "verified",
        "verification_complete",
        "full_verification_complete",
        "mt5_verification_complete",
        "runtime_probe_completed",
        "runtime_authority",
        "operating_promotion",
    }
)


@dataclass(frozen=True)
class AuditFinding:
    check_id: str
    message: str
    severity: str = "blocking"
    details: Mapping[str, Any] = field(default_factory=dict)

    @property
    def is_blocking(self) -> bool:
        return self.severity == "blocking"

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "message": self.message,
            "severity": self.severity,
            "details": dict(self.details),
        }


@dataclass(frozen=True)
class AuditResult:
    audit_name: str
    status: str
    findings: tuple[AuditFinding, ...] = ()
    counts: Mapping[str, Any] = field(default_factory=dict)
    allowed_claims: tuple[str, ...] = ()
    forbidden_claims: tuple[str, ...] = ()

    @property
    def passed(self) -> bool:
        return self.status in {"pass", "complete", "completed", "reduced_scope"}

    @property
    def has_blocking_findings(self) -> bool:
        return any(finding.is_blocking for finding in self.findings)

    @property
    def completed_forbidden(self) -> bool:
        return self.has_blocking_findings or bool(COMPLETION_CLAIMS.intersection(self.forbidden_claims))

    def to_dict(self) -> dict[str, Any]:
        return {
            "audit_name": self.audit_name,
            "status": self.status,
            "passed": self.passed,
            "completed_forbidden": self.completed_forbidden,
            "findings": [finding.to_dict() for finding in self.findings],
            "counts": dict(self.counts),
            "allowed_claims": list(self.allowed_claims),
            "forbidden_claims": list(self.forbidden_claims),
        }
