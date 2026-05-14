# BaselineAdapter Initial Contract(BaselineAdapter 초기 계약)

- adapter_id(어댑터 ID): `baseline_adapter_v0_stage56_run50BR_v64`
- anchor(기준점): `v64_v47_ctxgap14_refill_etfw_h2_no_b`
- selected_research_baseline(선택 연구 기준선): `none`
- label(라벨): `development_anchor`
- claim_boundary(주장 경계): `development_anchor_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference`

## Fixed Capabilities(고정 기능)

- `entry_decision`
- `tier_routing_or_tier_b_disablement`
- `model_controlled_risk_per_trade`
- `atr_bracket_decision`
- `hold_lifecycle_reentry`
- `mt5_execution_translation`
- `telemetry_recording`
- `onnx_compatible_outputs`

## Initial Rules(초기 규칙)

- entry_signal_column(진입 신호 컬럼): `stage56_context_gap_refill_signal`
- routing_mode(라우팅 모드): `tier_a_primary_with_explicit_tier_b_disablement`
- tier_b_policy(Tier B 정책): `disabled_initially_due_negative_fallback_only_evidence`
- risk_cap_pct(위험 상한): `0.05`
- min_lot(최소 랏): `0.01`
- ATR bracket(ATR 브래킷): period(기간) `14`, SL `1.5`, TP `2.0`

## Required Telemetry(필수 텔레메트리)

- `adapter_id`
- `anchor_variant_id`
- `entry_signal`
- `entry_decision`
- `tier_scope`
- `route_code`
- `tier_b_policy`
- `atr_stop_multiplier`
- `atr_take_profit_multiplier`
- `max_hold_bars`
- `reentry_cooldown_bars`
- `model_risk_pct`
- `clipped_risk_pct`
- `computed_lot`
- `executed_lot`
- `min_lot_floor_applied`
- `actual_risk_pct_after_floor`

ONNX-compatible outputs(ONNX 호환 출력)는 계약에만 잡고, ONNX hardening(ONNX 경화)은 adapter MT5 validation/OOS(어댑터 MT5 검증/표본외) 이후에 시작한다.
