# run364FX Profit Density Dual Anchor Rejoin(수익 밀도 이중 앵커 재결합)

Created(생성): 2026-06-07T07:44:56Z

Action(행동): FW failure memory(FW 실패 기억)를 받아 FT density anchor(FT 밀도 앵커)와 FV OOS profit anchor(FV 표본외 수익 앵커)를 같은 선택 점수로 학습했습니다.

Effect(효과): density-only(밀도 전용) 실패와 low-density profit-only(저밀도 수익 전용) 실패를 동시에 피할 수 있는지 확인합니다.

- judgment(판정): `inconclusive_profit_density_dual_anchor_rejoin_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `fx_sym_h1_m0p75__fx_profit_density_dual__et8_l18_n132`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `0.474` / `1.0004002915` / `3.0601092896`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `-77.441` / `0.8928911277` / `2.8396946565`
- OOS cost0.6 net(표본외 비용0.6 순수익): `-189.041`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `-76.967` / `2.9681528662` / `-636.167` / `0.7693133047`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364FY_review_h17_oos108_pf125_profit_density_dual_anchor_rejoin_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FX/fx_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FX/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FX/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FX/fx_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FX/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FX/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FX/fx_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FX/selected_fx_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FX/fx_fy_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FX/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FX/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FX/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
