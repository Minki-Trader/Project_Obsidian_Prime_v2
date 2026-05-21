# Stage267 run267BO Aggressive Second Tranche Cross-period MT5 Execution(공격형 2차 묶음 확장 기간 MT5 실행)

## Summary(요약)

- run_id(실행 ID): `run267BO_stage267_aggressive_second_tranche_cross_period_mt5_execution_v1`
- source_run(원천 실행): `run267BN_stage267_aggressive_second_tranche_cross_period_materialization_v1`
- status(상태): `run267BO_aggressive_second_tranche_cross_period_mt5_batch_partial`
- attempts_executed(실행 시도): `4`
- kpi_records(KPI 기록): `3`
- blocked_or_gap_attempts(차단 또는 공백 시도): `1`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Action(행동): run267BN(267BN 실행)의 s264_aih(핵심 도전자) cross-period(확장 기간) attempt(시도) 4개를 MT5(MetaTrader 5, 메타트레이더5) Strategy Tester(전략 테스터)로 실행했다.
Effect(효과): anti_overconstraint_prune(과제약 제거)이 2023H2/2025H1/2025H2에서 버티는지, state_acceleration_interaction(상태 가속 상호작용)이 2025H1 대조군으로 유효한지 확인한다.

## KPI Snapshot(KPI 요약)

| variant(변형) | period(기간) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | max_DD%(최대 손실폭 %) |
| --- | --- | ---: | ---: | ---: | ---: |
| `anti_overconstraint_prune` | `2023H2` | 998.53 | 1.92 | 221 | 9.07 |
| `anti_overconstraint_prune` | `2025H1` | 113.39 | 1.08 | 372 | 22.44 |
| `anti_overconstraint_prune` | `2025H2` | 55.79 | 1.05 | 219 | 29.0 |

## Blocked / Gap Attempts(차단/공백 시도)

| attempt(시도) | variant(변형) | period(기간) | tester(테스터) | runtime(런타임) | report(보고서) | note(메모) |
| --- | --- | --- | --- | --- | --- | --- |
| `run267bn_04_s264_aih_state_acceleration_interaction_2025h1` | `state_acceleration_interaction` | `2025H1` | `blocked` | `blocked` | `completed` | trade_count=0; runtime_summary_exists=False; runtime_telemetry_exists=False |

## Boundary(경계)

- 이 실행은 research racing(연구 경주) 실행이며 candidate selection(후보 선택)이 아니다.
- balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질) 검토 전에는 좋은 후보라고 말하지 않는다.
- ONNX parity(ONNX 동등성)나 ONNX conversion(ONNX 변환)은 시작하지 않는다.

## Artifacts(산출물)

- execution_result(실행 결과): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BO/aggressive_second_tranche_cross_period_mt5_execution/execution_result.json`
- kpi_summary(KPI 요약): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BO/aggressive_second_tranche_cross_period_mt5_execution/kpi_summary.csv`
- profile_encoding_receipt(프로필 인코딩 영수증): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BO/aggressive_second_tranche_cross_period_mt5_execution/profile_encoding_receipt.csv`
- forensics(포렌식): `stages/267_adapter_research__baseline_candidate_racing_protocol/02_runs/run267BO/aggressive_second_tranche_cross_period_mt5_execution/backtest_forensics.csv`
- next_action(다음 행동): `run267BO_classify_state_acceleration_zero_trade_runtime_gap_before_balance_review`
