# run364EV H17 OOS108 Cost09/Density Edge Recovery(비용0.9/밀도 엣지 회복)

Created(생성): 2026-06-06T23:14:23Z

Action(행동): EU review(EU 검토)의 실패 기억을 받아 cost0.9(비용0.9), validation density(검증 밀도), full-tape density(전체 테이프 밀도)를 더 세게 반영한 model/label/score(모델/라벨/점수)를 학습했습니다.

Effect(효과): ET의 OOS PF(표본외 수익 팩터) 단서를 보존하면서 검증 비용 압박과 밀도 3/day(일 3회) 간극을 직접 시험했습니다.

- judgment(판정): `inconclusive_cost09_density_edge_recovery_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `ev_asym_h2_l2_s3__ev_all72__rf8_l44_n96`
- validation net/PF/density(검증 순수익/PF/밀도): `316.706` / `1.3118378986` / `2.6721311475`
- OOS net/PF/density(표본외 순수익/PF/밀도): `-17.382` / `0.9763940571` / `2.5267175573`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `299.324` / `2.6114649682` / `-192.676` / `0.8219512195`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영형 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364EW_review_h17_oos108_cost09_density_edge_recovery_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EV/ev_cost09_density_edge_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EV/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EV/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EV/ev_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EV/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EV/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EV/ev_cost09_density_edge_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EV/selected_ev_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EV/run364EW_cost09_density_edge_review_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EV/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EV/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EV/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
