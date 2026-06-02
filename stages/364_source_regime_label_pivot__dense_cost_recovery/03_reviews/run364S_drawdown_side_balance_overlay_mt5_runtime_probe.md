# run364S Drawdown Side Balance Overlay MT5 Runtime Probe(364S 낙폭 방향 균형 오버레이 온엑스 MT5 런타임 탐침)

## Summary(요약)

- run_id(실행 ID): `run364S_execute_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1`
- status(상태): `completed_stage364S_drawdown_side_balance_overlay_mt5_runtime_probe_executed_review_required_no_authority`
- judgment(판정): `mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_authority`
- gates(게이트): `9/9`
- attempts(시도): `1`
- runtime_completed_rows(런타임 완료 수): `1`
- report_usable_rows(보고서 사용 가능 수): `1`
- matched_rows(일치 수): `17428`
- mismatch_rows(불일치 수): `0`
- external_verification_status(외부 검증 상태): `completed(완료)`
- next_run(다음 실행): `run364T_review_drawdown_side_balance_overlay_mt5_runtime_probe_without_db_v1`

## Runtime Read(런타임 판독)

- comparison_status(비교 상태): `completed_full_proxy_mt5_parity_reached_feature_last`
- expected_rows(예상 수): `17428`
- ready_model_rows(준비 모델 수): `17428`
- visited_expected_rows(방문 예상 수): `17428`
- unvisited_expected_rows(미방문 예상 수): `0`
- max_abs_probability_diff(최대 절대 확률 차이): `5.965400001750609e-08`
- net_profit(순수익): `928.89`
- profit_factor(수익 팩터): `1.34`
- trade_count(거래수): `935`
- expectancy(기대값): `0.99`
- recovery_factor(회복 계수): `4.59`
- max_drawdown_amount(최대 낙폭 금액): `202.3`
- max_drawdown_percent(최대 낙폭 퍼센트): `33.3`
- long_short_balance(롱/숏 균형): `935 long / 0 short(롱/숏)`

## Proxy vs MT5(프록시 대 MT5)

- expected_net_profit(예상 순수익): `725.227`
- actual_mt5_net_profit(실제 MT5 순수익): `928.89`
- net_profit_diff_actual_minus_expected(실제-예상 순수익 차이): `203.663`
- expected_trade_count(예상 거래수): `935`
- actual_mt5_trade_count(실제 MT5 거래수): `935`
- trade_count_diff_actual_minus_expected(실제-예상 거래수 차이): `0.0`

Action(행동): run364R(364R 실행) ONNX runtime package(온엑스 런타임 포장)를 MT5 Strategy Tester(MT5 전략 테스터)에서 실행하거나 blocker(차단 사유)를 기록했다.

Effect(효과): proxy expected value(프록시 예상값), probability parity(확률 동등성), MT5 KPI(MT5 핵심 성과 지표)를 분리해 다음 review/repair(검토/수리) 판단의 입력으로 남긴다.

## Evidence(근거)

- execution result(실행 결과): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364S/mt5_execution_result.json`
- runtime summary(런타임 요약): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364S/drawdown_side_balance_overlay_mt5_probe_summary.csv`
- probability diff(확률 차이): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364S/probability_runtime_difference.csv`
- proxy-MT5 diff(프록시-MT5 차이): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364S/proxy_mt5_runtime_difference.csv`
- tester reports(테스터 보고서): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364S/strategy_tester_report_records.json`
- runtime identity(런타임 정체성): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364S/runtime_identity.csv`

## Boundary(경계)

run364S(364S 실행)은 runtime_probe attempt(런타임 탐침 시도)다. operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
