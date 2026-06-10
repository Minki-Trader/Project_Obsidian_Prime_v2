# run364GS Cost-Near Density Floor Router Review(비용 근접 밀도 바닥 라우터 검토)

Created(생성): 2026-06-07T13:35:42Z

Action(행동): GR 결과를 combined cost0.9(합산 비용0.9), OOS cost0.6(표본외 비용0.6), density floor(밀도 바닥), package decision(패키지 결정) 기준으로 검토했습니다.

Effect(효과): 합산 비용 수리 단서는 보존하지만, 표본외 비용0.6과 밀도 상승이 약하므로 패키지 후보로 올리지 않습니다.

- judgment(판정): `negative_cost_near_density_floor_router_review_combined_cost_repaired_oos_cost_failed_density_floor_weak_no_package_no_authority`
- review_subject(검토 대상): `gr_cost_h2_m0p35__gr_gp_density_anchor__rf8_l20_n132`
- combined cost0.9 change(합산 비용0.9 변화): `-286.862` -> `-108.053` (`178.80900000000003`)
- OOS cost0.6 change(표본외 비용0.6 변화): `-14.643` -> `-22.809` (`-8.166`)
- selected OOS net/PF/density(선택 표본외 순수익/수익 팩터/밀도): `21.891` / `1.0732395214` / `1.1374045802`
- selected combined density/trades(선택 합산 밀도/거래수): `1.2643312102` / `397.0`
- combined_cost_repaired(합산 비용 수리): `true`
- cost_near_target_met(비용 근접 목표 충족): `false`
- density_floor_kept(밀도 바닥 유지): `true`
- package_eligible(패키지 가능): `false`
- next_run_id(다음 실행 ID): `run364GT_train_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GS/gs_review_summary.csv
- parent_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GS/input_manifest.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GS/gs_surface_diagnostic.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GS/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GS/gs_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GS/gs_gt_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GS/result_judgment_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GS/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GS/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
