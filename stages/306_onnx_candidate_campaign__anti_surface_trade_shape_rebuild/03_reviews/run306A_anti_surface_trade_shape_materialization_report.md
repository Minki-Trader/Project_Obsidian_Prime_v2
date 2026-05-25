# run306A Anti-Surface Trade Shape Materialization

- status(상태): `completed_anti_surface_trade_shape_candidates_materialized_no_selection`
- judgment(판정): `anti_surface_trade_shape_inputs_materialized_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run306B_execute_anti_surface_trade_shape_mt5_probe`

Effect(효과): Stage305(305단계)의 실제 MT5(메타트레이더5) 거래 기여도를 사용해 session/volatility/ADX/z-shape(세션/변동성/추세강도/변동 형태) 기준의 새 후보를 만들었다.

| package(패키지) | transform(변환) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(우위) | curve(곡선) |
|---|---|---:|---:|---:|---:|---|---|---|
| cp306A_cp305D_good_pocket_direct_density50_hold4_surface | good_pocket_direct | 1280.1 | 5.01 | -207.4 | 4.97 | passed | failed | failed |
| cp306D_cp305E_vol_adx_payoff_shape_density55_hold5_surface | vol_adx_payoff_shape | -988.3 | 6.77 | -797.7 | 6.98 | passed | failed | failed |
| cp306E_cp305F_late_runner_density85_hold8_surface | late_runner | -65.4 | 7.61 | -1360.4 | 7.53 | passed | failed | failed |
| cp306B_cp305D_bad_pocket_inverse_density65_hold3_surface | bad_pocket_inverse | -1309.5 | 6.24 | -1049.4 | 6.42 | passed | failed | failed |
| cp306F_blended_trade_shape_scale_density90_hold4_surface | blended_trade_shape_scale | -3300.1 | 8.99 | -151.3 | 8.95 | passed | failed | failed |
| cp306C_cp305C305D_hour20_payoff_router_density70_hold5_surface | hour20_payoff_router | -3398.1 | 7.03 | -652.0 | 7.01 | passed | failed | failed |

- mt5_queue_rows(MT5 대기열 수): `6`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
