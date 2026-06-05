# run348B Cash-Open Asymmetric Proxy Training Review(348B 현금장 비대칭 프록시 학습 검토)

## Result(결과)

- run_id(실행 ID): `run348B_review_cash_open_asymmetric_proxy_training_without_db_v1`
- status(상태): `completed_stage348B_proxy_review_triaged_onnx_deployable_short_probe_seed_no_selection`
- judgment(판정): `inconclusive_proxy_review_long_oos_missing_short_oos_weak_onnx_deployable_short_probe_seed_allowed_no_operating_claim`
- decision(결정): `stage348B_open_run348C_materialize_onnx_deployable_short_carry_probe_package`
- next_run(다음 실행): `run348C_materialize_onnx_deployable_short_carry_probe_package_without_db_v1`
- source_run(원천 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- probe_seed_rows(탐침 씨앗 행): `4`

Action(행동): run347C proxy training(347C 프록시 학습)을 OOS gap(표본외 공백), short-carry usability(숏 기여 활용 가능성), ONNX deployability(온엑스 배포 가능성)로 검토했다.
Effect(효과): long head(롱 헤드)는 repair condition(수리 조건)으로 낮추고, logistic/ExtraTrees(로지스틱/엑스트라트리) short-carry seeds(숏 기여 씨앗)만 다음 MT5 package(MT5 패키지) 후보로 남겼다.

## Key Findings(핵심 발견)

- long_oos(롱 표본외): validation/test positive labels(검증/테스트 양성 라벨) 없음.
- short_oos(숏 표본외): 기본 head(헤드)는 약하지만 threshold screen(임계값 선별)에서 test split(테스트 분할) 탐침 씨앗이 남음.
- ONNX(온엑스): logistic_balanced/ExtraTrees(로지스틱/엑스트라트리) allocator(배분기)만 smoke pass(점검 통과). HistGBM(히스토그램 GBM)은 reference only(참고 전용).

## Artifacts(산출물)

- findings(발견): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348B/review_findings.csv`
- oos_gap_audit(표본외 공백 감사): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348B/oos_gap_audit.csv`
- short_carry_triage(숏 기여 분류): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348B/short_carry_triage.csv`
- onnx_deployability(온엑스 배포 가능성): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348B/onnx_deployability_review.csv`
- probe_seed_queue(탐침 씨앗 대기열): `stages/348_cash_open_proxy_review__long_oos_gap_short_carry_triage/02_runs/run348B/run348C_onnx_deployable_short_probe_seed_queue.csv`

## Claim Boundary(주장 경계)

`research_development_proxy_review_triage_only_no_new_training_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
