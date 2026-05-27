# Stage337 run337BW Runtime Probe Review(런타임 탐침 리뷰)

## Conclusion(결론)

run337BW(337BW 실행)는 run337BV(337BV 실행)의 MT5 runtime probe(런타임 탐침)를 재학습 없이 리뷰했다.

Effect(효과): overlap parity(겹친 구간 동등성)는 통과했지만 tester gap(테스터 공백)과 KPI drift(성과 지표 차이)가 남아 Forward Passed/Failed(전진 통과/실패)는 주장하지 않는다.

## Result(결과)

- status(상태): `completed_stage337BW_runtime_probe_review_overlap_parity_passed_tester_gap_and_kpi_drift_named_no_forward_decision`
- judgment(판정): `runtime_parity_overlap_confirmed_but_tester_gap_and_strategy_kpi_drift_prevent_forward_decision`
- decision(결정): `stage337BW_open_run337BX_gap_reprobe_or_runtime_kpi_attribution`
- next_action(다음 행동): `run337BX_tester_gap_reprobe_or_runtime_kpi_attribution_without_db_v1`
- gates(게이트): `6/6`
- proxy_mt5_mismatch_rows(프록시-MT5 불일치 행): `0`
- tester_gap_rows(테스터 공백 행): `6`

## Gap Review(공백 리뷰)

| model(모델) | last ready(마지막 준비) | expected last(예상 마지막) | gap min(공백 분) |
|---|---|---|---:|
| `bt_technical42_low_stale_control__logreg_balanced_c1` | `2026.05.26 23:55:00` | `2026.05.27 06:55:00` | 420.0 |
| `bt_technical42_low_stale_control__extratrees_depth6_leaf120` | `2026.05.26 23:55:00` | `2026.05.27 06:55:00` | 420.0 |
| `bt_macro48_macro_lag_ablation__logreg_balanced_c1` | `2026.05.26 23:55:00` | `2026.05.27 06:55:00` | 420.0 |
| `bt_macro48_macro_lag_ablation__extratrees_depth6_leaf120` | `2026.05.26 23:55:00` | `2026.05.27 06:55:00` | 420.0 |
| `bt_core56_equity_stale_stress_not_primary__logreg_balanced_c1` | `2026.05.26 23:55:00` | `2026.05.27 06:55:00` | 420.0 |
| `bt_core56_equity_stale_stress_not_primary__extratrees_depth6_leaf120` | `2026.05.26 23:55:00` | `2026.05.27 06:55:00` | 420.0 |

## KPI Boundary(KPI 경계)

| model(모델) | proxy net log(프록시 로그 순익) | MT5 net(MT5 순익) | MT5 PF(MT5 수익 팩터) | MT5 trades(MT5 거래) |
|---|---:|---:|---:|---:|
| `bt_technical42_low_stale_control__logreg_balanced_c1` | 0.0317851477571352 | 1.18 | 1 | 350 |
| `bt_technical42_low_stale_control__extratrees_depth6_leaf120` | -0.1455969930824129 | -133.64 | 0.28 | 27 |
| `bt_macro48_macro_lag_ablation__logreg_balanced_c1` | 0.1011749787073735 | -100.28 | 0.89 | 375 |
| `bt_macro48_macro_lag_ablation__extratrees_depth6_leaf120` | -0.0718285329098547 | -17.06 | 0.73 | 17 |
| `bt_core56_equity_stale_stress_not_primary__logreg_balanced_c1` | 0.0024106538174435 | -142.81 | 0.85 | 367 |
| `bt_core56_equity_stale_stress_not_primary__extratrees_depth6_leaf120` | -0.1011486496340438 | -79.31 | 0.42 | 23 |

## Boundary(경계)

- forward_selection(전진 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `research_development_only_stage337BW_model_scout_runtime_probe_review_without_db_no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
