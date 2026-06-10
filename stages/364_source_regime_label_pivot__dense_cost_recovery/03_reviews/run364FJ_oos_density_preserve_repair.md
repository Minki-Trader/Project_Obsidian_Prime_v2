# run364FJ OOS Density Preserve Repair(표본외 밀도 보존 수리)

Created(생성): 2026-06-07T04:09:47Z

Action(행동): FI failure memory(FI 실패 기억)를 받아 OOS PF/cost score(표본외 수익 팩터/비용 점수), dual density guard(양쪽 밀도 가드), short balance guard(숏 균형 가드)를 학습했습니다.

Effect(효과): FH가 만든 validation-positive density3(검증 양수 밀도3) 단서를 버리지 않고 OOS PF/cost(표본외 수익 팩터/비용)를 회복할 수 있는지 확인합니다.

- judgment(판정): `inconclusive_oos_density_preserve_repair_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `fj_sym_h2_m1p75__fj_behavior_density_cost__et8_l18_n160`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `116.181` / `1.1134556811` / `2.131147541`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `333.32` / `1.4709758917` / `2.5496183206`
- OOS cost0.6 net(표본외 비용0.6 순수익): `233.12`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `449.501` / `2.3057324841` / `15.101` / `0.5483425414`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364FK_review_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/fj_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/fj_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/fj_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/selected_fj_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/fj_fk_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FJ/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
