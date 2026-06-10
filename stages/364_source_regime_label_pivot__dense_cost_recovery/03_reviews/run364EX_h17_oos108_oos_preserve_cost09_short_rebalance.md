# run364EX H17 OOS108 OOS Preserve Cost09/Short Rebalance(표본외 보존 비용0.9/숏 재균형)

Created(생성): 2026-06-07T01:26:11Z

Action(행동): EW review(EW 검토)의 실패 기억을 받아 OOS preserve first(표본외 보존 우선) model/label/score(모델/라벨/점수)를 학습했습니다.

Effect(효과): EV validation-only cost09(검증 전용 비용0.9) 붕괴를 줄이고 OOS net/PF/cost0.6(표본외 순수익/수익 팩터/비용0.6) 보존 여부를 먼저 봅니다.

- judgment(판정): `inconclusive_oos_preserve_cost09_short_rebalance_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `ex_sym_h2_m2__ex_all72__rf8_l48_n112`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `184.525` / `1.1374262691` / `3.0491803279`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `162.566` / `1.1942833377` / `3.0839694656`
- OOS cost0.6 net(표본외 비용0.6 순수익): `41.366`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `347.091` / `3.0636942675` / `-230.109` / `0.7141372141`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영형 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364EY_review_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EX/ex_oos_preserve_cost09_short_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EX/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EX/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EX/ex_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EX/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EX/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EX/ex_oos_preserve_cost09_short_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EX/selected_ex_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EX/run364EY_oos_preserve_cost09_short_review_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EX/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EX/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EX/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
