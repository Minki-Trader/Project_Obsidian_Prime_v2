# Stage60 ONNX Runtime Reproduction(60단계 ONNX 런타임 재현)

- decision(판정): `proceed_to_stage61_research_package_review`
- adapter_under_review(검토 중 어댑터): `s59ar_v41_sd8_h3`
- ONNX export(ONNX 내보내기): `stages/60_adapter_onnx__hardening_runtime_reproduction/02_runs/run60A/s59ar_v41_sd8_h3/models/s59ar_v41_sd8_h3_entry_probability.onnx`
- probability_parity_passed(확률 동등성 통과): `True`
- decision_parity_passed(결정 동등성 통과): `True`
- external_verification_status(외부 검증 상태): `completed`
- runtime_gate_passed(런타임 게이트 통과): `True`

Action(행동): Stage59AR(59AR단계)의 EBM table(EBM 표)을 ONNX(모델 교환 형식)로 내보내고 같은 ATR/risk(ATR/위험), lifecycle(수명주기), Tier B disabled(Tier B 비활성) 조건으로 MT5(메타트레이더5) validation/OOS(검증/표본외)를 실행했다.
Effect(효과): Python/ONNX(파이썬/ONNX) 동등성과 MT5 runtime reproduction(MT5 런타임 재현)을 한 단계 안에서 확인하되, deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위)는 주장하지 않는다.

## Routed KPI(라우팅 KPI)

- validation_net(검증 순손익): `426.22`
- validation_pf(검증 PF): `1.17`
- validation_drawdown(검증 드로다운): `148.18`
- validation_cost_stressed_expectancy(검증 비용 스트레스 기대값): `0.6388105726872246`
- oos_net(표본외 순손익): `490.24`
- oos_pf(표본외 PF): `1.29`
- oos_drawdown(표본외 드로다운): `160.3`
- oos_cost_stressed_expectancy(표본외 비용 스트레스 기대값): `1.1855757575757575`

## Gate(게이트)

- failure_reasons(실패 이유): `none`
- next_stage_or_branch(다음 단계/분기): `61_research_package__baseline_adapter_review_only`
