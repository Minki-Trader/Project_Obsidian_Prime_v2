# run317C Fresh Non-Time Profit Source Review(317C 새 비시간 수익 원천 검토)

- run_id(실행 ID): `run317C_review_fresh_non_time_profit_source_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- best_combined_net_profit(최고 합산 순수익): `-888.14`; source_package(원천 패키지): `cp317E_bollinger_position_extreme_hold1_surface`

Effect(효과): actual routed total(실제 라우팅 전체)을 거래 목록까지 읽어 최소 거래수, 4-10 trades/day(일 4-10거래), 순수익 규모, PF(수익 팩터), DD(손실폭), recovery(회복), expectancy(기대값), curve pocket(곡선 포켓)을 함께 판정했다.

| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | trades/day(일 거래) | combined(합산) | gates(관문) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp317E_bollinger_position_extreme_hold1_surface | -494.99 | 0.80 | -393.15 | 0.95 | 6.12/6.21 | -888.14 | scale,eff,curve |
| cp317D_momentum_breadth_long_hold1_surface | -499.21 | 0.60 | -469.00 | 0.93 | 3.02/6.08 | -968.21 | min,density,scale,eff,curve |
| cp317C_adx_high_short_hold1_defensive_surface | -494.62 | 0.89 | -475.64 | 0.82 | 7.19/8.20 | -970.26 | scale,eff,curve |
| cp317A_usdx_extreme_follow_hold1_dense_surface | -499.05 | 0.89 | -498.89 | 0.85 | 6.85/10.31 | -997.94 | density,scale,eff,curve |
| cp317F_usdx_adx_hybrid_router_hold1_surface | -499.19 | 0.84 | -498.86 | 0.83 | 4.92/6.83 | -998.05 | scale,eff,curve |
| cp317B_usdx_extreme_follow_hold2_scale_surface | -499.18 | 0.89 | -498.94 | 0.79 | 6.70/6.57 | -998.12 | scale,eff,curve |

- next_stage(다음 단계): `318_onnx_candidate_campaign__post_non_time_curve_stability_rebuild`
- next_action(다음 행동): `run318A_design_post_non_time_curve_stability_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
