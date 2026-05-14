from __future__ import annotations

from foundation.adapters.baseline_adapter import (
    adapter_contract_payload,
    initial_v64_contract,
    missing_telemetry_fields,
    risk_sizing_decision,
    telemetry_record,
    validate_contract_capabilities,
)


def test_initial_contract_has_all_required_capabilities() -> None:
    contract = initial_v64_contract()

    assert contract.anchor.variant_id == "v64_v47_ctxgap14_refill_etfw_h2_no_b"
    assert contract.anchor.selected_research_baseline == "none"
    assert validate_contract_capabilities(contract) == []
    assert contract.tier_b_policy.startswith("disabled_initially")


def test_model_risk_is_capped_and_min_lot_floor_is_recorded() -> None:
    decision = risk_sizing_decision(0.08, 0.004)

    assert decision.model_risk_pct == 0.08
    assert decision.clipped_risk_pct == 0.05
    assert decision.computed_lot == 0.004
    assert decision.executed_lot == 0.01
    assert decision.min_lot_floor_applied is True
    assert decision.actual_risk_pct_after_floor == 0.125


def test_telemetry_record_contains_required_risk_and_decision_fields() -> None:
    contract = initial_v64_contract()
    record = telemetry_record(
        contract,
        entry_signal=1,
        tier_scope="Tier A",
        model_risk_pct=0.03,
        computed_lot=0.02,
    )

    assert missing_telemetry_fields(record, contract.telemetry_required_fields) == []
    assert record["entry_decision"] == "long"
    assert record["executed_lot"] == 0.02
    assert record["min_lot_floor_applied"] is False


def test_contract_payload_marks_onnx_as_later_hardening_not_completion() -> None:
    payload = adapter_contract_payload()

    assert payload["capability_check"]["status"] == "passed"
    assert payload["onnx_rule"]["status"] == "compatible_output_contract_only"
    assert "after_adapter_mt5_validation_oos" in payload["onnx_rule"]["start_condition"]
