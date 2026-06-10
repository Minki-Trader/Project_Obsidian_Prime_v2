# run364HB OOS Profit-Density Rebalance Cost Floor Router(표본외 수익-밀도 재균형 비용 바닥 라우터)

Created(생성): 2026-06-07T16:08:10Z

Action(행동): HA failure memory(HA 실패 기억)를 받아 OOS density(표본외 밀도)와 combined cost0.9(합산 비용0.9)를 보존하면서 OOS net/PF/cost0.6(표본외 순수익/수익 팩터/비용0.6)과 combined density(합산 밀도)를 함께 점수화했습니다.

Effect(효과): HC review(HC 검토)가 HB 결과를 package(패키지), profit repair(수익 수리), density repair(밀도 수리), cost floor(비용 바닥) 경계로 분리 판정할 수 있습니다.

- judgment(판정): `inconclusive_oos_profit_density_rebalance_cost_floor_router_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `hb_rebalance_h2_m0p26__hb_oos_profit_density_bridge__rf9_l20_n192`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `175.397` / `1.4141214525` / `1.262295082`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `40.598` / `1.1145199235` / `1.2977099237`
- OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `-10.402` / `-61.402`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `215.995` / `1.2770700637` / `-24.605` / `0.8054862843`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364HC_review_h17_oos108_pf125_oos_profit_density_rebalance_cost_floor_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HB/hb_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HB/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HB/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HB/hb_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HB/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HB/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HB/hb_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HB/selected_hb_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HB/hb_hc_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HB/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HB/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HB/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
