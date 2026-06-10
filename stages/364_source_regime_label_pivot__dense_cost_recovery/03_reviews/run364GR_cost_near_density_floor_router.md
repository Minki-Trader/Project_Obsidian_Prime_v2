# run364GR Cost-Near Density Floor Router(비용 근접 밀도 바닥 라우터)

Created(생성): 2026-06-07T13:30:03Z

Action(행동): GQ failure memory(GQ 실패 기억)를 받아 cost-near first selection(비용 근접 우선 선택)과 hard density/trade floor(하드 밀도/거래수 바닥)를 결합해 학습했습니다.

Effect(효과): GP가 고친 PF999 sparse selector(PF999 희소 선택기) 문제를 되돌리지 않으면서, combined cost0.9(합산 비용0.9) 붕괴를 줄일 수 있는지 봅니다.

- judgment(판정): `inconclusive_cost_near_density_floor_router_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `gr_cost_h2_m0p35__gr_gp_density_anchor__rf8_l20_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `108.256` / `1.1812152551` / `1.3551912568`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `21.891` / `1.0732395214` / `1.1374045802`
- OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `-22.809` / `-67.509`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `130.147` / `1.2643312102` / `-108.053` / `0.8513853904`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364GS_review_h17_oos108_pf125_cost_near_density_floor_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GR/gr_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GR/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GR/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GR/gr_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GR/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GR/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GR/gr_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GR/selected_gr_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GR/gr_gs_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GR/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GR/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GR/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
