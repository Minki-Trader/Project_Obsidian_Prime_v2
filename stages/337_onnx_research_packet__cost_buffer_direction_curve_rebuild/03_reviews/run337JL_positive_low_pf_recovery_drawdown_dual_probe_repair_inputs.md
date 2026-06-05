# run337JL Positive Low PF Recovery Drawdown Repair Inputs(run337JL 양수 저PF 회복 낙폭 수리 입력)

## Summary(요약)

- run_id(실행 ID): `run337JL_materialize_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run337JK_design_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_without_db_v1`
- judgment(판정): `timestamp_safe_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs_materialized_review_required`
- gates(게이트): `14/14`
- rows(행): `87666`
- feature_count(피처 수): `58`
- weight_columns(가중치 열): `8`
- task_seed_rows(작업 씨앗 행): `8`
- positive_clue_model(긍정 단서 모델): `jf_jd_jc001_runtime_pnl_fwd18_xgboost`
- negative_control_model(부정 대조 모델): `jf_jd_jc007_session_regime_fwd18_xgboost`

## Action(행동)

JD input frame(JD 입력 프레임)에 JL train-only label/weight(학습 전용 라벨/가중치)를 추가했다.
Effect(효과): PF/recovery/drawdown/cost/side/equity(수익 팩터/회복/낙폭/비용/방향/수익곡선) 수리를 다음 JM review(JM 검토)와 JN training(JN 학습) 후보로 넘긴다.

## Boundary(경계)

No training(학습 없음), no candidate selection(후보 선정 없음), no MT5 execution(MT5 실행 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
