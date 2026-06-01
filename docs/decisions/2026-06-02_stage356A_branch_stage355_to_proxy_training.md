# Decision(결정): Stage356A Branch(356A 단계 분기)

- date(날짜): `2026-06-02`
- source_stage(원천 단계): `355_density_recovery_model_family__new_label_source_probe`
- new_stage(새 단계): `356_density_recovery_training__proxy_model_queue_scout`
- branch_run(분기 실행): `run356A_branch_stage355_to_density_recovery_proxy_training_without_db_v1`
- next_run(다음 실행): `run356B_train_density_recovery_proxy_models_without_db_v1`

Action(행동): Stage355(355단계)가 너무 무거워졌다는 사용자 요청에 따라, label materialization(라벨 물질화)은 Stage355(355단계)에 남기고 proxy model training(프록시 모델 학습)은 Stage356(356단계)으로 분리했다.

Effect(효과): 다음 작업은 작은 training queue ref(학습 대기열 참조) 4행에서 시작하고, 대형 feature_label_table(피처 라벨 표)은 hash/manifest(해시/목록)로 연결된다.

Claim Boundary(주장 경계): `state_sync_stage_branch_user_requested_proxy_training_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
