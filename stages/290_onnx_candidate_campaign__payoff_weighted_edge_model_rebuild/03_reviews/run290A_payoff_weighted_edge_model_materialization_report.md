# run290A Payoff Weighted Edge Model Materialization(290A 손익가중 엣지 모델 물질화)

- status(상태): `completed_payoff_weighted_edge_model_candidates_materialized_no_selection`
- judgment(판정): `payoff_weighted_model_inputs_materialized_no_candidate_selection`
- branch_count(분기 수): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run290B_execute_payoff_weighted_edge_model_mt5_probe`

## Fresh Thesis(새 논제)

Inherited signal filtering(계승 신호 필터링)을 더 깎지 않고, payoff-weighted model surface(손익가중 모델 표면)가 trade density(거래 밀도), profit scale(수익 규모), curve smoothness(곡선 매끈함)를 같이 만들 수 있는지 본다.

## Proxy Scoreboard(대리 점수판)

- `cp290A_xgb_payoff_fwd12_density_hold4_surface`: validation proxy(검증 대리) net `6104.6`bp PF `1.36` tpd `5.77`, OOS proxy(표본외 대리) net `-527.9`bp PF `0.96` tpd `6.08`, gates(게이트) `passed/failed/failed`.
- `cp290B_lgbm_payoff_cash_hold6_surface`: validation proxy(검증 대리) net `4428.0`bp PF `1.24` tpd `6.47`, OOS proxy(표본외 대리) net `-1342.6`bp PF `0.91` tpd `7.00`, gates(게이트) `passed/failed/failed`.
- `cp290D_logreg_smooth_curve_hold4_surface`: validation proxy(검증 대리) net `4357.7`bp PF `1.24` tpd `5.54`, OOS proxy(표본외 대리) net `-4439.1`bp PF `0.70` tpd `6.40`, gates(게이트) `passed/failed/failed`.
- `cp290E_xgb_payoff_fwd18_aggressive_hold8_surface`: validation proxy(검증 대리) net `4219.1`bp PF `1.26` tpd `4.73`, OOS proxy(표본외 대리) net `-1076.7`bp PF `0.91` tpd `4.85`, gates(게이트) `passed/failed/failed`.
- `cp290C_extratrees_direction_session_hold6_surface`: validation proxy(검증 대리) net `2041.1`bp PF `1.15` tpd `4.09`, OOS proxy(표본외 대리) net `-844.4`bp PF `0.89` tpd `3.79`, gates(게이트) `failed/failed/failed`.
- `cp290F_histgb_payoff_defensive_hold5_surface`: validation proxy(검증 대리) net `2377.4`bp PF `1.29` tpd `2.39`, OOS proxy(표본외 대리) net `44.0`bp PF `1.01` tpd `3.01`, gates(게이트) `failed/passed/failed`.

## MT5 Queue(MT5 대기열)

- `cp290A_xgb_payoff_fwd12_density_hold4_surface`: validation approx(검증 근사) `5.77`, OOS approx(표본외 근사) `6.08` trades/day(일 거래).
- `cp290B_lgbm_payoff_cash_hold6_surface`: validation approx(검증 근사) `6.47`, OOS approx(표본외 근사) `7.00` trades/day(일 거래).
- `cp290C_extratrees_direction_session_hold6_surface`: validation approx(검증 근사) `4.09`, OOS approx(표본외 근사) `3.79` trades/day(일 거래).
- `cp290D_logreg_smooth_curve_hold4_surface`: validation approx(검증 근사) `5.54`, OOS approx(표본외 근사) `6.40` trades/day(일 거래).
- `cp290E_xgb_payoff_fwd18_aggressive_hold8_surface`: validation approx(검증 근사) `4.73`, OOS approx(표본외 근사) `4.85` trades/day(일 거래).
- `cp290F_histgb_payoff_defensive_hold5_surface`: validation approx(검증 근사) `2.39`, OOS approx(표본외 근사) `3.01` trades/day(일 거래).

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
