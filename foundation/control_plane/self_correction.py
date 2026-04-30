from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult
from foundation.control_plane.ledger import io_path, path_exists


DEFAULT_POLICY_PATH = Path("docs/agent_control/self_correction_policy.yaml")
PASS_STATUSES = {"pass", "complete", "completed", "reduced_scope"}
MODES = ("plan_only", "safe_autofix", "guarded_autofix")


def audit_self_correction_plan(
    audit_payloads: Iterable[Mapping[str, Any]],
    *,
    mode: str = "plan_only",
    policy: Mapping[str, Any] | None = None,
) -> AuditResult:
    if mode not in MODES:
        raise ValueError(f"mode must be one of {', '.join(MODES)}")

    policy_payload = policy or {}
    safe_allowlist = set(_string_list(policy_payload.get("safe_autofix_allowlist")))
    forbidden_actions = set(_string_list(policy_payload.get("forbidden_actions")))
    source_audits: list[str] = []
    repair_items: list[dict[str, Any]] = []

    for payload in audit_payloads:
        audit_name = str(payload.get("audit_name", payload.get("packet_id", "unknown_audit")))
        source_audits.append(audit_name)
        if _audit_passed(payload):
            continue
        findings = _findings(payload)
        if not findings:
            findings = (
                {
                    "check_id": f"{audit_name}::blocked_without_findings",
                    "message": "Audit did not pass but did not include structured findings.",
                    "severity": "blocking",
                    "details": {},
                },
            )
        for finding in findings:
            repair_items.append(
                _repair_item_for_finding(
                    audit_name=audit_name,
                    finding=finding,
                    safe_allowlist=safe_allowlist,
                    forbidden_actions=forbidden_actions,
                )
            )

    mode_config = _mapping(_mapping(policy_payload.get("modes")).get(mode))
    findings = [
        AuditFinding(
            check_id=f"self_correction::{item['failure_kind']}",
            message="A source audit failure needs a repair plan before completion can be claimed.",
            details=item,
        )
        for item in repair_items
    ]
    if mode != "plan_only":
        findings.append(
            AuditFinding(
                check_id=f"self_correction::{mode}::proposal_only",
                message="This harness records autofix eligibility but does not mutate files in this entry point.",
                severity="warning" if not repair_items else "blocking",
                details={"requested_mode": mode, "mutation_performed": False},
            )
        )

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    return AuditResult(
        audit_name="self_correction_plan",
        status=status,
        findings=tuple(findings),
        counts={
            "mode": mode,
            "mode_mutates_files": bool(mode_config.get("mutates_files", False)),
            "mutation_performed": False,
            "source_audits": source_audits,
            "repair_item_count": len(repair_items),
            "safe_autofix_eligible_count": sum(1 for item in repair_items if item["safe_autofix_eligible"]),
            "guarded_autofix_count": sum(1 for item in repair_items if item["default_repair_mode"] == "guarded_autofix"),
            "repair_items": repair_items,
        },
        allowed_claims=("self_correction_not_needed",) if status == "pass" else ("repair_plan_ready", "blocked"),
        forbidden_claims=() if status == "pass" else tuple(sorted(COMPLETION_CLAIMS)),
    )


def _repair_item_for_finding(
    *,
    audit_name: str,
    finding: Mapping[str, Any],
    safe_allowlist: set[str],
    forbidden_actions: set[str],
) -> dict[str, Any]:
    check_id = str(finding.get("check_id", "unknown_check"))
    details = _mapping(finding.get("details"))
    failure_kind, action, default_mode = _classify(audit_name, check_id, details)
    target_gates = _string_list(details.get("missing_required_gates"))
    if not target_gates and "gate" in details:
        target_gates = [str(details["gate"])]
    action_forbidden = action in forbidden_actions
    return {
        "source_audit": audit_name,
        "source_check_id": check_id,
        "failure_kind": failure_kind,
        "message": str(finding.get("message", "")),
        "recommended_action": action,
        "default_repair_mode": default_mode,
        "safe_autofix_eligible": action in safe_allowlist and not action_forbidden,
        "action_forbidden": action_forbidden,
        "target_gates": target_gates,
        "details": dict(details),
    }


def _classify(audit_name: str, check_id: str, details: Mapping[str, Any]) -> tuple[str, str, str]:
    lowered = f"{audit_name}::{check_id}".lower()
    if "required_gate_coverage" in lowered and "missing_required_gates" in lowered:
        return "missing_closeout_gate_execution", "attach_existing_audit_json_to_closeout", "safe_autofix"
    if "detected" in lowered and "required_gate" in lowered:
        return "missing_required_gate_declaration", "add_missing_required_gate", "safe_autofix"
    if audit_name == "skill_receipt_lint" or check_id.startswith("skill::"):
        if "not_used_reason" in lowered:
            return "missing_skill_receipt", "normalize_skills_not_used_reason", "safe_autofix"
        return "missing_skill_receipt", "add_or_fix_skill_receipt", "guarded_autofix"
    if "schema" in lowered:
        return "schema_invalid", "fix_schema_or_packet_shape", "guarded_autofix"
    if "state_sync" in lowered:
        return "state_sync_mismatch", "sync_current_truth_or_block_merge", "guarded_autofix"
    if "code_surface" in lowered:
        return "code_surface_violation", "split_large_module_or_move_owner_logic", "guarded_autofix"
    if "final_claim_guard" in lowered or check_id.startswith("claim::"):
        return "final_claim_blocked", "withhold_completion_claim_until_source_audits_pass", "plan_only"
    if "test" in lowered:
        return "test_failure", "fix_behavior_or_test_contract", "guarded_autofix"
    if "ops_instruction" in lowered or "agent_control_contracts" in lowered:
        return "schema_invalid", "fix_schema_or_packet_shape", "guarded_autofix"
    if details.get("requires_user_decision"):
        return "human_decision_required", "stop_and_request_decision", "plan_only"
    return "human_decision_required", "stop_and_request_decision", "plan_only"


def _audit_passed(payload: Mapping[str, Any]) -> bool:
    status = str(payload.get("status", "blocked"))
    if status not in PASS_STATUSES:
        return False
    if payload.get("completed_forbidden") is True:
        return False
    return not any(_is_blocking(finding) for finding in _findings(payload))


def _findings(payload: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    findings = payload.get("findings", ())
    if isinstance(findings, Sequence) and not isinstance(findings, (str, bytes)):
        return tuple(finding for finding in findings if isinstance(finding, Mapping))
    return ()


def _is_blocking(finding: Mapping[str, Any]) -> bool:
    return str(finding.get("severity", "blocking")) == "blocking"


def _load_policy(path: Path) -> Mapping[str, Any]:
    if not path_exists(path):
        return {}
    payload = yaml.safe_load(io_path(path).read_text(encoding="utf-8-sig"))
    return payload if isinstance(payload, Mapping) else {}


def _load_audit_payloads(paths: Sequence[Path]) -> list[Mapping[str, Any]]:
    payloads: list[Mapping[str, Any]] = []
    for path in paths:
        payload = json.loads(io_path(path).read_text(encoding="utf-8-sig"))
        if not isinstance(payload, Mapping):
            raise ValueError(f"{path} must contain an audit object")
        payloads.extend(_flatten_audit_payload(payload))
    return payloads


def _flatten_audit_payload(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    flattened: list[Mapping[str, Any]] = []
    audits = payload.get("audits")
    if isinstance(audits, Sequence) and not isinstance(audits, (str, bytes)):
        flattened.extend(audit for audit in audits if isinstance(audit, Mapping))
    final_guard = payload.get("final_claim_guard")
    if isinstance(final_guard, Mapping):
        flattened.append(final_guard)
    if flattened:
        return flattened
    return [payload]


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _string_list(value: Any) -> list[str]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [str(item) for item in value if str(item).strip()]
    return []


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a plan-only repair report from failed control-plane audits.")
    parser.add_argument("--audit-json", action="append", default=[], help="AuditResult JSON or closeout_gate JSON to inspect.")
    parser.add_argument("--policy", default=str(DEFAULT_POLICY_PATH))
    parser.add_argument("--mode", choices=MODES, default="plan_only")
    parser.add_argument("--output-json")
    parser.add_argument("--allow-blocked-exit-zero", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = audit_self_correction_plan(
        _load_audit_payloads([Path(path) for path in args.audit_json]),
        mode=args.mode,
        policy=_load_policy(Path(args.policy)),
    )
    payload = result.to_dict()
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output_json:
        _write_json(Path(args.output_json), payload)
    print(text)
    return 0 if args.allow_blocked_exit_zero or result.status == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
