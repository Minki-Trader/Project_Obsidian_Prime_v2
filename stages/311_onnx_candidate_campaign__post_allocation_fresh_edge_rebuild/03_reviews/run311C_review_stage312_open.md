# run311C Post-Allocation Fresh Edge Review(311C 배분 이후 새 엣지 검토)

- run_id(실행 ID): `run311C_review_post_allocation_fresh_edge_mt5_probe_v1`
- source_run(원천 실행): `run311B_execute_post_allocation_fresh_edge_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- best_combined_net_profit(최고 합산 순수익): `-397.94`; source_package(원천 패키지): `cp311E_conservative_17_18_20_router_hold3_surface`

Effect(효과): actual routed total(실제 라우팅 전체)을 trade list(거래 목록)까지 읽어 최소 거래수, 4-10 trades/day(일 4-10거래), 수익 규모, 효율, curve pocket(곡선 포켓)을 함께 판정했다.

| package(패키지) | val net(검증 순수익) | val PF(검증 PF) | OOS net(표본외 순수익) | OOS PF(표본외 PF) | trades/day(일 거래) | combined(합산) | gates(관문) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp311E_conservative_17_18_20_router_hold3_surface | -430.78 | 0.85 | 32.84 | 1.01 | 6.93/4.86 | -397.94 | scale,eff,curve |
| cp311F_model_feature_adverse_hour_blend_hold4_surface | -471.83 | 0.94 | -65.07 | 0.99 | 10.65/6.07 | -536.90 | density,scale,eff,curve |
| cp311B_hour16_mirror_19_veto_hold4_surface | -454.49 | 0.91 | -279.54 | 0.95 | 10.44/9.82 | -734.03 | density,scale,eff,curve |
| cp311D_oos_scale_preserve_16_19_mirror_hold5_surface | -466.60 | 0.93 | -319.04 | 0.93 | 8.77/8.73 | -785.64 | scale,eff,curve |
| cp311C_adverse_cluster_mirror_hold3_surface | -472.69 | 0.89 | -352.97 | 0.93 | 12.16/11.02 | -825.66 | density,scale,eff,curve |
| cp311A_hour16_19_direction_mirror_hold4_surface | -477.76 | 0.92 | -353.79 | 0.94 | 9.95/9.82 | -831.55 | scale,eff,curve |

## Decision(결정)

Stage311(311단계)은 selected candidate(선택 후보) 없이 닫는다.
Effect(효과): ONNX-worthy(온엑스 가치 있음) 관문 통과 전에는 ONNX(온엑스)를 시작하지 않는다.

- opened_stage(열린 단계): `312_onnx_candidate_campaign__fresh_model_asymmetry_rebuild`
- next_action(다음 행동): `run312A_design_fresh_model_asymmetry_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
