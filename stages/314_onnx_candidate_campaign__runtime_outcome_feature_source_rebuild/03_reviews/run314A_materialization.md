# run314A Runtime Outcome Feature Source Materialization(314A 런타임 결과 피처 원천 물질화)

- run_id(실행 ID): `run314A_design_runtime_outcome_feature_source_rebuild_packet_v1`
- source_run(원천 실행): `run313C_review_runtime_outcome_source_pivot_mt5_probe_v1`
- candidates(후보): `6`
- MT5 queue rows(MT5 대기열 행): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run314B_execute_runtime_outcome_feature_source_mt5_probe`

Effect(효과): Stage313(313단계) 시간대 원천 실패를 그대로 고치지 않고, 실제 손실 포켓과 연결된 overconfidence/feature extreme(과신/피처 극단)을 새 decision surface(판단 표면)로 물질화했다.

| package(패키지) | val bp(검증 bp) | OOS bp(표본외 bp) | trades/day(일 거래) | gates(관문) |
|---|---:|---:|---:|---|
| cp314D_midscore_sell19_21_buy22_release_hold3_surface | 880.57 | 829.20 | 5.95/6.39 | curve |
| cp314A_overconfidence_inversion_sell19_hold3_surface | 711.29 | 763.44 | 5.43/5.85 | curve |
| cp314E_curve_pocket_avoidance_sell19_hold2_surface | 482.11 | 890.78 | 6.69/6.82 | curve |
| cp314F_aggressive_midscale_sell19_21_convexity_hold4_surface | 514.14 | 412.92 | 4.75/5.01 | curve |
| cp314B_mid_breadth_pullback_sell19_21_hold4_surface | 29.11 | 280.16 | 4.29/4.21 | edge,curve |
| cp314C_low_range_rsi_pullback_sell18_19_hold3_surface | -291.65 | 10.49 | 6.95/6.92 | edge,curve |

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
