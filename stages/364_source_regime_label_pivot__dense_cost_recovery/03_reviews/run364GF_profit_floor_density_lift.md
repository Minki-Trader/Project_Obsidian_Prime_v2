# run364GF Profit-Floor Density Lift(수익 바닥 밀도 상승)

Created(생성): 2026-06-07T10:05:31Z

Action(행동): GE failure memory(GE 실패 기억)를 받아 GD OOS profit floor(GD 표본외 수익 바닥)를 보존 조건으로 두고 threshold/density target(임계값/밀도 목표)을 다시 학습했습니다.

Effect(효과): OOS net/PF/cost0.6(표본외 순수익/수익 팩터/비용0.6)을 무너뜨리지 않으면서 validation net(검증 순수익)과 density(밀도)가 올라가는지 확인합니다.

- judgment(판정): `inconclusive_profit_floor_density_lift_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `gf_sym_h1_m0p50__gf_profit_density_blend__rf8_l18_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `78.008` / `1.101326856` / `2.2568306011`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `83.438` / `1.2040677568` / `1.9694656489`
- OOS cost0.6 net(표본외 비용0.6 순수익): `6.038`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `161.446` / `2.1369426752` / `-241.154` / `0.7615499255`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364GG_review_h17_oos108_pf125_profit_floor_density_lift_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GF/gf_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GF/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GF/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GF/gf_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GF/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GF/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GF/gf_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GF/selected_gf_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GF/gf_gg_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GF/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GF/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GF/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
