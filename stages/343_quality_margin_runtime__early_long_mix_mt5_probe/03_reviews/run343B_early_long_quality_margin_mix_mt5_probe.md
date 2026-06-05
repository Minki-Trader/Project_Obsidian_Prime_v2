# run343B Early Long Quality Margin Mix MT5 Probe(343B 초반 롱 품질/마진 혼합 MT5 탐침)

## Summary(요약)

- run_id(실행 ID): `run343B_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- status(상태): `completed_stage343B_early_long_quality_margin_mix_mt5_probe_executed_review_required_no_selection`
- judgment(판정): `mt5_early_long_quality_margin_mix_probe_outputs_available_review_required_no_selection`
- gates(게이트): `10/10`
- source_package(원천 패키지): `run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1`
- attempts(시도): `8`
- runtime_completed_rows(런타임 완료 행): `8`
- report_completed_rows(보고서 완료 행): `8`
- matched_rows(일치 행): `46616/46616`
- mismatch_rows(불일치 행): `0`
- best_attempt(최고 시도): `h04_q02_l515_blk45`
- best_net_profit(최고 순수익): `152.79`
- best_profit_factor(최고 수익 팩터): `3.55`
- best_expectancy(최고 기대값): `6.95`
- best_recovery_factor(최고 회복 계수): `1.71`
- best_drawdown(최고 시도 낙폭): `89.31`
- best_trade_count(최고 거래수): `22`
- best_long_short(최고 롱/숏): `2/20`
- external_verification_status(외부 검증 상태): `completed(완료)`
- next_run(다음 실행): `run343C_review_early_long_quality_margin_mix_mt5_probe_without_db_v1`

## Action(행동)

run342H(342H 실행)의 early-long quality/margin mix(초반 롱 품질/마진 혼합) ONNX package(온엑스 패키지)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행하고, expected tape(예상 테이프)와 telemetry(런타임 기록)를 비교한다.

## Effect(효과)

run343C(343C 실행)가 trade count(거래수), profit factor(수익 팩터), expectancy(기대값), drawdown(낙폭), recovery factor(회복 계수), long/short balance(롱/숏 균형), proxy-MT5 diff(프록시-MT5 차이)를 실제 런타임 근거로 검토할 수 있다.

## Boundary(경계)

run343B(343B 실행)는 runtime probe attempt(런타임 탐침 시도)다. selected model(선정 모델), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
