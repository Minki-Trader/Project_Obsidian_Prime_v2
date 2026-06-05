# run339G Quality Balance Blend MT5 Probe(품질-균형 혼합 MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `run339G_execute_quality_balance_blend_mt5_probe_without_db_v1`
- status(상태): `completed_stage339G_quality_balance_blend_mt5_probe_executed_review_required_no_selection`
- judgment(판정): `mt5_quality_balance_blend_probe_outputs_available_review_required_no_selection`
- gates(게이트): `9/9`
- attempts(시도): `10`
- runtime_completed_rows(런타임 완료 행): `10`
- report_completed_rows(보고서 완료 행): `10`
- matched_rows(일치 행): `58270/58270`
- mismatch_rows(불일치 행): `0`
- best_attempt(최고 시도): `f01_s55_l51_m01_h12`
- best_net_profit(최고 순수익): `122.9`
- best_profit_factor(최고 수익 팩터): `1.89`
- best_recovery_factor(최고 회복 계수): `1.38`
- best_trade_count(최고 거래수): `33`
- best_long_short(최고 롱/숏): `13/20`
- external_verification_status(외부 검증 상태): `completed(완료)`
- next_run(다음 실행): `run339H_review_quality_balance_blend_mt5_probe_without_db_v1`

## Action(행동)

run339F(339F 실행)의 quality-balance blend(품질-균형 혼합) package(패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고 telemetry(기록)를 expected tape(예상 테이프)와 비교했다.

## Effect(효과)

min_margin(최소 마진)이 weak long(약한 롱)을 줄이면서 trade_count(거래수), side_balance(방향 균형), recovery factor(회복 계수)를 동시에 회복하는지 review(검토)할 수 있게 했다.

## Boundary(경계)

run339G(339G 실행)는 runtime probe attempt(런타임 탐침 시도)다. selected model(선정 모델), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
