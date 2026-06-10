# run364GB Session Side Loss Veto Rescue(세션 방향 손실 차단 회수)

Created(생성): 2026-06-07T08:52:32Z

Action(행동): GA failure memory(GA 실패 기억)를 받아 FZ loss clusters(FZ 손실 군집)를 session/side veto(세션/방향 차단) 필터로 학습했습니다.

Effect(효과): 16-17 long loss(16-17시 롱 손실)와 20 short loss(20시 숏 손실)를 줄이면서 OOS profit(표본외 수익)과 near density(근접 밀도)를 회복할 수 있는지 확인합니다.

- judgment(판정): `inconclusive_session_side_loss_veto_rescue_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `gb_sym_h1_m0p60__gb_oos_profit_regime__rf8_l20_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `49.565` / `1.0554349516` / `2.5464480874`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `60.74` / `1.1268140527` / `2.106870229`
- OOS cost0.6 net(표본외 비용0.6 순수익): `-22.06`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `110.305` / `2.3630573248` / `-334.895` / `0.8477088949`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364GC_review_h17_oos108_pf125_session_side_loss_veto_rescue_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GB/gb_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GB/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GB/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GB/gb_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GB/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GB/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GB/gb_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GB/selected_gb_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GB/gb_gc_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GB/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GB/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GB/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
