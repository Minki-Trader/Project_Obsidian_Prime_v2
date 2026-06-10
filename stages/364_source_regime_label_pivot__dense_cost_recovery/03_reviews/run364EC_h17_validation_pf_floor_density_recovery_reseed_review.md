# run364EC H17 Validation PF Floor Review(검증 PF 바닥 검토)

Created(생성): 2026-06-06T12:32:38Z

## Decision(결정)

Action(행동): EB validation PF floor density recovery(EB 검증 PF 바닥 밀도 회복)를 package(패키지) 후보로 검토했습니다.

Effect(효과): density_net(밀도+순수익)은 늘었지만 dual PF floor(양쪽 PF 바닥)가 실패해 runtime package(런타임 패키지)는 열지 않습니다.

- judgment(판정): `negative_validation_pf_floor_review_dual_pf_below_floor_no_package_no_authority`
- selected_model_id(선택 모델 ID): `pf_floor_dir_h2_m1p5__stability82(안정성_82)__rf8_l60_n128(랜덤포레스트8_잎60_128)`
- validation net/PF/density(검증 순수익/PF/밀도): `145.015` / `1.094148222` / `3.7759562842`
- OOS net/PF/density(표본외 순수익/PF/밀도): `77.165` / `1.0619016601` / `4.3435114504`
- density_net_count(밀도+순수익 후보 수): `144`
- pf110_count(PF 1.10 양쪽 통과 수): `0`
- pf120_count(PF 1.20 양쪽 통과 수): `0`

## Next(다음)

`run364ED_train_h17_dual_pf_floor_bridge_reseed_without_db_v1`에서 validation/OOS min_pf(검증/표본외 최소 PF)를 직접 보상하는 dual PF floor bridge(양쪽 PF 바닥 연결) 탐색을 실행합니다.

## Boundary(경계)

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Gates(게이트)

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EC/input_manifest.csv
- eb_gate_inheritance_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EB/required_gate_coverage_audit.csv
- review_summary_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EC/ec_validation_pf_floor_review_summary.csv
- package_rejection_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EC/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EC/dual_pf_floor_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EC/run364ED_dual_pf_floor_bridge_reseed_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EC/result_judgment_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EC/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EC/claim_boundary_receipt.json
