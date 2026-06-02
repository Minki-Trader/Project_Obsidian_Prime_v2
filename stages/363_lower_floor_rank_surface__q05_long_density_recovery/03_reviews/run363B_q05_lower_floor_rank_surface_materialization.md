# run363B Q05 Lower-Floor Rank Surface Materialization(run363B q05 낮은 하한 순위 표면 구체화)

- run_id(실행 ID): `run363B_materialize_q05_lower_floor_rank_surface_without_db_v1`
- parent_run_id(부모 실행 ID): `run363A_branch_stage362_to_lower_floor_rank_surface_without_db_v1`
- status(상태): `completed_stage363B_q05_lower_floor_rank_surface_materialized_review_required_no_selection_no_mt5`
- judgment(판정): `lower_floor_rank_surface_materialized_no_cross_split_density_cost_pass_review_required_no_operating_claim`
- next_run_id(다음 실행 ID): `run363C_review_q05_lower_floor_rank_surface_without_db_v1`
- gates(게이트): `10/10`

Action(행동): Stage363A design queue(Stage363A 설계 대기열)의 8개 surface family(표면군)를 q05 long-only trade table(q05 롱 단독 거래 표)에 구체화했다.

Effect(효과): validation-derived threshold(검증 파생 임계값)만 OOS(표본외)에 고정 적용해 lower-floor/rank(낮은 하한/순위) 아이디어의 비용-밀도 교환을 확인했다.

## Result(결과)

- score_rows(점수 행): `180`
- cross_split_rows(교차 분할 행): `90`
- passing_cross_split_rows(교차 분할 통과 행): `0`
- both_cost_positive_density_fail_rows(양쪽 비용 양수지만 밀도 실패 행): `21`
- best_validation_variant_id(최선 검증 변형 ID): `s363_r02_f0.330_g0.006`
- best_validation_cost_0_30_net(최선 검증 +0.30 비용 순수익): `74.55`
- best_validation_density(최선 검증 밀도): `1.8907103825`
- best_oos_variant_id(최선 표본외 변형 ID): `s363_r02_f0.330_g0.008`
- best_oos_cost_0_30_net(최선 표본외 +0.30 비용 순수익): `257.35`
- best_oos_density(최선 표본외 밀도): `1.9160305344`

## Judgment Boundary(판정 경계)

Action(행동): passing_cross_split_rows(교차 분할 통과 행) `0`으로 기록했다.

Effect(효과): 이 결과는 negative materialization scout(부정 구체화 탐색)이며, candidate selection(후보 선택), MT5 execution(MT5 실행), operating promotion(운영 승격)이 아니다.

## Artifacts(산출물)

- scorecard(점수표): `stages/363_lower_floor_rank_surface__q05_long_density_recovery/02_runs/run363B/lower_floor_rank_scorecard.csv`
- cross_split(교차 분할): `stages/363_lower_floor_rank_surface__q05_long_density_recovery/02_runs/run363B/lower_floor_rank_cross_split.csv`
- failure_attribution(실패 귀속): `stages/363_lower_floor_rank_surface__q05_long_density_recovery/02_runs/run363B/lower_floor_rank_failure_attribution.csv`
- review_queue(검토 대기열): `stages/363_lower_floor_rank_surface__q05_long_density_recovery/02_runs/run363B/run363C_review_queue.csv`
- final_decision(최종 결정): `stages/363_lower_floor_rank_surface__q05_long_density_recovery/02_runs/run363B/final_decision.json`

Claim Boundary(주장 경계): `research_development_materialization_only_q05_lower_floor_rank_surface_report_derived_validation_thresholds_only_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
