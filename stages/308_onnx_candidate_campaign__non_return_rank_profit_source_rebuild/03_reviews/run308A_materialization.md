# run308A Non-Return-Rank Profit Source Materialization(308A 비수익순위 수익 원천 물질화)

- status(상태): `completed_non_return_rank_profit_source_candidates_materialized_no_selection`
- judgment(판정): `non_return_rank_profit_source_surfaces_materialized_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run308B_execute_non_return_rank_profit_source_mt5_probe`

Effect(효과): Stage307(307단계)의 return-rank(수익 순위) 실패를 버리고 session/breadth/volatility/trend(세션/브레드스/변동성/추세) 기반 비수익순위 후보를 만들었다.

| package(패키지) | surface(표면) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(우위) | curve(곡선) |
|---|---|---:|---:|---:|---:|---|---|---|
| cp308E_trend_quality_continuation_density50_hold7_surface | trend_quality_continuation_router | 376.0 | 5.01 | 2214.2 | 4.95 | passed | failed | failed |
| cp308F_opening_breadth_impulse_density90_hold3_surface | opening_breadth_impulse_router | 100.8 | 8.79 | 575.9 | 8.75 | passed | failed | failed |
| cp308C_macro_breadth_divergence_density55_hold6_surface | macro_breadth_divergence_router | -980.2 | 5.58 | -212.6 | 5.40 | passed | failed | failed |
| cp308A_realized_session_edge_density60_hold5_surface | realized_session_edge_router | -3670.4 | 5.89 | -944.4 | 5.99 | passed | failed | failed |
| cp308D_volatility_reversion_density85_hold3_surface | volatility_reversion_router | -2985.0 | 8.42 | -3573.3 | 8.51 | passed | failed | failed |
| cp308B_curve_pocket_guard_density70_hold4_surface | curve_pocket_guard_router | -5167.3 | 6.98 | -306.3 | 7.00 | passed | failed | failed |

- mt5_queue_rows(MT5 대기열 수): `6`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
