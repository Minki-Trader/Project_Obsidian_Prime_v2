# Stage337 run337CF Lifecycle Runtime Failure Attribution(생애주기 런타임 실패 귀속)

## Conclusion(결론)

run337CF(337CF 실행)는 run337CE(337CE 실행)의 proxy-MT5 parity(프록시-MT5 동등성) 성공과 run337CD(337CD 실행)의 cost2/direction failure(비용2/방향 실패)를 분리했다.

Effect(효과): 런타임이 틀려서 진 것이 아니라, fixed threshold(고정 임계값) 아래에서 label/action signal(라벨/행동 신호)이 비용과 방향을 이기지 못한 것으로 귀속한다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `completed_stage337CF_runtime_parity_cleared_cost_direction_failure_attributed_no_selection`
- judgment(판정): `runtime_parity_cleared_cost2_and_direction_signal_failure_confirmed_repair_design_next`
- decision(결정): `stage337CF_open_run337CG_directional_label_action_policy_repair_design`
- next_action(다음 행동): `run337CG_design_directional_label_action_policy_repair_without_db_v1`
- gates(게이트): `8/8`
- runtime_mismatch_rows(런타임 불일치 행): `0`
- cost2_failed_models(비용2 실패 모델): `6/6`
- direction_failed_models(방향 실패 모델): `6/6`
- feature_last_reached_rows(피처 끝 도달 행): `0`

## Runtime Attribution(런타임 귀속)

| model(모델) | matched(일치) | mismatch(불일치) | tester gap(테스터 공백) | MT5 trades(MT5 거래) | MT5 net(MT5 순익) | MT5 PF(MT5 수익 팩터) |
|---|---:|---:|---|---:|---:|---:|
| `cd_bt_technical42_low_stale_control__logreg_cost2_balanced_c075` | 7853 | 0 | `tester_gap_remains` | 354 | -22.5 | 0.97 |
| `cd_bt_technical42_low_stale_control__extratrees_cost2_depth5_leaf180` | 7853 | 0 | `tester_gap_remains` | 19 | -57.64 | 0.42 |
| `cd_bt_macro48_macro_lag_ablation__logreg_cost2_balanced_c075` | 7853 | 0 | `tester_gap_remains` | 380 | -40.22 | 0.95 |
| `cd_bt_macro48_macro_lag_ablation__extratrees_cost2_depth5_leaf180` | 7853 | 0 | `tester_gap_remains` | 13 | -41.21 | 0.46 |
| `cd_bt_core56_equity_stale_stress_not_primary__logreg_cost2_balanced_c075` | 7738 | 0 | `tester_gap_remains` | 381 | -56.38 | 0.93 |
| `cd_bt_core56_equity_stale_stress_not_primary__extratrees_cost2_depth5_leaf180` | 7738 | 0 | `tester_gap_remains` | 15 | -52.04 | 0.4 |

## Cost/Direction Attribution(비용/방향 귀속)

| model(모델) | family(계열) | lifecycle net cost1(생애주기 비용1 순익) | PF cost1(PF 비용1) | direction control(방향 대조) | driver(원인) |
|---|---|---:|---:|---|---|
| `cd_bt_technical42_low_stale_control__logreg_cost2_balanced_c075` | `logreg` | -0.0358433963806 | 0.889339628666 | `failed` | `directionality_inverted_or_non_signal` |
| `cd_bt_technical42_low_stale_control__extratrees_cost2_depth5_leaf180` | `extratrees` | -0.0231948478799 | 0.384579204423 | `failed` | `directionality_inverted_or_non_signal+sparse_nonlinear_shape` |
| `cd_bt_macro48_macro_lag_ablation__logreg_cost2_balanced_c075` | `logreg` | -0.0439064698471 | 0.866834427505 | `failed` | `directionality_inverted_or_non_signal` |
| `cd_bt_macro48_macro_lag_ablation__extratrees_cost2_depth5_leaf180` | `extratrees` | -0.0163041296552 | 0.426570590313 | `failed` | `directionality_inverted_or_non_signal+sparse_nonlinear_shape` |
| `cd_bt_core56_equity_stale_stress_not_primary__logreg_cost2_balanced_c075` | `logreg` | -0.0522941766878 | 0.83822813084 | `failed` | `directionality_inverted_or_non_signal` |
| `cd_bt_core56_equity_stale_stress_not_primary__extratrees_cost2_depth5_leaf180` | `extratrees` | -0.0204626607237 | 0.372141574232 | `failed` | `directionality_inverted_or_non_signal+sparse_nonlinear_shape` |

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `research_development_only_stage337CF_lifecycle_runtime_failure_attribution_without_db_no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
