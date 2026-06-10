# run364GK Density-Cost Floor Rejoin Review(밀도-비용 바닥 재결합 검토)

Created(생성): 2026-06-07T11:25:04Z

Action(행동): GJ proxy/ONNX smoke(GJ 프록시/ONNX 온엑스 간이 검증) 결과를 cost repair(비용 수리), density loss(밀도 손실), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): 비용 회복 단서는 보존하지만, 낮은 trade density(거래 밀도) 때문에 운영 후보로 올리지 않고 GL cost-repaired density reexpand(GL 비용 수리 후 밀도 재확장)로 넘깁니다.

- judgment(판정): `negative_density_cost_floor_rejoin_review_cost_floor_repaired_density_failed_no_package_no_authority`
- selected_model_id(선택 모델 ID): `gj_sym_h2_m0p35__gj_session_regime_cost__et7_l12_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `204.302` / `1.2407271468` / `1.7049180328`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `85.724` / `1.177054977` / `1.5419847328`
- OOS cost0.6/cost0.9(표본외 비용0.6/비용0.9): `25.124` / ``
- combined density/cost0.9(합산 밀도/비용0.9): `1.6369426752` / `-18.374`
- density20 + cost06 nonnegative count(밀도2.0 + 비용0.6 양수 수): `0`
- package_eligible(패키지 가능): `false`
- next_run_id(다음 실행 ID): `run364GL_train_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GK/gk_review_summary.csv
- parent_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GK/input_manifest.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GK/gk_surface_diagnostic.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GK/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GK/gk_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GK/gk_gl_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GK/result_judgment_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GK/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GK/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
