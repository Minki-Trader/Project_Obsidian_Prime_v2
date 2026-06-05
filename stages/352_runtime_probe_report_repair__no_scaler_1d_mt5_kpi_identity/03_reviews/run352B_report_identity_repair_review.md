# run352B Report Identity Repair Review(352B 보고서 정체성 수리 검토)

- run_id(실행 ID): `run352B_repair_no_scaler_1d_mt5_report_identity_reuse_outputs_without_db_v1`
- source_run_id(원천 실행 ID): `run351C_execute_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db_v1`
- status(상태): `completed_stage352B_report_identity_repaired_existing_mt5_reports_recovered_no_selection`
- judgment(판정): `negative_runtime_probe_report_recovered_validation_positive_oos_negative_high_drawdown_no_selection`
- decision(결정): `stage352B_open_stage353A_trade_shape_offensive_rebuild_from_density_ok_runtime_parity`
- gates(게이트): `8/8`

## KPI(핵심 성과 지표)

- validation(검증): net_profit(순수익) `241.59`, PF(수익 팩터) `1.09`, trades(거래 수) `749`, DD(낙폭) `63.95`.
- OOS(표본외): net_profit(순수익) `-200.11`, PF(수익 팩터) `0.92`, trades(거래 수) `564`, DD(낙폭) `65.34`.
- combined(합산): net_profit(순수익) `41.48`, PF(수익 팩터) `1.0079426019`, expectancy(기대값) `0.0315917746`, recovery_factor(회복 계수) `0.1107935575`, trades(거래 수) `1313`, trade_density(거래 밀도) `4.1815286624`.
- long/short balance(롱/숏 균형): `700/613`.

Action(행동): Stage351C(351C 실행)의 실제 `POPv2` tester report(테스터 보고서)를 수집하고 KPI(핵심 성과 지표)를 다시 산출했다.

Effect(효과): report identity blocker(보고서 정체성 차단)는 해소됐고, 성과 판정은 OOS 손실과 높은 drawdown(낙폭) 때문에 no_selection(선택 없음)으로 닫는다.

claim_boundary(주장 경계): `runtime_probe_report_repair_completed_proxy_mt5_diff_recorded_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`
