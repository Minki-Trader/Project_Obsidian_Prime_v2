# run302A Payoff Convexity Profit Scale Materialization(302A 보상 볼록성 수익 규모 물질화)

- status(상태): `completed_payoff_convexity_profit_scale_candidates_materialized_no_selection`
- judgment(판정): `payoff_convexity_profit_scale_inputs_materialized_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run302B_execute_payoff_convexity_profit_scale_mt5_probe`

Effect(효과): Stage301(301단계)의 작은 양수 edge(우위)를 보상/위험 비대칭으로 키울 후보 6개를 만들었다.

| package(패키지) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | scale(규모) | curve(곡선) |
|---|---:|---:|---:|---:|---|---|---|
| cp302A_hgb10_quiet_revert_atrscore_hold8_density95_atr_rr_surface | 2348.5 | 9.55 | 1629.8 | 9.50 | passed | passed | passed |
| cp302B_hgb10_cash_mid_late_atrscore_hold8_density95_atr_rr_surface | 2870.3 | 9.55 | 1603.3 | 9.53 | passed | passed | passed |
| cp302C_hgb02_quiet_revert_atrscore_hold4_density45_fixed_control_surface | 1744.4 | 4.44 | 1402.6 | 4.44 | passed | passed | passed |
| cp302D_hgb10_balanced_band_atrscore_hold8_density75_defensive_rr_surface | 1376.2 | 7.45 | 1470.7 | 7.53 | passed | failed | passed |
| cp302E_hgb10_late_us_atrscore_hold6_density75_convex_rr_surface | 4342.6 | 7.48 | 839.2 | 7.52 | passed | passed | passed |
| cp302F_hgb02_vol_convex_late_absscore_hold5_density55_rr_surface | 2227.0 | 5.49 | -403.7 | 5.38 | passed | failed | failed |

MT5 queue(MT5 대기열): `6` rows(행)
Claim boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
