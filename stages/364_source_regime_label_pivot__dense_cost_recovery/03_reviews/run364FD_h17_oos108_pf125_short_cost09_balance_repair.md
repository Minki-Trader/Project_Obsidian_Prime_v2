# run364FD H17 OOS108 PF125 Short/Cost09 Balance Repair(PF125 숏/비용0.9 균형 수리)

Created(생성): 2026-06-07T02:42:35Z

Action(행동): FC failure memory(FC 실패 기억)를 받아 short/cost09 balance score(숏/비용0.9 균형 점수), short veto(숏 차단), long bridge(롱 연결)를 학습했습니다.

Effect(효과): FB의 validation/density recovery(검증/밀도 회복)를 보존하면서 OOS PF/cost0.9/short share(표본외 PF/비용0.9/숏 비중) 간격을 좁힙니다.

- judgment(판정): `inconclusive_pf125_short_cost09_balance_repair_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `fd_sym_h3_m3__fd_session_macro_stack__et9_l36_n128`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `37.05` / `1.0253007408` / `2.6830601093`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `296.62` / `1.2980245899` / `3.0610687023`
- OOS cost0.6 net(표본외 비용0.6 순수익): `176.32`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `333.67` / `2.8407643312` / `-201.53` / `0.7668161435`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영형 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364FE_review_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FD/fd_pf125_short_cost09_balance_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FD/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FD/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FD/fd_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FD/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FD/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FD/fd_pf125_short_cost09_balance_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FD/selected_fd_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FD/run364FE_pf125_short_cost09_balance_review_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FD/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FD/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FD/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
