# Decision(결정): Stage362A Long-Only Margin Grid Branch(롱 단독 마진 격자 분기)

- date(날짜): `2026-06-02`
- run_id(실행 ID): `run362A_branch_stage361_to_long_only_margin_grid_without_db_v1`
- source_stage_id(원천 단계 ID): `361_long_only_cost_buffer__validation_oos_positive_cost_failure`
- target_stage_id(대상 단계 ID): `362_long_only_margin_grid__cost_buffer_first_branch`
- superseded_run_id(대체된 실행 ID): `run361B_materialize_long_only_cost_buffer_inputs_without_db_v1`
- next_run_id(다음 실행 ID): `run362B_materialize_q05_long_only_margin_grid_without_db_v1`
- judgment(판정): `stage_branch_completed_stage361_materialization_queue_split_to_stage362_margin_grid_no_operating_claim`
- claim_boundary(주장 경계): `state_sync_stage_branch_user_requested_long_only_margin_grid_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Action(행동): Stage361B(361B 실행)의 5개 materialization queue(구체화 대기열)를 바로 수행하지 않고, 첫 번째 q05 long-only margin grid(q05 롱 단독 마진 격자)를 Stage362(362단계)로 분기했다.

Effect(효과): work packet(작업 묶음)이 작아지고, +0.30 cost buffer(+0.30 비용 버퍼) 실패 원인을 가장 단순한 margin surface(마진 표면)에서 먼저 확인한다.

## Claim Boundary(주장 경계)

새 model training(모델 학습), proxy execution(프록시 실행), MT5 execution(MT5 실행), candidate selection(후보 선택), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 없다.
