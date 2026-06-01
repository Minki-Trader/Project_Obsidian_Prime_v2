# run355A Density Recovery Design(355A 밀도 회복 설계)

- run_id(실행 ID): `run355A_design_density_recovery_label_model_source_without_db_v1`
- status(상태): `completed_stage355A_density_recovery_design_queue_opened_no_selection`
- judgment(판정): `experiment_design_completed_new_label_model_source_queue_no_operating_claim`
- decision(결정): `stage355A_open_run355B_materialize_density_recovery_label_inputs`
- design_rows(설계 행): `5`
- materialization_queue_rows(물질화 대기열 행): `3`
- next_run_id(다음 실행 ID): `run355B_materialize_density_recovery_label_inputs_without_db_v1`

## Action(행동)

Stage354C(354C 실행)의 negative memory(부정 기억)를 설계 제약으로 바꾸고, 새 label/source/model family(라벨/원천/모델 계열) 후보를 정리했다.

## Effect(효과)

다음 실행은 기존 probability surface(확률 표면)의 threshold-only search(임계값 전용 탐색)를 반복하지 않고, 라벨과 모델 원천을 바꿔 trade/day(일별 거래수) 3+와 cost stress(비용 압박)를 같이 본다.

## Priority Queue(우선순위 대기열)

- priority 1(우선순위 1): `d01_microtrend_cost_buffer_fwd6_fwd8`
- priority 2(우선순위 2): `d02_triple_barrier_path_quality_fwd12`
- priority 3(우선순위 3): `d03_asymmetric_long_short_heads`

## Source Truth(원천 진실)

- stage354C_sweep_rows(354C 스윕 행): `6912`
- stage354C_density_valid_queue_rows(354C 밀도 유효 대기열 행): `0`
- source_failure_rows(원천 실패 행): `1`

## Boundary(경계)

이 결과는 experiment design(실험 설계)이다. training(학습), proxy execution(프록시 실행), MT5 execution(MT5 실행), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
