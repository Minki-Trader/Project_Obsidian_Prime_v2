# run364EH H17 OOS PF108 Bridge Density Preserve(표본외 PF108 연결 밀도 보존)

Created(생성): 2026-06-06T13:58:24Z

Action(행동): EG failure memory(EG 실패 기억)를 받아 OOS PF 1.08(표본외 PF 1.08)을 직접 보상하고 density>=3(밀도 3 이상)과 validation PF floor(검증 PF 바닥)를 보존하는 탐색을 실행했습니다.

Effect(효과): EF의 full-source h2 clue(전체 원천 h2 단서)가 package(패키지) 후보로 가까워질 수 있는지 확인합니다.

Selected(선택): `oos_pf108_dir_h2_m1p5__source_all82(원천전체_82)__et8_l90_n160(엑스트라트리8_잎90_160)`

- selection_pool(선택 풀): `exportable`
- validation net/PF/density(검증 순수익/PF/밀도): `89.569` / `1.0646379958` / `2.9344262295`
- OOS net/PF/density(표본외 순수익/PF/밀도): `208.907` / `1.2623046122` / `2.8320610687`
- min_pf(최소 PF): `1.0646379958`
- oos108_count(표본외 PF 1.08 후보 수): `0`
- pf108_count(PF 1.08 양쪽 통과 수): `0`
- pf110_count(PF 1.10 양쪽 통과 수): `0`
- strict_candidate_count(엄격 후보 수): `0`

Judgment(판정): `inconclusive_oos_pf108_bridge_density_preserve_no_pf108_candidate_no_package_no_authority`

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

Next(다음): `run364EI_review_h17_oos_pf108_bridge_density_preserve_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EH/eh_oos_pf108_bridge_trade_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EH/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EH/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EH/eh_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EH/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EH/onnx_smoke_report.csv
- candidate_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EH/eh_oos_pf108_bridge_trade_surface.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EH/run364EI_oos_pf108_bridge_density_preserve_review_queue.csv
- no_trade_splitting_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EH/selected_eh_trade_tape.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EH/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EH/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EH/claim_boundary_receipt.json
