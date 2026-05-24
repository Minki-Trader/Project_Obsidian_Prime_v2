# run290C Payoff Weighted Edge Review(290C 손익가중 엣지 검토)

- status(상태): `completed_payoff_weighted_edge_review_no_candidate_stage291_opened`
- judgment(판정): `payoff_weighted_edge_model_did_not_meet_onnx_worthy_gate_no_adapter_no_onnx`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- stage291_seed_count(291단계 씨앗 수): `3`
- next_action(다음 행동): `run291A_design_walk_forward_payoff_generalization_rebuild_packet`

## Scoreboard(점수판)

- `cp290A_xgb_payoff_fwd12_density_hold4_surface`: validation(검증) net `206.83`, PF `1.10`, `5.23` trades/day(일 거래); OOS(표본외) net `83.38`, PF `1.06`, `5.51` trades/day(일 거래); gates(게이트) `passed/failed/failed/failed`.
- `cp290B_lgbm_payoff_cash_hold6_surface`: validation(검증) net `365.01`, PF `1.17`, `6.20` trades/day(일 거래); OOS(표본외) net `216.73`, PF `1.12`, `6.61` trades/day(일 거래); gates(게이트) `passed/failed/failed/failed`.
- `cp290C_extratrees_direction_session_hold6_surface`: validation(검증) net `16.46`, PF `1.01`, `3.90` trades/day(일 거래); OOS(표본외) net `-25.72`, PF `0.98`, `3.61` trades/day(일 거래); gates(게이트) `failed/failed/failed/failed`.
- `cp290D_logreg_smooth_curve_hold4_surface`: validation(검증) net `-122.09`, PF `0.94`, `5.08` trades/day(일 거래); OOS(표본외) net `-182.03`, PF `0.90`, `5.87` trades/day(일 거래); gates(게이트) `passed/failed/failed/failed`.
- `cp290E_xgb_payoff_fwd18_aggressive_hold8_surface`: validation(검증) net `333.45`, PF `1.17`, `4.54` trades/day(일 거래); OOS(표본외) net `127.48`, PF `1.08`, `4.65` trades/day(일 거래); gates(게이트) `passed/failed/failed/failed`.
- `cp290F_histgb_payoff_defensive_hold5_surface`: validation(검증) net `197.89`, PF `1.26`, `2.31` trades/day(일 거래); OOS(표본외) net `173.51`, PF `1.23`, `2.90` trades/day(일 거래); gates(게이트) `failed/failed/passed/failed`.

## Decision(결정)

Stage290(290단계)는 MT5 runtime probe(MT5 런타임 탐침)와 curve/time-slice/trade-quality(곡선/시간구간/거래품질) 검토 전에는 후보를 부르지 않았다. 위 gate(게이트)를 모두 통과한 경우에만 Adapter(어댑터) 단계로 넘긴다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
