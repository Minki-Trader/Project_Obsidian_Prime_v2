# run364GT Cost-Near Density Lift Router(비용 근접 밀도 상승 라우터)

Created(생성): 2026-06-07T13:57:29Z

Action(행동): GS failure memory(GS 실패 기억)를 받아 combined cost0.9(합산 비용0.9) 보존과 OOS cost0.6/OOS density(표본외 비용0.6/표본외 밀도) 상승을 함께 점수화해 학습했습니다.

Effect(효과): GR의 비용 수리 단서를 잃지 않으면서 표본외 비용과 밀도를 같이 올릴 수 있는지 확인합니다.

- judgment(판정): `inconclusive_cost_near_density_lift_router_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `gt_cost_h2_m0p30__gt_gr_cost_anchor__rf8_l20_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `104.77` / `1.1681385679` / `1.4207650273`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `27.488` / `1.0714233747` / `1.4427480916`
- OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `-29.212` / `-85.912`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `132.258` / `1.4299363057` / `-137.142` / `0.7416481069`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364GU_review_h17_oos108_pf125_cost_near_density_lift_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GT/gt_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GT/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GT/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GT/gt_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GT/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GT/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GT/gt_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GT/selected_gt_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GT/gt_gu_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GT/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GT/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GT/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
