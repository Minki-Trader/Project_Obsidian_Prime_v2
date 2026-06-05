# Stage337 run337GZ Repair Design(337단계 337GZ 수리 설계)

## Conclusion(결론)

Action(행동): GY MT5 runtime probe(GY 메타트레이더5 런타임 탐침)의 negative KPI(음수 핵심 성과 지표)와 near parity(근접 동등성)를 repair design(수리 설계)로 바꿨다. Effect(효과): HA materialization(HA 물질화)은 학습 전용 입력만 만들고, training(학습), MT5 execution(MT5 실행), selection(선택)은 하지 않는다.

Action(행동): 모든 training task(학습 작업)의 target_column(목표 열)을 `label_class`로 고정했다. Effect(효과): sample weight(표본 가중치)를 target(목표)으로 쓰는 이전 버그를 막는다.

- status(상태): `completed_stage337GZ_probability_mismatch_and_net_recovery_repair_design_no_training_no_selection`
- judgment(판정): `mt5_negative_near_parity_converted_to_train_only_net_recovery_and_parity_repair_design`
- decision(결정): `stage337GZ_open_run337HA_probability_mismatch_and_net_recovery_repair_inputs`
- best_net_profit(최고 순수익): `-107.52`
- best_profit_factor(최고 수익 팩터): `0.95`
- best_recovery_factor(최고 회복 계수): `-0.28`
- best_drawdown(최고 낙폭): `389.65`
- probability_mismatch(확률 불일치): `3`
- max_abs_probability_diff(최대 절대 확률 차이): `0.00401173884077588`
- task_target_label_class(작업 목표 label_class): `5/5`
- release_gates(릴리스 게이트): `6`
- gates(게이트): `13/13`

## Boundary(경계)

- training(학습): `not_run`
- MT5 execution(MT5 실행): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `run337HA_materialize_mt5_negative_repair_lightgbm_probability_mismatch_and_net_recovery_inputs_without_db_v1`
- claim_boundary(주장 경계): `research_development_only_stage337GZ_probability_mismatch_and_net_recovery_repair_design_without_db_no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
