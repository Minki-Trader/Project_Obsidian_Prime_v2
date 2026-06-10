# run364FP Positive Density Floor Reseed(양수 밀도 바닥 재시드)

Created(생성): 2026-06-07T05:26:18Z

Action(행동): FO failure memory(FO 실패 기억)를 받아 positive density floor score(양수 밀도 바닥 점수), broad density labels(넓은 밀도 라벨), cost scout guard(비용 탐색 가드)를 학습했습니다.

Effect(효과): OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9) 단서를 저밀도 package(패키지)로 올리지 않고, validation positive density3(검증 양수 밀도3)부터 복구했는지 확인합니다.

- judgment(판정): `inconclusive_positive_density_floor_reseed_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `fp_sym_h2_m1p75__fp_validation_stability__rf8_l22_n176`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `22.075` / `1.0171796969` / `2.7704918033`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `-61.734` / `0.9244281986` / `2.7633587786`
- OOS cost0.6 net(표본외 비용0.6 순수익): `-170.334`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `-39.659` / `2.7675159236` / `-561.059` / `0.7583429229`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364FQ_review_h17_oos108_pf125_positive_density_floor_reseed_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FP/fp_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FP/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FP/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FP/fp_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FP/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FP/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FP/fp_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FP/selected_fp_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FP/fp_fq_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FP/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FP/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FP/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
