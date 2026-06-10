# run364GO Density-Cost Dual-Anchor Router Review(밀도-비용 이중 앵커 라우터 검토)

Created(생성): 2026-06-07T12:31:05Z

Action(행동): GN 결과를 density(밀도), cost stress(비용 압박), PF999 micro-sample(PF999 초소형 표본), package decision(패키지 결정) 기준으로 검토했습니다.

Effect(효과): 비용 양수처럼 보이는 7거래 후보를 운영 후보로 착각하지 않고, GP에서 PF cap(PF 캡)과 hard density floor(하드 밀도 바닥)를 수리하게 합니다.

- judgment(판정): `negative_density_cost_dual_anchor_router_review_sparse_pf999_density_failed_no_package_no_authority`
- review_subject(검토 대상): `gn_density_h1_m0p40__gn_gl_density_anchor__et7_l12_n132`
- selected combined density/trades(선택 합산 밀도/거래수): `0.0222929936` / `7.0`
- selected OOS net/PF/cost0.6(선택 표본외 순수익/수익 팩터/비용0.6): `21.938` / `999.0` / `21.038`
- density15 cost-near count(밀도1.5 비용 근접 수): `5`
- density20 cost-near count(밀도2.0 비용 근접 수): `0`
- density2.2 positive count(밀도2.2 양수 수): `0`
- package_eligible(패키지 가능): `false`
- next_run_id(다음 실행 ID): `run364GP_train_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GO/go_review_summary.csv
- parent_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GO/input_manifest.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GO/go_surface_diagnostic.csv
- package_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GO/package_decision.csv
- failure_memory_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GO/go_failure_memory.csv
- next_queue_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GO/go_gp_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GO/result_judgment_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GO/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GO/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
