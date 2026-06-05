# 2026-06-01 Stage347A Design Decision(347A 설계 결정)

- decision(결정): `stage347A_open_run347B_materialize_cash_open_asymmetric_source_inputs`
- source_review(원천 검토): `run346B_review_cash_open_runtime_probe_source_pivot_without_db_v1`
- next_run(다음 실행): `run347B_materialize_cash_open_asymmetric_source_inputs_without_db_v1`
- reason(이유): run346B(346B 실행)가 single side-filter(단일 방향 필터)를 실패 기억으로 닫고, asymmetric long/short source(비대칭 롱/숏 원천)를 다음 공격 탐색 씨앗으로 열었기 때문이다.

Action(행동): feature source(피처 원천), label head(라벨 헤드), model family(모델 계열), control/ablation(대조/제거 실험), timestamp safety(시점 안전)를 설계했다.
Effect(효과): run347B(347B 실행)는 입력 물질화와 프록시 선별 준비로 진행할 수 있다.

claim_boundary(주장 경계): `research_development_design_only_cash_open_asymmetric_long_short_source_no_model_training_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
