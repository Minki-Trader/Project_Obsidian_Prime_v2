# 2026-06-01 Stage338L Decision(338L 결정)

- run_id(실행 ID): `run338L_review_trade_count_recovery_expansion_mt5_probe_without_db_v1`
- decision(결정): `stage338L_open_run338M_lifecycle_exit_side_balance_recovery_expansion`
- judgment(판정): `threshold_corridor_improved_net_and_trade_count_but_recovery_trade_count_side_balance_not_ready_no_selection`
- next_run_id(다음 실행 ID): `run338M_materialize_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_package_without_db_v1`
- evidence(근거): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338L/run338L_threshold_corridor_scorecard.csv`, `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338L/run338L_kpi_judgment.csv`, `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338L/run338M_queue.csv`

Action(행동): threshold corridor(임계값 구간)를 operating promotion(운영 승격)이 아니라 lifecycle/exit repair(생명주기/청산 수리)로 넘겼다.

Effect(효과): 양수 단서를 유지하면서 drawdown(낙폭), recovery factor(회복 계수), side balance(방향 균형)를 다음 작업 제약으로 고정한다.

claim_boundary(주장 경계): `research_development_threshold_corridor_mt5_probe_review_only_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
