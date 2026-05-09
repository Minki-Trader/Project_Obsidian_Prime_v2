# Stage39 Input References(39단계 입력 참조)

- Stage38 base/carry reference(38단계 기준 운반 참고): `stages/38_decision_layer__permission_abstention_overlap/02_runs/run32A_permission_abstention_overlap_broad_mt5_probe_v1/tables/stage38_candidate_signal_table.parquet`
- Stage24 survival clock(24단계 생존 시계): `stages/24_exit_model__survival_time_to_event_hold_shape/02_runs/run18B_survival_time_to_event_runtime_probe_v1/predictions/tier_a_survival_permission_predictions.parquet`, `stages/24_exit_model__survival_time_to_event_hold_shape/02_runs/run18B_survival_time_to_event_runtime_probe_v1/predictions/tier_b_survival_permission_predictions.parquet`
- Stage25 hazard lifecycle risk(25단계 위험률 생애주기 위험): `stages/25_exit_model__hazard_trade_lifecycle_risk/02_runs/run19B_hazard_trade_lifecycle_runtime_probe_v1/predictions/tier_a_hazard_permission_predictions.parquet`, `stages/25_exit_model__hazard_trade_lifecycle_risk/02_runs/run19B_hazard_trade_lifecycle_runtime_probe_v1/predictions/tier_b_hazard_permission_predictions.parquet`
- Stage27 tail pressure(27단계 꼬리 압력): `stages/27_tail_model__quantile_boosting_risk_surface/02_runs/run21B_quantile_boosting_tail_risk_runtime_probe_v1/predictions/tier_a_quantile_runtime_predictions.parquet`, `stages/27_tail_model__quantile_boosting_risk_surface/02_runs/run21B_quantile_boosting_tail_risk_runtime_probe_v1/predictions/tier_b_quantile_runtime_predictions.parquet`

효과(effect, 효과): 모든 surface(표면)는 exact timestamp alignment(정확 시각 정렬)로 common table(공통 표)에 합쳐지고, Stage38(38단계)은 context-only(문맥 전용) 단서로만 남긴다.
