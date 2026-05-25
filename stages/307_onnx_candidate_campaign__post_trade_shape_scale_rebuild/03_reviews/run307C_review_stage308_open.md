# run307C Post-Trade-Shape Scale Review(307C 거래 형태 이후 수익 규모 검토)

- run_id(실행 ID): `run307C_review_post_trade_shape_scale_mt5_probe_v1`
- source_run(원천 실행): `run307B_post_trade_shape_scale_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- scoreboard_rows(점수표 행): `6`
- failure_rows(실패 기억 행): `6`
- best_combined_net_profit(최고 합산 순수익): `778.18` from `cp307E_inverse_tail_asymmetry_density45_hold8_surface`

Effect(효과): MT5(메타트레이더5) 원본 report source_path(보고서 원천 경로)를 fallback(대체 경로)로 읽어 실제 trade list(거래 목록) 기반 curve pocket(곡선 포켓)을 판정했다.

| package(패키지) | val net(검증 순수익) | val PF(검증 PF) | OOS net(표본외 순수익) | OOS PF(표본외 PF) | trades/day(일거래) | gates(관문) |
|---|---:|---:|---:|---:|---:|---|
| cp307A_hgb_inverse_rank_density55_hold4_surface | -372.81 | 0.86 | -242.31 | 0.94 | 5.53/5.50 | scale,eff,curve |
| cp307B_extratrees_inverse_rank_density70_hold4_surface | -390.39 | 0.89 | -47.78 | 0.99 | 7.20/7.18 | scale,eff,curve |
| cp307C_ensemble_inverse_consensus_density60_hold5_surface | 9.17 | 1.00 | -250.58 | 0.93 | 4.98/4.79 | scale,eff,curve |
| cp307D_outside_late_inverse_amplified_density50_hold6_surface | -345.55 | 0.92 | -32.66 | 0.99 | 4.19/4.01 | scale,eff,curve |
| cp307E_inverse_tail_asymmetry_density45_hold8_surface | 781.68 | 1.12 | -3.50 | 1.00 | 3.49/3.45 | min,density,scale,eff,curve |
| cp307F_inverse_high_density_rf_rank_density90_hold3_surface | -308.58 | 0.89 | 108.28 | 1.06 | 8.98/8.77 | scale,eff,curve |

## Next Stage(다음 단계)

- opened_stage(열린 단계): `308_onnx_candidate_campaign__non_return_rank_profit_source_rebuild`
- next_action(다음 행동): `run308A_design_non_return_rank_profit_source_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
