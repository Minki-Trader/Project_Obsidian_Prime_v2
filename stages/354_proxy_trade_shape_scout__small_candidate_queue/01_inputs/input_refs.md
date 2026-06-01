# Stage354 Input Refs(354단계 입력 참조)

- handoff_manifest(인계 목록): `stages/354_proxy_trade_shape_scout__small_candidate_queue/02_runs/run354A/stage353_to_stage354_handoff_manifest.csv`
- stage352_final_decision(352단계 최종 결정): `stages/352_runtime_probe_report_repair__no_scaler_1d_mt5_kpi_identity/02_runs/run352B/final_decision.json`
- stage352_combined_kpi(352단계 합산 핵심 성과 지표): `stages/352_runtime_probe_report_repair__no_scaler_1d_mt5_kpi_identity/02_runs/run352B/combined_kpi_summary.json`
- expected_tape(예상 테이프): `stages/351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract/02_runs/run351B/expected/expected_tape.csv`
- runtime_features(런타임 피처): `stages/351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract/02_runs/run351B/features/runtime_features.csv`
- next_queue(다음 대기열): `stages/354_proxy_trade_shape_scout__small_candidate_queue/02_runs/run354A/run354B_proxy_scout_queue.csv`

Action(행동): Stage352B(352B 실행)의 runtime truth(런타임 진실)와 Stage351B(351B 실행)의 expected tape(예상 테이프)를 Stage354(354단계)의 작은 입력 묶음으로 고정했다.

Effect(효과): 다음 실행은 불필요한 MT5 report repair(보고서 수리)와 Stage353(353단계)의 큰 질문을 다시 읽지 않고 proxy scout(프록시 탐색)에 집중한다.
