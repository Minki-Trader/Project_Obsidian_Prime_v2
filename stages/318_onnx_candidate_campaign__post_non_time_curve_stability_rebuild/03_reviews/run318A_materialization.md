# run318A Post Non-Time Curve Stability Materialization(318A 비시간 이후 곡선 안정성 물질화)

- run_id(실행 ID): `run318A_design_post_non_time_curve_stability_rebuild_packet_v1`
- source_run(원천 실행): `run317C_review_fresh_non_time_profit_source_mt5_probe_v1`
- candidates(후보): `6`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- next_action(다음 행동): `run318B_execute_post_non_time_curve_stability_mt5_probe`

Effect(효과): Stage317(317단계)의 실제 MT5(메타트레이더5) 손익 조각을 비시간 feature surface(피처 표면)로 증류해 MT5(메타트레이더5) 재실행 후보 6개를 만들었다.

Caution(주의): Stage317(317단계) OOS(표본외)도 학습에 포함됐으므로 이 결과는 design evidence(설계 근거)이고, 선택 후보(candidate, 후보)는 run318B/run318C(318B/318C 실행) 이후에만 판단한다.

| package(패키지) | source(원천) | est val net(추정 검증 순수익) | est OOS net(추정 표본외 순수익) | est trades/day(추정 일 거래수) | est PF(추정 수익 팩터) | gates(관문) |
|---|---|---:|---:|---:|---:|---|
| cp318A_outcome_dense20_curve_stability_surface | cp317A_usdx_extreme_follow_hold1_dense_surface | 2749.30 | 1731.30 | 4.04/6.93 | 3.16/2.48 | estimated_passed |
| cp318B_outcome_dense22_pocket_guard_surface | cp317A_usdx_extreme_follow_hold1_dense_surface | 2245.52 | 1425.83 | 4.57/7.75 | 2.26/1.96 | estimated_passed |
| cp318C_bollinger_curve_stability10_surface | cp317E_bollinger_position_extreme_hold1_surface | 347.16 | 3381.43 | 4.85/4.57 | 1.22/1.78 | estimated_passed |
| cp318E_scale_hold2_24_surface | cp317B_usdx_extreme_follow_hold2_scale_surface | 2454.02 | 821.36 | 4.36/4.79 | 2.37/1.79 | estimated_passed |
| cp318D_adx_short_defensive10_surface | cp317C_adx_high_short_hold1_defensive_surface | 2324.26 | 788.84 | 4.46/4.95 | 2.58/1.71 | estimated_passed |
| cp318F_adx_short_density12_surface | cp317C_adx_high_short_hold1_defensive_surface | 1665.95 | 466.16 | 5.39/6.08 | 1.75/1.30 | estimated_passed |

`research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_candidate_package_gate`
