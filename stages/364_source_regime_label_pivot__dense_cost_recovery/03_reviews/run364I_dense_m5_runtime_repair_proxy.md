# run364I Dense M5 Runtime Repair Proxy(364I 고밀도 M5 런타임 수리 프록시)

## Summary(요약)

- run_id(실행 ID): `run364I_design_dense_m5_runtime_repair_proxy_without_db_v1`
- parent_run_id(부모 실행 ID): `run364H_review_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`
- status(상태): `completed_stage364I_dense_m5_repair_proxy_scouted_direct_dense_onnx_scout_opened_no_authority`
- judgment(판정): `mixed_proxy_prefilter_dense_source_recovers_feature_density_but_stage364_cost_filter_edge_weak_direct_dense_model_scout_required_no_authority`
- gates(게이트): `10/10`
- dense_rows(고밀도 행): `17428`
- sparse_expected_rows(희소 예상 행): `1114`
- dense_to_sparse_row_multiplier(고밀도/희소 배율): `15.644524237`
- strict_cross_split_success_count(엄격 교차 분할 성공 수): `0`
- soft_cross_split_density_positive_count(느슨한 밀도+양수 수): `12`
- best_variant_id(최선 변형 ID): `all_m5_keep_probability_extreme_control__run364E_fixed_density_3_0__close_on_flat_m5_max24`
- best_validation_net(최선 검증 순수익): `74.882`
- best_oos_net(최선 표본외 순수익): `73.383`
- best_validation_density(최선 검증 밀도): `4.1256830601`
- best_oos_density(최선 표본외 밀도): `4.4809160305`
- next_run_id(다음 실행 ID): `run364J_train_direct_dense_m5_return_onnx_scout_without_db_v1`

## Judgment(판정)

Action(행동): run359B q05 dense runtime cycle(q05 고밀도 런타임 사이클)에 run364E ONNX cost filter(ONNX 비용 필터)를 다시 얹고, close_on_flat/calendar max-hold(Flat 청산/캘린더 최대 보유) proxy(프록시)를 넓게 시험했다.
Effect(효과): run364G의 sparse tape(희소 테이프) 문제는 고칠 수 있지만, 현재 cost filter(비용 필터)는 OOS profit factor(표본외 수익 팩터)가 약해서 운영 주장으로 갈 수 없다.

## Top Proxy Variants(상위 프록시 변형)

|variant_id|validation_density|oos_density|validation_net|oos_net|validation_pf|oos_pf|strict_cross_split_success|soft_cross_split_density_positive|
|---|---|---|---|---|---|---|---|---|
|all_m5_keep_probability_extreme_control__run364E_fixed_density_3_0__close_on_flat_m5_max24|4.1256830601|4.4809160305|74.882|73.383|1.0240431944|1.0317882568|False|True|
|all_m5_keep_probability_extreme_control__run364E_fixed_density_3_0__same_day_flat_m5_max24|4.6612021858|4.9465648855|45.482|55.083|1.0132679572|1.0221996441|False|True|
|q05_long_no_hour18_dense_flat_fill__run364E_fixed_density_3_0__close_on_flat_m5_max24|3.131147541|3.4045801527|93.973|44.71|1.0820458331|1.0453650256|False|True|
|q05_long_no_hour18_dense_flat_fill__run364E_fixed_density_3_0__same_day_flat_m5_max24|3.1475409836|3.4198473282|93.073|44.11|1.0812175167|1.0448803259|False|True|
|q05_long_no_hour18_dense_flat_fill__run364E_fixed_density_3_0__close_on_flat_m5_max12|3.2841530055|3.6335877863|85.573|35.71|1.070043398|1.0343865974|False|True|
|q05_long_no_hour18_dense_flat_fill__run364E_fixed_density_3_0__close_on_flat_m5_max6|3.8415300546|4.2519083969|54.973|11.41|1.0392948331|1.0099877976|False|True|
|all_m5_keep_probability_extreme_control__validation_dense_target_10_0__close_on_flat_m5_max24|3.3715846995|3.3816793893|111.217|11.058|1.1175168429|1.0137831147|False|True|
|all_m5_keep_probability_extreme_control__validation_dense_target_10_0__same_day_flat_m5_max24|3.3825136612|3.4045801527|110.617|10.158|1.1168828562|1.0125805637|False|True|

## Evidence(근거)

- dense feature matrix(고밀도 피처 행렬): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364I/dense_m5_source_feature_matrix.csv`
- dense coverage(고밀도 커버리지): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364I/dense_source_coverage.csv`
- variant scorecard(변형 점수표): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364I/dense_proxy_variant_scorecard.csv`
- findings(발견): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364I/dense_runtime_repair_findings.csv`
- next queue(다음 대기열): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364I/run364J_offensive_next_queue.csv`

## Boundary(경계)

proxy(프록시)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. 이번 실행은 model training(모델 학습), MT5 execution(MT5 실행), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.

claim_boundary(주장 경계): `research_development_dense_m5_proxy_prefilter_only_no_new_model_training_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
