# run364GU Cost-Near Density Lift Router Review(비용 근접 밀도 상승 라우터 검토)

Created(생성): 2026-06-07T14:06:49Z

Action(행동): GT result(GT 결과)를 GR baseline(GR 기준선)과 비교해 density lift(밀도 상승), cost repair(비용 수리), package decision(패키지 결정)을 분리 판정했습니다.

Effect(효과): OOS density(표본외 밀도) 개선은 살리고, OOS cost0.6(표본외 비용0.6) 실패는 다음 GV 제약으로 바꿉니다.

- judgment(판정): `negative_cost_near_density_lift_router_review_oos_density_lifted_combined_cost_preserved_oos_cost_failed_no_package_no_authority`
- review_subject(검토 대상): `gt_cost_h2_m0p30__gt_gr_cost_anchor__rf8_l20_n132`
- OOS density change(표본외 밀도 변화): `1.1374045802` -> `1.4427480916` (`0.30534351140000004`)
- combined density change(합산 밀도 변화): `1.2643312102` -> `1.4299363057` (`0.16560509550000013`)
- OOS cost0.6 change(표본외 비용0.6 변화): `-22.809` -> `-29.212` (`-6.402999999999999`)
- combined cost0.9 change(합산 비용0.9 변화): `-108.053` -> `-137.142` (`-29.089`)
- OOS net/PF(표본외 순수익/수익 팩터): `27.488` / `1.0714233747`
- strict candidate count(엄격 후보 수): `0`
- package eligible(패키지 적격): `false`
- next_run_id(다음 실행 ID): `run364GV_train_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GU/gu_review_summary.csv
- parent_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GU/input_manifest.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GU/gu_surface_diagnostic.csv
- delta_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GU/gu_delta_attribution.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GU/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GU/gu_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GU/gu_gv_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GU/result_judgment_receipt.json
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GU/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
