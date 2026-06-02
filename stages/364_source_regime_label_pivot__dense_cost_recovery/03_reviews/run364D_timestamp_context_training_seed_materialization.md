# run364D Timestamp Context Training Seed Materialization(run364D 시점 문맥 학습 씨앗 구체화)

- run_id(실행 ID): `run364D_materialize_timestamp_context_training_seed_without_db_v1`
- parent_run_id(부모 실행 ID): `run364C_review_timestamp_context_cost_surface_without_db_v1`
- status(상태): `completed_stage364D_timestamp_context_training_seed_materialized_model_training_opened_no_selection_no_mt5`
- judgment(판정): `timestamp_context_training_seed_materialized_ready_with_month_pressure_no_operating_claim`
- next_run_id(다음 실행 ID): `run364E_train_timestamp_context_cost_filter_model_without_db_v1`
- gates(게이트): `18/18`

Action(행동): q05 long-only trade table(q05 롱 단독 거래표) `1114`행에 timestamp-safe feature columns(시점 안전 피처 컬럼), realized label columns(실현 라벨 컬럼), seed membership(씨앗 소속), month pressure(月 압박)를 붙였다.

Effect(효과): 다음 실행은 hard-coded context rule(하드코딩 문맥 규칙)이 아니라 model training(모델 학습)과 ONNX precheck(ONNX 사전 점검)으로 넘어갈 수 있다.

## Result(결과)

- training_seed_rows(학습 씨앗 행): `1114`
- feature_columns(피처 컬럼): `21`
- label_columns(라벨 컬럼): `5`
- seed_metric_rows(씨앗 지표 행): `8`
- month_pressure_rows(月 압박 행): `64`
- model_task_rows(모델 작업 행): `4`
- primary_seed_id(주 씨앗 ID): `primary_hour_minute_context_guard`
- primary_seed_validation_cost_0_30_net(주 씨앗 검증 +0.30 비용 순수익): `94.32`
- primary_seed_oos_cost_0_30_net(주 씨앗 표본외 +0.30 비용 순수익): `100.52`
- primary_seed_validation_density(주 씨앗 검증 밀도): `3.0983606557`
- primary_seed_oos_density(주 씨앗 표본외 밀도): `3.106870229`

## Seed Metrics(씨앗 지표)

|seed_id|split|trade_count|trade_density|cost_0_30_net|cost_0_30_profit_factor|expectancy_cost_0_30|net_delta_vs_dense_control|
|---|---|---|---|---|---|---|---|
|dense_control_all_long|validation|642|3.5081967213|-146.63|0.9225908289|-0.2283956386|0.0|
|dense_control_all_long|oos|472|3.6030534351|95.96|1.0702303932|0.2033050847|0.0|
|primary_hour_minute_context_guard|validation|567|3.0983606557|94.32|1.0599127226|0.1663492063|240.95|
|primary_hour_minute_context_guard|oos|407|3.106870229|100.52|1.0843826601|0.246977887|4.56|
|hour17_p_long_q80_guard|validation|606|3.3114754098|53.79|1.0327662141|0.0887623762|200.42|
|hour17_p_long_q80_guard|oos|439|3.3511450382|130.18|1.1063205952|0.2965375854|34.22|

## Model Task Queue(모델 작업 대기열)

|queue_id|priority|model_family|target_label|objective|required_control|
|---|---|---|---|---|---|
|s364E_r01_cost_filter_lgbm_seed|1|LightGBM_or_tree_exportable_to_ONNX(LightGBM 또는 ONNX 변환 가능 트리)|label_cost_positive_0_30|learn timestamp context cost filter(시점 문맥 비용 필터 학습)|beat dense_control_all_long on validation and OOS(검증/표본외에서 전체 롱 고밀도 대조 초과)|
|s364E_r02_month_pressure_wfo_control|2|WFO_pressure_control(WFO 압박 대조)|label_cost_positive_0_30|reject models that only win a few months(소수 월만 이기는 모델 거부)|positive month coverage must improve before promotion(승격 전 양수 월 커버리지 개선 필요)|
|s364E_r03_pseudo_label_context_keep_control|3|pseudo_label_control(의사 라벨 대조)|label_primary_context_keep|separate rule imitation from real profit label(규칙 모방과 실제 수익 라벨 분리)|profit-label model must beat pseudo-label imitation(수익 라벨 모델이 의사 라벨 모방을 넘어야 함)|
|s364E_r04_onnx_handoff_precheck|4|ONNX_export_precheck(ONNX 내보내기 사전 점검)|label_cost_positive_0_30|prepare stable numeric feature order for ONNX(ONNX용 안정 숫자 피처 순서 준비)|feature order and output schema must be frozen before MT5 probe(MT5 탐침 전 피처 순서와 출력 스키마 고정)|

## Artifact Boundary(산출물 경계)

- training_seed_table(학습 씨앗 표): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364D/timestamp_context_training_seed_table.csv`
- feature_schema(피처 스키마): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364D/timestamp_context_feature_schema.json`
- seed_metrics(씨앗 지표): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364D/seed_metric_summary.csv`
- month_pressure(月 압박): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364D/month_pressure_matrix.csv`
- model_task_queue(모델 작업 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364D/run364E_model_task_queue.csv`

Action(행동): `run364E_train_timestamp_context_cost_filter_model_without_db_v1`를 열었다.

Effect(효과): 다음 작업은 cost-filter model(비용 필터 모델)을 학습하되, dense control(고밀도 대조), month pressure(月 압박), ONNX handoff(ONNX 인계)를 같이 검증한다.

Claim Boundary(주장 경계): `research_development_materialization_only_timestamp_context_training_seed_no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
