# Stage337AU Balanced No-Lookahead Repair Inputs Without D/B(337AU D/B 없는 균형 미래참조 방지 수리 입력)

- run_id(실행 ID): `run337AU_materialize_balanced_no_lookahead_repair_inputs_without_db_v1`
- status(상태): `completed_stage337AU_balanced_no_lookahead_repair_inputs_materialized_no_training_no_selection`
- judgment(판정): `materialized_repair_inputs_ready_for_review_but_no_forward_or_goal_claim`
- decision(결정): `stage337AU_open_run337AV_review_balanced_repair_inputs_without_db_no_selection`
- parent_run(부모 실행): `run337AT_balanced_no_lookahead_repair_protocol_without_db_v1`
- next_action(다음 행동): `run337AV_review_balanced_no_lookahead_repair_inputs_without_db_v1`
- repair_input_rows(수리 입력 행): `344`
- protocol_inputs(프로토콜 입력): `9`
- feature_bindings(피처 연결): `58`
- negative_controls(부정 대조): `3`
- proxy_contract_rows(프록시 계약 행): `10`
- gates_passed(게이트 통과): `9/9`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## What Was Materialized(물질화한 것)

run337AU(337AU 실행)는 run337AT(337AT 실행)의 9개 protocol(프로토콜)을 실제 completed-day pre-trade feature frame(완성일 진입 전 피처 프레임)과 연결했다. prior equity fields(이전 곡선 필드)는 current trade PnL(현재 거래 손익)을 쓰지 않고, 이전 종결 거래만 사용한다. 효과(effect, 효과)는 회복/곡선 수리가 미래 정보를 먹지 못하게 하는 것이다.

## Key Files(핵심 파일)

- repair frame(수리 프레임): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AU/completed_day_pretrade_repair_feature_frame.csv`
- protocol input matrix(프로토콜 입력 행렬): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AU/protocol_materialized_input_matrix.csv`
- feature binding(피처 연결): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AU/protocol_feature_binding_matrix.csv`
- negative controls(부정 대조): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AU/negative_control_input_recipe_matrix.csv`
- proxy contract(프록시 계약): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AU/proxy_mt5_materialization_contract.csv`
- runtime queue(런타임 대기열): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AU/mt5_runtime_probe_candidate_queue.csv`
- gate audit(게이트 감사): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337AU/required_gate_coverage_audit.csv`

## Boundary(경계)

새 model training(모델 학습), threshold retuning(임계값 재조정), D/B rule rewrite(D/B 규칙 재작성), lot optimization(랏 최적화), MT5 execution(MT5 실행)은 하지 않았다. proxy expected value(프록시 예상값)는 MT5 runtime signal parity(MT5 런타임 신호 동등성) 전용이고, net/PF/DD(순익/수익 팩터/손실폭) 권위가 아니다.

claim_boundary(주장 경계): `research_development_only_stage337AU_balanced_no_lookahead_repair_inputs_without_db_no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
