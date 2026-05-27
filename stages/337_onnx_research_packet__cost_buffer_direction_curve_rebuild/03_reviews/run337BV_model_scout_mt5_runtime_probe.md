# Stage337 run337BV Model Scout MT5 Runtime Probe(모델 스카우트 MT5 런타임 탐침)

## Conclusion(결론)

run337BV(337BV 실행)는 run337BU(337BU 실행)의 proxy expected(프록시 예상)와 MT5 runtime telemetry(MT5 런타임 기록)를 비교했다.

Effect(효과): status(상태)는 `completed_stage337BV_model_scout_mt5_runtime_probe_overlap_parity_tester_gap_remains_no_forward_decision`이고, Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 주장하지 않는다.

## Result(결과)

- status(상태): `completed_stage337BV_model_scout_mt5_runtime_probe_overlap_parity_tester_gap_remains_no_forward_decision`
- judgment(판정): `mt5_runtime_matches_proxy_expected_on_overlap_but_tester_did_not_reach_feature_last`
- decision(결정): `stage337BV_open_run337BW_runtime_probe_gap_review`
- next_action(다음 행동): `run337BW_review_model_scout_runtime_probe_without_db_v1`
- gates(게이트): `8/8`
- attempts(시도): `6`
- matched_rows(일치 행): `46888`
- mismatch_rows(불일치 행): `0`

## Runtime Summary(런타임 요약)

| model(모델) | feature_set(피처 세트) | status(상태) | ready(준비) | matched(일치) | max diff(최대 차이) | feature last(피처 끝) | trades(거래) | net(순익) |
|---|---|---|---:|---:|---:|---|---:|---:|
| `bt_technical42_low_stale_control__logreg_balanced_c1` | `us100_technical42_no_external` | `completed_overlap_proxy_mt5_parity_tester_gap_remains` | 7853 | 7853 | 1.385473902382195e-06 | `False` | 350 | 1.18 |
| `bt_technical42_low_stale_control__extratrees_depth6_leaf120` | `us100_technical42_no_external` | `completed_overlap_proxy_mt5_parity_tester_gap_remains` | 7853 | 7853 | 2.1984688480802816e-07 | `False` | 27 | -133.64 |
| `bt_macro48_macro_lag_ablation__logreg_balanced_c1` | `macro48_no_equity_breadth_or_top3` | `completed_overlap_proxy_mt5_parity_tester_gap_remains` | 7853 | 7853 | 1.5383819128578224e-06 | `False` | 375 | -100.28 |
| `bt_macro48_macro_lag_ablation__extratrees_depth6_leaf120` | `macro48_no_equity_breadth_or_top3` | `completed_overlap_proxy_mt5_parity_tester_gap_remains` | 7853 | 7853 | 2.343770229007447e-07 | `False` | 17 | -17.06 |
| `bt_core56_equity_stale_stress_not_primary__logreg_balanced_c1` | `core56_no_top3_weight_features` | `completed_overlap_proxy_mt5_parity_tester_gap_remains` | 7738 | 7738 | 1.5209375563429717e-06 | `False` | 367 | -142.81 |
| `bt_core56_equity_stale_stress_not_primary__extratrees_depth6_leaf120` | `core56_no_top3_weight_features` | `completed_overlap_proxy_mt5_parity_tester_gap_remains` | 7738 | 7738 | 2.1474952938138614e-07 | `False` | 23 | -79.31 |

## Boundary(경계)

- forward_selection(전진 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `research_development_only_stage337BV_model_scout_mt5_runtime_probe_without_db_no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
