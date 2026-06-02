# run364G Timestamp Context ONNX MT5 Runtime Probe(364G 시점 문맥 ONNX MT5 런타임 탐침)

## Summary(요약)

- run_id(실행 ID): `run364G_execute_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`
- status(상태): `completed_stage364G_timestamp_context_onnx_mt5_runtime_probe_executed_review_required_no_authority`
- judgment(판정): `mt5_runtime_probe_outputs_available_proxy_diff_review_required_no_authority`
- gates(게이트): `8/8`
- attempts(시도): `1`
- runtime_completed_rows(런타임 완료 행): `1`
- matched_rows(일치 행): `472`
- mismatch_rows(불일치 행): `0`
- external_verification_status(외부 검증 상태): `completed(완료)`
- next_run(다음 실행): `run364H_review_timestamp_context_onnx_mt5_runtime_probe_without_db_v1`

## Runtime Read(런타임 판독)

- comparison_status(비교 상태): `completed_overlap_proxy_mt5_parity_unvisited_expected_rows_remain`
- expected_rows(예상 행): `1114`
- ready_model_rows(준비 모델 행): `472`
- visited_expected_rows(방문 예상 행): `472`
- unvisited_expected_rows(미방문 예상 행): `642`
- max_abs_probability_diff(최대 절대 확률 차이): `4.768760000217753e-07`
- first_ready_bar_time(첫 준비 봉 시간): `2025.10.01 16:55:00`
- last_ready_bar_time(마지막 준비 봉 시간): `2026.04.13 20:05:00`
- net_profit(순수익): `-230.65`
- profit_factor(수익 팩터): `0.78`
- trade_count(거래수): `66`
- expectancy(기대값): `-3.49`
- recovery_factor(회복 계수): `-0.39`
- max_drawdown_amount(최대 낙폭 금액): `586.61`

Effect(효과): overlap parity(겹친 구간 동등성)는 통과했지만, MT5 KPI(MT5 핵심 성과 지표)는 negative(음수)라 운영 후보가 아니다.

## Action(행동)

run364F(364F 실행)의 ONNX runtime probe package(ONNX 런타임 탐침 패키지)를 MT5 Strategy Tester(MT5 전략 테스터)에 실행 시도했다.
Effect(효과): 성공하면 proxy-MT5 diff(프록시-MT5 차이)를 얻고, 실패하면 정확한 blocker(차단 사유)를 다음 repair/review(수리/검토)로 넘긴다.

## Evidence(근거)

- execution result(실행 결과): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364G/mt5_execution_result.json`
- runtime summary(런타임 요약): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364G/timestamp_context_onnx_mt5_probe_summary.csv`
- proxy-MT5 diff(프록시-MT5 차이): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364G/proxy_mt5_runtime_difference.csv`
- tester reports(테스터 보고서): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364G/strategy_tester_report_records.json`
- runtime identity(런타임 정체성): `stages/364_source_regime_label_pivot__dense_cost_recovery/02_runs/run364G/runtime_identity.csv`

## Boundary(경계)

run364G(364G 실행)는 runtime_probe attempt(런타임 탐침 시도)다. operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
