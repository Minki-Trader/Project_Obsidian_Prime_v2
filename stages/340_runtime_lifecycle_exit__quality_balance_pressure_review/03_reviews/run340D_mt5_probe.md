# run340D F01 Local Floor Pressure MT5 Probe(340D F01 로컬 하한 압박 MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `run340D_execute_f01_local_floor_pressure_mt5_probe_without_db_v1`
- status(상태): `completed_stage340D_f01_local_floor_pressure_mt5_probe_executed_review_required_no_selection`
- judgment(판정): `mt5_f01_local_floor_pressure_probe_outputs_available_review_required_no_selection`
- gates(게이트): `9/9`
- attempts(시도): `10`
- runtime_completed_rows(런타임 완료 행): `10`
- report_completed_rows(보고서 완료 행): `10`
- matched_rows(일치 행): `58270/58270`
- mismatch_rows(불일치 행): `0`
- best_attempt(최고 시도): `p09_s545_l51_m01_h12`
- best_net_profit(최고 순수익): `-25.81`
- best_profit_factor(최고 수익 팩터): `0.78`
- best_expectancy(최고 기대값): `-0.65`
- best_recovery_factor(최고 회복 계수): `-0.32`
- best_trade_count(최고 거래수): `40`
- best_long_short(최고 롱/숏): `14/26`
- external_verification_status(외부 검증 상태): `completed(완료)`
- next_run(다음 실행): `run340E_review_f01_local_floor_pressure_mt5_probe_without_db_v1`

## Action(행동)

run340C(340C 실행)의 f01(에프01) pressure variants(압박 변형)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고 telemetry(기록)를 expected tape(예상 테이프)와 비교했다.

## Effect(효과)

f01(에프01) local floor pass(로컬 하한 통과)가 threshold/min_margin/hold(임계값/최소 마진/보유) 압박에서 유지되는지 review(검토)할 수 있는 MT5 KPI(MT5 핵심 성과 지표)를 만든다.

## Boundary(경계)

run340D(340D 실행)는 runtime probe attempt(런타임 탐침 시도)다. selected model(선정 모델), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
