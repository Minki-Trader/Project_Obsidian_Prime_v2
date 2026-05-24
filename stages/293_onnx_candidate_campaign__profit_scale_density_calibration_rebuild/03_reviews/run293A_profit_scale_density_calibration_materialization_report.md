# run293A Profit-scale Density Calibration Materialization(293A ??갑??硫뷀??쇰꺼 嫄곕옒 ?쒕??덉씠??臾쇱쭏??

- run_id(?ㅽ뻾 ID): `run293A_design_profit_scale_density_calibration_rebuild_v1`
- status(?곹깭): `completed_profit_scale_density_calibration_candidates_materialized_no_selection`
- judgment(?먯젙): `profit_scale_density_calibration_inputs_materialized_no_candidate_selection`
- branch_count(遺꾧린 ??: `6`
- selected_candidate(?좏깮 ?꾨낫): `none`
- Adapter package(?대뙌???⑦궎吏): `none`
- ONNX readiness(?⑥뿊??以鍮?: `not_claimed`
- next_action(?ㅼ쓬 ?됰룞): `run293B_execute_profit_scale_density_calibration_mt5_probe`

## Thesis(?쇱젣)

Stage292(292단계)는 밀도는 맞지만 validation loss(검증 손실), 순수익 규모 부족, 곡선 포켓이 동시에 남았다. Stage293(293단계)는 같은 repair(수리)가 아니라 runtime-aware simulator calibration(런타임 인식 시뮬레이터 보정), profit-scale density router(순수익 규모/밀도 라우터), smooth curve objective(매끈한 곡선 목적함수)로 decision surface(판단 표면)를 새로 만든다.

## Scoreboard(?먯닔??

- `cp293A_runtime_calibrated_histgb_hold5_surface`: mode(紐⑤뱶) `runtime_calibrated_inverse`, WFO(?뚰겕?ъ썙?? net `-2398.05`bp, validation(寃利? `-4026.45`bp/`9.56` trades/day(??嫄곕옒), OOS(?쒕낯?? `-2302.52`bp/`11.88` trades/day(??嫄곕옒), gates(愿臾? `failed/failed/failed`.
- `cp293B_profit_scale_lgbm_hold7_surface`: mode(紐⑤뱶) `profit_scale_direct`, WFO(?뚰겕?ъ썙?? net `3399.23`bp, validation(寃利? `-3780.60`bp/`6.41` trades/day(??嫄곕옒), OOS(?쒕낯?? `-2241.01`bp/`6.98` trades/day(??嫄곕옒), gates(愿臾? `passed/failed/failed`.
- `cp293C_smooth_curve_extratrees_hold4_surface`: mode(紐⑤뱶) `smooth_curve_router`, WFO(?뚰겕?ъ썙?? net `1053.87`bp, validation(寃利? `-2681.76`bp/`3.97` trades/day(??嫄곕옒), OOS(?쒕낯?? `-301.74`bp/`4.82` trades/day(??嫄곕옒), gates(愿臾? `failed/failed/failed`.
- `cp293D_density_band_xgb_hold6_surface`: mode(紐⑤뱶) `direct`, WFO(?뚰겕?ъ썙?? net `-1743.94`bp, validation(寃利? `-8430.86`bp/`9.49` trades/day(??嫄곕옒), OOS(?쒕낯?? `-3586.70`bp/`10.68` trades/day(??嫄곕옒), gates(愿臾? `failed/failed/failed`.
- `cp293E_hybrid_meta_lgbm_hold8_surface`: mode(紐⑤뱶) `smooth_curve_router`, WFO(?뚰겕?ъ썙?? net `3808.66`bp, validation(寃利? `-5479.46`bp/`6.18` trades/day(??嫄곕옒), OOS(?쒕낯?? `-996.30`bp/`6.53` trades/day(??嫄곕옒), gates(愿臾? `passed/failed/failed`.
- `cp293F_asymmetric_tail_control_xgb_hold5_surface`: mode(紐⑤뱶) `density_profit_scale_router`, WFO(?뚰겕?ъ썙?? net `-1432.80`bp, validation(寃利? `-3854.97`bp/`6.25` trades/day(??嫄곕옒), OOS(?쒕낯?? `-1686.33`bp/`7.33` trades/day(??嫄곕옒), gates(愿臾? `passed/failed/failed`.

## MT5 Queue(MT5 ?湲곗뿴)

- `cp293A_runtime_calibrated_histgb_hold5_surface` -> `run293A_cp293A_runtime_calibrated_histgb_hold5` validation approx(寃利?洹쇱궗) `9.56`/day, OOS approx(?쒕낯??洹쇱궗) `11.88`/day
- `cp293B_profit_scale_lgbm_hold7_surface` -> `run293A_cp293B_profit_scale_lgbm_hold7` validation approx(寃利?洹쇱궗) `6.41`/day, OOS approx(?쒕낯??洹쇱궗) `6.98`/day
- `cp293C_smooth_curve_extratrees_hold4_surface` -> `run293A_cp293C_smooth_curve_extratrees_hold4` validation approx(寃利?洹쇱궗) `3.97`/day, OOS approx(?쒕낯??洹쇱궗) `4.82`/day
- `cp293D_density_band_xgb_hold6_surface` -> `run293A_cp293D_density_band_xgb_hold6` validation approx(寃利?洹쇱궗) `9.49`/day, OOS approx(?쒕낯??洹쇱궗) `10.68`/day
- `cp293E_hybrid_meta_lgbm_hold8_surface` -> `run293A_cp293E_hybrid_meta_lgbm_hold8` validation approx(寃利?洹쇱궗) `6.18`/day, OOS approx(?쒕낯??洹쇱궗) `6.53`/day
- `cp293F_asymmetric_tail_control_xgb_hold5_surface` -> `run293A_cp293F_asymmetric_tail_control_xgb_hold5` validation approx(寃利?洹쇱궗) `6.25`/day, OOS approx(?쒕낯??洹쇱궗) `7.33`/day

## Boundary(寃쎄퀎)

?좏깮 ?꾨낫, Adapter package(?대뙌???⑦궎吏), ONNX readiness(?⑥뿊??以鍮?, Goal Achieve(紐⑺몴 ?ъ꽦)???꾩쭅 二쇱옣?섏? ?딅뒗?? ???곗텧臾쇱? run293B(293B ?ㅽ뻾) MT5 runtime probe(MT5 ?고????먯묠) ?낅젰?대떎.
