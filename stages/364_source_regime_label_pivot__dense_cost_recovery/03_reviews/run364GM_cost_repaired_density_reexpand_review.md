# run364GM Cost-Repaired Density Reexpand Review(비용 수리 후 밀도 재확장 검토)

Created(생성): 2026-06-07T11:55:57Z

Action(행동): GL proxy/ONNX smoke(GL 프록시/ONNX 온엑스 간이 검증) 결과를 density recovery(밀도 회복), cost recollapse(비용 재붕괴), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): GL의 h1 density clue(h1 밀도 단서)는 보존하되, 비용 실패 때문에 운영 후보로 올리지 않고 GN dual-anchor router(GN 이중 앵커 라우터)로 넘깁니다.

- judgment(판정): `negative_cost_repaired_density_reexpand_review_density_recovered_cost_failed_no_package_no_authority`
- selected_model_id(선택 모델 ID): `gl_sym_h1_m0p40__gl_density_cost_blend__rf8_l18_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `26.532` / `1.0317575833` / `2.5901639344`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `11.528` / `1.0218949128` / `2.3053435115`
- OOS cost0.6/cost0.9(표본외 비용0.6/비용0.9): `-79.072` / `-169.672`
- combined density/cost0.9(합산 밀도/비용0.9): `2.4713375796` / `-427.54`
- density23 + cost near count(밀도2.3 + 비용 근접 수): `0`
- package_eligible(패키지 가능): `false`
- next_run_id(다음 실행 ID): `run364GN_train_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GM/gm_review_summary.csv
- parent_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GM/input_manifest.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GM/gm_surface_diagnostic.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GM/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GM/gm_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GM/gm_gn_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: pending -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GM/result_judgment_receipt.json
- required_gate_coverage_audit: pending -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GM/required_gate_coverage_audit.csv
- final_claim_guard: pending -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GM/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
