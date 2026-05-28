# Decision(결정): Stage337 run337ED

- date(날짜): `2026-05-28`
- run_id(실행 ID): `run337ED_review_validation_density_trade_count_repair_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run337EC_materialize_validation_density_trade_count_repair_inputs_without_db_v1`
- decision(결정): `stage337ED_open_run337EE_train_validation_density_trade_count_repair_candidates`
- judgment(판정): `train_only_repair_inputs_safe_for_guarded_training_with_feature_exclusion_and_onnx_filter`
- effect(효과): EC 입력을 검토했고, 적격 ExtraTrees 작업만 다음 방어 학습 실험으로 넘긴다.
- evidence(근거): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/03_reviews/run337ED_repair_input_review.md`, `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337ED/required_gate_coverage_audit.csv`, `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337ED/training_eligibility_matrix.csv`, `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337ED/training_feature_exclusion.csv`
- next_action(다음 행동): `run337EE_train_validation_density_trade_count_repair_candidates_without_db_v1`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_stage337ED_validation_density_trade_count_repair_input_review_without_db_no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
