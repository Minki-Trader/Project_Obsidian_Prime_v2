# Stage337 run337DZ Guarded Transfer Density Control Training(337DZ 방어 전이/밀도/대조 학습)

## Conclusion(결론)

run337DZ(337DZ 실행)는 DY에서 허용된 train-only auxiliary tags(학습 전용 보조 태그)를 sample weight(표본 가중치)로만 사용해 guarded action candidates(방어 행동 후보)를 학습했고 ONNX parity(ONNX 동등성)를 확인했다.

이 작업은 model training(모델 학습)이다. candidate selection(후보 선택), threshold tuning(임계값 조정), lot optimization(로트 최적화), MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 주장은 하지 않는다.

Effect(효과): 다음 run337EA(337EA 실행)는 scorecard/control/density/parity(점수표/대조/밀도/동등성)를 검토해 새 학습이 진짜 진전인지 또는 또 다른 과적합인지 판단한다.

## Result(결과)

- status(상태): `completed_stage337DZ_guarded_transfer_density_control_repair_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5`
- judgment(판정): `guarded_auxiliary_weighted_candidates_trained_onnx_parity_review_required_no_selection`
- decision(결정): `stage337DZ_open_run337EA_review_guarded_transfer_density_control_training`
- next_action(다음 행동): `run337EA_review_guarded_transfer_density_control_training_without_db_v1`
- trained_models(학습 모델): `54`
- onnx_parity(ONNX 동등성): `54/54`
- best_validation_pf(최고 검증 PF): `1.0444922477600567`
- best_oos_pf(최고 OOS PF): `3.5914109133121794`
- control_block_rows(대조 차단 행): `0`
- density_pressure_rows(밀도 압력 행): `36`
- release_candidate_rows(해제 후보 행): `0`
- gates_passed(게이트 통과): `13/13`

Claim boundary(주장 경계): `research_development_only_stage337DZ_guarded_transfer_density_control_training_without_db_train_only_auxiliary_weights_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
