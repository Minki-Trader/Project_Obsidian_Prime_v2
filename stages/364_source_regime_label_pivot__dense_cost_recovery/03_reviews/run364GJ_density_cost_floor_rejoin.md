# run364GJ Density-Cost Floor Rejoin(밀도-비용 바닥 재결합)

Created(생성): 2026-06-07T11:19:15Z

Action(행동): GI failure memory(GI 실패 기억)를 받아 GH density supply(GH 밀도 공급)에 cost floor(비용 바닥)와 validation floor(검증 바닥)를 다시 붙이는 모델 표면을 학습했습니다.

Effect(효과): density-only cost collapse(밀도 전용 비용 붕괴)를 피하면서, OOS cost0.6(표본외 비용0.6)과 combined cost0.9(합산 비용0.9)가 회복되는지 확인합니다.

- judgment(판정): `inconclusive_density_cost_floor_rejoin_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `gj_sym_h2_m0p35__gj_session_regime_cost__et7_l12_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `204.302` / `1.2407271468` / `1.7049180328`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `85.724` / `1.177054977` / `1.5419847328`
- OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `25.124` / `-35.476`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `290.026` / `1.6369426752` / `-18.374` / `0.766536965`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364GK_review_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GJ/gj_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GJ/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GJ/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GJ/gj_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GJ/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GJ/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GJ/gj_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GJ/selected_gj_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GJ/gj_gk_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GJ/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GJ/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GJ/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
