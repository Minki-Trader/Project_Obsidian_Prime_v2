# run343F Trade Shape Rescue Review(343F 거래 형태 복구 검토)

## Summary(요약)

- run_id(실행 ID): `run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- parent_run(부모 실행): `run343E_execute_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1`
- gates(게이트): `9/9`
- judgment(판정): `trade_shape_rescue_failed_to_improve_anchor_profit_quality_preserved_no_selection`
- best_attempt(최고 시도): `d01_h04_anchor45`
- best_net_profit(최고 순수익): `152.79`
- best_profit_factor(최고 수익 팩터): `3.55`
- best_expectancy(최고 기대값): `6.95`
- best_drawdown(최고 낙폭): `89.31`
- best_recovery_factor(최고 회복 계수): `1.71`
- best_trade_count(최고 거래수): `22`
- best_long_short(최고 롱/숏): `2/20`
- shape_control(거래 형태 대조): `d02_h02_shape_ctl`, net(순수익) `122.9`, PF(수익 팩터) `1.89`, trades(거래수) `33`, long/short(롱/숏) `13/20`
- near_anchor(앵커 근처): `d06_q04_m015_blk15`, net(순수익) `150.79`, PF(수익 팩터) `3.43`, trades(거래수) `23`
- next_run(다음 실행): `run343G_design_directional_long_supply_quality_surface_without_db_v1`

## Judgment(판정)

run343E(343E 실행)는 valid runtime probe(유효 런타임 탐침)다. MT5 telemetry(MT5 런타임 기록)는 expected tape(예상 테이프)와 58,270/58,270 행 일치했고 mismatch(불일치)는 0이다.

profit anchor(수익 앵커)는 보존됐다. `d01_h04_anchor45`, `d04_q02_blk15`, `d05_q02_blk30`, `d10_q02_blk60`은 모두 net profit(순수익) 152.79, PF(수익 팩터) 3.55, trades(거래수) 22로 같은 표면에 수렴했다.

trade shape rescue(거래 형태 복구)는 실패했다. `d02_h02_shape_ctl`은 trades(거래수) 33과 long/short(롱/숏) 13/20을 만들었지만 net profit(순수익) 122.9, PF(수익 팩터) 1.89로 수익 품질을 크게 잃었다. `d06_q04_m015_blk15`는 trades(거래수)를 23으로 1개 늘렸지만 net profit(순수익)은 150.79, PF(수익 팩터)는 3.43으로 앵커를 넘지 못했다.

## Attribution(성과 귀속)

- minute block micro-tuning(분 차단 미세조정): 0~15/30/45/60분 변형이 같은 결과로 수렴했다. 효과는 이 feature(피처)의 range tuning(범위 조정)을 반복하지 않게 하는 것이다.
- shape control tax(거래 형태 대조 비용): 롱 공급은 늘었지만 weak long(약한 롱)까지 같이 복구되어 expectancy(기대값)와 PF(수익 팩터)가 낮아졌다.
- near-anchor clue(앵커 근처 단서): d06/d07은 수익을 거의 유지하며 long trade(롱 거래)를 1개 늘렸지만 운영 가능한 균형 회복은 아니다.
- q10 cost stress(비용 압박): short threshold(숏 임계값) 단독 상승은 net/PF/recovery(순수익/수익 팩터/회복 계수)를 악화했다.

## Next(다음)

run343G(343G 실행)는 directional long quality surface(방향성 롱 품질 표면)를 설계한다. Action(행동): 시간 구간 차단 대신 long-only quality/regime(롱 전용 품질/국면) 원천을 찾는다. Effect(효과): profit anchor(수익 앵커)의 short supply(숏 공급)를 보존하면서 trade shape(거래 형태)를 다시 공격적으로 복구한다.

## Boundary(경계)

No selection(선정 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
