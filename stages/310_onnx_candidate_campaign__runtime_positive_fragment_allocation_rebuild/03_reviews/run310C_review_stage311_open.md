# run310C Runtime Positive Fragment Allocation Review(310C 런타임 양수 조각 배분 검토)

- run_id(실행 ID): `run310C_review_runtime_positive_fragment_allocation_mt5_probe_v1`
- source_run(원천 실행): `run310B_execute_runtime_positive_fragment_allocation_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- best_combined_net_profit(최고 합산 순수익): `986.72`; source_package(원천 패키지): `cp310A_overlap_density_lift_hold4_surface`

Effect(효과): actual routed total(실제 라우팅 전체)을 trade list(거래 목록)까지 읽어 최소 거래수, 4-10 trades/day(일 4-10거래), 수익 규모, 효율, curve pocket(곡선 포켓)을 함께 판정했다.

| package(패키지) | val net(검증 순수익) | val PF(검증 PF) | OOS net(표본외 순수익) | OOS PF(표본외 PF) | trades/day(일 거래) | combined(합산) | gates(관문) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp310A_overlap_density_lift_hold4_surface | -474.31 | 0.84 | 1461.03 | 1.16 | 9.41/5.61 | 986.72 | scale,eff,curve |
| cp310C_aggressive_fragment_union_hold5_surface | -456.46 | 0.92 | 61.34 | 1.01 | 9.04/9.40 | -395.12 | scale,eff,curve |
| cp310E_drawdown_avoidance_reallocation_hold3_surface | -357.85 | 0.91 | -124.53 | 0.97 | 7.91/7.52 | -482.38 | scale,eff,curve |
| cp310F_scale_density_dual_book_hold4_surface | -499.26 | 0.80 | -296.70 | 0.91 | 13.30/7.18 | -795.96 | density,scale,eff,curve |
| cp310B_curve_floor_session_allocator_hold3_surface | -457.99 | 0.91 | -400.16 | 0.86 | 12.26/11.96 | -858.15 | density,scale,eff,curve |
| cp310D_alternating_session_fragment_router_hold4_surface | -471.93 | 0.88 | -397.27 | 0.89 | 10.66/9.82 | -869.20 | density,scale,eff,curve |

## Decision(결정)

Stage310(310단계)은 selected candidate(선택 후보) 없이 닫는다.
Effect(효과): ONNX-worthy(온엑스 가치 있음) 관문 통과 전에는 ONNX(온엑스)를 시작하지 않는다.

- opened_stage(열린 단계): `311_onnx_candidate_campaign__post_allocation_fresh_edge_rebuild`
- next_action(다음 행동): `run311A_design_post_allocation_fresh_edge_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
