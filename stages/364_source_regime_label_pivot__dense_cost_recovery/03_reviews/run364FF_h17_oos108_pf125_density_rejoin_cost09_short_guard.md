# run364FF H17 OOS108 PF125 Density Rejoin Cost09 Short Guard(PF125 밀도 재결합 비용0.9 숏 가드)

Created(생성): 2026-06-07T03:24:09Z

Action(행동): FE failure memory(FE 실패 기억)를 받아 density rejoin score(밀도 재결합 점수), cost09 short guard(비용0.9 숏 가드), long bridge pressure(롱 연결 압력)를 학습했습니다.

Effect(효과): FD의 OOS PF/cost0.9(표본외 수익 팩터/비용0.9) 단서를 버리지 않고 validation/combined density(검증/합산 밀도) 재손실을 수리할 수 있는지 확인합니다.

- judgment(판정): `inconclusive_pf125_density_rejoin_cost09_short_guard_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `ff_sym_h2_m2p25__ff_all72__et8_l24_n128`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `208.962` / `1.1922187829` / `2.3551912568`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `215.966` / `1.3184287197` / `2.358778626`
- OOS cost0.6 net(표본외 비용0.6 순수익): `123.266`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `424.928` / `2.3566878981` / `-19.072` / `0.672972973`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364FG_review_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FF/ff_pf125_density_rejoin_cost09_short_guard_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FF/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FF/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FF/ff_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FF/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FF/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FF/ff_pf125_density_rejoin_cost09_short_guard_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FF/selected_ff_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FF/ff_fg_review_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FF/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FF/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FF/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
