# run364DW H17 Validation-Stability Reseed Review(검증 안정성 재시드 검토)

Created(생성): 2026-06-06T11:19:19Z

## Review(검토)

Action(행동): DV validation-stability reseed(DV 검증 안정성 재시드)를 package(패키지) 후보로 검토했습니다.

Effect(효과): validation/OOS net/PF(검증/표본외 순수익/PF)는 살아났지만 density(밀도)가 목표 미달이라 package(패키지)를 열지 않습니다.

## Decision(결정)

- decision(결정): `stage364DW_reject_package_open_run364DX_density_recovery_reseed`
- judgment(판정): `negative_validation_stability_review_density_below_trade_objective_no_package_no_authority`
- selected_model_id(선택 모델 ID): `stable_dir_h6_m3__short_stability57(숏_안정성_57)__rf8_l70_n112(랜덤포레스트8_잎70_112)`
- validation net/PF/density(검증 순수익/PF/밀도): `252.884` / `1.5321924179` / `0.650273224`
- OOS net/PF/density(표본외 순수익/PF/밀도): `276.32` / `1.9859908794` / `0.8473282443`
- density_both_count(양쪽 밀도 통과 수): `140`
- density_net_pf_count(양쪽 밀도+순수익+PF 통과 수): `0`

## Boundary(경계)

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`run364DX_train_h17_validation_stability_density_recovery_reseed_without_db_v1`에서 density recovery(밀도 회복)를 탐색합니다.

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DW/input_manifest.csv
- dv_gate_inheritance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DV/required_gate_coverage_audit.csv
- review_summary_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DW/dw_validation_stability_review_summary.csv
- density_failure_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DW/density_failure_memory.csv
- package_rejection_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DW/package_decision.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DW/run364DX_density_recovery_reseed_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DW/result_judgment_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DW/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DW/claim_boundary_receipt.json
