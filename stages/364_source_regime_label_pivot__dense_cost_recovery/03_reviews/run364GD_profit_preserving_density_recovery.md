# run364GD Profit Preserving Density Recovery(수익 보존 밀도 회복)

Created(생성): 2026-06-07T09:26:35Z

Action(행동): GC failure memory(GC 실패 기억)를 받아 GB profit recovery(GB 수익 회복)를 보존 조건으로 고정하고 density/cost(밀도/비용)를 다시 학습했습니다.

Effect(효과): OOS profit(표본외 수익)을 반납하지 않고 density(밀도)와 cost0.9(비용0.9)를 개선할 수 있는지 확인합니다.

- judgment(판정): `inconclusive_profit_preserving_density_recovery_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `gd_sym_h1_m0p65__gd_all72__rf8_l18_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `16.965` / `1.0259839517` / `2.0546448087`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `83.737` / `1.184927453` / `2.0458015267`
- OOS cost0.6 net(표본외 비용0.6 순수익): `3.337`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `100.702` / `2.050955414` / `-285.698` / `0.7329192547`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364GE_review_h17_oos108_pf125_profit_preserving_density_recovery_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GD/gd_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GD/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GD/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GD/gd_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GD/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GD/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GD/gd_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GD/selected_gd_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GD/gd_ge_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GD/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GD/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GD/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
