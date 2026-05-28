# Stage337 run337EA Guarded Training Review(337EA 방어 학습 검토)

## Conclusion(결론)

run337EA(337EA 실행)는 DZ 후보 54개를 검토했다. ONNX parity(ONNX 동등성)는 `54/54`이고 negative controls(부정 대조)는 차단 0행이다.

하지만 best_validation_pf(최고 검증 PF)는 `1.04449224776`로 1.05 하한보다 낮고, 해당 validation_trade_count(검증 거래 수)는 `482`로 500 미만이다. validation density pressure(검증 밀도 압력)도 `18`행이다.

Effect(효과): DZ ONNX는 research artifact(연구 산출물)로 보존하지만 candidate selection(후보 선택), MT5 probe(MT5 탐침), Forward/Goal(전진/목표)은 계속 금지한다. 다음은 validation-density/trade-count repair design(검증-밀도/거래수 수리 설계)이다.

## Result(결과)

- status(상태): `completed_stage337EA_guarded_transfer_density_control_training_review_validation_floor_density_blocks_release_no_selection_no_mt5`
- judgment(판정): `onnx_and_controls_clear_but_validation_pf_trade_count_and_density_block_release`
- decision(결정): `stage337EA_open_run337EB_design_validation_density_trade_count_repair`
- next_action(다음 행동): `run337EB_design_validation_density_trade_count_repair_without_db_v1`
- best_validation_model(최고 검증 모델): `dz012__costed_action_label__spread_plus_extra0_points__state_carry_ge70_pruned_cost_context__extratrees_depth6_leaf120__balanced_transfer_density_control`
- best_validation_pf(최고 검증 PF): `1.04449224776`
- best_validation_trade_count(최고 검증 거래 수): `482`
- best_oos_pf(최고 OOS PF): `3.59141091331`
- best_oos_trade_count(최고 OOS 거래 수): `38`
- control_block_rows(대조 차단 행): `0`
- density_validation_pressure_rows(검증 밀도 압력 행): `18`
- release_candidate_rows(해제 후보 행): `0`
- gates_passed(게이트 통과): `9/9`

Claim boundary(주장 경계): `research_development_only_stage337EA_guarded_transfer_density_control_training_review_without_db_no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
