# run340B Quality Balance Review(340B 품질-균형 검토)

## Summary(요약)

- run_id(실행 ID): `run340B_review_quality_balance_blend_mt5_probe_without_db_v1`
- source_runtime_run(원천 런타임 실행): `run339G_execute_quality_balance_blend_mt5_probe_without_db_v1`
- status(상태): `completed_stage340B_quality_balance_reviewed_local_floor_positive_clue_no_selection`
- judgment(판정): `f01_local_floor_pass_pressure_test_required_no_selection`
- gates(게이트): `10/10`
- exact_parity(정확 동등성): `58270/58270`, mismatch(불일치): `0`
- local_floor_pass_count(로컬 하한 통과 수): `1`
- best_attempt(최고 시도): `f01_s55_l51_m01_h12`
- best_net_profit(최고 순수익): `122.9`
- best_profit_factor(최고 수익 팩터): `1.89`
- best_expectancy(최고 기대값): `3.72`
- best_recovery_factor(최고 회복 계수): `1.38`
- best_drawdown(최고 낙폭): `89.31`
- best_trade_count(최고 거래수): `33`
- best_side_balance(최고 방향 균형): `0.650`
- next_run(다음 실행): `run340C_materialize_f01_local_floor_pressure_mt5_probe_package_without_db_v1`

## Judgment(판정)

`f01_s55_l51_m01_h12`는 runtime_probe(런타임 탐침) 안에서 local-floor positive clue(로컬 하한 통과 긍정 단서)다. selected model(선정 모델)은 아니다.
Effect(효과): profit factor(수익 팩터), expectancy(기대값), recovery factor(회복 계수), drawdown(낙폭), trade count(거래수), side balance(방향 균형)가 단일 구간에서 동시에 버틴 단서를 보존하지만, forward/replay(전진/재생), cost stress(비용 압박), session/regime(세션/국면), equity curve quality(수익곡선 품질)가 없으므로 운영 주장은 닫지 않는다.

## Attribution(귀속)

- f01(에프01): long_threshold(롱 임계값) 0.51과 min_margin(최소 마진) 0.01이 약한 long(롱)을 줄이면서 trade_count(거래수)를 33으로 회복했다.
- f05~f07(에프05~에프07): side_balance(방향 균형)는 좋아 보이지만 recovery/drawdown(회복/낙폭)이 깨져 단순 long relief(롱 완화)는 위험하다.
- f08(에프08): short_threshold(숏 임계값) 0.56은 균형 착시를 만들지만 net_profit(순수익)을 음수로 만든다.

## Next Action(다음 행동)

Open `run340C_materialize_f01_local_floor_pressure_mt5_probe_package_without_db_v1` with `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340B/run340C_queue.csv`.
Effect(효과): f01(에프01)을 exact replay control(정확 재생 대조)로 두고 threshold/min_margin/hold(임계값/최소 마진/보유) pressure test(압박 시험)를 MT5(메타트레이더5)에서 확인한다.

## Boundary(경계)

No selected model(선정 모델 없음), no promotion_candidate(승격 후보 없음), no operating_promotion(운영 승격 없음), no runtime_authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
