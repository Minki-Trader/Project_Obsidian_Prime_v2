# run364FB H17 OOS108 PF125 Density Bridge Repair(PF125 밀도 연결 수리)

Created(생성): 2026-06-07T02:22:02Z

Action(행동): FA failure memory(FA 실패 기억)를 받아 two-lane threshold stack(두 갈래 임계값 묶음), density bridge score(밀도 연결 점수), side/session veto(방향/세션 차단)를 학습했습니다.

Effect(효과): EZ의 OOS PF125/OOS cost0.9(표본외 PF125/표본외 비용0.9) 단서를 버리지 않고 validation/density(검증/밀도) 붕괴를 수리합니다.

- judgment(판정): `inconclusive_pf125_density_bridge_repair_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `fb_asym_h3_l2p5_s3p5__fb_all72__et8_l24_n128`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `119.219` / `1.0670692053` / `3.3661202186`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `277.934` / `1.2359191573` / `3.6870229008`
- OOS cost0.6 net(표본외 비용0.6 순수익): `133.034`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `397.153` / `3.5` / `-262.247` / `0.8771610555`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영형 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364FC_review_h17_oos108_pf125_density_bridge_repair_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FB/fb_pf125_density_bridge_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FB/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FB/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FB/fb_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FB/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FB/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FB/fb_pf125_density_bridge_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FB/selected_fb_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FB/run364FC_pf125_density_bridge_review_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FB/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FB/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FB/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
