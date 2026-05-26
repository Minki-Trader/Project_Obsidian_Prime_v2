# run335J Proxy-MT5 Existing Runtime Comparison(335J 프록시-MT5 기존 런타임 비교)

- run_id(실행 ID): `run335J_materialize_proxy_expected_values_and_mt5_runtime_probe_attempts_or_block_v1`
- parent_run_id(부모 실행 ID): `run335I_design_proxy_expected_and_mt5_runtime_probe_or_block_v1`
- status(상태): `completed_proxy_expected_and_existing_mt5_runtime_result_comparison_no_selection`
- judgment(판정): `proxy_mt5_comparison_completed_diagnostic_only_no_forward_decision`
- decision(결정): `stage335J_proxy_mt5_existing_runtime_comparison_diagnostic_usable_not_forward_usable_no_selection`
- difference_rows(차이 행): `132`
- missing_numeric_rows(숫자 누락 행): `0`
- diagnostic_usable_rows(진단 활용 가능 행): `11/11`
- forward_not_usable_rows(전진 판정 활용 불가 행): `11/11`
- failed_gates(실패 게이트): `0`
- next_action(다음 행동): `run335K_repair_independent_proxy_mt5_runtime_probe_materialization_v1`

Effect(효과): run335I(335I 실행)의 설계를 실제 숫자 proxy expected value(프록시 예상값)와 기존 Stage330E/334D MT5 runtime result(메타트레이더5 런타임 결과)로 채웠고, 132개 차이 비교를 만들었다.

Usability(활용 가능성): 진단과 repair prioritization(수리 우선순위)에는 `usable_with_boundary`다. 하지만 proxy(프록시)와 MT5(메타트레이더5)가 일부 같은 기존 런타임 근거를 공유하므로 Forward Passed/Failed(전진 통과/실패)나 Goal Achieve(목표 달성)에는 쓸 수 없다.

Boundary(경계): candidate selection(후보 선택), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed`다.
