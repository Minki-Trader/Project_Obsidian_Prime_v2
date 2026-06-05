# 2026-06-01 Stage348A Branch Decision(348A 분기 결정)

- decision(결정): `stage348A_open_run348B_review_cash_open_asymmetric_proxy_training`
- from(출발): `347_cash_open_asymmetric_source__long_short_head_design` / `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- to(도착): `348_cash_open_proxy_review__long_oos_gap_short_carry_triage` / `run348B_review_cash_open_asymmetric_proxy_training_without_db_v1`
- superseded_planned_run(대체된 예정 실행): `run347D_review_cash_open_asymmetric_source_proxy_training_without_db_v1`
- reason(이유): Stage347(347단계)이 design/materialization/proxy training(설계/물질화/프록시 학습)까지 안고 있어 무거워졌고, 다음 질문은 proxy review/triage(프록시 검토/분류)라는 별도 topic pivot(주제 전환)이기 때문이다.

Action(행동): Stage348(348단계)을 열고 run348B(348B 실행)를 review packet(검토 묶음)으로 둔다.
Effect(효과): run347C proxy training(347C 프록시 학습)은 source truth(원천 진실)로 보존하고, 검토는 새 stage(단계)에서 작게 시작한다.

claim_boundary(주장 경계): `state_sync_stage_branch_proxy_review_handoff_only_no_new_training_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
