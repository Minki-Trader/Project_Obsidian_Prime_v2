# run364FT Regime Profit Density Reexpand(국면 수익 밀도 재확장)

Created(생성): 2026-06-07T06:37:12Z

Action(행동): FS failure memory(FS 실패 기억)를 받아 broad hour/filter(넓은 시간/필터), lower label barrier(낮은 라벨 장벽), density reexpand score(밀도 재확장 점수)를 학습했습니다.

Effect(효과): FR profit salvage(FR 수익 회수)를 버리지 않고 validation/OOS/combined density(검증/표본외/합산 밀도)를 3/day(일 3회) 쪽으로 다시 넓혔는지 확인합니다.

- judgment(판정): `inconclusive_regime_profit_density_reexpand_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `ft_sym_h1_m0p75__ft_session_regime_broad__rf8_l24_n176`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `100.978` / `1.0922701014` / `3.3715846995`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `-79.583` / `0.8976134726` / `3.106870229`
- OOS cost0.6 net(표본외 비용0.6 순수익): `-201.683`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `21.395` / `3.2611464968` / `-593.005` / `0.7490234375`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364FU_review_h17_oos108_pf125_regime_profit_density_reexpand_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FT/ft_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FT/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FT/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FT/ft_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FT/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FT/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FT/ft_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FT/selected_ft_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FT/ft_fu_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FT/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FT/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364FT/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
