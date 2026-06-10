# run364EE H17 Dual PF Floor Bridge Review(양쪽 PF 바닥 연결 검토)

Created(생성): 2026-06-06T13:23:09Z

## Summary(요약)

Action(행동): ED dual PF floor bridge(ED 양쪽 PF 바닥 연결) 결과를 package(패키지), failure memory(실패 기억), next seed(다음 씨앗) 관점에서 검토했습니다.

Effect(효과): 직접 min_pf(최소 PF) 보상 실패를 EF의 validation source rotation(검증 원천 회전) 제약으로 바꿉니다.

## Findings(발견)

- selected min_pf(선택 최소 PF): `1.0219124076`
- EB best bridge min_pf(EB 최고 연결 최소 PF): `1.0619016601`
- min_pf delta(최소 PF 차이): `-0.0399892525`
- density_net_count(밀도+순수익 후보 수): `6`
- pf110_count(PF 1.10 양쪽 통과 수): `0`
- best_sparse_min_pf/best_sparse_min_density(최고 희소 최소 PF/최소 밀도): `2.0903376911` / `0.2950819672`

## Judgment(판정)

`negative_dual_pf_floor_bridge_review_min_pf_regressed_no_package_no_authority`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`run364EF_train_h17_validation_source_rotation_density_recovery_without_db_v1`에서 validation source rotation density recovery(검증 원천 회전 밀도 회복)를 탐색합니다.

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EE/input_manifest.csv
- review_summary_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EE/ee_dual_pf_floor_bridge_review_summary.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EE/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EE/dual_pf_floor_bridge_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EE/run364EF_validation_source_rotation_density_recovery_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EE/result_judgment_receipt.json|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EE/model_validation_receipt.json|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EE/performance_attribution_receipt.json|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EE/artifact_lineage_receipt.json|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EE/claim_boundary_receipt.json
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EE/claim_boundary_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EE/required_gate_coverage_audit.csv
