from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from foundation.control_plane.audit_result import AuditFinding, AuditResult, COMPLETION_CLAIMS
from foundation.control_plane.ledger import io_path


AUDIT_NAME = "runtime_learning_probe_decision_gate"

FORBIDDEN_NOT_RUN_REASON_CODES = frozenset(
    {
        "agent_recommended_skip",
        "candidate_0",
        "candidate_gate_0",
        "candidate_gate_failed",
        "candidate_gate_zero",
        "cost_expensive",
        "expensive",
        "long_short_imbalanced",
        "low_pf_dd",
        "low_trade_count_expected",
        "not_promotion_candidate",
        "not_strong_candidate",
        "pf_dd_poor",
        "proxy_bad",
        "proxy_result_bad",
        "too_expensive",
    }
)

ALLOWED_NOT_RUN_REASON_CODES_AFTER_REPAIR = frozenset(
    {
        "data_invalid_pre_runtime",
        "explicit_user_scope_excludes_mt5",
        "mt5_environment_blocked_after_attempt",
        "no_deterministic_decision_rule_after_repair",
        "no_entry_exit_translation_after_repair",
        "no_runtime_substrate_after_repair",
        "no_signal_rows_after_repair",
    }
)

RUN_ACTIONS = frozenset({"run_probe", "run_after_repair"})
NOT_RUN_ACTIONS = frozenset({"not_run_blocked", "not_run_after_repair_impossible"})
ALLOWED_ACTIONS = RUN_ACTIONS | NOT_RUN_ACTIONS
REPAIR_REQUIRED_STATUSES = frozenset({"repair_required", "no_actionable_runtime_surface"})

DECISION_REQUIRED_FIELDS = (
    "pre_gate_signal_count",
    "strong_candidate_count",
    "runtime_learning_probe_candidate_count",
    "runtime_surface_status",
    "mt5_action",
    "not_run_reason_code",
    "repair_attempt_required",
    "repair_attempts",
    "forbidden_skip_basis_seen",
    "claim_effect",
)


def audit_runtime_learning_probe_decision(decision: Mapping[str, Any]) -> AuditResult:
    findings: list[AuditFinding] = []
    _check_required_fields(decision, findings)

    strong_candidate_count = _int_value(decision.get("strong_candidate_count"))
    learning_candidate_count = _int_value(decision.get("runtime_learning_probe_candidate_count"))
    pre_gate_signal_count = _int_value(decision.get("pre_gate_signal_count"))
    runtime_surface_status = _norm(decision.get("runtime_surface_status"))
    mt5_action = _norm(decision.get("mt5_action"))
    not_run_reason_code = _norm(decision.get("not_run_reason_code"))
    repair_attempt_required = _bool_value(decision.get("repair_attempt_required"))
    repair_attempts = _list_value(decision.get("repair_attempts"))
    forbidden_seen = _list_value(decision.get("forbidden_skip_basis_seen"))

    if mt5_action and mt5_action not in ALLOWED_ACTIONS:
        findings.append(
            AuditFinding(
                check_id=f"{AUDIT_NAME}::unknown_mt5_action",
                message="mt5_action must use the runtime learning decision vocabulary.",
                details={"mt5_action": mt5_action, "allowed": sorted(ALLOWED_ACTIONS)},
            )
        )

    forbidden_reason_hits = sorted(
        {
            code
            for code in [not_run_reason_code, *(_norm(item) for item in forbidden_seen)]
            if code in FORBIDDEN_NOT_RUN_REASON_CODES
        }
    )
    if forbidden_reason_hits:
        findings.append(
            AuditFinding(
                check_id=f"{AUDIT_NAME}::forbidden_skip_reason",
                message="MT5 runtime learning probe cannot be skipped because the proxy or strong-candidate gate is poor.",
                details={"forbidden_reason_codes": forbidden_reason_hits},
            )
        )

    if learning_candidate_count > 0 and mt5_action not in RUN_ACTIONS:
        findings.append(
            AuditFinding(
                check_id=f"{AUDIT_NAME}::learning_candidate_requires_mt5_action",
                message="A runtime_learning_probe_candidate requires run_probe or run_after_repair.",
                details={
                    "runtime_learning_probe_candidate_count": learning_candidate_count,
                    "strong_candidate_count": strong_candidate_count,
                    "mt5_action": mt5_action,
                },
            )
        )

    if mt5_action in RUN_ACTIONS and learning_candidate_count <= 0:
        findings.append(
            AuditFinding(
                check_id=f"{AUDIT_NAME}::run_action_without_learning_candidate",
                message="A run_probe action must name at least one runtime learning probe candidate.",
                details={"runtime_learning_probe_candidate_count": learning_candidate_count, "mt5_action": mt5_action},
            )
        )

    repair_required = repair_attempt_required or runtime_surface_status in REPAIR_REQUIRED_STATUSES
    if repair_required and not repair_attempts:
        findings.append(
            AuditFinding(
                check_id=f"{AUDIT_NAME}::repair_required_without_attempt",
                message="A missing actionable runtime surface must get at least one repair attempt before no-run closeout.",
                details={
                    "runtime_surface_status": runtime_surface_status,
                    "repair_attempt_required": repair_attempt_required,
                    "repair_attempt_count": len(repair_attempts),
                },
            )
        )

    if mt5_action == "run_after_repair" and not repair_attempts:
        findings.append(
            AuditFinding(
                check_id=f"{AUDIT_NAME}::run_after_repair_without_repair_attempt",
                message="run_after_repair requires at least one recorded repair attempt.",
                details={"mt5_action": mt5_action},
            )
        )

    if mt5_action in NOT_RUN_ACTIONS:
        if not_run_reason_code not in ALLOWED_NOT_RUN_REASON_CODES_AFTER_REPAIR:
            findings.append(
                AuditFinding(
                    check_id=f"{AUDIT_NAME}::not_run_reason_not_allowed",
                    message="A no-run decision needs an allowed post-repair or environment-blocked reason.",
                    details={
                        "not_run_reason_code": not_run_reason_code,
                        "allowed_after_repair": sorted(ALLOWED_NOT_RUN_REASON_CODES_AFTER_REPAIR),
                    },
                )
            )
        if not_run_reason_code != "explicit_user_scope_excludes_mt5" and not repair_attempts:
            findings.append(
                AuditFinding(
                    check_id=f"{AUDIT_NAME}::not_run_without_repair_attempt",
                    message="A no-run runtime learning decision needs repair or environment-attempt evidence.",
                    details={"mt5_action": mt5_action, "not_run_reason_code": not_run_reason_code},
                )
            )

    status = "blocked" if any(finding.is_blocking for finding in findings) else "pass"
    allowed_claims = ("runtime_learning_probe_decision_recorded",) if status == "pass" else ("blocked",)
    forbidden_claims = (
        ()
        if status == "pass"
        else tuple(sorted(COMPLETION_CLAIMS | {"runtime_verified", "economics_pass", "materialization_ready", "handoff_complete"}))
    )
    return AuditResult(
        audit_name=AUDIT_NAME,
        status=status,
        findings=tuple(findings),
        counts={
            "pre_gate_signal_count": pre_gate_signal_count,
            "strong_candidate_count": strong_candidate_count,
            "runtime_learning_probe_candidate_count": learning_candidate_count,
            "repair_attempt_count": len(repair_attempts),
            "runtime_surface_status": runtime_surface_status,
            "mt5_action": mt5_action,
        },
        allowed_claims=allowed_claims,
        forbidden_claims=forbidden_claims,
    )


def audit_runtime_learning_probe_decision_path(path: Path) -> AuditResult:
    text = io_path(path).read_text(encoding="utf-8-sig")
    payload = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(payload, Mapping):
        return AuditResult(
            audit_name=AUDIT_NAME,
            status="blocked",
            findings=(
                AuditFinding(
                    check_id=f"{AUDIT_NAME}::not_mapping",
                    message="runtime learning probe decision must be a mapping.",
                    details={"path": path.as_posix()},
                ),
            ),
            forbidden_claims=tuple(sorted(COMPLETION_CLAIMS)),
        )
    decision = payload.get("runtime_learning_probe_decision", payload)
    if not isinstance(decision, Mapping):
        return AuditResult(
            audit_name=AUDIT_NAME,
            status="blocked",
            findings=(
                AuditFinding(
                    check_id=f"{AUDIT_NAME}::decision_not_mapping",
                    message="runtime_learning_probe_decision must be a mapping.",
                    details={"path": path.as_posix()},
                ),
            ),
            forbidden_claims=tuple(sorted(COMPLETION_CLAIMS)),
        )
    return audit_runtime_learning_probe_decision(decision)


def _check_required_fields(decision: Mapping[str, Any], findings: list[AuditFinding]) -> None:
    missing = [field for field in DECISION_REQUIRED_FIELDS if field not in decision]
    if missing:
        findings.append(
            AuditFinding(
                check_id=f"{AUDIT_NAME}::missing_required_fields",
                message="runtime_learning_probe_decision is missing required fields.",
                details={"missing": missing},
            )
        )


def _norm(value: Any) -> str:
    return str(value or "").strip().lower()


def _int_value(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return _norm(value) in {"1", "true", "yes", "required"}


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return list(value)
    return [value]


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit runtime learning probe decisions.")
    parser.add_argument("decision_path")
    parser.add_argument("--output-json")
    parser.add_argument("--allow-blocked-exit-zero", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = audit_runtime_learning_probe_decision_path(Path(args.decision_path))
    payload = result.to_dict()
    if args.output_json:
        _write_json(Path(args.output_json), payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.allow_blocked_exit_zero:
        return 0
    return 2 if result.completed_forbidden else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
