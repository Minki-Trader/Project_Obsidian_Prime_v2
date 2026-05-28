# Stage337 run337DY Transfer Density Control Objective Input Review(전이/밀도/대조/목표 입력 검토)

## Conclusion(결론)

run337DY(337DY 실행)는 DX 입력을 검토했고, 제한된 guarded training(방어 학습)을 열 수 있다고 본다.

허용되는 것은 low_margin_trade_tag(저여백 거래 태그)와 direction_residual_tag(방향 잔차 태그)의 보조 목표 사용이다. underwater_tag(침수 이진 태그)는 `0.9797717092905649` 비율로 너무 넓어서 binary target(이진 목표)으로 금지하고, drawdown_pressure_value(드로다운 압력값) 연속 진단으로만 허용한다.

이 작업은 review-only(검토 전용)이다. 새 학습, 후보 선택, 임계값 튜닝, MT5 probe(MT5 탐침), Forward/Goal(전진/목표) 주장은 하지 않는다.

Effect(효과): run337DZ(337DZ 실행)는 적격 보조 목표만 사용하고 density/control/WFO/firewall(밀도/대조/WFO/방화벽) 가드를 유지한 guarded training(방어 학습)을 실행한다.

## Result(결과)

- status(상태): `completed_stage337DY_repair_inputs_review_guarded_training_eligible_with_drawdown_tag_limit_no_selection_no_mt5`
- judgment(판정): `inputs_train_only_and_wfo_feasible_but_drawdown_binary_tag_broad_controls_required`
- decision(결정): `stage337DY_open_run337DZ_train_guarded_transfer_density_control_repair_candidates`
- next_action(다음 행동): `run337DZ_train_guarded_transfer_density_control_repair_candidates_without_db_v1`
- objective_rows(목표 행): `525996`
- low_margin_rows(저여백 행): `73564`
- direction_residual_rows(방향 잔차 행): `141547`
- underwater_ratio(침수 비율): `0.9797717092905649`
- control_block_rows(대조 차단 행): `3`
- wfo_feasible_rows(WFO 가능 행): `4/4`
- eligibility_rows(적격성 행): `6`
- gates_passed(게이트 통과): `12/12`

Claim boundary(주장 경계): `research_development_only_stage337DY_transfer_density_control_objective_input_review_without_db_no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
