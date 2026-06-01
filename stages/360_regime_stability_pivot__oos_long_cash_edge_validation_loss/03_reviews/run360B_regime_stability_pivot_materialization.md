# run360B Regime Stability Pivot Materialization(360B 국면 안정성 전환 구체화)

- run_id(실행 ID): `run360B_materialize_regime_stability_pivot_inputs_without_db_v1`
- parent_run_id(부모 실행 ID): `run360A_design_regime_stability_pivot_without_db_v1`
- next_run_id(다음 실행 ID): `run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1`
- status(상태): `completed_stage360B_regime_stability_pivot_inputs_materialized_review_required_no_selection_no_mt5`
- judgment(판정): `report_derived_filter_scorecards_materialized_review_required_no_operating_claim`
- gate_result(게이트 결과): `10/10`
- claim_boundary(주장 경계): `research_development_materialization_only_report_derived_filter_scorecards_no_new_model_training_no_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

## Current Truth(현재 진실)

Action(행동): Stage359B MT5 report(359B MT5 보고서) 4개를 trade-level records(거래 단위 기록)와 filter scorecard(필터 점수표)로 구체화했다.

Effect(효과): Stage360(360단계)을 바로 새 후보 선택(candidate selection, 후보 선택)으로 밀지 않고, `run360C` review(검토)에서 작은 필터 단위로 분기 판단할 수 있다.

## Materialized Evidence(구체화 근거)

- source_reports(원천 보고서): `4`
- trade_level_records(거래 단위 기록): `3215`
- filter_scorecard_rows(필터 점수표 행): `26`
- feasibility_counts(구체화 가능성 집계): `{"blocked_requires_label_input_build": 2, "blocked_requires_regime_feature_join": 1, "materialized_diagnostic_controls": 1, "materialized_diagnostic_only": 2, "materialized_report_derived": 2, "partial_materialized_meta_label_seed_only": 1, "partial_materialized_requires_feature_regime_buckets": 1, "partial_materialized_trade_level_cost_stress": 1, "partial_requires_bar_level_signal_merge": 1}`
- Tier A separate(Tier A 분리): `materialized_report_derived(보고서 파생 구체화)`
- Tier B separate(Tier B 분리): `missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)`
- Tier A+B combined(Tier A+B 합산): `out_of_scope_by_claim_no_combined_runtime(주장 범위 밖, 합산 런타임 없음)`

## Snapshot(스냅샷)

- best_oos_rule_id(최고 OOS, 표본외 규칙 ID): `s360_r03_q05_no_late`
- best_oos_net_profit(최고 OOS, 표본외 순수익): `305.66`
- best_oos_profit_factor(최고 OOS, 표본외 수익 팩터): `1.1194128977`
- q05_long_cash_validation_net(검증 q05 롱/현금장 순수익): `-56.89`
- q05_long_cash_oos_net(표본외 q05 롱/현금장 순수익): `254.86`
- q05_long_cash_oos_trade_density(표본외 q05 롱/현금장 일별 거래수): `3.3358778626`
- q05_long_cash_oos_cost_0_30(표본외 q05 롱/현금장 +0.30 비용 생존): `yes`

## Boundary(경계)

Action(행동): closed trade filter(종료 거래 필터)를 적용했다.

Effect(효과): 이는 signal sanity check(신호 점검)와 review queue(검토 대기열)로만 쓰며, position lifecycle replay(포지션 생명주기 재생)나 MT5 Strategy Tester result(MT5 전략 테스터 결과)를 대체하지 않는다.

No operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), or goal achieve(목표 달성) claim(주장)은 없다.

## Next Action(다음 행동)

Action(행동): `run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1`에서 scorecard(점수표)를 검토한다.

Effect(효과): validation loss(검증 손실), OOS long/cash clue(표본외 롱/현금장 단서), cost fragility(비용 취약성)를 분리해서 proxy(프록시) 또는 MT5 replay(MT5 재생)로 보낼지 결정한다.
