# run312A Fresh Model Asymmetry Materialization(312A 새 모델 비대칭 물질화)

- run_id(실행 ID): `run312A_design_fresh_model_asymmetry_rebuild_packet_v1`
- source_run(원천 실행): `run311C_review_post_allocation_fresh_edge_mt5_probe_v1`
- candidates(후보): `6`
- MT5 queue rows(MT5 대기열 행): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run312B_execute_fresh_model_asymmetry_mt5_probe`

Effect(효과): Stage311(311단계) 시간대 반전 실패를 그대로 고치지 않고, 실제 시간-방향 손익 기억과 품질/곡선 방어를 새 decision surface(판단 표면)로 물질화했다.

| package(패키지) | val bp(검증 bp) | OOS bp(표본외 bp) | trades/day(일 거래) | gates(관문) |
|---|---:|---:|---:|---|
| cp312B_short_core_buy19_release_hold3_surface | 922.72 | -985.08 | 9.00/6.70 | edge,curve |
| cp312A_cash_short_asymmetry_hold3_surface | 1797.02 | -1357.22 | 8.44/6.31 | edge,curve |
| cp312C_defensive_curve_guard_short_hold2_surface | 4175.15 | -2196.19 | 9.61/7.99 | edge,curve |
| cp312F_split_consensus_asymmetry_hold4_surface | 1562.14 | -1540.87 | 9.22/8.92 | edge,curve |
| cp312E_profile_table_density_balancer_hold3_surface | 1415.66 | -1510.46 | 11.11/8.41 | density,edge,curve |
| cp312D_aggressive_short_convexity_hold4_surface | 510.53 | -2046.45 | 8.47/8.57 | edge,curve |

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
