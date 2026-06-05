# run340E F01 Pressure Probe Review(340E F01 압박 탐침 검토)

## Summary(요약)

- run_id(실행 ID): `run340E_review_f01_local_floor_pressure_mt5_probe_without_db_v1`
- parent_run(부모 실행): `run340D_execute_f01_local_floor_pressure_mt5_probe_without_db_v1`
- status(상태): `completed_stage340E_f01_pressure_probe_reviewed_negative_with_control_semantics_repair_required_no_selection`
- judgment(판정): `pressure_surface_negative_but_exact_replay_control_semantics_invalid_close_on_flat_mismatch_repair_required_no_selection`
- gates(게이트): `12/12`
- exact_package_parity(정확 패키지 동등성): `58270/58270`, mismatch(불일치): `0`
- control_semantics_pass(대조 의미 통과): `False`
- best_attempt(최고 시도): `p09_s545_l51_m01_h12`
- best_net_profit(최고 순수익): `-25.81`
- best_profit_factor(최고 수익 팩터): `0.78`
- best_expectancy(최고 기대값): `-0.65`
- best_recovery_factor(최고 회복 계수): `-0.32`
- best_trade_count(최고 거래수): `40`
- source_f01_net_profit(원본 f01 순수익): `122.9`
- source_f01_profit_factor(원본 f01 수익 팩터): `1.89`
- next_run(다음 실행): `run340F_materialize_f01_close_on_flat_false_pressure_mt5_probe_package_without_db_v1`

## Judgment(판정)

run340D(340D 실행)는 MT5(메타트레이더5) package parity(패키지 동등성)는 정확하다. 하지만 p01 control(피01 대조)은 source f01(원본 f01)과 close_on_flat(평탄 신호 청산)이 달라 exact replay control(정확 재생 대조)이 아니다.

Effect(효과): run340D(340D 실행)의 음수 결과를 원본 f01 폐기 근거로 쓰지 않고, close_on_flat=True(평탄 청산 켬) 표면의 부정 결과로만 닫는다.

## Attribution(귀속)

- source f01(원본 f01): close_on_flat=False(평탄 청산 꺼짐), net_profit(순수익) `122.9`, profit_factor(수익 팩터) `1.89`.
- run340D best(340D 최고): close_on_flat=True(평탄 청산 켬), net_profit(순수익) `-25.81`, profit_factor(수익 팩터) `0.78`.
- cause(원인): threshold(임계값) 문제가 아니라 lifecycle exit semantics(생명주기 청산 의미) 변경이 대조군을 무효화했다.

## Next Action(다음 행동)

Open `run340F_materialize_f01_close_on_flat_false_pressure_mt5_probe_package_without_db_v1` with `stages/340_runtime_lifecycle_exit__quality_balance_pressure_review/02_runs/run340E/run340F_queue.csv`.
Effect(효과): close_on_flat=False(평탄 청산 꺼짐)로 원본 f01 exact control(정확 대조)을 복구하고 같은 pressure band(압박 범위)를 다시 MT5(메타트레이더5)에서 확인한다.

## Boundary(경계)

No selected model(선정 모델 없음), no promotion_candidate(승격 후보 없음), no operating_promotion(운영 승격 없음), no runtime_authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
