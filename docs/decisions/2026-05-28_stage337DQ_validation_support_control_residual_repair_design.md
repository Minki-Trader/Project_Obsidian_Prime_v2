# Decision(결정): Stage337 run337DQ

- date(날짜): `2026-05-28`
- run_id(실행 ID): `run337DQ_design_validation_support_and_control_residual_repair_without_db_v1`
- parent_run_id(부모 실행 ID): `run337DP_review_guarded_prediction_surface_validation_edge_training_without_db_v1`
- decision(결정): `stage337DQ_open_run337DR_materialize_validation_support_control_residual_repair_inputs`
- judgment(판정): `repair_design_ready_for_row_level_tape_materialization_no_selection`
- effect(효과): validation/control(검증/대조) 차단을 DR row-level materialization(행 단위 물질화)로 넘기고 선택/MT5/Forward(전진)는 계속 닫는다.
- evidence(근거): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/03_reviews/run337DQ_validation_support_control_residual_repair_design.md`, `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337DQ/required_gate_coverage_audit.csv`, `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337DQ/validation_support_repair_design.csv`, `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337DQ/control_residual_repair_design.csv`
- next_action(다음 행동): `run337DR_materialize_validation_support_control_residual_repair_inputs_without_db_v1`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_stage337DQ_validation_support_control_residual_repair_design_without_db_no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
