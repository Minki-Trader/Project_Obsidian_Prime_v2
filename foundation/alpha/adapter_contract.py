from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


ADAPTER_ROLES: tuple[str, ...] = (
    "Entry",
    "Permission / Filter / Abstention",
    "Risk / Tail-risk",
    "Sizing",
    "Position Management",
    "Exit / Hold",
    "Regime / Context",
    "Runtime / Packaging",
    "Negative Memory",
    "Deferred",
)

VALID_DIRECTIONS: tuple[str, ...] = ("long", "short", "flat", "both", "none")
VALID_ACTIONS: tuple[str, ...] = (
    "emit_signal",
    "allow",
    "block",
    "abstain",
    "resize",
    "hold",
    "exit",
    "package",
    "record_only",
)


@dataclass(frozen=True)
class SignalCard:
    """Small runtime-facing decision record shared by adapter candidates."""

    role: str
    action: str
    direction: str = "none"
    score: float | None = None
    confidence: float | None = None
    reason_codes: tuple[str, ...] = ()
    safe_fallback: str = "abstain"
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AdapterContract:
    adapter_id: str
    role: str
    mechanism_class: str
    input_contract: Mapping[str, Any]
    output_contract: Mapping[str, Any]
    safe_fallback: str
    comparison_kpi: tuple[str, ...]
    readiness_status: str
    claim_boundary: str
    version: str = "adapter_contract_v1"


def validate_signal_card(card: SignalCard) -> list[str]:
    errors: list[str] = []
    if card.role not in ADAPTER_ROLES:
        errors.append(f"unknown_role:{card.role}")
    if card.action not in VALID_ACTIONS:
        errors.append(f"unknown_action:{card.action}")
    if card.direction not in VALID_DIRECTIONS:
        errors.append(f"unknown_direction:{card.direction}")
    errors.extend(_bounded_score("score", card.score))
    errors.extend(_bounded_score("confidence", card.confidence))
    if not card.safe_fallback:
        errors.append("missing_safe_fallback")
    return errors


def validate_adapter_contract(contract: AdapterContract) -> list[str]:
    errors: list[str] = []
    if not contract.adapter_id:
        errors.append("missing_adapter_id")
    if contract.role not in ADAPTER_ROLES:
        errors.append(f"unknown_role:{contract.role}")
    if not contract.mechanism_class:
        errors.append("missing_mechanism_class")
    if not contract.input_contract:
        errors.append("missing_input_contract")
    if not contract.output_contract:
        errors.append("missing_output_contract")
    if not contract.safe_fallback:
        errors.append("missing_safe_fallback")
    if not contract.comparison_kpi:
        errors.append("missing_comparison_kpi")
    if not contract.claim_boundary:
        errors.append("missing_claim_boundary")
    return errors


def signal_card_output_contract() -> dict[str, Any]:
    return {
        "type": "SignalCard",
        "required_fields": ["role", "action", "direction", "safe_fallback"],
        "optional_fields": ["score", "confidence", "reason_codes", "metadata"],
        "valid_roles": list(ADAPTER_ROLES),
        "valid_actions": list(VALID_ACTIONS),
        "valid_directions": list(VALID_DIRECTIONS),
    }


def default_safe_signal(role: str, *, reason: str) -> SignalCard:
    return SignalCard(
        role=role if role in ADAPTER_ROLES else "Deferred",
        action="abstain",
        direction="none",
        score=None,
        confidence=None,
        reason_codes=(reason,),
        safe_fallback="abstain",
    )


def _bounded_score(name: str, value: float | None) -> list[str]:
    if value is None:
        return []
    if value < 0.0 or value > 1.0:
        return [f"{name}_outside_0_1"]
    return []


def role_slug(role: str) -> str:
    return (
        role.lower()
        .replace(" / ", "_")
        .replace("/", "_")
        .replace(" ", "_")
        .replace("-", "_")
    )


def make_contract(
    *,
    adapter_id: str,
    role: str,
    mechanism_class: str,
    input_contract: Mapping[str, Any],
    comparison_kpi: Sequence[str],
    readiness_status: str,
    claim_boundary: str,
) -> AdapterContract:
    return AdapterContract(
        adapter_id=adapter_id,
        role=role,
        mechanism_class=mechanism_class,
        input_contract=dict(input_contract),
        output_contract=signal_card_output_contract(),
        safe_fallback="abstain",
        comparison_kpi=tuple(comparison_kpi),
        readiness_status=readiness_status,
        claim_boundary=claim_boundary,
    )
