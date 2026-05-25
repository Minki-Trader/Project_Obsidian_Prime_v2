# run316C Post Interaction Profit Scale Curve Review(316C 상호작용 이후 수익 규모/곡선 검토)

- run_id(실행 ID): `run316C_review_post_interaction_profit_scale_curve_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- best_combined_net_profit(최고 합산 순수익): `-912.28`; source_package(원천 패키지): `cp316F_aggressive_hour20_22_sell_convexity_hold3_surface`

Effect(효과): actual routed total(실제 라우팅 전체)을 거래 목록까지 읽어 최소 거래수, 4-10 trades/day(일 4-10거래), 순수익 규모, PF(수익 팩터), DD(손실폭), recovery(회복), expectancy(기대값), curve pocket(곡선 포켓)을 함께 판정했다.

| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | trades/day(일 거래) | combined(합산) | gates(관문) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp316F_aggressive_hour20_22_sell_convexity_hold3_surface | -498.90 | 0.91 | -413.38 | 0.92 | 6.19/7.55 | -912.28 | scale,eff,curve |
| cp316B_hour20_22_dense_sell_curve_guard_hold1_surface | -493.27 | 0.88 | -426.48 | 0.85 | 5.02/5.62 | -919.75 | scale,eff,curve |
| cp316E_hour20_22_sell_23buy_tail_hold2_surface | -495.51 | 0.90 | -428.88 | 0.87 | 5.86/6.60 | -924.39 | scale,eff,curve |
| cp316A_hour20_22_stagger_sell_hold2_surface | -496.21 | 0.90 | -440.94 | 0.87 | 5.86/6.60 | -937.15 | scale,eff,curve |
| cp316C_hour20_primary_22_support_sell_scale_hold3_surface | -496.60 | 0.90 | -465.50 | 0.86 | 4.61/5.17 | -962.10 | scale,eff,curve |
| cp316D_hour20_22_lowvol_sell_smooth_hold2_surface | -495.13 | 0.87 | -479.29 | 0.83 | 5.09/5.76 | -974.42 | scale,eff,curve |

- next_stage(다음 단계): `317_onnx_candidate_campaign__fresh_non_time_profit_source_rebuild`
- next_action(다음 행동): `run317A_design_fresh_non_time_profit_source_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
