# 2026-06-02 Stage364L Density Lift Trade Shape ONNX Scout Decision(364L 밀도 상향 거래 형태 온엑스 탐색 결정)

- decision(결정): `stage364L_open_run364M_prepare_density_lift_trade_shape_onnx_runtime_probe_without_db_v1`
- run_id(실행 ID): `run364L_train_density_lift_trade_shape_onnx_scout_without_db_v1`
- parent_run_id(부모 실행 ID): `run364K_review_direct_dense_m5_onnx_scout_without_db_v1`
- next_run_id(다음 실행 ID): `run364M_prepare_density_lift_trade_shape_onnx_runtime_probe_without_db_v1`
- judgment(판정): `positive_proxy_candidate_density_lift_trade_shape_onnx_smoke_passed_runtime_probe_required_no_authority`
- gates(게이트): `5/5`

Action(행동): dynamic exit trade shape(동적 청산 거래 형태)로 density lift(밀도 상향)를 학습/검증했다.

Effect(효과): proxy(프록시) 기준 strict candidate(엄격 후보)가 `5`개 생겼고, 다음 실행에서 MT5 runtime probe(MT5 런타임 탐침) 포장 또는 검토로 넘어간다.

Evidence(근거): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364L/dynamic_trade_shape_surface.csv`, `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364L/onnx_smoke_report.csv`, `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364L/selected_model_summary.json`.

Claim Boundary(주장 경계): `research_development_density_lift_trade_shape_model_training_and_proxy_scout_only_no_mt5_execution_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
