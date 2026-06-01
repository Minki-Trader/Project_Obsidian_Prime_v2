# Decision(결정): Stage362B Q05 Long-Only Margin Grid Materialization(q05 롱 단독 마진 격자 구체화)

- date(날짜): `2026-06-02`
- run_id(실행 ID): `run362B_materialize_q05_long_only_margin_grid_without_db_v1`
- status(상태): `completed_stage362B_q05_long_only_margin_grid_materialized_review_required_no_selection_no_mt5`
- judgment(판정): `margin_grid_materialized_all_designed_rows_fail_density_cost_gate_review_required_no_operating_claim`
- next_run_id(다음 실행 ID): `run362C_review_q05_long_only_margin_grid_without_db_v1`
- claim_boundary(주장 경계): `research_development_materialization_only_q05_long_only_margin_grid_report_derived_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Action(행동): Stage361A(361A 실행)의 35-row margin grid(35행 마진 격자)를 q05 long-only open-time probability(진입 시점 확률)로 구체화했다.

Effect(효과): margin grid(마진 격자)는 sparse cost-positive pockets(희소 비용 양수 구간)를 만들었지만 trade/day(일별 거래수) 3 이상을 만족하지 못해 candidate selection(후보 선택)으로 올리지 않는다.

## Next Condition(다음 조건)

`run362C_review_q05_long_only_margin_grid_without_db_v1`는 이 negative materialization(부정 구체화)을 검토하고, 낮은 p_long floor(p_long 하한), rank/quantile surface(순위/분위수 표면), 또는 regime/label branch(국면/라벨 분기) 중 하나를 다음 작은 stage(단계)로 선택한다.
