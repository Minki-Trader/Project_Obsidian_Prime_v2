# 2026-06-01 Stage347C Proxy Training Decision(347C 프록시 학습 결정)

- decision(결정): `stage347C_open_run347D_review_cash_open_asymmetric_source_proxy_training`
- source_materialization(원천 물질화): `run347B_materialize_cash_open_asymmetric_source_inputs_without_db_v1`
- next_run(다음 실행): `run347D_review_cash_open_asymmetric_source_proxy_training_without_db_v1`
- reason(이유): run347B(347B 실행)가 feature/teacher-label source(피처/교사 라벨 원천)를 만들었으므로, 이제 model family(모델 계열)별 proxy reconstruction(프록시 재구성)을 확인해야 한다.

Action(행동): allocator/long/short proxy models(배분기/롱/숏 프록시 모델)을 학습하고 ONNX smoke parity(온엑스 점검 동등성)를 시도했다.
Effect(효과): run347D(347D 실행)가 MT5 runtime probe(MT5 런타임 탐침)로 넘길 가치가 있는지 낮은 주장 범위에서 검토할 수 있다.

claim_boundary(주장 경계): `research_development_proxy_training_only_cash_open_asymmetric_source_teacher_distillation_onnx_smoke_only_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
