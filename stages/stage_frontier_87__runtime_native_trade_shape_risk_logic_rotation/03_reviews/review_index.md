# F87 Review Index(F87 검토 색인)

- `stages/stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation/03_reviews/f87b_execution_summary.json`: F87B execution summary(F87B 실행 요약)
- `stages/stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation/03_reviews/f87b_feature_leakage_audit.json`: feature leakage audit(피처 누수 감사)
- `stages/stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation/03_reviews/f87b_split_boundary_audit.json`: split boundary audit(분할 경계 감사)
- `stages/stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation/03_reviews/f87b_model_validation_audit.json`: model validation audit(모델 검증 감사)
- `stages/stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation/03_reviews/f87b_result_judgment_audit.json`: result judgment receipt(결과 판정 영수증)
- `stages/stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation/03_reviews/f87b_final_claim_guard.json`: final claim guard(최종 주장 보호)
<!-- frontier87C_trade_shape_risk_repair_or_rotation_decision_v1 -->

## frontier87C_trade_shape_risk_repair_or_rotation_decision_v1

- Action(행동): F87B trade-shape/risk proxy(거래 형태/위험 프록시)를 repair/rotation decision(수리/회전 결정)으로 닫았다.
- Effect(효과): `frontier87D_stage_closeout_or_f88_rotation_handoff_v1`가 현재 실행이 되며, Strategy Tester runtime economics(전략 테스터 런타임 경제성)는 주장하지 않는다.
- Evidence(근거): `stages/stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation/02_runs/frontier87C_trade_shape_risk_repair_or_rotation_decision_v1/reports/result_summary.md`.
<!-- frontier87D_stage_closeout_or_f88_rotation_handoff_v1 -->

## frontier87D_stage_closeout_or_f88_rotation_handoff_v1

- Action(행동): F87 stage closeout(단계 마감) and F88 rotation handoff(F88 회전 인계).
- Effect(효과): `frontier88A_stage_open_runtime_substrate_first_materialization_probe_v1` becomes the next current run(다음 현재 실행) without claiming runtime authority(런타임 권위).
- Evidence(근거): `stages/stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation/02_runs/frontier87D_stage_closeout_or_f88_rotation_handoff_v1/reports/result_summary.md`.
