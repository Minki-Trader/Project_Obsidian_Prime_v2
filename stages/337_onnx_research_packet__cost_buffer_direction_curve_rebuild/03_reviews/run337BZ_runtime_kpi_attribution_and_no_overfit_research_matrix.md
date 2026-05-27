# Stage337 run337BZ Runtime KPI/No-Overfit Matrix(런타임 성과/무과적합 행렬)

## Conclusion(결론)

run337BZ(337BZ 실행)는 새 model training(모델 학습), threshold tuning(임계값 조정), lot optimization(로트 최적화)을 하지 않고 BY/BX/BU 근거를 합쳐 원인 행렬을 만들었다.

Effect(효과): 다음 probe(탐침)는 label boundary(라벨 경계)와 execution lifecycle(실행 생애주기)을 먼저 고쳐야 하며, Forward/Goal(전진/목표)은 계속 주장하지 않는다.

## Result(결과)

- status(상태): `completed_stage337BZ_runtime_kpi_no_overfit_matrix_label_lifecycle_first_no_forward_decision`
- judgment(판정): `diagnostic_matrix_points_to_label_boundary_and_runtime_lifecycle_before_new_onnx_claim`
- decision(결정): `stage337BZ_open_run337CA_label_boundary_lifecycle_cost_frontier_probe`
- next_action(다음 행동): `run337CA_label_boundary_lifecycle_cost_frontier_probe_without_db_v1`
- gates(게이트): `19/19`
- runtime_matrix_rows(런타임 행렬 행): `6`
- split_matrix_rows(분할 행렬 행): `6`
- cost_sensitivity_rows(비용 민감도 행): `18`

## Runtime Matrix(런타임 행렬)

| model(모델) | MT5 net(MT5 순익) | MT5 PF(MT5 수익 팩터) | failure modes(실패 모드) | implication(의미) |
|---|---:|---:|---|---|
| `bt_technical42_low_stale_control__logreg_balanced_c1` | 1.18 | 1.0 | `label_boundary_gap;split_overfit_or_fragility;signal_to_trade_compression` | `run337CA_label_boundary_lifecycle_proxy_first` |
| `bt_technical42_low_stale_control__extratrees_depth6_leaf120` | -133.64 | 0.28 | `mt5_pf_below_one;mt5_net_negative;label_boundary_gap;split_overfit_or_fragility` | `run337CA_label_boundary_lifecycle_proxy_first` |
| `bt_macro48_macro_lag_ablation__logreg_balanced_c1` | -100.28 | 0.89 | `mt5_pf_below_one;mt5_net_negative;label_boundary_gap;split_overfit_or_fragility;signal_to_trade_compression` | `run337CA_label_boundary_lifecycle_proxy_first` |
| `bt_macro48_macro_lag_ablation__extratrees_depth6_leaf120` | -17.06 | 0.73 | `mt5_pf_below_one;mt5_net_negative;split_overfit_or_fragility` | `rolling_split_negative_control_before_training` |
| `bt_core56_equity_stale_stress_not_primary__logreg_balanced_c1` | -142.81 | 0.85 | `mt5_pf_below_one;mt5_net_negative;label_boundary_gap;split_overfit_or_fragility;signal_to_trade_compression` | `run337CA_label_boundary_lifecycle_proxy_first` |
| `bt_core56_equity_stale_stress_not_primary__extratrees_depth6_leaf120` | -79.31 | 0.42 | `mt5_pf_below_one;mt5_net_negative;split_overfit_or_fragility;session_concentration` | `rolling_split_negative_control_before_training` |

## Research Lanes(연구 레인)

| lane(레인) | priority(우선순위) | hypothesis(가설) |
|---|---|---|
| `defensive_label_boundary_repair` | `P0` | locked proxy rows mix labelable and non-labelable signals, so profit diagnostics must separate label boundary |
| `defensive_execution_lifecycle_proxy` | `P0` | signal count compresses into far fewer trades under one-position, reverse, and max-hold runtime lifecycle |
| `offensive_cost_session_frontier` | `P1` | a useful future ONNX must survive cost and session concentration without relying on one fragile threshold |
| `visibility_repair_plan` | `P0` | latest tester gap still blocks latest-forward and operating claims |
| `rolling_split_negative_control` | `P1` | train-to-forward degradation suggests model family or feature set may be fitting stale structure |

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `research_development_only_stage337BZ_runtime_kpi_no_overfit_matrix_without_db_no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
