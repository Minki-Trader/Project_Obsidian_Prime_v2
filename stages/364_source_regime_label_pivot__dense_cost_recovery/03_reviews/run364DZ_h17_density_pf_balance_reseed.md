# run364DZ H17 Density/PF Balance Reseed(밀도/PF 균형 재시드)

Created(생성): 2026-06-06T11:52:54Z

## Summary(요약)

Action(행동): DY failure memory(DY 실패 기억)를 받아 OOS bad-hour pruning(표본외 나쁜 시간 가지치기), side payoff balance(방향별 손익 균형), PF-aware selection(PF 인식 선택)을 실험했습니다.

Effect(효과): density>=3(밀도 3 이상)을 유지하면서 validation/OOS net/PF(검증/표본외 순수익/PF)를 동시에 회복할 수 있는지 확인했습니다.

## Selected(선택)

- selected_model_id(선택 모델 ID): `balance_dir_h3_m2__stability82(안정성_82)__et8_l60_n144(엑스트라트리8_잎60_144)`
- selected_filter(선택 필터): `no_h21`
- validation net/PF/density(검증 순수익/PF/밀도): `5.989` / `1.0038126802` / `3.262295082`
- OOS net/PF/density(표본외 순수익/PF/밀도): `258.875` / `1.2357412406` / `3.5877862595`
- strict_candidate_count(엄격 후보 수): `0`

## Judgment(판정)

`inconclusive_density_pf_balance_reseed_no_cross_split_candidate_no_package_no_authority`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`run364EA_review_h17_density_pf_balance_reseed_without_db_v1`에서 DZ 밀도/PF 균형 씨앗을 review(검토)합니다.

## Gates(게이트)

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DZ/dz_density_pf_balance_trade_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DZ/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DZ/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DZ/dz_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DZ/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DZ/onnx_smoke_report.csv
- candidate_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DZ/dz_density_pf_balance_trade_surface.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DZ/run364EA_density_pf_balance_review_queue.csv
- no_trade_splitting_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DZ/selected_dz_trade_tape.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DZ/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DZ/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DZ/claim_boundary_receipt.json
