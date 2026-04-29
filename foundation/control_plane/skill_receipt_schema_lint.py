from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult
from foundation.control_plane.ledger import io_path, path_exists


def audit_skill_receipt_schemas(
    receipts: Sequence[Mapping[str, Any]],
    *,
    schema_path: Path = Path("docs/agent_control/skill_receipt_schema.yaml"),
    root: Path = Path("."),
    requested_claims: Sequence[str] = (),
) -> AuditResult:
    schema = _load_schema(root / schema_path)
    schemas = schema.get("schemas", {}) if isinstance(schema, Mapping) else {}
    if not isinstance(schemas, Mapping):
        schemas = {}
    findings: list[AuditFinding] = []

    for index, receipt in enumerate(receipts):
        skill = str(receipt.get("skill", ""))
        receipt_status = str(receipt.get("status", ""))
        receipt_path = str(receipt.get("receipt_path", ""))
        if receipt_path and not path_exists(root / receipt_path):
            findings.append(
                AuditFinding(
                    check_id=f"skill_receipt_schema::{skill or index}::path_missing",
                    message="Skill receipt path does not exist.",
                    details={"receipt_path": receipt_path},
                )
            )
        required = _required_fields_for_skill(schemas, skill)
        if receipt_status == "executed":
            missing = [field for field in required if _is_missing(receipt.get(field))]
            if missing:
                findings.append(
                    AuditFinding(
                        check_id=f"skill_receipt_schema::{skill}::missing_fields",
                        message="Executed skill receipt is missing required content fields.",
                        details={"missing": missing},
                    )
                )
        forbidden = set(str(item) for item in receipt.get("forbidden_claims", ()) if item)
        requested = set(str(item) for item in requested_claims)
        conflict = sorted(forbidden.intersection(requested))
        if conflict:
            findings.append(
                AuditFinding(
                    check_id=f"skill_receipt_schema::{skill}::claim_conflict",
                    message="Requested final claim conflicts with a skill receipt forbidden claim.",
                    details={"conflicting_claims": conflict},
                )
            )

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    return AuditResult(
        audit_name="skill_receipt_schema_lint",
        status=status,
        findings=tuple(findings),
        counts={"receipt_count": len(receipts), "schema_path": schema_path.as_posix()},
        allowed_claims=("completed",) if status == "pass" else ("partial", "blocked"),
        forbidden_claims=() if status == "pass" else tuple(sorted(COMPLETION_CLAIMS)),
    )


def load_receipts(path: Path) -> list[Mapping[str, Any]]:
    payload = json.loads(io_path(path).read_text(encoding="utf-8-sig"))
    rows = payload.get("receipts", payload) if isinstance(payload, Mapping) else payload
    if not isinstance(rows, list):
        raise ValueError("skill receipt JSON must be a list or an object with a `receipts` list")
    return [row for row in rows if isinstance(row, Mapping)]


def _load_schema(path: Path) -> Mapping[str, Any]:
    if not path_exists(path):
        return {}
    payload = yaml.safe_load(io_path(path).read_text(encoding="utf-8-sig"))
    return payload if isinstance(payload, Mapping) else {}


def _required_fields_for_skill(schemas: Mapping[str, Any], skill: str) -> tuple[str, ...]:
    payload = schemas.get(skill, {})
    if not isinstance(payload, Mapping):
        payload = schemas.get("default", {})
    if not isinstance(payload, Mapping):
        return ("packet_id", "skill", "status")
    fields = payload.get("required_fields", ("packet_id", "skill", "status"))
    return tuple(str(field) for field in fields)


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) == 0
    return False


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Project Obsidian skill receipt content schema.")
    parser.add_argument("skill_receipt_json")
    parser.add_argument("--schema-path", default="docs/agent_control/skill_receipt_schema.yaml")
    parser.add_argument("--root", default=".")
    parser.add_argument("--requested-claim", action="append", default=[])
    parser.add_argument("--output-json")
    parser.add_argument("--allow-blocked-exit-zero", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root)
    result = audit_skill_receipt_schemas(
        load_receipts(Path(args.skill_receipt_json)),
        schema_path=Path(args.schema_path),
        root=root,
        requested_claims=tuple(args.requested_claim),
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
