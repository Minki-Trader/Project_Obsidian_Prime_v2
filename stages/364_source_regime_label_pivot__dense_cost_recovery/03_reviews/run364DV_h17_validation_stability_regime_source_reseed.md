# run364DV H17 Validation-Stability Regime Source Reseed(검증 안정성 국면 원천 재시드)

Created(생성): 2026-06-06T11:14:36Z

## Summary(요약)

Action(행동): DU failure memory(DU 실패 기억)를 받아 validation-stability labels/filters(검증 안정성 라벨/필터)를 붙인 새 모델을 학습했습니다.

Effect(효과): OOS-only clue(OOS 전용 단서)를 쫓지 않고 validation quality(검증 품질)를 먼저 살리는 방향으로 탐색 압력을 옮겼습니다.

## Selected(선택)

- selected_model_id(선택 모델 ID): `stable_dir_h6_m3__short_stability57(숏_안정성_57)__rf8_l70_n112(랜덤포레스트8_잎70_112)`
- selected_filter(선택 필터): `drop_validation_negative_months`
- validation net/PF/density(검증 순수익/PF/밀도): `252.884` / `1.5321924179` / `0.650273224`
- OOS net/PF/density(표본외 순수익/PF/밀도): `276.32` / `1.9859908794` / `0.8473282443`
- strict_candidate_count(엄격 후보 수): `0`

## Judgment(판정)

`inconclusive_validation_stability_reseed_no_cross_split_candidate_no_package_no_authority`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`run364DW_review_h17_validation_stability_regime_source_reseed_without_db_v1`에서 DV 모델/필터 씨앗을 review(검토)합니다.

## Gates(게이트)

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DV/dv_validation_stability_trade_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DV/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DV/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DV/dv_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DV/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DV/onnx_smoke_report.csv
- candidate_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DV/dv_validation_stability_trade_surface.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DV/run364DW_validation_stability_review_queue.csv
- no_trade_splitting_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DV/selected_dv_trade_tape.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DV/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DV/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DV/claim_boundary_receipt.json
