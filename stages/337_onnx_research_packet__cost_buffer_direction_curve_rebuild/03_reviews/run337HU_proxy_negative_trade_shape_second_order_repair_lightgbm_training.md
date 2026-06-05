# Stage337 run337HU Proxy Negative Trade Shape Second Order Repair LightGBM ONNX Training(337단계 run337HU 프록시 음수 거래 형태 2차 수리 LightGBM ONNX 학습)

Action(행동): HS/HT reviewed train-only inputs(HS/HT 검토 학습 전용 입력)로 LGBMClassifier(LightGBM 분류기) 후보 `5`개를 학습하고 ONNX(온엑스)로 내보냈다. Effect(효과): 다음 HV review(HV 검토)가 실제 model artifacts(모델 산출물), ONNX parity(ONNX 동등성), proxy score(프록시 점수)를 검토할 수 있다.

- status(상태): `completed_stage337HU_proxy_negative_trade_shape_second_order_repair_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5`
- judgment(판정): `guarded_proxy_negative_trade_shape_second_order_repair_lightgbm_candidates_trained_with_onnx_parity_review_required_no_selection`
- decision(결정): `stage337HU_open_run337HV_review_proxy_negative_trade_shape_second_order_training`
- trained_models(학습 모델): `5`
- onnx_parity(ONNX 동등성): `5/5`
- best_inner_holdout_balanced_accuracy(최고 내부 보류 균형 정확도): `0.3840905345147439`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `-1.384783683633941`
- positive_inner_holdout_proxy_rows(양수 내부 보류 프록시 행): `0`
- gates(게이트): `12/12`

Boundary(경계): HU(337HU 실행)는 training and ONNX materialization(학습과 ONNX 물질화)만 했다. MT5 execution(MT5 실행), candidate selection(후보 선택), Forward/Goal(전진/목표), runtime authority(런타임 권위)는 모두 `not_claimed`다.

Next action(다음 행동): `run337HV_review_proxy_negative_trade_shape_second_order_repair_training_without_db_v1`
