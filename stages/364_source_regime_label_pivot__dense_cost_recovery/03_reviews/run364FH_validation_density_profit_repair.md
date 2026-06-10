# run364FH Validation Density Profit Repair(검증 밀도 수익 수리)

Created(생성): 2026-06-07T03:45:51Z

Action(행동): FG failure memory(FG 실패 기억)를 받아 validation density profit score(검증 밀도 수익 점수), dense profit labels(고밀도 수익 라벨), short bleed veto(숏 손실 차단)를 학습했습니다.

Effect(효과): FF의 OOS PF/cost/short(표본외 수익 팩터/비용/숏) 단서를 보존하면서 validation/combined density(검증/합산 밀도) 3/day(일 3회)를 회복할 수 있는지 확인합니다.

- judgment(판정): `inconclusive_validation_density_profit_repair_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `fh_sym_h2_m1p75__fh_session_macro_profit__et7_l18_n128`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `76.781` / `1.0531729164` / `2.7103825137`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `152.487` / `1.1853206259` / `2.7175572519`
- OOS cost0.6 net(표본외 비용0.6 순수익): `45.687`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `229.268` / `2.7133757962` / `-281.932` / `0.691314554`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364FI_review_h17_oos108_pf125_validation_density_profit_repair_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FH/fh_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FH/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FH/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FH/fh_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FH/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FH/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FH/fh_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FH/selected_fh_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FH/fh_fi_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FH/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FH/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FH/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
