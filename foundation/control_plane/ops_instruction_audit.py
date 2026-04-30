from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult
from foundation.control_plane.ledger import io_path, path_exists


DEFAULT_WORK_FAMILY_REGISTRY = Path("docs/agent_control/work_family_registry.yaml")
DEFAULT_SKILL_RECEIPT_SCHEMA = Path("docs/agent_control/skill_receipt_schema.yaml")
DEFAULT_WORK_PACKET_SCHEMA = Path("docs/agent_control/work_packet.schema.yaml")
DEFAULT_AGENT_TRIGGER_POLICY = Path("docs/policies/agent_trigger_policy.md")
DEFAULT_AGENTS = Path("AGENTS.md")

REQUIRED_ROUTING_CONTRACT_KEYS = (
    "primary_skill_limit",
    "support_skill_limit_default",
    "max_required_skills_per_family",
    "required_skill_order",
    "closeout_rule",
    "stage_agnostic_rule",
)
REQUIRED_FAMILY_KEYS = (
    "description",
    "mutation_default",
    "execution_default",
    "primary_skill",
    "support_skills",
    "required_skills",
    "required_gates",
)
REQUIRED_SKILL_ROUTING_FIELDS = (
    "primary_family",
    "primary_skill",
    "support_skills",
    "skills_considered",
    "skills_selected",
    "skills_not_used",
    "required_skill_receipts",
    "required_gates",
)


def audit_ops_instructions(root: Path | str = Path(".")) -> AuditResult:
    root_path = Path(root)
    findings: list[AuditFinding] = []

    family_registry = _load_mapping(root_path / DEFAULT_WORK_FAMILY_REGISTRY)
    receipt_schema = _load_mapping(root_path / DEFAULT_SKILL_RECEIPT_SCHEMA)
    work_packet_schema = _load_mapping(root_path / DEFAULT_WORK_PACKET_SCHEMA)
    agent_policy = _read_text(root_path / DEFAULT_AGENT_TRIGGER_POLICY)
    agents = _read_text(root_path / DEFAULT_AGENTS)

    routing_contract = _mapping(family_registry.get("routing_contract"))
    families = _mapping(family_registry.get("families"))
    schemas = _mapping(receipt_schema.get("schemas"))
    default_support_limit = _int_value(routing_contract.get("support_skill_limit_default"), fallback=3)
    max_required = _int_value(routing_contract.get("max_required_skills_per_family"), fallback=5)

    _check_routing_contract(routing_contract, findings)
    _check_families(root_path, families, schemas, default_support_limit, max_required, findings)
    _check_policy_surfaces(agent_policy, agents, work_packet_schema, findings)

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    return AuditResult(
        audit_name="ops_instruction_audit",
        status=status,
        findings=tuple(findings),
        counts={
            "family_count": len(families),
            "explicit_skill_schema_count": max(0, len(schemas) - (1 if "default" in schemas else 0)),
            "default_support_skill_limit": default_support_limit,
            "max_required_skills_per_family": max_required,
        },
        allowed_claims=("ops_instructions_stable",) if status == "pass" else ("blocked",),
        forbidden_claims=() if status == "pass" else tuple(sorted(COMPLETION_CLAIMS)),
    )


def _check_routing_contract(routing_contract: Mapping[str, Any], findings: list[AuditFinding]) -> None:
    for key in REQUIRED_ROUTING_CONTRACT_KEYS:
        if _is_missing(routing_contract.get(key)):
            findings.append(
                AuditFinding(
                    check_id=f"ops_instruction::routing_contract::missing::{key}",
                    message="Routing contract is missing a required stability field.",
                    details={"missing": key},
                )
            )
    if _int_value(routing_contract.get("primary_skill_limit"), fallback=0) != 1:
        findings.append(
            AuditFinding(
                check_id="ops_instruction::routing_contract::primary_skill_limit",
                message="Routing contract must limit each work packet to exactly one primary skill.",
                details={"actual": routing_contract.get("primary_skill_limit")},
            )
        )


def _check_families(
    root: Path,
    families: Mapping[str, Any],
    schemas: Mapping[str, Any],
    default_support_limit: int,
    max_required: int,
    findings: list[AuditFinding],
) -> None:
    if not families:
        findings.append(
            AuditFinding(
                check_id="ops_instruction::families::missing",
                message="Work family registry must define reusable work families.",
            )
        )
        return

    for family_name, raw_family in families.items():
        family = _mapping(raw_family)
        if re.search(r"stage\d+", str(family_name), flags=re.IGNORECASE):
            findings.append(
                AuditFinding(
                    check_id=f"ops_instruction::{family_name}::stage_specific_family",
                    message="Work family names must stay stage-agnostic for future Stage 50+ reuse.",
                    details={"family": family_name},
                )
            )

        for key in REQUIRED_FAMILY_KEYS:
            if _is_missing(family.get(key)):
                findings.append(
                    AuditFinding(
                        check_id=f"ops_instruction::{family_name}::missing::{key}",
                        message="Work family is missing a required routing field.",
                        details={"family": family_name, "missing": key},
                    )
                )

        primary = str(family.get("primary_skill", "")).strip()
        support = _string_list(family.get("support_skills"))
        required = _string_list(family.get("required_skills"))
        gates = _string_list(family.get("required_gates"))
        limit = _int_value(family.get("support_skill_limit"), fallback=default_support_limit)

        if primary and required and required[0] != primary:
            findings.append(
                AuditFinding(
                    check_id=f"ops_instruction::{family_name}::primary_not_first",
                    message="Required skill order must start with the primary skill.",
                    details={"family": family_name, "primary_skill": primary, "required_skills": required},
                )
            )
        if primary and primary in support:
            findings.append(
                AuditFinding(
                    check_id=f"ops_instruction::{family_name}::primary_duplicated_in_support",
                    message="Primary skill must not also appear as a support skill.",
                    details={"family": family_name, "primary_skill": primary},
                )
            )
        if primary and primary not in required:
            findings.append(
                AuditFinding(
                    check_id=f"ops_instruction::{family_name}::primary_missing_from_required",
                    message="Primary skill must also be listed in required_skills.",
                    details={"family": family_name, "primary_skill": primary},
                )
            )
        missing_support = [skill for skill in support if skill not in required]
        if missing_support:
            findings.append(
                AuditFinding(
                    check_id=f"ops_instruction::{family_name}::support_missing_from_required",
                    message="Support skills must be listed in required_skills so receipts can be checked.",
                    details={"family": family_name, "missing_support_skills": missing_support},
                )
            )
        if len(support) > limit:
            findings.append(
                AuditFinding(
                    check_id=f"ops_instruction::{family_name}::too_many_support_skills",
                    message="Work family selects too many support skills for stable routing.",
                    details={"family": family_name, "support_skill_count": len(support), "limit": limit},
                )
            )
        if len(required) > max_required:
            findings.append(
                AuditFinding(
                    check_id=f"ops_instruction::{family_name}::too_many_required_skills",
                    message="Work family requires too many skills for stable execution.",
                    details={"family": family_name, "required_skill_count": len(required), "limit": max_required},
                )
            )
        if not gates:
            findings.append(
                AuditFinding(
                    check_id=f"ops_instruction::{family_name}::missing_required_gates",
                    message="Work family must name at least one closeout gate.",
                    details={"family": family_name},
                )
            )

        for skill in required:
            _check_skill_available(root, family_name=str(family_name), skill=skill, schemas=schemas, findings=findings)


def _check_skill_available(
    root: Path,
    *,
    family_name: str,
    skill: str,
    schemas: Mapping[str, Any],
    findings: list[AuditFinding],
) -> None:
    skill_path = root / ".agents" / "skills" / skill / "SKILL.md"
    if not path_exists(skill_path):
        findings.append(
            AuditFinding(
                check_id=f"ops_instruction::{family_name}::{skill}::missing_skill_file",
                message="Required skill must have a repo-scoped SKILL.md file.",
                details={"family": family_name, "skill": skill, "path": skill_path.as_posix()},
            )
        )
    if skill not in schemas:
        findings.append(
            AuditFinding(
                check_id=f"ops_instruction::{family_name}::{skill}::missing_receipt_schema",
                message="Required skill must have an explicit receipt schema, not only the default schema.",
                details={"family": family_name, "skill": skill},
            )
        )


def _check_policy_surfaces(
    agent_policy: str,
    agents: str,
    work_packet_schema: Mapping[str, Any],
    findings: list[AuditFinding],
) -> None:
    policy_needles = (
        "work_family_registry.yaml",
        "primary_skill",
        "support_skills",
        "required_gates",
        "required_gate_coverage_audit",
    )
    for needle in policy_needles:
        if needle not in agent_policy:
            findings.append(
                AuditFinding(
                    check_id=f"ops_instruction::agent_trigger_policy::missing::{needle}",
                    message="Agent trigger policy must route through the primary-skill work family contract.",
                    details={"missing": needle},
                )
            )

    agent_needles = ("work_family_registry.yaml", "primary_skill", "required_gate_coverage_audit")
    for needle in agent_needles:
        if needle not in agents:
            findings.append(
                AuditFinding(
                    check_id=f"ops_instruction::agents::missing::{needle}",
                    message="AGENTS.md must expose the operating kernel and closeout gate contract.",
                    details={"missing": needle},
                )
            )

    fields = _string_list(_mapping(_mapping(work_packet_schema.get("fields")).get("skill_routing")).get("required_fields"))
    missing_fields = [field for field in REQUIRED_SKILL_ROUTING_FIELDS if field not in fields]
    if missing_fields:
        findings.append(
            AuditFinding(
                check_id="ops_instruction::work_packet_schema::missing_skill_routing_fields",
                message="Work packet schema must require primary-family routing fields.",
                details={"missing": missing_fields},
            )
        )


def _load_mapping(path: Path) -> Mapping[str, Any]:
    if not path_exists(path):
        return {}
    payload = yaml.safe_load(io_path(path).read_text(encoding="utf-8-sig"))
    return payload if isinstance(payload, Mapping) else {}


def _read_text(path: Path) -> str:
    if not path_exists(path):
        return ""
    return io_path(path).read_text(encoding="utf-8-sig")


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _string_list(value: Any) -> list[str]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [str(item) for item in value if str(item).strip()]
    return []


def _int_value(value: Any, *, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) == 0
    return False


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Project Obsidian operational instruction routing stability.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--output-json")
    parser.add_argument("--allow-blocked-exit-zero", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = audit_ops_instructions(Path(args.root))
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
