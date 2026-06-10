# run364GX Density Recover Cost0.6 Hold Router(밀도 회복 비용0.6 유지 라우터)

Created(생성): 2026-06-07T15:01:40Z

Action(행동): GW failure memory(GW 실패 기억)를 받아 OOS cost0.6(표본외 비용0.6)과 combined cost0.9(합산 비용0.9)을 지키면서 OOS/combined density(표본외/합산 밀도)를 회복하는 score(점수)를 학습했습니다.

Effect(효과): GV의 cost repair(비용 수리) 단서가 density recovery(밀도 회복)와 같이 유지되는지 GY review(GY 검토)로 넘깁니다.

- judgment(판정): `inconclusive_density_recover_cost06_hold_router_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `gx_cost_h2_m0p30__gx_cost_hold_behavior_anchor__rf9_l22_n160`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `33.93` / `1.0763346757` / `1.2950819672`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `78.765` / `1.2405860936` / `1.3053435115`
- OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `27.465` / `-23.835`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `112.695` / `1.2993630573` / `-132.105` / `0.8946078431`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364GY_review_h17_oos108_pf125_density_recover_cost06_hold_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GX/gx_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GX/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GX/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GX/gx_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GX/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GX/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GX/gx_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GX/selected_gx_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GX/gx_gy_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GX/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GX/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GX/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
