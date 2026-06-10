# run364HA Cost-Density Joint Frontier Router Review(비용-밀도 공동 경계 라우터 검토)

Created(생성): 2026-06-07T15:38:17Z

Action(행동): GZ result(GZ 결과)를 GX baseline(GX 기준선)과 비교해 OOS density(표본외 밀도), combined cost0.9(합산 비용0.9), OOS profit/cost0.6(표본외 수익/비용0.6), combined density(합산 밀도)를 분리 판정했습니다.

Effect(효과): 비용/밀도 회복 단서는 보존하고, 수익/비용0.6과 합산 밀도 실패는 HB의 직접 제약으로 넘깁니다.

- judgment(판정): `negative_for_package_positive_oos_density_combined_cost_clue_profit_cost06_and_combined_density_failed_no_authority`
- review_subject(검토 대상): `gz_cost_h2_m0p32__gz_joint_frontier_blend__rf9_l20_n176`
- OOS net/PF/cost0.6 change(표본외 순수익/수익 팩터/비용0.6 변화): `78.765` / `1.2405860936` / `27.465` -> `45.36` / `1.1193919853` / `-8.94`
- OOS density change(표본외 밀도 변화): `1.3053435115` -> `1.3816793893` (`0.07633587779999984`)
- combined density change(합산 밀도 변화): `1.2993630573` -> `1.3057324841` (`0.0063694268000000775`)
- combined cost0.9 change(합산 비용0.9 변화): `-132.105` -> `-86.331` (`45.77399999999999`)
- package eligible(패키지 적격): `false`
- next_run_id(다음 실행 ID): `run364HB_train_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HA/ha_review_summary.csv
- parent_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HA/input_manifest.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HA/ha_surface_diagnostic.csv
- delta_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HA/ha_delta_attribution.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HA/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HA/ha_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HA/ha_hb_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HA/result_judgment_receipt.json
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HA/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
