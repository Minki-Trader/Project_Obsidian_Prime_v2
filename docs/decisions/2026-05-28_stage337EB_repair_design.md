# Decision(결정): Stage337 run337EB

- date(날짜): `2026-05-28`
- run_id(실행 ID): `run337EB_design_validation_density_trade_count_repair_without_db_v1`
- parent_run_id(부모 실행 ID): `run337EA_review_guarded_transfer_density_control_training_without_db_v1`
- decision(결정): `stage337EB_open_run337EC_materialize_validation_density_trade_count_repair_inputs`
- judgment(판정): `repair_design_ready_for_train_only_validation_density_trade_count_materialization`
- effect(효과): EA의 validation/density/trade blockers(검증/밀도/거래 차단)를 EC의 train-only repair inputs(학습 전용 수리 입력)로 넘긴다.
- evidence(근거): `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/03_reviews/run337EB_repair_design.md`, `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337EB/required_gate_coverage_audit.csv`, `stages/337_onnx_research_packet__cost_buffer_direction_curve_rebuild/02_runs/run337EB/validation_density_trade_count_repair_design.csv`
- next_action(다음 행동): `run337EC_materialize_validation_density_trade_count_repair_inputs_without_db_v1`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `research_development_only_stage337EB_validation_density_trade_count_repair_design_without_db_no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve`
