# Stage337 run337EW Broker-Confirmed Side/Cost/Curve Repair Inputs(337단계 337EW 브로커 확인 방향/비용/곡선 수리 입력)

## Conclusion(결론)

run337EW(337EW 실행)는 EV design contracts(EV 설계 계약)을 실제 train-only input frame(학습 전용 입력 프레임)으로 물질화했다.

Action(행동): EC/DX train-only frames(EC/DX 학습 전용 프레임)을 결합해 side target(방향 목표), cost survival weight(비용 생존 가중치), curve state weight(곡선 상태 가중치), density floor(밀도 하한)를 만들었다. Effect(효과): 다음 run337EX(337EX 실행)가 학습 전에 feature-label boundary(피처-라벨 경계)와 overfit control(과적합 통제)을 검토할 수 있다.

Action(행동): ET/EU broker forward evidence(ET/EU 브로커 전진 근거)는 quarantine(격리) 표에만 남겼다. Effect(효과): 실제 MT5(MetaTrader 5, 메타트레이더5) 실패 기억은 보존하지만 피처(feature, 피처), 라벨(label, 라벨), 임계값(threshold, 임계값), 방향 거부(side veto, 방향 거부)에는 섞이지 않는다.

- status(상태): `completed_stage337EW_broker_confirmed_side_cost_curve_repair_inputs_materialized_no_training_no_selection`
- judgment(판정): `train_only_side_cost_curve_inputs_materialized_forward_evidence_quarantined_review_required`
- decision(결정): `stage337EW_open_run337EX_review_side_cost_curve_repair_inputs_without_db_no_training`
- next_action(다음 행동): `run337EX_review_broker_confirmed_side_cost_curve_repair_inputs_without_db_v1`
- frame_rows(프레임 행): `87666`
- frame_columns(프레임 열): `115`
- allowed_feature_rows(허용 피처 행): `58`
- target_or_weight_rows(목표/가중치 행): `46`
- side_target_rows(방향 목표 행): `87666`
- quarantine_rows(격리 행): `7`
- gates(게이트): `12/12`

## Boundary(경계)

- model training(모델 학습): `not_run`
- candidate selection(후보 선택): `not_run`
- threshold tuning(임계값 조정): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_stage337EW_broker_confirmed_side_cost_curve_repair_input_materialization_without_db_no_model_training_no_threshold_tuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
