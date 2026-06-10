# run364HG Near-Miss Profit/PF Lift Review(근접 실패 수익/PF 리프트 검토)

Created(생성): 2026-06-08T11:33:21Z

Action(행동): HF strict proxy(HF 엄격 프록시)를 KPI(핵심 성과 지표), veto attribution(차단 귀속), package boundary(패키지 경계), runtime capability gap(런타임 기능 누락)으로 검토했습니다.

Effect(효과): 수익/PF 개선 단서는 보존하지만, 현재 EA(전문가 자문)가 probability-bin veto(확률 구간 차단)를 그대로 표현하지 못하므로 package(패키지)는 열지 않습니다.

- judgment(판정): `positive_proxy_no_package_hf_strict_pass_runtime_capability_gap_no_authority`
- package_eligible(패키지 적격): `False`
- runtime_capability_gap(런타임 기능 누락): `True`
- selected_route_variant_id(선택 라우트 변형 ID): `hf__veto_open_hour_pflat_sl_gap__mc2__sfm18p0__hd002__score_plus_0p02_점수_0_02_추가___hb_rebalance_h2_m0p26__hb_oos_profit_density_bridge__rf9_l20_n192`
- selected_veto_policy(선택 차단 정책): `open_hour+pflat_bin+short_long_gap_bin(진입 시간+평탄확률 구간+숏롱차 구간)`
- OOS net/PF/density/cost0.6(표본외 순수익/PF/밀도/비용0.6): `78.188` / `1.2173488818` / `1.3740458015` / `24.188`
- combined density/cost0.9(합산 밀도/비용0.9): `1.3025477707` / `-21.452`
- next_run_id(다음 실행 ID): `run364HH_materialize_h17_oos108_pf125_near_miss_profit_pf_lift_runtime_capability_inputs_without_db_v1`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HG/hg_review_summary.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HG/input_manifest.csv
- kpi_review_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HG/hg_review_summary.csv
- veto_attribution_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HG/hg_veto_attribution.csv
- package_boundary_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HG/hg_package_decision.csv
- runtime_capability_gap_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HG/hg_runtime_capability_gap.csv
- next_action_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HG/hg_hh_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HG/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HG/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HG/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
