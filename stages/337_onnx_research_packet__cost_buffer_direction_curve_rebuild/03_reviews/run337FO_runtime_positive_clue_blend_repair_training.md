# Stage337 run337FO Runtime Positive Clue Blend ONNX Training(337단계 337FO 런타임 긍정 단서 혼합 ONNX 학습)

## Conclusion(결론)

Action(행동): FN reviewed train-only inputs(FN 검토 학습 전용 입력)로 ExtraTreesClassifier(엑스트라트리스 분류기) 후보 `5`개를 학습하고 ONNX(온엑스)로 내보냈다. Effect(효과): 다음 FP review(FP 검토)가 실제 모델 산출물, ONNX parity(ONNX 동등성), proxy score(프록시 점수)를 검토할 수 있다.

- status(상태): `completed_stage337FO_runtime_positive_clue_blend_repair_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5`
- judgment(판정): `guarded_runtime_positive_clue_blend_repair_candidates_trained_with_onnx_parity_review_required_no_selection`
- decision(결정): `stage337FO_open_run337FP_review_runtime_positive_clue_blend_training_without_db`
- trained_models(학습 모델): `5`
- onnx_parity(ONNX 동등성): `5/5`
- best_inner_holdout_balanced_accuracy(최고 내부 보류 균형 정확도): `0.40333393213675306`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `0.8459644678291625`
- gates(게이트): `12/12`

Boundary(경계): FO(337FO 실행)는 training and ONNX materialization(학습과 ONNX 물질화)만 했다. MT5 execution(MT5 실행), candidate selection(후보 선택), Forward/Goal(전진/목표), runtime authority(런타임 권위)는 모두 `not_claimed`다.

Next action(다음 행동): `run337FP_review_runtime_positive_clue_blend_pf_recovery_drawdown_training_without_db_v1`
