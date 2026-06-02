# run364J Direct Dense M5 ONNX Scout(364J 직접 고밀도 5분봉 온엑스 탐색)

## Summary(요약)

- run_id(실행 ID): `run364J_train_direct_dense_m5_return_onnx_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364I_design_dense_m5_runtime_repair_proxy_without_db_v1`
- status(상태): `completed_stage364J_direct_dense_m5_onnx_scout_trained_no_runtime_authority`
- judgment(판정): `negative_direct_dense_m5_onnx_scout_no_cross_split_cost_density_candidate_no_authority`
- gates(게이트): `6/6`
- trained_model_rows(학습 모델 수): `16`
- threshold_rows(임계값 행 수): `192`
- onnx_smoke_pass_rows(온엑스 연기 점검 통과 수): `16/16`
- strict_cross_split_success_count(엄격 교차 분할 성공 수): `0`
- soft_cross_split_positive_count(느슨한 교차 양수 수): `0`
- best_model_id(최선 모델 ID): `all58__dense_h24_move8pts__rf_depth5_leaf80_n48`
- best_label_id(최선 라벨 ID): `dense_h24_move8pts`
- best_policy_id(최선 정책 ID): `two_sided_argmax_margin`
- best_validation_net(최선 검증 순수익): `152.887`
- best_oos_net(최선 표본외 순수익): `439.321`
- best_validation_profit_factor(최선 검증 수익 팩터): `1.2240201034`
- best_oos_profit_factor(최선 표본외 수익 팩터): `1.9215048779`
- best_validation_trade_density(최선 검증 거래 밀도): `0.6830601093`
- best_oos_trade_density(최선 표본외 거래 밀도): `0.8473282443`
- next_run_id(다음 실행 ID): `run364K_review_direct_dense_m5_onnx_scout_without_db_v1`

## Judgment(판정)

Action(행동): dense M5 model input(고밀도 5분봉 모델 입력)에 direct return label(직접 수익 라벨)을 붙이고 ONNX-exportable model(온엑스 변환 가능 모델)을 학습했다.

Effect(효과): sparse runtime tape(희소 런타임 테이프) 문제와 model family(모델 계열) 문제를 분리해, MT5 runtime probe(MT5 런타임 탐침)로 보낼 수 있는 후보만 남긴다.

## Top Proxy Rows(상위 프록시 행)

|model_id|label_id|policy_id|threshold_id|validation_net|oos_net|validation_profit_factor|oos_profit_factor|validation_trade_density|oos_trade_density|strict_cross_split_success|onnx_smoke_status|
|---|---|---|---|---|---|---|---|---|---|---|---|
|all58__dense_h24_move8pts__rf_depth5_leaf80_n48|dense_h24_move8pts|two_sided_argmax_margin|two_sided_argmax_margin__validation_density_5_0|152.887|439.321|1.2240201034|1.9215048779|0.6830601093|0.8473282443|False|passed|
|all58__native_fwd12_contract_label_class__rf_depth4_leaf120_n48|native_fwd12_contract_label_class|two_sided_argmax_margin|two_sided_argmax_margin__validation_density_3_0|-38.571|261.51|0.9432820282|2.1686970978|0.6229508197|0.4809160305|False|passed|
|all58__dense_h24_move8pts__rf_depth4_leaf120_n48|dense_h24_move8pts|two_sided_argmax_margin|two_sided_argmax_margin__validation_density_5_0|-35.61|302.986|0.9486216135|1.6976791311|0.5737704918|0.7022900763|False|passed|
|all58__dense_h24_move8pts__rf_depth5_leaf80_n48|dense_h24_move8pts|two_sided_argmax_margin|two_sided_argmax_margin__validation_density_3_0|105.92|237.762|1.2032810545|1.6115686749|0.4644808743|0.5648854962|False|passed|
|all58__native_fwd12_contract_label_class__rf_depth4_leaf120_n48|native_fwd12_contract_label_class|two_sided_argmax_margin|two_sided_argmax_margin__validation_density_12_0|-232.318|374.994|0.8626968667|1.3681190094|1.7650273224|1.9083969466|False|passed|
|runtime_core__dense_h12_move5pts__rf_depth4_leaf120_n48|dense_h12_move5pts|long_only_margin|long_only_margin__validation_density_3_0|68.003|199.049|1.154395421|1.7957917378|0.5027322404|0.7328244275|False|passed|
|all58__native_fwd12_contract_label_class__rf_depth5_leaf80_n48|native_fwd12_contract_label_class|two_sided_argmax_margin|two_sided_argmax_margin__validation_density_8_0|20.913|249.671|1.0176930431|1.3562174077|1.2240437158|1.1832061069|False|passed|
|all58__dense_h12_move5pts__rf_depth5_leaf80_n48|dense_h12_move5pts|two_sided_argmax_margin|two_sided_argmax_margin__validation_density_3_0|-212.678|309.252|0.792055442|1.5382489313|0.956284153|0.9389312977|False|passed|
|all58__dense_h12_move5pts__rf_depth5_leaf80_n48|dense_h12_move5pts|short_only_margin|short_only_margin__validation_density_3_0|-201.398|256.305|0.7163188698|1.8711338454|0.7322404372|0.7328244275|False|passed|
|all58__dense_h24_move8pts__rf_depth4_leaf120_n48|dense_h24_move8pts|short_only_margin|short_only_margin__validation_density_3_0|-24.596|190.137|0.9494883322|1.8514334077|0.4316939891|0.4427480916|False|passed|
|all58__dense_h24_move8pts__rf_depth4_leaf120_n48|dense_h24_move8pts|short_only_margin|short_only_margin__validation_density_5_0|5.206|206.836|1.0089343482|1.5534295691|0.5737704918|0.6183206107|False|passed|
|runtime_core__dense_h12_move5pts__rf_depth4_leaf120_n48|dense_h12_move5pts|two_sided_argmax_margin|two_sided_argmax_margin__validation_density_3_0|-96.6|239.501|0.9005265093|1.4663036198|0.8797814208|0.8549618321|False|passed|

## ONNX Smoke(온엑스 연기 점검)

|model_id|status|sample_rows|max_abs_diff|failure|
|---|---|---|---|---|
|all58__native_fwd12_contract_label_class__lr_balanced_c0_40|passed|64|7.3019e-08||
|all58__native_fwd12_contract_label_class__rf_depth4_leaf120_n48|passed|64|7.4295e-08||
|all58__native_fwd12_contract_label_class__rf_depth5_leaf80_n48|passed|64|1.14471e-07||
|all58__dense_h6_move3pts__lr_balanced_c0_40|passed|64|7.374e-08||
|all58__dense_h6_move3pts__rf_depth4_leaf120_n48|passed|64|9.4227e-08||
|all58__dense_h6_move3pts__rf_depth5_leaf80_n48|passed|64|1.08992e-07||
|all58__dense_h12_move5pts__lr_balanced_c0_40|passed|64|8.1906e-08||
|all58__dense_h12_move5pts__rf_depth4_leaf120_n48|passed|64|6.9441e-08||
|all58__dense_h12_move5pts__rf_depth5_leaf80_n48|passed|64|8.2152e-08||
|all58__dense_h24_move8pts__lr_balanced_c0_40|passed|64|6.3516e-08||
|all58__dense_h24_move8pts__rf_depth4_leaf120_n48|passed|64|7.8901e-08||
|all58__dense_h24_move8pts__rf_depth5_leaf80_n48|passed|64|9.4e-08||

## Next Queue(다음 대기열)

|queue_id|priority|next_run_id|model_id|action|guardrail|
|---|---|---|---|---|---|
|run364K_Q01_review_direct_dense_m5_scout_failure_memory|1|run364K_review_direct_dense_m5_onnx_scout_without_db_v1|all58__dense_h24_move8pts__rf_depth5_leaf80_n48|review direct dense M5 scout(직접 고밀도 5분봉 탐색) failure memory(실패 기억)|no runtime authority(런타임 권위 없음)|

## Evidence(근거)

- model_scorecard(모델 점수표): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364J/model_scorecard.csv`
- proxy_threshold_surface(프록시 임계값 표면): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364J/proxy_threshold_surface.csv`
- ONNX smoke report(온엑스 연기 보고서): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364J/onnx_smoke_report.csv`
- selected_model_summary(선택 모델 요약): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364J/selected_model_summary.json`
- gate audit(게이트 감사): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364J/required_gate_coverage_audit.csv`

## Boundary(경계)

proxy(프록시)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. 이번 실행은 MT5 execution(MT5 실행), forward pass(전진 검증), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.

claim_boundary(주장 경계): `research_development_direct_dense_m5_model_training_and_proxy_scout_only_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
