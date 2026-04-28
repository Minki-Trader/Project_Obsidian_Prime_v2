from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult


ALLOWED_NOT_USED_REASONS = frozenset(
    {
        "no_related_surface_touched",
        "summary_only_no_new_claim",
        "already_executed_same_packet",
        "user_explicitly_excluded_with_quote",
        "blocked_missing_required_input",
    }
)


@dataclass(frozen=True)
class SkillReceipt:
    skill: str
    triggered: bool
    status: str
    receipt_path: str = ""
    blocking: bool = False
    not_used_reason: str = ""

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object]) -> "SkillReceipt":
        return cls(
            skill=str(payload.get("skill", "")),
            triggered=bool(payload.get("triggered", True)),
            status=str(payload.get("status", "")),
            receipt_path=str(payload.get("receipt_path", "")),
            blocking=bool(payload.get("blocking", False)),
            not_used_reason=str(payload.get("not_used_reason", "")),
        )


def lint_skill_receipts(
    *,
    required_skills: Iterable[str],
    receipts: Iterable[SkillReceipt | Mapping[str, object]],
) -> AuditResult:
    required = tuple(required_skills)
    receipt_list = tuple(
        receipt if isinstance(receipt, SkillReceipt) else SkillReceipt.from_mapping(receipt) for receipt in receipts
    )
    by_skill = {receipt.skill: receipt for receipt in receipt_list}
    findings: list[AuditFinding] = []

    for skill in required:
        receipt = by_skill.get(skill)
        if receipt is None:
            findings.append(
                AuditFinding(
                    check_id=f"skill::{skill}",
                    message=f"Required skill `{skill}` has no receipt.",
                )
            )
            continue
        if receipt.not_used_reason and receipt.not_used_reason not in ALLOWED_NOT_USED_REASONS:
            findings.append(
                AuditFinding(
                    check_id=f"skill::{skill}::not_used_reason",
                    message=f"Skill `{skill}` has an unapproved not_used_reason.",
                    details={"not_used_reason": receipt.not_used_reason},
                )
            )
        if receipt.triggered and receipt.status != "executed":
            findings.append(
                AuditFinding(
                    check_id=f"skill::{skill}::status",
                    message=f"Triggered skill `{skill}` status is `{receipt.status}`, not `executed`.",
                    details={"receipt_path": receipt.receipt_path, "not_used_reason": receipt.not_used_reason},
                )
            )
        if receipt.blocking:
            findings.append(
                AuditFinding(
                    check_id=f"skill::{skill}::blocking",
                    message=f"Skill `{skill}` reported a blocking finding.",
                    details={"receipt_path": receipt.receipt_path},
                )
            )

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    return AuditResult(
        audit_name="skill_receipt_lint",
        status=status,
        findings=tuple(findings),
        counts={"required_skills": required, "receipt_count": len(receipt_list)},
        allowed_claims=("completed",) if status == "pass" else ("partial", "incomplete", "blocked"),
        forbidden_claims=() if status == "pass" else tuple(sorted(COMPLETION_CLAIMS)),
    )
