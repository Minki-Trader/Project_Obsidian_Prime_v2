from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult
from foundation.control_plane.ledger import io_path


RESERVED_GATE_KEYS = {
    "required",
    "actual_status_source",
    "not_applicable_with_reason",
    "declared_not_implemented",
}


def audit_required_gate_coverage(
    work_packet: Mapping[str, Any],
    closeout_gate: Mapping[str, Any],
    *,
    extra_executed_audits: Sequence[str] = (),
) -> AuditResult:
    required_gates = _required_gates(work_packet)
    not_applicable = _reason_mapping(_mapping(work_packet.get("gates")).get("not_applicable_with_reason"))
    declared_not_implemented = _reason_mapping(_mapping(work_packet.get("gates")).get("declared_not_implemented"))
    executed_audits = _executed_audits(closeout_gate, extra_executed_audits=extra_executed_audits)
    findings: list[AuditFinding] = []

    missing = sorted(required_gates - executed_audits - set(not_applicable) - set(declared_not_implemented))
    if missing:
        findings.append(
            AuditFinding(
                check_id="required_gate_coverage::missing_required_gates",
                message="Required gates were declared in the work packet but not executed in closeout.",
                details={"missing_required_gates": missing},
            )
        )

    if declared_not_implemented:
        findings.append(
            AuditFinding(
                check_id="required_gate_coverage::declared_not_implemented",
                message="A required gate is declared but not implemented; completion claims are forbidden.",
                details={"declared_not_implemented": dict(declared_not_implemented)},
            )
        )

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    return AuditResult(
        audit_name="required_gate_coverage_audit",
        status=status,
        findings=tuple(findings),
        counts={
            "required_gates": sorted(required_gates),
            "executed_audits": sorted(executed_audits),
            "not_applicable_with_reason": dict(not_applicable),
            "declared_not_implemented": dict(declared_not_implemented),
        },
        allowed_claims=("gate_coverage_complete",) if status == "pass" else ("blocked",),
        forbidden_claims=() if status == "pass" else tuple(sorted(COMPLETION_CLAIMS)),
    )


def audit_required_gate_coverage_paths(
    work_packet_path: Path,
    closeout_gate_path: Path,
    *,
    extra_executed_audits: Sequence[str] = (),
) -> AuditResult:
    return audit_required_gate_coverage(
        _load_mapping(work_packet_path),
        _load_mapping(closeout_gate_path),
        extra_executed_audits=extra_executed_audits,
    )


def _required_gates(work_packet: Mapping[str, Any]) -> set[str]:
    required: set[str] = set()
    risk_scan = _mapping(work_packet.get("risk_vector_scan"))
    required.update(_string_list(risk_scan.get("required_gates")))

    gates = _mapping(work_packet.get("gates"))
    if "required" in gates:
        required.update(_string_list(gates.get("required")))
    else:
        for key in gates:
            if key not in RESERVED_GATE_KEYS:
                required.add(str(key))
    return {gate for gate in required if gate}


def _executed_audits(closeout_gate: Mapping[str, Any], *, extra_executed_audits: Sequence[str]) -> set[str]:
    executed = set(str(item) for item in extra_executed_audits if item)
    audits = closeout_gate.get("audits", ())
    if isinstance(audits, Sequence) and not isinstance(audits, (str, bytes)):
        for audit in audits:
            if isinstance(audit, Mapping):
                audit_name = audit.get("audit_name")
                if audit_name:
                    executed.add(str(audit_name))
    final_guard = closeout_gate.get("final_claim_guard")
    if isinstance(final_guard, Mapping):
        audit_name = final_guard.get("audit_name")
        if audit_name:
            executed.add(str(audit_name))
    return executed


def _reason_mapping(value: Any) -> Mapping[str, str]:
    if isinstance(value, Mapping):
        return {str(key): str(reason) for key, reason in value.items() if key and str(reason).strip()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return {str(item): "declared_without_structured_reason" for item in value if item}
    return {}


def _string_list(value: Any) -> list[str]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [str(item) for item in value if item]
    return []


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _load_mapping(path: Path) -> Mapping[str, Any]:
    text = io_path(path).read_text(encoding="utf-8-sig")
    payload = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(payload, Mapping):
        raise ValueError(f"{path} must contain a mapping")
    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit that required gates declared in a work packet executed in closeout.")
    parser.add_argument("--work-packet", required=True)
    parser.add_argument("--closeout-gate", required=True)
    parser.add_argument("--extra-executed-audit", action="append", default=[])
    parser.add_argument("--output-json")
    parser.add_argument("--allow-blocked-exit-zero", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = audit_required_gate_coverage_paths(
        Path(args.work_packet),
        Path(args.closeout_gate),
        extra_executed_audits=tuple(args.extra_executed_audit),
    )
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
