# Stage356 Density Recovery Training(356단계 밀도 회복 학습)

- current_run(현재 실행): `run356B_train_density_recovery_proxy_models_without_db_v1`
- branch_run(분기 실행): `run356A_branch_stage355_to_density_recovery_proxy_training_without_db_v1`
- source_stage(원천 단계): `355_density_recovery_model_family__new_label_source_probe`
- source_run(원천 실행): `run355B_materialize_density_recovery_label_inputs_without_db_v1`
- claim_boundary(주장 경계): `state_sync_stage_branch_user_requested_proxy_training_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Action(행동): Stage355B(355B 실행)의 라벨 물질화 산출물을 Stage356(356단계)의 proxy model training(프록시 모델 학습) 입력으로 넘긴다.

Effect(효과): Stage355(355단계)의 무거운 label/source/model family(라벨/원천/모델 계열) 문맥과 Stage356(356단계)의 학습 탐색 문맥이 분리된다.
