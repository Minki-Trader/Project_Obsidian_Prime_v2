# run364EZ H17 OOS108 OOS PF125 Cost09 Gap Repair(표본외 PF 1.25 비용0.9 간격 수리)

Created(생성): 2026-06-07T01:47:58Z

Action(행동): EY failure memory(EY 실패 기억)를 받아 PF quality guard(PF 품질 가드), cost09 trim score(비용0.9 절단 점수), higher movement labels(더 큰 이동 라벨)을 학습했습니다.

Effect(효과): EX의 OOS net/cost0.6/density/short share(표본외 순수익/비용0.6/밀도/숏 비중) 단서를 보존하면서 PF 1.25(수익 팩터 1.25)와 cost0.9(비용0.9) 병목을 좁힙니다.

- judgment(판정): `inconclusive_oos_pf125_cost09_gap_repair_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `ez_sym_h3_m3p5__ez_all72__et9_l32_n112`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `-61.362` / `0.9592346245` / `2.7049180328`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `272.44` / `1.2934574205` / `2.9770992366`
- OOS cost0.6 net(표본외 비용0.6 순수익): `155.44`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `211.078` / `2.8184713376` / `-319.922` / `0.7898305085`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영형 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364FA_review_h17_oos108_oos_pf125_cost09_gap_repair_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EZ/ez_oos_pf125_cost09_gap_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EZ/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EZ/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EZ/ez_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EZ/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EZ/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EZ/ez_oos_pf125_cost09_gap_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EZ/selected_ez_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EZ/run364FA_oos_pf125_cost09_gap_review_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EZ/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EZ/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EZ/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
