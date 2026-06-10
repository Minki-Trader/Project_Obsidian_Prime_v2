# run364GW OOS Cost0.6 Density Preserve Router Review(표본외 비용0.6 밀도 보존 라우터 검토)

Created(생성): 2026-06-07T14:40:40Z

Action(행동): GV result(GV 결과)를 GT baseline(GT 기준선)과 비교해 cost repair(비용 수리), density preserve(밀도 보존), package decision(패키지 결정)을 분리 판정했습니다.

Effect(효과): 비용 수리 단서는 살리고, 밀도 하락은 GX의 직접 수리 조건으로 넘깁니다.

- judgment(판정): `negative_for_package_positive_cost_repair_clue_density_failed_no_authority`
- review_subject(검토 대상): `gv_cost_h2_m0p32__gv_cost_side_behavior_anchor__rf9_l22_n144`
- OOS cost0.6 change(표본외 비용0.6 변화): `-29.212` -> `-12.85` (`16.362000000000002`)
- OOS density change(표본외 밀도 변화): `1.4427480916` -> `1.2900763359` (`-0.1526717556999999`)
- combined density change(합산 밀도 변화): `1.4299363057` -> `1.3280254777` (`-0.10191082800000006`)
- combined cost0.9 change(합산 비용0.9 변화): `-137.142` -> `-77.619` (`59.522999999999996`)
- package eligible(패키지 적격): `false`
- next_run_id(다음 실행 ID): `run364GX_train_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GW/gw_review_summary.csv
- parent_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GW/input_manifest.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GW/gw_surface_diagnostic.csv
- delta_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GW/gw_delta_attribution.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GW/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GW/gw_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GW/gw_gx_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GW/result_judgment_receipt.json
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GW/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
