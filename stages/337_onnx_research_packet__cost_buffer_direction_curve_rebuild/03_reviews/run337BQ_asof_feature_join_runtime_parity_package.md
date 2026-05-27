# Stage337 run337BQ As-Of Feature Join Runtime Parity Package(시점 기준 피처 결합 런타임 동등성 패키지)

## Conclusion(결론)

run337BQ(337BQ 실행)는 exact timestamp join(정확 시각 결합)을 backward as-of join(후방 시점 기준 결합)으로 바꿔 외부 심볼 정렬 공백을 줄이고, MT5 feature parity probe(MT5 피처 동등성 탐침) 입력 패키지를 만들었다.

Effect(효과): core/macro(핵심/거시) 피처 세트는 더 많은 유효 행을 얻었지만, 최신 raw(원천) 끝 `2026-05-27T13:45:00Z`까지 전부 승격하지 않는다. `overnight_return`이 현재 cash open(현금장 개장)을 요구하므로 session-safe feature end(세션 안전 피처 끝)는 `2026-05-27T06:55:00+00:00`다.

## Result(결과)

- status(상태): `completed_stage337BQ_asof_feature_join_runtime_parity_package_no_training_no_selection`
- judgment(판정): `asof_join_reduced_external_alignment_gap_runtime_parity_package_ready_mt5_not_executed`
- decision(결정): `stage337BQ_open_run337BR_mt5_feature_parity_probe`
- gates(게이트): `12/12`
- materialized_feature_sets(생성 피처 세트): `3`
- latest_feature_timestamp(최신 피처 시각): `2026-05-27T06:55:00+00:00`
- runtime_package(런타임 패키지): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337BQ/mt5_runtime_parity_package/runtime_parity_package_manifest.json`
- next_action(다음 행동): `run337BR_execute_mt5_feature_parity_probe_without_db_v1`

## Improvement(개선)

| feature_set(피처 세트) | BP valid(BP 유효) | BQ valid(BQ 유효) | delta(차이) | BQ last(BQ 마지막) |
|---|---:|---:|---:|---|
| core56_no_top3_weight_features | 2145 | 7810 | 5665 | 2026-05-27T06:55:00+00:00 |
| macro48_no_equity_breadth_or_top3 | 5657 | 7925 | 2268 | 2026-05-27T06:55:00+00:00 |
| us100_technical42_no_external | 7925 | 7925 | 0 | 2026-05-27T06:55:00+00:00 |

## Session Boundary(세션 경계)

- raw_to_feature_gap_minutes(원천-피처 공백 분): `410`
- reason(이유): `overnight_return_requires_current_cash_open_and_current_raw_rows_are_pre_cash_open`

## Lag Risk(지연 위험)

- macro_proxy_max_lag_minutes(거시 대리 최대 지연 분): `975.0`
- equity_cash_max_lag_minutes(주식 현금장 최대 지연 분): `4140.0`
- lookahead_violations(미래참조 위반): `0`
- interpretation(해석): equity(주식) as-of carry(시점 기준 이월)는 행을 살리지만 stale-risk(지연 위험)를 만들 수 있으므로 MT5 parity(동등성) 뒤 별도 stress(압박 시험)가 필요하다.

## Boundary(경계)

- training(학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- actual_mt5_execution(실제 MT5 실행): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `research_development_only_stage337BQ_asof_feature_join_runtime_parity_package_without_db_no_model_training_no_threshold_tuning_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
