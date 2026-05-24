# run288A Risk Reward Exit Asymmetry Materialization(288A 위험/보상/청산 비대칭 물질화)

- status(상태): `completed_risk_reward_exit_asymmetry_candidates_materialized_no_selection`
- judgment(판정): `risk_reward_exit_candidate_inputs_materialized_no_candidate_selection`
- branch_count(분기 수): `5`
- feature_order(피처 순서): `run288b_route_signal|exit_close_long_flag|exit_close_short_flag|exit_max_hold_bars`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run288B_execute_risk_reward_exit_asymmetry_mt5_probe`

## Queue(대기열)

- `cp288A_scale_rr18_atr_surface`: ATR stop/take `1.0/1.8`, overlay(오버레이) `False`, validation approx(검증 근사) `9.13`, OOS approx(표본외 근사) `9.53` trades/day(일 거래).
- `cp288B_scale_tight_rr30_surface`: ATR stop/take `0.7/2.1`, overlay(오버레이) `False`, validation approx(검증 근사) `9.13`, OOS approx(표본외 근사) `9.53` trades/day(일 거래).
- `cp288C_scale_overlay_rr22_surface`: ATR stop/take `0.9/2.0`, overlay(오버레이) `True`, validation approx(검증 근사) `8.64`, OOS approx(표본외 근사) `8.85` trades/day(일 거래).
- `cp288D_smooth_control_rr24_surface`: ATR stop/take `0.9/2.2`, overlay(오버레이) `False`, validation approx(검증 근사) `4.05`, OOS approx(표본외 근사) `4.38` trades/day(일 거래).
- `cp288E_scale_risk_sized_rr20_surface`: ATR stop/take `1.1/2.2`, overlay(오버레이) `False`, validation approx(검증 근사) `9.13`, OOS approx(표본외 근사) `9.53` trades/day(일 거래).

Effect(효과): 방향 신호의 좁은 임계값 수리가 아니라 ATR SL/TP(ATR 손절/익절), exit overlay(청산 오버레이), risk sizing(위험 크기)을 MT5 probe(MT5 탐침)에 넘긴다.
