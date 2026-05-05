from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


ADAPTER_ROLE_NAMES = (
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

SIGNAL_DIRECTIONS = ("short", "flat", "long", "no_trade")
SAFE_FALLBACK_DEFAULT = "no_trade"


def feature_order_hash(feature_names: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(str(name) for name in feature_names).encode("utf-8")).hexdigest()


def normalize_roles(roles: Sequence[str]) -> tuple[str, ...]:
    known = set(ADAPTER_ROLE_NAMES)
    normalized: list[str] = []
    for role in roles:
        text = str(role).strip()
        if not text:
            continue
        if text not in known:
            raise ValueError(f"Unknown adapter role: {text}")
        if text not in normalized:
            normalized.append(text)
    if not normalized:
        raise ValueError("At least one adapter role is required.")
    return tuple(normalized)


def _finite_probability(value: float, *, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or not 0.0 <= number <= 1.0:
        raise ValueError(f"{name} must be finite and inside [0, 1].")
    return number


@dataclass(frozen=True)
class SignalCard:
    adapter_id: str
    roles: tuple[str, ...]
    direction: str
    score: float
    confidence: float
    safe_fallback: str = SAFE_FALLBACK_DEFAULT
    reason_codes: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not str(self.adapter_id).strip():
            raise ValueError("adapter_id is required.")
        object.__setattr__(self, "roles", normalize_roles(self.roles))
        if self.direction not in SIGNAL_DIRECTIONS:
            raise ValueError(f"direction must be one of {SIGNAL_DIRECTIONS}.")
        if self.safe_fallback not in SIGNAL_DIRECTIONS:
            raise ValueError(f"safe_fallback must be one of {SIGNAL_DIRECTIONS}.")
        object.__setattr__(self, "score", _finite_probability(self.score, name="score"))
        object.__setattr__(self, "confidence", _finite_probability(self.confidence, name="confidence"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "roles": list(self.roles),
            "direction": self.direction,
            "score": self.score,
            "confidence": self.confidence,
            "safe_fallback": self.safe_fallback,
            "reason_codes": list(self.reason_codes),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class AdapterInputContract:
    feature_names: tuple[str, ...] = ()
    state_names: tuple[str, ...] = ()
    missing_policy: str = SAFE_FALLBACK_DEFAULT

    def __post_init__(self) -> None:
        if self.missing_policy != SAFE_FALLBACK_DEFAULT:
            raise ValueError("Only no_trade safe fallback is supported for missing inputs.")
        if not self.feature_names and not self.state_names:
            raise ValueError("Adapter input contract requires features or state names.")

    def to_dict(self) -> dict[str, Any]:
        return {
            "feature_names": list(self.feature_names),
            "state_names": list(self.state_names),
            "feature_order_hash": feature_order_hash(self.feature_names) if self.feature_names else None,
            "missing_policy": self.missing_policy,
        }


@dataclass(frozen=True)
class AdapterOutputContract:
    output_type: str = "SignalCard.v1"
    required_fields: tuple[str, ...] = (
        "adapter_id",
        "roles",
        "direction",
        "score",
        "confidence",
        "safe_fallback",
        "reason_codes",
    )
    safe_fallback: str = SAFE_FALLBACK_DEFAULT

    def to_dict(self) -> dict[str, Any]:
        return {
            "output_type": self.output_type,
            "required_fields": list(self.required_fields),
            "safe_fallback": self.safe_fallback,
        }


@dataclass(frozen=True)
class AdapterCandidateContract:
    candidate_id: str
    source_stage_id: str
    source_run_id: str
    mechanism_class: str
    roles: tuple[str, ...]
    input_contract: AdapterInputContract
    output_contract: AdapterOutputContract = field(default_factory=AdapterOutputContract)
    safe_fallback: str = SAFE_FALLBACK_DEFAULT
    claim_boundary: str = "adapter_candidate_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"

    def __post_init__(self) -> None:
        if not str(self.candidate_id).strip():
            raise ValueError("candidate_id is required.")
        object.__setattr__(self, "roles", normalize_roles(self.roles))
        if self.safe_fallback != SAFE_FALLBACK_DEFAULT:
            raise ValueError("Adapter candidates must have no_trade safe fallback.")

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "source_stage_id": self.source_stage_id,
            "source_run_id": self.source_run_id,
            "mechanism_class": self.mechanism_class,
            "roles": list(self.roles),
            "input_contract": self.input_contract.to_dict(),
            "output_contract": self.output_contract.to_dict(),
            "safe_fallback": self.safe_fallback,
            "claim_boundary": self.claim_boundary,
        }
