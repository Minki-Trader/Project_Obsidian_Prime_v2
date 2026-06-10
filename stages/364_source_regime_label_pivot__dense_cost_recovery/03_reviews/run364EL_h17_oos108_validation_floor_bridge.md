# run364EL H17 OOS108 Validation Floor Bridge(표본외108 검증 바닥 연결)

Created(생성): 2026-06-06T15:02:12Z

Action(행동): EK failure memory(EK 실패 기억)를 받아 density>=3 and OOS PF>=1.08(밀도 3 이상 및 표본외 PF 1.08 이상) 후보의 validation PF floor(검증 PF 바닥)를 수리하는 모델 탐색을 실행했습니다.

Effect(효과): EJ의 가까운 실패 경계를 bridge(연결) 후보로 바꿀 수 있는지 확인합니다.

Selected(선택): `oos108_valfloor_dir_h2_m1__source_all82__rf8_l70_n160`

- selection_pool(선택 풀): `pf108`
- validation net/PF/density(검증 순수익/PF/밀도): `202.78` / `1.1329169764` / `3.9344262295`
- OOS net/PF/density(표본외 순수익/PF/밀도): `201.155` / `1.1960498616` / `3.9618320611`
- min_pf(최소 PF): `1.1329169764`
- bridge_count(연결 후보 수): `322`
- pf108_count(PF 1.08 양쪽 통과 수): `84`
- oos108_count(표본외 PF 1.08 후보 수): `714`
- val104_count(검증 PF 1.04 후보 수): `504`

Judgment(판정): `proxy_oos108_validation_floor_bridge_pf108_candidate_review_required_no_authority`

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

Next(다음): `run364EM_review_h17_oos108_validation_floor_bridge_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/el_oos108_validation_floor_bridge_trade_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/el_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/onnx_smoke_report.csv
- candidate_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/el_oos108_validation_floor_bridge_trade_surface.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/run364EM_oos108_validation_floor_bridge_review_queue.csv
- no_trade_splitting_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/selected_el_trade_tape.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EL/claim_boundary_receipt.json
