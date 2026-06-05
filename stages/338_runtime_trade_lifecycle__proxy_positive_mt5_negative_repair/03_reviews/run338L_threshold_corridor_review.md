# run338L Trade Count Recovery Expansion Review(거래수 회복 확장 검토)

## Summary(요약)

- run_id(실행 ID): `run338L_review_trade_count_recovery_expansion_mt5_probe_without_db_v1`
- status(상태): `completed_stage338L_threshold_corridor_positive_but_operating_not_ready_reviewed_no_selection`
- judgment(판정): `threshold_corridor_improved_net_and_trade_count_but_recovery_trade_count_side_balance_not_ready_no_selection`
- gates(게이트): `8/8`
- best_attempt(최고 시도): `j02_p55_m00`
- net profit(순수익): `70.32`
- profit factor(수익 팩터): `1.84`
- expectancy(기대값): `3.35`
- recovery factor(회복 계수): `0.91`
- drawdown(낙폭): `77.15`
- trade count(거래수): `21`
- long/short(롱/숏): `4/17`
- weakness(약점): `recovery;trade_count;side_balance;forward_or_live_missing`
- next_run(다음 실행): `run338M_materialize_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_package_without_db_v1`

## Action(행동)

run338K(338K 실행)의 4개 MT5 threshold corridor(MT5 임계값 구간)를 KPI(핵심 성과 지표), runtime parity(런타임 동등성), threshold attribution(임계값 귀속)으로 검토했다.

Effect(효과): j02_p55_m00은 control(대조)보다 net profit(순수익)과 trade count(거래수)를 늘렸지만 recovery factor(회복 계수), trade count(거래수), side balance(방향 균형), forward evidence(전진 근거)가 부족해 운영 승격(operating promotion, 운영 승격)을 막는다.

## Evidence(근거)

- scorecard(점수표): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338L/run338L_threshold_corridor_scorecard.csv`
- KPI judgment(KPI 판정): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338L/run338L_kpi_judgment.csv`
- attribution(귀속): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338L/run338L_threshold_corridor_attribution.csv`
- next queue(다음 대기열): `stages/338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair/02_runs/run338L/run338M_queue.csv`
