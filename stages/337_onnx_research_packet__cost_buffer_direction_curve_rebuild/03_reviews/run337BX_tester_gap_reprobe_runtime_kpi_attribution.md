# Stage337 run337BX Tester Gap Reprobe and Runtime KPI Attribution(테스터 공백 재탐침 및 런타임 성과 귀속)

## Conclusion(결론)

run337BX(337BX 실행)는 run337BV/BW(337BV/BW 실행)의 tester gap(테스터 공백)을 같은 ONNX/feature/threshold/lot(온엑스/피처/임계값/로트) 조건으로 다시 탐침하고, MT5 KPI drift(성과 지표 차이)를 귀속했다.

Effect(효과): status(상태)는 `completed_stage337BX_tester_gap_reprobe_gap_remains_runtime_kpi_attribution_partial_no_forward_decision`이다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.

## Result(결과)

- status(상태): `completed_stage337BX_tester_gap_reprobe_gap_remains_runtime_kpi_attribution_partial_no_forward_decision`
- judgment(판정): `tester_gap_remains_after_reprobe_proxy_mt5_overlap_parity_still_holds`
- decision(결정): `stage337BX_open_run337BY_completed_day_lock_or_visibility_repair`
- next_action(다음 행동): `run337BY_completed_day_lock_or_tester_visibility_repair_without_db_v1`
- gates(게이트): `6/6`
- proxy_mt5_mismatch_rows(프록시-MT5 불일치 행): `0`
- feature_last_reached_rows(피처 끝 도달 행): `0`

## Gap Reprobe(공백 재탐침)

| model(모델) | previous gap(이전 공백) | new gap(새 공백) | reached(도달) |
|---|---:|---:|---|
| `bt_technical42_low_stale_control__logreg_balanced_c1` | 420.0 | 420.0 | `False` |
| `bt_technical42_low_stale_control__extratrees_depth6_leaf120` | 420.0 | 420.0 | `False` |
| `bt_macro48_macro_lag_ablation__logreg_balanced_c1` | 420.0 | 420.0 | `False` |
| `bt_macro48_macro_lag_ablation__extratrees_depth6_leaf120` | 420.0 | 420.0 | `False` |
| `bt_core56_equity_stale_stress_not_primary__logreg_balanced_c1` | 420.0 | 420.0 | `False` |
| `bt_core56_equity_stale_stress_not_primary__extratrees_depth6_leaf120` | 420.0 | 420.0 | `False` |

## KPI Attribution(KPI 귀속)

| model(모델) | proxy net log(프록시 로그 순익) | new MT5 net(새 MT5 순익) | PF(수익 팩터) | trades(거래) |
|---|---:|---:|---:|---:|
| `bt_technical42_low_stale_control__logreg_balanced_c1` | 0.0317851477571352 | 1.18 | 1.0 | 350 |
| `bt_technical42_low_stale_control__extratrees_depth6_leaf120` | -0.1455969930824129 | -133.64 | 0.28 | 27 |
| `bt_macro48_macro_lag_ablation__logreg_balanced_c1` | 0.1011749787073735 | -100.28 | 0.89 | 375 |
| `bt_macro48_macro_lag_ablation__extratrees_depth6_leaf120` | -0.0718285329098547 | -17.06 | 0.73 | 17 |
| `bt_core56_equity_stale_stress_not_primary__logreg_balanced_c1` | 0.0024106538174435 | -142.81 | 0.85 | 367 |
| `bt_core56_equity_stale_stress_not_primary__extratrees_depth6_leaf120` | -0.1011486496340438 | -79.31 | 0.42 | 23 |

## Proxy Usability(프록시 사용성)

| model(모델) | usability(사용성) | not usable for(불가 범위) |
|---|---|---|
| `bt_technical42_low_stale_control__logreg_balanced_c1` | `usable_for_overlap_runtime_parity_only(겹친 구간 런타임 동등성에만 사용 가능)` | `not usable for latest forward pocket or operating claim(최신 전진 구간/운영 주장 불가)` |
| `bt_technical42_low_stale_control__extratrees_depth6_leaf120` | `usable_for_overlap_runtime_parity_only(겹친 구간 런타임 동등성에만 사용 가능)` | `not usable for latest forward pocket or operating claim(최신 전진 구간/운영 주장 불가)` |
| `bt_macro48_macro_lag_ablation__logreg_balanced_c1` | `usable_for_overlap_runtime_parity_only(겹친 구간 런타임 동등성에만 사용 가능)` | `not usable for latest forward pocket or operating claim(최신 전진 구간/운영 주장 불가)` |
| `bt_macro48_macro_lag_ablation__extratrees_depth6_leaf120` | `usable_for_overlap_runtime_parity_only(겹친 구간 런타임 동등성에만 사용 가능)` | `not usable for latest forward pocket or operating claim(최신 전진 구간/운영 주장 불가)` |
| `bt_core56_equity_stale_stress_not_primary__logreg_balanced_c1` | `usable_for_overlap_runtime_parity_only(겹친 구간 런타임 동등성에만 사용 가능)` | `not usable for latest forward pocket or operating claim(최신 전진 구간/운영 주장 불가)` |
| `bt_core56_equity_stale_stress_not_primary__extratrees_depth6_leaf120` | `usable_for_overlap_runtime_parity_only(겹친 구간 런타임 동등성에만 사용 가능)` | `not usable for latest forward pocket or operating claim(최신 전진 구간/운영 주장 불가)` |

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `research_development_only_stage337BX_tester_gap_reprobe_runtime_kpi_attribution_without_db_no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
