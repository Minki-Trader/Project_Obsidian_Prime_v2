# Stage337 run337FE Repair Input Materialization(337단계 337FE 수리 입력 물질화)

## Conclusion(결론)

Action(행동): run337EW train-only frame(337EW 학습 전용 프레임)에 FD repair weights(FD 수리 가중치)를 물질화했다. Effect(효과): ey003 positive clue(ey003 긍정 단서)를 보존하면서 drawdown/recovery/side balance(낙폭/회복/방향 균형) 수리 입력을 만들었다.

Action(행동): model training(모델 학습), threshold tuning(임계값 튜닝), MT5 execution(MT5 실행)은 하지 않았다. Effect(효과): 다음 FF review(FF 검토)가 feature boundary(피처 경계), weight audit(가중치 감사), training eligibility(학습 적격성)를 먼저 판단한다.

- status(상태): `completed_stage337FE_runtime_positive_clue_repair_inputs_materialized_no_training_no_selection`
- judgment(판정): `train_only_drawdown_recovery_side_balance_repair_inputs_materialized_review_required`
- decision(결정): `stage337FE_open_run337FF_review_runtime_positive_clue_repair_inputs_without_db`
- rows(행): `87666`
- unique_timestamps(고유 시각): `29222`
- cost_policy_count(비용 정책 수): `3`
- feature_count(피처 수): `58`
- new_weight_count(새 가중치 수): `7`
- nonfinite_weight_rows(비유한 가중치 행): `0`
- gates(게이트): `12/12`

## Artifacts(산출물)

- train_only_frame(학습 전용 프레임): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337FE/train_only_runtime_positive_clue_repair_input_frame.parquet`
- feature_set(피처 묶음): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337FE/fe_allowed_model_feature_set.csv`
- weight_recipe(가중치 조리법): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337FE/fd_repair_weight_recipe_matrix.csv`
- weight_audit(가중치 감사): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337FE/fd_repair_weight_audit.csv`
- feature_boundary(피처 경계): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337FE/feature_label_boundary_audit.csv`
- training_task_seeds(학습 작업 씨앗): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337FE/run337FG_training_task_seed_matrix.csv`
- next_queue(다음 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337FE/run337FF_review_queue.csv`

Boundary(경계): FE(337FE 실행)는 materialization only(물질화 전용)이다. Forward/Goal(전진/목표), runtime authority(런타임 권위), operating promotion(운영 승격)은 모두 `not_claimed`다.

Next action(다음 행동): `run337FF_review_side_cost_curve_runtime_positive_clue_drawdown_balance_repair_inputs_without_db_v1`
