# Stage337 run337CK Guarded Directional Label/Action Training(방어 방향 라벨/행동 학습)

## Conclusion(결론)

run337CK(337CK 실행)는 CJ 후보 입력을 이용해 `10`개 sklearn/ONNX(사이킷런/온엑스) 후보를 학습하고 proxy expected(프록시 예상)와 negative-control scorecard(부정 대조 점수표)를 만들었다.

Effect(효과): shifted-control high alignment(이동 대조 높은 정렬)을 `review_required(검토 필요)`로 드러냈고, 다음 run337CL(337CL 실행)에서 이 위험을 먼저 검토한다. Forward/Goal/runtime authority(전진/목표/런타임 권위)는 주장하지 않는다.

## Result(결과)

- status(상태): `completed_stage337CK_guarded_directional_label_action_candidate_training_onnx_materialized_negative_control_review_required_no_selection`
- judgment(판정): `exploratory_guarded_candidate_models_trained_onnx_parity_passed_shifted_control_risk_flagged_no_forward_selection`
- decision(결정): `stage337CK_open_run337CL_guarded_training_negative_control_review`
- next_action(다음 행동): `run337CL_review_guarded_directional_label_action_candidate_training_without_db_v1`
- trained_models(학습 모델): `10`
- onnx_parity(ONNX 동등성): `10/10`
- scorecard_rows(점수표 행): `30`
- negative_control_rows(부정 대조 행): `50`
- negative_control_review_required_rows(부정 대조 검토 필요 행): `11`
- proxy_expected_rows(프록시 예상 행): `75840`
- gates_passed(게이트 통과): `9/9`

## Boundary(경계)

- candidate_selection(후보 선택): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- lot_optimization(로트 최적화): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `research_development_only_stage337CK_guarded_directional_label_action_training_without_db_negative_control_review_required_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
