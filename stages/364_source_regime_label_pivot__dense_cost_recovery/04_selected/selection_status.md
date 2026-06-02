# Stage364 Selection Status(364단계 선택 상태)

- selection_status(선택 상태): `density_lift_trade_shape_proxy_candidate_opened_no_operating_claim(밀도 상향 거래 형태 프록시 후보 열림, 운영 주장 없음)`
- active_stage_id(활성 단계 ID): `364_source_regime_label_pivot__dense_cost_recovery`
- current_run_id(현재 실행 ID): `run364M_prepare_density_lift_trade_shape_onnx_runtime_probe_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `run364L_train_density_lift_trade_shape_onnx_scout_without_db_v1`
- selected_model_id(선택 모델 ID): `h12_move5__rf5_l80_n64`
- selected_policy_id(선택 정책 ID): `long_only_margin`
- selected_exit_mode(선택 청산 방식): `flat_or_opp`
- selected_max_hold_m5(선택 최대 보유 5분봉 수): `8`
- strict_cross_split_success_count(엄격 교차 분할 성공 수): `5`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

## run364L Closeout(364L 종료 기록)

- status(상태): `completed_stage364L_density_lift_trade_shape_onnx_scout_trained_proxy_positive_no_runtime_authority`
- judgment(판정): `positive_proxy_candidate_density_lift_trade_shape_onnx_smoke_passed_runtime_probe_required_no_authority`
- gate_result(게이트 결과): `5/5`
- best_validation_net(최선 검증 순수익): `138.05`
- best_oos_net(최선 표본외 순수익): `154.056`
- best_validation_trade_density(최선 검증 거래 밀도): `3.6830601093`
- best_oos_trade_density(최선 표본외 거래 밀도): `4.0229007634`
- next_run_id(다음 실행 ID): `run364M_prepare_density_lift_trade_shape_onnx_runtime_probe_without_db_v1`
- claim_boundary(주장 경계): `research_development_density_lift_trade_shape_model_training_and_proxy_scout_only_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Action(행동): dynamic exit(동적 청산)으로 trade density(거래 밀도)를 회복했다.

Effect(효과): 후보는 proxy(프록시) 기준이며 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다.
