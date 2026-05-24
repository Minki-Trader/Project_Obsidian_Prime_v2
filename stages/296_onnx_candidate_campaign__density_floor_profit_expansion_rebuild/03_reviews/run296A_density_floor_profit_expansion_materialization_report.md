# run296A Density-Floor Profit Expansion Materialization(296A 거래 밀도 하한 수익 확장 물질화)

- status(상태): `completed_density_floor_profit_expansion_candidates_materialized_no_selection`
- judgment(판정): `density_floor_profit_expansion_inputs_materialized_no_candidate_selection`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- next_action(다음 행동): `run296B_execute_density_floor_profit_expansion_mt5_probe`

Effect(효과): Stage295(295단계)의 저밀도 수익 단서를 후보로 보존하지 않고, Stage294(294단계)의 고밀도 OOS(표본외) 단서와 결합해 MT5(메타트레이더5) runtime probe(런타임 탐침) 후보 6개를 만들었다.

| package(패키지) | val bp(검증 bp) | val/day(검증 일거래) | OOS bp(표본외 bp) | OOS/day(표본외 일거래) | density(밀도) | edge(우위) | curve(곡선) |
|---|---:|---:|---:|---:|---|---|---|
| cp296A_cp294C_validation_counter_density8_hold4_surface | 1817.0 | 5.10 | 1878.0 | 5.72 | passed | passed | passed |
| cp296B_cp294F_union_counter_density9_hold4_surface | 1502.1 | 5.66 | 496.4 | 6.31 | passed | passed | failed |
| cp296C_cp294D_profit_expand_density7_hold4_surface | 1117.0 | 3.33 | 1164.5 | 3.75 | failed | passed | passed |
| cp296D_cp294D_session_quota_density9_hold3_surface | 1887.1 | 4.39 | 97.4 | 4.30 | passed | failed | failed |
| cp296E_cp294C_payoff_tail_density10_hold4_surface | 1953.5 | 5.30 | 1567.4 | 5.95 | passed | passed | passed |
| cp296F_cp294E_lowdensity_profit_expand_density8_hold4_surface | -1106.7 | 3.19 | 545.1 | 3.40 | failed | failed | failed |

MT5 queue(MT5 대기열): `6` rows(행)
Claim boundary(주장 경계): `research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
