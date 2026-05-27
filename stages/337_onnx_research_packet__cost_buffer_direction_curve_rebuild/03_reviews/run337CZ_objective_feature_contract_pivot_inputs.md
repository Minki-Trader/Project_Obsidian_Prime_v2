# Stage337 run337CZ Objective/Feature Inputs(목표/피처 입력)

## Conclusion(결론)

run337CZ(337CZ 실행)는 run337CY(337CY 실행)의 objective/feature contract pivot(목표/피처 계약 전환)을 실제 input artifacts(입력 산출물)로 물질화했다.

Effect(효과): 다음 run337DA(337DA 실행)는 cost tradeability gate(비용 거래가능성 게이트), payoff ranker(보상 순위기), control residual review(대조 잔차 검토)를 같은 입력에서 학습할 수 있다. 이번 실행은 training(학습), candidate selection(후보 선택), MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 판정이 아니다.

## Materialized Artifacts(물질화 산출물)

- source_rows(원천 행): `46650`
- source_timestamp_max(원천 마지막 시각): `2026-04-13T22:00:00+00:00`
- cost_label_rows(비용 라벨 행): `93300`
- payoff_rank_rows(보상 순위 행): `93300`
- control_residual_rows(대조 잔차 행): `139950`
- feature_set_rows(피처 묶음 행): `3`
- queue_rows(대기열 행): `5`
- gates_passed(게이트 통과): `12/12`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 조정): `not_run`
- candidate_selection(후보 선택): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Cost proxy note(비용 프록시 메모): 비용 포인트는 원천 입력에 close price(종가)가 없어서 train_median_hl_range_over_atr14(학습 중앙값 고저범위/ATR14) 방식의 proxy(프록시)로 return unit(수익률 단위)에 매핑했다. Effect(효과): DA 학습 전 단계에서 비용 취약 라벨을 만들 수 있지만, 운영 비용 판정으로 과장하지 않는다.

Claim boundary(주장 경계): `research_development_only_stage337CZ_objective_feature_contract_pivot_inputs_without_db_train_only_thresholds_no_model_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
