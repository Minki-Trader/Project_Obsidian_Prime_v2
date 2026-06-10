# run364GQ Density-Floor PF-Capped Router Review(밀도 바닥 PF 캡 라우터 검토)

Created(생성): 2026-06-07T12:58:21Z

Action(행동): GP 결과를 selector repair(선택기 수리), density floor(밀도 바닥), cost stress(비용 압박), package decision(패키지 결정) 기준으로 검토했습니다.

Effect(효과): PF999 sparse selection(PF999 희소 선택)은 수리됐음을 보존하되, combined cost0.9(합산 비용0.9) 실패 때문에 패키지 후보로 올리지 않습니다.

- judgment(판정): `negative_density_floor_pf_capped_router_review_selector_repaired_cost_density_incomplete_no_package_no_authority`
- review_subject(검토 대상): `gp_density_h1_m0p40__gp_gl_density_anchor__rf8_l20_n132`
- selector_repaired(선택기 수리): `true`
- selected combined density/trades(선택 합산 밀도/거래수): `1.8089171975` / `568.0`
- selected OOS net/PF/cost0.6(선택 표본외 순수익/수익 팩터/비용0.6): `51.657` / `1.1302092392` / `-14.643`
- density15 cost-near count(밀도1.5 비용 근접 수): `0`
- density20 cost-near count(밀도2.0 비용 근접 수): `0`
- density2.2 positive count(밀도2.2 양수 수): `0`
- package_eligible(패키지 가능): `false`
- next_run_id(다음 실행 ID): `run364GR_train_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GQ/gq_review_summary.csv
- parent_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GQ/input_manifest.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GQ/gq_surface_diagnostic.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GQ/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GQ/gq_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GQ/gq_gr_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GQ/result_judgment_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GQ/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GQ/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
