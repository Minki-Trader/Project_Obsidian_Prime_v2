# run308C Non-Return-Rank Profit Source Review(308C 비수익순위 수익 원천 검토)

- run_id(실행 ID): `run308C_review_non_return_rank_profit_source_mt5_probe_v1`
- source_run(원천 실행): `run308B_execute_non_return_rank_profit_source_mt5_probe_v1`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- scoreboard_rows(점수표 행): `6`
- failure_rows(실패 기억 행): `6`
- best_combined_net_profit(최고 합산 순수익): `814.18`; source_package(원천 패키지): `cp308E_trend_quality_continuation_density50_hold7_surface`

Effect(효과): MT5(메타트레이더5) actual routed total(실제 라우팅 전체)을 trade list(거래 목록)까지 다시 읽어 profit scale(수익 규모), efficiency(효율), curve pocket(곡선 포켓), 4-10 trades/day(일 4-10거래)를 함께 판정했다.

| package(패키지) | val net(검증 순수익) | val PF(검증 PF) | OOS net(표본외 순수익) | OOS PF(표본외 PF) | trades/day(일거래) | gates(관문) |
|---|---:|---:|---:|---:|---:|---|
| cp308E_trend_quality_continuation_density50_hold7_surface | 9.23 | 1.00 | 804.95 | 1.12 | 4.27/4.05 | scale,eff,curve |
| cp308F_opening_breadth_impulse_density90_hold3_surface | -335.32 | 0.87 | 159.15 | 1.10 | 8.72/8.69 | scale,eff,curve |
| cp308D_volatility_reversion_density85_hold3_surface | -318.18 | 0.86 | -244.04 | 0.86 | 10.05/10.08 | density,scale,eff,curve |
| cp308C_macro_breadth_divergence_density55_hold6_surface | -256.22 | 0.91 | -362.99 | 0.89 | 4.33/4.20 | scale,eff,curve |
| cp308B_curve_pocket_guard_density70_hold4_surface | -427.94 | 0.82 | -277.57 | 0.88 | 6.89/6.71 | scale,eff,curve |
| cp308A_realized_session_edge_density60_hold5_surface | -480.67 | 0.76 | -310.35 | 0.89 | 4.69/4.79 | scale,eff,curve |

## Decision(결정)

Stage308(308단계)는 selected candidate(선택 후보) 없이 닫는다.
Effect(효과): cp308E(308E 후보)의 OOS(표본외) 수익 단서는 보존하지만, validation(검증) 수익과 curve pocket(곡선 포켓)이 부족해 ONNX(온엑스)는 시작하지 않는다.

- opened_stage(열린 단계): `309_onnx_candidate_campaign__split_coherent_profit_curve_source_rebuild`
- next_action(다음 행동): `run309A_design_split_coherent_profit_curve_source_rebuild_packet`

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
