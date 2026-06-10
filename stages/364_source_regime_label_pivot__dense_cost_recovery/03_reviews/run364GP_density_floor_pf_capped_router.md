# run364GP Density-Floor PF-Capped Router(밀도 바닥 PF 캡 라우터)

Created(생성): 2026-06-07T12:51:17Z

Action(행동): GN dual-anchor router(GN 이중 앵커 라우터)에 PF cap(PF 캡)과 hard density/trade floor(하드 밀도/거래수 바닥)를 추가해 학습했습니다.

Effect(효과): PF999 micro-sample(PF999 초소형 표본)이 선택되는 실패를 막고, 실제 거래 밀도가 있는 density-cost frontier(밀도-비용 경계)를 다시 확인합니다.

- judgment(판정): `inconclusive_density_floor_pf_capped_router_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `gp_density_h1_m0p40__gp_gl_density_anchor__rf8_l20_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `2.281` / `1.0041761871` / `1.8961748634`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `51.657` / `1.1302092392` / `1.6870229008`
- OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `-14.643` / `-80.943`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `53.938` / `1.8089171975` / `-286.862` / `0.8538732394`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364GQ_review_h17_oos108_pf125_density_floor_pf_capped_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GP/gp_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GP/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GP/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GP/gp_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GP/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GP/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GP/gp_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GP/selected_gp_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GP/gp_gq_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GP/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GP/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GP/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
