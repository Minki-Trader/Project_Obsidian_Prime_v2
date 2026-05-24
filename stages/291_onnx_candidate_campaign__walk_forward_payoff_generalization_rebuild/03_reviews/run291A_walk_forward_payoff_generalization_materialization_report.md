# run291A Walk-forward Payoff Generalization Materialization(291A 워크포워드 손익 일반화 물질화)

- run_id(실행 ID): `run291A_design_walk_forward_payoff_generalization_rebuild_v1`
- status(상태): `completed_walk_forward_payoff_generalization_candidates_materialized_no_selection`
- judgment(판정): `walk_forward_payoff_generalization_inputs_materialized_no_candidate_selection`
- branch_count(분기 수): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run291B_execute_walk_forward_payoff_generalization_mt5_probe`

## Thesis(논제)

Stage290(290단계)의 가까운 후보는 trade density(거래 밀도)는 맞췄지만 OOS profit scale(표본외 수익 규모), recovery(회복), curve pocket(곡선 포켓)에서 탈락했다. Stage291(291단계)은 validation-only threshold fit(검증 단일 임계값 적합)을 피하기 위해 train-only WFO folds(학습 전용 워크포워드 접힘)로 quantile threshold(분위 임계값)와 orientation(방향)을 고른다.

## Scoreboard(점수판)

- `cp291A_wfo_lgbm_cash_hold6_surface`: WFO(워크포워드) net `1312.96`bp, positive folds(양수 접힘) `0.75`, validation(검증) `-6058.90`bp/`4.95` trades/day(일 거래), OOS(표본외) `-1832.33`bp/`5.71` trades/day(일 거래), gates(게이트) `passed/failed/failed`.
- `cp291B_side_return_xgb_hold8_surface`: WFO(워크포워드) net `1131.63`bp, positive folds(양수 접힘) `0.75`, validation(검증) `-5841.73`bp/`6.86` trades/day(일 거래), OOS(표본외) `1201.82`bp/`7.50` trades/day(일 거래), gates(게이트) `passed/failed/failed`.
- `cp291C_cost_curve_lgbm_hold5_surface`: WFO(워크포워드) net `-576.83`bp, positive folds(양수 접힘) `0.25`, validation(검증) `-4479.99`bp/`6.42` trades/day(일 거래), OOS(표본외) `-1894.78`bp/`7.91` trades/day(일 거래), gates(게이트) `passed/failed/failed`.
- `cp291D_defensive_density_histgb_hold4_surface`: WFO(워크포워드) net `536.77`bp, positive folds(양수 접힘) `0.50`, validation(검증) `-4658.41`bp/`3.90` trades/day(일 거래), OOS(표본외) `-2447.27`bp/`4.82` trades/day(일 거래), gates(게이트) `failed/failed/failed`.
- `cp291E_side_relabel_extratrees_hold6_surface`: WFO(워크포워드) net `-292.07`bp, positive folds(양수 접힘) `0.50`, validation(검증) `-4348.57`bp/`3.26` trades/day(일 거래), OOS(표본외) `-236.75`bp/`3.94` trades/day(일 거래), gates(게이트) `failed/failed/failed`.
- `cp291F_wfo_xgb_fwd12_hold6_surface`: WFO(워크포워드) net `1659.24`bp, positive folds(양수 접힘) `0.50`, validation(검증) `-4534.16`bp/`5.09` trades/day(일 거래), OOS(표본외) `-1050.06`bp/`5.42` trades/day(일 거래), gates(게이트) `passed/failed/failed`.

## MT5 Queue(MT5 대기열)

- `cp291A_wfo_lgbm_cash_hold6_surface` -> `run291A_cp291A_wfo_lgbm_cash_hold6` validation approx `4.95`/day, OOS approx `5.71`/day
- `cp291B_side_return_xgb_hold8_surface` -> `run291A_cp291B_side_return_xgb_hold8` validation approx `6.86`/day, OOS approx `7.50`/day
- `cp291C_cost_curve_lgbm_hold5_surface` -> `run291A_cp291C_cost_curve_lgbm_hold5` validation approx `6.42`/day, OOS approx `7.91`/day
- `cp291D_defensive_density_histgb_hold4_surface` -> `run291A_cp291D_defensive_density_histgb_hold4` validation approx `3.90`/day, OOS approx `4.82`/day
- `cp291E_side_relabel_extratrees_hold6_surface` -> `run291A_cp291E_side_relabel_extratrees_hold6` validation approx `3.26`/day, OOS approx `3.94`/day
- `cp291F_wfo_xgb_fwd12_hold6_surface` -> `run291A_cp291F_wfo_xgb_fwd12_hold6` validation approx `5.09`/day, OOS approx `5.42`/day

## Boundary(경계)

선택 후보, Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 아직 주장하지 않는다. 이 산출물은 run291B(291B 실행) MT5 runtime probe(MT5 런타임 탐침) 입력이다.
