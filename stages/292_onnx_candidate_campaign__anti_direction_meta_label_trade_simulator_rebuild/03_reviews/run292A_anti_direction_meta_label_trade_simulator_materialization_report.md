# run292A Anti-direction Meta-label Trade Simulator Materialization(292A 역방향 메타라벨 거래 시뮬레이터 물질화)

- run_id(실행 ID): `run292A_design_anti_direction_meta_label_trade_simulator_rebuild_v1`
- status(상태): `completed_anti_direction_meta_label_trade_simulator_candidates_materialized_no_selection`
- judgment(판정): `anti_direction_meta_label_trade_simulator_inputs_materialized_no_candidate_selection`
- branch_count(분기 수): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run292B_execute_anti_direction_meta_label_trade_simulator_mt5_probe`

## Thesis(논제)

Stage291(291단계)의 broad WFO payoff generalization(넓은 워크포워드 손익 일반화)은 MT5(MetaTrader 5, 메타트레이더5)에서 전부 순손실이었다. Stage292(292단계)는 같은 repair(수리)가 아니라 anti-direction meta-label(역방향 메타라벨), trade simulator objective(거래 시뮬레이터 목적함수), density/profit two-head router(밀도/수익 이중 헤드 라우터)로 direction decision(방향 판단)과 trade acceptance(거래 수락)를 새로 만든다.

## Scoreboard(점수판)

- `cp292A_anti_direction_lgbm_meta_hold6_surface`: mode(모드) `conditional_inverse`, WFO(워크포워드) net `290.04`bp, validation(검증) `202.64`bp/`0.39` trades/day(일 거래), OOS(표본외) `140.52`bp/`0.52` trades/day(일 거래), gates(관문) `failed/passed/failed`.
- `cp292B_trade_sim_xgb_inverse_hold8_surface`: mode(모드) `direct`, WFO(워크포워드) net `1078.06`bp, validation(검증) `-4565.50`bp/`6.25` trades/day(일 거래), OOS(표본외) `253.91`bp/`6.90` trades/day(일 거래), gates(관문) `passed/failed/failed`.
- `cp292C_density_profit_two_head_histgb_hold5_surface`: mode(모드) `conditional_inverse`, WFO(워크포워드) net `53.97`bp, validation(검증) `601.78`bp/`5.96` trades/day(일 거래), OOS(표본외) `904.08`bp/`7.50` trades/day(일 거래), gates(관문) `passed/failed/failed`.
- `cp292D_contrarian_session_extratrees_hold4_surface`: mode(모드) `conditional_inverse`, WFO(워크포워드) net `-1073.33`bp, validation(검증) `-1360.02`bp/`4.04` trades/day(일 거래), OOS(표본외) `-2293.09`bp/`4.73` trades/day(일 거래), gates(관문) `passed/failed/failed`.
- `cp292E_curve_guarded_lgbm_hold10_surface`: mode(모드) `quality_veto_direct`, WFO(워크포워드) net `4351.46`bp, validation(검증) `-4178.55`bp/`7.97` trades/day(일 거래), OOS(표본외) `-1575.49`bp/`8.49` trades/day(일 거래), gates(관문) `passed/failed/failed`.
- `cp292F_aggressive_tail_xgb_meta_hold6_surface`: mode(모드) `inverse`, WFO(워크포워드) net `66.49`bp, validation(검증) `2487.85`bp/`0.36` trades/day(일 거래), OOS(표본외) `273.00`bp/`0.40` trades/day(일 거래), gates(관문) `failed/passed/failed`.

## MT5 Queue(MT5 대기열)

- `cp292A_anti_direction_lgbm_meta_hold6_surface` -> `run292A_cp292A_anti_direction_lgbm_meta_hold6` validation approx(검증 근사) `0.39`/day, OOS approx(표본외 근사) `0.52`/day
- `cp292B_trade_sim_xgb_inverse_hold8_surface` -> `run292A_cp292B_trade_sim_xgb_inverse_hold8` validation approx(검증 근사) `6.25`/day, OOS approx(표본외 근사) `6.90`/day
- `cp292C_density_profit_two_head_histgb_hold5_surface` -> `run292A_cp292C_density_profit_two_head_histgb_hold5` validation approx(검증 근사) `5.96`/day, OOS approx(표본외 근사) `7.50`/day
- `cp292D_contrarian_session_extratrees_hold4_surface` -> `run292A_cp292D_contrarian_session_extratrees_hold4` validation approx(검증 근사) `4.04`/day, OOS approx(표본외 근사) `4.73`/day
- `cp292E_curve_guarded_lgbm_hold10_surface` -> `run292A_cp292E_curve_guarded_lgbm_hold10` validation approx(검증 근사) `7.97`/day, OOS approx(표본외 근사) `8.49`/day
- `cp292F_aggressive_tail_xgb_meta_hold6_surface` -> `run292A_cp292F_aggressive_tail_xgb_meta_hold6` validation approx(검증 근사) `0.36`/day, OOS approx(표본외 근사) `0.40`/day

## Boundary(경계)

선택 후보, Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 아직 주장하지 않는다. 이 산출물은 run292B(292B 실행) MT5 runtime probe(MT5 런타임 탐침) 입력이다.
