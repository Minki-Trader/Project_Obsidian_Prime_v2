# run364EJ H17 Density Floor OOS PF Salvage(밀도 바닥 표본외 PF 회수)

Created(생성): 2026-06-06T14:27:53Z

Action(행동): EI failure memory(EI 실패 기억)를 받아 EH high OOS PF clue(EH 높은 표본외 PF 단서)를 density>=3/day(밀도 일 3회 이상) 조건 안으로 되돌리는 모델 탐색을 실행했습니다.

Effect(효과): sparse high PF(희소 고PF)를 package(패키지)로 오해하지 않고, density floor(밀도 바닥) 회복 여부를 분리해 봅니다.

Selected(선택): `density_salvage_dir_h2_m1__source_all82__et7_l70_n192`

- selection_pool(선택 풀): `density_net`
- validation net/PF/density(검증 순수익/PF/밀도): `241.321` / `1.175471598` / `3.2896174863`
- OOS net/PF/density(표본외 순수익/PF/밀도): `18.508` / `1.0183147066` / `3.4122137405`
- min_pf(최소 PF): `1.0183147066`
- density_net_count(밀도+순수익 후보 수): `210`
- oos112_count(표본외 PF 1.12 후보 수): `0`
- pf108_count(PF 1.08 양쪽 통과 수): `0`
- pf110_count(PF 1.10 양쪽 통과 수): `0`
- near_density_oos108_count(근접 밀도 표본외 PF 1.08 후보 수): `165`

Judgment(판정): `inconclusive_density_floor_oos_pf_salvage_no_oos112_density_candidate_no_package_no_authority`

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

Next(다음): `run364EK_review_h17_density_floor_oos_pf_salvage_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EJ/ej_density_floor_oos_pf_salvage_trade_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EJ/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EJ/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EJ/ej_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EJ/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EJ/onnx_smoke_report.csv
- candidate_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EJ/ej_density_floor_oos_pf_salvage_trade_surface.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EJ/run364EK_density_floor_oos_pf_salvage_review_queue.csv
- no_trade_splitting_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EJ/selected_ej_trade_tape.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EJ/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EJ/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EJ/claim_boundary_receipt.json
