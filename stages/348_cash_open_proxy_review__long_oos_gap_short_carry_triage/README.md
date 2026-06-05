# Stage348 Cash-Open Proxy Review(348단계 현금장 프록시 검토)

## Stage ID(단계 ID)

`348_cash_open_proxy_review__long_oos_gap_short_carry_triage`

## Question(질문)

Can run347C proxy training(347C 프록시 학습)을 long OOS gap(롱 표본외 공백)과 short carry clue(숏 기여 단서)로 분류해, MT5 runtime probe(MT5 런타임 탐침)로 보낼 만한 가장 작은 seed(씨앗)만 남길 수 있는가?

## Source Inputs(원천 입력)

- source_stage(원천 단계): `347_cash_open_asymmetric_source__long_short_head_design`
- source_run(원천 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- superseded_run(대체된 실행): `run347D_review_cash_open_asymmetric_source_proxy_training_without_db_v1`
- branch_run(분기 실행): `run348A_branch_stage347_to_cash_open_proxy_review_without_db_v1`
- source_rows(원천 행): `5827`
- feature_count(피처 수): `53`
- trained_model_artifacts(학습 모델 산출물): `9`
- onnx_smoke_passes(온엑스 점검 통과): `2`
- long_oos_positive_labels(롱 표본외 양성 라벨): `0`

## Scope(범위)

Stage348(348단계)은 review/triage(검토/분류) 전용이다. New training(새 학습), MT5 execution(MT5 실행), candidate selection(후보 선정)은 이 분기 실행의 범위가 아니다.

## Exit Condition(종료 조건)

run348B(348B 실행)는 proxy queue(프록시 대기열)를 `probe seed(탐침 씨앗)`, `repair condition(수리 조건)`, `negative memory(부정 기억)`, `blocked retry condition(차단 재시도 조건)` 중 하나로 분류해야 한다.

## Claim Boundary(주장 경계)

`state_sync_stage_branch_proxy_review_handoff_only_no_new_training_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## run348C ONNX Short-Carry Probe Package(348C 온엑스 숏 기여 탐침 패키지)

- report(보고서): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/03_reviews/run348C_onnx_deployable_short_carry_probe_package.md`
- package(패키지): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/runtime_probe_attempt_package.csv`
- queue(대기열): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/run348D_queue.csv`
- effect(효과): Stage348(348단계)이 가벼운 MT5 execution(실행) 작업으로 넘어갈 수 있다.

## run348C ONNX Short-Carry Probe Package(348C 온엑스 숏 기여 탐침 패키지)

- report(보고서): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/03_reviews/run348C_onnx_deployable_short_carry_probe_package.md`
- package(패키지): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/runtime_probe_attempt_package.csv`
- queue(대기열): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348C/run348D_queue.csv`
- effect(효과): Stage348(348단계)이 가벼운 MT5 execution(실행) 작업으로 넘어갈 수 있다.
