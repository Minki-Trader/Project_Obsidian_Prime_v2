# run364FZ Density Profit Conflict Reblend(밀도 수익 충돌 재혼합)

Created(생성): 2026-06-07T08:23:52Z

Action(행동): FY failure memory(FY 실패 기억)를 받아 density3 negative rows(밀도3 음수 행)와 low-density OOS-positive rows(저밀도 표본외 양수 행)를 conflict constraints(충돌 제약)로 재혼합했습니다.

Effect(효과): density-only negative(밀도 전용 음수) 실패와 low-density profit-only(저밀도 수익 전용) 실패를 동시에 줄일 수 있는지 확인합니다.

- judgment(판정): `inconclusive_density_profit_conflict_reblend_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `fz_sym_h1_m0p65__fz_all72__rf8_l18_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `-95.425` / `0.9025867965` / `2.7103825137`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `-107.009` / `0.8470401907` / `2.786259542`
- OOS cost0.6 net(표본외 비용0.6 순수익): `-216.509`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `-202.434` / `2.7420382166` / `-719.034` / `0.7944250871`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364GA_review_h17_oos108_pf125_density_profit_conflict_reblend_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FZ/fz_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FZ/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FZ/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FZ/fz_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FZ/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FZ/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FZ/fz_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FZ/selected_fz_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FZ/fz_ga_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FZ/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FZ/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FZ/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
