from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from foundation.control_plane.audit_result import AuditResult
from foundation.control_plane.final_claim_guard import guard_final_claims
from foundation.control_plane.kpi_contract_audit import KpiContract, audit_kpi_contract
from foundation.control_plane.scope_completion_gate import ScopeCountCheck, evaluate_scope_completion
from foundation.control_plane.skill_receipt_lint import SkillReceipt, lint_skill_receipts


@dataclass(frozen=True)
class WorkPacketGateReport:
    packet_id: str
    status: str
    audits: tuple[AuditResult, ...]
    final_claim_guard: AuditResult

    @property
    def completed_forbidden(self) -> bool:
        return self.final_claim_guard.status == "blocked" or any(audit.completed_forbidden for audit in self.audits)

    def to_dict(self) -> dict[str, object]:
        return {
            "packet_id": self.packet_id,
            "status": self.status,
            "completed_forbidden": self.completed_forbidden,
            "audits": [audit.to_dict() for audit in self.audits],
            "final_claim_guard": self.final_claim_guard.to_dict(),
        }


def evaluate_work_packet_closeout(
    *,
    packet_id: str,
    requested_claims: Iterable[str],
    scope_checks: Iterable[ScopeCountCheck] = (),
    required_skills: Iterable[str] = (),
    skill_receipts: Iterable[SkillReceipt | Mapping[str, object]] = (),
    kpi_contracts: Iterable[KpiContract] = (),
    extra_audits: Iterable[AuditResult] = (),
) -> WorkPacketGateReport:
    audits: list[AuditResult] = []

    scope_checks_tuple = tuple(scope_checks)
    if scope_checks_tuple:
        audits.append(evaluate_scope_completion(scope_checks_tuple))

    required_skills_tuple = tuple(required_skills)
    if required_skills_tuple:
        audits.append(lint_skill_receipts(required_skills=required_skills_tuple, receipts=skill_receipts))

    for contract in kpi_contracts:
        audits.append(audit_kpi_contract(contract))

    audits.extend(extra_audits)

    final_guard = guard_final_claims(requested_claims=requested_claims, audit_results=audits)
    if final_guard.status == "blocked":
        status = "blocked"
    elif any(audit.status == "partial" for audit in audits):
        status = "partial"
    elif any(audit.status == "reduced_scope" for audit in audits):
        status = "reduced_scope"
    else:
        status = "pass"

    return WorkPacketGateReport(
        packet_id=packet_id,
        status=status,
        audits=tuple(audits),
        final_claim_guard=final_guard,
    )
