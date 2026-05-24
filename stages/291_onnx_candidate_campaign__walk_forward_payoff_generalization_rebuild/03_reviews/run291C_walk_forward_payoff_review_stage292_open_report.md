# run291C Walk-forward Payoff Review(291C 워크포워드 손익 검토)

- status(상태): `completed_walk_forward_payoff_review_no_candidate_stage292_opened`
- judgment(판정): `walk_forward_payoff_generalization_runtime_probe_negative_no_adapter_no_onnx`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- stage292_seed_count(292단계 씨앗 수): `3`
- next_action(다음 행동): `run292A_design_anti_direction_meta_label_trade_simulator_rebuild_packet`

## Scoreboard(점수판)

- `cp291A_wfo_lgbm_cash_hold6_surface`: validation(검증) net `-495.56`, PF `0.63`, `2.16` trades/day(일 거래); OOS(표본외) net `-496.28`, PF `0.73`, `5.24` trades/day(일 거래); gate(관문) `failed/failed/failed/failed`.
- `cp291B_side_return_xgb_hold8_surface`: validation(검증) net `-300.87`, PF `0.91`, `6.51` trades/day(일 거래); OOS(표본외) net `-347.70`, PF `0.87`, `7.05` trades/day(일 거래); gate(관문) `passed/failed/failed/failed`.
- `cp291C_cost_curve_lgbm_hold5_surface`: validation(검증) net `-496.18`, PF `0.68`, `2.74` trades/day(일 거래); OOS(표본외) net `-88.55`, PF `0.96`, `7.33` trades/day(일 거래); gate(관문) `failed/failed/failed/failed`.
- `cp291D_defensive_density_histgb_hold4_surface`: validation(검증) net `-187.06`, PF `0.88`, `3.62` trades/day(일 거래); OOS(표본외) net `-241.38`, PF `0.81`, `4.53` trades/day(일 거래); gate(관문) `failed/failed/failed/failed`.
- `cp291E_side_relabel_extratrees_hold6_surface`: validation(검증) net `-75.28`, PF `0.95`, `3.14` trades/day(일 거래); OOS(표본외) net `-32.81`, PF `0.97`, `3.74` trades/day(일 거래); gate(관문) `failed/failed/failed/failed`.
- `cp291F_wfo_xgb_fwd12_hold6_surface`: validation(검증) net `-358.73`, PF `0.84`, `4.81` trades/day(일 거래); OOS(표본외) net `-196.33`, PF `0.89`, `5.07` trades/day(일 거래); gate(관문) `passed/failed/failed/failed`.

## Stage292 Seeds(292단계 씨앗)

- `stage292_anti_direction_meta_label`: anti-direction meta-label(역방향 메타라벨)이 direct WFO loss(직접 워크포워드 손실)를 invert/skip decision(반전/회피 판단)으로 바꿀 수 있다.
- `stage292_trade_simulator_objective`: trade simulator objective(거래 시뮬레이터 목적함수)가 bar-return proxy(봉 수익 대리값)보다 net/PF/recovery(순수익/PF/회복)를 직접 맞출 수 있다.
- `stage292_density_profit_two_head_router`: two-head router(이중 헤드 라우터)가 density head(밀도 헤드)와 profit-quality head(수익 품질 헤드)를 분리해 4-10 trades/day(일 4-10거래)와 수익 규모를 함께 맞출 수 있다.

## Decision(결정)

Stage291(291단계)은 WFO payoff generalization(워크포워드 손익 일반화)을 실제 MT5(MetaTrader 5, 메타트레이더5) routed total(실제 라우팅 전체)로 확인했지만, 모든 분기가 순손실과 낮은 PF(수익 팩터)로 candidate package(후보 패키지) 기준을 통과하지 못했다.
Effect(효과): 같은 WFO classifier/regressor(분류기/회귀기) repair(수리)를 반복하지 않고 Stage292(292단계)에서 anti-direction meta-label(역방향 메타라벨), trade simulator objective(거래 시뮬레이터 목적함수), density/profit two-head router(밀도/수익 이중 헤드 라우터)로 새 질문을 연다.

## Boundary(경계)

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
