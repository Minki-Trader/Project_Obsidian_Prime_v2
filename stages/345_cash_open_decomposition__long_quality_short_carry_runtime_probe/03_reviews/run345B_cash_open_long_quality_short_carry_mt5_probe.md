# run345B Cash-Open Long Quality/Short Carry MT5 Probe(345B 현금장 롱 품질/숏 기여 MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1`
- status(상태): `completed_stage345B_cash_open_long_quality_short_carry_mt5_probe_executed_review_required_no_selection`
- judgment(판정): `mt5_cash_open_long_quality_short_carry_outputs_available_review_required_no_selection`
- gates(게이트): `10/10`
- source_package(원천 패키지): `run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1`
- attempts(시도): `6`
- runtime_completed_rows(런타임 완료 행): `6`
- report_completed_rows(보고서 완료 행): `6`
- matched_rows(일치 행): `34962/34962`
- mismatch_rows(불일치 행): `0`
- best_attempt(최고 시도): `n01_s07_base_control`
- best_net_profit(최고 순수익): `186.67`
- best_profit_factor(최고 수익 팩터): `4.11`
- best_expectancy(최고 기대값): `7.18`
- best_recovery_factor(최고 회복 계수): `2.09`
- best_drawdown(최고 시도 낙폭): `89.31`
- best_trade_count(최고 거래수): `26`
- best_long_short(최고 롱/숏): `6/20`
- external_verification_status(외부 검증 상태): `completed(완료)`
- next_run(다음 실행): `run345C_review_cash_open_long_quality_short_carry_mt5_probe_without_db_v1`

## Action(행동)

run344N package(패키지)의 6개 cash-open decomposition attempt(현금장 분해 시도)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고, expected tape(예상 테이프)와 telemetry(런타임 기록)를 비교했다.

## Effect(효과)

run345C review(검토)가 net profit(순수익), profit factor(수익 팩터), expectancy(기대값), drawdown(낙폭), recovery factor(회복 계수), trade count(거래수), long/short balance(롱/숏 균형), proxy-MT5 diff(프록시-MT5 차이)를 실제 runtime evidence(런타임 근거)로 판정할 수 있다.

## Boundary(경계)

이 run(실행)은 runtime probe attempt(런타임 탐침 시도)다. selected model(선정 모델), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
