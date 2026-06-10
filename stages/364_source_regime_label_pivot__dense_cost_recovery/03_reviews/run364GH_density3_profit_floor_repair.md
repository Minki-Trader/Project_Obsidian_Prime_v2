# run364GH Density3 Profit-Floor Repair(밀도3 수익 바닥 수리)

Created(생성): 2026-06-07T10:44:30Z

Action(행동): GG failure memory(GG 실패 기억)를 받아 GF validation/OOS floor(GF 검증/표본외 바닥)를 보존 조건으로 두고 lower threshold/wider hours(낮은 임계값/넓은 시간)를 다시 학습했습니다.

Effect(효과): validation net(검증 순수익)과 OOS floor(표본외 바닥)를 잃지 않으면서 density(밀도)가 3/day(일 3회)에 접근하는지 확인합니다.

- judgment(판정): `inconclusive_density3_profit_floor_repair_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `gh_sym_h1_m0p35__gh_all72__rf8_l18_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `0.439` / `1.0005209817` / `2.7103825137`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `82.117` / `1.1481991485` / `2.6870229008`
- OOS cost0.6 net(표본외 비용0.6 순수익): `-23.483`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `82.556` / `2.7006369427` / `-426.244` / `0.6827830189`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364GI_review_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GH/gh_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GH/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GH/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GH/gh_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GH/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GH/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GH/gh_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GH/selected_gh_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GH/gh_gi_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GH/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GH/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GH/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
