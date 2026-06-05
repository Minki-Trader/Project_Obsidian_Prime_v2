# Stage337 run337FG Runtime Positive Clue ONNX Training(337단계 337FG 런타임 긍정 단서 ONNX 학습)

## Conclusion(결론)

Action(행동): FF reviewed train-only inputs(FF 검토 학습 전용 입력)로 ExtraTreesClassifier(엑스트라트리스 분류기) 후보 `4`개를 학습하고 ONNX(온엑스)로 내보냈다. Effect(효과): 다음 FH review(FH 검토)가 실제 모델 산출물, ONNX parity(ONNX 동등성), proxy score(프록시 점수)를 검토할 수 있다.

- status(상태): `completed_stage337FG_runtime_positive_clue_repair_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5`
- judgment(판정): `guarded_runtime_positive_clue_repair_candidates_trained_with_onnx_parity_review_required_no_selection`
- decision(결정): `stage337FG_open_run337FH_review_runtime_positive_clue_training_without_db`
- trained_models(학습 모델): `4`
- onnx_parity(ONNX 동등성): `4/4`
- best_inner_holdout_balanced_accuracy(최고 내부 보류 균형 정확도): `0.40414377669308815`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `0.01986028614874158`
- gates(게이트): `12/12`

Boundary(경계): FG(337FG 실행)는 training and ONNX materialization(학습 및 ONNX 물질화)만 한다. MT5 execution(MT5 실행), candidate selection(후보 선택), Forward/Goal(전진/목표), runtime authority(런타임 권위)는 모두 `not_claimed`다.

Next action(다음 행동): `run337FH_review_side_cost_curve_runtime_positive_clue_training_without_db_v1`
