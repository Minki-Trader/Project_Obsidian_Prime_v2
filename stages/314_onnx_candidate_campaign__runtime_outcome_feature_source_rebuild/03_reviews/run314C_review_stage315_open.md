# run314C Runtime Outcome Feature Source Review(314C 런타임 결과 피처 원천 검토)

- run_id(실행 ID): `run314C_review_runtime_outcome_feature_source_mt5_probe_v1`
- source_run(원천 실행): `run314B_execute_runtime_outcome_feature_source_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- best_combined_net_profit(최고 합산 순수익): `21.64`; source_package(원천 패키지): `cp314A_overconfidence_inversion_sell19_hold3_surface`

Effect(효과): actual routed total(실제 라우팅 전체)의 trade list(거래 목록)를 읽어 최소 거래 수, 4-10 trades/day(일 4-10거래), 순수익 규모, 효율, curve pocket(곡선 포켓)을 함께 판정했다.

| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | trades/day(일 거래) | combined(합산) | gates(관문) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp314A_overconfidence_inversion_sell19_hold3_surface | -461.99 | 0.78 | 483.63 | 1.14 | 4.54/4.60 | 21.64 | scale,eff,curve |
| cp314E_curve_pocket_avoidance_sell19_hold2_surface | -378.82 | 0.86 | 68.57 | 1.03 | 5.58/5.69 | -310.25 | scale,eff,curve |
| cp314D_midscore_sell19_21_buy22_release_hold3_surface | -464.00 | 0.82 | 145.04 | 1.05 | 5.03/5.15 | -318.96 | scale,eff,curve |
| cp314B_mid_breadth_pullback_sell19_21_hold4_surface | -399.40 | 0.88 | -145.46 | 0.97 | 3.46/3.32 | -544.86 | min,density,scale,eff,curve |
| cp314F_aggressive_midscale_sell19_21_convexity_hold4_surface | -441.19 | 0.86 | -231.46 | 0.95 | 3.79/3.85 | -672.65 | min,density,scale,eff,curve |
| cp314C_low_range_rsi_pullback_sell18_19_hold3_surface | -420.01 | 0.82 | -257.30 | 0.88 | 5.76/5.56 | -677.31 | scale,eff,curve |

## Decision(결정)

Stage314(314단계)는 selected candidate(선택 후보) 없이 닫는다.
Effect(효과): ONNX-worthy(온엑스 가치 있음) 관문 통과 전에는 ONNX(온엑스)를 시작하지 않는다.

- opened_stage(열린 단계): `315_onnx_candidate_campaign__runtime_outcome_feature_interaction_rebuild`
- next_action(다음 행동): `run315A_design_runtime_outcome_feature_interaction_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
