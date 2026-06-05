# run342G Soft Session-Long Firewall MT5 Probe Review(342G 부드러운 세션 롱 방화벽 MT5 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `run342G_review_soft_session_long_firewall_mt5_probe_without_db_v1`
- parent_run(부모 실행): `run342F_execute_soft_session_long_firewall_mt5_probe_without_db_v1`
- status(상태): `completed_stage342G_soft_firewall_reviewed_no_trade_shape_recovery_no_selection`
- judgment(판정): `soft_window_does_not_recover_trade_count_hard_firewall_profit_quality_clue_preserved_no_selection`
- gates(게이트): `9/9`
- exact_parity(정확 동등성): `40789/40789`, mismatch(불일치) `0`
- best_attempt(최고 시도): `e04_q09_blk_early45`
- best_net_profit(최고 순수익): `151.49`
- best_profit_factor(최고 수익 팩터): `3.47`
- best_recovery_factor(최고 회복 계수): `1.53`
- best_trade_count(최고 거래수): `23`
- best_long_short(최고 롱/숏): `3/20`
- next_run(다음 실행): `run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1`

## Action(행동)

run342F(342F 실행)의 soft session-long firewall(부드러운 세션 롱 방화벽) MT5 runtime probe(MT5 런타임 탐침)를 검토했다.
Effect(효과): 0~45/0~75 soft window(부드러운 구간)는 hard block(강한 차단)과 같은 거래 형태를 만들어 trade count(거래수)와 long/short balance(롱/숏 균형)를 회복하지 못했다는 점을 닫았다.

## Judgment(판정)

hard/soft early-long block(강한/부드러운 초반 롱 차단)은 profit-quality clue(수익 품질 단서)를 보존하지만 selected model(선정 모델)은 아니다.
Effect(효과): 다음 탐색은 time-window pruning(시간 구간 절단)이 아니라 long threshold/min_margin(롱 임계값/최소 마진) 혼합으로 이동한다.

## Next(다음)

Open `run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1` with `stages/342_session_long_firewall__early_long_filter_mt5_probe/02_runs/run342G/run342H_early_long_quality_margin_mix_queue.csv`.
Effect(효과): early-long quality gate(초반 롱 품질 게이트)를 MT5 package(MT5 패키지)로 시험할 준비를 한다.

## Boundary(경계)

No selection(선정 없음), no forward(전진 없음), no live readiness(실거래 준비 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
