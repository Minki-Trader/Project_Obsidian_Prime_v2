# Stage337 run337BY Completed-Day Lock(완성일 잠금)

## Conclusion(결론)

run337BY(337BY 실행)는 tester gap(테스터 공백)을 성공으로 포장하지 않고, MT5가 실제로 본 completed-day window(완성일 구간)를 잠갔다.

Effect(효과): status(상태)는 `completed_stage337BY_completed_day_lock_usable_latest_gap_excluded_no_forward_decision`이다. 이 lock(잠금)은 proxy(프록시)를 겹친 구간 분석에 쓰게 하지만 latest forward(최신 전진), operating(운영), Goal Achieve(목표 달성)는 열지 않는다.

## Result(결과)

- status(상태): `completed_stage337BY_completed_day_lock_usable_latest_gap_excluded_no_forward_decision`
- judgment(판정): `completed_day_proxy_mt5_parity_usable_but_latest_forward_and_operating_claims_not_usable`
- decision(결정): `stage337BY_open_run337BZ_runtime_kpi_attribution_and_no_overfit_research_matrix`
- next_action(다음 행동): `run337BZ_runtime_kpi_attribution_and_no_overfit_research_matrix_without_db_v1`
- gates(게이트): `5/5`
- locked_models(잠근 모델): `6`
- locked_mismatch_rows(잠근 구간 불일치): `0`

## Lock Table(잠금 표)

| model(모델) | cutoff(컷오프) | locked rows(잠근 행) | excluded gap min(제외 공백 분) |
|---|---|---:|---:|
| `bt_technical42_low_stale_control__logreg_balanced_c1` | `2026.05.26 23:55:00` | 7853 | 420.0 |
| `bt_technical42_low_stale_control__extratrees_depth6_leaf120` | `2026.05.26 23:55:00` | 7853 | 420.0 |
| `bt_macro48_macro_lag_ablation__logreg_balanced_c1` | `2026.05.26 23:55:00` | 7853 | 420.0 |
| `bt_macro48_macro_lag_ablation__extratrees_depth6_leaf120` | `2026.05.26 23:55:00` | 7853 | 420.0 |
| `bt_core56_equity_stale_stress_not_primary__logreg_balanced_c1` | `2026.05.26 23:55:00` | 7738 | 420.0 |
| `bt_core56_equity_stale_stress_not_primary__extratrees_depth6_leaf120` | `2026.05.26 23:55:00` | 7738 | 420.0 |

## Locked Proxy Score(잠근 프록시 점수)

| model(모델) | signals(신호) | net log(로그 순익) | PF(수익 팩터) | DD(손실폭) |
|---|---:|---:|---:|---:|
| `bt_technical42_low_stale_control__logreg_balanced_c1` | 3343 | nan | 1.0126274514644107 | nan |
| `bt_technical42_low_stale_control__extratrees_depth6_leaf120` | 84 | nan | 0.2793685701180058 | nan |
| `bt_macro48_macro_lag_ablation__logreg_balanced_c1` | 3372 | nan | 1.040520005732865 | nan |
| `bt_macro48_macro_lag_ablation__extratrees_depth6_leaf120` | 47 | -0.07182853290985383 | 0.35955398954621376 | -0.07711172919387425 |
| `bt_core56_equity_stale_stress_not_primary__logreg_balanced_c1` | 3161 | nan | 1.0009855520082762 | nan |
| `bt_core56_equity_stale_stress_not_primary__extratrees_depth6_leaf120` | 62 | -0.10114864963404271 | 0.3367971126928863 | -0.11067834592297689 |

## Usability(사용성)

| model(모델) | completed day usable(완성일 가능) | latest usable(최신 가능) | operating usable(운영 가능) |
|---|---|---|---|
| `bt_technical42_low_stale_control__logreg_balanced_c1` | `True` | `False` | `False` |
| `bt_technical42_low_stale_control__extratrees_depth6_leaf120` | `True` | `False` | `False` |
| `bt_macro48_macro_lag_ablation__logreg_balanced_c1` | `True` | `False` | `False` |
| `bt_macro48_macro_lag_ablation__extratrees_depth6_leaf120` | `True` | `False` | `False` |
| `bt_core56_equity_stale_stress_not_primary__logreg_balanced_c1` | `True` | `False` | `False` |
| `bt_core56_equity_stale_stress_not_primary__extratrees_depth6_leaf120` | `True` | `False` | `False` |

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `research_development_only_stage337BY_completed_day_lock_without_db_no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
