# run313C Runtime Outcome Source Pivot Review(313C 런타임 결과 원천 전환 검토)

- run_id(실행 ID): `run313C_review_runtime_outcome_source_pivot_mt5_probe_v1`
- source_run(원천 실행): `run313B_execute_runtime_outcome_source_pivot_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- best_combined_net_profit(최고 합산 순수익): `52.04`; source_package(원천 패키지): `cp313B_sell_19_21_scale_hold4_surface`

Effect(효과): actual routed total(실제 라우팅 전체)의 trade list(거래 목록)를 읽어 최소 거래 수, 4-10 trades/day(일 4-10거래), 순수익 규모, 효율, curve pocket(곡선 포켓)을 함께 판정했다.

| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | trades/day(일 거래) | combined(합산) | gates(관문) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp313B_sell_19_21_scale_hold4_surface | -360.48 | 0.90 | 412.52 | 1.07 | 5.14/5.18 | 52.04 | scale,eff,curve |
| cp313F_aggressive_19_21_sell_convexity_hold4_surface | -190.92 | 0.97 | -16.58 | 1.00 | 4.82/4.74 | -207.50 | scale,eff,curve |
| cp313E_month_stabilized_sell_source_hold3_surface | -374.75 | 0.91 | -154.15 | 0.95 | 7.23/8.68 | -528.90 | scale,eff,curve |
| cp313A_sell_18_19_21_outcome_source_hold3_surface | -435.08 | 0.94 | -115.42 | 0.97 | 7.68/8.17 | -550.50 | scale,eff,curve |
| cp313C_sell_18_19_21_density_floor_hold2_surface | -379.36 | 0.89 | -222.53 | 0.90 | 6.95/5.98 | -601.89 | scale,eff,curve |
| cp313D_sell_18_19_21_with_buy22_release_hold3_surface | -483.71 | 0.84 | -207.90 | 0.94 | 9.16/9.77 | -691.61 | scale,eff,curve |

## Decision(결정)

Stage313(313단계)는 selected candidate(선택 후보) 없이 닫는다.
Effect(효과): ONNX-worthy(온엑스 가치 있음) 관문 통과 전에는 ONNX(온엑스)를 시작하지 않는다.

- opened_stage(열린 단계): `314_onnx_candidate_campaign__runtime_outcome_feature_source_rebuild`
- next_action(다음 행동): `run314A_design_runtime_outcome_feature_source_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
