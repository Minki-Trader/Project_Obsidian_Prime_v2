# run349B ONNX Short-Carry MT5 Probe(349B 온엑스 숏 기여 MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`
- status(상태): `completed_stage349B_onnx_short_carry_mt5_probe_executed_review_required_no_selection`
- judgment(판정): `mt5_onnx_short_carry_probe_outputs_available_proxy_diff_and_trade_density_review_required_no_selection`
- gates(게이트): `10/10`
- source_package(원천 패키지): `run348C_materialize_onnx_deployable_short_carry_probe_package_without_db_v1`
- attempts(시도): `4`
- runtime_completed_rows(런타임 완료 행): `4`
- report_completed_rows(보고서 완료 행): `4`
- matched_rows(일치 행): `6904/23308`
- diff_mismatch_rows(차이 행): `16404`
- best_attempt(최고 시도): `c03_xtrees_cashopen_q95q90`
- best_net_profit(최고 순수익): `-197.95`
- best_profit_factor(최고 수익 팩터): `0.89`
- best_expectancy(최고 기대값): `-0.44`
- best_recovery_factor(최고 회복 계수): `-0.41`
- best_trade_count(최고 거래 수): `451`
- best_trade_density(최고 일일 거래 밀도): `4.254716981132075`
- trade_density_status(거래 밀도 상태): `meets_min_3_to_10_band(최소 3~10 구간 충족)`
- external_verification_status(외부 검증 상태): `completed(완료)`

## Action(행동)

Stage348(348단계)의 ONNX short-carry package(온엑스 숏 기여 패키지)를 복사하지 않고, Stage349(349단계)에서 `.set/.ini` 실행 adapter(어댑터)만 새로 만들어 MT5 Strategy Tester(MT5 전략 테스터)를 실행했다.

## Effect(효과)

Stage348(348단계)는 package handoff(패키지 인계)로 가볍게 유지되고, Stage349(349단계)는 runtime output(런타임 출력), tester report(테스터 보고서), proxy-MT5 diff(프록시-MT5 차이), trade density(거래 밀도)를 별도 evidence(근거)로 가진다.

## Boundary(경계)

이 run(실행)은 runtime probe(런타임 탐침)이다. selected model(선정 모델), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
