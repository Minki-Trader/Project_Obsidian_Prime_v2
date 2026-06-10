# run364HE Dual-Surface Router Review(이중 표면 라우터 검토)

Created(생성): 2026-06-08T10:58:05Z

Action(행동): HD dual-surface router(HD 이중 표면 라우터)를 GZ/HB 기준과 비교하고, package(패키지) 가능성, positive clue(긍정 단서), next seed(다음 씨앗)를 분리했습니다.

Effect(효과): 좋아진 프록시(proxy, 프록시)를 운영 후보로 과장하지 않고, HF near-miss lift(HF 근접 실패 리프트)로 이어갑니다.

- judgment(판정): `positive_clue_no_package_hd_near_miss_improved_oos_profit_cost_density_missed_net_pf_targets_no_authority`
- package_eligible(패키지 적격): `False`
- positive_clue(긍정 단서): `True`
- selected route(선택 라우트): `hd002__score_plus_0p02_점수_0_02_추가___hb_rebalance_h2_m0p26__hb_oos_profit_density_bridge__rf9_l20_n192`
- OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6): `57.998` / `1.1526564454` / `1.3893129771` / `3.398`
- delta vs GZ(기준 GZ 대비 차이): net `12.638`, PF `0.0332644601`, cost0.6 `12.338`, density `0.0076335878`
- strict_candidate_count(엄격 후보 수): `0`
- next_run_id(다음 실행 ID): `run364HF_train_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HE/he_review_summary.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HE/input_manifest.csv
- kpi_review_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HE/he_delta_attribution.csv
- package_boundary_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HE/he_package_decision.csv
- next_action_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HE/he_hf_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HE/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HE/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HE/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
