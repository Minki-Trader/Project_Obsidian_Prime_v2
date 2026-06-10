# run364EB H17 Validation PF Floor Density Recovery Reseed(검증 PF 바닥 밀도 회복 재시드)

Created(생성): 2026-06-06T12:26:43Z

## Summary(요약)

Action(행동): EA failure memory(EA 실패 기억)를 받아 validation PF floor(검증 PF 바닥)를 직접 보상하는 label/filter/model sweep(라벨/필터/모델 탐색)을 실행했습니다.

Effect(효과): DZ의 OOS recovery clue(표본외 회복 단서)를 보존하면서 validation PF(검증 PF)를 끌어올릴 수 있는지 확인했습니다.

## Selected(선택)

- selected_model_id(선택 모델 ID): `pf_floor_dir_h2_m1p5__stability82(안정성_82)__rf8_l60_n128(랜덤포레스트8_잎60_128)`
- selected_filter(선택 필터): `no_h21`
- validation net/PF/density(검증 순수익/PF/밀도): `145.015` / `1.094148222` / `3.7759562842`
- OOS net/PF/density(표본외 순수익/PF/밀도): `77.165` / `1.0619016601` / `4.3435114504`
- strict_candidate_count(엄격 후보 수): `0`

## Judgment(판정)

`inconclusive_validation_pf_floor_reseed_no_cross_split_candidate_no_package_no_authority`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`run364EC_review_h17_validation_pf_floor_density_recovery_reseed_without_db_v1`에서 EB validation PF floor seed(EB 검증 PF 바닥 씨앗)를 review(검토)합니다.

## Gates(게이트)

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EB/eb_validation_pf_floor_trade_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EB/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EB/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EB/eb_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EB/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EB/onnx_smoke_report.csv
- candidate_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EB/eb_validation_pf_floor_trade_surface.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EB/run364EC_validation_pf_floor_review_queue.csv
- no_trade_splitting_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EB/selected_eb_trade_tape.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EB/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EB/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EB/claim_boundary_receipt.json
