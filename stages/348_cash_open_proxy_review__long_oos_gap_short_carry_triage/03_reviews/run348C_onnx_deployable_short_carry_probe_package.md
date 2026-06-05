# run348C ONNX Short-Carry Probe Package(348C 온엑스 숏 기여 탐침 패키지)

## Summary(요약)

- run_id(실행 ID): `run348C_materialize_onnx_deployable_short_carry_probe_package_without_db_v1`
- status(상태): `completed_stage348C_onnx_deployable_short_carry_probe_package_materialized_no_mt5_execution`
- judgment(판정): `runtime_probe_package_ready_feature_order_53_boundary_cash_open_rule_partial_mapping_mt5_execution_required_no_selection`
- attempts(시도): `4`
- feature_rows(피처 행): `5827`
- feature_count(피처 수): `53` vs MT5 contract(MT5 계약) `58`
- expected_rows(예상 행): `23308`
- cash_open_partial_mapping_attempts(현금장 부분 매핑 시도): `2`
- next_run(다음 실행): `run348D_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`

## Action(행동)

run348B(348B 실행)의 ONNX deployable seed(온엑스 배포 가능 씨앗) 4개를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 물질화했다.

## Effect(효과)

run348D(348D 실행)에서 Strategy Tester(전략 테스터)를 바로 실행해 proxy-MT5 diff(프록시-MT5 차이), runtime KPI(런타임 핵심 성과 지표), execution behavior(실행 행동)를 볼 수 있다.

## Boundary(경계)

이 run(실행)은 package only(패키지 전용)다. MT5 execution(MT5 실행), candidate selection(후보 선정), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
