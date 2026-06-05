# run349C ONNX Short-Carry MT5 Probe Review(349C 온엑스 숏 기여 MT5 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `run349C_review_onnx_short_carry_mt5_probe_without_db_v1`
- parent_run(상위 실행): `run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`
- status(상태): `reviewed_stage349C_onnx_short_carry_mt5_probe_negative_runtime_parity_repair_required_no_selection`
- judgment(판정): `negative_runtime_probe_trade_density_partial_but_loss_and_mt5_onnx_probability_mismatch_repair_required`
- result_judgment(결과 판정): `negative(부정)`
- best_trade_attempt(거래 발생 최고 시도): `c03_xtrees_cashopen_q95q90`
- best_trade_net_profit(거래 발생 최고 순수익): `-197.95`
- best_trade_profit_factor(거래 발생 최고 수익 팩터): `0.89`
- best_trade_expectancy(거래 발생 최고 기대값): `-0.44`
- best_trade_recovery_factor(거래 발생 최고 회복 계수): `-0.41`
- best_trade_count(거래 수): `451`
- best_trade_density(거래 밀도): `4.25471698113`
- python_onnx_expected_max_abs_diff(파이썬 온엑스-예상 최대 차이): `2.159295790449267e-06`
- python_onnx_mt5_max_abs_diff(파이썬 온엑스-MT5 최대 차이): `1.0`
- next_run(다음 실행): `run349D_test_onnx_no_conversion_runtime_parity_diagnostic_without_db_v1`

## Action(행동)

run349B(349B 실행)의 MT5 KPI(MT5 핵심 성과 지표), proxy-MT5 diff(프록시-MT5 차이), Python ONNX diagnostic(파이썬 온엑스 진단)을 함께 검토했다.

## Effect(효과)

Python ONNX(파이썬 온엑스)는 expected tape(예상 테이프)와 맞지만 MT5 ONNX probabilities(MT5 온엑스 확률)가 어긋난다는 것을 분리했다. 따라서 수익 음수 결과는 운영 실패로 닫되, 다음에는 `InpModelNoConversion=true`와 tensor output handling(텐서 출력 처리)을 좁게 검증한다.

## Boundary(경계)

Negative result(부정 결과)이며 reusable evidence(재사용 근거)다. selected model(선정 모델), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
