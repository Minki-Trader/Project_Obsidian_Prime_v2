# run364E Timestamp Context Cost Filter Model Training(run364E 시점 문맥 비용 필터 모델 학습)

- run_id(실행 ID): `run364E_train_timestamp_context_cost_filter_model_without_db_v1`
- parent_run_id(부모 실행 ID): `run364D_materialize_timestamp_context_training_seed_without_db_v1`
- status(상태): `completed_stage364E_cost_filter_model_trained_onnx_exported_probe_preparation_opened_no_mt5`
- judgment(판정): `positive_model_training_onnx_exportable_research_candidate_for_runtime_probe_no_operating_claim`
- next_run_id(다음 실행 ID): `run364F_prepare_timestamp_context_onnx_runtime_probe_without_db_v1`
- gates(게이트): `19/19`

Action(행동): Stage364D(364D) training seed(학습 씨앗)로 cost-filter classifier(비용 필터 분류기) 4종을 학습하고 validation-derived threshold(검증 파생 임계값)를 OOS(표본외)에 고정 적용했다.

Effect(효과): ONNX-exportable model(ONNX 변환 가능 모델) 중 `best_onnx_model_id`는 `rf_depth3_balanced`이고, MT5 runtime probe(MT5 런타임 탐침) 준비 대상으로 넘길 수 있다.

## Result(결과)

- best_training_model_id(최선 학습 모델 ID): `histgb_l2_leaf7`
- best_training_validation_net(최선 학습 검증 순수익): `294.68`
- best_training_oos_net(최선 학습 표본외 순수익): `137.1`
- best_onnx_model_id(최선 ONNX 모델 ID): `rf_depth3_balanced`
- best_onnx_threshold_id(최선 ONNX 임계값 ID): `density_3_0`
- best_onnx_validation_net(최선 ONNX 검증 순수익): `287.83`
- best_onnx_oos_net(최선 ONNX 표본외 순수익): `78.86`
- best_onnx_validation_density(최선 ONNX 검증 밀도): `3.0`
- best_onnx_oos_density(최선 ONNX 표본외 밀도): `3.0763358779`
- onnx_smoke_pass_rows(ONNX 스모크 통과 행): `3/4`

## Top Thresholds(상위 임계값)

|model_id|threshold_id|validation_cost_0_30_net|oos_cost_0_30_net|validation_trade_density|oos_trade_density|validation_profit_factor|oos_profit_factor|cross_split_status|
|---|---|---|---|---|---|---|---|---|
|histgb_l2_leaf7|density_3_0|294.68|137.1|3.0|3.1908396947|1.2070894473|1.1192879268|passes_cost_density_gate|
|rf_depth3_balanced|density_3_0|287.83|78.86|3.0|3.0763358779|1.2134778126|1.0721764598|passes_cost_density_gate|
|gb_depth2_lr004|density_3_0|265.97|129.66|3.0|3.1221374046|1.187712612|1.1130102063|passes_cost_density_gate|
|rf_depth3_balanced|density_3_1|220.2|29.27|3.1038251366|3.1526717557|1.1538536783|1.0252453813|passes_cost_density_gate|
|histgb_l2_leaf7|density_3_1|211.16|133.51|3.1038251366|3.3282442748|1.1394163476|1.1103817185|passes_cost_density_gate|
|gb_depth2_lr004|density_3_1|159.38|93.57|3.1038251366|3.1984732824|1.104131821|1.0782593423|passes_cost_density_gate|
|logreg_l2_balanced|density_3_0|129.1|92.78|3.0|3.1603053435|1.0891180694|1.077819902|passes_cost_density_gate|
|logreg_l2_balanced|density_3_3|93.59|72.21|3.3005464481|3.427480916|1.057721366|1.055623599|passes_cost_density_gate|

## ONNX Smoke(ONNX 스모크)

|model_id|status|sample_rows|max_abs_diff|failure|
|---|---|---|---|---|
|logreg_l2_balanced|passed|32|4.054e-08||
|rf_depth3_balanced|passed|32|2.07524e-07||
|gb_depth2_lr004|passed|32|6.6375e-08||
|histgb_l2_leaf7|failed|0||ValueError: Unable to create node 'TreeEnsembleClassifier' with name='TreeEnsembleClassifier' and attributes={'base_values': array([-0.32686704], dtype=float32),
 'class_ids': [0,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
               0,
        |

## Runtime Probe Queue(런타임 탐침 대기열)

|queue_id|priority|model_id|threshold_id|threshold|action|guardrail|
|---|---|---|---|---|---|---|
|s364F_r01_onnx_runtime_handoff_package|1|rf_depth3_balanced|density_3_0|0.435066855164|package ONNX cost-filter model for MT5 runtime probe(ONNX 비용 필터 모델을 MT5 런타임 탐침용으로 포장)|runtime_probe only, no runtime authority(런타임 탐침일 뿐 런타임 권위 아님)|
|s364F_r02_threshold_handoff_and_feature_order_check|2|rf_depth3_balanced|density_3_0|0.435066855164|freeze feature order and threshold handoff(피처 순서와 임계값 인계를 고정)|fail-fast if feature schema or hash mismatches(피처 스키마나 해시 불일치 시 즉시 실패)|
|s364F_r03_month_pressure_runtime_guard|3|rf_depth3_balanced|density_3_0|0.435066855164|carry month pressure diagnostics into runtime probe(月 압박 진단을 런타임 탐침에 포함)|no promotion if month pressure remains unstable(月 압박이 불안정하면 승격 없음)|

## Claim Boundary(주장 경계)

Action(행동): `run364F_prepare_timestamp_context_onnx_runtime_probe_without_db_v1`를 열었다.

Effect(효과): 다음 작업은 ONNX artifact(ONNX 산출물), feature order(피처 순서), threshold(임계값)를 MT5 probe(MT5 탐침) 인계로 준비한다. 아직 MT5 실행, runtime authority(런타임 권위), operating promotion(운영 승격)은 아니다.

Claim Boundary(주장 경계): `research_development_model_training_and_onnx_export_only_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
