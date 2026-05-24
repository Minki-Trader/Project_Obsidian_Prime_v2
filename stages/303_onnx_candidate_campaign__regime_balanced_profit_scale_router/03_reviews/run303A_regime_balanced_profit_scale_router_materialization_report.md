# run303A Regime Balanced Profit Scale Router Materialization(303A 레짐 균형 수익 규모 라우터 물질화)

- status(상태): `completed_regime_balanced_profit_scale_router_candidates_materialized_no_selection`
- judgment(판정): `regime_balanced_profit_scale_router_inputs_materialized_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run303B_execute_regime_balanced_profit_scale_router_mt5_probe`

Effect(효과): Stage302(302단계)의 OOS scale(표본외 규모) 단서를 no-late/session router(후반 제외/세션 라우터) 후보 6개로 바꿨다.

| package(패키지) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | scale(규모) | curve(곡선) |
|---|---:|---:|---:|---:|---|---|---|
| cp303A_hgb10_quiet_cash_open_mid_hold6_density95_balanced_router_surface | 955.8 | 9.43 | 1081.7 | 9.51 | passed | failed | failed |
| cp303B_hgb02_quiet_no_late_hold4_density55_defensive_router_surface | 1542.1 | 5.44 | -0.4 | 5.56 | passed | failed | failed |
| cp303C_hgb02_quiet_no_late_hold4_density45_low_density_router_surface | 1246.7 | 4.58 | 390.4 | 4.40 | passed | failed | failed |
| cp303D_hgb10_quiet_no_late_hold8_density85_oos_scale_router_surface | 468.9 | 8.48 | 455.7 | 8.47 | passed | failed | failed |
| cp303E_hgb02_quiet_cash_open_mid_hold4_density45_validation_guard_surface | 2656.3 | 4.50 | 529.1 | 4.46 | passed | failed | passed |
| cp303F_hgb10_quiet_cash_open_mid_hold8_density85_scale_control_surface | 1143.4 | 8.44 | 1496.2 | 8.56 | passed | failed | failed |

MT5 queue(MT5 대기열): `6` rows(행)
Claim boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
