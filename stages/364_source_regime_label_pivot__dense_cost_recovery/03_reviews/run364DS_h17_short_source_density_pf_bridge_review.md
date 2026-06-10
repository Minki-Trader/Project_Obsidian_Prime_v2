# run364DS H17 Short-Source Density/PF Bridge Review(숏 원천 밀도/PF 브리지 검토)

Created(생성): 2026-06-06T10:27:54Z

## Review(검토)

Action(행동): DR density/PF bridge(DR 밀도/PF 브리지)의 package(패키지) 가능성을 검토했습니다.

Effect(효과): density_both_count(양쪽 밀도 통과 수) `2013`에도 density_and_net_count(양쪽 밀도+순수익 통과 수)가 `0`라 runtime package(런타임 패키지)를 열지 않습니다.

## Decision(결정)

- decision(결정): `stage364DS_reject_package_open_run364DT_regime_behavior_reseed`
- judgment(판정): `negative_density_pf_bridge_review_density_recovery_breaks_validation_no_package_no_authority`
- selected_variant_id(선택 변형 ID): `dr03252_h16_21_s0p516397_p0p0_mn0p2_dominant_h8`
- validation net/PF/density(검증 순수익/PF/밀도): `126.292` / `1.119622337` / `1.4153005464`
- OOS net/PF/density(표본외 순수익/PF/밀도): `223.165` / `1.3264464563` / `1.4198473282`

## Boundary(경계)

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`run364DT_train_h17_density_failure_regime_behavior_reseed_without_db_v1`에서 regime/market-behavior reseed(국면/시장 현상 재시드)를 엽니다.

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DS/input_manifest.csv
- parent_gate_inheritance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DR/required_gate_coverage_audit.csv
- review_summary_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DS/ds_density_pf_bridge_review_summary.csv
- package_rejection_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DS/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DS/density_pf_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DS/run364DT_regime_behavior_reseed_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DS/result_judgment_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DS/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364DS/claim_boundary_receipt.json
