# run364EF H17 Validation Source Rotation Density Recovery(검증 원천 회전 밀도 회복)

Created(생성): 2026-06-06T13:40:53Z

Action(행동): EE failure memory(EE 실패 기억)를 받아 feature source rotation(피처 원천 회전)과 density-first selection(밀도 우선 선택)을 실행했습니다.

Effect(효과): direct min_pf sparse grid(직접 최소 PF 희소 격자) 반복을 피하고, 검증 PF 회복과 표본외 밀도 보존을 같이 판정합니다.

Selected(선택): `source_rotate_dir_h2_m1p5__source_all82(원천전체_82)__et6_l70_n160(엑스트라트리6_잎70_160)`

- selection_pool(선택 풀): `density_net`
- validation net/PF/density(검증 순수익/PF/밀도): `73.985` / `1.0474042816` / `3.2950819672`
- OOS net/PF/density(표본외 순수익/PF/밀도): `80.357` / `1.0769378806` / `3.4122137405`
- min_pf(최소 PF): `1.0474042816`
- pf108_count(PF 1.08 양쪽 통과 수): `0`
- pf110_count(PF 1.10 양쪽 통과 수): `0`
- strict_candidate_count(엄격 후보 수): `0`

Judgment(판정): `inconclusive_validation_source_rotation_density_recovery_no_pf_bridge_candidate_no_package_no_authority`

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

Next(다음): `run364EG_review_h17_validation_source_rotation_density_recovery_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EF/ef_validation_source_rotation_trade_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EF/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EF/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EF/ef_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EF/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EF/onnx_smoke_report.csv
- candidate_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EF/ef_validation_source_rotation_trade_surface.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EF/run364EG_validation_source_rotation_density_recovery_review_queue.csv
- no_trade_splitting_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EF/selected_ef_trade_tape.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EF/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EF/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364EF/claim_boundary_receipt.json
