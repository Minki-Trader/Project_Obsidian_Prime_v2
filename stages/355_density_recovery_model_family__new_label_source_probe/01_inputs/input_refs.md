# Stage355 Input Refs(355단계 입력 참조)

- source_final_decision(원천 최종 결정): `stages/354_proxy_trade_shape_scout__small_candidate_queue/02_runs/run354C/final_decision.json`
- source_sweep(원천 스윕): `stages/354_proxy_trade_shape_scout__small_candidate_queue/02_runs/run354C/expanded_outcome_horizon_sweep.csv`
- source_queue(원천 대기열): `stages/354_proxy_trade_shape_scout__small_candidate_queue/02_runs/run354C/density_valid_queue.csv`
- source_failure_memory(원천 실패 기억): `stages/354_proxy_trade_shape_scout__small_candidate_queue/02_runs/run354C/failure_memory.csv`
- runtime_features(런타임 피처): `stages/351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract/02_runs/run351B/features/runtime_features.csv`
- raw_us100_bars(원시 US100 봉): `data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv`
- design_matrix(설계 행렬): `stages/355_density_recovery_model_family__new_label_source_probe/02_runs/run355A/density_recovery_design_matrix.csv`
- materialization_queue(물질화 대기열): `stages/355_density_recovery_model_family__new_label_source_probe/02_runs/run355A/run355B_materialization_queue.csv`

Action(행동): Stage354C(354C 실행)의 failure memory(실패 기억)를 Stage355A(355A 실행)의 design constraint(설계 제약)로 고정한다.

Effect(효과): 다음 실행이 기존 surface(표면)의 미세 임계값 검색을 반복하지 않는다.
