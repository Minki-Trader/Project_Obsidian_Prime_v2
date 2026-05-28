# Stage337 run337EE Training(337EE 학습)

## Conclusion(결론)

run337EE(337EE 실행)는 ED가 허용한 eligible ExtraTrees tasks(적격 ExtraTrees 작업) `81`개를 학습하고 ONNX parity(ONNX 동등성)를 확인했다.

Action(행동): threshold tuning(임계값 조정), lot optimization(랏 최적화), candidate selection(후보 선택), MT5 probe(MT5 탐침)는 실행하지 않았다.

Effect(효과): 후보는 학습 산출물로만 남고, 다음 run337EF(337EF 실행)에서 validation PF/trade count/density/control(검증 PF/거래수/밀도/대조)을 검토한다. Forward/Goal(전진/목표)은 주장하지 않는다.

## Result(결과)

- status(상태): `completed_stage337EE_validation_density_trade_count_repair_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5`
- judgment(판정): `eligible_extratrees_candidates_trained_with_onnx_parity_review_required`
- decision(결정): `stage337EE_open_run337EF_review_validation_density_trade_count_repair_training`
- next_action(다음 행동): `run337EF_review_validation_density_trade_count_repair_training_without_db_v1`
- trained_models(학습 모델): `81`
- onnx_parity(ONNX 동등성): `81/81`
- best_validation_pf(최고 검증 PF): `1.3355649010033337`
- best_validation_trade_count(최고 검증 거래수): `414`
- best_oos_pf(최고 OOS PF): `2.0170601756691218`
- best_oos_trade_count(최고 OOS 거래수): `163`
- release_candidate_rows(해제 후보 행): `0`
- gates_passed(게이트 통과): `11/11`

Claim boundary(주장 경계): `research_development_only_stage337EE_validation_density_trade_count_repair_training_without_db_train_only_reviewed_weights_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
