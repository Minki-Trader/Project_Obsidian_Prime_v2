# Stage337 run337CE Lifecycle-Aware MT5 Runtime Probe(생애주기 인식 MT5 런타임 탐침)

## Conclusion(결론)

run337CE(337CE 실행)는 run337CD(337CD 실행)의 cost2-aware ONNX scout(비용2 인식 온엑스 스카우트)를 MT5 RuntimeProbeEA(MT5 런타임 탐침 EA)로 실행하고 proxy expected(프록시 예상)와 MT5 telemetry(MT5 기록)를 비교했다.

Effect(효과): runtime parity(런타임 동등성) 범위와 tester gap(테스터 공백)을 분리한다. 이 결과는 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.

## Result(결과)

- status(상태): `completed_stage337CE_lifecycle_aware_mt5_runtime_probe_overlap_parity_tester_gap_remains_no_forward_decision`
- judgment(판정): `mt5_runtime_matches_cd_proxy_expected_on_overlap_but_tester_gap_remains_cost2_proxy_guard_failed`
- decision(결정): `stage337CE_open_run337CF_runtime_probe_gap_and_failure_attribution_review`
- next_action(다음 행동): `run337CF_review_lifecycle_aware_runtime_probe_and_failure_attribution_without_db_v1`
- gates(게이트): `8/8`
- attempts(시도): `6`
- matched_rows(일치 행): `46888`
- mismatch_rows(불일치 행): `0`
- runtime_completed_rows(런타임 완료 행): `6`
- feature_last_reached_rows(피처 끝 도달 행): `0`
- parent_cost2_survivors(부모 비용2 생존): `0`

## Runtime Summary(런타임 요약)

| model(모델) | feature_set(피처 세트) | status(상태) | ready(준비) | matched(일치) | max diff(최대 차이) | feature last(피처 끝) | trades(거래) | net(순익) |
|---|---|---|---:|---:|---:|---|---:|---:|
| `cd_bt_technical42_low_stale_control__logreg_cost2_balanced_c075` | `us100_technical42_no_external` | `completed_overlap_proxy_mt5_parity_tester_gap_remains` | 7853 | 7853 | 1.2803779999570608e-06 | `False` | 354 | -22.5 |
| `cd_bt_technical42_low_stale_control__extratrees_cost2_depth5_leaf180` | `us100_technical42_no_external` | `completed_overlap_proxy_mt5_parity_tester_gap_remains` | 7853 | 7853 | 3.0665000000373865e-07 | `False` | 19 | -57.64 |
| `cd_bt_macro48_macro_lag_ablation__logreg_cost2_balanced_c075` | `macro48_no_equity_breadth_or_top3` | `completed_overlap_proxy_mt5_parity_tester_gap_remains` | 7853 | 7853 | 1.4293689999389514e-06 | `False` | 380 | -40.22 |
| `cd_bt_macro48_macro_lag_ablation__extratrees_cost2_depth5_leaf180` | `macro48_no_equity_breadth_or_top3` | `completed_overlap_proxy_mt5_parity_tester_gap_remains` | 7853 | 7853 | 2.918500000004265e-07 | `False` | 13 | -41.21 |
| `cd_bt_core56_equity_stale_stress_not_primary__logreg_cost2_balanced_c075` | `core56_no_top3_weight_features` | `completed_overlap_proxy_mt5_parity_tester_gap_remains` | 7738 | 7738 | 1.387635000016374e-06 | `False` | 381 | -56.38 |
| `cd_bt_core56_equity_stale_stress_not_primary__extratrees_cost2_depth5_leaf180` | `core56_no_top3_weight_features` | `completed_overlap_proxy_mt5_parity_tester_gap_remains` | 7738 | 7738 | 2.9135399998159173e-07 | `False` | 15 | -52.04 |

## CD Lifecycle Proxy(CD 생애주기 프록시)

| model(모델) | closed events(닫힌 이벤트) | net cost1(비용1 순수익) | PF cost1(비용1 수익 팩터) | net cost2(비용2 순수익) | cost2 guard(비용2 가드) |
|---|---:|---:|---:|---:|---|
| `cd_bt_core56_equity_stale_stress_not_primary__extratrees_cost2_depth5_leaf180` | 15 | -0.0204626607237 | 0.372141574232 | -0.0219626607237 | `cost2_forward_proxy_failed_guard` |
| `cd_bt_core56_equity_stale_stress_not_primary__logreg_cost2_balanced_c075` | 381 | -0.0522941766878 | 0.83822813084 | -0.0903941766878 | `cost2_forward_proxy_failed_guard` |
| `cd_bt_macro48_macro_lag_ablation__extratrees_cost2_depth5_leaf180` | 13 | -0.0163041296552 | 0.426570590313 | -0.0176041296552 | `cost2_forward_proxy_failed_guard` |
| `cd_bt_macro48_macro_lag_ablation__logreg_cost2_balanced_c075` | 380 | -0.0439064698471 | 0.866834427505 | -0.0819064698471 | `cost2_forward_proxy_failed_guard` |
| `cd_bt_technical42_low_stale_control__extratrees_cost2_depth5_leaf180` | 19 | -0.0231948478799 | 0.384579204423 | -0.0250948478799 | `cost2_forward_proxy_failed_guard` |
| `cd_bt_technical42_low_stale_control__logreg_cost2_balanced_c075` | 354 | -0.0358433963806 | 0.889339628666 | -0.0712433963806 | `cost2_forward_proxy_failed_guard` |

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `research_development_only_stage337CE_lifecycle_aware_mt5_runtime_probe_without_db_no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
