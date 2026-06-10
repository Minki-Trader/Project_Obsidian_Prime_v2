# run364EA H17 Density/PF Balance Review(밀도/PF 균형 검토)

Created(생성): 2026-06-06T12:00:16Z

## Decision(결정)

Action(행동): DZ density/PF balance reseed(DZ 밀도/PF 균형 재시드)를 package(패키지) 후보로 검토했습니다.

Effect(효과): OOS(표본외) 회복 단서는 보존하지만 validation PF(검증 수익 팩터)가 약해 runtime package(런타임 패키지)는 열지 않습니다.

- judgment(판정): `negative_density_pf_balance_review_validation_pf_floor_failure_no_package_no_authority`
- selected_model_id(선택 모델 ID): `balance_dir_h3_m2__stability82(안정성_82)__et8_l60_n144(엑스트라트리8_잎60_144)`
- validation net/PF/density(검증 순수익/PF/밀도): `5.989` / `1.0038126802` / `3.262295082`
- OOS net/PF/density(표본외 순수익/PF/밀도): `258.875` / `1.2357412406` / `3.5877862595`
- strict_candidate_count(엄격 후보 수): `0`
- density_net_pf_count(밀도+순수익+PF 양쪽 통과 수): `0`
- relaxed_pf110_count(PF 1.10 완화 통과 수): `4`

## Next(다음)

`run364EB_train_h17_validation_pf_floor_density_recovery_reseed_without_db_v1`에서 validation PF floor(검증 PF 바닥)를 직접 올리는 density recovery(밀도 회복) 탐색을 실행합니다.

## Boundary(경계)

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EA/input_manifest.csv
- dz_gate_inheritance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DZ/required_gate_coverage_audit.csv
- review_summary_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EA/ea_density_pf_balance_review_summary.csv
- package_rejection_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EA/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EA/validation_pf_floor_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EA/run364EB_validation_pf_floor_density_recovery_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EA/result_judgment_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EA/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EA/claim_boundary_receipt.json
