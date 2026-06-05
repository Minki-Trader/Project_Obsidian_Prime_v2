# run347C Cash-Open Asymmetric Source Proxy Training(347C 현금장 비대칭 원천 프록시 학습)

## Result(결과)

- status(상태): `completed_stage347C_cash_open_asymmetric_proxy_training_screened_no_selection`
- judgment(판정): `proxy_training_completed_short_teacher_reconstruction_available_long_oos_missing_no_operating_claim`
- decision(결정): `stage347C_open_run347D_review_cash_open_asymmetric_source_proxy_training`
- next_run(다음 실행): `run347D_review_cash_open_asymmetric_source_proxy_training_without_db_v1`

Action(행동): run347B(347B 실행)의 teacher/source labels(교사/원천 라벨)을 logistic/ExtraTrees/HistGBM(로지스틱/엑스트라 트리/히스토그램 GBM) proxy models(프록시 모델)로 학습했다.
Effect(효과): 다음 run347D(347D 실행)에서 proxy score(프록시 점수), ONNX smoke(온엑스 점검), long-label weakness(롱 라벨 약점)를 검토할 수 있다.

## Scope(범위)

- rows(행): `5827`
- feature_count(피처 수): `53`
- trained_model_artifacts(학습 모델 산출물): `9`
- onnx_allocator_smoke_passes(온엑스 배분기 점검 통과): `2`
- threshold_screen_rows(임계값 선별 행): `900`
- probe_priority_rows(탐침 우선순위 행): `20`

## Key Caveat(핵심 주의)

Validation/test(검증/테스트) 구간에는 long teacher positive(롱 교사 양성)가 없다. 따라서 long quality(롱 품질)는 아직 OOS(`out-of-sample`, 표본외)로 검증되지 않았다.

## Artifacts(산출물)

- scorecard(점수표): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347C/model_training_scorecard.csv`
- threshold_screen(임계값 선별): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347C/proxy_threshold_screen.csv`
- probe_priority_queue(탐침 우선순위 대기열): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347C/probe_priority_queue.csv`
- model_artifacts(모델 산출물): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347C/model_artifact_manifest.csv`
- onnx_smoke(온엑스 점검): `stages/347_cash_open_asymmetric_source__long_short_head_design/02_runs/run347C/onnx_parity_smoke.csv`

## Claim Boundary(주장 경계)

`research_development_proxy_training_only_cash_open_asymmetric_source_teacher_distillation_onnx_smoke_only_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
