# run312C Fresh Model Asymmetry Review(312C 새 모델 비대칭 검토)

- run_id(실행 ID): `run312C_review_fresh_model_asymmetry_mt5_probe_v1`
- source_run(원천 실행): `run312B_execute_fresh_model_asymmetry_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- best_combined_net_profit(최고 합산 순수익): `-44.57`; source_package(원천 패키지): `cp312D_aggressive_short_convexity_hold4_surface`

Effect(효과): actual routed total(실제 라우팅 전체)의 trade list(거래 목록)를 읽어 최소 거래 수, 4-10 trades/day(일 4-10거래), 순수익 규모, 효율, curve pocket(곡선 포켓)을 함께 판정했다.

| package(패키지) | val net(검증 순수익) | val PF(검증 수익 팩터) | OOS net(표본외 순수익) | OOS PF(표본외 수익 팩터) | trades/day(일 거래) | combined(합산) | gates(관문) |
|---|---:|---:|---:|---:|---:|---:|---|
| cp312D_aggressive_short_convexity_hold4_surface | -465.59 | 0.89 | 421.02 | 1.05 | 6.24/6.21 | -44.57 | scale,eff,curve |
| cp312C_defensive_curve_guard_short_hold2_surface | -207.66 | 0.97 | -233.22 | 0.90 | 8.16/6.73 | -440.88 | scale,eff,curve |
| cp312F_split_consensus_asymmetry_hold4_surface | -377.24 | 0.96 | -102.60 | 0.98 | 7.25/7.02 | -479.84 | scale,eff,curve |
| cp312B_short_core_buy19_release_hold3_surface | -400.84 | 0.94 | -252.61 | 0.90 | 8.52/6.21 | -653.45 | scale,eff,curve |
| cp312E_profile_table_density_balancer_hold3_surface | -362.28 | 0.96 | -328.87 | 0.89 | 10.68/7.97 | -691.15 | density,scale,eff,curve |
| cp312A_cash_short_asymmetry_hold3_surface | -322.59 | 0.96 | -371.37 | 0.82 | 6.48/4.72 | -693.96 | scale,eff,curve |

## Decision(결정)

Stage312(312단계)는 selected candidate(선택 후보) 없이 닫는다.
Effect(효과): ONNX-worthy(온엑스 가치 있음) 관문 통과 전에는 ONNX(온엑스)를 시작하지 않는다.

- opened_stage(열린 단계): `313_onnx_candidate_campaign__runtime_outcome_source_pivot_rebuild`
- next_action(다음 행동): `run313A_design_runtime_outcome_source_pivot_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
