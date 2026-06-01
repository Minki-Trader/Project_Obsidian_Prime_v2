# run362B Q05 Long-Only Margin Grid Materialization(run362B q05 롱 단독 마진 격자 구체화)

- run_id(실행 ID): `run362B_materialize_q05_long_only_margin_grid_without_db_v1`
- parent_run_id(부모 실행 ID): `run362A_branch_stage361_to_long_only_margin_grid_without_db_v1`
- source_runtime_run_id(원천 런타임 실행 ID): `run359B_execute_high_density_label_pivot_mt5_probe_without_db_v1`
- status(상태): `completed_stage362B_q05_long_only_margin_grid_materialized_review_required_no_selection_no_mt5`
- judgment(판정): `margin_grid_materialized_all_designed_rows_fail_density_cost_gate_review_required_no_operating_claim`
- next_run_id(다음 실행 ID): `run362C_review_q05_long_only_margin_grid_without_db_v1`
- gates(게이트): `10/10`

Action(행동): q05 long-only closed trades(q05 롱 단독 종료 거래)를 open-time runtime probability(진입 시점 런타임 확률)와 결합하고 35-row margin grid(35행 마진 격자)를 validation/OOS(검증/표본외) 각각 평가했다.

Effect(효과): Stage362(362단계)는 margin grid(마진 격자)만으로 +0.30 cost buffer(+0.30 비용 버퍼)를 확보할 수 있는지 확인했고, 새 MT5 execution(MT5 실행)이나 candidate selection(후보 선택)은 하지 않았다.

## Result(결과)

- long_trade_probability_rows(롱 거래 확률 결합 행): `1114`
- margin_grid_score_rows(마진 격자 점수 행): `70`
- cross_split_rows(교차 분할 행): `35`
- passing_cross_split_rows(검증/표본외 동시 통과 행): `0`
- best_oos_grid_id(최선 표본외 격자 ID): `s361_margin_006`
- best_oos_cost_0_30_net(최선 표본외 +0.30 비용 순수익): `50.2`
- best_oos_density(최선 표본외 밀도): `0.1755725191`
- best_oos_validation_cost_0_30_net(해당 격자 검증 +0.30 비용 순수익): `-87.58`
- best_validation_grid_id(최선 검증 격자 ID): `s361_margin_016`
- best_validation_cost_0_30_net(최선 검증 +0.30 비용 순수익): `18.67`
- best_validation_density(최선 검증 밀도): `0.043715847`

## Judgment Boundary(판정 경계)

Action(행동): passing_cross_split_rows(교차 분할 통과 행) `0`으로 기록했다.

Effect(효과): 이 결과는 negative materialization scout(부정 구체화 탐색)이며, 운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 후보 선택(candidate selection, 후보 선택)이 아니다.

## Failure Attribution(실패 귀속)

- primary_failure(주 실패): `density_collapse_after_margin_filter(마진 필터 후 밀도 붕괴)`
- best_oos_failure(최선 표본외 실패): `oos_cost_positive_but_trade_density_far_below_3(표본외 비용 후 양수지만 거래 밀도 3 미만)`
- best_validation_failure(최선 검증 실패): `validation_cost_positive_only_in_sparse_surface(검증 비용 후 양수가 희소 표면에 한정)`

## Artifacts(산출물)

- trade_probability_table(거래 확률 표): `stages/362_long_only_margin_grid__cost_buffer_first_branch/02_runs/run362B/q05_long_trade_probability_table.csv`
- margin_grid_scorecard(마진 격자 점수표): `stages/362_long_only_margin_grid__cost_buffer_first_branch/02_runs/run362B/margin_grid_scorecard.csv`
- cross_split(교차 분할): `stages/362_long_only_margin_grid__cost_buffer_first_branch/02_runs/run362B/margin_grid_cross_split.csv`
- failure_attribution(실패 귀속): `stages/362_long_only_margin_grid__cost_buffer_first_branch/02_runs/run362B/margin_grid_failure_attribution.csv`
- review_queue(검토 대기열): `stages/362_long_only_margin_grid__cost_buffer_first_branch/02_runs/run362B/run362C_review_queue.csv`

Claim Boundary(주장 경계): `research_development_materialization_only_q05_long_only_margin_grid_report_derived_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
