# run364B Timestamp Context Cost Surface Materialization(run364B 시점 문맥 비용 표면 구체화)

- run_id(실행 ID): `run364B_materialize_timestamp_context_cost_surface_without_db_v1`
- parent_run_id(부모 실행 ID): `run364A_branch_stage363_to_source_regime_label_pivot_without_db_v1`
- status(상태): `completed_stage364B_timestamp_context_cost_surface_materialized_review_required_no_selection_no_mt5`
- judgment(판정): `timestamp_context_surface_materialized_cross_split_density_cost_pass_review_required_no_operating_claim`
- next_run_id(다음 실행 ID): `run364C_review_timestamp_context_cost_surface_without_db_v1`
- gates(게이트): `11/11`

Action(행동): q05 long-only trade table(q05 롱 단독 거래 표)에 timestamp-safe context(시점 안전 문맥) 필터를 구체화했다.

Effect(효과): validation-derived threshold(검증 파생 임계값)를 OOS(표본외)에 고정 적용해 비용(cost, 비용)과 trade density(거래 밀도)를 같이 보는 positive scout(긍정 스카우트)를 찾았다.

## Result(결과)

- score_rows(점수 행): `366`
- cross_split_rows(교차 분할 행): `183`
- passing_cross_split_rows(교차 분할 통과 행): `33`
- best_pass_variant_id(최선 통과 변형 ID): `s364_r02_drop_worst_open_hour_minute_bucket15_k2`
- best_pass_validation_cost_0_30_net(최선 통과 검증 +0.30 비용 순수익): `94.32`
- best_pass_validation_density(최선 통과 검증 밀도): `3.0983606557`
- best_pass_oos_cost_0_30_net(최선 통과 표본외 +0.30 비용 순수익): `100.52`
- best_pass_oos_density(최선 통과 표본외 밀도): `3.106870229`
- best_validation_variant_id(최선 검증 변형 ID): `s364_r02_drop_worst_open_hour_minute_bucket15_k6`
- best_oos_variant_id(최선 표본외 변형 ID): `s364_r05_best_oos_plus_h17_plong_q80_guard`

## Judgment Boundary(판정 경계)

Action(행동): passing_cross_split_rows(교차 분할 통과 행) `33`를 review-required scout(검토 필요 스카우트)로 기록했다.

Effect(효과): 이 결과는 candidate selection(후보 선택), MT5 execution(MT5 실행), operating promotion(운영 승격)이 아니다.

## Artifacts(산출물)

- scorecard(점수표): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364B/timestamp_context_scorecard.csv`
- cross_split(교차 분할): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364B/timestamp_context_cross_split.csv`
- failure_attribution(실패/성과 귀속): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364B/timestamp_context_failure_attribution.csv`
- review_queue(검토 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364B/run364C_review_queue.csv`
- final_decision(최종 결정): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364B/final_decision.json`

Claim Boundary(주장 경계): `research_development_materialization_only_timestamp_context_cost_surface_validation_thresholds_report_derived_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
