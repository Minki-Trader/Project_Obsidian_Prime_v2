# run297A Bi-Level Curve-Monotonic Profit Materialization(297A 이중 단계 곡선 단조 수익 물질화)

- status(상태): `completed_bilevel_curve_monotonic_profit_candidates_materialized_no_selection`
- judgment(판정): `bilevel_curve_monotonic_profit_inputs_materialized_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- next_action(다음 행동): `run297B_execute_bilevel_curve_monotonic_profit_mt5_probe`

Effect(효과): Stage296(296단계)의 실제 MT5(메타트레이더5) 거래 결과를 robust bucket score(강건 구간 점수)로 바꿔, 4-10 trades/day(일 4-10거래)와 수익 규모를 동시에 겨냥하는 후보 6개를 만들었다.

| package(패키지) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(우위) | curve(곡선) |
|---|---:|---:|---:|---:|---|---|---|
| cp297A_robust_bucket_agree_hold2_density45_surface | 1581.1 | 4.48 | 596.6 | 4.49 | passed | passed | passed |
| cp297B_robust_bucket_agree_hold3_density45_surface | 1544.1 | 4.39 | 740.5 | 4.50 | passed | passed | passed |
| cp297C_robust_bucket_agree_hold4_density41_surface | 1235.1 | 4.12 | 824.1 | 4.08 | passed | passed | passed |
| cp297D_union_robust_veto_hold3_density80_surface | 2697.4 | 4.81 | -58.4 | 4.66 | passed | failed | failed |
| cp297E_soft_flip_bad_bucket_hold3_density70_surface | 2544.3 | 4.81 | 53.0 | 4.68 | passed | failed | failed |
| cp297F_curve_veto_agree_hold2_density41_surface | 967.3 | 4.09 | 671.6 | 4.12 | passed | passed | passed |

MT5 queue(MT5 대기열): `6` rows(행)
Claim boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
