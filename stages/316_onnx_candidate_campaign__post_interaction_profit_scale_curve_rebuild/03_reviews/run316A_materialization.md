# run316A Post Interaction Profit Scale Curve Materialization(316A 상호작용 이후 수익 규모/곡선 물질화)

- run_id(실행 ID): `run316A_design_post_interaction_profit_scale_curve_rebuild_packet_v1`
- source_run(원천 실행): `run315C_review_runtime_outcome_feature_interaction_mt5_probe_v1`
- candidates(후보): `6`
- MT5 queue rows(MT5 대기열 행): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- next_action(다음 행동): `run316B_execute_post_interaction_profit_scale_curve_mt5_probe`

Effect(효과): Stage315(315단계)의 mirror(반전) 실패를 버리고, 20/22시 sell-only(매도 전용) 시간 내부 샘플링으로 수익 규모와 곡선을 다시 압박한다.

| package(패키지) | val bp(검증 bp) | OOS bp(표본외 bp) | trades/day(일 거래) | gates(관문) |
|---|---:|---:|---:|---|
| cp316B_hour20_22_dense_sell_curve_guard_hold1_surface | -2539.55 | -1078.73 | 4.79/5.28 | edge,curve |
| cp316C_hour20_primary_22_support_sell_scale_hold3_surface | -2576.28 | -1060.55 | 4.75/5.24 | edge,curve |
| cp316D_hour20_22_lowvol_sell_smooth_hold2_surface | -2464.99 | -1211.55 | 4.84/5.34 | edge,curve |
| cp316F_aggressive_hour20_22_sell_convexity_hold3_surface | -2959.54 | -845.73 | 4.40/4.73 | edge,curve |
| cp316A_hour20_22_stagger_sell_hold2_surface | -3367.57 | -1172.53 | 4.93/5.40 | edge,curve |
| cp316E_hour20_22_sell_23buy_tail_hold2_surface | -3367.57 | -1172.53 | 4.93/5.40 | edge,curve |

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
