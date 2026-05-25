# run307A Post-Trade-Shape Scale Materialization

- status(상태): `completed_post_trade_shape_scale_candidates_materialized_no_selection`
- judgment(판정): `post_trade_shape_scale_ml_surfaces_materialized_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run307B_execute_post_trade_shape_scale_mt5_probe`

Effect(효과): Stage306(306단계)의 rule repair(규칙 수리)를 버리고 ML return-rank(머신러닝 수익 순위) 표면으로 새 수익 규모 후보를 만들었다.

| package(패키지) | model(모델) | surface(표면) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(우위) | curve(곡선) |
|---|---|---|---:|---:|---:|---:|---|---|---|
| cp307A_hgb_inverse_rank_density55_hold4_surface | hgb_return | rank_tail_balanced;signal_policy=inverse_rank | 4000.9 | 5.38 | 106.2 | 5.58 | passed | failed | failed |
| cp307D_outside_late_inverse_amplified_density50_hold6_surface | ensemble_return | outside_late_amplified_rank;signal_policy=inverse_rank | 1836.5 | 4.81 | 216.8 | 4.90 | passed | passed | failed |
| cp307C_ensemble_inverse_consensus_density60_hold5_surface | ensemble_return | consensus_rank_tail;signal_policy=inverse_rank | 984.7 | 5.94 | -241.9 | 6.01 | passed | failed | failed |
| cp307F_inverse_high_density_rf_rank_density90_hold3_surface | rf_return | high_density_rank;signal_policy=inverse_rank | 3308.6 | 9.05 | -1208.5 | 9.05 | passed | failed | failed |
| cp307E_inverse_tail_asymmetry_density45_hold8_surface | hgb_return | extreme_tail_asymmetry;signal_policy=inverse_rank | -92.5 | 4.57 | -202.7 | 4.64 | passed | failed | failed |
| cp307B_extratrees_inverse_rank_density70_hold4_surface | extratrees_return | rank_tail_wide;signal_policy=inverse_rank | 2480.0 | 7.01 | -1377.4 | 7.05 | passed | failed | failed |

- mt5_queue_rows(MT5 대기열 수): `6`
- claim_boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
