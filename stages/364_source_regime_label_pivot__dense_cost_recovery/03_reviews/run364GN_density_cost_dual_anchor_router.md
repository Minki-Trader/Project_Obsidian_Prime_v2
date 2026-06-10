# run364GN Density-Cost Dual-Anchor Router(밀도-비용 이중 앵커 라우터)

Created(생성): 2026-06-07T12:23:48Z

Action(행동): GJ cost anchor(GJ 비용 앵커)와 GL density anchor(GL 밀도 앵커)를 같은 점수로 뭉개지 않고, label(라벨), filter(필터), score(점수)를 분리해 학습했습니다.

Effect(효과): sparse cost-only(희소 비용 전용)와 dense cost-collapse(고밀도 비용 붕괴) 사이의 왕복을 줄일 수 있는지 확인합니다.

- judgment(판정): `inconclusive_density_cost_dual_anchor_router_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `gn_density_h1_m0p40__gn_gl_density_anchor__et7_l12_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `26.363` / `999.0` / `0.0218579235`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `21.938` / `999.0` / `0.0229007634`
- OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `21.038` / `20.138`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `48.301` / `0.0222929936` / `44.101` / `1.0`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364GO_review_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GN/gn_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GN/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GN/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GN/gn_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GN/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GN/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GN/gn_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GN/selected_gn_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GN/gn_go_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GN/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GN/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GN/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
