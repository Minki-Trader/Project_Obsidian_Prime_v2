# run364GL Cost-Repaired Density Reexpand(비용 수리 후 밀도 재확장)

Created(생성): 2026-06-07T11:50:48Z

Action(행동): GK failure memory(GK 실패 기억)를 받아 h1 density supply(h1 밀도 공급)를 GJ cost repair(GJ 비용 수리) 조건 아래 다시 넓혔습니다.

Effect(효과): 희소 h2 cost-only recovery(희소 h2 비용 전용 회복)를 피하면서 combined density(합산 밀도)를 다시 올릴 수 있는지 확인합니다.

- judgment(판정): `inconclusive_cost_repaired_density_reexpand_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `gl_sym_h1_m0p40__gl_density_cost_blend__rf8_l18_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `26.532` / `1.0317575833` / `2.5901639344`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `11.528` / `1.0218949128` / `2.3053435115`
- OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `-79.072` / `-169.672`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `38.06` / `2.4713375796` / `-427.54` / `0.7164948454`
- strict_candidate_count(엄격 후보 수): `0`
- next_run_id(다음 실행 ID): `run364GM_review_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GL/gl_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GL/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GL/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GL/gl_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GL/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GL/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GL/gl_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GL/selected_gl_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GL/gl_gm_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GL/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GL/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GL/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
