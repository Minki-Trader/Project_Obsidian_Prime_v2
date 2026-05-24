# run304A Curve-Pocket-Aware Profit Source Materialization(304A 곡선 포켓 인식 수익 원천 물질화)

- status(상태): `completed_curve_pocket_aware_profit_source_candidates_materialized_no_selection`
- judgment(판정): `curve_pocket_aware_profit_source_inputs_materialized_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run304B_execute_curve_pocket_aware_profit_source_mt5_probe`

Effect(효과): Stage303(303단계)의 low net profit(낮은 순수익)과 curve pocket(곡선 포켓) 실패를 좁게 수리하지 않고, WFO(walk-forward optimization, 워크포워드 최적화)에서 local pocket(국소 포켓)을 벌점으로 넣은 새 후보 6개를 MT5(메타트레이더5) 대기열로 넘긴다.

| package(패키지) | mode(모드) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(거래우위) | curve(곡선) |
|---|---|---:|---:|---:|---:|---|---|---|
| cp304B_extratrees_quality_veto_density55_hold4_scale_surface | two_head_router | -2334.4 | 3.38 | 16.4 | 3.77 | failed | failed | failed |
| cp304F_histgb_aggressive_curve_capped_density95_hold8_surface | runtime_calibrated_inverse | -3238.1 | 7.63 | -1299.7 | 9.79 | passed | failed | failed |
| cp304A_histgb_smooth_cash_density65_hold4_scale_surface | runtime_calibrated_inverse | -2996.2 | 8.90 | -3129.6 | 11.92 | failed | failed | failed |
| cp304E_extratrees_inverse_pocket_guard_density45_hold3_surface | conditional_inverse | -2346.3 | 5.14 | -3277.4 | 6.21 | passed | failed | failed |
| cp304C_histgb_classifier_density_router_hold6_surface | smooth_curve_router | -6240.9 | 4.03 | -1454.1 | 4.38 | passed | failed | failed |
| cp304D_histgb_return_profit_scale_density85_hold6_surface | profit_scale_direct | -6110.2 | 7.14 | -2369.8 | 8.28 | passed | failed | failed |

- mt5_queue_rows(MT5 대기열 행): `6`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
