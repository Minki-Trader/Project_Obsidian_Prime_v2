# Stage330 Input References(330단계 입력 참조)

- source_closeout(원천 종료): `stages/329_onnx_rebuild__live_feature_control/03_reviews/run329H_cp322a_exact_handoff_repair_feasibility.md`
- raw_forward_gap(원본 전진 간극): `stages/329_onnx_rebuild__live_feature_control/02_runs/run329G/raw_forward_session_gap_report.csv`
- overfit_pressure(과적합 압력): `stages/329_onnx_rebuild__live_feature_control/02_runs/run329G/overfit_pressure_report.csv`
- session_parity_mt5(세션 동등 MT5): `stages/329_onnx_rebuild__live_feature_control/02_runs/run329F/forward_mt5_kpi_report.csv`
- feature_frames(피처 프레임): `stages/329_onnx_rebuild__live_feature_control/02_runs/run329B/feature_frames/`
- research_onnx(연구 온엑스): `stages/329_onnx_rebuild__live_feature_control/02_runs/run329C/onnx/`

Effect(효과): 입력은 다음 설계를 위한 evidence(근거)이며 selected candidate(선택 후보)가 아니다.

## run330A_design_outputs(330A 설계 출력)

- design_report(설계 보고서): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/03_reviews/run330A_forward_safe_non_identity_surface_robustness_design.md`
- candidate_evidence(후보 근거): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330A/candidate_evidence_input_matrix.csv`
- materialization_queue(물질화 대기열): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330A/stage330B_materialization_queue.csv`

Effect(효과): run330B(330B 실행)는 이 설계 출력만 입력으로 삼아 forward data audit(전진 데이터 감사)와 고정 규칙 replay(재생)를 시작한다.

## run330B_materialization_outputs(330B 물질화 출력)

- materialization_report(물질화 보고서): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/03_reviews/run330B_forward_safe_control_surface_materialization.md`
- fixed_threshold_summary(고정 임계값 요약): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330B/fixed_threshold_replay_summary.csv`
- signal_payload_manifest(신호 인계 목록): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330B/signal_payload_manifest.csv`
- raw_session_gap_guard(원본/세션 간극 방어): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330B/raw_session_gap_guard.csv`

Effect(효과): run330C(330C 실행)는 새 점수 계산 없이 이 고정 인계물을 소비할 수 있다.
