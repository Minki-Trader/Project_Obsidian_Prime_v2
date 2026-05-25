# run306C Anti-Surface Trade Shape Review(306C 반표면 거래 형태 검토)

- run_id(실행 ID): `run306C_review_anti_surface_trade_shape_mt5_probe_v1`
- source_run(원천 실행): `run306B_anti_surface_trade_shape_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- scoreboard_rows(점수표 행): `6`
- failure_rows(실패 기억 행): `6`
- best_combined_net_profit(최고 합산 순수익): `-40.58` from `cp306C_cp305C305D_hour20_payoff_router_density70_hold5_surface`

Effect(효과): MT5(메타트레이더5) 원본 report source_path(보고서 원천 경로)를 fallback(대체 경로)로 읽어 실제 trade list(거래 목록) 기반 curve pocket(곡선 포켓)을 판정했다.

| package(패키지) | val net(검증 순수익) | val PF(검증 PF) | OOS net(표본외 순수익) | OOS PF(표본외 PF) | trades/day(일거래) | gates(관문) |
|---|---:|---:|---:|---:|---:|---|
| cp306A_cp305D_good_pocket_direct_density50_hold4_surface | -105.10 | 0.97 | -32.40 | 0.98 | 4.90/4.91 | scale,eff,curve |
| cp306B_cp305D_bad_pocket_inverse_density65_hold3_surface | -66.25 | 0.96 | -4.62 | 1.00 | 6.00/6.16 | scale,eff,curve |
| cp306C_cp305C305D_hour20_payoff_router_density70_hold5_surface | -307.02 | 0.96 | 266.44 | 1.06 | 5.74/5.69 | scale,eff,curve |
| cp306D_cp305E_vol_adx_payoff_shape_density55_hold5_surface | -111.17 | 0.98 | -182.35 | 0.91 | 6.96/7.11 | scale,eff,curve |
| cp306E_cp305F_late_runner_density85_hold8_surface | -428.74 | 0.89 | -249.64 | 0.93 | 6.81/6.63 | scale,eff,curve |
| cp306F_blended_trade_shape_scale_density90_hold4_surface | -385.85 | 0.96 | -138.52 | 0.96 | 7.52/7.51 | scale,eff,curve |

## Next Stage(다음 단계)

- opened_stage(열린 단계): `307_onnx_candidate_campaign__post_trade_shape_scale_rebuild`
- next_action(다음 행동): `run307A_design_post_trade_shape_scale_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
