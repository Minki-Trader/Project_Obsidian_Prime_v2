# run364FR Density3 Regime Split Repair(밀도3 국면 분할 수리)

Created(생성): 2026-06-07T05:55:17Z

Action(행동): FQ failure memory(FQ 실패 기억)를 받아 regime/session/side split(국면/세션/방향 분할), density3 score(밀도3 점수), cost scout guard(비용 탐색 가드)를 학습했습니다.

Effect(효과): FP의 dense losing rows(고밀도 손실 행)가 섞임 문제인지 확인하고, validation positive density3(검증 양수 밀도3)를 되살릴 수 있는 하위 국면을 찾습니다.

- judgment(판정): `inconclusive_density3_regime_split_repair_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `fr_sym_h2_m1p5__fr_regime_macro__rf8_l20_n160`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `188.314` / `1.1749938204` / `2.393442623`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `-6.562` / `0.9901955218` / `2.2824427481`
- OOS cost0.6 net(표본외 비용0.6 순수익): `-96.262`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `181.752` / `2.347133758` / `-260.448` / `0.7598371777`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364FS_review_h17_oos108_pf125_density3_regime_split_repair_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FR/fr_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FR/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FR/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FR/fr_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FR/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FR/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FR/fr_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FR/selected_fr_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FR/fr_fs_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FR/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FR/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FR/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
