# run298A Profit-Scale Edge Amplification Materialization(298A 수익 규모 거래우위 증폭 물질화)

- status(상태): `completed_profit_scale_edge_amplification_candidates_materialized_no_selection`
- judgment(판정): `profit_scale_edge_amplification_inputs_materialized_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- next_action(다음 행동): `run298B_execute_profit_scale_edge_amplification_mt5_probe`

Effect(효과): Stage297(297단계)의 실제 MT5(메타트레이더5) 청산 거래 결과를 payoff score(보상 점수)로 바꿔, 4-10 trades/day(일 4-10거래)와 더 큰 순수익 규모를 동시에 겨냥하는 후보 6개를 만들었다.

| package(패키지) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | scale(규모) | curve(곡선) |
|---|---:|---:|---:|---:|---|---|---|
| cp298A_payoff_tail_rank_hold4_density45_surface | -2360.5 | 4.34 | -273.9 | 4.28 | passed | failed | failed |
| cp298B_asymmetric_exit_hold6_density45_surface | -2136.7 | 4.62 | -626.1 | 4.60 | passed | failed | failed |
| cp298C_high_vol_tail_hold5_density40_surface | -431.4 | 4.07 | -303.5 | 3.93 | failed | failed | failed |
| cp298D_session_payoff_router_hold5_density55_surface | 2759.7 | 5.48 | 791.4 | 5.48 | passed | failed | failed |
| cp298E_bad_bucket_flip_hold4_density50_surface | 1318.1 | 4.99 | 845.8 | 5.01 | passed | failed | failed |
| cp298F_density8_payoff_tail_control_surface | -3385.2 | 7.95 | -1457.2 | 8.07 | passed | failed | failed |

MT5 queue(MT5 대기열): `6` rows(행)
Claim boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
