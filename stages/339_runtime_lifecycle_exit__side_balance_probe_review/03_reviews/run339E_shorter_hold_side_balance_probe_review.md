# run339E Shorter Hold Side Balance Probe Review(짧은 보유 방향 균형 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `run339E_review_shorter_hold_side_balance_trade_count_expansion_mt5_probe_without_db_v1`
- parent_run(부모 실행): `run339D_execute_shorter_hold_side_balance_trade_count_expansion_mt5_probe_without_db_v1`
- status(상태): `completed_stage339E_shorter_hold_side_balance_probe_reviewed_bifurcated_positive_clue_no_selection`
- judgment(판정): `profit_quality_and_side_balance_split_positive_clues_but_no_operating_ready_selection`
- gates(게이트): `9/9`
- exact_parity(정확 동등성): `52443/52443`, mismatch(불일치) `0`
- best_attempt(최고 시도): `c01_s55_l52_h12`
- best_net_profit(최고 순수익): `115.32`
- best_profit_factor(최고 수익 팩터): `1.88`
- best_recovery_factor(최고 회복 계수): `1.29`
- best_trade_count(최고 거래수): `29`
- best_side_balance(최고 방향 균형): `0.450`
- operating_ready_count(운영 준비 수): `0`
- next_run(다음 실행): `run339F_materialize_quality_balance_blend_mt5_probe_package_without_db_v1`

## Judgment(판정)

run339D(339D 실행)는 positive runtime_probe clue(긍정 런타임 탐침 단서)지만 selected model(선정 모델)은 아니다.
Effect(효과): c01(씨01)은 profit quality(수익 품질)를 보존했지만 trade_count(거래수) 29로 하한 30에 부족하고, c07(씨07)은 trade_count(거래수) 43과 side_balance(방향 균형) 0.870을 만들었지만 recovery factor(회복 계수) 0.77로 낮다.

## Attribution(귀속)

- c01(씨01): mild long relief(약한 롱 완화)가 side_balance(방향 균형)를 개선했지만 m02(엠02) 대비 순수익과 PF(수익 팩터)를 낮췄다.
- c07(씨07): strong long relief(강한 롱 완화)가 trade shape(거래 형태)를 개선했지만 weak long supply(약한 롱 공급)가 recovery(회복)를 깎았다.
- strict short(엄격한 숏): short_threshold(숏 임계값) 0.57 이상은 profitable short supply(수익성 있는 숏 공급)를 과하게 줄였다.

## Next Action(다음 행동)

Open `run339F_materialize_quality_balance_blend_mt5_probe_package_without_db_v1` with `run339F_queue.csv`.
Effect(효과): long relief(롱 완화)에 min_margin(최소 마진)을 붙여 c07(씨07)의 균형 단서와 c01(씨01)의 수익 품질을 섞어 본다.

## Boundary(경계)

No selected model(선정 모델 없음), no promotion_candidate(승격 후보 없음), no operating_promotion(운영 승격 없음), no runtime_authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
