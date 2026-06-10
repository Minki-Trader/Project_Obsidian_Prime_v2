# run364FN Density Cost Decoupled Bridge(밀도 비용 분리 연결)

Created(생성): 2026-06-07T04:50:34Z

Action(행동): FM failure memory(FM 실패 기억)를 받아 density leg(밀도 다리), cost leg(비용 다리), overlap score(겹침 점수)를 학습했습니다.

Effect(효과): density3(밀도3)와 OOS PF/cost(표본외 수익 팩터/비용)가 한쪽씩 번갈아 깨지는 왕복 실패를 줄이는지 확인합니다.

- judgment(판정): `inconclusive_density_cost_decoupled_bridge_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `fn_sym_h2_m1p25__fn_cost_leg__rf9_l18_n192`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `136.115` / `1.1130419978` / `2.8743169399`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `-40.679` / `0.9500226673` / `2.7938931298`
- OOS cost0.6 net(표본외 비용0.6 순수익): `-150.479`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `95.436` / `2.8407643312` / `-439.764` / `0.730941704`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364FO_review_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FN/fn_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FN/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FN/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FN/fn_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FN/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FN/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FN/fn_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FN/selected_fn_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FN/fn_fo_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FN/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FN/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FN/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
