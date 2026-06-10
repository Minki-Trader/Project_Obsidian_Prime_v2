# run364DT H17 Density-Failure Regime/Behavior Reseed(밀도 실패 국면/현상 재시드)

Created(생성): 2026-06-06T10:47:36Z

## Summary(요약)

Action(행동): DS failure memory(DS 실패 기억)를 받아 3-class direction label(3분류 방향 라벨)과 regime/market-behavior features(국면/시장 현상 피처)를 붙인 새 모델을 학습했습니다.

Effect(효과): DP score bridge(DP 점수 브리지) 확대 반복에서 벗어나, long/short asymmetric source(롱/숏 비대칭 원천)를 새로 탐색했습니다.

## Selected(선택)

- selected_model_id(선택 모델 ID): `dir_h6_m3__behavior72(현상_72)__et7_l50_n128(엑스트라트리7_잎50_128)`
- validation net/PF/density(검증 순수익/PF/밀도): `-350.453` / `0.8114673359` / `2.5191256831`
- OOS net/PF/density(표본외 순수익/PF/밀도): `507.691` / `1.5005590349` / `2.6870229008`
- OOS long/short(표본외 롱/숏): `105` / `247`
- strict_candidate_count(엄격 후보 수): `0`

## Judgment(판정)

`inconclusive_regime_behavior_reseed_oos_clue_validation_quality_fail_no_package_no_authority`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`run364DU_review_h17_density_failure_regime_behavior_reseed_without_db_v1`에서 DT 모델/라벨/피처 씨앗을 검토합니다.

## Gates(게이트)

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DT/dt_regime_behavior_trade_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DT/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DT/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DT/dt_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DT/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DT/onnx_smoke_report.csv
- candidate_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DT/dt_regime_behavior_trade_surface.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DT/run364DU_regime_behavior_review_queue.csv
- no_trade_splitting_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DT/selected_dt_trade_tape.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DT/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DT/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DT/claim_boundary_receipt.json
