# Stage337 run337EY Side/Cost/Curve ONNX Training(337단계 337EY 방향/비용/곡선 ONNX 학습)

## Conclusion(결론)

run337EY(337EY 실행)는 EX에서 검토된 train-only inputs(학습 전용 입력)로 ExtraTreesClassifier(엑스트라트리 분류기) 후보 `4`개를 학습하고 ONNX(온엑스)로 내보냈다.

Action(행동): allowed feature schema(허용 피처 스키마) `58`개만 사용해 모델을 학습했다. Effect(효과): label/weight/forward evidence(라벨/가중치/전진 근거)가 피처에 섞이지 않은 ONNX 후보가 생겼다.

Action(행동): onnxruntime probability parity(ONNX 런타임 확률 동등성)를 `4/4`로 확인했다. Effect(효과): Python model(파이썬 모델)과 ONNX artifact(ONNX 산출물)의 확률 출력이 같은 의미인지 좁게 검증했다.

- status(상태): `completed_stage337EY_side_cost_curve_repair_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5`
- judgment(판정): `guarded_side_cost_curve_candidates_trained_with_onnx_parity_review_required_no_selection`
- decision(결정): `stage337EY_open_run337EZ_review_broker_confirmed_side_cost_curve_training_without_db`
- next_action(다음 행동): `run337EZ_review_broker_confirmed_side_cost_curve_training_without_db_v1`
- trained_models(학습 모델): `4`
- onnx_exports(ONNX 내보내기): `4`
- best_inner_holdout_balanced_accuracy(최고 내부 보류 균형 정확도): `0.4069289083471486`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순값): `0.15923354712458604`
- gates(게이트): `12/12`

## Boundary(경계)

- candidate selection(후보 선택): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_stage337EY_broker_confirmed_side_cost_curve_training_without_db_reviewed_train_only_inputs_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
