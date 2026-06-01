# Decision(결정): Stage357A Branch(357A 단계 분기)

- date(날짜): `2026-06-02`
- source_stage(원천 단계): `356_density_recovery_training__proxy_model_queue_scout`
- new_stage(새 단계): `357_high_density_label_pivot__trade_frequency_recovery`
- branch_run(분기 실행): `run357A_branch_stage356_to_high_density_label_pivot_without_db_v1`
- next_run(다음 실행): `run357B_design_high_density_label_pivot_without_db_v1`

Action(행동): Stage356(356단계)이 너무 무거워졌다는 사용자 요청에 따라, density recovery training scout(밀도 회복 학습 탐색)은 Stage356(356단계)에 남기고 high-density label pivot(고밀도 라벨 전환)은 Stage357(357단계)로 분리했다.

Effect(효과): 다음 작업은 Stage357B(357B 실행)에서 H12 train-quantile label(학습 분위수 H12 라벨)과 ONNX classifier(온엑스 분류기)를 다루며, Stage356C(356C 실행)의 실패 기억은 제약으로만 재사용한다.

Claim Boundary(주장 경계): `state_sync_stage_branch_user_requested_high_density_label_pivot_handoff_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
