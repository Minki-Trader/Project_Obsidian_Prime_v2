# run317A Fresh Non-Time Profit Source Materialization(317A 비시간 수익 원천 물질화)

- run_id(실행 ID): `run317A_design_fresh_non_time_profit_source_rebuild_packet_v1`
- source_run(원천 실행): `run316C_review_post_interaction_profit_scale_curve_mt5_probe_v1`
- candidates(후보): `6`
- MT5 queue rows(MT5 대기열 행): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- next_action(다음 행동): `run317B_execute_fresh_non_time_profit_source_mt5_probe`

Effect(효과): Stage316(316단계)의 시간 기반 실패를 버리고 USDX/ADX/momentum/Bollinger(달러지수/ADX/모멘텀/볼린저) 비시간 feature surface(피처 표면)를 MT5(메타트레이더5) 압박 대상으로 만들었다.

| package(패키지) | val bp(검증 bp) | val PF(검증 수익 팩터) | OOS bp(표본외 bp) | OOS PF(표본외 수익 팩터) | trades/day(일 거래) | gates(관문) |
|---|---:|---:|---:|---:|---:|---|
| cp317A_usdx_extreme_follow_hold1_dense_surface | 2412.70 | 1.10 | 3477.90 | 1.26 | 8.99/8.93 | passed |
| cp317B_usdx_extreme_follow_hold2_scale_surface | 2378.94 | 1.09 | 2890.99 | 1.24 | 9.69/7.84 | passed |
| cp317F_usdx_adx_hybrid_router_hold1_surface | 1228.93 | 1.06 | 4624.75 | 1.46 | 6.68/6.73 | passed |
| cp317C_adx_high_short_hold1_defensive_surface | 1519.04 | 1.15 | 1696.57 | 1.24 | 4.22/4.77 | passed |
| cp317E_bollinger_position_extreme_hold1_surface | 1730.77 | 1.12 | 1173.69 | 1.13 | 4.84/4.85 | passed |
| cp317D_momentum_breadth_long_hold1_surface | 1967.64 | 1.14 | 736.28 | 1.09 | 4.36/4.47 | passed |

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
