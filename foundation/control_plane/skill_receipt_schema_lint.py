from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.audit_result import COMPLETION_CLAIMS, AuditFinding, AuditResult
from foundation.control_plane.ledger import io_path, path_exists


TASK_FORCE_REVIEW_SKILL = "obsidian-task-force-review"
TASK_FORCE_REQUIRED_MARKERS = {
    "required",
    "gate_required",
    "packet_required",
    "family_required",
    "user_required",
    "user_instruction_required",
    "explicit_user_instruction_required",
    "active_goal_required",
    "goal_required",
    "router_selected_required",
    "router_selection_required",
    "router_overlay_required",
    "router_selected_task_force_overlay",
    "closeout_required",
    "codex_task_force_review_packet",
}
TASK_FORCE_BLOCKED_STATUSES = {
    "tool_unavailable",
    "not_called",
    "not_applicable_with_reason",
    "blocked_for_task_force_review",
}
TASK_FORCE_REVIEW_CLAIMS = {
    "reviewed",
    "verified",
    "pass",
    "stage_closeout_pass",
    "internally_reviewed",
    "rehearsed_control_plane",
    "task_force_reviewed",
}
TASK_FORCE_CALL_REQUIRED_FIELDS = (
    "roster_agent_id",
    "spawned_agent_id",
    "tool_name",
    "result_status",
    "opinion_classification",
)
TASK_FORCE_CALL_TOOL_NAME = "multi_agent_v1.spawn_agent"
TASK_FORCE_OPINION_CLASSIFICATIONS = {"accepted", "rejected", "needs_local_verification"}
TASK_FORCE_FULL_ROSTER_SIZE = 8


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
        receipt_path = str(receipt.get("receipt_path") or receipt.get("path") or "")
        if receipt_path and not path_exists(root / receipt_path):
            findings.append(
                AuditFinding(
                    check_id=f"skill_receipt_schema::{skill or index}::path_missing",
                    message="Skill receipt path does not exist.",
                    details={"receipt_path": receipt_path},
                )
            )
        required = _required_fields_for_skill(schemas, skill, receipt)
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
        if skill == TASK_FORCE_REVIEW_SKILL:
            findings.extend(_task_force_review_findings(receipt, requested_claims=requested_claims))
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


def _required_fields_for_skill(schemas: Mapping[str, Any], skill: str, receipt: Mapping[str, Any]) -> tuple[str, ...]:
    payload = schemas.get(skill, {})
    default_payload = schemas.get("default", {})
    if not isinstance(default_payload, Mapping):
        default_payload = {}
    if not isinstance(payload, Mapping):
        payload = default_payload
    if not isinstance(payload, Mapping):
        return ("packet_id", "skill", "status")
    compact_fields = payload.get("compact_required_fields")
    if _uses_compact_receipt(payload, receipt):
        if isinstance(compact_fields, Sequence) and not isinstance(compact_fields, (str, bytes)):
            return tuple(str(field) for field in compact_fields)
        default_compact_fields = default_payload.get("compact_required_fields")
        if isinstance(default_compact_fields, Sequence) and not isinstance(default_compact_fields, (str, bytes)):
            return tuple(str(field) for field in default_compact_fields)
    fields = payload.get("required_fields", ("packet_id", "skill", "status"))
    return tuple(str(field) for field in fields)


def _uses_compact_receipt(schema_payload: Mapping[str, Any], receipt: Mapping[str, Any]) -> bool:
    if str(receipt.get("receipt_mode", "")).strip().lower() == "compact":
        return True
    compact_when = schema_payload.get("compact_when")
    if not isinstance(compact_when, Mapping):
        return False
    for key, expected in compact_when.items():
        actual = receipt.get(str(key))
        if str(actual).strip().lower() != str(expected).strip().lower():
            return False
    return bool(compact_when)


def _task_force_review_findings(receipt: Mapping[str, Any], *, requested_claims: Sequence[str]) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    status = _normalized(receipt.get("status"))
    requirement = _normalized(receipt.get("review_requirement") or receipt.get("task_force_review_requirement"))
    is_required = requirement in TASK_FORCE_REQUIRED_MARKERS or bool(receipt.get("codex_task_force_review_packet_required"))
    actual_calls = receipt.get("actual_subagent_calls")

    if is_required:
        agents_used = _string_list(receipt.get("agents_used"))
        unique_agents_used = sorted(set(agents_used))
        if len(unique_agents_used) >= TASK_FORCE_FULL_ROSTER_SIZE and _is_missing(receipt.get("full_roster_call_reason")):
            findings.append(
                AuditFinding(
                    check_id="skill_receipt_schema::obsidian-task-force-review::full_roster_call_missing_reason",
                    message="Calling all Task Force agents is not the default and requires a full_roster_call_reason.",
                    details={"agents_used": unique_agents_used},
                )
            )
        if status in TASK_FORCE_BLOCKED_STATUSES:
            findings.append(
                AuditFinding(
                    check_id="skill_receipt_schema::obsidian-task-force-review::required_review_not_called",
                    message="Required Task Force review cannot pass when selected sub-agent calls are unavailable, absent, or marked not applicable.",
                    details={"status": status, "review_requirement": requirement},
                )
            )
        if _is_missing(actual_calls) or _looks_like_missing_task_force_calls(actual_calls):
            findings.append(
                AuditFinding(
                    check_id="skill_receipt_schema::obsidian-task-force-review::missing_actual_subagent_calls",
                    message="Required Task Force review needs actual selected-agent spawn_agent call evidence.",
                    details={"actual_subagent_calls": actual_calls},
                )
            )
        else:
            findings.extend(_task_force_actual_call_structure_findings(actual_calls))

    if status == "optional_not_called_no_task_force_claim":
        requested = {_normalized(claim) for claim in requested_claims}
        conflict = sorted(TASK_FORCE_REVIEW_CLAIMS.intersection(requested))
        if conflict:
            findings.append(
                AuditFinding(
                    check_id="skill_receipt_schema::obsidian-task-force-review::optional_not_called_claim_conflict",
                    message="Optional not-called Task Force checkpoint cannot support Task Force review claims.",
                    details={"conflicting_claims": conflict},
                )
            )
    return findings


def _task_force_actual_call_structure_findings(value: Any) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return [
            AuditFinding(
                check_id="skill_receipt_schema::obsidian-task-force-review::actual_subagent_calls_not_list",
                message="Task Force actual_subagent_calls must be a list of real spawn_agent call records.",
                details={"actual_type": type(value).__name__},
            )
        ]

    for index, raw_call in enumerate(value):
        if not isinstance(raw_call, Mapping):
            findings.append(
                AuditFinding(
                    check_id="skill_receipt_schema::obsidian-task-force-review::actual_subagent_call_not_mapping",
                    message="Each Task Force sub-agent call record must be a mapping.",
                    details={"index": index, "actual_type": type(raw_call).__name__},
                )
            )
            continue
        missing = [field for field in TASK_FORCE_CALL_REQUIRED_FIELDS if _is_missing(raw_call.get(field))]
        if missing:
            findings.append(
                AuditFinding(
                    check_id="skill_receipt_schema::obsidian-task-force-review::actual_subagent_call_missing_fields",
                    message="Each Task Force sub-agent call must include roster id, spawned id, tool name, result status, and opinion classification.",
                    details={"index": index, "missing": missing},
                )
            )
        tool_name = str(raw_call.get("tool_name", "")).strip()
        if tool_name and tool_name != TASK_FORCE_CALL_TOOL_NAME:
            findings.append(
                AuditFinding(
                    check_id="skill_receipt_schema::obsidian-task-force-review::actual_subagent_call_wrong_tool",
                    message="Task Force sub-agent call evidence must identify the real spawn_agent tool.",
                    details={"index": index, "tool_name": tool_name, "expected": TASK_FORCE_CALL_TOOL_NAME},
                )
            )
        opinion = _normalized(raw_call.get("opinion_classification"))
        if opinion and opinion not in TASK_FORCE_OPINION_CLASSIFICATIONS:
            findings.append(
                AuditFinding(
                    check_id="skill_receipt_schema::obsidian-task-force-review::actual_subagent_call_bad_opinion_classification",
                    message="Task Force opinion classification must be accepted, rejected, or needs_local_verification.",
                    details={"index": index, "opinion_classification": opinion, "allowed": sorted(TASK_FORCE_OPINION_CLASSIFICATIONS)},
                )
            )
    return findings


def _looks_like_missing_task_force_calls(value: Any) -> bool:
    text = _normalized(value)
    if not text:
        return True
    missing_markers = ("not_called", "tool_unavailable", "0/0", "0 of 0", "none")
    return any(marker in text for marker in missing_markers)


def _normalized(value: Any) -> str:
    return str(value or "").strip().lower()


def _string_list(value: Any) -> list[str]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [str(item) for item in value if str(item).strip()]
    return []


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
