from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from foundation.control_plane.prompt_intake_classifier import PromptClassification


RISK_LEVELS = ("none", "low", "medium", "high")


@dataclass(frozen=True)
class RiskVectorScan:
    risks: Mapping[str, str]
    hard_stop_risks: tuple[str, ...] = ()
    required_decision_locks: tuple[str, ...] = ()
    required_gates: tuple[str, ...] = ()
    required_skills: tuple[str, ...] = ()
    forbidden_claims: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "risks": dict(self.risks),
            "hard_stop_risks": list(self.hard_stop_risks),
            "required_decision_locks": list(self.required_decision_locks),
            "required_gates": list(self.required_gates),
            "required_skills": list(self.required_skills),
            "forbidden_claims": list(self.forbidden_claims),
            "reasons": list(self.reasons),
        }


def scan_risk_vector(
    classification: PromptClassification,
    *,
    current_truth_conflict: bool = False,
    destructive_requested: bool = False,
) -> RiskVectorScan:
    risks: dict[str, str] = {
        "scope_ambiguous": "none",
        "mutation_ambiguous": "none",
        "state_sync_risk": "none",
        "claim_boundary_risk": "low",
        "skill_abandonment_risk": "low",
        "evidence_gap_risk": "low",
        "runtime_parity_risk": "none",
        "kpi_source_risk": "none",
        "code_surface_risk": "none",
        "destructive_change_risk": "none",
        "unattended_autonomy_risk": "none",
        "answer_clarity_risk": "medium",
    }
    hard_stops: list[str] = []
    locks: list[str] = []
    gates: list[str] = ["final_claim_guard"]
    skills: list[str] = ["obsidian-answer-clarity", "obsidian-claim-discipline"]
    forbidden_claims: list[str] = []
    reasons: list[str] = []

    families = set(classification.detected_families)
    surfaces = set(classification.touched_surfaces)

    if "experiment_execution" in families and not classification.execution_intent:
        risks["scope_ambiguous"] = "medium"
        locks.append("execution_scope")
    if classification.mutation_intent and classification.primary_family in {
        "state_sync",
        "policy_skill_governance",
        "code_refactor",
        "kpi_evidence",
        "cleanup_archive",
    }:
        risks["mutation_ambiguous"] = "high"
        locks.append("edit_policy")
        reasons.append("mutation_or_scope_requires_decision_lock")
    if current_truth_conflict or "state_sync" in families or "docs_current_truth" in surfaces:
        risks["state_sync_risk"] = "high"
        gates.append("state_sync_audit")
        skills.append("obsidian-reentry-read")
        forbidden_claims.extend(("current_truth_synced", "stage_transition_completed"))
        if current_truth_conflict:
            hard_stops.append("state_sync_risk")
            locks.append("canonical_current_truth")
            reasons.append("current_truth_conflict_detected")
    if classification.requested_claims or classification.mutation_intent or classification.execution_intent:
        risks["claim_boundary_risk"] = "high"
        gates.append("final_claim_guard")
    if "runtime_backtest" in families or "mt5_runtime" in surfaces:
        risks["runtime_parity_risk"] = "high"
        gates.extend(("runtime_evidence_gate", "kpi_contract_audit"))
        skills.extend(("obsidian-runtime-parity", "obsidian-backtest-forensics"))
        forbidden_claims.extend(("runtime_authority", "mt5_verification_complete"))
    if "kpi_evidence" in families or "kpi_ledgers" in surfaces:
        risks["kpi_source_risk"] = "high"
        gates.extend(("kpi_contract_audit", "row_grain_audit", "source_authority_audit"))
        skills.extend(("obsidian-run-evidence-system", "obsidian-result-judgment"))
    if {"code_edit", "code_refactor"}.intersection(families) or {"foundation_code", "pipelines"}.intersection(surfaces):
        risks["code_surface_risk"] = "high"
        gates.append("code_surface_audit")
        skills.append("obsidian-code-surface-guard")
    if destructive_requested or "cleanup_archive" in families:
        risks["destructive_change_risk"] = "high"
        hard_stops.append("destructive_change_risk")
        locks.append("destructive_change_permission")
        gates.append("destructive_change_guard")
    if classification.execution_intent and "experiment_execution" in families:
        risks["unattended_autonomy_risk"] = "medium"
        gates.append("scope_completion_gate")
    if classification.primary_family != "information_only":
        risks["evidence_gap_risk"] = "medium"
        gates.append("artifact_lineage_audit")
        skills.append("obsidian-artifact-lineage")

    return RiskVectorScan(
        risks=risks,
        hard_stop_risks=tuple(_unique(hard_stops)),
        required_decision_locks=tuple(_unique(locks)),
        required_gates=tuple(_unique(gates)),
        required_skills=tuple(_unique(skills)),
        forbidden_claims=tuple(_unique(forbidden_claims)),
        reasons=tuple(_unique(reasons)),
    )


def _unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))
