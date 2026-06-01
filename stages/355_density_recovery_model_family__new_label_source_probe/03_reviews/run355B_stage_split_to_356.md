# run355B Stage Split To Stage356(run355B 356단계 분기)

- source_stage_id(원천 단계 ID): `355_density_recovery_model_family__new_label_source_probe`
- source_completed_run_id(완료 원천 실행 ID): `run355B_materialize_density_recovery_label_inputs_without_db_v1`
- split_run_id(분기 실행 ID): `run356A_branch_stage355_to_density_recovery_proxy_training_without_db_v1`
- superseded_run_id(대체된 실행 ID): `run355C_train_density_recovery_proxy_models_without_db_v1`
- next_stage_id(다음 단계 ID): `356_density_recovery_training__proxy_model_queue_scout`
- next_run_id(다음 실행 ID): `run356B_train_density_recovery_proxy_models_without_db_v1`
- status(상태): `split_to_stage356_proxy_training(356단계 프록시 학습으로 분기)`

Action(행동): Stage355(355단계)는 timestamp-safe label materialization(시점 안전 라벨 물질화)까지 닫고, model training(모델 학습)은 Stage356(356단계)으로 분리했다.

Effect(효과): 다음 재진입(re-entry, 재진입)은 186600행 label table(라벨 표) 전체 맥락을 다시 읽기보다, 학습 대기열(training queue, 학습 대기열) 4행에서 바로 시작한다.

Boundary(경계): 새 model training(모델 학습), proxy execution(프록시 실행), MT5 execution(MT5 실행), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
