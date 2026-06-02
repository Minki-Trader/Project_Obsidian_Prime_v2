# run364L Density Lift Trade Shape ONNX Scout(364L 밀도 상향 거래 형태 온엑스 탐색)

## Summary(요약)

- run_id(실행 ID): `run364L_train_density_lift_trade_shape_onnx_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364K_review_direct_dense_m5_onnx_scout_without_db_v1`
- status(상태): `completed_stage364L_density_lift_trade_shape_onnx_scout_trained_proxy_positive_no_runtime_authority`
- judgment(판정): `positive_proxy_candidate_density_lift_trade_shape_onnx_smoke_passed_runtime_probe_required_no_authority`
- gates(게이트): `5/5`
- model_rows(모델 수): `6`
- surface_rows(표면 행): `480`
- strict_cross_split_success_count(엄격 교차 분할 성공 수): `5`
- onnx_smoke_pass_rows(온엑스 연기 점검 통과 수): `6/6`
- best_model_id(최선 모델 ID): `h12_move5__rf5_l80_n64`
- best_policy_id(최선 정책 ID): `long_only_margin`
- best_exit_mode(최선 청산 방식): `flat_or_opp`
- best_max_hold_m5(최선 최대 보유 5분봉 수): `8`
- best_validation_net(최선 검증 순수익): `138.05`
- best_oos_net(최선 표본외 순수익): `154.056`
- best_validation_profit_factor(최선 검증 수익 팩터): `1.075867739`
- best_oos_profit_factor(최선 표본외 수익 팩터): `1.1053236088`
- best_validation_trade_density(최선 검증 거래 밀도): `3.6830601093`
- best_oos_trade_density(최선 표본외 거래 밀도): `4.0229007634`
- next_run_id(다음 실행 ID): `run364M_prepare_density_lift_trade_shape_onnx_runtime_probe_without_db_v1`

## Judgment(판정)

Action(행동): h6/h12/h24 label(6/12/24봉 라벨) RF model(랜덤포레스트 모델)에 flat_or_opp/weak_or_opp dynamic exit(Flat/반대, 약화/반대 동적 청산)을 얹어 density lift(밀도 상향)를 시험했다.

Effect(효과): run364J(364J 실행)의 저빈도 수익 단서를 3/day+(일 3회 이상) trade shape(거래 형태)로 끌어올릴 수 있는 proxy candidate(프록시 후보)를 만들었다. MT5 runtime probe(MT5 런타임 탐침) 전에는 운영 주장(operating claim, 운영 주장)을 하지 않는다.

## Top Surface Rows(상위 표면 행)

|model_id|policy_id|threshold_id|exit_mode|max_hold_m5|validation_net|oos_net|validation_profit_factor|oos_profit_factor|validation_trade_density|oos_trade_density|strict_cross_split_success|
|---|---|---|---|---|---|---|---|---|---|---|---|
|h12_move5__rf5_l80_n64|long_only_margin|long_only_margin__density_16_0__maxhold_8__flat_or_opp|flat_or_opp|8|138.05|154.056|1.075867739|1.1053236088|3.6830601093|4.0229007634|True|
|h24_move8__rf5_l80_n64|long_only_margin|long_only_margin__density_20_0__maxhold_12__flat_or_opp|flat_or_opp|12|136.239|120.752|1.0785480949|1.0857957916|3.4426229508|3.6335877863|True|
|h6_move3__rf4_l120_n64|long_only_margin|long_only_margin__density_8_0__maxhold_8__weak_or_opp|weak_or_opp|8|117.723|72.806|1.1179476904|1.0872106743|3.4426229508|3.8244274809|True|
|h6_move3__rf4_l120_n64|long_only_margin|long_only_margin__density_8_0__maxhold_12__weak_or_opp|weak_or_opp|12|119.979|56.695|1.1230730566|1.0698236643|3.3551912568|3.6641221374|True|
|h6_move3__rf4_l120_n64|long_only_margin|long_only_margin__density_8_0__maxhold_4__weak_or_opp|weak_or_opp|4|76.428|55.367|1.0698646366|1.0620073692|3.7595628415|4.2824427481|True|
|h24_move8__rf5_l80_n64|two_sided_argmax_margin|two_sided_argmax_margin__density_8_0__maxhold_8__weak_or_opp|weak_or_opp|8|-75.271|419.391|0.9446725529|1.4911286951|1.6721311475|1.9541984733|False|
|h24_move8__rf5_l80_n64|two_sided_argmax_margin|two_sided_argmax_margin__density_8_0__maxhold_8__flat_or_opp|flat_or_opp|8|-80.721|412.98|0.9409227702|1.4804567934|1.6721311475|1.9541984733|False|
|h24_move8__rf5_l80_n64|two_sided_argmax_margin|two_sided_argmax_margin__density_8_0__maxhold_6__flat_or_opp|flat_or_opp|6|-41.555|378.558|0.9709697115|1.4512003547|1.912568306|2.1832061069|False|
|h24_move8__rf5_l80_n64|two_sided_argmax_margin|two_sided_argmax_margin__density_8_0__maxhold_6__weak_or_opp|weak_or_opp|6|-50.005|381.02|0.9652014703|1.4560028244|1.912568306|2.1832061069|False|
|h24_move8__rf5_l80_n64|two_sided_argmax_margin|two_sided_argmax_margin__density_16_0__maxhold_8__weak_or_opp|weak_or_opp|8|84.169|324.17|1.0379540551|1.2126629479|3.174863388|3.6641221374|False|
|h12_move5__rf5_l80_n64|long_only_margin|long_only_margin__density_16_0__maxhold_12__flat_or_opp|flat_or_opp|12|81.52|304.743|1.0443696967|1.2489148777|3.131147541|3.320610687|False|
|h12_move5__rf5_l80_n64|long_only_margin|long_only_margin__density_12_0__maxhold_12__flat_or_opp|flat_or_opp|12|-99.397|365.442|0.9398155661|1.3622828932|2.4207650273|2.7480916031|False|

## ONNX Smoke(온엑스 연기 점검)

|model_id|status|sample_rows|max_abs_diff|failure|
|---|---|---|---|---|
|h6_move3__rf4_l120_n64|passed|64|9.8914e-08||
|h6_move3__rf5_l80_n64|passed|64|1.27873e-07||
|h12_move5__rf4_l120_n64|passed|64|1.77108e-07||
|h12_move5__rf5_l80_n64|passed|64|9.8315e-08||
|h24_move8__rf4_l120_n64|passed|64|1.17581e-07||
|h24_move8__rf5_l80_n64|passed|64|1.26719e-07||

## Next Queue(다음 대기열)

|queue_id|priority|next_run_id|model_id|threshold_id|action|guardrail|
|---|---|---|---|---|---|---|
|run364M_Q01_package_density_lift_trade_shape_runtime_probe|1|run364M_prepare_density_lift_trade_shape_onnx_runtime_probe_without_db_v1|h12_move5__rf5_l80_n64|long_only_margin__density_16_0__maxhold_8__flat_or_opp|package ONNX model(온엑스 모델) and dynamic exit policy(동적 청산 정책) for MT5 runtime probe(MT5 런타임 탐침)|proxy does not replace MT5 KPI(프록시는 MT5 핵심 성과 지표를 대체하지 않는다)|

## Evidence(근거)

- trade_shape_surface(거래 형태 표면): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364L/dynamic_trade_shape_surface.csv`
- cost_stress_surface(비용 압박 표면): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364L/cost_stress_surface.csv`
- onnx_smoke_report(온엑스 연기 보고서): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364L/onnx_smoke_report.csv`
- selected_model_summary(선택 모델 요약): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364L/selected_model_summary.json`
- gate_audit(게이트 감사): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364L/required_gate_coverage_audit.csv`

## Boundary(경계)

proxy(프록시)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. 이번 실행은 MT5 execution(MT5 실행), forward pass(전진 검증), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 주장하지 않는다.

claim_boundary(주장 경계): `research_development_density_lift_trade_shape_model_training_and_proxy_scout_only_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
