# run305C Runtime-Realized Curve Attribution Review(305C 런타임 실제 곡선 기여도 검토)

- run_id(실행 ID): `run305C_review_runtime_realized_curve_attribution_mt5_probe_v1`
- source_run(원천 실행): `run305B_runtime_realized_curve_attribution_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- scoreboard_rows(점수판 행): `6`
- failure_rows(실패 행): `6`
- best_combined_net_profit(최고 합산 순수익): `131.41` from `cp305C_cp304E_hour19_direct_else_flip_density80_hold6_surface`

Effect(효과): MT5 report source_path(보고서 원천 경로)를 사용해 fallback(대체 경로) 곡선과 trade list(거래 목록)를 기록하고 curve pocket(곡선 포켓)을 판정했다.

| package(패키지) | val net(순수익) | val PF(검증 수익 팩터) | OOS net(순수익) | OOS PF(표본외 수익 팩터) | trades/day(하루 거래) | gates(게이트) |
|---|---:|---:|---:|---:|---:|---|
| cp305A_runtime_loss_flip_cp304D_mid_density65_hold4_surface | -218.03 | 0.93 | 157.62 | 1.07 | 6.40/6.31 | scale,eff,curve |
| cp305B_runtime_loss_flip_cp304E_mid_density65_hold4_surface | -163.69 | 0.87 | -26.44 | 0.97 | 4.83/5.87 | scale,eff,curve |
| cp305C_cp304E_hour19_direct_else_flip_density80_hold6_surface | 147.09 | 1.04 | -15.68 | 0.99 | 3.21/3.76 | min,density,scale,eff,curve |
| cp305D_cp304C_broad_flip_density65_hold4_surface | 81.52 | 1.04 | 17.57 | 1.01 | 4.11/4.53 | scale,eff,curve |
| cp305E_cp304D_lowvol_flip_density55_hold4_surface | 109.35 | 1.12 | -28.74 | 0.97 | 4.10/5.30 | scale,eff,curve |
| cp305F_cp304F_aggressive_flip_mid_density85_hold6_surface | 254.43 | 1.07 | -246.13 | 0.89 | 5.49/7.31 | scale,eff,curve |

## Next Stage(다음 단계)

- opened_stage(개방 단계): `306_onnx_candidate_campaign__anti_surface_trade_shape_rebuild`
- next_action(다음 행동): `run306A_design_anti_surface_trade_shape_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
