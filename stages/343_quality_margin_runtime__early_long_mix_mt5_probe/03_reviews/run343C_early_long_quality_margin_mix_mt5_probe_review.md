# run343C Early Long Quality Margin Mix Review(343C 초반 롱 품질/마진 혼합 검토)

## Summary(요약)

- run_id(실행 ID): `run343C_review_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- parent_run(부모 실행): `run343B_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1`
- gates(게이트): `9/9`
- judgment(판정): `quality_margin_improves_profit_quality_but_does_not_recover_trade_shape_no_selection`
- best_attempt(최고 시도): `h04_q02_l515_blk45`
- best_net_profit(최고 순수익): `152.79`
- best_profit_factor(최고 수익 팩터): `3.55`
- best_expectancy(최고 기대값): `6.95`
- best_drawdown(최고 낙폭): `89.31`
- best_recovery_factor(최고 회복 계수): `1.71`
- best_trade_count(최고 거래수): `22`
- best_long_short(최고 롱/숏): `2/20`
- trade_shape_best(거래 형태 최고): `h02_q04_m015_ctl`, trade_count(거래수) `33`, side_balance(방향 균형) `0.65`
- next_run(다음 실행): `run343D_materialize_trade_shape_rescue_quality_margin_blend_package_without_db_v1`

## Attribution(귀속)

- previous_best(이전 최고): `e04_q09_blk_early45` net(순수익) `151.49`, PF(수익 팩터) `3.47`, drawdown(낙폭) `99.31`, trades(거래수) `23`, long/short(롱/숏) `3/20`
- new_best(새 최고): `h04_q02_l515_blk45` net(순수익) `152.79`, PF(수익 팩터) `3.55`, drawdown(낙폭) `89.31`, trades(거래수) `22`, long/short(롱/숏) `2/20`
- delta(차이): net `1.3`, PF `0.08`, drawdown `-10.0`, trade_count `-1`

## Judgment(판정)

profit quality(수익 품질)는 보존되었고 소폭 개선됐다. 그러나 best attempt(최고 시도)는 trade count(거래수) 22, long/short(롱/숏) 2/20이라 trade shape(거래 형태)는 회복되지 않았다. h02/h03 controls(대조군)는 거래수 33과 long/short(롱/숏) 13/20을 보였지만 net profit(순수익) 122.9, PF(수익 팩터) 1.89로 수익 품질이 낮다.

Action(행동): run343D(343D 실행)에서 short anchor + long sidecar(숏 앵커 + 롱 보조)와 session-aware long rescue(세션 인지 롱 복구)를 package(패키지)로 만든다.
Effect(효과): 수익 앵커와 거래 형태 회복 단서를 분리하지 않고 같은 MT5 probe(MT5 탐침) 안에서 충돌 시험한다.

## Boundary(경계)

No selection(선정 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
