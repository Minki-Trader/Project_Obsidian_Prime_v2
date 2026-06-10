# run364DY H17 Density Recovery Reseed Review(밀도 회복 재시드 검토)

Created(생성): 2026-06-06T11:35:13Z

## Decision(결정)

Action(행동): DX density recovery(DX 밀도 회복)를 package(패키지) 후보로 검토했습니다.

Effect(효과): density(밀도)는 회복됐지만 OOS net/PF(표본외 순수익/PF)가 깨져 package(패키지)를 열지 않습니다.

- judgment(판정): `negative_density_recovery_review_oos_pf_net_failure_no_package_no_authority`
- selected_model_id(선택 모델 ID): `dense_dir_h2_m1p5__stability82(안정성_82)__rf8_l70_n112(랜덤포레스트8_잎70_112)`
- validation net/PF/density(검증 순수익/PF/밀도): `319.284` / `1.2174535479` / `3.6830601093`
- OOS net/PF/density(표본외 순수익/PF/밀도): `-77.908` / `0.9351630619` / `4.3053435115`
- density_both_count(양쪽 밀도 통과 수): `2890`
- density_net_count(양쪽 밀도+순수익 통과 수): `84`
- density_net_pf_count(양쪽 밀도+순수익+PF 통과 수): `0`

## Next(다음)

`run364DZ_train_h17_density_pf_balance_reseed_without_db_v1`에서 density/PF balance(밀도/PF 균형)를 탐색합니다.

## Boundary(경계)

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DY/input_manifest.csv
- dx_gate_inheritance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DX/required_gate_coverage_audit.csv
- review_summary_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DY/dy_density_recovery_review_summary.csv
- oos_failure_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DY/density_pf_failure_memory.csv
- package_rejection_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DY/package_decision.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DY/run364DZ_density_pf_balance_reseed_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DY/result_judgment_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DY/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DY/claim_boundary_receipt.json
