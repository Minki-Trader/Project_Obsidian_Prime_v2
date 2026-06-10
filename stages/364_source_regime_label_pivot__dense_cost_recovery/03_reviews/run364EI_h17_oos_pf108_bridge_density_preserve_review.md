# run364EI H17 OOS PF108 Bridge Review(표본외 PF108 연결 검토)

Created(생성): 2026-06-06T14:03:22Z

Action(행동): EH OOS PF108 bridge density preserve(EH 표본외 PF108 연결 밀도 보존)를 package(패키지), failure memory(실패 기억), next seed(다음 씨앗) 관점에서 검토했습니다.

Effect(효과): OOS PF(표본외 수익 팩터) 개선을 density floor salvage(밀도 바닥 회수) 문제로 바꿉니다.

Findings(발견):

- selected OOS PF(선택 표본외 PF): `1.2623046122`
- selected validation/OOS density(선택 검증/표본외 밀도): `2.9344262295` / `2.8320610687`
- near_density_count(근접 밀도 후보 수): `15`
- density_net_count(밀도+순수익 후보 수): `0`
- oos108_count(표본외 PF 1.08 후보 수): `15`

Judgment(판정): `negative_oos_pf108_bridge_review_density_floor_failed_no_package_no_authority`

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

Next(다음): `run364EJ_train_h17_density_floor_oos_pf_salvage_without_db_v1`

Gates(게이트):

- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EI/input_manifest.csv
- review_summary_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EI/ei_oos_pf108_bridge_review_summary.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EI/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EI/oos_pf108_bridge_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EI/run364EJ_density_floor_oos_pf_salvage_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EI/result_judgment_receipt.json|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EI/model_validation_receipt.json|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EI/performance_attribution_receipt.json|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EI/artifact_lineage_receipt.json|stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EI/claim_boundary_receipt.json
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EI/claim_boundary_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EI/required_gate_coverage_audit.csv
