from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping

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
RUN_ONLY_FIELDS = ("variants_requested", "verification_layers", "mt5_required", "top_k_reduction_allowed")
RUN_FAMILIES = ("experiment_execution", "runtime_backtest")


def audit_work_packet_schema(packet: Mapping[str, Any]) -> AuditResult:
    findings: list[AuditFinding] = []
    version = str(packet.get("version", "work_packet_schema_v1"))
    requested_action = str(_mapping(packet.get("user_request")).get("requested_action", ""))
    has_v2_fields = any(key in packet for key in ("work_classification", "risk_vector_scan", "decision_lock", "work_plan"))

    if version.endswith("_v2") or has_v2_fields:
        _require_top_level(packet, V2_REQUIRED, findings, version="v2")
        interpreted = _mapping(packet.get("interpreted_scope"))
        _require_fields(interpreted, V2_SCOPE_REQUIRED, findings, prefix="interpreted_scope")
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
    return AuditResult(
        audit_name="work_packet_schema_lint",
        status=status,
        findings=tuple(findings),
        counts={"version": version, "has_v2_fields": has_v2_fields},
        allowed_claims=("work_packet_schema_valid",) if status == "pass" else ("blocked",),
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


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _looks_like_non_run_action(requested_action: str, work_families: tuple[str, ...]) -> bool:
    if work_families:
        return not any(family in RUN_FAMILIES for family in work_families)
    lowered = requested_action.lower()
    return any(term in lowered for term in ("state", "sync", "policy", "code_refactor", "kpi", "report_only"))


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
