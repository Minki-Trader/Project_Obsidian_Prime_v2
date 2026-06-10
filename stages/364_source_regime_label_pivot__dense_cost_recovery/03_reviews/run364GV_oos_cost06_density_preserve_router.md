# run364GV OOS Cost0.6 Density Preserve Router(표본외 비용0.6 밀도 보존 라우터)

Created(생성): 2026-06-07T14:35:25Z

Action(행동): GU failure memory(GU 실패 기억)를 받아 OOS cost0.6(표본외 비용0.6) 수리와 OOS density(표본외 밀도) 보존을 동시에 점수화해 학습했습니다.

Effect(효과): GT의 density clue(밀도 단서)를 유지할 수 있는지 보면서, 비용 실패가 줄어드는 frontier(경계면)를 다음 GW review(GW 검토)로 넘깁니다.

- judgment(판정): `inconclusive_oos_cost06_density_preserve_router_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `gv_cost_h2_m0p32__gv_cost_side_behavior_anchor__rf9_l22_n144`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `134.731` / `1.2991330025` / `1.3551912568`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `37.85` / `1.1052444257` / `1.2900763359`
- OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `-12.85` / `-63.55`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `172.581` / `1.3280254777` / `-77.619` / `0.7961630695`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364GW_review_h17_oos108_pf125_oos_cost06_density_preserve_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GV/gv_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GV/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GV/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GV/gv_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GV/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GV/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GV/gv_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GV/selected_gv_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GV/gv_gw_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GV/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GV/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GV/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
