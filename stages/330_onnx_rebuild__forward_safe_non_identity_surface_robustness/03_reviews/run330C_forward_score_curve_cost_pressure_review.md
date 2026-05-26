# Run330C Forward Score-Curve Cost Pressure Review(330C 전진 점수 곡선 비용 압박 검토)

- run_id(실행 ID): `run330C_forward_mt5_or_score_curve_review_v1`
- parent_run_id(부모 실행 ID): `run330B_materialize_forward_safe_non_identity_control_surfaces_v1`
- status(상태): `completed_score_curve_cost_pressure_review_no_forward_decision`
- judgment(판정): `score_curve_cost_pressure_completed_research_only_no_forward_decision`
- decision(결정): `stage330C_score_curve_pressure_fragile_runtime_and_regime_review_next`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_score_curve_proxy_and_session_mt5_reference_no_forward_threshold_tuning_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`

## Method(방법)

run330B(330B 실행)의 fixed threshold signal payload(고정 임계값 신호 인계물)를 그대로 읽고, `hold12 non-overlap score proxy(12봉 비중복 점수 대리검증)`를 만들었다. Effect(효과): MT5(`MetaTrader 5`, 메타트레이더5) fill(체결)과 risk logic(위험 로직)을 흉내 낸 성공 주장이 아니라, raw-forward(원본 전진) 공급이 곡선과 비용에서 먼저 깨지는지 보는 압박 판독이다.

Stage329F(329F 실행)의 old-session MT5(기존 세션 MT5)는 reference(참고)로만 복사했다. Effect(효과): 세션 동등 양수 결과를 raw-forward MT5 결과처럼 쓰지 못하게 한다.

## Raw Proxy Top Read(원본 대리검증 상위 판독)

| artifact(산출물) | view(보기) | net(순손익) | PF(수익 팩터) | trades(거래) | DD(손실폭) |
|---|---|---:|---:|---:|---:|
| c56_plain | raw_forward | 208.66 | 2.2885416988 | 76 | 39.085 |
| c56_bal | raw_forward | 166.685 | 1.9400767018 | 70 | 43.05 |
| u42_plain | raw_forward | 125.275 | 1.1830903577 | 322 | 90.2 |
| m48_plain | raw_forward | 123.41 | 1.1924507411 | 299 | 99.275 |
| m48_bal | raw_forward | 103.82 | 1.1662290252 | 297 | 108.375 |
| u42_bal | raw_forward | 93.24 | 1.1326362957 | 306 | 138.575 |

## Pressure Read(압박 판독)

- raw/session high pressure count(원본/세션 고압 개수): `4`
- cost failures at or below +1(비용 +1 이하 실패): `8`
- worst curve pocket net(최악 곡선 포켓 순손익): `-90.5`
- score/MT5 bridge disagreement(점수/MT5 연결 불일치): `0`

Effect(효과): 이 결과는 Forward Passed(전진 통과)가 아니라 run330D(330D 실행)의 regime/source attribution(국면/원천 귀속)과 이후 raw-forward MT5(원본 전진 MT5) 여부를 결정하는 압박 증거다.

## Key Files(주요 파일)

- score kpi(점수 핵심 지표): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330C/score_curve_proxy_kpi_report.csv`
- curve pocket(곡선 포켓): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330C/score_curve_pocket_report.csv`
- cost stress(비용 압박): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330C/score_cost_stress_report.csv`
- lot normalized(로트 정규화): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330C/score_lot_normalized_report.csv`
- raw/session gap(원본/세션 간극): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330C/raw_session_curve_gap_report.csv`
- MT5 reference(메타트레이더5 참고): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330C/session_mt5_reference_kpi_report.csv`

## Next(다음)

`run330D_regime_attribution_v1`
