# run302C Payoff Convexity Profit Scale Review(302C 보상 볼록성 수익 규모 검토)

- run_id(실행 ID): `run302C_review_payoff_convexity_profit_scale_mt5_probe_v1`
- source_run(원천 실행): `run302B_payoff_convexity_profit_scale_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- scoreboard_rows(점수판 행): `6`
- failure_rows(실패 기억 행): `6`
- best_combined_net_profit(최고 합산 순수익): `1711.96` from `cp302A_hgb10_quiet_revert_atrscore_hold8_density95_atr_rr_surface`

Effect(효과): Stage302(302단계)는 OOS(표본외) 수익 규모를 일부 만들었지만 validation(검증) 안정성, 효율, 곡선 품질을 동시에 만족하지 못해 Adapter(어댑터)와 ONNX(온엑스)로 넘기지 않는다.

## Scoreboard(점수판)

| package(패키지) | val net(검증 순수익) | val PF(검증 수익요인) | OOS net(표본외 순수익) | OOS PF(표본외 수익요인) | trades/day(일 거래수) | gates(관문) |
|---|---:|---:|---:|---:|---:|---|
| cp302A_hgb10_quiet_revert_atrscore_hold8_density95_atr_rr_surface | 169.06 | 1.03 | 1542.90 | 1.22 | 6.42/6.29 | scale,eff,curve |
| cp302B_hgb10_cash_mid_late_atrscore_hold8_density95_atr_rr_surface | -3.60 | 1.00 | 275.72 | 1.05 | 7.56/7.41 | scale,eff,curve |
| cp302C_hgb02_quiet_revert_atrscore_hold4_density45_fixed_control_surface | 243.29 | 1.15 | 91.11 | 1.08 | 4.13/4.08 | scale,eff,curve |
| cp302D_hgb10_balanced_band_atrscore_hold8_density75_defensive_rr_surface | -36.37 | 0.99 | 93.78 | 1.03 | 5.73/5.70 | scale,eff,curve |
| cp302E_hgb10_late_us_atrscore_hold6_density75_convex_rr_surface | -303.29 | 0.90 | 1007.49 | 1.22 | 5.74/5.46 | scale,eff,curve |
| cp302F_hgb02_vol_convex_late_absscore_hold5_density55_rr_surface | -93.32 | 0.96 | 71.48 | 1.04 | 3.63/3.48 | density,scale,eff,curve |

## Next Stage(다음 단계)

- opened_stage(열린 단계): `303_onnx_candidate_campaign__regime_balanced_profit_scale_router`
- next_action(다음 행동): `run303A_design_regime_balanced_profit_scale_router_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
