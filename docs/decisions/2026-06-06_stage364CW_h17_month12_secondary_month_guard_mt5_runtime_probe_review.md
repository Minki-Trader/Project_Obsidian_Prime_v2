# Stage364CW decision(결정): h17 month12 secondary guard MT5 review

- date(날짜): 2026-06-06
- run_id(실행 ID): `run364CW_review_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db_v1`
- decision(결정): `stage364CW_open_run364CX_equity_drawdown_side_balance_stress_repair_inputs`
- judgment(판정): `mixed_positive_runtime_probe_month12_repaired_net_pf_density_short_floor_positive_equity_dd_long_skew_proxy_gap_repair_required_no_authority`
- MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수): `1011.02` / `1.42` / `972.0`
- month12 repair(12월 수리): `passed_mt5_month12_nonnegative` with month12 long net(12월 롱 순수익) `8.79`
- remaining repair(잔여 수리): equity DD(수익곡선 낙폭) `130.11`, long share(롱 비중) `0.896090535`, proxy net diff(프록시 순수익 차이) `-56.18`
- next action(다음 행동): `run364CX_materialize_h17_equity_drawdown_side_balance_stress_repair_inputs_without_db_v1`
- effect(효과): 12월 수리는 보존하고, 평가손익 경로(equity path, 수익곡선 경로)와 방향 균형(side balance, 방향 균형)을 다음 입력으로 넘깁니다.
- claim_boundary(주장 경계): `research_development_mt5_runtime_probe_review_only_no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
