# run356B Density Recovery Proxy Training(run356B 밀도 회복 프록시 학습)

- run_id(실행 ID): `run356B_train_density_recovery_proxy_models_without_db_v1`
- parent_run_id(부모 실행 ID): `run356A_branch_stage355_to_density_recovery_proxy_training_without_db_v1`
- status(상태): `completed_stage356B_proxy_training_no_density_stress_queue_expand_required_no_selection`
- judgment(판정): `negative_proxy_training_scout_no_density_stress_edge_queue_no_operating_claim`
- decision(결정): `stage356B_open_run356C_expand_density_recovery_proxy_training_search_without_db_v1`
- next_run_id(다음 실행 ID): `run356C_expand_density_recovery_proxy_training_search_without_db_v1`
- trained_models(학습 모델): `12`
- threshold_sweep_rows(임계값 탐색 행): `6480`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `0`
- gates(게이트): `12/12`

Action(행동): 4개 density recovery label(밀도 회복 라벨)을 3개 ONNX-compatible model family(온엑스 호환 모델 계열)로 학습하고, validation/OOS(검증/표본외)에서 non-overlap proxy trade(비중첩 프록시 거래)를 압박 비용(stress cost, 압박 비용)으로 평가했다.

Effect(효과): proxy(프록시)에서 MT5 runtime probe(MT5 런타임 탐침)로 보낼 queue(대기열)가 있는지 확인했고, proxy result(프록시 결과)는 운영 주장(operating claim, 운영 주장)으로 쓰지 않는다.

## Best Proxy Row(최선 프록시 행)

- model_id(모델 ID): `run356B_d01_h6_cost_buffer__lgbm_depth4_leaf31_lr003`
- label_variant_id(라벨 변형 ID): `d01_h6_cost_buffer`
- validation_stress_net(검증 압박 순수익): `0.12775819374738198`
- oos_stress_net(표본외 압박 순수익): `0.004359062761285799`
- validation_trade_per_day(검증 일별 거래수): `0.08743169398907104`
- oos_trade_per_day(표본외 일별 거래수): `0.06870229007633588`
- candidate_gate(후보 게이트): `failed_proxy_scout_queue(프록시 탐색 대기열 실패)`

## Boundary(경계)

MT5 execution(MT5 실행), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 `not_claimed(주장 안 함)`이다.
