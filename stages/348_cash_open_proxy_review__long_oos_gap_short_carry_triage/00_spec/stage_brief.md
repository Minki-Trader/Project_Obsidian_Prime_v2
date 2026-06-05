# Stage348 Cash-Open Proxy Review(348단계 현금장 프록시 검토)

## Stage ID(단계 ID)

`348_cash_open_proxy_review__long_oos_gap_short_carry_triage`

## Question(질문)

Can run347C proxy training(347C 프록시 학습)을 long OOS gap(롱 표본외 공백)과 short carry clue(숏 기여 단서)로 분류해, MT5 runtime probe(MT5 런타임 탐침)로 보낼 만한 가장 작은 seed(씨앗)만 남길 수 있는가?

## Source Inputs(원천 입력)

- source_stage(원천 단계): `347_cash_open_asymmetric_source__long_short_head_design`
- source_run(원천 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- source_package_run(원천 패키지 실행): `run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1`
- branch_run(분기 실행): `run348A_branch_stage347_to_cash_open_proxy_review_without_db_v1`
- source_rows(원천 행): `5827`
- feature_count(피처 수): `53`

## Scope(범위)

Stage348(348단계)은 review/triage/package handoff(검토/분류/패키지 인계) 전용이다. MT5 execution(MT5 실행), candidate selection(후보 선정), runtime authority(런타임 권위)는 Stage349(349단계) 이후 근거가 있어야만 말한다.

## Completed Runs(완료 실행)

- run348A(348A 실행): Stage347(347단계) proxy review(프록시 검토)를 Stage348(348단계)로 분리했다.
- run348B(348B 실행): ONNX deployable short-carry seeds(온엑스 배포 가능 숏 기여 씨앗)만 다음 패키지로 넘겼다.
- run348C(348C 실행): attempts(시도) `4`, expected_rows(예상 행) `23308`인 MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만들었다.

## Stage349 Handoff(349단계 인계)

- branch_run(분기 실행): `run349A_branch_stage348_to_onnx_short_carry_runtime_probe_without_db_v1`
- next_stage(다음 단계): `349_onnx_short_carry_runtime__execute_mt5_probe`
- next_run(다음 실행): `run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1`

Action(행동): Stage348(348단계)의 run348D planned execution(예정 실행)을 Stage349 run349B(349B 실행)로 retarget(재지정)했다.
Effect(효과): Stage348(348단계)은 무거운 실행 근거 수집을 더 품지 않고, package evidence(패키지 근거)까지만 보존한다.

## Claim Boundary(주장 경계)

`state_sync_stage_branch_onnx_short_carry_runtime_probe_handoff_only_no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
