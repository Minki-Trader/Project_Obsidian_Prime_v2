# run364HF Near-Miss Profit/PF Lift Switch Router(근접 실패 수익/PF 리프트 전환 라우터)

Created(생성): 2026-06-08T11:27:05Z

Action(행동): HD dual-surface router(HD 이중 표면 라우터)의 source row neighborhood(원천 행 이웃)를 다시 replay(재생)하고, validation-derived micro veto(검증 유래 미세 차단)를 각 라우트에 적용했습니다.

Effect(효과): HD near miss(HD 근접 실패)를 OOS net/PF/cost0.6(표본외 순수익/PF/비용0.6) 목표 위로 올릴 수 있는지 보되, OOS-only deletion(표본외 전용 삭제)과 runtime authority(런타임 권위) 주장을 차단합니다.

- judgment(판정): `positive_proxy_near_miss_profit_pf_lift_switch_router_candidate_review_required_no_authority`
- selected_route_variant_id(선택 라우트 변형 ID): `hf__veto_open_hour_pflat_sl_gap__mc2__sfm18p0__hd002__score_plus_0p02_점수_0_02_추가___hb_rebalance_h2_m0p26__hb_oos_profit_density_bridge__rf9_l20_n192`
- selected_parent_route(선택 상위 라우트): `hd002__score_plus_0p02_점수_0_02_추가___hb_rebalance_h2_m0p26__hb_oos_profit_density_bridge__rf9_l20_n192`
- selected_veto_policy(선택 차단 정책): `open_hour+pflat_bin+short_long_gap_bin(진입 시간+평탄확률 구간+숏롱차 구간)`
- selected_veto_rule(선택 차단 규칙): key `open_hour|pflat_bin|sl_gap_bin`, min_count `2`, sum_floor `-18.0`
- OOS net/PF/density/cost0.6(표본외 순수익/PF/밀도/비용0.6): `78.188` / `1.2173488818` / `1.3740458015` / `24.188`
- combined net/density/cost0.9(합산 순수익/밀도/비용0.9): `223.948` / `1.3025477707` / `-21.452`
- delta vs HD(HD 대비 차이): OOS net `20.19`, PF `0.0646924364`, cost0.6 `20.79`, OOS density `-0.0152671756`, combined density `-0.0191082803`, combined cost0.9 `65.015`
- veto removed total/OOS(차단 제거 전체/표본외): `6` / `2`
- strict_candidate_count(엄격 후보 수): `216`
- source_onnx_smoke_pass_rows(원천 ONNX 스모크 통과 행): `2`
- next_run_id(다음 실행 ID): `run364HG_review_h17_oos108_pf125_near_miss_profit_pf_lift_switch_router_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HF/hf_surface.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HF/input_manifest.csv
- source_neighborhood_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HF/hf_source_neighborhood_audit.csv
- kpi_contract_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HF/hf_surface.csv
- validation_veto_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HF/selected_hf_veto_groups.csv
- data_integrity_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HF/data_integrity_audit.csv
- source_onnx_smoke_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HF/source_onnx_smoke_report.csv
- no_trade_splitting_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HF/selected_hf_trade_tape.csv
- skill_receipt_lint: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HF/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HF/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HF/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
