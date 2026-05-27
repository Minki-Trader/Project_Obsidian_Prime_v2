
# Stage337Y Actual Measurement Inputs(337Y 실제 측정 입력)

- run_id(실행 ID): `run337Y_materialize_actual_source_age_proxy_mt5_repair_probe_inputs_v1`
- status(상태): `completed_stage337Y_actual_source_age_proxy_mt5_repair_probe_inputs_materialized_no_training_no_new_mt5`
- judgment(판정): `actual_source_age_and_proxy_values_materialized_runtime_probe_package_ready_tester_gap_remains_no_forward_decision`
- decision(결정): `stage337Y_open_run337Z_execute_or_review_actual_source_age_proxy_mt5_repair_probe_no_selection`
- parent_run(부모 실행): `run337X_review_materialized_cost_buffer_source_policy_repair_inputs_v1`
- next_action(다음 행동): `run337Z_execute_or_review_actual_source_age_proxy_mt5_repair_probe_v1`
- selected_candidate(선택 후보): `none`
- model training(모델 학습): `not_run`
- new MT5 execution(신규 MT5 실행): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Counts(수치)

- source timestamp rows(원천 시점 행): `12`
- source blocker rows(원천 차단/수리 행): `8`
- proxy expected rows(프록시 예상 행): `6`
- proxy-MT5 difference rows(프록시-MT5 차이 행): `30`
- tester history rows(테스터 이력 행): `6`
- split audit rows(분할 감사 행): `4`
- negative control rows(부정 대조 행): `12`
- required gates present(필수 게이트 존재): `13/13`

## Read(판독)

run337Y(337Y 실행)는 run337X(337X 실행)의 5개 hard blocker(강한 차단 요소)를 실제 파일로 바꾸는 물질화(materialization, 물질화) 작업이다. 효과(effect, 효과)는 source age(원천 나이), proxy expected value(프록시 예상값), timestamp-aligned proxy-MT5 difference(시점 정렬 프록시-MT5 차이), split membership(분할 소속), negative control(부정 대조)을 다음 MT5 reprobe(MT5 재탐침) 판단에 바로 쓸 수 있게 만든 것이다.

이번 실행은 신규 MT5(메타트레이더5)를 돌리지 않았다. 대신 run337P/run337U(337P/337U 실행)의 timestamp-aligned runtime evidence(시점 정렬 런타임 증거)를 계보와 해시로 묶고, run337Z(337Z 실행)에서 실행하거나 즉시 차단 사유를 기록해야 하는 `mt5_reprobe_manifest.json`을 만들었다.

판정은 `exploratory_runtime_probe_input_package_ready(탐색적 런타임 탐침 입력 준비)`다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 아직 금지된다.
