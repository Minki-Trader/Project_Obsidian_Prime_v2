# Stage337 run337AY Shifted Protocol Attribution(337단계 337AY 이동 경로 프로토콜 귀속)

## Purpose(목적)

run337AY(337AY 실행)는 run337AX(337AX 실행)가 고른 shifted custom exact timestamp(이동 커스텀 정확 시각) 경로를 실제 MT5(MetaTrader 5, 메타트레이더5) trade report(거래 보고서), telemetry(런타임 기록), feature matrix(피처 행렬)로 귀속했다.

Effect(효과): tester feature-last gap(테스터 피처 끝 공백)을 진단용으로 수리한 경로에서 direction/recovery/cost/curve/regime(방향/회복/비용/곡선/국면)이 어디서 약한지 확인한다.

## Findings(발견)

- shifted_trades(이동 거래): `266`
- completed_anchor_trades(완성일 앵커 거래): `344`
- shifted_net/PF/DD(이동 순익/수익 팩터/손실폭): `58.66` / `1.1` / `119.34`
- completed_net/PF/DD(완성일 순익/수익 팩터/손실폭): `99.9` / `1.13` / `112.86`
- protocol_fragility(프로토콜 취약성): cost buffer(비용 버퍼), direction symmetry(방향 대칭), recovery shape(회복 형태), trade density(거래 밀도)
- gates(게이트): `10/10`

## Judgment(판정)

shifted custom route(이동 커스텀 경로)는 feature_last(피처 끝)에 도달하고 exact proxy-MT5 parity(정확 프록시-MT5 동등성)를 유지한다. 하지만 completed-day broker anchor(완성일 브로커 앵커) 대비 net/PF/trade count/DD(순익/수익 팩터/거래수/손실폭)가 약해 no-overfit repair design(무과적합 수리 설계)로 넘긴다.

Effect(효과): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.

## Outputs(산출물)

- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AY/shifted_custom_trade_records.csv`
- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AY/protocol_attribution_matrix.csv`
- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AY/shifted_custom_regime_attribution.csv`
- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AY/cost_stress_report.csv`
- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AY/curve_pocket_report.csv`
- `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AY/required_gate_coverage_audit.csv`

## Decision(결정)

- status(상태): `completed_stage337AY_shifted_custom_protocol_attribution_fragile_no_forward_decision`
- judgment(판정): `shifted_custom_route_reaches_feature_last_but_cost_direction_recovery_and_trade_density_fragility_remain`
- decision(결정): `stage337AY_open_run337AZ_no_overfit_repair_design_from_shifted_attribution_without_db_no_selection`
- next_action(다음 행동): `run337AZ_no_overfit_repair_design_from_shifted_attribution_without_db_v1`
- claim_boundary(주장 경계): `research_development_only_stage337AY_shifted_custom_protocol_attribution_without_db_no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
