from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence


REQUIRED_CAPABILITIES = (
    "entry_decision",
    "tier_routing_or_tier_b_disablement",
    "model_controlled_risk_per_trade",
    "atr_bracket_decision",
    "hold_lifecycle_reentry",
    "mt5_execution_translation",
    "telemetry_recording",
    "onnx_compatible_outputs",
)

RISK_TELEMETRY_FIELDS = (
    "model_risk_pct",
    "clipped_risk_pct",
    "computed_lot",
    "executed_lot",
    "min_lot_floor_applied",
    "actual_risk_pct_after_floor",
)

DECISION_TELEMETRY_FIELDS = (
    "adapter_id",
    "anchor_variant_id",
    "entry_signal",
    "entry_decision",
    "tier_scope",
    "route_code",
    "tier_b_policy",
    "atr_stop_multiplier",
    "atr_take_profit_multiplier",
    "max_hold_bars",
    "reentry_cooldown_bars",
)


@dataclass(frozen=True)
class BaselineAdapterAnchor:
    anchor_id: str
    run_id: str
    variant_id: str
    source_stage_id: str
    report_path: str
    summary_path: str
    audit_path: str
    selected_research_baseline: str
    development_label: str


@dataclass(frozen=True)
class BracketDecision:
    atr_period: int
    atr_stop_multiplier: float
    atr_take_profit_multiplier: float
    max_hold_bars: int
    reentry_cooldown_bars: int


@dataclass(frozen=True)
class RiskSizingDecision:
    model_risk_pct: float
    clipped_risk_pct: float
    computed_lot: float
    executed_lot: float
    min_lot_floor_applied: bool
    actual_risk_pct_after_floor: float | None


@dataclass(frozen=True)
class BaselineAdapterContract:
    adapter_id: str
    version: str
    anchor: BaselineAdapterAnchor
    capabilities: tuple[str, ...]
    entry_signal_column: str
    entry_source: str
    routing_mode: str
    tier_b_policy: str
    risk_cap_pct: float
    min_lot: float
    default_bracket: BracketDecision
    onnx_output_names: tuple[str, ...]
    telemetry_required_fields: tuple[str, ...]
    claim_boundary: str


def risk_sizing_decision(
    model_risk_pct: float,
    computed_lot: float,
    *,
    risk_cap_pct: float = 0.05,
    min_lot: float = 0.01,
) -> RiskSizingDecision:
    model_risk = max(float(model_risk_pct), 0.0)
    clipped_risk = min(model_risk, float(risk_cap_pct))
    raw_lot = max(float(computed_lot), 0.0)
    floor_applied = raw_lot < float(min_lot)
    executed_lot = float(min_lot) if floor_applied else raw_lot
    if raw_lot > 0.0:
        actual_risk = clipped_risk * executed_lot / raw_lot
    elif clipped_risk == 0.0:
        actual_risk = 0.0
    else:
        actual_risk = None
    return RiskSizingDecision(
        model_risk_pct=model_risk,
        clipped_risk_pct=clipped_risk,
        computed_lot=raw_lot,
        executed_lot=executed_lot,
        min_lot_floor_applied=floor_applied,
        actual_risk_pct_after_floor=actual_risk,
    )


def onnx_compatible_output_schema() -> tuple[str, ...]:
    return (
        "entry_signal",
        "route_code",
        "model_risk_pct",
        "atr_stop_multiplier",
        "atr_take_profit_multiplier",
        "max_hold_bars",
        "reentry_cooldown_bars",
    )


def telemetry_fields() -> tuple[str, ...]:
    return DECISION_TELEMETRY_FIELDS + RISK_TELEMETRY_FIELDS


def initial_v64_contract() -> BaselineAdapterContract:
    anchor = BaselineAdapterAnchor(
        anchor_id="development_anchor_stage56_run50BR_v64",
        run_id="run50BR_stage56_context_extratrees_context_gap_refill_v1",
        variant_id="v64_v47_ctxgap14_refill_etfw_h2_no_b",
        source_stage_id="56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection",
        report_path=(
            "stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/"
            "03_reviews/run50BR_context_extratrees_context_gap_refill.md"
        ),
        summary_path=(
            "stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/"
            "03_reviews/run50BR_summary.csv"
        ),
        audit_path=(
            "stages/56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection/"
            "03_reviews/run50BR_audit.csv"
        ),
        selected_research_baseline="none",
        development_label="development_anchor",
    )
    return BaselineAdapterContract(
        adapter_id="baseline_adapter_v0_stage56_run50BR_v64",
        version="baseline_adapter_contract_v0",
        anchor=anchor,
        capabilities=REQUIRED_CAPABILITIES,
        entry_signal_column="stage56_context_gap_refill_signal",
        entry_source="context_primary_gap14_plus_et40_slot_fill_firewall",
        routing_mode="tier_a_primary_with_explicit_tier_b_disablement",
        tier_b_policy="disabled_initially_due_negative_fallback_only_evidence",
        risk_cap_pct=0.05,
        min_lot=0.01,
        default_bracket=BracketDecision(
            atr_period=14,
            atr_stop_multiplier=1.5,
            atr_take_profit_multiplier=2.0,
            max_hold_bars=2,
            reentry_cooldown_bars=0,
        ),
        onnx_output_names=onnx_compatible_output_schema(),
        telemetry_required_fields=telemetry_fields(),
        claim_boundary=(
            "development_anchor_only_no_live_readiness_no_runtime_authority_"
            "no_operating_promotion_no_operating_reference"
        ),
    )


def validate_contract_capabilities(contract: BaselineAdapterContract) -> list[str]:
    present = set(contract.capabilities)
    return [name for name in REQUIRED_CAPABILITIES if name not in present]


def adapter_contract_payload(contract: BaselineAdapterContract | None = None) -> dict[str, Any]:
    selected = contract or initial_v64_contract()
    missing = validate_contract_capabilities(selected)
    payload = asdict(selected)
    payload["capability_check"] = {
        "required": list(REQUIRED_CAPABILITIES),
        "missing": missing,
        "status": "passed" if not missing else "failed",
    }
    payload["risk_rule"] = {
        "risk_per_trade_owner": "model_output",
        "risk_cap_pct": selected.risk_cap_pct,
        "min_lot_floor": selected.min_lot,
        "floor_rule": "execute_min_lot_when_computed_lot_is_below_min_lot",
        "required_telemetry": list(RISK_TELEMETRY_FIELDS),
    }
    payload["onnx_rule"] = {
        "status": "compatible_output_contract_only",
        "start_condition": "after_adapter_mt5_validation_oos_and_telemetry_are_recorded",
        "outputs": list(selected.onnx_output_names),
    }
    return payload


def telemetry_record(
    contract: BaselineAdapterContract,
    *,
    entry_signal: int,
    tier_scope: str,
    model_risk_pct: float,
    computed_lot: float,
    route_code: int = 0,
    bracket: BracketDecision | None = None,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    selected_bracket = bracket or contract.default_bracket
    risk = risk_sizing_decision(
        model_risk_pct,
        computed_lot,
        risk_cap_pct=contract.risk_cap_pct,
        min_lot=contract.min_lot,
    )
    decision = "long" if int(entry_signal) > 0 else "short" if int(entry_signal) < 0 else "flat"
    payload: dict[str, Any] = {
        "adapter_id": contract.adapter_id,
        "anchor_variant_id": contract.anchor.variant_id,
        "entry_signal": int(entry_signal),
        "entry_decision": decision,
        "tier_scope": tier_scope,
        "route_code": int(route_code),
        "tier_b_policy": contract.tier_b_policy,
        "atr_stop_multiplier": selected_bracket.atr_stop_multiplier,
        "atr_take_profit_multiplier": selected_bracket.atr_take_profit_multiplier,
        "max_hold_bars": selected_bracket.max_hold_bars,
        "reentry_cooldown_bars": selected_bracket.reentry_cooldown_bars,
    }
    payload.update(asdict(risk))
    if extra:
        payload.update(dict(extra))
    return payload


def missing_telemetry_fields(record: Mapping[str, Any], required: Sequence[str] | None = None) -> list[str]:
    fields = tuple(required or telemetry_fields())
    return [field for field in fields if field not in record]
