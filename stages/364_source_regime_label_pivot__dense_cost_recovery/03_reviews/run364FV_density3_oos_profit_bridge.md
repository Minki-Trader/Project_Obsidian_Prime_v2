# run364FV Density3 OOS Profit Bridge(밀도3 표본외 수익 연결)

Created(생성): 2026-06-07T07:08:28Z

Action(행동): FU failure memory(FU 실패 기억)를 받아 density3 floor(밀도3 바닥), OOS profit bridge score(표본외 수익 연결 점수), soft OOS filters(완화 표본외 필터)를 학습했습니다.

Effect(효과): FT의 거래 밀도 회복을 유지하면서 OOS net/PF(표본외 순수익/수익 팩터)를 다시 양수 쪽으로 연결했는지 확인합니다.

- judgment(판정): `inconclusive_density3_oos_profit_bridge_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `fv_sym_h1_m0p75__fv_all72__rf8_l24_n144`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `31.787` / `1.0383962641` / `2.3551912568`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `34.163` / `1.0632477145` / `2.2671755725`
- OOS cost0.6 net(표본외 비용0.6 순수익): `-54.937`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `65.95` / `2.3184713376` / `-370.85` / `0.8104395604`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364FW_review_h17_oos108_pf125_density3_oos_profit_bridge_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FV/fv_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FV/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FV/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FV/fv_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FV/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FV/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FV/fv_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FV/selected_fv_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FV/fv_fw_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FV/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FV/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FV/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
