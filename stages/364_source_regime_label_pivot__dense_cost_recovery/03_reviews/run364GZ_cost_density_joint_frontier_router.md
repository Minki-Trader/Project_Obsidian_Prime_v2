# run364GZ Cost-Density Joint Frontier Router(비용-밀도 공동 경계 라우터)

Created(생성): 2026-06-07T15:31:13Z

Action(행동): GY failure memory(GY 실패 기억)를 받아 OOS profit/cost0.6(표본외 수익/비용0.6), OOS/combined density(표본외/합산 밀도), combined cost0.9(합산 비용0.9)를 같은 frontier score(경계 점수)에 묶어 학습했습니다.

Effect(효과): 수익만 좋은 후보와 밀도만 좋은 후보를 분리하고, HA review(HA 검토)가 공동 경계 통과 여부를 판정하게 합니다.

- judgment(판정): `inconclusive_cost_density_joint_frontier_router_no_strict_pass_review_required_no_authority`
- selected_model_id(선택 모델 ID): `gz_cost_h2_m0p32__gz_joint_frontier_blend__rf9_l20_n176`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `114.309` / `1.2644297165` / `1.2513661202`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `45.36` / `1.1193919853` / `1.3816793893`
- OOS cost0.6/cost0.9 net(표본외 비용0.6/비용0.9 순수익): `-8.94` / `-63.24`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `159.669` / `1.3057324841` / `-86.331` / `0.8170731707`
- strict_candidate_count(엄격 후보 수): `0`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `0`
- next_run_id(다음 실행 ID): `run364HA_review_h17_oos108_pf125_cost_density_joint_frontier_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GZ/gz_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GZ/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GZ/data_integrity_audit.csv
- training_split_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GZ/gz_model_scorecard.csv
- model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GZ/model_artifact_manifest.csv
- onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GZ/onnx_smoke_report.csv
- density_cost_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GZ/gz_surface.csv
- full_trade_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GZ/selected_gz_trade_tape.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GZ/gz_ha_queue.csv
- paired_tier_record_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/stage_run_ledger.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GZ/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GZ/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364GZ/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
