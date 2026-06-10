# run364DX H17 Validation-Stability Density Recovery Reseed(검증 안정성 밀도 회복 재시드)

Created(생성): 2026-06-06T11:30:42Z

## Summary(요약)

Action(행동): DW density failure memory(DW 밀도 실패 기억)를 받아 shorter-hold labels(짧은 보유 라벨), score-band expansion(점수 구간 확장), density recovery filters(밀도 회복 필터)를 학습했습니다.

Effect(효과): DV에서 회복한 net/PF(순수익/PF)를 보호하면서 trade density(거래 밀도)를 일 3회 목표에 가까이 올릴 수 있는지 확인했습니다.

## Selected(선택)

- selected_model_id(선택 모델 ID): `dense_dir_h2_m1p5__stability82(안정성_82)__rf8_l70_n112(랜덤포레스트8_잎70_112)`
- selected_filter(선택 필터): `drop_jan_feb_jun_sep`
- validation net/PF/density(검증 순수익/PF/밀도): `319.284` / `1.2174535479` / `3.6830601093`
- OOS net/PF/density(표본외 순수익/PF/밀도): `-77.908` / `0.9351630619` / `4.3053435115`
- strict_candidate_count(엄격 후보 수): `0`

## Judgment(판정)

`inconclusive_density_recovery_reseed_no_cross_split_candidate_no_package_no_authority`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`run364DY_review_h17_validation_stability_density_recovery_reseed_without_db_v1`에서 DX 밀도 회복 씨앗을 review(검토)합니다.

## Gates(게이트)

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DX/dx_density_recovery_trade_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DX/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DX/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DX/dx_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DX/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DX/onnx_smoke_report.csv
- candidate_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DX/dx_density_recovery_trade_surface.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DX/run364DY_density_recovery_review_queue.csv
- no_trade_splitting_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DX/selected_dx_trade_tape.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DX/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DX/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DX/claim_boundary_receipt.json
