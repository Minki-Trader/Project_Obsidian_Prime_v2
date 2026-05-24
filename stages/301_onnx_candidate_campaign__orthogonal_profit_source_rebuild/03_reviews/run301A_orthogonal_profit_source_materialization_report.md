# run301A Orthogonal Profit Source Materialization(301A 직교 수익 원천 물질화)

- status(상태): `completed_orthogonal_profit_source_candidates_materialized_no_selection`
- judgment(판정): `orthogonal_profit_source_inputs_materialized_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `run301B_execute_orthogonal_profit_source_mt5_probe`

Effect(효과): train-only HGB(학습 전용 히스토그램 그래디언트 부스팅)의 predicted return(예측 수익률)을 반대로 써서 mean-reversion(평균회귀) 수익 원천 후보 6개를 만들었다.

| package(패키지) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | scale(규모) | curve(곡선) |
|---|---:|---:|---:|---:|---|---|---|
| cp301A_hgb_inverse_tail_density45_hold2_surface | 4793.3 | 4.59 | 311.2 | 4.57 | passed | passed | failed |
| cp301B_hgb_inverse_efficiency_density55_hold3_surface | 3336.2 | 5.58 | 368.6 | 5.45 | passed | passed | passed |
| cp301C_hgb_inverse_balance_density70_hold4_surface | 2113.6 | 7.01 | 199.6 | 7.05 | passed | failed | failed |
| cp301D_hgb_inverse_scale_density85_hold4_surface | 2149.2 | 8.57 | -447.1 | 8.55 | passed | failed | failed |
| cp301E_hgb_inverse_late_us_density70_hold4_surface | 4364.5 | 6.97 | -857.7 | 7.08 | passed | failed | failed |
| cp301F_hgb_inverse_regularized_density85_hold4_surface | 946.1 | 8.38 | 104.1 | 8.55 | passed | failed | failed |

MT5 queue(MT5 대기열): `6` rows(행)
Claim boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
