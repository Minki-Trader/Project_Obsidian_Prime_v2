# run315A Runtime Outcome Feature Interaction Materialization(315A 런타임 결과 피처 상호작용 물질화)

- run_id(실행 ID): `run315A_design_runtime_outcome_feature_interaction_rebuild_packet_v1`
- source_run(원천 실행): `run314C_review_runtime_outcome_feature_source_mt5_probe_v1`
- candidates(후보): `6`
- MT5 queue rows(MT5 대기열 행): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run315B_execute_runtime_outcome_feature_interaction_mt5_probe`

Effect(효과): Stage314(314단계)의 약한 순수익을 그대로 repair(수리)하지 않고, 실제 MT5(메타트레이더5) 시간별 결과에서 20시 sell(매도) 양수 단서와 19/21시 손실 반전 단서를 feature interaction(피처 상호작용) 후보로 물질화했다.

| package(패키지) | val bp(검증 bp) | OOS bp(표본외 bp) | trades/day(일 거래) | gates(관문) |
|---|---:|---:|---:|---|
| cp315D_curve_guard_hour20_22_sell_mirror_release_hold2_surface | -808.86 | -1260.42 | 8.60/9.51 | edge,curve |
| cp315A_hour20_sell_lowvol_mirror19_21_hold3_surface | -1760.99 | -1874.27 | 8.29/8.77 | edge,curve |
| cp315E_hour20_sell_23buy_asymmetric_release_hold3_surface | -2000.11 | -2456.77 | 8.50/9.04 | edge,curve |
| cp315B_hour20_22_sell_full_mirror_hold3_surface | -3041.94 | -4131.42 | 9.98/10.81 | density,edge,curve |
| cp315F_aggressive_hour20_sell_inversion_convexity_hold4_surface | -4529.02 | -3035.63 | 8.45/8.94 | edge,curve |
| cp315C_hour20_sell_21mirror_19guard_hold2_surface | -5960.41 | -3790.28 | 10.64/11.33 | density,edge,curve |

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
