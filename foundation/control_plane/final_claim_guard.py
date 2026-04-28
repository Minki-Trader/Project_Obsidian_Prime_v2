from __future__ import annotations

from typing import Iterable

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult


def guard_final_claims(*, requested_claims: Iterable[str], audit_results: Iterable[AuditResult]) -> AuditResult:
    requested = tuple(str(claim) for claim in requested_claims)
    results = tuple(audit_results)
    forbidden_by_audits = {claim for result in results for claim in result.forbidden_claims}
    completion_blocked = any(result.completed_forbidden for result in results)
    findings: list[AuditFinding] = []

    if completion_blocked:
        for claim in requested:
            if claim in COMPLETION_CLAIMS or claim in forbidden_by_audits:
                findings.append(
                    AuditFinding(
                        check_id=f"claim::{claim}",
                        message=f"Final claim `{claim}` is forbidden because a required audit did not pass.",
                        details={"requested_claim": claim},
                    )
                )

    if findings:
        status = "blocked"
        allowed_claims = ("partial", "incomplete", "blocked")
        forbidden_claims = tuple(sorted(set(forbidden_by_audits).union(COMPLETION_CLAIMS.intersection(requested))))
    else:
        status = "pass"
        allowed_claims = requested
        forbidden_claims = tuple(sorted(forbidden_by_audits.intersection(requested)))

    return AuditResult(
        audit_name="final_claim_guard",
        status=status,
        findings=tuple(findings),
        counts={"requested_claims": requested, "source_audits": [result.audit_name for result in results]},
        allowed_claims=allowed_claims,
        forbidden_claims=forbidden_claims,
    )
