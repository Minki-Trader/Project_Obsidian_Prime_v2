# run364FL Dual Density OOS Cost Bridge(양쪽 밀도 표본외 비용 연결)

Created(생성): 2026-06-07T04:29:38Z

Action(행동): FK failure memory(FK 실패 기억)를 받아 hard density floor score(강제 밀도 바닥 점수), OOS cost bridge(표본외 비용 연결), balanced density labels(균형 밀도 라벨)를 학습했습니다.

Effect(효과): FJ의 OOS PF/cost(표본외 수익 팩터/비용) 회수 단서를 버리지 않고 validation/OOS/combined density(검증/표본외/합산 밀도)를 3/day(일 3회)로 올릴 수 있는지 확인합니다.

- judgment(판정): `inconclusive_dual_density_oos_cost_bridge_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `fl_sym_h2_m1p75__fl_oos_cost_session_macro__rf8_l24_n160`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `102.566` / `1.0778107449` / `3.0218579235`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `43.189` / `1.0477871778` / `3.0763358779`
- OOS cost0.6 net(표본외 비용0.6 순수익): `-77.711`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `145.755` / `3.0445859873` / `-427.845` / `0.6809623431`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364FM_review_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FL/fl_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FL/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FL/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FL/fl_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FL/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FL/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FL/fl_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FL/selected_fl_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FL/fl_fm_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FL/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FL/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FL/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
