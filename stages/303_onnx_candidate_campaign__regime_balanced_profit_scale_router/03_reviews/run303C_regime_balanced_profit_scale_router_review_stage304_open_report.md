# run303C Regime Balanced Profit Scale Router Review(302C 보상 볼록성 수익 규모 검토)

- run_id(실행 ID): `run303C_review_regime_balanced_profit_scale_router_mt5_probe_v1`
- source_run(원천 실행): `run303B_regime_balanced_profit_scale_router_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- scoreboard_rows(점수판 행): `6`
- failure_rows(실패 기억 행): `6`
- best_combined_net_profit(최고 합산 순수익): `63.47` from `cp303A_hgb10_quiet_cash_open_mid_hold6_density95_balanced_router_surface`

Effect(효과): Stage303(302단계)는 OOS(표본외) 수익 규모를 일부 만들었지만 validation(검증) 안정성, 효율, 곡선 품질을 동시에 만족하지 못해 Adapter(어댑터)와 ONNX(온엑스)로 넘기지 않는다.

## Scoreboard(점수판)

| package(패키지) | val net(검증 순수익) | val PF(검증 수익요인) | OOS net(표본외 순수익) | OOS PF(표본외 수익요인) | trades/day(일 거래수) | gates(관문) |
|---|---:|---:|---:|---:|---:|---|
| cp303A_hgb10_quiet_cash_open_mid_hold6_density95_balanced_router_surface | -117.59 | 0.97 | 181.06 | 1.05 | 6.90/6.95 | scale,eff,curve |
| cp303B_hgb02_quiet_no_late_hold4_density55_defensive_router_surface | -136.62 | 0.93 | 10.87 | 1.01 | 5.01/5.08 | scale,eff,curve |
| cp303C_hgb02_quiet_no_late_hold4_density45_low_density_router_surface | -63.10 | 0.96 | 61.32 | 1.06 | 4.23/4.05 | scale,eff,curve |
| cp303D_hgb10_quiet_no_late_hold8_density85_oos_scale_router_surface | -246.81 | 0.92 | 16.51 | 1.01 | 5.87/5.82 | scale,eff,curve |
| cp303E_hgb02_quiet_cash_open_mid_hold4_density45_validation_guard_surface | -79.44 | 0.94 | 124.73 | 1.14 | 4.25/4.16 | scale,eff,curve |
| cp303F_hgb10_quiet_cash_open_mid_hold8_density85_scale_control_surface | 31.65 | 1.01 | -4.23 | 1.00 | 6.65/6.62 | scale,eff,curve |

## Next Stage(다음 단계)

- opened_stage(열린 단계): `304_onnx_candidate_campaign__curve_pocket_aware_profit_source_rebuild`
- next_action(다음 행동): `run304A_design_curve_pocket_aware_profit_source_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
