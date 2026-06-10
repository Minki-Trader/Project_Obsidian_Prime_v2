# run364EK H17 Density Floor OOS PF Salvage Review(밀도 바닥 표본외 PF 회수 검토)

Created(생성): 2026-06-06T14:33:39Z

Action(행동): EJ density floor OOS PF salvage(EJ 밀도 바닥 표본외 PF 회수)를 package(패키지), failure memory(실패 기억), next seed(다음 씨앗) 관점에서 검토했습니다.

Effect(효과): density restore(밀도 회복)와 OOS PF collapse(표본외 PF 붕괴)를 분리해, EL validation floor bridge(EL 검증 바닥 연결)로 넘깁니다.

Findings(발견):

- selected validation/OOS PF(선택 검증/표본외 PF): `1.175471598` / `1.0183147066`
- selected validation/OOS density(선택 검증/표본외 밀도): `3.2896174863` / `3.4122137405`
- density_net_count(밀도+순수익 후보 수): `240`
- density_oos108_count(밀도+표본외 PF 1.08 후보 수): `30`
- density_oos108_val104_count(밀도+표본외 PF 1.08+검증 PF 1.04 후보 수): `0`
- best density OOS108 validation/OOS PF(최선 밀도 OOS108 검증/표본외 PF): `1.0298633893` / `1.0817131109`

Judgment(판정): `negative_density_floor_oos_pf_salvage_review_oos_pf_collapsed_validation_floor_gap_no_package_no_authority`

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

Next(다음): `run364EL_train_h17_oos108_validation_floor_bridge_without_db_v1`

Gates(게이트):

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EK/input_manifest.csv
- review_summary_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EK/ek_density_floor_oos_pf_salvage_review_summary.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EK/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EK/density_floor_oos_pf_salvage_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EK/run364EL_oos108_validation_floor_bridge_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EK/result_judgment_receipt.json|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EK/model_validation_receipt.json|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EK/performance_attribution_receipt.json|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EK/artifact_lineage_receipt.json|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EK/claim_boundary_receipt.json
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EK/claim_boundary_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EK/required_gate_coverage_audit.csv
