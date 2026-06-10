# run364HC OOS Profit-Density Rebalance Review(표본외 수익-밀도 재균형 검토)

Created(생성): 2026-06-07T16:14:20Z

Action(행동): HB result(HB 결과)를 GZ reference(GZ 기준)와 비교해 OOS profit/PF/cost0.6(표본외 수익/수익 팩터/비용0.6), OOS density(표본외 밀도), combined density/cost0.9(합산 밀도/비용0.9)를 분리 판정했습니다.

Effect(효과): HB는 combined cost0.9(합산 비용0.9)를 개선했지만 density/profit(밀도/수익)을 후퇴시켰으므로 package(패키지)를 닫고 HD dual-surface switch(HD 이중 표면 전환)를 엽니다.

- judgment(판정): `negative_for_package_hb_cost_improved_density_profit_regressed_no_package_no_authority`
- review_subject(검토 대상): `hb_rebalance_h2_m0p26__hb_oos_profit_density_bridge__rf9_l20_n192`
- OOS net/PF/cost0.6 change(표본외 순수익/수익 팩터/비용0.6 변화): `45.36` / `1.1193919853` / `-8.94` -> `40.598` / `1.1145199235` / `-10.402`
- OOS density change(표본외 밀도 변화): `1.3816793893` -> `1.2977099237` (`-0.08396946559999985`)
- combined density change(합산 밀도 변화): `1.3057324841` -> `1.2770700637` (`-0.02866242039999989`)
- combined cost0.9 change(합산 비용0.9 변화): `-86.331` -> `-24.605` (`61.726`)
- surface counts(표면 수): target_profit(목표 수익) `165`, oos_density_cost(표본외 밀도-비용) `0`, joint_target(공동 목표) `0`
- package eligible(패키지 적격): `false`
- next_run_id(다음 실행 ID): `run364HD_train_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HC/hc_review_summary.csv
- parent_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HC/input_manifest.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HC/hc_surface_diagnostic.csv
- delta_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HC/hc_delta_attribution.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HC/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HC/hc_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HC/hc_hd_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HC/result_judgment_receipt.json
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HC/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
