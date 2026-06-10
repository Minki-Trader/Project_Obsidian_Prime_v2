# run364HH Runtime Capability Input Materialization(런타임 기능 입력 물질화)

Created(생성): 2026-06-08T11:52:36Z

Action(행동): HG review(HG 검토)가 요청한 runtime capability inputs(런타임 기능 입력)을 contract(계약), expected tape(예상 테이프), source model manifest(원천 모델 목록), veto rule manifest(차단 규칙 목록)로 물질화했습니다.

Effect(효과): 다음 `run364HI_implement_h17_oos108_pf125_probability_bin_veto_runtime_support_without_db_v1`에서 EA(전문가 자문)가 어떤 ONNX(온엑스) 모델과 probability-bin veto(확률 구간 차단)를 재현해야 하는지 다시 해석하지 않아도 됩니다.

- judgment(판정): `materialization_completed_runtime_capability_inputs_probability_bin_veto_support_required_no_authority`
- selected_route_variant_id(선택 라우트 변형 ID): `hf__veto_open_hour_pflat_sl_gap__mc2__sfm18p0__hd002__score_plus_0p02_점수_0_02_추가___hb_rebalance_h2_m0p26__hb_oos_profit_density_bridge__rf9_l20_n192`
- selected_veto_policy(선택 차단 정책): `open_hour+pflat_bin+short_long_gap_bin(진입 시간+평탄확률 구간+숏롱차 구간)`
- veto_key_fields(차단 키 필드): `open_hour|pflat_bin|sl_gap_bin`
- OOS net/profit factor/density/cost0.6(표본밖 순수익/수익 팩터/거래 밀도/비용0.6): `78.188` / `1.2173488818` / `1.3740458015` / `24.188`
- expected_tape_rows(예상 테이프 행): `409`
- veto_rule_count(차단 규칙 수): `2`
- source_model_count(원천 모델 수): `2`
- runtime_package(런타임 패키지): `not_opened`
- next_run_id(다음 실행 ID): `run364HI_implement_h17_oos108_pf125_probability_bin_veto_runtime_support_without_db_v1`

Key Artifacts(핵심 산출물):

- runtime_capability_contract(런타임 기능 계약): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/runtime_capability_contract.csv`
- source_model_runtime_manifest(원천 모델 런타임 목록): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/source_model_runtime_manifest.csv`
- veto_rule_manifest(차단 규칙 목록): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/veto_rule_manifest.csv`
- expected_trade_tape(예상 거래 테이프): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/expected_trade_tape.csv`
- runtime_parity_contract(런타임 동등성 계약): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/runtime_parity_contract.json`

Gates(게이트):

- scope_completion_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/runtime_capability_contract.csv
- input_lineage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/input_manifest.csv
- expected_tape_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/expected_trade_tape.csv
- source_model_manifest_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/source_model_runtime_manifest.csv
- veto_rule_manifest_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/veto_rule_manifest.csv
- runtime_capability_contract_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/runtime_capability_contract.csv
- runtime_parity_boundary_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/runtime_parity_contract.json
- next_action_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/hh_hi_queue.csv
- receipt_coverage_gate: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/run_evidence_receipt.json
- required_gate_coverage_audit: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/required_gate_coverage_audit.csv
- final_claim_guard: passed -> stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364HH/claim_boundary_receipt.json

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
