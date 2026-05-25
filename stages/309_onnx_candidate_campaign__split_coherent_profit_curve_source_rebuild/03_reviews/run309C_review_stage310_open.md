# run309C Split-Coherent Profit Curve Source Review(309C 분할 일관 수익 곡선 원천 검토)

- run_id(실행 ID): `run309C_review_split_coherent_profit_curve_source_mt5_probe_v1`
- source_run(원천 실행): `run309B_execute_split_coherent_profit_curve_source_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- best_combined_net_profit(최고 합산 순수익): `891.63`; source_package(원천 패키지): `cp309E_aggressive_oos_scale_trend_reallocation_density45_hold8_surface`

Effect(효과): MT5(메타트레이더5) actual routed total(실제 라우팅 전체)을 trade list(거래 목록)까지 다시 읽어 사용자의 최소 거래 수, 4-10 trades/day(일 4-10거래), 수익 규모, 효율, curve pocket(곡선 포켓) 조건을 함께 판정했다.

| package(패키지) | val net(검증 순수익) | val PF(검증 PF) | OOS net(표본외 순수익) | OOS PF(표본외 PF) | trades/day(일거래) | combined(합산) | gates(관문) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp309E_aggressive_oos_scale_trend_reallocation_density45_hold8_surface | 649.68 | 1.07 | 241.95 | 1.06 | 2.91/2.85 | 891.63 | min,density,scale,eff,curve |
| cp309A_validation_curve_trend_guard_density50_hold5_surface | 522.36 | 1.08 | 273.96 | 1.08 | 3.55/3.40 | 796.32 | min,density,scale,eff,curve |
| cp309C_trend_breadth_confirmation_density55_hold5_surface | 78.44 | 1.02 | 74.31 | 1.03 | 3.40/3.43 | 152.75 | min,density,scale,eff,curve |
| cp309D_open_mid_reversion_curve_floor_density80_hold3_surface | -152.96 | 0.93 | -84.90 | 0.94 | 8.96/8.82 | -237.86 | scale,eff,curve |
| cp309B_defensive_curve_quality_density60_hold4_surface | -430.48 | 0.81 | -291.49 | 0.86 | 5.85/5.79 | -721.97 | scale,eff,curve |
| cp309F_session_balanced_dual_source_density70_hold4_surface | -449.45 | 0.85 | -318.83 | 0.87 | 7.01/6.80 | -768.28 | scale,eff,curve |

## Decision(결정)

Stage309(309단계)는 selected candidate(선택 후보) 없이 닫는다.
Effect(효과): cp309A/cp309E(309A/309E 후보)의 양수 조각은 보존하지만, 전체 관문을 통과하지 못해 ONNX(온엑스)는 시작하지 않는다.

- opened_stage(열린 단계): `310_onnx_candidate_campaign__runtime_positive_fragment_allocation_rebuild`
- next_action(다음 행동): `run310A_design_runtime_positive_fragment_allocation_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
