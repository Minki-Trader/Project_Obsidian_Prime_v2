# run304C Curve-Pocket-Aware Profit Source Review(304C 곡선 포켓 인식 수익 원천 검토)

- run_id(실행 ID): `run304C_review_curve_pocket_aware_profit_source_mt5_probe_v1`
- source_run(원천 실행): `run304B_curve_pocket_aware_profit_source_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- scoreboard_rows(점수표 행): `6`
- failure_rows(실패 기억 행): `6`
- best_combined_net_profit(최고 합산 순수익): `-112.11` from `cp304E_extratrees_inverse_pocket_guard_density45_hold3_surface`

Effect(효과): MT5(메타트레이더5) 원본 report source_path(보고서 원천 경로)를 fallback(대체 경로)로 읽어 실제 trade list(거래 목록) 기반 curve pocket(곡선 포켓)을 판정했다.

| package(패키지) | val net(검증 순수익) | val PF(검증 PF) | OOS net(표본외 순수익) | OOS PF(표본외 PF) | trades/day(일거래) | gates(관문) |
|---|---:|---:|---:|---:|---:|---|
| cp304A_histgb_smooth_cash_density65_hold4_scale_surface | -350.65 | 0.87 | -228.73 | 0.90 | 8.97/11.89 | density,scale,eff,curve |
| cp304B_extratrees_quality_veto_density55_hold4_scale_surface | -213.35 | 0.83 | 7.08 | 1.01 | 3.34/3.81 | min,density,scale,eff,curve |
| cp304C_histgb_classifier_density_router_hold6_surface | -302.73 | 0.73 | -126.58 | 0.89 | 4.12/4.42 | scale,eff,curve |
| cp304D_histgb_return_profit_scale_density85_hold6_surface | -338.99 | 0.91 | -396.30 | 0.85 | 4.84/5.59 | scale,eff,curve |
| cp304E_extratrees_inverse_pocket_guard_density45_hold3_surface | -36.95 | 0.97 | -75.16 | 0.93 | 5.21/6.30 | scale,eff,curve |
| cp304F_histgb_aggressive_curve_capped_density95_hold8_surface | -445.48 | 0.79 | -256.66 | 0.91 | 6.33/8.48 | scale,eff,curve |

## Next Stage(다음 단계)

- opened_stage(열린 단계): `305_onnx_candidate_campaign__runtime_realized_curve_attribution_rebuild`
- next_action(다음 행동): `run305A_design_runtime_realized_curve_attribution_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
