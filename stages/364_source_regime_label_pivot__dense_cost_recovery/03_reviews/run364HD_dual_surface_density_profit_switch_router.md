# run364HD Dual-Surface Density-Profit Switch Router(이중 표면 밀도-수익 전환 라우터)

Created(생성): 2026-06-08T10:52:17Z

Action(행동): GZ density-cost anchor(GZ 밀도-비용 기준)를 기본 거래 기록으로 두고, HB target-profit surface(HB 목표 수익 표면)를 재생한 뒤 겹치지 않는 위치에만 fallback(대체 진입)으로 붙였습니다.

Effect(효과): HB 단독 교체처럼 밀도를 크게 잃는지, 또는 GZ 기준을 지키면서 OOS profit/PF/cost0.6(표본외 수익/수익 팩터/비용0.6)을 복구하는지 분리해서 봅니다.

- judgment(판정): `inconclusive_dual_surface_density_profit_switch_router_no_strict_pass_review_required_no_authority`
- selected_route_variant_id(선택 라우트 변형 ID): `hd002__score_plus_0p02_점수_0_02_추가___hb_rebalance_h2_m0p26__hb_oos_profit_density_bridge__rf9_l20_n192`
- selected_route_policy(선택 라우트 정책): `score_plus_0p02(점수 0.02 추가)`
- OOS net/PF/density/cost0.6(표본외 순수익/수익 팩터/밀도/비용0.6): `57.998` / `1.1526564454` / `1.3893129771` / `3.398`
- combined net/density/cost0.9(합산 순수익/밀도/비용0.9): `162.533` / `1.321656051` / `-86.467`
- delta vs GZ(기준 GZ 대비 차이): OOS net `12.638`, PF `0.0332644601`, cost0.6 `12.338`, OOS density `0.0076335878`, combined density `0.0159235669`, combined cost0.9 `-0.136`
- fallback added/skipped(대체 추가/겹침 건너뜀): `5` / `33`
- strict_candidate_count(엄격 후보 수): `0`
- source_onnx_smoke_pass_rows(원천 ONNX 스모크 통과 행): `2`
- next_run_id(다음 실행 ID): `run364HE_review_h17_oos108_pf125_dual_surface_density_profit_switch_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HD/hd_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HD/input_manifest.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HD/data_integrity_audit.csv
- source_model_artifact_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HD/source_model_artifact_manifest.csv
- source_onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HD/source_onnx_smoke_report.csv
- candidate_surface_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HD/hd_surface.csv
- strict_contract_decision_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HD/hd_he_queue.csv
- no_trade_splitting_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HD/selected_hd_trade_tape.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HD/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HD/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HD/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
