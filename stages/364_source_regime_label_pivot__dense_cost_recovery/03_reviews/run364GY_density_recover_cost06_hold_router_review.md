# run364GY Density Recover Cost0.6 Hold Router Review(밀도 회복 비용0.6 유지 라우터 검토)

Created(생성): 2026-06-07T15:07:03Z

Action(행동): GX result(GX 결과)를 GV baseline(GV 기준선)과 비교해 OOS profit/cost clue(표본외 수익/비용 단서), density recovery(밀도 회복), combined cost hold(합산 비용 유지)를 분리 판정했습니다.

Effect(효과): OOS profit/cost0.6(표본외 수익/비용0.6) 단서는 살리고, density(밀도)와 combined cost(합산 비용) 실패는 GZ의 직접 제약으로 넘깁니다.

- judgment(판정): `negative_for_package_positive_oos_profit_cost06_clue_density_not_recovered_combined_cost_slipped_no_authority`
- review_subject(검토 대상): `gx_cost_h2_m0p30__gx_cost_hold_behavior_anchor__rf9_l22_n160`
- OOS net/PF change(표본외 순수익/수익 팩터 변화): `37.85` / `1.1052444257` -> `78.765` / `1.2405860936`
- OOS cost0.6 change(표본외 비용0.6 변화): `-12.85` -> `27.465` (`40.315`)
- OOS density change(표본외 밀도 변화): `1.2900763359` -> `1.3053435115` (`0.015267175600000016`)
- combined density change(합산 밀도 변화): `1.3280254777` -> `1.2993630573` (`-0.02866242040000011`)
- combined cost0.9 change(합산 비용0.9 변화): `-77.619` -> `-132.105` (`-54.48599999999999`)
- package eligible(패키지 적격): `false`
- next_run_id(다음 실행 ID): `run364GZ_train_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GY/gy_review_summary.csv
- parent_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GY/input_manifest.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GY/gy_surface_diagnostic.csv
- delta_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GY/gy_delta_attribution.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GY/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GY/gy_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GY/gy_gz_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GY/result_judgment_receipt.json
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GY/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
