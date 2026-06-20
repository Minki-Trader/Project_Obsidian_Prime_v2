from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult
from foundation.control_plane.ledger import io_path


V1_REQUIRED = (
    "packet_id",
    "created_at_utc",
    "user_request",
    "current_truth",
    "preflight",
    "interpreted_scope",
    "acceptance_criteria",
    "row_grain",
    "kpi_contract",
    "artifact_contract",
    "skill_routing",
    "gates",
    "final_claim_policy",
)
V2_REQUIRED = (
    "packet_id",
    "created_at_utc",
    "user_request",
    "current_truth",
    "work_classification",
    "risk_vector_scan",
    "decision_lock",
    "interpreted_scope",
    "acceptance_criteria",
    "work_plan",
    "skill_routing",
    "evidence_contract",
    "gates",
    "final_claim_policy",
)
V2_1_REQUIRED = (
    "packet_lifecycle",
    "packet_id",
    "created_at_utc",
    "user_request",
    "current_truth",
    "work_classification",
    "risk_vector_scan",
    "decision_lock",
    "interpreted_scope",
    "verification_profile",
    "acceptance_criteria",
    "work_plan",
    "skill_routing",
    "evidence_contract",
    "gates",
    "final_claim_policy",
)
NEW_PACKET_REQUIRED_VERSION = "work_packet_schema_v2_1"
ARCHIVE_ONLY_PACKET_LIFECYCLES = frozenset({"archive_only", "legacy_archive_only", "historical_archive_only"})
V2_SCOPE_REQUIRED = (
    "work_families",
    "target_surfaces",
    "scope_units",
    "execution_layers",
    "mutation_policy",
    "evidence_layers",
    "reduction_policy",
    "claim_boundary",
)
V2_SKILL_ROUTING_REQUIRED = (
    "primary_family",
    "primary_skill",
    "support_skills",
    "skills_considered",
    "skills_selected",
    "skills_not_used",
    "required_skill_receipts",
    "required_gates",
)
VERIFICATION_PROFILE_REQUIRED = (
    "profile_id",
    "claim_surface",
    "trigger_sources",
    "protected_claims",
    "required_evidence",
    "gates_not_run_with_reason",
    "stop_conditions",
)
VERIFICATION_PROFILE_IDS = frozenset(
    {
        "read_only_minimal",
        "design_only",
        "static_contract",
        "targeted_local_execution",
        "proxy_scout",
        "experiment_run",
        "runtime_learning_probe",
        "runtime_probe",
        "stage_closeout",
        "authority_candidate",
        "blocked_pending_decision",
    }
)
PROFILE_EXTRA_REQUIRED_GATES = {
    "static_contract": frozenset({"work_packet_schema_lint"}),
    "targeted_local_execution": frozenset({"test_gate"}),
    "proxy_scout": frozenset({"kpi_contract_audit"}),
    "experiment_run": frozenset({"kpi_contract_audit", "required_gate_coverage_audit"}),
    "runtime_learning_probe": frozenset({"runtime_learning_probe_decision_gate", "required_gate_coverage_audit", "final_claim_guard"}),
    "runtime_probe": frozenset(
        {
            "runtime_evidence_gate",
            "mt5_runtime_probe_contract_audit",
            "kpi_contract_audit",
            "required_gate_coverage_audit",
            "final_claim_guard",
        }
    ),
    "stage_closeout": frozenset({"required_gate_coverage_audit", "final_claim_guard"}),
    "authority_candidate": frozenset({"runtime_evidence_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"}),
}
GATE_NA_REQUIRED = ("gate", "reason_code", "reason", "claim_effect")
RUN_ONLY_FIELDS = ("variants_requested", "verification_layers", "mt5_required", "top_k_reduction_allowed")
RUN_FAMILIES = ("experiment_execution", "runtime_backtest")
AUTHORITY_CLAIMS = frozenset({"runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"})
RUNTIME_CLAIMS = frozenset({"runtime_probe", "runtime_probe_completed", "mt5_verification_complete", "runtime_verified"})
RUNTIME_LEARNING_PROBE_CLAIMS = frozenset(
    {
        "runtime_learning_probe",
        "runtime_learning_probe_candidate",
        "runtime_learning_probe_decision",
        "runtime_learning_probe_decision_recorded",
        "runtime_learning_probe_guard",
    }
)
RUNTIME_ADJACENT_CLAIMS = frozenset(
    {
        "runtime_economics",
        "runtime_economics_pass",
        "economics_pass",
        "materialization_ready",
        "mt5_materialization_ready",
        "runtime_materialization_ready",
        "mt5_handoff_ready",
        "onnx_handoff_ready",
        "ea_handoff_ready",
        "strategy_tester_verified",
        "runtime_backtest_complete",
    }
)
RUNTIME_PROBE_PROFILES = frozenset({"runtime_probe", "authority_candidate"})
RUNTIME_PROBE_EVIDENCE_TERMS = (
    "runtime_probe",
    "runtime evidence",
    "runtime_evidence",
    "mt5",
    "strategy tester",
    "tester output",
    "deal row",
    "trade list",
    "report hash",
    "terminal output",
    "backtest",
)
RUNTIME_PROOF_EVIDENCE_TERMS = (
    "dataset_id",
    "feature_set_id",
    "label_id",
    "split_id",
    "onnx_hash",
    "ea_source_hash",
    "ea_binary_hash",
    "set_ini_hash",
    "feature_order_hash",
    "tester_identity",
    "report_hash",
    "trade_list_hash",
    "telemetry_hash",
)
COMPILE_ONLY_EVIDENCE_TERMS = ("compile_status", "metaeditor compile", "compile-only")
TESTER_RUNTIME_EVIDENCE_TERMS = (
    "tester_status",
    "runtime_status",
    "report_status",
    "strategy tester",
    "tester output",
    "runtime output",
    "terminal output",
    "trade list",
    "deal row",
    "report hash",
)
DISALLOWED_RUNTIME_DEFERRAL_REASON_CODES = frozenset(
    {
        "cost_deferred",
        "too_expensive",
        "expensive",
        "defer_to_next_work",
        "deferred_to_next_work",
        "next_work",
        "later",
        "budget_only",
        "agent_recommended_skip",
        "candidate_0",
        "candidate_gate_0",
        "candidate_gate_failed",
        "candidate_gate_zero",
        "cost_expensive",
        "long_short_imbalanced",
        "low_pf_dd",
        "low_trade_count_expected",
        "not_promotion_candidate",
        "not_strong_candidate",
        "pf_dd_poor",
        "proxy_bad",
        "proxy_result_bad",
    }
)
STRONG_REVIEW_CLAIMS = frozenset({"completed", "reviewed", "verified", "verification_complete", "full_verification_complete"})
BROAD_ONNX_TERMS = (
    "onnx",
    "온엑스",
    "온닉스",
    "open neural network exchange",
)
BROAD_FRONTIER_GOAL_TERMS = (
    "broad goal",
    "frontier continuation",
    "continue frontier",
    "next frontier",
    "new frontier",
    "frontier campaign",
    "개쩌는",
    "쩌는",
    "onnx 만들어",
    "온엑스 만들어",
    "온닉스 만들어",
)
FRONTIER_EXTRA_CLOSEOUT_GATES = frozenset(
    {
        "frontier_extra_mix_depth_lint",
        "runtime_evidence_gate",
        "required_gate_coverage_audit",
        "final_claim_guard",
    }
)
FRONTIER_FIVE_STAGE_DIRECTION_SYNTHESIS_GATE = "frontier_five_stage_direction_synthesis"
FRONTIER_STAGE_OPEN_TERMS = (
    "frontier open",
    "stage open",
    "canonical frontier",
    "new frontier",
    "next frontier",
    "resume frontier",
    "frontier continuation",
    "frontier campaign",
    "전선 개방",
    "정식 전선",
    "다음 전선",
    "재개 전선",
)


def audit_work_packet_schema(packet: Mapping[str, Any]) -> AuditResult:
    findings: list[AuditFinding] = []
    version = str(packet.get("version", "work_packet_schema_v1"))
    requested_action = str(_mapping(packet.get("user_request")).get("requested_action", ""))
    has_v2_fields = any(key in packet for key in ("work_classification", "risk_vector_scan", "decision_lock", "work_plan"))
    is_v2_1 = "v2_1" in version
    packet_lifecycle = _normalized_lifecycle(packet.get("packet_lifecycle"))

    _check_new_packet_version(version, is_v2_1, packet_lifecycle, findings)

    if is_v2_1:
        _require_top_level(packet, V2_1_REQUIRED, findings, version="v2_1")
    elif version.endswith("_v2") or has_v2_fields:
        _require_top_level(packet, V2_REQUIRED, findings, version="v2")

    if is_v2_1 or "verification_profile" in packet:
        _check_verification_profile(packet, findings)

    _check_frontier_extra_overlay_requirements(packet, findings)

    if is_v2_1 or version.endswith("_v2") or has_v2_fields:
        interpreted = _mapping(packet.get("interpreted_scope"))
        _require_fields(interpreted, V2_SCOPE_REQUIRED, findings, prefix="interpreted_scope")
        _require_fields(_mapping(packet.get("skill_routing")), V2_SKILL_ROUTING_REQUIRED, findings, prefix="skill_routing")
    else:
        _require_top_level(packet, V1_REQUIRED, findings, version="v1")

    interpreted = _mapping(packet.get("interpreted_scope"))
    work_families = tuple(str(item) for item in interpreted.get("work_families", ()) if item)
    if _looks_like_non_run_action(requested_action, work_families) and any(field in interpreted for field in RUN_ONLY_FIELDS):
        if not has_v2_fields:
            findings.append(
                AuditFinding(
                    check_id="work_packet_schema::non_run_uses_run_only_scope",
                    message="Non-run work cannot be represented only by run/variant/MT5 fields.",
                    details={"requested_action": requested_action, "run_only_fields": [field for field in RUN_ONLY_FIELDS if field in interpreted]},
                )
            )

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    allowed_claims = ("work_packet_schema_valid",) if status == "pass" else ("blocked",)
    if status == "pass" and not is_v2_1:
        allowed_claims = ("archive_only_work_packet_schema_valid",)
    return AuditResult(
        audit_name="work_packet_schema_lint",
        status=status,
        findings=tuple(findings),
        counts={"version": version, "has_v2_fields": has_v2_fields, "packet_lifecycle": packet_lifecycle or "missing"},
        allowed_claims=allowed_claims,
        forbidden_claims=() if status == "pass" else tuple(sorted(COMPLETION_CLAIMS)),
    )


def audit_work_packet_schema_path(path: Path) -> AuditResult:
    text = io_path(path).read_text(encoding="utf-8-sig")
    payload = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(payload, Mapping):
        return AuditResult(
            audit_name="work_packet_schema_lint",
            status="blocked",
            findings=(AuditFinding(check_id="work_packet_schema::not_mapping", message="Work packet must be a mapping."),),
            forbidden_claims=tuple(sorted(COMPLETION_CLAIMS)),
        )
    return audit_work_packet_schema(payload)


def _require_top_level(packet: Mapping[str, Any], required: tuple[str, ...], findings: list[AuditFinding], *, version: str) -> None:
    for key in required:
        if key not in packet:
            findings.append(
                AuditFinding(
                    check_id=f"work_packet_schema::{version}::missing_top_level::{key}",
                    message="Work packet is missing a required top-level section.",
                    details={"missing": key, "version": version},
                )
            )


def _check_new_packet_version(version: str, is_v2_1: bool, packet_lifecycle: str, findings: list[AuditFinding]) -> None:
    if is_v2_1:
        return
    if packet_lifecycle in ARCHIVE_ONLY_PACKET_LIFECYCLES:
        return
    finding_details = {
        "version": version,
        "packet_lifecycle": packet_lifecycle or "missing",
        "required_version_for_new_packets": NEW_PACKET_REQUIRED_VERSION,
        "archive_only_lifecycles": sorted(ARCHIVE_ONLY_PACKET_LIFECYCLES),
    }
    findings.append(
        AuditFinding(
            check_id="work_packet_schema::version::new_packet_requires_v2_1",
            message="New work packets must use work_packet_schema_v2_1; older schema versions are archive-only.",
            details=finding_details,
        )
    )


def _require_fields(payload: Mapping[str, Any], required: tuple[str, ...], findings: list[AuditFinding], *, prefix: str) -> None:
    for key in required:
        if key not in payload:
            findings.append(
                AuditFinding(
                    check_id=f"work_packet_schema::{prefix}::missing::{key}",
                    message="Work packet section is missing a required field.",
                    details={"section": prefix, "missing": key},
                )
            )


def _check_verification_profile(packet: Mapping[str, Any], findings: list[AuditFinding]) -> None:
    profile = _mapping(packet.get("verification_profile"))
    _require_fields(profile, VERIFICATION_PROFILE_REQUIRED, findings, prefix="verification_profile")

    profile_id = str(profile.get("profile_id", "")).strip()
    if profile_id and profile_id not in VERIFICATION_PROFILE_IDS:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::unknown_profile_id",
                message="Verification profile id is not allowed.",
                details={"profile_id": profile_id, "allowed": sorted(VERIFICATION_PROFILE_IDS)},
            )
        )

    trigger_sources = _string_list(profile.get("trigger_sources"))
    if profile_id != "blocked_pending_decision" and not trigger_sources:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::missing_trigger_sources",
                message="Verification profile must name at least one trigger source unless it is blocked before verification.",
                details={"profile_id": profile_id},
            )
        )

    _check_gate_na_reasons(profile.get("gates_not_run_with_reason"), findings)
    _check_profile_claim_compatibility(packet, profile, findings)


def _check_gate_na_reasons(value: Any, findings: list[AuditFinding]) -> None:
    if _is_missing(value):
        return
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::gates_not_run_not_list",
                message="gates_not_run_with_reason must be a list of structured gate reason records.",
                details={"actual_type": type(value).__name__},
            )
        )
        return
    for index, raw_item in enumerate(value):
        item = _mapping(raw_item)
        if not item:
            findings.append(
                AuditFinding(
                    check_id="work_packet_schema::verification_profile::gate_na_reason_not_mapping",
                    message="Each gate N/A reason must be a mapping, not a bare string or list item.",
                    details={"index": index, "value": raw_item},
                )
            )
            continue
        missing = [field for field in GATE_NA_REQUIRED if _is_missing(item.get(field))]
        if missing:
            findings.append(
                AuditFinding(
                    check_id="work_packet_schema::verification_profile::gate_na_reason_missing_fields",
                    message="Each gate N/A reason must name the gate, reason code, reason, and claim effect.",
                    details={"index": index, "missing": missing},
                )
            )


def _check_profile_claim_compatibility(packet: Mapping[str, Any], profile: Mapping[str, Any], findings: list[AuditFinding]) -> None:
    profile_id = str(profile.get("profile_id", "")).strip()
    claims = _claims_from_packet(packet, profile)
    required_gates = set(_string_list(_mapping(packet.get("skill_routing")).get("required_gates")))
    execution_layers = set(_string_list(_mapping(packet.get("interpreted_scope")).get("execution_layers")))
    runtime_claims = (RUNTIME_CLAIMS | RUNTIME_ADJACENT_CLAIMS | AUTHORITY_CLAIMS).intersection(claims)
    missing_profile_gates = sorted(PROFILE_EXTRA_REQUIRED_GATES.get(profile_id, frozenset()) - required_gates)
    if missing_profile_gates:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::missing_profile_required_gates",
                message="Verification profile extra_required_gates must be present in skill_routing.required_gates.",
                details={"profile_id": profile_id, "missing_profile_gates": missing_profile_gates, "required_gates": sorted(required_gates)},
            )
        )

    if AUTHORITY_CLAIMS.intersection(claims) and profile_id != "authority_candidate":
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::authority_claim_requires_authority_profile",
                message="Authority, promotion, live-readiness, or Goal Achieve claims require the authority_candidate profile.",
                details={"profile_id": profile_id, "claims": sorted(AUTHORITY_CLAIMS.intersection(claims))},
            )
        )
    if RUNTIME_CLAIMS.intersection(claims) and profile_id not in {"runtime_probe", "authority_candidate"}:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::runtime_claim_requires_runtime_profile",
                message="Runtime verification claims require a runtime_probe or authority_candidate profile.",
                details={"profile_id": profile_id, "claims": sorted(RUNTIME_CLAIMS.intersection(claims))},
            )
        )
    if RUNTIME_LEARNING_PROBE_CLAIMS.intersection(claims) and profile_id not in {"runtime_learning_probe", "runtime_probe", "authority_candidate"}:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::runtime_learning_claim_requires_learning_profile",
                message="Runtime learning probe claims require a runtime_learning_probe, runtime_probe, or authority_candidate profile.",
                details={"profile_id": profile_id, "claims": sorted(RUNTIME_LEARNING_PROBE_CLAIMS.intersection(claims))},
            )
        )
    if RUNTIME_ADJACENT_CLAIMS.intersection(claims) and profile_id not in RUNTIME_PROBE_PROFILES:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::runtime_adjacent_claim_requires_runtime_profile",
                message="Runtime materialization, handoff, or economics claims require a runtime_probe or authority_candidate profile.",
                details={"profile_id": profile_id, "claims": sorted(RUNTIME_ADJACENT_CLAIMS.intersection(claims))},
            )
        )
    if "mt5_execution" in execution_layers and profile_id not in {"runtime_learning_probe", "runtime_probe", "authority_candidate"}:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::mt5_execution_requires_runtime_profile",
                message="MT5 execution requires a runtime_learning_probe, runtime_probe, or authority_candidate verification profile.",
                details={"profile_id": profile_id, "execution_layers": sorted(execution_layers)},
            )
        )
    if profile_id == "runtime_learning_probe":
        _check_runtime_learning_probe_profile(profile=profile, required_gates=required_gates, findings=findings)
    if (runtime_claims or "mt5_execution" in execution_layers) and profile_id in RUNTIME_PROBE_PROFILES:
        _check_runtime_probe_evidence(
            profile=profile,
            profile_id=profile_id,
            runtime_claims=runtime_claims or {"mt5_execution"},
            required_gates=required_gates,
            findings=findings,
        )

    strong_claim = bool(STRONG_REVIEW_CLAIMS.intersection(claims) or COMPLETION_CLAIMS.intersection(claims))
    if strong_claim and "final_claim_guard" not in required_gates:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::strong_claim_missing_final_claim_guard",
                message="Strong completion/review/verification claims require final_claim_guard in required_gates.",
                details={"claims": sorted(claims), "required_gates": sorted(required_gates)},
            )
        )
    if (strong_claim or profile_id in {"stage_closeout", "authority_candidate"}) and "required_gate_coverage_audit" not in required_gates:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::strong_claim_missing_gate_coverage",
                message="Strong claims and closeout/authority profiles require required_gate_coverage_audit in required_gates.",
                details={"profile_id": profile_id, "claims": sorted(claims), "required_gates": sorted(required_gates)},
            )
        )


def _check_runtime_learning_probe_profile(*, profile: Mapping[str, Any], required_gates: set[str], findings: list[AuditFinding]) -> None:
    required_evidence = _string_list(profile.get("required_evidence"))
    if "runtime_learning_probe_decision_gate" not in required_gates:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::runtime_learning_missing_decision_gate",
                message="runtime_learning_probe profile requires runtime_learning_probe_decision_gate.",
                details={"required_gates": sorted(required_gates)},
            )
        )
    if not _strings_contain_any(required_evidence, ("runtime_learning_probe_decision", "mt5_action", "repair_attempts")):
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::runtime_learning_missing_decision_evidence",
                message="runtime_learning_probe profile must require runtime_learning_probe_decision evidence.",
                details={"required_evidence": required_evidence},
            )
        )
    _check_runtime_learning_probe_deferral_reasons(profile.get("gates_not_run_with_reason"), findings)


def _check_frontier_extra_overlay_requirements(packet: Mapping[str, Any], findings: list[AuditFinding]) -> None:
    required_gates = set(_string_list(_mapping(packet.get("skill_routing")).get("required_gates")))
    packet_text = _packet_text(packet)
    if _looks_like_broad_onnx_frontier_goal(packet_text) and "frontier_extra_due_check" not in required_gates:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::frontier_extra::broad_onnx_missing_due_check",
                message="Broad ONNX or frontier continuation packets must include frontier_extra_due_check before opening or continuing a frontier campaign.",
                details={"required_gates": sorted(required_gates)},
            )
        )

    if _looks_like_canonical_frontier_open(packet_text) and FRONTIER_FIVE_STAGE_DIRECTION_SYNTHESIS_GATE not in required_gates:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::frontier_direction::missing_five_stage_synthesis",
                message="Canonical frontier open or continuation packets must include the light five-stage direction synthesis gate.",
                details={"required_gates": sorted(required_gates)},
            )
        )

    if _looks_like_frontier_extra_closeout(packet_text):
        missing = sorted(FRONTIER_EXTRA_CLOSEOUT_GATES - required_gates)
        if missing:
            findings.append(
                AuditFinding(
                    check_id="work_packet_schema::frontier_extra::closeout_missing_required_gates",
                    message="Frontier Extra closeout packets must include mix-depth lint, runtime evidence, gate coverage, and final claim guard.",
                    details={"missing_gates": missing, "required_gates": sorted(required_gates)},
                )
            )


def _check_runtime_probe_evidence(
    *,
    profile: Mapping[str, Any],
    profile_id: str,
    runtime_claims: set[str],
    required_gates: set[str],
    findings: list[AuditFinding],
) -> None:
    required_evidence = _string_list(profile.get("required_evidence"))
    if "runtime_evidence_gate" not in required_gates:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::runtime_claim_missing_runtime_evidence_gate",
                message="Runtime probe, materialization, handoff, or economics claims require runtime_evidence_gate.",
                details={"profile_id": profile_id, "claims": sorted(runtime_claims), "required_gates": sorted(required_gates)},
            )
        )
    if not _strings_contain_any(required_evidence, RUNTIME_PROBE_EVIDENCE_TERMS):
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::runtime_claim_missing_probe_evidence",
                message="Runtime-related claims must name narrow runtime probe evidence instead of relying on procedural review.",
                details={"profile_id": profile_id, "claims": sorted(runtime_claims), "required_evidence": required_evidence},
            )
        )
    missing_proof_terms = _missing_required_evidence_terms(required_evidence, RUNTIME_PROOF_EVIDENCE_TERMS)
    if missing_proof_terms:
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::runtime_claim_missing_identity_proof_fields",
                message="Runtime, ONNX, EA, or MT5 claims must predeclare identity and output proof fields.",
                details={"profile_id": profile_id, "claims": sorted(runtime_claims), "missing_evidence_terms": missing_proof_terms},
            )
        )
    if _strings_contain_any(required_evidence, COMPILE_ONLY_EVIDENCE_TERMS) and not _strings_contain_any(required_evidence, TESTER_RUNTIME_EVIDENCE_TERMS):
        findings.append(
            AuditFinding(
                check_id="work_packet_schema::verification_profile::compile_only_not_runtime_evidence",
                message="Compile evidence alone cannot satisfy runtime probe evidence.",
                details={"profile_id": profile_id, "claims": sorted(runtime_claims), "required_evidence": required_evidence},
            )
        )
    _check_runtime_probe_deferral_reasons(profile.get("gates_not_run_with_reason"), runtime_claims, findings)


def _check_runtime_probe_deferral_reasons(value: Any, runtime_claims: set[str], findings: list[AuditFinding]) -> None:
    if _is_missing(value) or not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return
    for index, raw_item in enumerate(value):
        item = _mapping(raw_item)
        if not item:
            continue
        if str(item.get("gate", "")).strip() != "runtime_evidence_gate":
            continue
        reason_code = str(item.get("reason_code", "")).strip().lower()
        if reason_code in DISALLOWED_RUNTIME_DEFERRAL_REASON_CODES:
            findings.append(
                AuditFinding(
                    check_id="work_packet_schema::verification_profile::runtime_probe_cost_deferral_forbidden",
                    message="Runtime probe evidence cannot be skipped as too expensive when runtime-related claims are protected.",
                    details={"index": index, "reason_code": reason_code, "claims": sorted(runtime_claims)},
                )
            )


def _check_runtime_learning_probe_deferral_reasons(value: Any, findings: list[AuditFinding]) -> None:
    if _is_missing(value) or not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return
    for index, raw_item in enumerate(value):
        item = _mapping(raw_item)
        if not item:
            continue
        if str(item.get("gate", "")).strip() != "runtime_learning_probe_decision_gate":
            continue
        reason_code = str(item.get("reason_code", "")).strip().lower()
        if reason_code in DISALLOWED_RUNTIME_DEFERRAL_REASON_CODES:
            findings.append(
                AuditFinding(
                    check_id="work_packet_schema::verification_profile::runtime_learning_probe_skip_forbidden",
                    message="runtime_learning_probe_decision_gate cannot be skipped because a proxy or candidate gate looked weak.",
                    details={"index": index, "reason_code": reason_code},
                )
            )


def _claims_from_packet(packet: Mapping[str, Any], profile: Mapping[str, Any]) -> set[str]:
    claims: set[str] = set()
    claims.update(_string_list(profile.get("protected_claims")))
    claim_surface = _mapping(profile.get("claim_surface"))
    claims.update(_string_list(claim_surface.get("allowed_claims")))
    claims.update(_string_list(_mapping(packet.get("final_claim_policy")).get("allowed_claims")))
    claim_boundary = _mapping(_mapping(packet.get("interpreted_scope")).get("claim_boundary"))
    claims.update(_string_list(claim_boundary.get("allowed_claims")))
    return {claim.strip() for claim in claims if claim.strip()}


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _string_list(value: Any) -> list[str]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [str(item) for item in value if str(item).strip()]
    return []


def _strings_contain_any(items: Sequence[str], terms: Sequence[str]) -> bool:
    lowered_items = [item.lower() for item in items]
    return any(term in item for item in lowered_items for term in terms)


def _missing_required_evidence_terms(items: Sequence[str], terms: Sequence[str]) -> list[str]:
    lowered_blob = "\n".join(item.lower() for item in items)
    return [term for term in terms if term not in lowered_blob]


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) == 0
    return False


def _looks_like_non_run_action(requested_action: str, work_families: tuple[str, ...]) -> bool:
    if work_families:
        return not any(family in RUN_FAMILIES for family in work_families)
    lowered = requested_action.lower()
    return any(term in lowered for term in ("state", "sync", "policy", "code_refactor", "kpi", "report_only"))


def _packet_text(packet: Mapping[str, Any]) -> str:
    parts: list[str] = []

    def visit(value: Any) -> None:
        if isinstance(value, Mapping):
            for nested in value.values():
                visit(nested)
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            for nested in value:
                visit(nested)
        elif value is not None:
            parts.append(str(value))

    visit(packet)
    return "\n".join(parts).lower()


def _looks_like_broad_onnx_frontier_goal(packet_text: str) -> bool:
    has_onnx = any(term in packet_text for term in BROAD_ONNX_TERMS)
    has_broad_frontier_shape = any(term in packet_text for term in BROAD_FRONTIER_GOAL_TERMS)
    return has_onnx and has_broad_frontier_shape


def _looks_like_frontier_extra_closeout(packet_text: str) -> bool:
    has_extra = "stage_frontier_extra" in packet_text or "frontier extra" in packet_text or "전선 추가" in packet_text
    has_closeout = "closeout" in packet_text or "stage_closeout" in packet_text or "마감" in packet_text
    return has_extra and has_closeout


def _looks_like_canonical_frontier_open(packet_text: str) -> bool:
    if "frontier extra" in packet_text or "stage_frontier_extra" in packet_text or "전선 추가" in packet_text:
        return False
    has_frontier = "stage_frontier_" in packet_text or "frontier" in packet_text or "전선" in packet_text
    has_open_shape = any(term in packet_text for term in FRONTIER_STAGE_OPEN_TERMS)
    return has_frontier and has_open_shape


def _normalized_lifecycle(value: Any) -> str:
    return str(value or "").strip().lower()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Project Obsidian work packet schema.")
    parser.add_argument("path")
    parser.add_argument("--output-json")
    parser.add_argument("--allow-blocked-exit-zero", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = audit_work_packet_schema_path(Path(args.path))
    payload = result.to_dict()
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output_json:
        output = Path(args.output_json)
        io_path(output.parent).mkdir(parents=True, exist_ok=True)
        io_path(output).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if args.allow_blocked_exit_zero or result.status == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
